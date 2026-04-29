from __future__ import annotations

import os

from dotenv import load_dotenv

try:
    from .app import create_app
except ImportError:
    from app import create_app


def run() -> None:
    load_dotenv()

    app = create_app()
    port = int(os.getenv("PORT", "5011"))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    print(f"Week9 API Swagger running at http://127.0.0.1:{port}/apidocs/")
    print(f"Week9 API running at http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug)


if __name__ == "__main__":
    run()