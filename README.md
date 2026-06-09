# ProGym - Gym Management System

ProGym là hệ thống quản lý trung tâm thể hình được xây dựng bằng **Python Flask** và **MySQL**, phục vụ cho chuyên đề tốt nghiệp ngành **Khoa học máy tính**.

Hệ thống mô phỏng các nghiệp vụ vận hành thực tế tại một phòng gym/trung tâm thể hình, bao gồm quản lý hội viên, gói tập, đăng ký gói, thanh toán, check-in/check-out, huấn luyện viên cá nhân, lịch tập PT, thiết bị, bảo trì và báo cáo.

---

## Tính năng

* Đăng nhập và phân quyền theo vai trò: Admin, Lễ tân, PT.
* Quản lý thông tin hội viên, trạng thái hội viên và lịch sử sử dụng dịch vụ.
* Quản lý gói tập thường và gói tập có PT.
* Đăng ký gói tập cho hội viên.
* Ghi nhận thanh toán bằng tiền mặt hoặc chuyển khoản.
* Theo dõi trạng thái thanh toán và trạng thái hiệu lực gói tập.
* Ghi nhận check-in/check-out của hội viên.
* Quản lý huấn luyện viên cá nhân và phân công PT cho hội viên.
* Tạo lịch tập PT, kiểm tra trùng lịch và cập nhật trạng thái buổi tập.
* Quản lý thiết bị phòng tập và phiếu bảo trì thiết bị.
* Theo dõi báo cáo tổng quan về hội viên, doanh thu, check-in, lịch tập và thiết bị.

---

## Yêu cầu hệ thống

| Công cụ            | Phiên bản khuyến nghị | Mục đích                    |
| ------------------ | --------------------- | --------------------------- |
| Python             | 3.10+                 | Chạy ứng dụng Flask         |
| MySQL              | 8.0+                  | Lưu trữ cơ sở dữ liệu       |
| XAMPP/phpMyAdmin   | Mới nhất              | Quản lý và import database  |
| Git                | Mới nhất              | Clone và quản lý mã nguồn   |
| Visual Studio Code | Mới nhất              | Mở và chỉnh sửa source code |
| Trình duyệt web    | Chrome/Edge           | Truy cập giao diện hệ thống |

Kiểm tra phiên bản Python và Git:

```bash
python --version
git --version
```

---

## Công nghệ sử dụng

| Thành phần      | Công nghệ         |
| --------------- | ----------------- |
| Backend         | Python Flask      |
| Database        | MySQL             |
| Frontend        | HTML, CSS, Jinja2 |
| UI Icons        | Bootstrap Icons   |
| Database Tool   | XAMPP, phpMyAdmin |
| Version Control | Git, GitHub       |

---

## Cài đặt

### Bước 1 — Clone repository

```bash
git clone https://github.com/hoang-duc-24/progym-gym-management-flask.git
cd progym-gym-management-flask
```

### Bước 2 — Tạo và kích hoạt môi trường ảo

Tạo môi trường ảo:

```bash
python -m venv venv
```

Kích hoạt môi trường ảo trên Windows:

```bash
venv\Scripts\activate
```

### Bước 3 — Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### Bước 4 — Tạo database MySQL

Mở phpMyAdmin và tạo database mới với tên:

```text
progym_final
```

Khuyến nghị chọn collation:

```text
utf8mb4_unicode_ci
```

### Bước 5 — Import database

Import file SQL sau vào database vừa tạo:

```text
database/progym_db.sql
```

Thao tác trên phpMyAdmin:

```text
phpMyAdmin → chọn database progym_final → Import → chọn file progym_db.sql → Go
```

### Bước 6 — Cấu hình kết nối database

Mở file:

```text
config.py
```

Kiểm tra lại thông tin kết nối MySQL:

```python
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "progym_final"
DB_PORT = 3307
```

Lưu ý:

* Nếu MySQL chạy ở port `3306`, đổi `DB_PORT` thành `3306`.
* Nếu MySQL có mật khẩu, cập nhật lại `DB_PASSWORD`.
* Tên database trong `config.py` phải trùng với database đã tạo trong phpMyAdmin.

### Bước 7 — Chạy dự án

```bash
python run.py
```

Sau khi Flask khởi chạy thành công, mở trình duyệt và truy cập:

```text
http://127.0.0.1:5000
```

---

## Tài khoản demo

| Vai trò | Tài khoản | Mật khẩu   |
| ------- | --------- | ---------- |
| Admin   | admin     | Admin@2026 |
| Lễ tân  | letan     | Letan@2026 |
| PT      | ptha      | 123456     |

Lưu ý: tài khoản demo có thể thay đổi theo dữ liệu trong bảng `TaiKhoan` của database.

---

## Cấu trúc dự án

