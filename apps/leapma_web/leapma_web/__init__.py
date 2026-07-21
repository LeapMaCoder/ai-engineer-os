"""LeapMa Web — SPEC-GL-001 vertical slice (Flask SSR)."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask

# Load repo-root .env then app .env
_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(_ROOT / ".env")
load_dotenv(Path(__file__).resolve().parents[1] / ".env")


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "leapma-dev-only-change-me")
    app.config["LEAPMA_LLM_PROVIDER"] = os.getenv("LEAPMA_LLM_PROVIDER", "mock")
    app.config["DATABASE_URL"] = os.getenv(
        "DATABASE_URL",
        "sqlite:///" + str(Path(__file__).resolve().parents[1] / "data" / "leapma.db"),
    )

    from flask import session

    from leapma_web.db import init_db
    from leapma_web.routes import bp

    init_db(app.config["DATABASE_URL"])
    app.register_blueprint(bp)

    @app.context_processor
    def inject_guest():
        name = (session.get("display_name") or "").strip()
        return {
            "guest_label": name if name else "游客",
            "logged_in": bool(session.get("logged_in")),
        }

    return app
