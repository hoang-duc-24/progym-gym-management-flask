# ProGym - Gym Management System

ProGym là hệ thống quản lý trung tâm thể hình được xây dựng bằng **Flask** và **MySQL**, phục vụ cho chuyên đề tốt nghiệp ngành Khoa học máy tính.

Hệ thống tập trung mô phỏng các nghiệp vụ vận hành thực tế tại một phòng gym/trung tâm thể hình, bao gồm quản lý hội viên, gói tập, đăng ký dịch vụ, thanh toán, check-in, PT, lịch tập, thiết bị, bảo trì và báo cáo.

---

## 1. Mục tiêu dự án

Dự án được xây dựng nhằm hỗ trợ nhân sự vận hành trung tâm thể hình trong các nghiệp vụ chính:

* Quản lý thông tin hội viên.
* Quản lý gói tập và gói PT.
* Đăng ký gói tập cho hội viên.
* Theo dõi thanh toán và công nợ.
* Ghi nhận check-in / check-out.
* Quản lý PT, phân công PT và lịch tập PT.
* Quản lý thiết bị phòng tập và lịch sử bảo trì.
* Theo dõi báo cáo tổng quan về hội viên, doanh thu, check-in và thiết bị.

---

## 2. Công nghệ sử dụng

| Thành phần      | Công nghệ          |
| --------------- | ------------------ |
| Backend         | Python Flask       |
| Database        | MySQL              |
| Frontend        | HTML, CSS, Jinja2  |
| UI Library      | Bootstrap Icons    |
| Database Tool   | phpMyAdmin / XAMPP |
| Version Control | Git, GitHub        |

---

## 3. Chức năng chính

### 3.1. Quản lý hội viên

* Thêm mới hội viên.
* Cập nhật thông tin hội viên.
* Tìm kiếm và lọc hội viên.
* Xem chi tiết hội viên.
* Theo dõi các gói đã đăng ký.
* Theo dõi lịch sử thanh toán.
* Theo dõi lịch sử check-in.
* Chuyển hội viên sang trạng thái ngừng hoạt động.
* Chặn đăng ký gói và check-in đối với hội viên ngừng hoạt động.

### 3.2. Quản lý gói tập

* Quản lý danh sách gói tập.
* Phân loại gói có PT và không PT.
* Theo dõi thời hạn gói, số buổi PT và giá gói.
* Thêm, sửa thông tin gói tập.

### 3.3. Đăng ký gói tập

* Đăng ký gói mới cho hội viên.
* Tự động tính ngày bắt đầu, ngày kết thúc.
* Ghi nhận số tiền phải trả.
* Theo dõi trạng thái thanh toán.
* Theo dõi trạng thái hiệu lực dịch vụ.
* Hỗ trợ gói thường và gói PT.

### 3.4. Thanh toán

* Ghi nhận thanh toán khi đăng ký gói.
* Hỗ trợ thanh toán tiền mặt và chuyển khoản.
* Theo dõi trạng thái đã thanh toán, chưa thanh toán, thanh toán một phần.
* Đối soát số tiền phải trả và số tiền đã thu.

### 3.5. Check-in / Check-out

* Check-in hội viên có gói hợp lệ.
* Chặn check-in nếu hội viên ngừng hoạt động hoặc không có gói hiệu lực.
* Ghi nhận thời gian vào, thời gian ra.
* Theo dõi lịch sử check-in của từng hội viên.

### 3.6. Quản lý PT và lịch tập

* Quản lý danh sách huấn luyện viên cá nhân.
* Phân công PT cho hội viên đăng ký gói PT.
* Tạo lịch tập PT.
* Chặn trùng lịch PT.
* Cập nhật trạng thái buổi tập.
* Tự động trừ số buổi PT khi buổi tập hoàn thành.

### 3.7. Quản lý thiết bị và bảo trì

* Quản lý danh sách thiết bị phòng tập.
* Thêm và cập nhật thông tin thiết bị.
* Theo dõi tình trạng thiết bị: đang sử dụng, đang bảo trì, ngừng sử dụng.
* Ghi nhận phiếu bảo trì thiết bị.
* Tự động chuyển thiết bị sang trạng thái đang bảo trì khi có phiếu bảo trì đang mở.
* Cập nhật kết quả bảo trì và tình trạng thiết bị sau bảo trì.

### 3.8. Báo cáo

* Báo cáo tổng quan hội viên.
* Báo cáo doanh thu.
* Báo cáo đăng ký gói.
* Báo cáo check-in.
* Báo cáo thiết bị và bảo trì.

---

## 4. Cấu trúc thư mục chính

```text
ProGym-Flask/
├── app/
│   ├── repositories/
│   ├── routes/
│   ├── services/
│   ├── static/
│   │   ├── css/
│   │   ├── img/
│   │   ├── js/
│   │   └── uploads/
│   ├── templates/
│   ├── utils/
│   ├── __init__.py
│   └── db.py
├── database/
│   └── progym_final_clean.sql
├── config.py
├── requirements.txt
├── run.py
├── .gitignore
└── README.md
```

---

## 5. Cài đặt và chạy project

### Bước 1: Clone project

```bash
git clone https://github.com/hoang-duc-24/progym-gym-management-flask.git
cd progym-gym-management-flask
```

### Bước 2: Tạo môi trường ảo

```bash
python -m venv venv
```

Kích hoạt môi trường ảo trên Windows:

```bash
venv\Scripts\activate
```

### Bước 3: Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### Bước 4: Tạo database MySQL

Tạo database mới trong MySQL/phpMyAdmin với tên:

