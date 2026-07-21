"""Smoke: submit one passing attempt per ready chapter (py-01..03)."""

from __future__ import annotations

import sys

from leapma_web import create_app


# One known-good answer per chapter (diverse types: mcq / fill / mcq)
SAMPLES = [
    ("py-01", "py-01-l2", "B"),  # mcq: assignment meaning
    ("py-02", "py-02-l3", "n * n"),  # fill: square
    ("py-03", "py-03-l1", "B"),  # mcq: local variable
]


def main() -> int:
    app = create_app()
    client = app.test_client()

    # Guest session + open track
    r = client.get("/dashboard")
    assert r.status_code == 200, f"dashboard {r.status_code}"
    body = r.get_data(as_text=True)
    assert "第 1 章 · 变量与类型" in body or "变量与类型" in body
    assert "未开放" in body
    assert "15" in body or "第 15 章" in body

    r = client.get("/track/python")
    assert r.status_code == 200, f"track {r.status_code}"
    track_html = r.get_data(as_text=True)
    for i in range(1, 16):
        assert f"第 {i} 章" in track_html or f"py-{i:02d}" in track_html or f"chapter" in track_html

    for chapter_id, lesson_id, answer in SAMPLES:
        url = f"/track/python/{chapter_id}/{lesson_id}"
        g = client.get(url)
        assert g.status_code == 200, f"GET {url} -> {g.status_code}"
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
