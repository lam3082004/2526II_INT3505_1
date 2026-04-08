# TypeSpec Demo

File chính: `main.tsp`

> Lưu ý: đề bài ghi `TypeSec`, nhưng format/tool phổ biến là **TypeSpec**.

## Luồng dùng

```text
TypeSpec (main.tsp)
	↓
Compile
	↓
OpenAPI.yaml
	↓
Frontend + Backend + Docs
```

Ý nghĩa ngắn gọn:

- `main.tsp`: nơi bạn viết mô tả API bằng TypeSpec.
- `npm run build`: compile sang OpenAPI.
- `tsp-output/openapi3/openapi.yaml`: file OpenAPI đầu ra.
- Từ file OpenAPI này, bạn có thể sinh frontend client, backend stub/server và tài liệu API.

## Cài đặt

```bash
npm install
```

## Chạy (compile sang OpenAPI)

```bash
npm run build
```

Kết quả sinh ra tại:

- `tsp-output/openapi3/openapi.yaml`

## Preview tài liệu sau khi compile

```bash
npx --yes @redocly/cli@1 preview-docs tsp-output/openapi3/openapi.yaml --port 8083
```

Mở: `http://localhost:8083`

## Clean + Rebuild từ đầu

Bạn có thể xóa để làm lại từ đầu.

Nên giữ lại các file nguồn sau:

- `main.tsp`
- `package.json`
- `tspconfig.yaml`
- `openapitools.json`
- `README.md`

Có thể xóa an toàn:

- `generated`
- `node_modules`
- `tsp-output`

Tùy chọn:

- Có thể xóa thêm `package-lock.json` nếu muốn cài lại dependency sạch hoàn toàn (không bắt buộc).

Làm sạch và chạy lại toàn bộ:

```bash
cd /home/hh/Desktop/2526II_INT3505_1/openapi-comparison/typespec
rm -rf generated node_modules tsp-output
npm install
npm run build
npx --yes @redocly/cli@1 preview-docs tsp-output/openapi3/openapi.yaml --port 8083
npx --yes @openapitools/openapi-generator-cli generate -i tsp-output/openapi3/openapi.yaml -g python-fastapi -o generated/server-fastapi
```

## Kịch bản demo cho thầy (3-5 phút)

Mục tiêu: chứng minh luồng `TypeSpec -> OpenAPI -> Docs -> Sinh code` chạy được.

### Bước 1: Build từ TypeSpec

```bash
npm run build
```

Bạn nói khi demo:

- "Em viết API ở file `main.tsp` rồi compile sang OpenAPI."
- "File output nằm ở `tsp-output/openapi3/openapi.yaml`."

### Bước 2: Mở file OpenAPI sinh ra

```bash
cat tsp-output/openapi3/openapi.yaml
```

Bạn nói khi demo:

- "Đây là OpenAPI được sinh tự động từ TypeSpec, không viết tay."

### Bước 3: Preview tài liệu API

```bash
npx --yes @redocly/cli@1 preview-docs tsp-output/openapi3/openapi.yaml --port 8083
```

Mở trình duyệt: `http://localhost:8083`

Bạn nói khi demo:

- "Từ OpenAPI vừa sinh, em render docs ngay để review endpoint và schema."

Ghi chú: dừng server bằng `Ctrl + C` (exit code `130` là bình thường).

### Bước 4: Demo sinh backend/client từ OpenAPI (tuỳ chọn, +1 phút)

Yêu cầu trước khi chạy `openapi-generator-cli`:

- Máy cần có Java (JRE/JDK). Nếu thiếu sẽ lỗi: `java: not found`.

Kiểm tra nhanh:

```bash
java -version
```

Nếu chưa có Java (Ubuntu/Debian):

```bash
sudo apt update
sudo apt install -y default-jre
```

Nếu không muốn cài Java, dùng Docker:

```bash
docker run --rm -v "${PWD}:/local" openapitools/openapi-generator-cli generate \
	-i /local/tsp-output/openapi3/openapi.yaml \
	-g python-fastapi \
	-o /local/generated/server-fastapi
```

Sinh backend stub (FastAPI):

```bash
npx --yes @openapitools/openapi-generator-cli generate \
	-i tsp-output/openapi3/openapi.yaml \
	-g python-fastapi \
	-o generated/server-fastapi
```

Sinh frontend client (TypeScript Axios):

```bash
npx --yes @openapitools/openapi-generator-cli generate \
	-i tsp-output/openapi3/openapi.yaml \
	-g typescript-axios \
	-o generated/client-ts
```

Bạn nói khi demo:

- "Cùng một nguồn TypeSpec, em sinh được OpenAPI, tài liệu, backend stub và frontend client."

### Bước 5: Chạy FastAPI đã sinh ra (nếu muốn demo backend)

```bash
cd generated/server-fastapi
python3 -m pip install -r requirements.txt
PYTHONPATH=src uvicorn openapi_server.main:app --host 0.0.0.0 --port 8080
```

Mở trình duyệt:

- `http://localhost:8080/docs/`

Bạn nói khi demo:

- "Đây là backend FastAPI sinh tự động từ OpenAPI, chạy lên là có Swagger UI ngay."
