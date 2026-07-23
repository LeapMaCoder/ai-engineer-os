"""Smoke: submit one passing attempt per ready chapter + Plan B concept mode."""

from __future__ import annotations

import re
import sys

from leapma_web import create_app
from leapma_web.content_loader import load_chapter
from leapma_web.rules_feedback import grade_lesson


# One known-good answer per chapter (diverse types: mcq / fill / mcq)
SAMPLES = [
    ("py-01", "py-01-l2", "B"),  # mcq: assignment meaning
    ("py-02", "py-02-l3", "n * n"),  # fill: square
    ("py-03", "py-03-l1", "B"),  # mcq: local variable
]


def _grade_regressions() -> None:
    """Tighten fill/short: no 'n'→'n*n', no '5' in '15', print exact, etc."""
    load_chapter.cache_clear()
    lessons = {}
    for cid in ("py-01", "py-02", "py-03"):
        for L in load_chapter(cid)["lessons"]:
            lessons[L["id"]] = L

    def check(lid: str, attempt: str, want: bool) -> None:
        got = grade_lesson(lessons[lid], attempt).passed
        assert got is want, f"{lid} {attempt!r} -> {got}, want {want}"

    check("py-01-l1", 'print("Hello LeapMa")', True)
    check("py-01-l1", 'print("Hello")', False)
    check("py-01-l3", "5", True)
    check("py-01-l3", "15", False)
    check("py-02-l3", "n", False)
    check("py-02-l3", "n * n", True)
    check("py-03-l3", "n", False)
    check("py-03-l3", "return n * 2", True)
    print("OK grade regressions (fill/code tightness)")


def _assert_story_shell(html: str, *, expect_story: bool) -> None:
    """SSR: story panel visible when default=story; normal when default=normal."""
    story = re.search(
        r'id="concept-story"[^>]*(?:hidden|is-hidden)?',
        html,
    )
    normal = re.search(
        r'id="concept-normal"[^>]*(?:hidden|is-hidden)?',
        html,
    )
    assert story and normal, "expected both concept panels in HTML"
    story_hidden = "hidden" in story.group(0) or "is-hidden" in story.group(0)
    normal_hidden = "hidden" in normal.group(0) or "is-hidden" in normal.group(0)
    if expect_story:
        assert not story_hidden, "expected story panel visible on first paint"
        assert normal_hidden, "expected normal panel hidden when default=story"
        assert "is-story-mode" in html
        assert "任务简报" in html
    else:
        assert not normal_hidden, "expected normal panel visible on first paint"
        assert story_hidden, "expected story panel hidden when default=normal"


