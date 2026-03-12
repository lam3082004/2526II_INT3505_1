# Buổi 2: Kiến trúc REST và HTTP Fundamentals

## Phần 1: 6 Nguyên tắc của Kiến trúc REST

REST (Representational State Transfer) là một phong cách kiến trúc phần mềm được Roy Fielding định nghĩa năm 2000. Một API được coi là RESTful khi tuân thủ đầy đủ 6 nguyên tắc sau:

---

### 1. Client-Server (Tách biệt Client và Server)

**Mô tả:** Client và Server hoạt động độc lập với nhau. Client chịu trách nhiệm giao diện người dùng, Server chịu trách nhiệm lưu trữ và xử lý dữ liệu.

**Lợi ích:**
- Tăng khả năng mở rộng (scalability) của server
- Client và Server có thể phát triển độc lập mà không ảnh hưởng nhau
- Dễ dàng thay thế hoặc nâng cấp từng phần

**Ví dụ:** Ứng dụng mobile gọi API backend. Backend không cần biết giao diện mobile trông như thế nào.

---

### 2. Stateless (Phi trạng thái)

**Mô tả:** Mỗi request từ client đến server phải chứa đầy đủ thông tin cần thiết để server xử lý, không phụ thuộc vào bất kỳ context hay session nào được lưu phía server.

**Lợi ích:**
- Dễ scale horizontal (thêm nhiều server)
- Server không cần quản lý session → giảm tải bộ nhớ
- Mỗi request độc lập → dễ debug, monitor

**Ví dụ:** Thay vì lưu session đăng nhập trên server, client gửi JWT token trong mỗi request:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

### 3. Cacheable (Có thể cache)

**Mô tả:** Response từ server phải đánh dấu rõ ràng là có thể cache hay không, giúp client hoặc các tầng trung gian có thể tái sử dụng response mà không cần gửi request lại.

**Lợi ích:**
- Giảm số lượng request đến server
- Cải thiện performance và tốc độ phản hồi
- Tiết kiệm băng thông

**Ví dụ:**
```
Cache-Control: max-age=3600, public
ETag: "abc123"
Last-Modified: Tue, 10 Mar 2026 08:00:00 GMT
```

---

### 4. Uniform Interface (Giao diện đồng nhất)

**Mô tả:** Tất cả tài nguyên (resource) được truy cập thông qua một giao diện thống nhất, bao gồm 4 ràng buộc:
- **Identification of resources:** Tài nguyên được định danh qua URI
- **Manipulation through representations:** Client thao tác tài nguyên qua representation (JSON, XML...)
- **Self-descriptive messages:** Mỗi message chứa đủ thông tin để hiểu cách xử lý
- **HATEOAS:** Response chứa link đến các action liên quan

**Ví dụ endpoint nhất quán:**
```
GET    /users          → Lấy danh sách users
GET    /users/{id}     → Lấy user theo ID
POST   /users          → Tạo user mới
PUT    /users/{id}     → Cập nhật toàn bộ user
PATCH  /users/{id}     → Cập nhật một phần user
DELETE /users/{id}     → Xóa user
```

---

### 5. Layered System (Hệ thống phân lớp)

**Mô tả:** Client không cần biết liệu nó đang giao tiếp trực tiếp với server cuối hay thông qua các tầng trung gian (load balancer, cache, API gateway, security layer...).

**Lợi ích:**
- Dễ thêm tầng bảo mật, caching, load balancing mà không ảnh hưởng client
- Tăng khả năng mở rộng hệ thống
- Che giấu kiến trúc nội bộ

**Ví dụ:**
```
Client → API Gateway → Load Balancer → App Server → Database
```
Client chỉ biết địa chỉ API Gateway, không biết phía sau là gì.

---

### 6. Code on Demand *(tùy chọn)*

**Mô tả:** Server có thể gửi code thực thi (JavaScript, applet...) về client để mở rộng chức năng. Đây là nguyên tắc duy nhất có tính tùy chọn trong REST.

**Lợi ích:**
- Giảm logic cần implement sẵn ở client
- Client có thể được cập nhật tính năng mà không cần deploy lại

**Ví dụ:** Server trả về đoạn JavaScript để client render widget động, hoặc trả về script validation form.

---

## Phần 2: HTTP Methods

| Method   | Mô tả                                      | Idempotent | Safe |
|----------|--------------------------------------------|------------|------|
| `GET`    | Lấy dữ liệu từ server                      | Có         | Có   |
| `POST`   | Tạo resource mới                           | Không      | Không|
| `PUT`    | Thay thế toàn bộ resource                  | Có         | Không|
| `PATCH`  | Cập nhật một phần resource                 | Không      | Không|
| `DELETE` | Xóa resource                               | Có         | Không|
| `HEAD`   | Như GET nhưng không trả về body            | Có         | Có   |
| `OPTIONS`| Lấy thông tin về các method được hỗ trợ   | Có         | Có   |

> **Idempotent:** Gọi nhiều lần cho kết quả giống nhau.  
> **Safe:** Không thay đổi trạng thái server.

---

## Phần 3: HTTP Status Codes

### 2xx – Thành công

| Code  | Tên                | Ý nghĩa                              |
|-------|--------------------|--------------------------------------|
| `200` | OK                 | Request thành công                   |
| `201` | Created            | Tạo resource mới thành công          |
| `204` | No Content         | Thành công nhưng không có dữ liệu trả về |

### 3xx – Chuyển hướng

| Code  | Tên                | Ý nghĩa                              |
|-------|--------------------|--------------------------------------|
| `301` | Moved Permanently  | URI đã thay đổi vĩnh viễn            |
| `304` | Not Modified       | Dữ liệu chưa thay đổi (dùng cache)  |

### 4xx – Lỗi từ phía Client

| Code  | Tên                  | Ý nghĩa                              |
|-------|----------------------|--------------------------------------|
| `400` | Bad Request          | Request không hợp lệ                 |
| `401` | Unauthorized         | Chưa xác thực                        |
| `403` | Forbidden            | Không có quyền truy cập              |
| `404` | Not Found            | Không tìm thấy resource              |
| `422` | Unprocessable Entity | Dữ liệu không hợp lệ về mặt logic   |
| `429` | Too Many Requests    | Vượt quá giới hạn request (rate limit)|

### 5xx – Lỗi từ phía Server

| Code  | Tên                    | Ý nghĩa                              |
|-------|------------------------|--------------------------------------|
| `500` | Internal Server Error  | Lỗi không xác định phía server       |
| `502` | Bad Gateway            | Server nhận response không hợp lệ    |
| `503` | Service Unavailable    | Server tạm thời không khả dụng       |
| `504` | Gateway Timeout        | Server không phản hồi kịp thời       |

---

## Phần 4: HTTP Headers quan trọng

### Request Headers

| Header            | Mô tả                                         |
|-------------------|-----------------------------------------------|
| `Authorization`   | Thông tin xác thực (Bearer token, Basic auth) |
| `Content-Type`    | Định dạng dữ liệu gửi lên (`application/json`)|
| `Accept`          | Định dạng dữ liệu client muốn nhận            |
| `User-Agent`      | Thông tin về client                           |
| `Cache-Control`   | Chính sách cache của request                  |

### Response Headers

| Header              | Mô tả                                       |
|---------------------|---------------------------------------------|
| `Content-Type`      | Định dạng dữ liệu trả về                    |
| `Cache-Control`     | Chính sách cache của response               |
| `ETag`              | Định danh phiên bản của resource            |
| `X-RateLimit-Limit` | Giới hạn số request được phép              |
| `Location`          | URI của resource mới tạo (dùng với 201)     |
