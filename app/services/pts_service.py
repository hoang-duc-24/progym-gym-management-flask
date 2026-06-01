from datetime import timedelta
from app.repositories.pts_repository import (
    get_pts,
    get_pt_by_id,
    get_pt_by_phone,
    insert_pt,
    update_pt,
    get_pt_assignments,
    get_pt_schedules,
    count_future_schedules_by_pt,
    count_active_assignments_by_pt,
)


PT_STATUS_OPTIONS = [
    {"value": "DANG_LAM_VIEC", "label": "Đang làm việc"},
    {"value": "TAM_NGHI", "label": "Tạm nghỉ"},
    {"value": "NGUNG_LAM_VIEC", "label": "Ngừng làm việc"},
]


def format_date(value):
    if not value:
        return "-"

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


def get_pt_status_label(status):
    mapping = {
        "DANG_LAM_VIEC": ("Đang làm việc", "badge-green"),
        "TAM_NGHI": ("Tạm nghỉ", "badge-orange"),
        "NGUNG_LAM_VIEC": ("Ngừng làm việc", "badge-gray"),
    }

    return mapping.get(status, ("Chưa rõ", "badge-gray"))


def get_assignment_status_label(status):
    mapping = {
        "DANG_PHU_TRACH": ("Đang phụ trách", "badge-green"),
        "DA_KET_THUC": ("Đã kết thúc", "badge-gray"),
        "DA_HUY": ("Đã hủy", "badge-red"),
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


def get_schedule_status_label(status):
    mapping = {
        "DA_LEN_LICH": ("Đã lên lịch", "badge-gray"),
        "HOAN_THANH": ("Hoàn thành", "badge-green"),
        "HOAN": ("Hoãn", "badge-orange"),
        "HUY": ("Hủy", "badge-red"),
    }

    return mapping.get(status, ("Chưa rõ", "badge-gray"))


def normalize_optional(value):
    value = (value or "").strip()
    return value if value else None


def validate_pt_form(form_data, current_pt_id=None):
    ho_ten = (form_data.get("ho_ten") or "").strip()
    so_dien_thoai = (form_data.get("so_dien_thoai") or "").strip()
    email = normalize_optional(form_data.get("email"))
    chuyen_mon = normalize_optional(form_data.get("chuyen_mon"))
    kinh_nghiem = normalize_optional(form_data.get("kinh_nghiem"))
    trang_thai_lam_viec = (form_data.get("trang_thai_lam_viec") or "DANG_LAM_VIEC").strip()
    ghi_chu = normalize_optional(form_data.get("ghi_chu"))

    if not ho_ten:
        raise ValueError("Vui lòng nhập họ tên huấn luyện viên.")

    if not so_dien_thoai:
        raise ValueError("Vui lòng nhập số điện thoại huấn luyện viên.")

    if trang_thai_lam_viec not in ["DANG_LAM_VIEC", "TAM_NGHI", "NGUNG_LAM_VIEC"]:
        raise ValueError("Trạng thái làm việc không hợp lệ.")

    existing = get_pt_by_phone(so_dien_thoai)
    if existing and int(existing["ma_pt"]) != int(current_pt_id or 0):
        raise ValueError("Số điện thoại này đã tồn tại ở một huấn luyện viên khác.")

    return {
        "ho_ten": ho_ten,
        "so_dien_thoai": so_dien_thoai,
        "email": email,
        "chuyen_mon": chuyen_mon,
        "kinh_nghiem": kinh_nghiem,
        "trang_thai_lam_viec": trang_thai_lam_viec,
        "ghi_chu": ghi_chu,
    }


def build_pt_rows(raw_rows):
    rows = []

    for item in raw_rows:
        status_text, status_class = get_pt_status_label(item.get("trang_thai_lam_viec"))

        rows.append({
            "ma_pt": item.get("ma_pt"),
            "ma_nhan_su": f"PT{item.get('ma_pt'):06d}",
            "ho_ten": item.get("ho_ten"),
            "so_dien_thoai": item.get("so_dien_thoai"),
            "email": item.get("email") or "-",
            "chuyen_mon": item.get("chuyen_mon") or "-",
            "kinh_nghiem": item.get("kinh_nghiem") or "-",
            "ghi_chu": item.get("ghi_chu") or "",
            "trang_thai_lam_viec": item.get("trang_thai_lam_viec"),
            "status_text": status_text,
            "status_class": status_class,
            "so_phan_cong": item.get("so_phan_cong") or 0,
            "so_phan_cong_dang_phu_trach": item.get("so_phan_cong_dang_phu_trach") or 0,
            "so_lich_tap": item.get("so_lich_tap") or 0,
        })

    return rows


def build_pts_index(filters):
    raw_rows = get_pts(filters)

    return {
        "filters": filters,
        "pts": build_pt_rows(raw_rows),
        "total": len(raw_rows),
        "status_options": PT_STATUS_OPTIONS,
    }


def create_pt(form_data):
    data = validate_pt_form(form_data)
    return insert_pt(data)


def update_pt_info(pt_id, form_data):
    pt = get_pt_by_id(pt_id)
    if not pt:
        raise ValueError("Không tìm thấy huấn luyện viên.")

    data = validate_pt_form(form_data, current_pt_id=pt_id)

    active_assignments = count_active_assignments_by_pt(pt_id)
    future_schedules = count_future_schedules_by_pt(pt_id)

    if data["trang_thai_lam_viec"] == "NGUNG_LAM_VIEC":
        if active_assignments > 0:
            raise ValueError(
                f"Không thể ngừng làm việc PT này vì còn {active_assignments} phân công đang phụ trách. "
                "Vui lòng kết thúc hoặc chuyển phân công trước."
            )

        if future_schedules > 0:
            raise ValueError(
                f"Không thể ngừng làm việc PT này vì còn {future_schedules} lịch tập sắp tới. "
                "Vui lòng xử lý lịch tập trước."
            )

    update_pt(pt_id, data)
    return pt_id


def build_pt_form_context(pt_id=None):
    pt = None

    if pt_id:
        pt = get_pt_by_id(pt_id)
        if not pt:
            return None

    return {
        "pt": pt,
        "status_options": PT_STATUS_OPTIONS,
    }


def build_assignment_rows(raw_rows):
    rows = []

    for item in raw_rows:
        assignment_text, assignment_class = get_assignment_status_label(item.get("trang_thai"))
        service_text, service_class = get_service_status_label(item.get("trang_thai_hieu_luc"))

        remaining = item.get("so_buoi_pt_con_lai") or 0
        total = item.get("so_buoi_pt_ban_dau") or 0

        rows.append({
            "ma_phan_cong": item.get("ma_phan_cong"),
            "ma_dang_ky": item.get("ma_dang_ky"),
            "ma_hoi_vien": item.get("ma_hoi_vien"),
            "ten_hoi_vien": item.get("ten_hoi_vien"),
            "sdt_hoi_vien": item.get("sdt_hoi_vien"),
            "ten_goi_tap": item.get("ten_goi_tap"),
            "ngay_phan_cong": format_date(item.get("ngay_phan_cong")),
            "ngay_ket_thuc": format_date(item.get("ngay_ket_thuc")),
            "thoi_han_goi": f"{format_date(item.get('ngay_bat_dau'))} - {format_date(item.get('ngay_ket_thuc_goi'))}",
            "remaining_text": f"{remaining}/{total} buổi",
            "assignment_text": assignment_text,
            "assignment_class": assignment_class,
            "service_text": service_text,
            "service_class": service_class,
            "ghi_chu": item.get("ghi_chu") or "-",
        })

    return rows


def build_schedule_rows(raw_rows):
    rows = []

    for item in raw_rows:
        status_text, status_class = get_schedule_status_label(item.get("trang_thai_buoi_tap"))

        rows.append({
            "ma_lich_tap": item.get("ma_lich_tap"),
            "ma_hoi_vien": item.get("ma_hoi_vien"),
            "ten_hoi_vien": item.get("ten_hoi_vien"),
            "sdt_hoi_vien": item.get("sdt_hoi_vien"),
            "ten_goi_tap": item.get("ten_goi_tap"),
            "ngay_tap": format_date(item.get("ngay_tap")),
            "thoi_gian": f"{format_time(item.get('gio_bat_dau'))} - {format_time(item.get('gio_ket_thuc'))}",
            "status_text": status_text,
            "status_class": status_class,
            "ghi_chu": item.get("ghi_chu") or "-",
        })

    return rows


def build_pt_detail(pt_id):
    pt = get_pt_by_id(pt_id)

    if not pt:
        return None

    status_text, status_class = get_pt_status_label(pt.get("trang_thai_lam_viec"))

    assignments = get_pt_assignments(pt_id)
    schedules = get_pt_schedules(pt_id)

    return {
        "pt": {
            "ma_pt": pt.get("ma_pt"),
            "ma_nhan_su": f"PT{pt.get('ma_pt'):06d}",
            "ho_ten": pt.get("ho_ten"),
            "so_dien_thoai": pt.get("so_dien_thoai"),
            "email": pt.get("email") or "-",
            "chuyen_mon": pt.get("chuyen_mon") or "-",
            "kinh_nghiem": pt.get("kinh_nghiem") or "-",
            "ghi_chu": pt.get("ghi_chu") or "-",
            "status_text": status_text,
            "status_class": status_class,
        },
        "assignments": build_assignment_rows(assignments),
        "schedules": build_schedule_rows(schedules),
        "total_assignments": len(assignments),
        "total_schedules": len(schedules),
    }


def get_pt_future_schedule_warning(pt_id, new_status):
    if new_status not in ["TAM_NGHI", "NGUNG_LAM_VIEC"]:
        return None

    count = count_future_schedules_by_pt(pt_id)

    if count <= 0:
        return None

    return f"PT này đang có {count} lịch tập sắp tới. Hệ thống vẫn lưu trạng thái mới, nhưng cần kiểm tra lại lịch đã lên."