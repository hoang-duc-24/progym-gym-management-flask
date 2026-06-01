from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation
from app.repositories.members_repository import (
    get_members_with_current_package,
    count_members_with_current_package,
    get_member_by_id,
    get_member_by_phone,
    get_member_registrations,
    get_member_payments,
    get_member_checkins,
    get_member_schedules,
    get_active_packages,
    get_package_by_id,
    insert_member,
    insert_registration,
    get_pt_registration_for_assignment,
    get_active_pts,
    get_active_assignment_by_registration,
    insert_pt_assignment,
    close_current_assignment,
    get_assignments_by_member,
    get_assignment_for_schedule,
    get_pt_schedule_conflict,
    get_member_schedule_conflict,
    insert_training_schedule,
    get_schedule_for_update,
    update_schedule_status,
    decrease_remaining_pt_session,
    increase_remaining_pt_session,
    mark_registration_expired_if_no_sessions,
    get_member_for_edit,
    update_member_basic_info,
    count_open_member_registrations,
    count_open_same_package_registration,
)

from app.repositories.workout_logs_repository import (
    get_workout_log_with_details_by_schedule,
    insert_workout_log,
    insert_many_exercise_details,
)

def format_date(value):
    if not value:
        return ""

    if isinstance(value, str):
        return value

    return value.strftime("%d/%m/%Y")


def get_remaining_text(member):
    package_name = member.get("ten_goi_tap")

    if not package_name:
        return "-"

    package_type = member.get("loai_goi")
    total_sessions = member.get("so_buoi_pt_ban_dau")
    remaining_sessions = member.get("so_buoi_pt_con_lai")
    end_date = member.get("ngay_ket_thuc")

    if package_type == "CO_PT":
        total = total_sessions or 0
        remaining = remaining_sessions or 0
        return f"{remaining}/{total} buổi"

    if end_date:
        today = date.today()
        days_left = (end_date - today).days

        if days_left < 0:
            return "0 ngày"

        return f"{days_left} ngày"

    return "-"


def get_payment_label(status):
    mapping = {
        "DA_THANH_TOAN": ("Đã thanh toán", "badge-green"),
        "CHUA_THANH_TOAN": ("Chưa thanh toán", "badge-orange"),
        "THANH_TOAN_MOT_PHAN": ("Thanh toán một phần", "badge-orange"),
    }

    return mapping.get(status, ("Chưa rõ", "badge-gray"))


def get_service_label(member):
    payment_status = member.get("trang_thai_thanh_toan")
    service_status = member.get("trang_thai_hieu_luc")
    end_date = member.get("ngay_ket_thuc")
    package_type = member.get("loai_goi")
    remaining_sessions = member.get("so_buoi_pt_con_lai")

    if not member.get("ma_dang_ky"):
        return "Chưa đăng ký", "badge-gray"

    # Quy tắc nghiệp vụ chính thức của ProGym:
    # Chưa thanh toán đủ thì chưa được kích hoạt dịch vụ.
    if payment_status != "DA_THANH_TOAN":
        return "Chưa kích hoạt", "badge-gray"

    if service_status == "CHUA_KICH_HOAT":
        return "Chưa kích hoạt", "badge-gray"

    if service_status == "TAM_DUNG":
        return "Tạm dừng", "badge-gray"

    if service_status == "DA_HUY":
        return "Đã hủy", "badge-red"

    if service_status == "HET_HAN":
        return "Hết hạn", "badge-red"

    if service_status == "SAP_HET_HAN":
        return "Sắp hết hạn", "badge-orange"

    if package_type == "CO_PT" and remaining_sessions is not None and remaining_sessions <= 0:
        return "Hết buổi", "badge-red"

    if end_date:
        days_left = (end_date - date.today()).days

        if days_left < 0:
            return "Hết hạn", "badge-red"

        if days_left <= 3:
            return "Sắp hết hạn", "badge-orange"

    if service_status == "DANG_HIEU_LUC":
        return "Đang hiệu lực", "badge-green"

    return "Chưa rõ", "badge-gray"

def build_member_rows(filters=None, page=1, per_page=10):
    filters = filters or {}

    total_records = count_members_with_current_package(filters)
    total_pages = (total_records + per_page - 1) // per_page if total_records > 0 else 1

    if page > total_pages:
        page = total_pages

    offset = (page - 1) * per_page

    raw_members = get_members_with_current_package(
        filters=filters,
        limit=per_page,
        offset=offset
    )

    rows = []

    for item in raw_members:
        payment_text, payment_class = get_payment_label(item.get("trang_thai_thanh_toan"))
        service_text, service_class = get_service_label(item)

        rows.append({
            "ma_hoi_vien": item.get("ma_hoi_vien"),
            "ma_khach_hang": f"CUS{item.get('ma_hoi_vien'):06d}",
            "ho_ten": item.get("ho_ten"),
            "so_dien_thoai": item.get("so_dien_thoai"),
            "ten_goi_tap": item.get("ten_goi_tap") or "Chưa có gói",
            "con_lai": get_remaining_text(item),
            "ngay_bat_dau": format_date(item.get("ngay_bat_dau")),
            "ngay_ket_thuc": format_date(item.get("ngay_ket_thuc")),
            "payment_text": payment_text,
            "payment_class": payment_class,
            "service_text": service_text,
            "service_class": service_class,
        })

    return {
        "rows": rows,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total_records": total_records,
            "total_pages": total_pages,
            "start_record": offset + 1 if total_records > 0 else 0,
            "end_record": min(offset + per_page, total_records),
        }
    }

def format_datetime(value):
    if not value:
        return ""

    if isinstance(value, str):
        return value

    return value.strftime("%d/%m/%Y %H:%M")


