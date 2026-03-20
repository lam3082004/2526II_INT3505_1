# RAML Demo

File chính: `api.raml`

## Cài đặt

```bash
npm install -g raml2html-cli
```

## Chạy (render tài liệu HTML)

```bash
raml2html api.raml > index.html
python3 -m http.server 8082
```

Mở: `http://localhost:8082/index.html`

## Tuỳ chọn validate nhanh

Bạn có thể mở file RAML bằng VS Code extension `RAML` để check syntax trực tiếp.
