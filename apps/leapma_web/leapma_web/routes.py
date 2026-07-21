"""HTTP routes — coach-first + Python track (Boot.dev-style chapters)."""

from __future__ import annotations

import re

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
    "学 Python 基础：会用 print",
    "Python：写几个小脚本输出",
    "职场补 Python 入门",
]


def _uid() -> str:
    if "user_id" not in session:
        session["user_id"] = db.create_user(is_paid=False)
    return session["user_id"]


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


def _continue_target(user_id: str) -> tuple[str, str]:
    """Return (url, title) for continue CTA."""
    passed = db.list_passed_lessons(user_id, "python")
    ch1 = content.load_chapter("py-01")
    for lesson in ch1.get("lessons") or []:
        if lesson["id"] not in passed and not lesson.get("locked"):
            return (
                url_for(
                    "growth.lesson_play",
                    chapter_id="py-01",
                    lesson_id=lesson["id"],
                ),
                f"继续：{ch1['title']} · {lesson['title']}",
            )
    last = db.latest_attempted_lesson(user_id, "python")
    if last:
        cid, lid = last
        lesson = content.get_lesson(cid, lid)
        title = lesson["title"] if lesson else lid
        return (
            url_for("growth.lesson_play", chapter_id=cid, lesson_id=lid),
            f"回到：{title}",
        )
    return (
        url_for("growth.chapter_view", chapter_id="py-01"),
        "开始：Python 第 1 章",
    )


@bp.get("/dashboard")
@bp.get("/me")
def dashboard():
    uid = _uid()
    display_name = (session.get("display_name") or "").strip() or "游客"
    passed = db.list_passed_lessons(uid, "python")
    chapter_rows = []
    for meta in content.list_chapters():
        ch = content.load_chapter(meta["id"])
        lessons = [x for x in (ch.get("lessons") or []) if not x.get("locked")]
        total = len(lessons) if meta["status"] == "ready" else 0
        n_pass = sum(1 for x in lessons if x["id"] in passed)
        if meta["status"] != "ready":
            pct = 0
            pct_label = "未开放"
        elif total == 0:
            pct = 0
            pct_label = "0%"
        else:
            pct = int(round(100 * n_pass / total))
            pct_label = f"{pct}%"
        chapter_rows.append(
            {
                "id": meta["id"],
                "title": meta["title"],
                "status": meta["status"],
                "passed": n_pass,
                "total": total if meta["status"] == "ready" else 0,
                "pct": pct,
                "pct_label": pct_label,
                "url": url_for("growth.chapter_view", chapter_id=meta["id"]),
            }
        )
    continue_url, continue_title = _continue_target(uid)
    gs = db.latest_session_for_user(uid)
    progress_line = None
    if gs and (gs.progress_note or gs.next_step or gs.feedback_body):
        if gs.progress_note:
            progress_line = f"最近进展：{gs.progress_note[:120]}"
        elif gs.next_step:
            progress_line = f"当前下一步：{gs.next_step[:120]}"
        else:
            progress_line = "你已开始一轮练习；继续推进章节即可。"
    return render_template(
        "dashboard.html",
        guest_id_short=uid[:8],
        display_name=display_name,
        chapter_rows=chapter_rows,
        continue_url=continue_url,
        continue_title=continue_title,
        progress_line=progress_line,
    )


@bp.post("/dashboard/name")
def dashboard_name():
    _uid()
    name = (request.form.get("display_name") or "").strip()[:32]
    session["display_name"] = name
    flash("显示名已更新。" if name else "已恢复为「游客」。")
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
            goal_intent="学 Python 基础：会用 print",
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
                flash("提交判定前请先写下代码。")
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
                    if lesson_id == "py-01-l3":
                        return redirect(url_for("growth.progress"))
                    if nxt:
                        nch, nl = nxt
                        nlesson = content.get_lesson(nch, nl)
                        if nlesson and nlesson.get("locked"):
                            flash("下一章仍是骨架占位；你可回顾进展或重练第 1 章。")
                            return redirect(
                                url_for("growth.chapter_view", chapter_id=chapter_id)
                            )
                        return redirect(
                            url_for("growth.lesson_play", chapter_id=nch, lesson_id=nl)
                        )

    return render_template(
        "lesson.html",
        chapter=ch,
        lesson=lesson,
        grade=grade,
        run_demo=run_demo,
        attempt_text=request.form.get("attempt_text", "") if request.method == "POST" else "",
    )
