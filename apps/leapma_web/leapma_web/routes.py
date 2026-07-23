"""HTTP routes — coach-first + Python track (Boot.dev-style chapters)."""

from __future__ import annotations

import re

from datetime import date, datetime

from flask import (
    Blueprint,
    current_app,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from leapma_web import db
from leapma_web import content_loader as content
from leapma_web.entitlement import ensure_core_allowed
from leapma_web.llm import get_provider
from leapma_web.orientation import is_extremely_vague_goal
from leapma_web.rules_feedback import grade_lesson
from leapma_web.validation import validate_feedback, validate_progress_note

bp = Blueprint("growth", __name__)

_PYTHON_GOAL_RE = re.compile(r"python|蟒蛇|\bpy\b|学\s*py", re.I)

PYTHON_CHIPS = [
    "学 Python 基础：变量与类型",
    "Python：函数与作用域入门",
    "职场补 Python 入门",
]

# 章级能力短标签（进度文案用，非问卷）
CHAPTER_CAPABILITY = {
    "py-01": "会用变量与类型",
    "py-02": "会写函数",
    "py-03": "懂作用域",
    "py-04": "导论",
    "py-05": "测试调试",
    "py-06": "计算",
    "py-07": "比较",
    "py-08": "循环",
    "py-09": "列表",
    "py-10": "字典",
    "py-11": "集合",
    "py-12": "错误处理",
    "py-13": "类型提示",
    "py-14": "综合练习",
    "py-15": "章末测验",
}

COACH_TIPS = [
    "模糊了就复习上一课，再回来继续。",
    "一次只练一小步；通过了再往下。",
    "提交判定比完美代码更重要——先动手。",
    "卡住超过十分钟？回头看教练提示。",
    "进度用「会不会」衡量，不看虚荣百分比。",
]

_VALID_CONCEPT_MODES = frozenset({"normal", "story"})
_CONCEPT_MODE_COOKIE = "concept_mode_default"
_CONCEPT_MODE_COOKIE_MAX_AGE = 365 * 24 * 3600


def _uid() -> str:
    if "user_id" not in session:
        session["user_id"] = db.create_user(is_paid=False)
    return session["user_id"]


def _is_logged_in() -> bool:
    return bool(session.get("logged_in"))


def _normalize_concept_mode(raw: str | None) -> str:
    m = (raw or "").strip().lower()
    return m if m in _VALID_CONCEPT_MODES else "normal"


def _get_concept_mode_default() -> str:
    """Resolve default concept mode (Plan B). Account wins when logged in."""
    if _is_logged_in():
        if "concept_mode_default" in session:
            return _normalize_concept_mode(session.get("concept_mode_default"))
        user = db.get_user(_uid())
        if user and user.concept_mode_default:
            mode = _normalize_concept_mode(user.concept_mode_default)
            session["concept_mode_default"] = mode
            return mode
        return "normal"
    if "concept_mode_default" in session:
        return _normalize_concept_mode(session.get("concept_mode_default"))
    cookie = request.cookies.get(_CONCEPT_MODE_COOKIE)
    if cookie:
        mode = _normalize_concept_mode(cookie)
        session["concept_mode_default"] = mode
        return mode
    return "normal"


def _attach_concept_mode_cookie(resp, mode: str):
    """Persist guest default preference in a cookie (optional but recommended)."""
    resp.set_cookie(
        _CONCEPT_MODE_COOKIE,
        mode,
        max_age=_CONCEPT_MODE_COOKIE_MAX_AGE,
        samesite="Lax",
        httponly=False,
    )
    return resp


def _set_concept_mode_default(mode: str) -> str:
    """Write default preference only (never called from in-lesson toggle)."""
    mode = _normalize_concept_mode(mode)
    session["concept_mode_default"] = mode
    if _is_logged_in():
        db.set_user_concept_mode_default(_uid(), mode)
    return mode


def _coach_tip(user_id: str) -> str:
    """Rotate one tip per calendar day (stable for same user)."""
    seed = sum(ord(c) for c in (user_id or "x")[:8]) + date.today().toordinal()
    return COACH_TIPS[seed % len(COACH_TIPS)]


def _sid() -> str | None:
    return session.get("growth_session_id")


def _require_gs():
    sid = _sid()
    if not sid:
        return None
    return db.get_session(sid)


def _is_python_goal(goal: str) -> bool:
    g = (goal or "").strip()
    if g in PYTHON_CHIPS:
        return True
    return bool(_PYTHON_GOAL_RE.search(g))


def _apply_orientation(gs_id: str, goal: str) -> str:
    """Return flask endpoint name for next hop."""
    if _is_python_goal(goal):
        ch = content.load_chapter("py-01")
        lesson = ch["lessons"][0]
        db.update_session(
            gs_id,
            goal_intent=goal,
            position_hint="初期赛道：Python。我们用章节动手路径，不填问卷。",
            probe_question=None,
            next_step=f"进入 {ch['title']} · {lesson['title']}",
            exercise_prompt=lesson["prompt"],
            stage="track",
        )
        session["track_id"] = "python"
        session["chapter_id"] = "py-01"
        session["lesson_id"] = lesson["id"]
        return "growth.track_home"

    provider = get_provider(current_app.config["LEAPMA_LLM_PROVIDER"])
    assist = provider.assist_orientation(goal)
    vague = is_extremely_vague_goal(goal)
    db.update_session(
        gs_id,
        goal_intent=goal,
        position_hint=assist.position_hint,
        probe_question=assist.probe_question if vague else None,
        next_step=assist.next_step,
        exercise_prompt=assist.exercise_prompt,
        stage="probe" if vague else "next_step",
    )
    return "growth.probe" if vague else "growth.next_step"


@bp.get("/")
def home():
    return render_template("home.html", chips=PYTHON_CHIPS)


@bp.post("/begin")
def begin():
    ensure_core_allowed("orientation", is_paid=db.user_is_paid(_uid()))
    goal = (request.form.get("goal_intent") or "").strip()
    if len(goal) < 2:
        flash("先用一句话告诉我：你想提升什么？")
        return render_template("home.html", chips=PYTHON_CHIPS)
    uid = _uid()
    sid = db.create_session(uid)
    session["growth_session_id"] = sid
    nxt = _apply_orientation(sid, goal)
    return redirect(url_for(nxt))


@bp.post("/start")
def start():
    ensure_core_allowed("orientation", is_paid=db.user_is_paid(_uid()))
    uid = _uid()
    sid = db.create_session(uid)
    session["growth_session_id"] = sid
    return redirect(url_for("growth.orient"))


@bp.route("/orient", methods=["GET", "POST"])
def orient():
    ensure_core_allowed("orientation", is_paid=db.user_is_paid(_uid()))
    gs = _require_gs()
    if not gs:
        return redirect(url_for("growth.home"))
    if request.method == "POST":
        goal = (request.form.get("goal_intent") or "").strip()
        if len(goal) < 2:
            flash("先用一句话告诉我：你想提升什么？")
            return render_template("orient.html", gs=gs, chips=PYTHON_CHIPS)
        nxt = _apply_orientation(gs.id, goal)
        return redirect(url_for(nxt))
    return render_template("orient.html", gs=gs, chips=PYTHON_CHIPS)


@bp.route("/probe", methods=["GET", "POST"])
def probe():
    ensure_core_allowed("orientation", is_paid=db.user_is_paid(_uid()))
    gs = _require_gs()
    if not gs or not gs.goal_intent:
        return redirect(url_for("growth.home"))
    if not gs.probe_question and request.method == "GET":
        db.update_session(gs.id, stage="next_step")
        return redirect(url_for("growth.next_step"))
    if request.method == "POST":
        action = request.form.get("action") or "skip"
        if action == "skip":
            db.update_session(gs.id, probe_answer=None, stage="next_step")
        else:
            ans = (request.form.get("probe_answer") or "").strip()
            hint = gs.position_hint or ""
            if ans:
                hint = f"{hint}\n你补充：{ans}"
            db.update_session(
                gs.id, probe_answer=ans or None, position_hint=hint, stage="next_step"
            )
        return redirect(url_for("growth.next_step"))
    return render_template("probe.html", gs=gs)


@bp.get("/next-step")
def next_step():
    ensure_core_allowed("orientation", is_paid=db.user_is_paid(_uid()))
    gs = _require_gs()
    if not gs or not gs.next_step:
        return redirect(url_for("growth.home"))
    return render_template("next_step.html", gs=gs)


@bp.route("/exercise", methods=["GET", "POST"])
def exercise():
    """Generic free-form exercise (non-track). Track uses /track/.../lesson."""
    ensure_core_allowed("action", is_paid=db.user_is_paid(_uid()))
    gs = _require_gs()
    if not gs or not gs.exercise_prompt:
        return redirect(url_for("growth.home"))
    if request.method == "POST":
        ensure_core_allowed("feedback", is_paid=db.user_is_paid(_uid()))
        attempt = (request.form.get("attempt_text") or "").strip()
        force_uncertain = request.form.get("force_uncertain") == "1"
        if not attempt:
            flash("写一小段就行——我们马上给你反馈。")
            return render_template("exercise.html", gs=gs)
        provider = get_provider(current_app.config["LEAPMA_LLM_PROVIDER"])
        raw = provider.feedback_on_attempt(
            goal_intent=gs.goal_intent or "",
            next_step=gs.next_step or "",
            exercise_prompt=gs.exercise_prompt or "",
            attempt_text=attempt,
            force_uncertain=force_uncertain,
        )
        fb = validate_feedback(raw)
        db.update_session(
            gs.id,
            attempt_text=attempt,
            feedback_body=fb.body,
            feedback_uncertain=1 if fb.uncertain else 0,
            feedback_rejected_codegen=1 if fb.rejected_codegen else 0,
            stage="feedback",
        )
        return redirect(url_for("growth.feedback"))
    return render_template("exercise.html", gs=gs)


@bp.get("/feedback")
def feedback():
    ensure_core_allowed("feedback", is_paid=db.user_is_paid(_uid()))
    gs = _require_gs()
    if not gs or not gs.feedback_body:
        return redirect(url_for("growth.exercise"))
    return render_template("feedback.html", gs=gs)


@bp.route("/progress", methods=["GET", "POST"])
def progress():
    ensure_core_allowed("progress", is_paid=db.user_is_paid(_uid()))
    gs = _require_gs()
    if not gs or not gs.feedback_body:
        return redirect(url_for("growth.home"))
    if request.method == "POST":
        ok, note = validate_progress_note(request.form.get("progress_note") or "")
        next_intent = (request.form.get("next_intent") or "").strip()
        if not ok:
            flash(note)
            return render_template("progress.html", gs=gs)
        if len(next_intent) < 4:
            flash("下次回来你想继续哪一小步？写一句就行。")
            return render_template("progress.html", gs=gs)
        db.update_session(
            gs.id,
            progress_note=note,
            next_intent=next_intent,
            stage="done",
        )
        return redirect(url_for("growth.done"))
    return render_template("progress.html", gs=gs)


@bp.get("/done")
def done():
    gs = _require_gs()
    if not gs or gs.stage != "done":
        return redirect(url_for("growth.home"))
    return render_template("done.html", gs=gs, unpaid=True)


# --- Guest dashboard / personal center ---


def _chapter_progress(user_id: str, chapter_id: str, status: str) -> tuple[int, int]:
    """Return (passed, total) for unlocked lessons; skeleton → (0, 0)."""
    if status != "ready":
        return 0, 0
    ch = content.load_chapter(chapter_id)
    lessons = [x for x in (ch.get("lessons") or []) if not x.get("locked")]
    passed = db.list_passed_lessons(user_id, "python")
    n_pass = sum(1 for x in lessons if x["id"] in passed)
    return n_pass, len(lessons)


def _chapter_num(chapter_id: str) -> str:
    try:
        return str(int(str(chapter_id).split("-", 1)[1]))
    except (IndexError, ValueError):
        return chapter_id


def _continue_target(user_id: str) -> tuple[str, str, str | None]:
    """Return (url, cta_label, lesson_title) for continue CTA.

    Jumps to the next incomplete unlocked lesson on a ready chapter.
    """
    passed = db.list_passed_lessons(user_id, "python")
    for meta in content.list_chapters():
        if meta["status"] != "ready":
            continue
        ch = content.load_chapter(meta["id"])
        for lesson in ch.get("lessons") or []:
            if lesson.get("locked") or lesson["id"] in passed:
                continue
            cap = CHAPTER_CAPABILITY.get(meta["id"], "")
            n, total = _chapter_progress(user_id, meta["id"], meta["status"])
            label = f"继续学习 · 第{_chapter_num(meta['id'])}章 {n}/{total}"
            if cap:
                label = f"{label} · {cap}"
            return (
                url_for(
                    "growth.lesson_play",
                    chapter_id=meta["id"],
                    lesson_id=lesson["id"],
                ),
                label,
                lesson.get("title"),
            )
    last = db.latest_attempted_lesson(user_id, "python")
    if last:
        cid, lid = last
        lesson = content.get_lesson(cid, lid)
        title = lesson["title"] if lesson else lid
        return (
            url_for("growth.lesson_play", chapter_id=cid, lesson_id=lid),
            f"回到上一练 · {title}",
            title,
        )
    return (
        url_for("growth.chapter_view", chapter_id="py-01"),
        "开始学习 · 第1章 0/5 · 会用变量与类型",
        None,
    )


def _current_status_line(user_id: str) -> str:
    """一行状态：能力语言 + N/M。"""
    last_ready = None
    for meta in content.list_chapters():
        if meta["status"] != "ready":
            continue
        last_ready = meta
        n, total = _chapter_progress(user_id, meta["id"], meta["status"])
        cap = CHAPTER_CAPABILITY.get(meta["id"], "")
        ch_num = _chapter_num(meta["id"])
        if n < total:
            base = f"第{ch_num}章 {n}/{total}"
            return f"{base} · {cap}" if cap else base
    if last_ready:
        n, total = _chapter_progress(user_id, last_ready["id"], "ready")
        cap = CHAPTER_CAPABILITY.get(last_ready["id"], "")
        ch_num = _chapter_num(last_ready["id"])
        base = f"第{ch_num}章 {n}/{total}"
        if cap:
            return f"{base} · {cap}（已开放章已过）"
        return f"{base}（已开放章已过）"
    return "第1章 0/5 · 会用变量与类型（尚未开始）"


def _resolve_display_name(user: db.UserRecord | None) -> str:
    display_name = (session.get("display_name") or "").strip()
    if not display_name and user and user.display_name:
        display_name = user.display_name
        session["display_name"] = display_name
    return display_name or "游客"


def _ensure_guest_first_seen(user: db.UserRecord | None) -> str:
    """Guest first-seen: session, else users.created_at from guest row."""
    existing = (session.get("guest_first_seen") or "").strip()
    if existing:
        return existing
    stamp = ""
    if user and user.created_at:
        stamp = str(user.created_at)[:19]
    if not stamp:
        stamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    session["guest_first_seen"] = stamp
    return stamp


def _chapter_rows(user_id: str) -> list[dict]:
    rows = []
    for meta in content.list_chapters():
        n_pass, total = _chapter_progress(user_id, meta["id"], meta["status"])
        cap = CHAPTER_CAPABILITY.get(meta["id"], "")
        if meta["status"] != "ready":
            nm_label = "未开放"
            status_text = "尚未交付 · 诚实占位"
        elif total == 0:
            nm_label = "0/0"
            status_text = cap or ""
        else:
            nm_label = f"{n_pass}/{total}"
            status_text = cap
        rows.append(
            {
                "id": meta["id"],
                "title": meta["title"],
                "status": meta["status"],
                "passed": n_pass,
                "total": total,
                "nm_label": nm_label,
                "capability": status_text,
                "bar_pct": int(round(100 * n_pass / total)) if total else 0,
                "url": url_for("growth.chapter_view", chapter_id=meta["id"]),
            }
        )
    return rows


def _ready_chapter_summaries(user_id: str, limit: int = 3) -> list[str]:
    """第 1～N 章 N/M 摘要（仅 ready）。"""
    out: list[str] = []
    for meta in content.list_chapters():
        if len(out) >= limit:
            break
        if meta["status"] != "ready":
            continue
        n, total = _chapter_progress(user_id, meta["id"], meta["status"])
        out.append(f"第{_chapter_num(meta['id'])}章 {n}/{total}")
    return out


@bp.get("/dashboard")
def dashboard():
    """续学 + 章列表；个人信息仅摘要，完整设置在 /profile。"""
    uid = _uid()
    logged_in = _is_logged_in()
    user = db.get_user(uid) if logged_in else None
    display_name = _resolve_display_name(user)
    mode = _get_concept_mode_default()
    mode_label = "故事" if mode == "story" else "正常"
    continue_url, continue_title, continue_lesson = _continue_target(uid)
    return render_template(
        "dashboard.html",
        display_name=display_name,
        logged_in=logged_in,
        concept_mode_default=mode,
        concept_mode_label=mode_label,
        chapter_rows=_chapter_rows(uid),
        continue_url=continue_url,
        continue_title=continue_title,
        continue_lesson=continue_lesson,
        status_line=_current_status_line(uid),
        coach_tip=_coach_tip(uid),
    )


@bp.get("/me")
def me_redirect():
    """兼容旧入口：曾等同 Dashboard，现指向个人中心。"""
    return redirect(url_for("growth.profile"), code=302)


@bp.get("/profile")
def profile():
    """个人中心：昵称、时间、默认概念模式、进度、可选账号。"""
    uid = _uid()
    logged_in = _is_logged_in()
    user = db.get_user(uid)
    display_name = _resolve_display_name(user if logged_in else None)
    if logged_in and user and user.created_at:
        joined_at = str(user.created_at)[:19]
        joined_label = "注册时间"
    else:
        joined_at = _ensure_guest_first_seen(user)
        joined_label = "首次进入时间"
    continue_url, continue_title, continue_lesson = _continue_target(uid)
    return render_template(
        "profile.html",
        guest_id_short=uid[:8],
        display_name=display_name,
        logged_in=logged_in,
        username=(user.username if user and logged_in else None),
        joined_at=joined_at,
        joined_label=joined_label,
        concept_mode_default=_get_concept_mode_default(),
        track_name="Python 赛道",
        status_line=_current_status_line(uid),
        chapter_summaries=_ready_chapter_summaries(uid, 3),
        continue_url=continue_url,
        continue_title=continue_title,
        continue_lesson=continue_lesson,
    )


@bp.post("/profile/name")
def profile_name():
    uid = _uid()
    name = (request.form.get("display_name") or "").strip()[:32]
    session["display_name"] = name
    if _is_logged_in():
        db.set_user_display_name(uid, name or None)
    flash("显示名已更新。" if name else "已恢复为「游客」。")
    return redirect(url_for("growth.profile"))


@bp.post("/profile/concept-mode")
def profile_concept_mode():
    """方案 B 唯一写入点：保存默认概念模式。课内切换不得调用。"""
    mode = _set_concept_mode_default(request.form.get("concept_mode_default"))
    label = "故事" if mode == "story" else "正常"
    flash(f"默认概念模式已设为「{label}」。课内切换不会改动此项。")
    resp = make_response(redirect(url_for("growth.profile")))
    return _attach_concept_mode_cookie(resp, mode)


# 旧路径兼容：表单已迁到 /profile，POST 仍生效并跳转个人中心
@bp.post("/dashboard/name")
def dashboard_name():
    return profile_name()


@bp.post("/dashboard/concept-mode")
def dashboard_concept_mode():
    return profile_concept_mode()


def _bind_account(account_id: str, *, display_name: str | None = None) -> None:
    """Switch session to registered account; merge guest progress if any."""
    guest_id = session.get("user_id")
    if guest_id and guest_id != account_id and not session.get("logged_in"):
        db.merge_guest_into_user(guest_id, account_id)
    session["user_id"] = account_id
    session["logged_in"] = True
    if display_name is not None:
        session["display_name"] = display_name
    elif not session.get("display_name"):
        user = db.get_user(account_id)
        if user and user.display_name:
            session["display_name"] = user.display_name
    # Account preference wins over guest session/cookie.
    user = db.get_user(account_id)
    if user and user.concept_mode_default:
        session["concept_mode_default"] = _normalize_concept_mode(
            user.concept_mode_default
        )
    else:
        session["concept_mode_default"] = "normal"


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    username = (request.form.get("username") or "").strip()
    password = request.form.get("password") or ""
    display_name = (request.form.get("display_name") or "").strip()[:32]
    email = (request.form.get("email") or "").strip()[:255] or None
    if len(username) < 2 or len(username) > 32:
        flash("用户名请用 2～32 个字符。")
        return render_template("register.html")
    if len(password) < 6:
        flash("密码至少 6 位。")
        return render_template("register.html")
    try:
        uid = db.register_user(
            username=username,
            password_hash=generate_password_hash(password),
            display_name=display_name or username,
            email=email,
        )
    except ValueError as exc:
        flash(str(exc))
        return render_template("register.html")
    _bind_account(uid, display_name=display_name or username)
    flash("注册成功。游客进度已尽量并入账号；Dashboard 仍可不登录使用。")
    return redirect(url_for("growth.dashboard"))


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    username = (request.form.get("username") or "").strip()
    password = request.form.get("password") or ""
    user = db.get_user_by_username(username)
    if not user or not user.password_hash:
        flash("用户名或密码不对。")
        return render_template("login.html")
    if not check_password_hash(user.password_hash, password):
        flash("用户名或密码不对。")
        return render_template("login.html")
    _bind_account(user.id, display_name=user.display_name or user.username)
    flash("已登录。进度已关联到账号。")
    return redirect(url_for("growth.dashboard"))


@bp.post("/logout")
def logout():
    session.pop("logged_in", None)
    # Keep a fresh guest identity so Dashboard stays usable without wall.
    session["user_id"] = db.create_user(is_paid=False)
    session.pop("growth_session_id", None)
    session.pop("guest_first_seen", None)
    flash("已退出。你仍可游客身份继续练。")
    return redirect(url_for("growth.dashboard"))


# --- Python track (chapters) ---


@bp.get("/track/python")
def track_home():
    ensure_core_allowed("orientation", is_paid=db.user_is_paid(_uid()))
    if not _require_gs():
        # allow browse: create lightweight session
        sid = db.create_session(_uid())
        session["growth_session_id"] = sid
        db.update_session(
            sid,
            goal_intent="学 Python 基础：变量与类型",
            next_step="进入 Python 第 1 章",
            stage="track",
        )
    track = content.load_track()
    passed = db.list_passed_lessons(_uid(), "python")
    return render_template(
        "track.html",
        track=track,
        chapters=content.list_chapters(),
        passed=passed,
    )


@bp.get("/track/python/<chapter_id>")
def chapter_view(chapter_id: str):
    ensure_core_allowed("action", is_paid=db.user_is_paid(_uid()))
    try:
        ch = content.load_chapter(chapter_id)
    except KeyError:
        flash("章节不存在。")
        return redirect(url_for("growth.track_home"))
    passed = db.list_passed_lessons(_uid(), "python")
    return render_template("chapter.html", chapter=ch, passed=passed)


@bp.route("/track/python/<chapter_id>/<lesson_id>", methods=["GET", "POST"])
def lesson_play(chapter_id: str, lesson_id: str):
    ensure_core_allowed("action", is_paid=db.user_is_paid(_uid()))
    ensure_core_allowed("feedback", is_paid=db.user_is_paid(_uid()))
    lesson = content.get_lesson(chapter_id, lesson_id)
    if not lesson:
        flash("练习不存在。")
        return redirect(url_for("growth.track_home"))
    ch = content.load_chapter(chapter_id)
    gs = _require_gs()
    if not gs:
        sid = db.create_session(_uid())
        session["growth_session_id"] = sid
        gs = db.get_session(sid)

    grade = None
    run_demo = False
    if request.method == "POST":
        action = request.form.get("action") or "submit"
        attempt = (request.form.get("attempt_text") or "").strip()
        if action == "run":
            run_demo = True
            flash("Run 为 Demo 占位：真沙箱执行即将支持。请先用 Submit 做判定反馈。")
        else:
            if not attempt:
                flash("提交判定前请先作答。")
            else:
                grade = grade_lesson(lesson, attempt)
                db.upsert_lesson_progress(
                    _uid(),
                    "python",
                    chapter_id,
                    lesson_id,
                    status="passed" if grade.passed else "attempted",
                    last_attempt=attempt,
                    last_passed=grade.passed,
                )
                if gs:
                    db.update_session(
                        gs.id,
                        goal_intent=gs.goal_intent or "学 Python 基础",
                        next_step=f"{ch['title']} · {lesson['title']}",
                        exercise_prompt=lesson.get("prompt"),
                        attempt_text=attempt,
                        feedback_body=grade.body,
                        feedback_uncertain=0,
                        feedback_rejected_codegen=0,
                        stage="feedback" if grade.passed else "exercise",
                    )
                if grade and grade.passed:
                    nxt = content.next_lesson(chapter_id, lesson_id)
                    if nxt:
                        nch, nl = nxt
                        nlesson = content.get_lesson(nch, nl)
                        nmeta = next(
                            (c for c in content.list_chapters() if c["id"] == nch),
                            None,
                        )
                        locked_next = bool(nlesson and nlesson.get("locked"))
                        skeleton_next = bool(
                            nmeta and nmeta.get("status") != "ready"
                        )
                        if locked_next or skeleton_next:
                            flash(
                                "已开放章节的练习已打穿；第 4～15 章仍是骨架占位。"
                                "可回顾进展或重练第 1～3 章。"
                            )
                            return redirect(url_for("growth.progress"))
                        return redirect(
                            url_for("growth.lesson_play", chapter_id=nch, lesson_id=nl)
                        )
                    return redirect(url_for("growth.progress"))

    prev = content.prev_lesson(chapter_id, lesson_id)
    nxt = content.next_lesson(chapter_id, lesson_id)
    prev_url = (
        url_for("growth.lesson_play", chapter_id=prev[0], lesson_id=prev[1])
        if prev
        else None
    )
    next_url = None
    if nxt:
        nch, nl = nxt
        nlesson = content.get_lesson(nch, nl)
        nmeta = next((c for c in content.list_chapters() if c["id"] == nch), None)
        locked_next = bool(nlesson and nlesson.get("locked"))
        skeleton_next = bool(nmeta and nmeta.get("status") != "ready")
        if not locked_next and not skeleton_next:
            next_url = url_for("growth.lesson_play", chapter_id=nch, lesson_id=nl)

    # Plan B: first paint always from default; ignore ?mode= deep links.
    concept_mode_default = _get_concept_mode_default()
    initial_concept_mode = concept_mode_default
    story_mode_fallback = False
    if initial_concept_mode == "story" and not lesson.get("has_story"):
        initial_concept_mode = "normal"
        story_mode_fallback = True

    return render_template(
        "lesson.html",
        chapter=ch,
        lesson=lesson,
        grade=grade,
        run_demo=run_demo,
        attempt_text=request.form.get("attempt_text", "") if request.method == "POST" else "",
        prev_url=prev_url,
        next_url=next_url,
        concept_mode_default=concept_mode_default,
        initial_concept_mode=initial_concept_mode,
        story_mode_fallback=story_mode_fallback,
    )