```text
progym_final
```

Khuyến nghị chọn collation:

```text
utf8mb4_unicode_ci
```

### Bước 5: Import database

Import file SQL sau vào database vừa tạo:

```text
database/progym_final_clean.sql
```

Có thể import bằng phpMyAdmin:

```text
phpMyAdmin → chọn database progym_final → Import → chọn file progym_final_clean.sql → Go
```

### Bước 6: Cấu hình kết nối database

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

* Nếu MySQL của bạn chạy port `3306`, đổi `DB_PORT` thành `3306`.
* Nếu MySQL có mật khẩu, cập nhật lại `DB_PASSWORD`.

### Bước 7: Chạy ứng dụng

```bash
python run.py
```

Sau đó mở trình duyệt:

```text
http://127.0.0.1:5000
```

---

## 6. Tài khoản demo

| Vai trò | Tài khoản | Mật khẩu |
| ------- | --------- | -------- |
| Admin   | admin     | 123456   |
| Lễ tân  | letan     | 123456   |
| PT      | pt        | 123456   |

Lưu ý: tài khoản demo có thể thay đổi theo dữ liệu trong bảng `TaiKhoan` của database.

---

## 7. Luồng demo đề xuất

Có thể demo hệ thống theo thứ tự sau:

### Luồng 1: Đăng nhập hệ thống

1. Mở trang đăng nhập.
2. Đăng nhập bằng tài khoản Admin hoặc Lễ tân.
3. Kiểm tra giao diện chính sau đăng nhập.

### Luồng 2: Quản lý hội viên

1. Vào module Hội viên.
2. Tìm kiếm hội viên.
3. Xem chi tiết hội viên.
4. Kiểm tra các tab: dịch vụ đã đăng ký, thanh toán, lịch sử check-in, phân công PT, lịch tập PT.
5. Thử chuyển một hội viên hết hạn gói sang trạng thái ngừng hoạt động.

### Luồng 3: Đăng ký gói và thanh toán

1. Chọn một hội viên đang hoạt động.
2. Đăng ký thêm gói tập.
3. Ghi nhận thanh toán.
4. Kiểm tra gói mới trong chi tiết hội viên.
5. Kiểm tra phiếu thanh toán được tạo.

### Luồng 4: Check-in / Check-out

1. Vào module Check-in.
2. Tìm hội viên có gói hiệu lực.
3. Thực hiện check-in.
4. Thực hiện check-out.
5. Kiểm tra lịch sử check-in trong chi tiết hội viên.

### Luồng 5: PT và lịch tập

1. Chọn hội viên có gói PT.
2. Kiểm tra phân công PT.
3. Tạo lịch tập PT.
4. Kiểm tra hệ thống chặn trùng lịch PT.
5. Cập nhật trạng thái buổi tập.

### Luồng 6: Thiết bị và bảo trì

1. Vào module Thiết bị.
2. Thêm thiết bị mới.
3. Ghi nhận phiếu bảo trì.
4. Kiểm tra thiết bị chuyển sang trạng thái đang bảo trì.
5. Xử lý phiếu bảo trì.
6. Kiểm tra thiết bị quay về trạng thái sau bảo trì.

### Luồng 7: Báo cáo

1. Vào module Báo cáo.
2. Kiểm tra số liệu tổng quan.
3. Đối chiếu nhanh với dữ liệu trong database nếu cần.

---

## 8. Một số quy tắc nghiệp vụ chính

### Hội viên

* Hội viên đang hoạt động có thể đăng ký gói và check-in.
* Hội viên ngừng hoạt động không được đăng ký gói mới.
* Hội viên ngừng hoạt động không được check-in.

### Gói tập

* Gói không PT được theo dõi theo số ngày còn lại.
* Gói có PT được theo dõi theo số buổi PT còn lại.
* Gói hết hạn khi quá ngày kết thúc hoặc hết số buổi PT.

### Check-in

* Chỉ hội viên có gói đã thanh toán và còn hiệu lực mới được check-in.
* Mỗi lượt check-in cần có thời gian vào và thời gian ra.
* Lịch sử check-in được lưu để phục vụ theo dõi hoạt động hội viên.

### PT và lịch tập

* Một PT không được có hai lịch tập trùng thời gian.
* Số buổi PT chỉ giảm khi buổi tập được cập nhật hoàn thành.
* Lịch tập phải nằm trong thời hạn gói PT.

### Thiết bị và bảo trì

* Thiết bị mới mặc định ở trạng thái đang sử dụng.
* Khi tạo phiếu bảo trì chờ xử lý, thiết bị tự động chuyển sang đang bảo trì.
* Khi hoàn thành bảo trì, thiết bị được cập nhật về trạng thái sau bảo trì.
* Thiết bị đang có phiếu bảo trì chưa hoàn thành không được tạo thêm phiếu bảo trì mới.

---

## 9. Ghi chú triển khai

Dự án hiện được cấu hình để chạy ở môi trường local bằng Flask và MySQL.

Một số điểm có thể phát triển thêm trong tương lai:

* Mã hóa mật khẩu người dùng.
* Phân quyền chi tiết hơn theo từng thao tác.
* Ghi log hệ thống.
* Xuất báo cáo ra Excel/PDF.
* Triển khai hệ thống lên cloud.
* Tối ưu giao diện cho nhiều kích thước màn hình.
* Bổ sung kiểm thử tự động.

---

## 10. Tác giả

Dự án được thực hiện phục vụ mục đích học tập và demo đồ án tốt nghiệp.

Repository: https://github.com/hoang-duc-24/progym-gym-management-flask
