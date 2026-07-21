"""HTTP routes — SSR pages for GL-1…8 minimal path (coach-first, 方案 1)."""

from __future__ import annotations

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
from leapma_web.entitlement import ensure_core_allowed
from leapma_web.llm import get_provider
from leapma_web.orientation import is_extremely_vague_goal
from leapma_web.validation import validate_feedback, validate_progress_note

bp = Blueprint("growth", __name__)


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


def _apply_orientation(gs_id: str, goal: str) -> str:
    """Persist orientation; return next endpoint endpoint name: probe | next_step."""
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
    return render_template("home.html")


@bp.post("/begin")
def begin():
    """Single coach entry: one goal input → NextStep (probe only if extremely vague)."""
    ensure_core_allowed("orientation", is_paid=db.user_is_paid(_uid()))
    goal = (request.form.get("goal_intent") or "").strip()
    if len(goal) < 2:
        flash("先用一句话告诉我：你想提升什么？")
        return render_template("home.html")
    uid = _uid()
    sid = db.create_session(uid)
    session["growth_session_id"] = sid
    nxt = _apply_orientation(sid, goal)
    return redirect(url_for(nxt))


@bp.post("/start")
def start():
    """Legacy entry without goal — send to coach home input."""
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
            return render_template("orient.html", gs=gs)
        nxt = _apply_orientation(gs.id, goal)
        return redirect(url_for(nxt))
    return render_template("orient.html", gs=gs)


@bp.route("/probe", methods=["GET", "POST"])
def probe():
    ensure_core_allowed("orientation", is_paid=db.user_is_paid(_uid()))
    gs = _require_gs()
    if not gs or not gs.goal_intent:
        return redirect(url_for("growth.home"))
    # If we landed here without a suggested probe, skip straight to next step
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
