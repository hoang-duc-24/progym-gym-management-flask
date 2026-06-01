from datetime import date
from decimal import Decimal


from app.repositories.registrations_repository import (
    get_registrations,
    get_registration_by_id,
    get_payments_by_registration,
    get_assignments_by_registration,
    get_schedules_by_registration,
    get_checkins_by_registration,
    get_registration_kpis,
    search_members_for_registration,
)


PACKAGE_TYPE_OPTIONS = [
    {"value": "KHONG_PT", "label": "Không PT"},
    {"value": "CO_PT", "label": "Có PT"},
]


PAYMENT_STATUS_OPTIONS = [
    {"value": "CHUA_THANH_TOAN", "label": "Chưa thanh toán"},
    {"value": "THANH_TOAN_MOT_PHAN", "label": "Thanh toán một phần"},
    {"value": "DA_THANH_TOAN", "label": "Đã thanh toán"},
]


SERVICE_STATUS_OPTIONS = [
    {"value": "CHUA_KICH_HOAT", "label": "Chưa kích hoạt"},
    {"value": "DANG_HIEU_LUC", "label": "Đang hiệu lực"},
    {"value": "HET_HAN", "label": "Hết hạn"},
]


def format_date(value):
    if not value:
        return "-"

    if isinstance(value, str):
        return value

    return value.strftime("%d/%m/%Y")


def format_datetime(value):
    if not value:
        return "-"

    if isinstance(value, str):
        return value

    return value.strftime("%d/%m/%Y %H:%M")


