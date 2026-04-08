from __future__ import annotations

import os
from typing import Any

from flask import Flask
from flasgger import Swagger

try:
  from .routes import api_bp
except ImportError:
  from routes import api_bp

app = Flask(__name__)

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Week5 Library Management API",
        "description": "Resource modeling + search + pagination strategies (offset/page/cursor)",
        "version": "1.0.0",
    },
    "basePath": "/",
    "schemes": ["http"],
}

Swagger(app, template=swagger_template)
app.register_blueprint(api_bp)


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5008"))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    print(f"Week5 API running at http://127.0.0.1:{port}/apidocs/")
    app.run(port=port, debug=debug)
