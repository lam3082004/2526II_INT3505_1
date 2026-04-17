# Week7 - OpenAPI + MongoDB Product CRUD (Python)

Muc tieu cua phan thuc hanh nay la dung backend Python tu OpenAPI spec va ket noi MongoDB de thao tac CRUD cho resource Product.

## Cau truc

- openapi.yaml: dac ta API cho Product
- requirements.txt: danh sach thu vien Python
- src/server.py: entrypoint chay server
- src/app.py: cau hinh Flask, Flasgger, routes
- src/config/db.py: ket noi MongoDB
- src/models/product.py: helper xac thuc/serialize Product
- src/controllers/product_controller.py: logic CRUD
- src/routes/product_routes.py: dinh tuyen API

## Chay local

1. Cai dependencies:

python -m pip install -r requirements.txt

2. Tao file moi truong:

cp .env.example .env

3. Khoi dong MongoDB local, roi chay backend:

python src/server.py

4. Mo Swagger UI:

http://127.0.0.1:5009/apidocs/

## Sinh code backend tu OpenAPI (Swagger Codegen)

Neu may co Docker, chay lenh sau tai thu muc week7:

docker run --rm -v "${PWD}:/local" swaggerapi/swagger-codegen-cli-v3 generate -i /local/openapi.yaml -l python-flask -o /local/generated-server

## API

- GET /products
- POST /products
- GET /products/{productId}
- PUT /products/{productId}
- DELETE /products/{productId}

## Vi du payload

{
  "name": "Mechanical Keyboard",
  "description": "Compact keyboard with hot-swappable switches",
  "price": 79.99,
  "category": "peripherals",
  "stock": 25,
  "imageUrl": "https://example.com/product.png"
}