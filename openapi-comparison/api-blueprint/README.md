# API Blueprint Demo

File chính: `api.apib`

## Cài đặt

```bash
npm init -y
npm install --save-dev aglio drafter
```

## Chạy

```bash
npx aglio -i api.apib -s -p 8081
```

Mở: `http://localhost:8081`

## Tuỳ chọn parse AST với Drafter

```bash
npx drafter -f json api.apib > ast.json
```

## Chạy nhanh không cần cài local

```bash
npx --yes aglio -i api.apib -s -p 8081
```