def format_time(value):
    if not value:
        return ""

    if isinstance(value, str):
        return value[:5]

    if hasattr(value, "total_seconds"):
        total_seconds = int(value.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{hours:02d}:{minutes:02d}"

    return value.strftime("%H:%M")


def format_money(value):
    if value is None:
        return "0 đ"

    return f"{Decimal(str(value)):,.0f} đ"


def get_package_type_label(value):
    mapping = {
        "KHONG_PT": "Không PT",
        "CO_PT": "Có PT",
    }
    return mapping.get(value, value or "-")


def get_payment_status_label(value):
    mapping = {
        "CHUA_THANH_TOAN": ("Chưa thanh toán", "badge-red"),
        "THANH_TOAN_MOT_PHAN": ("Thanh toán một phần", "badge-orange"),
        "DA_THANH_TOAN": ("Đã thanh toán", "badge-green"),
    }
    return mapping.get(value, ("Chưa rõ", "badge-gray"))


def get_service_status_label(value):
    mapping = {
        "CHUA_KICH_HOAT": ("Chưa kích hoạt", "badge-gray"),
        "DANG_HIEU_LUC": ("Đang hiệu lực", "badge-green"),
        "HET_HAN": ("Hết hạn", "badge-red"),
        "TAM_DUNG": ("Tạm dừng", "badge-orange"),
        "DA_HUY": ("Đã hủy", "badge-red"),
    }
    return mapping.get(value, ("Chưa rõ", "badge-gray"))


def get_assignment_status_label(value):
    mapping = {
        "DANG_PHU_TRACH": ("Đang phụ trách", "badge-green"),
        "DA_KET_THUC": ("Đã kết thúc", "badge-gray"),
        "DA_HUY": ("Đã hủy", "badge-red"),
    }
    return mapping.get(value, ("Chưa rõ", "badge-gray"))


def get_schedule_status_label(value):
    mapping = {
        "DA_LEN_LICH": ("Đã lên lịch", "badge-gray"),
        "HOAN_THANH": ("Hoàn thành", "badge-green"),
        "HOAN": ("Hoãn", "badge-orange"),
        "HUY": ("Hủy", "badge-red"),
    }
    return mapping.get(value, ("Chưa rõ", "badge-gray"))


def get_checkin_type_label(value):
    mapping = {
        "TU_DO": "Tự do",
        "THEO_LICH_PT": "Theo lịch PT",
    }
    return mapping.get(value, value or "-")


def get_checkin_status_label(value):
    mapping = {
        "DANG_CHECKIN": ("Đang trong phòng", "badge-green"),
        "DA_CHECKOUT": ("Đã check-out", "badge-gray"),
        "HUY": ("Hủy", "badge-red"),
    }
    return mapping.get(value, ("Chưa rõ", "badge-gray"))


def calculate_remaining_text(row):
    start_date = row.get("ngay_bat_dau")
    end_date = row.get("ngay_ket_thuc")
    service_status = row.get("trang_thai_hieu_luc")
    package_type = row.get("loai_goi")

    today = date.today()

    if service_status == "CHUA_KICH_HOAT":
        if start_date and not isinstance(start_date, str):
            days_until_start = (start_date - today).days

            if days_until_start > 0:
                return f"Bắt đầu sau {days_until_start} ngày"

        return "Chưa bắt đầu"

    if package_type == "CO_PT":
        remaining = row.get("so_buoi_pt_con_lai") or 0
        total = row.get("so_buoi_pt_ban_dau") or 0

        if service_status == "HET_HAN":
            if end_date and not isinstance(end_date, str) and end_date < today and remaining > 0:
                return f"{remaining}/{total} buổi · Hết hạn"

            return f"{remaining}/{total} buổi"

        return f"{remaining}/{total} buổi"

    if service_status == "HET_HAN":
        return "Đã hết hạn"

    if not end_date:
        return "-"

    if isinstance(end_date, str):
        return "-"

    remaining_days = (end_date - today).days

    if remaining_days < 0:
        return "Đã hết hạn"

    return f"{remaining_days} ngày"


def build_registration_rows(raw_rows):
    rows = []

    for item in raw_rows:
        payment_text, payment_class = get_payment_status_label(item.get("trang_thai_thanh_toan"))
        service_text, service_class = get_service_status_label(item.get("trang_thai_hieu_luc"))

        total_amount = Decimal(str(item.get("tong_tien_phai_tra") or 0))
        paid_amount = Decimal(str(item.get("da_thanh_toan") or 0))
        remaining_amount = total_amount - paid_amount
        if remaining_amount < 0:
            remaining_amount = Decimal("0")

        rows.append({
            "ma_dang_ky": item.get("ma_dang_ky"),
            "ma_hien_thi": f"DK{item.get('ma_dang_ky'):06d}",
            "ma_hoi_vien": item.get("ma_hoi_vien"),
            "ten_hoi_vien": item.get("ten_hoi_vien"),
            "so_dien_thoai": item.get("so_dien_thoai"),
            "ten_goi_tap": item.get("ten_goi_tap"),
            "loai_goi": get_package_type_label(item.get("loai_goi")),
            "ngay_dang_ky": format_date(item.get("ngay_dang_ky")),
            "ngay_bat_dau": format_date(item.get("ngay_bat_dau")),
            "ngay_ket_thuc": format_date(item.get("ngay_ket_thuc")),
            "con_lai": calculate_remaining_text(item),
            "tong_tien": format_money(total_amount),
            "da_thanh_toan": format_money(paid_amount),
            "con_phai_thanh_toan": format_money(remaining_amount),
            "payment_text": payment_text,
            "payment_class": payment_class,
            "service_text": service_text,
            "service_class": service_class,
            "so_phan_cong": item.get("so_phan_cong") or 0,
            "so_lich_tap": item.get("so_lich_tap") or 0,
            "so_luot_checkin": item.get("so_luot_checkin") or 0,
            "trang_thai_thanh_toan": item.get("trang_thai_thanh_toan"),
            "trang_thai_hieu_luc": item.get("trang_thai_hieu_luc"),
        })

    return rows


def build_registrations_index(filters):
    raw_rows = get_registrations(filters)
    kpis = get_registration_kpis() or {}

    return {
        "filters": filters,
        "registrations": build_registration_rows(raw_rows),
        "total": len(raw_rows),
        "kpis": {
            "tong_dang_ky": kpis.get("tong_dang_ky") or 0,
            "dang_hieu_luc": kpis.get("dang_hieu_luc") or 0,
            "chua_kich_hoat": kpis.get("chua_kich_hoat") or 0,
            "het_han": kpis.get("het_han") or 0,
            "da_thanh_toan": kpis.get("da_thanh_toan") or 0,
            "chua_thanh_toan_du": kpis.get("chua_thanh_toan_du") or 0,
        },
        "package_type_options": PACKAGE_TYPE_OPTIONS,
        "payment_status_options": PAYMENT_STATUS_OPTIONS,
        "service_status_options": SERVICE_STATUS_OPTIONS,
    }


def build_payment_rows(raw_rows):
    rows = []

    for item in raw_rows:
        payment_text, payment_class = get_payment_status_label(item.get("trang_thai_thanh_toan"))

        rows.append({
            "ma_thanh_toan": item.get("ma_thanh_toan"),
            "ma_hien_thi": f"TT{item.get('ma_thanh_toan'):06d}",
            "ngay_thanh_toan": format_datetime(item.get("ngay_thanh_toan")),
            "so_tien": format_money(item.get("so_tien")),
            "hinh_thuc": {
                "TIEN_MAT": "Tiền mặt",
                "CHUYEN_KHOAN": "Chuyển khoản",
                "THE": "Thẻ",
                "KHAC": "Khác",
            }.get(item.get("hinh_thuc_thanh_toan"), item.get("hinh_thuc_thanh_toan") or "-"),
            "payment_text": payment_text,
            "payment_class": payment_class,
            "ghi_chu": item.get("ghi_chu") or "-",
        })

    return rows


def build_assignment_rows(raw_rows):
    rows = []

    for item in raw_rows:
        status_text, status_class = get_assignment_status_label(item.get("trang_thai"))

        rows.append({
            "ma_phan_cong": item.get("ma_phan_cong"),
            "ma_hien_thi": f"PC{item.get('ma_phan_cong'):06d}",
            "ma_pt": item.get("ma_pt"),
            "ten_pt": item.get("ten_pt"),
            "sdt_pt": item.get("sdt_pt"),
            "ngay_phan_cong": format_date(item.get("ngay_phan_cong")),
            "ngay_ket_thuc": format_date(item.get("ngay_ket_thuc")),
            "status_text": status_text,
            "status_class": status_class,
            "trang_thai_lam_viec": item.get("trang_thai_lam_viec"),
            "ghi_chu": item.get("ghi_chu") or "-",
        })

    return rows


def build_schedule_rows(raw_rows):
    rows = []

    for item in raw_rows:
        status_text, status_class = get_schedule_status_label(item.get("trang_thai_buoi_tap"))

        rows.append({
            "ma_lich_tap": item.get("ma_lich_tap"),
            "ma_hien_thi": f"LT{item.get('ma_lich_tap'):06d}",
            "ngay_tap": format_date(item.get("ngay_tap")),
            "thoi_gian": f"{format_time(item.get('gio_bat_dau'))} - {format_time(item.get('gio_ket_thuc'))}",
            "ten_pt": item.get("ten_pt"),
            "status_text": status_text,
            "status_class": status_class,
            "ghi_chu": item.get("ghi_chu") or "-",
        })

    return rows


def build_checkin_rows(raw_rows):
    rows = []

    for item in raw_rows:
        status_text, status_class = get_checkin_status_label(item.get("trang_thai"))

        rows.append({
            "ma_check": item.get("ma_check"),
            "ma_hien_thi": f"CI{item.get('ma_check'):06d}",
            "gio_vao": format_datetime(item.get("thoi_gian_check_in")),
            "gio_ra": format_datetime(item.get("thoi_gian_check_out")),
            "loai": get_checkin_type_label(item.get("loai_checkin")),
            "status_text": status_text,
            "status_class": status_class,
            "ghi_chu": item.get("ghi_chu") or "-",
        })

    return rows


def build_registration_detail(registration_id):
    registration = get_registration_by_id(registration_id)

    if not registration:
        return None

    payment_text, payment_class = get_payment_status_label(registration.get("trang_thai_thanh_toan"))
    service_text, service_class = get_service_status_label(registration.get("trang_thai_hieu_luc"))

    total_amount = Decimal(str(registration.get("tong_tien_phai_tra") or 0))
    payments = get_payments_by_registration(registration_id)
    paid_amount = sum(Decimal(str(item.get("so_tien") or 0)) for item in payments if item.get("trang_thai_thanh_toan") == "DA_THANH_TOAN")
    remaining_amount = total_amount - paid_amount
    if remaining_amount < 0:
        remaining_amount = Decimal("0")

    return {
        "registration": {
            "ma_dang_ky": registration.get("ma_dang_ky"),
            "ma_hien_thi": f"DK{registration.get('ma_dang_ky'):06d}",
            "ma_hoi_vien": registration.get("ma_hoi_vien"),
            "ten_hoi_vien": registration.get("ten_hoi_vien"),
            "so_dien_thoai": registration.get("so_dien_thoai"),
            "email": registration.get("email") or "-",
            "ngay_sinh": format_date(registration.get("ngay_sinh")),
            "gioi_tinh": registration.get("gioi_tinh") or "-",
            "dia_chi": registration.get("dia_chi") or "-",
            "ten_goi_tap": registration.get("ten_goi_tap"),
            "loai_goi": get_package_type_label(registration.get("loai_goi")),
            "ngay_dang_ky": format_date(registration.get("ngay_dang_ky")),
            "ngay_bat_dau": format_date(registration.get("ngay_bat_dau")),
            "ngay_ket_thuc": format_date(registration.get("ngay_ket_thuc")),
            "so_buoi_pt_ban_dau": registration.get("so_buoi_pt_ban_dau") or 0,
            "so_buoi_pt_con_lai": registration.get("so_buoi_pt_con_lai") or 0,
            "tong_tien": format_money(total_amount),
            "da_thanh_toan": format_money(paid_amount),
            "con_phai_thanh_toan": format_money(remaining_amount),
            "payment_text": payment_text,
            "payment_class": payment_class,
            "service_text": service_text,
            "service_class": service_class,
            "trang_thai_thanh_toan": registration.get("trang_thai_thanh_toan"),
            "trang_thai_hieu_luc": registration.get("trang_thai_hieu_luc"),
            "loai_goi_raw": registration.get("loai_goi"),
            "ghi_chu": registration.get("ghi_chu") or "-",
        },
        "payments": build_payment_rows(payments),
        "assignments": build_assignment_rows(get_assignments_by_registration(registration_id)),
        "schedules": build_schedule_rows(get_schedules_by_registration(registration_id)),
        "checkins": build_checkin_rows(get_checkins_by_registration(registration_id)),
    }

def get_member_status_label(value):
    mapping = {
        "HOAT_DONG": ("Hoạt động", "badge-green"),
        "NGUNG_HOAT_DONG": ("Ngừng hoạt động", "badge-gray"),
    }

    return mapping.get(value, ("Chưa rõ", "badge-gray"))


def build_member_selection_rows(raw_rows):
    rows = []

    for item in raw_rows:
        member_status_text, member_status_class = get_member_status_label(item.get("trang_thai"))

        service_text, service_class = get_service_status_label(item.get("trang_thai_hieu_luc"))

        if not item.get("ma_dang_ky"):
            service_text = "Chưa có gói"
            service_class = "badge-gray"

        current_package = item.get("ten_goi_tap") or "-"

        remaining_text = "-"
        if item.get("ma_dang_ky"):
            if item.get("loai_goi") == "CO_PT":
                remaining = item.get("so_buoi_pt_con_lai") or 0
                total = item.get("so_buoi_pt_ban_dau") or 0
                remaining_text = f"{remaining}/{total} buổi"
            else:
                end_date = item.get("ngay_ket_thuc")
                if end_date and not isinstance(end_date, str):
                    remaining_days = (end_date - date.today()).days
                    remaining_text = "Đã hết hạn" if remaining_days < 0 else f"{remaining_days} ngày"

        rows.append({
            "ma_hoi_vien": item.get("ma_hoi_vien"),
            "ma_hien_thi": f"CUS{item.get('ma_hoi_vien'):06d}",
            "ho_ten": item.get("ho_ten"),
            "so_dien_thoai": item.get("so_dien_thoai"),
            "email": item.get("email") or "-",
            "ngay_tham_gia": format_date(item.get("ngay_tham_gia")),
            "trang_thai_hoi_vien": item.get("trang_thai"),
            "member_status_text": member_status_text,
            "member_status_class": member_status_class,
            "current_package": current_package,
            "remaining_text": remaining_text,
            "service_text": service_text,
            "service_class": service_class,
        })

    return rows


def build_registration_create_context(keyword=None):
    keyword = (keyword or "").strip()
    raw_rows = search_members_for_registration(keyword)

    return {
        "keyword": keyword,
        "members": build_member_selection_rows(raw_rows),
        "total": len(raw_rows),
    }