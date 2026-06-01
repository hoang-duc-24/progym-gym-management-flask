from decimal import Decimal, InvalidOperation

from app.repositories.packages_repository import (
    get_packages,
    get_package_by_id,
    count_registrations_by_package,
    insert_package,
    update_package,
    update_package_basic_info,
    update_package_status,
)

MAX_PACKAGE_NAME_LENGTH = 80
MAX_PACKAGE_DESCRIPTION_LENGTH = 255

def format_money(value):
    if value is None:
        return "0 đ"

    return f"{float(value):,.0f} đ"


def get_package_type_label(package_type):
    mapping = {
        "KHONG_PT": ("Không PT", "badge-gray"),
        "CO_PT": ("Có PT", "badge-blue"),
    }

    return mapping.get(package_type, ("Chưa rõ", "badge-gray"))


def get_package_status_label(status):
    mapping = {
        "DANG_AP_DUNG": ("Đang áp dụng", "badge-green"),
        "NGUNG_AP_DUNG": ("Ngừng áp dụng", "badge-red"),
    }

    return mapping.get(status, ("Chưa rõ", "badge-gray"))


def build_package_rows(raw_rows):
    rows = []

    for item in raw_rows:
        type_text, type_class = get_package_type_label(item.get("loai_goi"))
        status_text, status_class = get_package_status_label(item.get("trang_thai_ap_dung"))
        registration_count = item.get("so_luot_dang_ky") or 0

        rows.append({
            "ma_goi_tap": item.get("ma_goi_tap"),
            "ten_goi_tap": item.get("ten_goi_tap"),
            "loai_goi": item.get("loai_goi"),
            "type_text": type_text,
            "type_class": type_class,
            "gia_goi": format_money(item.get("gia_goi")),
            "thoi_han_ngay": item.get("thoi_han_ngay"),
            "so_buoi_pt": item.get("so_buoi_pt") or 0,
            "mo_ta": item.get("mo_ta") or "",
            "trang_thai_ap_dung": item.get("trang_thai_ap_dung"),
            "status_text": status_text,
            "status_class": status_class,
            "so_luot_dang_ky": registration_count,
            "has_registrations": registration_count > 0,
            "can_stop": item.get("trang_thai_ap_dung") == "DANG_AP_DUNG",
            "can_activate": item.get("trang_thai_ap_dung") == "NGUNG_AP_DUNG",
        })

    return rows


def build_packages_index(filters):
    raw_rows = get_packages(filters)

    return {
        "filters": filters,
        "packages": build_package_rows(raw_rows),
        "total": len(raw_rows),
    }


def build_package_form(package_id=None):
    package = None
    registration_count = 0

    if package_id:
        package = get_package_by_id(package_id)

        if not package:
            return None

        registration_count = count_registrations_by_package(package_id)

    return {
        "package": package,
        "registration_count": registration_count,
        "has_registrations": registration_count > 0,
        "type_options": [
            {"value": "KHONG_PT", "label": "Không PT"},
            {"value": "CO_PT", "label": "Có PT"},
        ],
    }


def parse_package_form(form_data):
    ten_goi_tap = form_data.get("ten_goi_tap", "").strip()
    loai_goi = form_data.get("loai_goi", "").strip()
    gia_goi_raw = form_data.get("gia_goi", "").strip()
    thoi_han_raw = form_data.get("thoi_han_ngay", "").strip()
    so_buoi_pt_raw = form_data.get("so_buoi_pt", "").strip()
    mo_ta = form_data.get("mo_ta", "").strip()

    if not ten_goi_tap:
        raise ValueError("Vui lòng nhập tên gói tập.")
    
    if len(ten_goi_tap) > MAX_PACKAGE_NAME_LENGTH:
        raise ValueError(f"Tên gói tập không được vượt quá {MAX_PACKAGE_NAME_LENGTH} ký tự.")

    if len(mo_ta) > MAX_PACKAGE_DESCRIPTION_LENGTH:
        raise ValueError(f"Mô tả gói tập không được vượt quá {MAX_PACKAGE_DESCRIPTION_LENGTH} ký tự.")

    if loai_goi not in ["KHONG_PT", "CO_PT"]:
        raise ValueError("Loại gói không hợp lệ.")

    try:
        gia_goi = Decimal(gia_goi_raw)
    except InvalidOperation:
        raise ValueError("Giá gói không hợp lệ.")

    if gia_goi < 0:
        raise ValueError("Giá gói không được nhỏ hơn 0.")

    try:
        thoi_han_ngay = int(thoi_han_raw)
    except ValueError:
        raise ValueError("Thời hạn gói không hợp lệ.")

    if thoi_han_ngay <= 0:
        raise ValueError("Thời hạn gói phải lớn hơn 0.")

    if so_buoi_pt_raw == "":
        so_buoi_pt = 0
    else:
        try:
            so_buoi_pt = int(so_buoi_pt_raw)
        except ValueError:
            raise ValueError("Số buổi PT không hợp lệ.")

    if so_buoi_pt < 0:
        raise ValueError("Số buổi PT không được nhỏ hơn 0.")

    if loai_goi == "KHONG_PT":
        so_buoi_pt = 0

    if loai_goi == "CO_PT" and so_buoi_pt <= 0:
        raise ValueError("Gói có PT phải có số buổi PT lớn hơn 0.")

    return {
        "ten_goi_tap": ten_goi_tap,
        "loai_goi": loai_goi,
        "gia_goi": gia_goi,
        "thoi_han_ngay": thoi_han_ngay,
        "so_buoi_pt": so_buoi_pt,
        "mo_ta": mo_ta,
    }


def parse_package_basic_info_form(form_data):
    ten_goi_tap = form_data.get("ten_goi_tap", "").strip()
    mo_ta = form_data.get("mo_ta", "").strip()

    if not ten_goi_tap:
        raise ValueError("Vui lòng nhập tên gói tập.")

    if len(ten_goi_tap) > MAX_PACKAGE_NAME_LENGTH:
        raise ValueError(f"Tên gói tập không được vượt quá {MAX_PACKAGE_NAME_LENGTH} ký tự.")

    if len(mo_ta) > MAX_PACKAGE_DESCRIPTION_LENGTH:
        raise ValueError(f"Mô tả gói tập không được vượt quá {MAX_PACKAGE_DESCRIPTION_LENGTH} ký tự.")

    return {
        "ten_goi_tap": ten_goi_tap,
        "mo_ta": mo_ta,
    }


def create_package(form_data):
    data = parse_package_form(form_data)
    insert_package(data)


def edit_package(package_id, form_data):
    package = get_package_by_id(package_id)

    if not package:
        raise ValueError("Không tìm thấy gói tập.")

    registration_count = count_registrations_by_package(package_id)

    if registration_count > 0:
        data = parse_package_basic_info_form(form_data)
        update_package_basic_info(package_id, data)
        return

    data = parse_package_form(form_data)
    update_package(package_id, data)


def stop_package(package_id):
    package = get_package_by_id(package_id)

    if not package:
        raise ValueError("Không tìm thấy gói tập.")

    update_package_status(package_id, "NGUNG_AP_DUNG")


def activate_package(package_id):
    package = get_package_by_id(package_id)

    if not package:
        raise ValueError("Không tìm thấy gói tập.")

    update_package_status(package_id, "DANG_AP_DUNG")