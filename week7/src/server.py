from __future__ import annotations

import os

from dotenv import load_dotenv

try:
    from .app import create_app
    from .config.db import connect_db
except ImportError:
    from app import create_app
    from config.db import connect_db


def run() -> None:
    load_dotenv()

    app = create_app()
    mongodb_uri = os.getenv("MONGODB_URI")
    mongodb_db_name = os.getenv("MONGODB_DB_NAME", "week7_products")

    connect_db(mongodb_uri, mongodb_db_name)

    port = int(os.getenv("PORT", "5009"))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"

    print(f"Week7 Product API running at http://127.0.0.1:{port}")
    print(f"Swagger UI available at http://127.0.0.1:{port}/apidocs/")
    app.run(host="0.0.0.0", port=port, debug=debug)


if __name__ == "__main__":
    run()