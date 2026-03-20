from pathlib import Path
import os

from flask import Flask, jsonify, make_response, request, send_from_directory

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent

BOOKS = [
    {"id": 1, "title": "Clean Code", "author": "Robert C. Martin", "year": 2008},
    {"id": 2, "title": "Refactoring", "author": "Martin Fowler", "year": 1999},
]


def find_book(book_id):
    return next((book for book in BOOKS if book["id"] == book_id), None)


def next_book_id():
    return max((book["id"] for book in BOOKS), default=0) + 1


def validate_book_payload(data, require_all_fields):
    if not isinstance(data, dict):
        return "Payload must be a JSON object"

    allowed_fields = {"title", "author", "year"}
    unknown_fields = set(data.keys()) - allowed_fields
    if unknown_fields:
        return f"Unknown fields: {', '.join(sorted(unknown_fields))}"

    if require_all_fields:
        required_fields = {"title", "author", "year"}
        missing_fields = required_fields - set(data.keys())
        if missing_fields:
            return f"Missing fields: {', '.join(sorted(missing_fields))}"
    elif not data:
        return "At least one field is required"

    if "title" in data and (not isinstance(data["title"], str) or not data["title"].strip()):
        return "title must be a non-empty string"

    if "author" in data and (not isinstance(data["author"], str) or not data["author"].strip()):
        return "author must be a non-empty string"

    if "year" in data and (not isinstance(data["year"], int) or data["year"] < 0):
        return "year must be a non-negative integer"

    return None


@app.route("/openapi.yaml", methods=["GET"])
def openapi_file():
    return send_from_directory(str(BASE_DIR), "openapi.yaml")


@app.route("/docs", methods=["GET"])
def swagger_ui():
    html = """
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8" />
        <title>Week4 Book API Docs</title>
        <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css" />
      </head>
      <body>
        <div id="swagger-ui"></div>
        <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
        <script>
          window.onload = function () {
            SwaggerUIBundle({
              url: '/openapi.yaml',
              dom_id: '#swagger-ui',
              deepLinking: true,
            });
          };
        </script>
      </body>
    </html>
    """
    return make_response(html, 200)


@app.route("/books", methods=["GET"])
def get_books():
    return jsonify(BOOKS), 200


@app.route("/books", methods=["POST"])
def create_book():
    data = request.get_json(silent=True)
    error = validate_book_payload(data, require_all_fields=True)
    if error:
        return jsonify({"error": error}), 400

    new_book = {
        "id": next_book_id(),
        "title": data["title"].strip(),
        "author": data["author"].strip(),
        "year": data["year"],
    }
    BOOKS.append(new_book)

    response = make_response(jsonify(new_book), 201)
    response.headers["Location"] = f"/books/{new_book['id']}"
    return response


@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = find_book(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book), 200


@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = find_book(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    data = request.get_json(silent=True)
    error = validate_book_payload(data, require_all_fields=False)
    if error:
        return jsonify({"error": error}), 400

    if "title" in data:
        book["title"] = data["title"].strip()
    if "author" in data:
        book["author"] = data["author"].strip()
    if "year" in data:
        book["year"] = data["year"]

    return jsonify(book), 200


@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = find_book(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    BOOKS.remove(book)
    return "", 204


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5007"))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    print(f"Week4 Book API is running on http://127.0.0.1:{port}/docs")
    app.run(port=port, debug=debug)