# OpenAPI Demo

File chính: `openapi.yaml`

## Cài đặt

Không cần cài global (`-g`) để tránh lỗi quyền `EACCES`.

Chọn một trong hai cách:

### Cách 1: Redocly CLI

```bash
npx --yes @redocly/cli@1 --version
```

### Cách 2: Prism (mock server)

```bash
npx --yes @stoplight/prism-cli --version
```

## Chạy

### Xem tài liệu trực tiếp

```bash
npx --yes @redocly/cli@1 preview-docs openapi.yaml --port 8080
```

Mở: `http://localhost:8080`

### Chạy mock API từ spec

```bash
npx --yes @stoplight/prism-cli mock openapi.yaml -p 4010
```

Mở: `http://localhost:4010/books`

## Kiểm tra nhanh

```bash
npx --yes @redocly/cli@1 lint openapi.yaml
```
