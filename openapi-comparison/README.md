# So sánh OpenAPI, API Blueprint, RAML và TypeSpec

## 1) So sánh nhanh

| Tiêu chí | OpenAPI | API Blueprint | RAML | TypeSpec *(TypeSec theo đề bài)* |
|---|---|---|---|---|
| Triết lý | Chuẩn mô tả API phổ biến nhất, tool-rich | Viết API như tài liệu Markdown, dễ đọc | API-first với thiết kế có cấu trúc và tái sử dụng | Mô tả API bằng ngôn ngữ định nghĩa kiểu, sinh spec tự động |
| Định dạng | YAML/JSON | Markdown + cú pháp Blueprint | YAML | Ngôn ngữ `.tsp` (DSL) |
| Độ phổ biến | Rất cao | Trung bình | Trung bình | Đang tăng (đặc biệt trong hệ sinh thái Microsoft) |
| Hệ sinh thái | Swagger UI, Redoc, Postman, codegen | Aglio, Drafter | Anypoint tooling, raml2html | TypeSpec compiler, emit OpenAPI |
| Dễ bắt đầu | Dễ | Rất dễ nếu quen Markdown | Trung bình | Trung bình (cần làm quen DSL) |
| Tái sử dụng schema | Tốt (`components`) | Hạn chế hơn | Tốt (`types`, traits, resourceTypes) | Rất tốt (type system mạnh) |
| Sinh client/server | Rất tốt | Hạn chế | Có nhưng ít phổ biến hơn OAS | Qua OpenAPI emitter |
| Phù hợp khi nào | Dự án thực tế, tích hợp nhiều tool | Team nhỏ, cần docs dễ đọc nhanh | Team API design-first có kỷ luật | Muốn maintain từ source typed và sinh nhiều output |

## 2) Demo ứng dụng quản lý thư viện

Demo dùng cùng một mô hình API cho cả 4 format với 5 endpoint:

- `GET /books`
- `POST /books`
- `GET /books/{bookId}`
- `POST /loans`
- `DELETE /loans/{loanId}`

Thư mục:

- [openapi](openapi)
- [api-blueprint](api-blueprint)
- [raml](raml)
- [typespec](typespec)

## 3) Gợi ý chọn công nghệ

- Cần tương thích rộng và deploy nhanh docs: chọn **OpenAPI**.
- Cần viết tài liệu như Markdown, nhẹ nhàng: chọn **API Blueprint**.
- Theo hướng design-first chặt chẽ với YAML thuần: chọn **RAML**.
- Muốn định nghĩa kiểu mạnh, tái sử dụng cao, sinh OpenAPI từ source: chọn **TypeSpec**.
- Luồng của TypeSpec trong bài này là: `main.tsp` → compile → `openapi.yaml` → sinh frontend/backend/docs.

## 4) Chạy nhanh từng format (tối giản)

### OpenAPI

```bash
cd openapi
npx --yes @redocly/cli@1 preview-docs openapi.yaml --port 8080
```

Mở: `http://localhost:8080`

### API Blueprint

```bash
cd api-blueprint
npx aglio -i api.apib -s -p 8081
```

Mở: `http://localhost:8081`

### RAML

```bash
cd raml
raml2html api.raml > index.html
python3 -m http.server 8082
```

Mở: `http://localhost:8082/index.html`

### TypeSpec (TypeSec trong đề)

```bash
cd typespec
npm run build
npx --yes @redocly/cli@1 preview-docs tsp-output/openapi3/openapi.yaml --port 8083
```

Mở: `http://localhost:8083`

## 5) Demo sinh code/test từ file tài liệu API

Khuyến nghị dùng file OpenAPI làm chuẩn để sinh code/test:

- File nguồn: `openapi/openapi.yaml`
- Hoặc từ TypeSpec: build trước để ra `typespec/tsp-output/openapi3/openapi.yaml`

### Sinh code client/server (OpenAPI Generator)

```bash
# Sinh Python FastAPI server
npx --yes @openapitools/openapi-generator-cli generate -i openapi/openapi.yaml -g python-fastapi -o generated/server-fastapi

# Sinh TypeScript client (axios)
npx --yes @openapitools/openapi-generator-cli generate -i openapi/openapi.yaml -g typescript-axios -o generated/client-ts
```

### Sinh test hợp đồng API (Schemathesis)

```bash
pip install schemathesis
schemathesis run openapi/openapi.yaml --base-url http://localhost:5007
```

Ý nghĩa: công cụ sẽ tự tạo nhiều test case từ schema để kiểm tra API thật có đúng hợp đồng hay không.
