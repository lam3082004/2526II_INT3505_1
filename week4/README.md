# Week 4 - API Specification và OpenAPI

## Mục tiêu bài thực hành

- Viết OpenAPI YAML cho API quản lý sách (5 endpoints)
- Render tài liệu tự động bằng Swagger UI
- Chia sẻ link tài liệu API

## Cấu trúc file

- `openapi.yaml`: OpenAPI 3.0.3 specification
- `app.py`: Flask server + Swagger UI renderer

## 5 endpoints của Book API

1. `GET /books` - Lấy danh sách sách
2. `POST /books` - Tạo sách mới
3. `GET /books/{book_id}` - Lấy chi tiết sách
4. `PUT /books/{book_id}` - Cập nhật sách
5. `DELETE /books/{book_id}` - Xóa sách

## Cách chạy

Từ thư mục gốc project:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python week4/app.py
```

## Link tài liệu Swagger UI

- Local docs: http://127.0.0.1:5007/docs
- OpenAPI YAML: http://127.0.0.1:5007/openapi.yaml

Bạn có thể chụp màn hình trang `/docs` để đính kèm khi nộp bài hoặc commit lên GitHub.

## Deploy lên Vercel

Project đã có sẵn cấu hình deploy:

- `vercel.json`
- `api/index.py` (entrypoint cho Vercel)
- `requirements.txt`

### Các bước

1. Push code lên GitHub.
2. Vào Vercel → **Add New Project** → Import repo GitHub.
3. Ở phần Environment Variables, thêm:
	- `FLASK_ENV=production`
	- `FLASK_DEBUG=0`
	- `JWT_SECRET=<secret-manh>`
	- `JWT_ALGORITHM=HS256`
	- `JWT_EXPIRE_MINUTES=60`
4. Bấm **Deploy**.

Sau khi deploy xong, mở:

- `https://<your-vercel-domain>/docs`
- `https://<your-vercel-domain>/openapi.yaml`