```text
ProGym-Flask/
├── app/
│   ├── repositories/          # Truy vấn và thao tác dữ liệu với MySQL
│   ├── routes/                # Định tuyến và tiếp nhận request từ người dùng
│   ├── services/              # Xử lý nghiệp vụ của hệ thống
│   ├── static/
│   │   ├── css/               # File định dạng giao diện
│   │   ├── img/               # Hình ảnh sử dụng trong hệ thống
│   │   └── js/                # File JavaScript
│   ├── templates/             # Giao diện HTML/Jinja2
│   ├── utils/                 # Hàm tiện ích dùng chung
│   ├── __init__.py
│   └── db.py                  # Kết nối cơ sở dữ liệu
├── database/
│   └── progym_db.sql          # File khởi tạo database và dữ liệu mẫu
├── config.py                  # Cấu hình hệ thống
├── requirements.txt           # Danh sách thư viện Python
├── run.py                     # File khởi chạy ứng dụng Flask
├── .gitignore
└── README.md
```

---

## Module chính

### Quản lý hội viên

* Thêm mới hội viên.
* Cập nhật thông tin hội viên.
* Tìm kiếm và lọc hội viên.
* Xem chi tiết hội viên.
* Theo dõi gói đã đăng ký, thanh toán, lịch sử check-in, phân công PT và lịch tập PT.
* Chuyển hội viên sang trạng thái ngừng hoạt động.
* Chặn đăng ký gói và check-in đối với hội viên ngừng hoạt động.

### Quản lý gói tập

* Quản lý danh sách gói tập.
* Phân loại gói có PT và không PT.
* Theo dõi thời hạn gói, số buổi PT và giá gói.
* Thêm, sửa thông tin gói tập.
* Theo dõi trạng thái áp dụng của gói tập.

### Đăng ký gói và thanh toán

* Đăng ký gói mới cho hội viên.
* Tính ngày bắt đầu và ngày kết thúc gói.
* Ghi nhận số tiền phải trả.
* Ghi nhận thanh toán bằng tiền mặt hoặc chuyển khoản.
* Theo dõi trạng thái thanh toán và hiệu lực dịch vụ.
* Hỗ trợ gói thường và gói PT.

### Check-in/Check-out

* Tìm kiếm hội viên để check-in.
* Kiểm tra điều kiện sử dụng dịch vụ của hội viên.
* Ghi nhận thời gian vào và thời gian ra.
* Theo dõi lịch sử check-in/check-out của từng hội viên.

### PT và lịch tập

* Quản lý danh sách huấn luyện viên cá nhân.
* Phân công PT cho hội viên đăng ký gói PT.
* Tạo lịch tập PT.
* Kiểm tra trùng lịch PT.
* Cập nhật trạng thái buổi tập.
* Tự động trừ số buổi PT khi buổi tập hoàn thành.

### Thiết bị và bảo trì

* Quản lý danh sách thiết bị phòng tập.
* Thêm và cập nhật thông tin thiết bị.
* Theo dõi trạng thái thiết bị: đang sử dụng, cần bảo trì, đang bảo trì, ngừng sử dụng.
* Ghi nhận phiếu bảo trì thiết bị.
* Cập nhật kết quả bảo trì và tình trạng thiết bị sau bảo trì.

### Báo cáo

* Báo cáo tổng quan hội viên.
* Báo cáo doanh thu.
* Báo cáo đăng ký gói.
* Báo cáo check-in/check-out.
* Báo cáo lịch tập PT.
* Báo cáo thiết bị và bảo trì.

---

## Quy tắc nghiệp vụ chính

### Hội viên

* Hội viên đang hoạt động có thể đăng ký gói và check-in.
* Hội viên ngừng hoạt động không được đăng ký gói mới.
* Hội viên ngừng hoạt động không được check-in.

### Gói tập và thanh toán

* Gói không PT được theo dõi theo thời hạn sử dụng.
* Gói có PT được theo dõi theo thời hạn sử dụng và số buổi PT còn lại.
* Đăng ký gói phát sinh số tiền cần thanh toán.
* Hệ thống ghi nhận số tiền đã thanh toán và trạng thái thanh toán.
* Hội viên cần có gói đủ điều kiện sử dụng để thực hiện check-in.

### Check-in/Check-out

* Chỉ hội viên có gói đã thanh toán và còn hiệu lực mới được check-in.
* Mỗi lượt check-in cần ghi nhận thời gian vào và thời gian ra.
* Lịch sử check-in/check-out được lưu để phục vụ theo dõi hoạt động hội viên.

### PT và lịch tập

* Một PT không được có hai lịch tập trùng thời gian.
* Số buổi PT chỉ giảm khi buổi tập được cập nhật hoàn thành.
* Lịch tập phải nằm trong thời hạn gói PT.
* PT chỉ theo dõi và cập nhật các lịch tập thuộc phạm vi được phân công.

### Thiết bị và bảo trì

