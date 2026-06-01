from datetime import date
from decimal import Decimal, InvalidOperation

from app.repositories.payments_repository import (
    get_registration_for_payment,
    get_total_paid_by_registration,
    insert_payment,
    update_registration_payment_status,
)


def format_date(value):
    if not value:
        return ""

    if isinstance(value, str):
        return value

    return value.strftime("%d/%m/%Y")


def format_money(value):
    if value is None:
        return "0 đ"

    return f"{value:,.0f} đ"


def parse_money(value):
    if value is None:
        raise ValueError("Số tiền không hợp lệ.")

    normalized = str(value).replace(",", "").replace(".", "").strip()

    if not normalized:
        raise ValueError("Vui lòng nhập số tiền thanh toán.")

    try:
        amount = Decimal(normalized)
    except InvalidOperation:
        raise ValueError("Số tiền thanh toán không hợp lệ.")

    if amount <= 0:
        raise ValueError("Số tiền thanh toán phải lớn hơn 0.")

    return amount


def calculate_service_status_after_payment(registration):
    start_date = registration.get("ngay_bat_dau")
    end_date = registration.get("ngay_ket_thuc")
    total_sessions = registration.get("so_buoi_pt_ban_dau")
    remaining_sessions = registration.get("so_buoi_pt_con_lai")

    today = date.today()

    if start_date and start_date > today:
        return "CHUA_KICH_HOAT"

    if end_date and end_date < today:
        return "HET_HAN"

    if total_sessions and total_sessions > 0:
        if remaining_sessions is not None and remaining_sessions <= 0:
            return "HET_HAN"

    return "DANG_HIEU_LUC"


def build_payment_form_data(registration_id):
    registration = get_registration_for_payment(registration_id)

    if not registration:
        return None

    total_paid = Decimal(str(get_total_paid_by_registration(registration_id)))
    total_amount = Decimal(str(registration.get("tong_tien_phai_tra") or 0))
    remaining_amount = total_amount - total_paid

    if remaining_amount < 0:
        remaining_amount = Decimal("0")

    return {
        "ma_dang_ky": registration.get("ma_dang_ky"),
        "ma_hoi_vien": registration.get("ma_hoi_vien"),
        "ten_hoi_vien": registration.get("ten_hoi_vien"),
        "so_dien_thoai": registration.get("so_dien_thoai"),
        "ten_goi_tap": registration.get("ten_goi_tap"),
        "loai_goi": "Có PT" if registration.get("loai_goi") == "CO_PT" else "Không PT",
        "ngay_bat_dau": format_date(registration.get("ngay_bat_dau")),
        "ngay_ket_thuc": format_date(registration.get("ngay_ket_thuc")),
        "tong_tien_phai_tra": format_money(total_amount),
        "da_thanh_toan": format_money(total_paid),
        "con_phai_thanh_toan": format_money(remaining_amount),
        "con_phai_thanh_toan_raw": int(remaining_amount),
        "ngay_thanh_toan_default": date.today().isoformat(),
        "trang_thai_thanh_toan": registration.get("trang_thai_thanh_toan"),
        "trang_thai_hieu_luc": registration.get("trang_thai_hieu_luc"),
    }


def record_payment(registration_id, account_id, form_data):
    registration = get_registration_for_payment(registration_id)

    if not registration:
        raise ValueError("Không tìm thấy đăng ký gói cần thanh toán.")

    payment_method = form_data.get("payment_method")
    note = form_data.get("note", "").strip()

    if payment_method not in ["TIEN_MAT", "CHUYEN_KHOAN"]:
        raise ValueError("Hình thức thanh toán không hợp lệ.")

    amount = parse_money(form_data.get("amount"))

    total_amount = Decimal(str(registration.get("tong_tien_phai_tra") or 0))
    paid_before = Decimal(str(get_total_paid_by_registration(registration_id)))
    remaining_before = total_amount - paid_before

    if remaining_before <= 0:
        raise ValueError("Gói này đã được thanh toán đủ.")

    if amount > remaining_before:
        raise ValueError("Số tiền thanh toán không được lớn hơn số tiền còn phải thanh toán.")

    insert_payment(
        registration_id=registration_id,
        account_id=account_id,
        amount=amount,
        payment_method=payment_method,
        note=note
    )

    paid_after = paid_before + amount

    if paid_after >= total_amount:
        payment_status = "DA_THANH_TOAN"
        service_status = calculate_service_status_after_payment(registration)
    else:
        payment_status = "THANH_TOAN_MOT_PHAN"
        service_status = "CHUA_KICH_HOAT"

    update_registration_payment_status(
        registration_id=registration_id,
        payment_status=payment_status,
        service_status=service_status
    )

    return registration.get("ma_hoi_vien")