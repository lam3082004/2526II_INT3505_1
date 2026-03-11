# Phân tích 3 API công khai

---

## 1. GitHub API

### Giới thiệu

GitHub API cho phép các ứng dụng bên ngoài truy cập và quản lý dữ liệu trên GitHub như repository, issue, pull request và thông tin người dùng.

### Ví dụ endpoint

```
GET https://api.github.com/users/{username}
```

### Ví dụ request

```
GET https://api.github.com/users/octocat
```

### Ví dụ response

```json
{
  "login": "octocat",
  "id": 583231,
  "public_repos": 8,
  "followers": 10000
}
```

### Phân tích

| Thuộc tính       | Giá trị       |
|------------------|---------------|
| Loại API         | REST API      |
| Giao thức        | HTTP/HTTPS    |
| Định dạng dữ liệu | JSON         |

### Ứng dụng

- Xây dựng dashboard quản lý project
- Công cụ phân tích repository

---

## 2. TypeRacer API

### Giới thiệu

TypeRacer API cung cấp dữ liệu về các cuộc đua gõ phím của người chơi trên nền tảng TypeRacer. API này cho phép truy xuất thông tin người chơi, kết quả cuộc đua và thống kê tốc độ gõ phím.

### Ví dụ endpoint

```
GET https://data.typeracer.com/games
```

### Ví dụ request

```
GET https://data.typeracer.com/games?playerId=tr:username&n=5
```

### Ví dụ response

```json
[
  {
    "gn": 123456,
    "wpm": 95,
    "accuracy": 98.5,
    "timestamp": 1700000000
  }
]
```

### Phân tích

| Thuộc tính       | Giá trị       |
|------------------|---------------|
| Loại API         | REST API      |
| Giao thức        | HTTP/HTTPS    |
| Định dạng dữ liệu | JSON         |

### Ứng dụng

- Thống kê tốc độ gõ phím
- Tạo bảng xếp hạng
- Phân tích hiệu suất luyện gõ

---

## 3. Bybit API

### Giới thiệu

Bybit API cho phép các ứng dụng truy cập dữ liệu thị trường và thực hiện giao dịch trên sàn Bybit. API thường được sử dụng để xây dựng bot giao dịch, hệ thống phân tích thị trường hoặc ứng dụng theo dõi giá tiền điện tử.

### Ví dụ endpoint

```
GET https://api.bybit.com/v5/market/tickers
```

### Ví dụ request

```
GET https://api.bybit.com/v5/market/tickers?category=spot&symbol=BTCUSDT
```

### Ví dụ response

```json
{
  "retCode": 0,
  "result": {
    "list": [
      {
        "symbol": "BTCUSDT",
        "lastPrice": "60000",
        "volume24h": "12345"
      }
    ]
  }
}
```

### Phân tích

| Thuộc tính       | Giá trị       |
|------------------|---------------|
| Loại API         | REST API      |
| Giao thức        | HTTPS         |
| Định dạng dữ liệu | JSON         |

### Ứng dụng

- Bot trading tự động
- Phân tích dữ liệu thị trường
- Ứng dụng theo dõi giá crypto