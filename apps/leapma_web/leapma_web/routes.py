"""HTTP routes — coach-first + Python track (Boot.dev-style chapters)."""

from __future__ import annotations

import re

from datetime import date

from flask import (
    Blueprint,
    current_app,
    flash,
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


def _uid() -> str:
    if "user_id" not in session:
        session["user_id"] = db.create_user(is_paid=False)
    return session["user_id"]


def _is_logged_in() -> bool:
    return bool(session.get("logged_in"))


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


@bp.get("/dashboard")
@bp.get("/me")
def dashboard():
    uid = _uid()
    logged_in = _is_logged_in()
    user = db.get_user(uid) if logged_in else None
    display_name = (session.get("display_name") or "").strip()
    if not display_name and user and user.display_name:
        display_name = user.display_name
        session["display_name"] = display_name
    if not display_name:
        display_name = "游客"

    chapter_rows = []
    for meta in content.list_chapters():
        n_pass, total = _chapter_progress(uid, meta["id"], meta["status"])
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
        chapter_rows.append(
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
    continue_url, continue_title, continue_lesson = _continue_target(uid)
    status_line = _current_status_line(uid)
    return render_template(
        "dashboard.html",
        guest_id_short=uid[:8],
        display_name=display_name,
        logged_in=logged_in,
        username=(user.username if user else None),
        chapter_rows=chapter_rows,
        continue_url=continue_url,
        continue_title=continue_title,
        continue_lesson=continue_lesson,
        status_line=status_line,
        coach_tip=_coach_tip(uid),
    )


@bp.post("/dashboard/name")
def dashboard_name():
    uid = _uid()
    name = (request.form.get("display_name") or "").strip()[:32]
    session["display_name"] = name
    if _is_logged_in():
        db.set_user_display_name(uid, name or None)
    flash("显示名已更新。" if name else "已恢复为「游客」。")
    return redirect(url_for("growth.dashboard"))


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

    return render_template(
        "lesson.html",
        chapter=ch,
        lesson=lesson,
        grade=grade,
        run_demo=run_demo,
        attempt_text=request.form.get("attempt_text", "") if request.method == "POST" else "",
    )