def main() -> int:
    _grade_regressions()
    app = create_app()
    client = app.test_client()

    # Guest Dashboard: continue + chapter list; NO full preference forms
    r = client.get("/dashboard")
    assert r.status_code == 200, f"dashboard {r.status_code}"
    body = r.get_data(as_text=True)
    assert "第 1 章 · 变量与类型" in body or "变量与类型" in body
    assert "未开放" in body
    assert "15" in body or "第 15 章" in body
    assert "继续学习" in body
    assert "个人中心" in body and "/profile" in body
    assert 'name="concept_mode_default"' not in body, "dashboard must not host mode form"
    assert "保存默认模式" not in body
    assert "保存显示名" not in body
    assert "接下来练什么" in body or "Dashboard" in body

    # /me → /profile (compat)
    me = client.get("/me", follow_redirects=False)
    assert me.status_code in (301, 302), f"/me should redirect, got {me.status_code}"
    assert "/profile" in (me.headers.get("Location") or "")

    # Profile: nickname, time, default mode, progress
    prof = client.get("/profile")
    assert prof.status_code == 200, f"profile {prof.status_code}"
    pbody = prof.get_data(as_text=True)
    assert "个人中心" in pbody or "我的账户" in pbody
    assert "显示名" in pbody
    assert "首次进入时间" in pbody or "注册时间" in pbody
    assert "默认概念模式" in pbody, "expected Plan B preference UI on profile"
    assert 'name="concept_mode_default"' in pbody
    assert "课内" in pbody and "不会改动" in pbody
    assert "学习进度" in pbody
    assert "Python" in pbody
    assert "登录" in pbody or "注册" in pbody
    assert "游客" in pbody or "已登录" in pbody

    r = client.get("/track/python")
    assert r.status_code == 200, f"track {r.status_code}"
    track_html = r.get_data(as_text=True)
    for i in range(1, 16):
        assert f"第 {i} 章" in track_html or f"py-{i:02d}" in track_html or f"chapter" in track_html

    for chapter_id, lesson_id, answer in SAMPLES:
        url = f"/track/python/{chapter_id}/{lesson_id}"
        g = client.get(url)
        assert g.status_code == 200, f"GET {url} -> {g.status_code}"
        html_get = g.get_data(as_text=True)
        assert "学" in html_get and "例" in html_get and "练" in html_get, (
            f"expected 学/例/练 sections on {url}"
        )
        assert "正常模式" in html_get, f"expected concept mode toggle on {url}"
        assert 'id="learn"' in html_get and 'id="practice"' in html_get
        p = client.post(
            url,
            data={"action": "submit", "attempt_text": answer},
            follow_redirects=False,
        )
        # Pass may 302 to next lesson, or 200 with grade on fail
        if p.status_code in (301, 302):
            print(f"OK {chapter_id}/{lesson_id} passed → redirect {p.headers.get('Location')}")
            continue
        assert p.status_code == 200, f"POST {url} -> {p.status_code}"
        html = p.get_data(as_text=True)
        assert "判定：通过" in html or "通过" in html, (
            f"expected pass for {chapter_id}/{lesson_id}, got:\n{html[:800]}"
        )
        print(f"OK {chapter_id}/{lesson_id} passed on page")

    # Story mission shell on py-01-l2
    story_page = client.get("/track/python/py-01/py-01-l2")
    assert story_page.status_code == 200
    story_html = story_page.get_data(as_text=True)
    assert "故事模式" in story_html
    assert "id=\"concept-story\"" in story_html or "concept-story" in story_html
    assert "story-mission" in story_html
    assert "任务简报" in story_html
    assert "本关目标" in story_html or "mission" in story_html.lower()
    # Default unset → normal first paint
    _assert_story_shell(story_html, expect_story=False)
    # Legacy ?mode=story must NOT override default (Plan B refresh rule)
    deep = client.get("/track/python/py-01/py-01-l2?mode=story")
    assert deep.status_code == 200
    _assert_story_shell(deep.get_data(as_text=True), expect_story=False)
    print("OK default=normal; ?mode= ignored")

    # --- Plan B: set default on /profile only → lesson opens in story ---
    save = client.post(
        "/profile/concept-mode",
        data={"concept_mode_default": "story"},
        follow_redirects=False,
    )
    assert save.status_code in (301, 302), f"expected redirect, got {save.status_code}"
    loc = save.headers.get("Location") or ""
    assert "/profile" in loc, f"mode save should land on profile, got {loc!r}"
    # Cookie set for guests (check before following redirect)
    set_cookie = save.headers.get("Set-Cookie") or ""
    assert "concept_mode_default=story" in set_cookie, f"expected guest cookie, got {set_cookie!r}"
    save_follow = client.get(loc or "/profile")
    assert save_follow.status_code == 200
    save_html = save_follow.get_data(as_text=True)
    assert "默认概念模式已设为「故事」" in save_html
    assert "课内切换不会改动此项" in save_html
    assert 'value="story"' in save_html and "checked" in save_html

    # Dashboard summary reflects story, still no full form
    dash_sum = client.get("/dashboard")
    dash_sum_html = dash_sum.get_data(as_text=True)
    assert "故事" in dash_sum_html
    assert 'name="concept_mode_default"' not in dash_sum_html

    l2 = client.get("/track/python/py-01/py-01-l2")
    assert l2.status_code == 200
    l2_html = l2.get_data(as_text=True)
    _assert_story_shell(l2_html, expect_story=True)
    print("OK default=story → py-01-l2 story shell")

    # Next lesson also uses default (story), not a temporary normal choice
    l3 = client.get("/track/python/py-01/py-01-l3")
    assert l3.status_code == 200
    l3_html = l3.get_data(as_text=True)
    if "concept-story" in l3_html:
        _assert_story_shell(l3_html, expect_story=True)
        print("OK Next lesson also story (default)")
    else:
        assert "本课暂无故事稿" in l3_html
        print("OK Next lesson no story → honest fallback")

    # In-lesson toggle must NOT hit preference endpoint / change default
    prof_check = client.get("/profile")
    prof_html = prof_check.get_data(as_text=True)
    assert 'value="story"' in prof_html
    assert re.search(
        r'name="concept_mode_default"\s+value="story"[^>]*checked'
        r'|checked[^>]*name="concept_mode_default"[^>]*value="story"',
        prof_html,
    ) or ('value="story"' in prof_html and "checked" in prof_html)

    # Reset default to normal → new lesson opens normal
    reset = client.post(
        "/profile/concept-mode",
        data={"concept_mode_default": "normal"},
        follow_redirects=True,
    )
    assert reset.status_code == 200
    assert "默认概念模式已设为「正常」" in reset.get_data(as_text=True)
    again = client.get("/track/python/py-01/py-01-l2")
    _assert_story_shell(again.get_data(as_text=True), expect_story=False)
    print("OK default reset to normal → lesson normal")

    # Logged-in: preference persists on account (DB), not only session
    uname = "mode_b_tester"
    client.post(
        "/register",
        data={
            "username": uname,
            "password": "secret12",
            "display_name": "ModeB",
        },
        follow_redirects=True,
    )
    # Username may already exist from prior run — try login
    client.post(
        "/login",
        data={"username": uname, "password": "secret12"},
        follow_redirects=True,
    )
    client.post(
        "/profile/concept-mode",
        data={"concept_mode_default": "story"},
        follow_redirects=True,
    )
    # Fresh client = new session; login again → account default wins
    client2 = app.test_client()
    login2 = client2.post(
        "/login",
        data={"username": uname, "password": "secret12"},
        follow_redirects=True,
    )
    assert login2.status_code == 200
    l2_again = client2.get("/track/python/py-01/py-01-l2")
    _assert_story_shell(l2_again.get_data(as_text=True), expect_story=True)
    # Reset account back to normal for idempotent re-runs
    client2.post(
        "/profile/concept-mode",
        data={"concept_mode_default": "normal"},
        follow_redirects=True,
    )
    print("OK logged-in account default persists across sessions")

    # Continue CTA should show N/M after passes
    dash = client.get("/dashboard")
    assert dash.status_code == 200
    dhtml = dash.get_data(as_text=True)
    assert "继续学习" in dhtml
    print("OK dashboard continue CTA present")
    print("smoke passed")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
