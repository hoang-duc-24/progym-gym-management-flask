from app.repositories.payment_reports_repository import (
    get_payment_transactions,
    get_payment_summary,
    get_payment_summary_by_method,
)


def format_money(value):
    if value is None:
        return "0 đ"

    return f"{float(value):,.0f} đ"


def format_datetime(value):
    if not value:
        return ""

    if isinstance(value, str):
        return value

    return value.strftime("%d/%m/%Y %H:%M")


def get_payment_method_label(method):
    mapping = {
        "TIEN_MAT": "Tiền mặt",
        "CHUYEN_KHOAN": "Chuyển khoản",
    }

    return mapping.get(method, "Chưa rõ")


def get_payment_status_label(status):
    mapping = {
        "CHO_XAC_NHAN": ("Chờ xác nhận", "badge-orange"),
        "DA_THANH_TOAN": ("Đã thanh toán", "badge-green"),
        "HUY": ("Hủy", "badge-red"),
    }

    return mapping.get(status, ("Chưa rõ", "badge-gray"))


def get_registration_payment_status_label(status):
    mapping = {
        "CHUA_THANH_TOAN": ("Chưa thanh toán", "badge-orange"),
        "THANH_TOAN_MOT_PHAN": ("Thanh toán một phần", "badge-orange"),
        "DA_THANH_TOAN": ("Đã thanh toán", "badge-green"),
    }

    return mapping.get(status, ("Chưa rõ", "badge-gray"))


def get_service_status_label(status):
    mapping = {
        "CHUA_KICH_HOAT": ("Chưa kích hoạt", "badge-gray"),
        "DANG_HIEU_LUC": ("Đang hiệu lực", "badge-green"),
        "HET_HAN": ("Hết hạn", "badge-red"),
        "TAM_DUNG": ("Tạm dừng", "badge-orange"),
    }

    return mapping.get(status, ("Chưa rõ", "badge-gray"))


def get_package_type_label(package_type):
    mapping = {
        "KHONG_PT": "Không PT",
        "CO_PT": "Có PT",
    }

    return mapping.get(package_type, "Chưa rõ")


def build_payment_rows(raw_rows):
    rows = []

    for item in raw_rows:
        payment_status_text, payment_status_class = get_payment_status_label(
            item.get("trang_thai_thanh_toan")
        )

        registration_payment_text, registration_payment_class = get_registration_payment_status_label(
            item.get("trang_thai_dang_ky")
        )

        service_text, service_class = get_service_status_label(
            item.get("trang_thai_hieu_luc")
        )

        rows.append({
            "ma_thanh_toan": item.get("ma_thanh_toan"),
            "ma_dang_ky": item.get("ma_dang_ky"),
            "ma_hoi_vien": item.get("ma_hoi_vien"),

            "ngay_thanh_toan": format_datetime(item.get("ngay_thanh_toan")),
            "so_tien": format_money(item.get("so_tien")),
            "hinh_thuc_thanh_toan": get_payment_method_label(item.get("hinh_thuc_thanh_toan")),

            "payment_status_text": payment_status_text,
            "payment_status_class": payment_status_class,

            "registration_payment_text": registration_payment_text,
            "registration_payment_class": registration_payment_class,

            "service_text": service_text,
            "service_class": service_class,

            "ten_hoi_vien": item.get("ten_hoi_vien"),
            "so_dien_thoai": item.get("so_dien_thoai"),
            "ten_goi_tap": item.get("ten_goi_tap"),
            "loai_goi": get_package_type_label(item.get("loai_goi")),
            "tong_tien_phai_tra": format_money(item.get("tong_tien_phai_tra")),
            "ghi_chu": item.get("ghi_chu") or "",
        })

    return rows


def build_method_summary(raw_rows):
    rows = []

    for item in raw_rows:
        rows.append({
            "hinh_thuc_thanh_toan": get_payment_method_label(item.get("hinh_thuc_thanh_toan")),
            "so_giao_dich": item.get("so_giao_dich") or 0,
            "tong_tien": format_money(item.get("tong_tien")),
        })

    return rows


def build_payment_report_index(filters):
    raw_transactions = get_payment_transactions(filters)
    summary = get_payment_summary(filters)
    method_summary = get_payment_summary_by_method(filters)

    return {
        "filters": filters,
        "transactions": build_payment_rows(raw_transactions),
        "summary": {
            "so_giao_dich": summary.get("so_giao_dich") or 0,
            "tong_tien": format_money(summary.get("tong_tien")),
        },
        "method_summary": build_method_summary(method_summary),
        "total": len(raw_transactions),
        "method_options": [
            {"value": "TIEN_MAT", "label": "Tiền mặt"},
            {"value": "CHUYEN_KHOAN", "label": "Chuyển khoản"},
        ],
        "status_options": [
            {"value": "DA_THANH_TOAN", "label": "Đã thanh toán"},
            {"value": "CHO_XAC_NHAN", "label": "Chờ xác nhận"},
            {"value": "HUY", "label": "Hủy"},
        ],
    }