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
