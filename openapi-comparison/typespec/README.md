# TypeSpec Demo

File chính: `main.tsp`

> Lưu ý: đề bài ghi `TypeSec`, nhưng format/tool phổ biến là **TypeSpec**.

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
npx @redocly/cli preview-docs tsp-output/openapi3/openapi.yaml --port 8083
```

Mở: `http://localhost:8083`
