from flask import Flask, jsonify
from flasgger import Swagger

try:
  from .auth import auth_bp
  from .items import items_bp
except ImportError:
  from auth import auth_bp
  from items import items_bp

app = Flask(__name__)

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Week3 Basic API",
        "description": "Simple API for testing Swagger UI + JWT",
        "version": "1.0.0",
    },
    "basePath": "/",
    "schemes": ["http"],
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Format: Bearer <JWT_TOKEN>",
        }
    }
}

Swagger(app, template=swagger_template)
app.register_blueprint(auth_bp)
app.register_blueprint(items_bp)


@app.route("/", methods=["GET"])
def home():
    """
    Welcome endpoint
    ---
    tags:
      - System
    responses:
      200:
        description: API is running
    """
    return jsonify({"message": "Week3 Basic API is running", "docs": "/apidocs/"}), 200


@app.route("/health", methods=["GET"])
def health_check():
    """
    Health check endpoint
    ---
    tags:
      - System
    responses:
      200:
        description: Service health status
    """
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    print("Week3 Swagger Basic API running on http://127.0.0.1:5006/apidocs/")
    app.run(port=5006, debug=True)
