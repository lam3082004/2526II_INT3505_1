# Week8 - Secure Product API (JWT + OpenAPI + MongoDB)

Tuần 8 xây dựng backend Python theo phong cách các tuần trước:

- Flask + Flasgger hiển thị Swagger UI từ OpenAPI spec (`openapi.yaml`)
- MongoDB lưu Product (CRUD)
- JWT Auth (register/login/me)
- **Chỉ cho phép ghi** (POST/PUT/DELETE) khi có Bearer token; GET public

## Cấu trúc

- `openapi.yaml`: đặc tả OpenAPI
- `.env.example`: biến môi trường mẫu
- `requirements.txt`: dependencies
- `src/server.py`: entrypoint chạy server
- `src/app.py`: tạo Flask app + swagger + register routes
- `src/auth/jwt_auth.py`: JWT helpers + decorator
- `src/config/db.py`: kết nối MongoDB
- `src/models/product.py`: validate/serialize product
- `src/controllers/product_controller.py`: CRUD logic
- `src/routes/auth_routes.py`: routes auth
- `src/routes/product_routes.py`: routes product

## Chạy local

```bash
cd week8
python -m pip install -r requirements.txt
cp .env.example .env
python src/server.py
```

Mở Swagger UI: `http://127.0.0.1:5010/apidocs/`

## Quick test

1) Register / Login để lấy token:

- `POST /auth/register`
- `POST /auth/login`

2) Gắn header cho API ghi:

`Authorization: Bearer <JWT_TOKEN>`

