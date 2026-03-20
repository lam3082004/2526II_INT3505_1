# OpenAPI Demo

File chính: `openapi.yaml`

## Cài đặt

Chọn một trong hai cách:

### Cách 1: Redocly CLI

```bash
npm install -g @redocly/cli
```

### Cách 2: Prism (mock server)

```bash
npm install -g @stoplight/prism-cli
```

## Chạy

### Xem tài liệu trực tiếp

```bash
redocly preview-docs openapi.yaml --port 8080
```

Mở: `http://localhost:8080`

### Chạy mock API từ spec

```bash
prism mock openapi.yaml -p 4010
```

Mở: `http://localhost:4010/books`

## Kiểm tra nhanh

```bash
redocly lint openapi.yaml
```
