from datetime import timedelta

from app.repositories.schedules_repository import (
    get_all_pts,
    get_schedules,
    get_schedulable_assignments,
)


def format_date(value):
    if not value:
        return ""

    if isinstance(value, str):
        return value

    return value.strftime("%d/%m/%Y")


def format_time(value):
    if not value:
        return ""

    if isinstance(value, str):
        return value[:5]

    if isinstance(value, timedelta):
        total_seconds = int(value.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{hours:02d}:{minutes:02d}"

    return value.strftime("%H:%M")


def get_schedule_status_label(status):
    mapping = {
        "DA_LEN_LICH": ("Đã lên lịch", "badge-blue"),
        "HOAN_THANH": ("Hoàn thành", "badge-green"),
        "HUY": ("Không diễn ra", "badge-orange"),
    }

    return mapping.get(status, ("Chưa rõ", "badge-gray"))


def get_payment_status_label(status):
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


def build_schedule_rows(raw_rows):
    rows = []

    for item in raw_rows:
        schedule_text, schedule_class = get_schedule_status_label(
            item.get("trang_thai_buoi_tap")
        )

        payment_text, payment_class = get_payment_status_label(
            item.get("trang_thai_thanh_toan")
        )

        service_text, service_class = get_service_status_label(
            item.get("trang_thai_hieu_luc")
        )

        rows.append({
            "ma_lich_tap": item.get("ma_lich_tap"),
            "ma_hoi_vien": item.get("ma_hoi_vien"),
            "ma_dang_ky": item.get("ma_dang_ky"),
            "ma_phan_cong": item.get("ma_phan_cong"),

            "ngay_tap": format_date(item.get("ngay_tap")),
            "gio_bat_dau": format_time(item.get("gio_bat_dau")),
            "gio_ket_thuc": format_time(item.get("gio_ket_thuc")),

            "ten_hoi_vien": item.get("ten_hoi_vien"),
            "sdt_hoi_vien": item.get("sdt_hoi_vien"),

            "ten_pt": item.get("ten_pt"),
            "sdt_pt": item.get("sdt_pt"),

            "ten_goi_tap": item.get("ten_goi_tap"),
            "loai_goi": "Có PT" if item.get("loai_goi") == "CO_PT" else "Không PT",

            "so_buoi_pt_ban_dau": item.get("so_buoi_pt_ban_dau") or 0,
            "so_buoi_pt_con_lai": item.get("so_buoi_pt_con_lai") or 0,

            "payment_text": payment_text,
            "payment_class": payment_class,
            "service_text": service_text,
            "service_class": service_class,

            "schedule_status_raw": item.get("trang_thai_buoi_tap"),
            "schedule_text": schedule_text,
            "schedule_class": schedule_class,

            "ghi_chu": item.get("ghi_chu") or "",
        })

    return rows


def build_pt_filter_options(pt_account_id=None):
    pts = get_all_pts(account_id=pt_account_id)

    return [
        {
            "ma_pt": pt.get("ma_pt"),
            "ho_ten": pt.get("ho_ten"),
            "so_dien_thoai": pt.get("so_dien_thoai"),
        }
        for pt in pts
    ]


def build_schedules_index(filters, current_role=None, current_user_id=None):
    filters = dict(filters or {})

    pt_account_id = None

    if current_role == "PT":
        pt_account_id = current_user_id
        filters["pt_account_id"] = current_user_id
        filters["ma_pt"] = ""

    schedules = get_schedules(filters)

    status_options = [
        {"value": "DA_LEN_LICH", "label": "Đã lên lịch"},
        {"value": "HOAN_THANH", "label": "Hoàn thành"},
        {"value": "HUY", "label": "Không diễn ra"},
    ]

    return {
        "filters": filters,
        "pt_options": build_pt_filter_options(pt_account_id=pt_account_id),
        "status_options": status_options,
        "schedules": build_schedule_rows(schedules),
        "total": len(schedules),
        "is_pt_view": current_role == "PT",
    }

def get_assignment_status_label(status):
    mapping = {
        "DANG_PHU_TRACH": ("Đang phụ trách", "badge-green"),
        "DA_KET_THUC": ("Đã kết thúc", "badge-gray"),
        "DA_HUY": ("Đã hủy", "badge-red"),
    }

    return mapping.get(status, ("Chưa rõ", "badge-gray"))


def build_schedulable_assignment_rows(raw_rows):
    rows = []

    for item in raw_rows:
        assignment_text, assignment_class = get_assignment_status_label(
            item.get("trang_thai_phan_cong")
        )

        payment_text, payment_class = get_payment_status_label(
            item.get("trang_thai_thanh_toan")
        )

        service_text, service_class = get_service_status_label(
            item.get("trang_thai_hieu_luc")
        )

        remaining = item.get("so_buoi_pt_con_lai") or 0
        total = item.get("so_buoi_pt_ban_dau") or 0

        rows.append({
            "ma_phan_cong": item.get("ma_phan_cong"),
            "ma_dang_ky": item.get("ma_dang_ky"),
            "ma_hoi_vien": item.get("ma_hoi_vien"),
            "ma_pt": item.get("ma_pt"),

            "ten_hoi_vien": item.get("ten_hoi_vien"),
            "sdt_hoi_vien": item.get("sdt_hoi_vien"),

            "ten_pt": item.get("ten_pt"),
            "sdt_pt": item.get("sdt_pt"),

            "ten_goi_tap": item.get("ten_goi_tap"),
            "loai_goi": "Có PT" if item.get("loai_goi") == "CO_PT" else "Không PT",

            "ngay_phan_cong": format_date(item.get("ngay_phan_cong")),
            "ngay_bat_dau": format_date(item.get("ngay_bat_dau")),
            "ngay_ket_thuc_goi": format_date(item.get("ngay_ket_thuc_goi")),

            "so_buoi_pt_ban_dau": total,
            "so_buoi_pt_con_lai": remaining,
            "remaining_text": f"{remaining}/{total} buổi",

            "assignment_text": assignment_text,
            "assignment_class": assignment_class,

            "payment_text": payment_text,
            "payment_class": payment_class,

            "service_text": service_text,
            "service_class": service_class,
        })

    return rows


def build_schedule_create_assignment_index(filters):
    assignments = get_schedulable_assignments(filters)

    service_status_options = [
        {"value": "DANG_HIEU_LUC", "label": "Đang hiệu lực"},
        {"value": "CHUA_KICH_HOAT", "label": "Chưa kích hoạt"},
    ]

    return {
        "filters": filters,
        "pt_options": build_pt_filter_options(),
        "service_status_options": service_status_options,
        "assignments": build_schedulable_assignment_rows(assignments),
        "total": len(assignments),
    }