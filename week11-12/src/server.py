from __future__ import annotations

import os

from dotenv import load_dotenv

from app import create_app


def run() -> None:
    load_dotenv()

    app = create_app()
    port = int(os.getenv("PORT", "5013"))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"

    print(f"Week11-12 API running at http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug)


if __name__ == "__main__":
    run()