* Thiết bị mới mặc định ở trạng thái đang sử dụng.
* Khi tạo phiếu bảo trì chờ xử lý, thiết bị được cập nhật sang trạng thái đang bảo trì.
* Khi hoàn thành bảo trì, thiết bị được cập nhật về trạng thái sau bảo trì.
* Thiết bị đang có phiếu bảo trì chưa hoàn thành không được tạo thêm phiếu bảo trì mới.

---

## Luồng demo đề xuất

### Luồng 1 — Đăng nhập hệ thống

1. Mở trang đăng nhập.
2. Đăng nhập bằng tài khoản Admin hoặc Lễ tân.
3. Kiểm tra giao diện chính sau đăng nhập.

### Luồng 2 — Quản lý hội viên

1. Vào module Hội viên.
2. Tìm kiếm hội viên.
3. Xem chi tiết hội viên.
4. Kiểm tra các tab: dịch vụ đã đăng ký, thanh toán, lịch sử check-in, phân công PT và lịch tập PT.
5. Chuyển một hội viên sang trạng thái ngừng hoạt động nếu cần kiểm tra ràng buộc nghiệp vụ.

### Luồng 3 — Đăng ký gói và thanh toán

1. Chọn một hội viên đang hoạt động.
2. Đăng ký thêm gói tập.
3. Ghi nhận thanh toán.
4. Kiểm tra gói mới trong chi tiết hội viên.
5. Kiểm tra phiếu thanh toán được tạo.

### Luồng 4 — Check-in/Check-out

1. Vào module Check-in/Check-out.
2. Tìm hội viên có gói hợp lệ.
3. Thực hiện check-in.
4. Thực hiện check-out.
5. Kiểm tra lịch sử check-in/check-out trong chi tiết hội viên.

### Luồng 5 — PT và lịch tập

1. Chọn hội viên có gói PT.
2. Kiểm tra phân công PT.
3. Tạo lịch tập PT.
4. Kiểm tra hệ thống chặn trùng lịch PT.
5. Cập nhật trạng thái buổi tập.

### Luồng 6 — Thiết bị và bảo trì

1. Vào module Thiết bị.
2. Thêm hoặc chọn một thiết bị.
3. Ghi nhận phiếu bảo trì.
4. Kiểm tra trạng thái thiết bị sau khi tạo phiếu bảo trì.
5. Xử lý hoàn thành phiếu bảo trì.
6. Kiểm tra trạng thái thiết bị sau bảo trì.

### Luồng 7 — Báo cáo

1. Vào module Báo cáo.
2. Kiểm tra số liệu tổng quan.
3. Đối chiếu nhanh với dữ liệu trong hệ thống nếu cần.

---

## Các lệnh thường dùng

Kiểm tra trạng thái Git:

```bash
git status
```

Thêm toàn bộ thay đổi:

```bash
git add .
```

Commit thay đổi:

```bash
git commit -m "Update ProGym project"
```

Đẩy source code lên GitHub:

```bash
git push origin main
```

Chạy ứng dụng:

```bash
python run.py
```

---

## Lỗi thường gặp

### Không kết nối được MySQL

Nguyên nhân thường gặp:

* MySQL chưa được bật trong XAMPP.
* Sai `DB_PORT`.
* Sai tên database trong `config.py`.
* Chưa import file `database/progym_db.sql`.

Cách xử lý:

* Bật MySQL trong XAMPP.
* Kiểm tra port MySQL đang chạy là `3306` hay `3307`.
* Kiểm tra `DB_NAME` trong `config.py`.
* Import lại file SQL bằng phpMyAdmin.

### Không đăng nhập được tài khoản demo

Nguyên nhân thường gặp:

* Chưa import đúng database.
* Dữ liệu tài khoản trong bảng `TaiKhoan` đã bị thay đổi.
* Nhập sai tài khoản hoặc mật khẩu.

Cách xử lý:

* Kiểm tra lại bảng `TaiKhoan` trong phpMyAdmin.
* Dùng đúng tài khoản demo được ghi trong README.
* Import lại database nếu cần.

### Không hiển thị ảnh thiết bị hoặc ảnh giao diện

Nguyên nhân thường gặp:

* File ảnh không nằm trong thư mục `app/static/img`.
* Đường dẫn ảnh trong database hoặc trong template không đúng.
* Trình duyệt đang cache dữ liệu cũ.

Cách xử lý:

* Kiểm tra file ảnh trong `app/static/img`.
* Kiểm tra đường dẫn ảnh đang được lưu trong database.
* Tải lại trang bằng `Ctrl + F5`.


---

## Tác giả

Sinh viên thực hiện: **Hoàng Minh Đức**
Mã sinh viên: **A44844**
Ngành: **Khoa học máy tính**
Trường: **Đại học Thăng Long**

Repository: https://github.com/hoang-duc-24/progym-gym-management-flask