def format_time(value):
    if not value:
        return ""

    if isinstance(value, str):
        return value

    # PyMySQL có thể trả cột TIME của MySQL về dạng datetime.timedelta
    if isinstance(value, timedelta):
        total_seconds = int(value.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{hours:02d}:{minutes:02d}"

    return value.strftime("%H:%M")


def normalize_db_date(value):
    if isinstance(value, str):
        return date.fromisoformat(value)

    return value


def build_schedule_datetime(training_date, start_time, end_time):
    if not training_date:
        raise ValueError("Vui lòng chọn ngày tập.")

    if not start_time:
        raise ValueError("Vui lòng chọn giờ bắt đầu.")

    if not end_time:
        raise ValueError("Vui lòng chọn giờ kết thúc.")

    schedule_start = datetime.strptime(
        f"{training_date} {start_time[:5]}",
        "%Y-%m-%d %H:%M"
    )

    schedule_end = datetime.strptime(
        f"{training_date} {end_time[:5]}",
        "%Y-%m-%d %H:%M"
    )

    if schedule_end <= schedule_start:
        raise ValueError("Giờ kết thúc phải lớn hơn giờ bắt đầu.")

    if schedule_start <= datetime.now():
        raise ValueError("Không thể tạo lịch tập có giờ bắt đầu đã qua.")

    return schedule_start, schedule_end


def format_money(value):
    if value is None:
        return "0 đ"

    return f"{value:,.0f} đ"


def format_money_input(value):
    if value is None:
        return "0"

    amount = Decimal(str(value))

    if amount == amount.to_integral_value():
        return str(int(amount))

    return str(amount.normalize())


def get_member_status_label(status):
    mapping = {
        "HOAT_DONG": ("Hoạt động", "badge-green"),
        "NGUNG_HOAT_DONG": ("Ngừng hoạt động", "badge-gray"),
    }

    return mapping.get(status, ("Chưa rõ", "badge-gray"))


def get_package_type_label(package_type):
    mapping = {
        "CO_PT": "Có PT",
        "KHONG_PT": "Không PT",
    }

    return mapping.get(package_type, "Chưa rõ")


def get_registration_remaining_text(registration):
    package_type = registration.get("loai_goi")
    total_sessions = registration.get("so_buoi_pt_ban_dau")
    remaining_sessions = registration.get("so_buoi_pt_con_lai")
    end_date = registration.get("ngay_ket_thuc")

    if package_type == "CO_PT":
        return f"{remaining_sessions or 0}/{total_sessions or 0} buổi"

    if end_date:
        days_left = (end_date - date.today()).days
        return f"{max(days_left, 0)} ngày"

    return "-"


def build_registration_rows(registrations):
    rows = []

    for item in registrations:
        payment_text, payment_class = get_payment_label(item.get("trang_thai_thanh_toan"))
        service_text, service_class = get_service_label(item)

        rows.append({
            "ma_dang_ky": item.get("ma_dang_ky"),
            "ten_goi_tap": item.get("ten_goi_tap"),
            "loai_goi": get_package_type_label(item.get("loai_goi")),
            "loai_goi_raw": item.get("loai_goi"),
            "ngay_dang_ky": format_date(item.get("ngay_dang_ky")),
            "ngay_bat_dau": format_date(item.get("ngay_bat_dau")),
            "ngay_ket_thuc": format_date(item.get("ngay_ket_thuc")),
            "con_lai": get_registration_remaining_text(item),
            "tong_tien_phai_tra": format_money(item.get("tong_tien_phai_tra")),
            "payment_text": payment_text,
            "payment_class": payment_class,
            "service_text": service_text,
            "service_class": service_class,
            "payment_status": item.get("trang_thai_thanh_toan"),
            "service_status_raw": item.get("trang_thai_hieu_luc"),
            "can_pay": item.get("trang_thai_thanh_toan") != "DA_THANH_TOAN",
            "can_assign_pt": (
                item.get("loai_goi") == "CO_PT"
                and item.get("trang_thai_thanh_toan") == "DA_THANH_TOAN"
                and item.get("trang_thai_hieu_luc") in ["DANG_HIEU_LUC", "CHUA_KICH_HOAT"]
            ),
            "ghi_chu": item.get("ghi_chu") or "",
        })

    return rows

def get_payment_method_label(method):
    mapping = {
        "TIEN_MAT": "Tiền mặt",
        "CHUYEN_KHOAN": "Chuyển khoản",
        # "THE": "Thẻ",
        # "KHAC": "Khác",
    }

    return mapping.get(method, method or "-")

def build_payment_rows(payments):
    rows = []

    for item in payments:
        payment_text, payment_class = get_payment_label(item.get("trang_thai_thanh_toan"))

        rows.append({
            "ma_thanh_toan": item.get("ma_thanh_toan"),
            "ma_dang_ky": item.get("ma_dang_ky"),
            "ngay_thanh_toan": format_date(item.get("ngay_thanh_toan")),
            "so_tien": format_money(item.get("so_tien")),
            "hinh_thuc_thanh_toan": get_payment_method_label(item.get("hinh_thuc_thanh_toan")),
            "trang_thai_text": payment_text,
            "trang_thai_class": payment_class,
            "ten_goi_tap": item.get("ten_goi_tap"),
            "nguoi_ghi_nhan": item.get("nguoi_ghi_nhan") or "-",
            "ghi_chu": item.get("ghi_chu") or "",
        })

    return rows

# 2 ham moi them
def get_checkin_type_label(value):
    mapping = {
        "TU_DO": "Tập tự do",
        "THEO_LICH_PT": "Tập với PT",
    }

    return mapping.get(value, value or "-")


def get_checkin_status_label(status):
    mapping = {
        "DANG_CHECKIN": ("Đang trong phòng", "badge-green"),
        "DA_CHECKOUT": ("Đã check-out", "badge-gray"),
        "HUY": ("Đã hủy", "badge-red"),
    }

    return mapping.get(status, ("Chưa rõ", "badge-gray"))

def build_checkin_rows(checkins):
    rows = []

    for item in checkins:
        status_text, status_class = get_checkin_status_label(item.get("trang_thai"))

        rows.append({
            "ma_check": item.get("ma_check"),
            "ten_goi_tap": item.get("ten_goi_tap") or "-",
            "thoi_gian_check_in": format_datetime(item.get("thoi_gian_check_in")),
            "thoi_gian_check_out": format_datetime(item.get("thoi_gian_check_out")) or "-",
            "loai_checkin": get_checkin_type_label(item.get("loai_checkin")),
            "trang_thai": status_text,
            "trang_thai_class": status_class,
            "ghi_chu": item.get("ghi_chu") or "-",
        })

    return rows


def get_schedule_status_label(status):
    mapping = {
        "DA_LEN_LICH": ("Đã lên lịch", "badge-green"),
        "HOAN_THANH": ("Hoàn thành", "badge-green"),
        "HOAN": ("Không diễn ra", "badge-orange"),
        "HUY": ("Không diễn ra", "badge-orange"),
    }

    return mapping.get(status, ("Chưa rõ", "badge-gray"))


def build_schedule_rows(schedules):
    rows = []

    for item in schedules:
        status_text, status_class = get_schedule_status_label(item.get("trang_thai_buoi_tap"))

        rows.append({
            "ma_lich_tap": item.get("ma_lich_tap"),
            "ngay_tap": format_date(item.get("ngay_tap")),
            "gio_bat_dau": format_time(item.get("gio_bat_dau")),
            "gio_ket_thuc": format_time(item.get("gio_ket_thuc")),
            "ten_pt": item.get("ten_pt") or "-",
            "ten_goi_tap": item.get("ten_goi_tap") or "-",
            "status_text": status_text,
            "status_class": status_class,
            "ghi_chu": item.get("ghi_chu") or "",
        })

    return rows


def build_member_detail(member_id):
    member = get_member_by_id(member_id)

    if not member:
        return None

    member_status_text, member_status_class = get_member_status_label(member.get("trang_thai"))

    member_view = {
        "ma_hoi_vien": member.get("ma_hoi_vien"),
        "ma_khach_hang": f"CUS{member.get('ma_hoi_vien'):06d}",
        "ho_ten": member.get("ho_ten"),
        "ngay_sinh": format_date(member.get("ngay_sinh")),
        "gioi_tinh": member.get("gioi_tinh") or "",
        "so_dien_thoai": member.get("so_dien_thoai"),
        "email": member.get("email") or "",
        "dia_chi": member.get("dia_chi") or "",
        "ngay_tham_gia": format_date(member.get("ngay_tham_gia")),
        "trang_thai_text": member_status_text,
        "trang_thai_class": member_status_class,
        "ghi_chu": member.get("ghi_chu") or "",
    }

    registrations = get_member_registrations(member_id)
    payments = get_member_payments(member_id)
    checkins = get_member_checkins(member_id)
    schedules = get_member_schedules(member_id)
    assignments = get_assignments_by_member(member_id)

    return {
        "member": member_view,
        "registrations": build_registration_rows(registrations),
        "payments": build_payment_rows(payments),
        "checkins": build_checkin_rows(checkins),
        "schedules": build_schedule_rows(schedules),
        "assignments": build_assignment_rows(assignments),
    }

def to_input_date(value):
    if not value:
        return ""

    if isinstance(value, str):
        return value

    return value.isoformat()


def build_member_edit_form(member_id):
    member = get_member_for_edit(member_id)

    if not member:
        return None

    return {
        "ma_hoi_vien": member.get("ma_hoi_vien"),
        "ma_khach_hang": f"CUS{member.get('ma_hoi_vien'):06d}",
        "ho_ten": member.get("ho_ten") or "",
        "ngay_sinh": to_input_date(member.get("ngay_sinh")),
        "gioi_tinh": member.get("gioi_tinh") or "NAM",
        "so_dien_thoai": member.get("so_dien_thoai") or "",
        "email": member.get("email") or "",
        "dia_chi": member.get("dia_chi") or "",
        "ngay_tham_gia": format_date(member.get("ngay_tham_gia")),
        "trang_thai": member.get("trang_thai") or "HOAT_DONG",
        "ghi_chu": member.get("ghi_chu") or "",
    }


def update_member_info(member_id, form_data):
    current_member = get_member_for_edit(member_id)

    if not current_member:
        raise ValueError("Không tìm thấy hội viên.")

    ho_ten = form_data.get("ho_ten", "").strip()
    ngay_sinh = form_data.get("ngay_sinh") or None
    gioi_tinh = form_data.get("gioi_tinh", "").strip()
    so_dien_thoai = form_data.get("so_dien_thoai", "").strip()
    email = form_data.get("email", "").strip() or None
    dia_chi = form_data.get("dia_chi", "").strip() or None
    trang_thai = form_data.get("trang_thai", "").strip()
    ghi_chu = form_data.get("ghi_chu", "").strip() or None

    if not ho_ten:
        raise ValueError("Vui lòng nhập họ tên hội viên.")

    if not so_dien_thoai:
        raise ValueError("Vui lòng nhập số điện thoại.")

    if gioi_tinh not in ["NAM", "NU", "KHAC"]:
        raise ValueError("Giới tính không hợp lệ.")

    if trang_thai not in ["HOAT_DONG", "NGUNG_HOAT_DONG"]:
        raise ValueError("Trạng thái hội viên không hợp lệ.")

    existing_member = get_member_by_phone(so_dien_thoai)

    if existing_member and int(existing_member.get("ma_hoi_vien")) != int(member_id):
        raise ValueError("Số điện thoại này đã được sử dụng bởi hội viên khác.")
    
    if trang_thai == "NGUNG_HOAT_DONG":
        open_registration_count = count_open_member_registrations(member_id)

        if open_registration_count > 0:
            raise ValueError(
                "Không thể ngừng hoạt động hội viên khi còn gói đang hiệu lực. "
                "Vui lòng kiểm tra và xử lý các gói đang sử dụng trước."
            )

    update_member_basic_info(
        member_id=member_id,
        data={
            "ho_ten": ho_ten,
            "ngay_sinh": ngay_sinh,
            "gioi_tinh": gioi_tinh,
            "so_dien_thoai": so_dien_thoai,
            "email": email,
            "dia_chi": dia_chi,
            "trang_thai": trang_thai,
            "ghi_chu": ghi_chu,
        }
    )

    return member_id

def parse_decimal(value, field_name):
    if value is None:
        return Decimal("0")

    normalized = str(value).replace(",", "").strip()

    if normalized == "":
        return Decimal("0")

    try:
        amount = Decimal(normalized)
    except InvalidOperation:
        raise ValueError(f"{field_name} không hợp lệ.")

    if amount < 0:
        raise ValueError(f"{field_name} không được nhỏ hơn 0.")

    return amount


def calculate_end_date(start_date_value, duration_days):
    start_date = validate_start_date(start_date_value)

    try:
        duration_days = int(duration_days)
    except (TypeError, ValueError):
        raise ValueError("Thời hạn gói không hợp lệ.")

    if duration_days <= 0:
        raise ValueError("Thời hạn gói phải lớn hơn 0.")

    return start_date + timedelta(days=duration_days - 1)


def calculate_initial_service_status(payment_status, start_date_value, end_date_value):
    if payment_status != "DA_THANH_TOAN":
        return "CHUA_KICH_HOAT"

    today = date.today()
    start_date = date.fromisoformat(start_date_value)

    if isinstance(end_date_value, str):
        end_date = date.fromisoformat(end_date_value)
    else:
        end_date = end_date_value

    if start_date > today:
        return "CHUA_KICH_HOAT"

    if end_date < today:
        return "HET_HAN"

    return "DANG_HIEU_LUC"


def build_member_create_form():
    packages = get_active_packages()

    package_rows = []
    for package in packages:
        package_rows.append({
            "ma_goi_tap": package["ma_goi_tap"],
            "ten_goi_tap": package["ten_goi_tap"],
            "gia_goi": format_money_input(package["gia_goi"]),
            "gia_goi_text": format_money(package["gia_goi"]),
            "thoi_han_ngay": package["thoi_han_ngay"],
            "so_buoi_pt": package["so_buoi_pt"] or 0,
        })

    return {
        "packages": package_rows,
        "today": date.today().isoformat(),
    }


def create_member_with_registration(form_data, account_id):
    ho_ten = form_data.get("ho_ten", "").strip()
    so_dien_thoai = form_data.get("so_dien_thoai", "").strip()
    gioi_tinh = form_data.get("gioi_tinh", "NAM")
    ngay_sinh = form_data.get("ngay_sinh") or None
    email = form_data.get("email", "").strip()
    dia_chi = form_data.get("dia_chi", "").strip()
    ghi_chu_hoi_vien = form_data.get("ghi_chu_hoi_vien", "").strip()

    package_id = form_data.get("ma_goi_tap")
    start_date = form_data.get("ngay_bat_dau")
    payment_amount = parse_decimal(form_data.get("so_tien_thanh_toan"), "Số tiền thanh toán")
    payment_method = form_data.get("hinh_thuc_thanh_toan", "TIEN_MAT")
    registration_note = form_data.get("ghi_chu_dang_ky", "").strip()

    if not ho_ten:
        raise ValueError("Vui lòng nhập họ tên hội viên.")

    if not so_dien_thoai:
        raise ValueError("Vui lòng nhập số điện thoại.")
    
    existing_member = get_member_by_phone(so_dien_thoai)

    if existing_member:
        raise ValueError("Số điện thoại này đã tồn tại trong hệ thống.")

    if not package_id:
        raise ValueError("Vui lòng chọn gói tập.")

    package = get_package_by_id(package_id)
    if not package:
        raise ValueError("Gói tập không tồn tại hoặc đã ngừng áp dụng.")

    if payment_method not in ["TIEN_MAT", "CHUYEN_KHOAN"]:
        raise ValueError("Hình thức thanh toán không hợp lệ.")

    total_amount = Decimal(str(package["gia_goi"] or 0))

    if payment_amount > total_amount:
        raise ValueError("Số tiền thanh toán không được lớn hơn giá gói.")

    if payment_amount == 0:
        payment_status = "CHUA_THANH_TOAN"
    elif payment_amount < total_amount:
        payment_status = "THANH_TOAN_MOT_PHAN"
    else:
        payment_status = "DA_THANH_TOAN"

    end_date = calculate_end_date(start_date, package["thoi_han_ngay"])
    service_status = calculate_initial_service_status(payment_status, start_date, end_date)

    if package["loai_goi"] == "CO_PT":
        initial_sessions = package["so_buoi_pt"] or 0

        if initial_sessions <= 0:
            raise ValueError("Gói PT phải có số buổi PT lớn hơn 0.")
    else:
        initial_sessions = 0

    member_id = insert_member({
        "ho_ten": ho_ten,
        "ngay_sinh": ngay_sinh,
        "gioi_tinh": gioi_tinh,
        "so_dien_thoai": so_dien_thoai,
        "email": email,
        "dia_chi": dia_chi,
        "ghi_chu": ghi_chu_hoi_vien,
    })

    registration_id = insert_registration({
        "ma_hoi_vien": member_id,
        "ma_goi_tap": package["ma_goi_tap"],
        "ngay_bat_dau": start_date,
        "ngay_ket_thuc": end_date,
        "so_buoi_pt_ban_dau": initial_sessions,
        "so_buoi_pt_con_lai": initial_sessions,
        "tong_tien_phai_tra": total_amount,
        "trang_thai_thanh_toan": payment_status,
        "trang_thai_hieu_luc": service_status,
        "ghi_chu": registration_note,
    })

    # Nếu có thanh toán ngay khi tạo hội viên thì ghi nhận vào bảng ThanhToan.
    if payment_amount > 0:
        from app.repositories.payments_repository import insert_payment

        insert_payment(
            registration_id=registration_id,
            account_id=account_id,
            amount=payment_amount,
            payment_method=payment_method,
            note="Thanh toán khi tạo mới hội viên và đăng ký gói"
        )

    return member_id

def build_register_package_form(member_id):
    member = get_member_by_id(member_id)

    if not member:
        return None
    
    if member.get("trang_thai") != "HOAT_DONG":
        raise ValueError("Hội viên đã ngừng hoạt động, không thể đăng ký gói mới.")

    packages = get_active_packages()

    package_rows = []
    for package in packages:
        package_rows.append({
            "ma_goi_tap": package["ma_goi_tap"],
            "ten_goi_tap": package["ten_goi_tap"],
            "loai_goi": "Có PT" if package["loai_goi"] == "CO_PT" else "Không PT",
            "gia_goi": format_money_input(package["gia_goi"]),
            "gia_goi_text": format_money(package["gia_goi"]),
            "thoi_han_ngay": package["thoi_han_ngay"],
            "so_buoi_pt": package["so_buoi_pt"] or 0,
        })

    member_status_text, member_status_class = get_member_status_label(member.get("trang_thai"))

    return {
        "member": {
            "ma_hoi_vien": member.get("ma_hoi_vien"),
            "ma_khach_hang": f"CUS{member.get('ma_hoi_vien'):06d}",
            "ho_ten": member.get("ho_ten"),
            "so_dien_thoai": member.get("so_dien_thoai"),
            "email": member.get("email") or "",
            "trang_thai_text": member_status_text,
            "trang_thai_class": member_status_class,
        },
        "packages": package_rows,
        "today": date.today().isoformat(),
    }


def register_package_for_existing_member(member_id, form_data, account_id):
    member = get_member_by_id(member_id)

    if not member:
        raise ValueError("Không tìm thấy hội viên.")

    if member.get("trang_thai") != "HOAT_DONG":
        raise ValueError("Chỉ có thể đăng ký gói cho hội viên đang hoạt động.")

    package_id = form_data.get("ma_goi_tap")
    start_date = form_data.get("ngay_bat_dau")
    payment_amount = parse_decimal(form_data.get("so_tien_thanh_toan"), "Số tiền thanh toán")
    payment_method = form_data.get("hinh_thuc_thanh_toan", "TIEN_MAT")
    registration_note = form_data.get("ghi_chu_dang_ky", "").strip()

    if not package_id:
        raise ValueError("Vui lòng chọn gói tập.")

    package = get_package_by_id(package_id)
    if not package:
        raise ValueError("Gói tập không tồn tại hoặc đã ngừng áp dụng.")
    
    if count_open_same_package_registration(member_id, package["ma_goi_tap"]) > 0:
        raise ValueError(
            "Hội viên đang có đăng ký cùng gói còn hiệu lực. "
            "Vui lòng kiểm tra gói hiện tại trước khi đăng ký thêm."
        )

    if payment_method not in ["TIEN_MAT", "CHUYEN_KHOAN"]:
        raise ValueError("Hình thức thanh toán không hợp lệ.")

    total_amount = Decimal(str(package["gia_goi"] or 0))

    if payment_amount > total_amount:
        raise ValueError("Số tiền thanh toán không được lớn hơn giá gói.")

    if payment_amount == 0:
        payment_status = "CHUA_THANH_TOAN"
    elif payment_amount < total_amount:
        payment_status = "THANH_TOAN_MOT_PHAN"
    else:
        payment_status = "DA_THANH_TOAN"

    end_date = calculate_end_date(start_date, package["thoi_han_ngay"])
    service_status = calculate_initial_service_status(payment_status, start_date, end_date)

    if package["loai_goi"] == "CO_PT":
        initial_sessions = package["so_buoi_pt"] or 0

        if initial_sessions <= 0:
            raise ValueError("Gói PT phải có số buổi PT lớn hơn 0.")
    else:
        initial_sessions = 0

    registration_id = insert_registration({
        "ma_hoi_vien": member_id,
        "ma_goi_tap": package["ma_goi_tap"],
        "ngay_bat_dau": start_date,
        "ngay_ket_thuc": end_date,
        "so_buoi_pt_ban_dau": initial_sessions,
        "so_buoi_pt_con_lai": initial_sessions,
        "tong_tien_phai_tra": total_amount,
        "trang_thai_thanh_toan": payment_status,
        "trang_thai_hieu_luc": service_status,
        "ghi_chu": registration_note,
    })

    if payment_amount > 0:
        from app.repositories.payments_repository import insert_payment

        insert_payment(
            registration_id=registration_id,
            account_id=account_id,
            amount=payment_amount,
            payment_method=payment_method,
            note="Thanh toán khi đăng ký thêm gói cho hội viên cũ"
        )

    return registration_id

def get_assignment_status_label(status):
    mapping = {
        "DANG_PHU_TRACH": ("Đang phụ trách", "badge-green"),
        "DA_KET_THUC": ("Đã kết thúc", "badge-gray"),
        "DA_HUY": ("Đã hủy", "badge-red"),
    }

    return mapping.get(status, ("Chưa rõ", "badge-gray"))


def build_assignment_rows(assignments):
    rows = []

    for item in assignments:
        status_text, status_class = get_assignment_status_label(item.get("trang_thai"))

        rows.append({
            "ma_phan_cong": item.get("ma_phan_cong"),
            "ma_dang_ky": item.get("ma_dang_ky"),
            "ten_goi_tap": item.get("ten_goi_tap"),
            "ten_pt": item.get("ten_pt"),
            "so_dien_thoai_pt": item.get("so_dien_thoai_pt") or "-",
            "ngay_phan_cong": format_date(item.get("ngay_phan_cong")),
            "ngay_ket_thuc": format_date(item.get("ngay_ket_thuc")),
            "status_text": status_text,
            "status_class": status_class,
            "ghi_chu": item.get("ghi_chu") or "",
        })

    return rows


def build_assign_pt_form(registration_id):
    registration = get_pt_registration_for_assignment(registration_id)

    if not registration:
        return None

    if registration.get("loai_goi") != "CO_PT":
        raise ValueError("Chỉ có thể phân công PT cho gói có PT.")
    
    if registration.get("trang_thai_hoi_vien") != "HOAT_DONG":
        raise ValueError("Hội viên đã ngừng hoạt động, không thể phân công PT.")

    pts = get_active_pts()
    current_assignment = get_active_assignment_by_registration(registration_id)

    return {
        "registration": {
            "ma_dang_ky": registration.get("ma_dang_ky"),
            "ma_hoi_vien": registration.get("ma_hoi_vien"),
            "ten_hoi_vien": registration.get("ten_hoi_vien"),
            "so_dien_thoai": registration.get("so_dien_thoai"),
            "ten_goi_tap": registration.get("ten_goi_tap"),
            "ngay_bat_dau": format_date(registration.get("ngay_bat_dau")),
            "ngay_ket_thuc": format_date(registration.get("ngay_ket_thuc")),
            "so_buoi_pt_ban_dau": registration.get("so_buoi_pt_ban_dau") or 0,
            "so_buoi_pt_con_lai": registration.get("so_buoi_pt_con_lai") or 0,
            "trang_thai_thanh_toan": registration.get("trang_thai_thanh_toan"),
            "trang_thai_hieu_luc": registration.get("trang_thai_hieu_luc"),
        },
        "pts": pts,
        "current_assignment": current_assignment,
        "today": date.today().isoformat(),
    }


def assign_pt_to_registration(registration_id, form_data):
    registration = get_pt_registration_for_assignment(registration_id)

    if not registration:
        raise ValueError("Không tìm thấy đăng ký gói.")

    if registration.get("loai_goi") != "CO_PT":
        raise ValueError("Gói này không phải gói PT, không cần phân công PT.")
    
    if registration.get("trang_thai_hoi_vien") != "HOAT_DONG":
        raise ValueError("Hội viên đã ngừng hoạt động, không thể phân công PT.")

    if registration.get("trang_thai_thanh_toan") != "DA_THANH_TOAN":
        raise ValueError("Chỉ phân công PT sau khi hội viên đã thanh toán đủ.")

    if registration.get("trang_thai_hieu_luc") not in ["DANG_HIEU_LUC", "CHUA_KICH_HOAT"]:
        raise ValueError("Chỉ phân công PT cho gói còn hiệu lực hoặc chờ kích hoạt.")

    pt_id = form_data.get("ma_pt")
    assignment_date = form_data.get("ngay_phan_cong")
    note = form_data.get("ghi_chu", "").strip()

    if not pt_id:
        raise ValueError("Vui lòng chọn PT phụ trách.")

    if not assignment_date:
        raise ValueError("Vui lòng chọn ngày phân công.")
    
    try:
        assignment_date_obj = date.fromisoformat(assignment_date)
    except ValueError:
        raise ValueError("Ngày phân công không hợp lệ.")

    if assignment_date_obj < date.today():
        raise ValueError("Ngày phân công không được nhỏ hơn ngày hiện tại.")

    package_start = normalize_db_date(registration.get("ngay_bat_dau"))
    package_end = normalize_db_date(registration.get("ngay_ket_thuc"))

    if assignment_date_obj < package_start:
        raise ValueError("Ngày phân công không được trước ngày bắt đầu của gói PT.")

    if assignment_date_obj > package_end:
        raise ValueError("Ngày phân công không được sau ngày hết hạn của gói PT.")

    pts = get_active_pts()
    valid_pt_ids = {str(pt["ma_pt"]) for pt in pts}

    if str(pt_id) not in valid_pt_ids:
        raise ValueError("PT được chọn không hợp lệ hoặc không còn làm việc.")

    # Một đăng ký gói PT chỉ có một PT đang phụ trách tại một thời điểm.
    # Nếu phân công lại, kết thúc phân công cũ rồi tạo phân công mới.
    close_current_assignment(registration_id)

    insert_pt_assignment({
        "ma_dang_ky": registration_id,
        "ma_pt": pt_id,
        "ngay_phan_cong": assignment_date,
        "ngay_ket_thuc": None,
        "ghi_chu": note,
    })

    return registration.get("ma_hoi_vien")

def build_create_schedule_form(assignment_id):
    assignment = get_assignment_for_schedule(assignment_id)

    if not assignment:
        return None

    if assignment.get("trang_thai_phan_cong") != "DANG_PHU_TRACH":
        raise ValueError("Chỉ có thể tạo lịch cho phân công PT đang phụ trách.")
    
    if assignment.get("trang_thai_hoi_vien") != "HOAT_DONG":
        raise ValueError("Hội viên đã ngừng hoạt động, không thể tạo lịch tập.")

    if assignment.get("trang_thai_lam_viec_pt") != "DANG_LAM_VIEC":
        raise ValueError("PT hiện không ở trạng thái đang làm việc, không thể tạo lịch tập mới.")

    if assignment.get("trang_thai_thanh_toan") != "DA_THANH_TOAN":
        raise ValueError("Chỉ có thể tạo lịch khi hội viên đã thanh toán đủ gói PT.")

    if assignment.get("trang_thai_hieu_luc") not in ["DANG_HIEU_LUC", "CHUA_KICH_HOAT"]:
        raise ValueError("Gói PT không còn ở trạng thái có thể tạo lịch.")

    if (assignment.get("so_buoi_pt_con_lai") or 0) <= 0:
        raise ValueError("Gói PT đã hết số buổi, không thể tạo lịch mới.")

    return {
        "assignment": {
            "ma_phan_cong": assignment.get("ma_phan_cong"),
            "ma_hoi_vien": assignment.get("ma_hoi_vien"),
            "ten_hoi_vien": assignment.get("ten_hoi_vien"),
            "so_dien_thoai_hoi_vien": assignment.get("so_dien_thoai_hoi_vien"),
            "ten_pt": assignment.get("ten_pt"),
            "so_dien_thoai_pt": assignment.get("so_dien_thoai_pt"),
            "ten_goi_tap": assignment.get("ten_goi_tap"),
            "ngay_bat_dau": format_date(assignment.get("ngay_bat_dau")),
            "ngay_ket_thuc_goi": format_date(assignment.get("ngay_ket_thuc_goi")),
            "so_buoi_pt_ban_dau": assignment.get("so_buoi_pt_ban_dau") or 0,
            "so_buoi_pt_con_lai": assignment.get("so_buoi_pt_con_lai") or 0,
        },
        "today": date.today().isoformat(),
    }


def create_training_schedule_from_assignment(assignment_id, form_data):
    assignment = get_assignment_for_schedule(assignment_id)

    if not assignment:
        raise ValueError("Không tìm thấy phân công PT.")

    if assignment.get("trang_thai_phan_cong") != "DANG_PHU_TRACH":
        raise ValueError("Chỉ có thể tạo lịch cho phân công PT đang phụ trách.")
    
    if assignment.get("trang_thai_hoi_vien") != "HOAT_DONG":
        raise ValueError("Hội viên đã ngừng hoạt động, không thể tạo lịch tập.")

    if assignment.get("trang_thai_lam_viec_pt") != "DANG_LAM_VIEC":
        raise ValueError("PT hiện không ở trạng thái đang làm việc, không thể tạo lịch tập mới.")

    if assignment.get("trang_thai_thanh_toan") != "DA_THANH_TOAN":
        raise ValueError("Hội viên chưa thanh toán đủ, không thể tạo lịch tập.")

    if assignment.get("trang_thai_hieu_luc") not in ["DANG_HIEU_LUC", "CHUA_KICH_HOAT"]:
        raise ValueError("Gói PT không còn hợp lệ để tạo lịch.")

    if (assignment.get("so_buoi_pt_con_lai") or 0) <= 0:
        raise ValueError("Gói PT đã hết số buổi.")

    training_date = form_data.get("ngay_tap")
    start_time = form_data.get("gio_bat_dau")
    end_time = form_data.get("gio_ket_thuc")
    note = form_data.get("ghi_chu", "").strip()

    schedule_start, schedule_end = build_schedule_datetime(
        training_date=training_date,
        start_time=start_time,
        end_time=end_time
    )

    training_date_obj = schedule_start.date()

    package_start = normalize_db_date(assignment.get("ngay_bat_dau"))
    package_end = normalize_db_date(assignment.get("ngay_ket_thuc_goi"))

    if training_date_obj < package_start:
        raise ValueError("Ngày tập không được trước ngày bắt đầu của gói PT.")

    if training_date_obj > package_end:
        raise ValueError("Ngày tập không được sau ngày hết hạn của gói PT.")

    conflict = get_pt_schedule_conflict(
        pt_id=assignment.get("ma_pt"),
        training_date=training_date,
        start_time=start_time,
        end_time=end_time
    )

    if conflict:
        raise ValueError(
            "PT đã có lịch trong khung giờ này. Vui lòng chọn thời gian khác."
        )
    
    member_conflict = get_member_schedule_conflict(
        member_id=assignment.get("ma_hoi_vien"),
        training_date=training_date,
        start_time=start_time,
        end_time=end_time
    )
    if member_conflict:
        raise ValueError(
            "Hội viên đã có lịch tập trong khung giờ này. Vui lòng chọn thời gian khác."
        )

    insert_training_schedule({
        "ma_phan_cong": assignment_id,
        "ngay_tap": training_date,
        "gio_bat_dau": start_time,
        "gio_ket_thuc": end_time,
        "ghi_chu": note,
    })

    return assignment.get("ma_hoi_vien")


def parse_optional_int(value, field_name):
    if value is None:
        return None

    value = str(value).strip()

    if value == "":
        return None

    try:
        number = int(value)
    except ValueError:
        raise ValueError(f"{field_name} không hợp lệ.")

    if number < 0:
        raise ValueError(f"{field_name} không được nhỏ hơn 0.")

    return number


def parse_optional_decimal(value, field_name):
    if value is None:
        return None

    value = str(value).replace(",", "").strip()

    if value == "":
        return None

    try:
        number = Decimal(value)
    except InvalidOperation:
        raise ValueError(f"{field_name} không hợp lệ.")

    if number < 0:
        raise ValueError(f"{field_name} không được nhỏ hơn 0.")

    return number


def build_existing_workout_log_view(schedule_id):
    workout_log = get_workout_log_with_details_by_schedule(schedule_id)

    if not workout_log:
        return None

    exercises = []

    for item in workout_log.get("exercise_details", []):
        exercises.append({
            "ten_bai_tap": item.get("ten_bai_tap"),
            "so_set": item.get("so_set"),
            "so_rep": item.get("so_rep"),
            "muc_ta": item.get("muc_ta"),
            "don_vi_ta": item.get("don_vi_ta") or "kg",
            "thoi_gian_phut": item.get("thoi_gian_phut"),
            "ghi_chu": item.get("ghi_chu") or "",
        })

    return {
        "ma_nhat_ky": workout_log.get("ma_nhat_ky"),
        "muc_tieu_buoi_tap": workout_log.get("muc_tieu_buoi_tap") or "",
        "nhom_co_chinh": workout_log.get("nhom_co_chinh") or "",
        "thoi_luong_phut": workout_log.get("thoi_luong_phut") or "",
        "muc_do_hoan_thanh": workout_log.get("muc_do_hoan_thanh") or "",
        "tinh_trang_hoi_vien": workout_log.get("tinh_trang_hoi_vien") or "",
        "nhan_xet_pt": workout_log.get("nhan_xet_pt") or "",
        "ke_hoach_buoi_sau": workout_log.get("ke_hoach_buoi_sau") or "",
        "exercise_details": exercises,
        "created_at": format_datetime(workout_log.get("created_at")),
    }


def parse_exercise_rows(form_data):
    names = form_data.getlist("ten_bai_tap[]")
    sets = form_data.getlist("so_set[]")
    reps = form_data.getlist("so_rep[]")
    weights = form_data.getlist("muc_ta[]")
    units = form_data.getlist("don_vi_ta[]")
    durations = form_data.getlist("thoi_gian_phut[]")
    notes = form_data.getlist("ghi_chu_bai_tap[]")

    exercises = []

    for index, name in enumerate(names):
        exercise_name = (name or "").strip()

        if not exercise_name:
            continue

        exercise = {
            "ten_bai_tap": exercise_name,
            "so_set": parse_optional_int(
                sets[index] if index < len(sets) else None,
                "Số set"
            ),
            "so_rep": (reps[index] if index < len(reps) else "").strip() or None,
            "muc_ta": parse_optional_decimal(
                weights[index] if index < len(weights) else None,
                "Mức tạ"
            ),
            "don_vi_ta": (units[index] if index < len(units) else "kg").strip() or "kg",
            "thoi_gian_phut": parse_optional_int(
                durations[index] if index < len(durations) else None,
                "Thời gian bài tập"
            ),
            "ghi_chu": (notes[index] if index < len(notes) else "").strip() or None,
        }

        exercises.append(exercise)

    return exercises


def parse_workout_log_form(schedule_id, form_data, account_id):
    duration = parse_optional_int(
        form_data.get("thoi_luong_phut"),
        "Thời lượng thực tế"
    )

    workout_log = {
        "ma_lich_tap": schedule_id,
        "muc_tieu_buoi_tap": form_data.get("muc_tieu_buoi_tap", "").strip() or None,
        "nhom_co_chinh": form_data.get("nhom_co_chinh", "").strip() or None,
        "thoi_luong_phut": duration,
        "muc_do_hoan_thanh": form_data.get("muc_do_hoan_thanh", "").strip() or None,
        "tinh_trang_hoi_vien": form_data.get("tinh_trang_hoi_vien", "").strip() or None,
        "nhan_xet_pt": form_data.get("nhan_xet_pt", "").strip() or None,
        "ke_hoach_buoi_sau": form_data.get("ke_hoach_buoi_sau", "").strip() or None,
        "ma_tai_khoan_tao": account_id,
    }

    valid_completion_levels = ["", "TOT", "TRUNG_BINH", "CHUA_DAT"]

    if (workout_log["muc_do_hoan_thanh"] or "") not in valid_completion_levels:
        raise ValueError("Mức độ hoàn thành không hợp lệ.")

    exercises = parse_exercise_rows(form_data)

    return workout_log, exercises


def validate_workout_log_required_by_status(new_status, workout_log, exercises):
    if new_status == "HOAN_THANH":
        if not workout_log.get("nhan_xet_pt"):
            raise ValueError("Vui lòng nhập nhận xét của PT cho buổi tập hoàn thành.")

    if new_status == "HUY":
        if not workout_log.get("nhan_xet_pt"):
            raise ValueError("Vui lòng nhập lý do buổi tập không diễn ra.")


def ensure_pt_can_access_schedule(schedule, current_user_id=None, current_role=None):
    if current_role != "PT":
        return

    if not current_user_id:
        raise ValueError("Không xác định được tài khoản PT đang đăng nhập.")

    if str(schedule.get("ma_tai_khoan_pt")) != str(current_user_id):
        raise ValueError("Bạn không có quyền thao tác buổi tập này.")

    if schedule.get("trang_thai_lam_viec_pt") != "DANG_LAM_VIEC":
        raise ValueError("Tài khoản PT hiện không còn ở trạng thái đang làm việc.")


def build_update_schedule_form(schedule_id, current_user_id=None, current_role=None):
    schedule = get_schedule_for_update(schedule_id)

    if not schedule:
        return None

    ensure_pt_can_access_schedule(
        schedule=schedule,
        current_user_id=current_user_id,
        current_role=current_role
    )

    status_text, status_class = get_schedule_status_label(schedule.get("trang_thai_buoi_tap"))
    workout_log = build_existing_workout_log_view(schedule_id)

    return {
        "schedule": {
            "ma_lich_tap": schedule.get("ma_lich_tap"),
            "ma_hoi_vien": schedule.get("ma_hoi_vien"),
            "ma_dang_ky": schedule.get("ma_dang_ky"),
            "ten_hoi_vien": schedule.get("ten_hoi_vien"),
            "so_dien_thoai_hoi_vien": schedule.get("so_dien_thoai_hoi_vien"),
            "ten_pt": schedule.get("ten_pt"),
            "ten_goi_tap": schedule.get("ten_goi_tap"),
            "ngay_tap": format_date(schedule.get("ngay_tap")),
            "gio_bat_dau": format_time(schedule.get("gio_bat_dau")),
            "gio_ket_thuc": format_time(schedule.get("gio_ket_thuc")),
            "trang_thai_buoi_tap": schedule.get("trang_thai_buoi_tap"),
            "status_text": status_text,
            "status_class": status_class,
            "so_buoi_pt_ban_dau": schedule.get("so_buoi_pt_ban_dau") or 0,
            "so_buoi_pt_con_lai": schedule.get("so_buoi_pt_con_lai") or 0,
            "ghi_chu": schedule.get("ghi_chu") or "",
        },
        "workout_log": workout_log,
        "status_options": [
            {"value": "HOAN_THANH", "label": "Hoàn thành"},
            {"value": "HUY", "label": "Không diễn ra"},
        ],
        "completion_options": [
            {"value": "", "label": "-- Chọn mức độ --"},
            {"value": "TOT", "label": "Tốt"},
            {"value": "TRUNG_BINH", "label": "Trung bình"},
            {"value": "CHUA_DAT", "label": "Chưa đạt"},
        ]
    }


def update_training_schedule_status(schedule_id, form_data, current_user_id=None, current_role=None):
    schedule = get_schedule_for_update(schedule_id)

    if not schedule:
        raise ValueError("Không tìm thấy lịch tập.")

    ensure_pt_can_access_schedule(
        schedule=schedule,
        current_user_id=current_user_id,
        current_role=current_role
    )

    old_status = schedule.get("trang_thai_buoi_tap")
    new_status = form_data.get("trang_thai_buoi_tap")
    note = form_data.get("nhan_xet_pt", "").strip()

    valid_statuses = ["HOAN_THANH", "HUY"]

    if new_status not in valid_statuses:
        raise ValueError("Trạng thái buổi tập không hợp lệ.")

    if old_status != "DA_LEN_LICH":
        raise ValueError("Buổi tập đã được chốt trạng thái, không thể cập nhật lại.")
    
    schedule_date = normalize_db_date(schedule.get("ngay_tap"))
    schedule_start_time = format_time(schedule.get("gio_bat_dau"))

    schedule_start_datetime = datetime.strptime(
        f"{schedule_date.isoformat()} {schedule_start_time}",
        "%Y-%m-%d %H:%M"
    )

    now = datetime.now()

    if new_status == "HOAN_THANH" and now < schedule_start_datetime:
        raise ValueError(
            "Chưa đến thời gian buổi tập, không thể cập nhật hoàn thành."
        )

    existing_log = get_workout_log_with_details_by_schedule(schedule_id)

    if existing_log:
        raise ValueError("Buổi tập này đã có nhật ký, không thể ghi trùng.")

    workout_log, exercises = parse_workout_log_form(
        schedule_id=schedule_id,
        form_data=form_data,
        account_id=current_user_id
    )

    validate_workout_log_required_by_status(
        new_status=new_status,
        workout_log=workout_log,
        exercises=exercises
    )

    registration_id = schedule.get("ma_dang_ky")
    remaining_sessions = schedule.get("so_buoi_pt_con_lai") or 0

    if new_status == "HOAN_THANH":
        if remaining_sessions <= 0:
            raise ValueError("Gói PT đã hết buổi, không thể hoàn thành thêm buổi tập.")

        decrease_remaining_pt_session(registration_id)

    log_id = insert_workout_log(workout_log)

    if exercises:
        insert_many_exercise_details(log_id, exercises)

    update_schedule_status(
        schedule_id=schedule_id,
        status=new_status,
        note=note
    )

    if new_status == "HOAN_THANH":
        mark_registration_expired_if_no_sessions(registration_id)

    return schedule.get("ma_hoi_vien")


def validate_start_date(start_date_value):
    if not start_date_value:
        raise ValueError("Vui lòng chọn ngày bắt đầu.")

    try:
        start_date = date.fromisoformat(start_date_value)
    except ValueError:
        raise ValueError("Ngày bắt đầu không hợp lệ.")

    if start_date < date.today():
        raise ValueError("Ngày bắt đầu không được nhỏ hơn ngày hiện tại.")

    return start_date