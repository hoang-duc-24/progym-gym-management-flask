from app.repositories.checkin_repository import (
    search_members_for_checkin,
    get_member_for_checkin,
    get_active_registrations_for_checkin,
    get_today_available_pt_schedules,
    get_open_checkin_by_member,
    insert_checkin,
    update_checkout,
    get_current_training_members,
    auto_close_old_open_checkins,
    auto_close_old_open_checkins_by_member,
)

from app.services.service_status_service import sync_registration_service_statuses

GYM_CLOSING_TIME = "22:00:00"


def format_datetime(value):
    if not value:
        return ""

    if isinstance(value, str):
        return value

    return value.strftime("%d/%m/%Y %H:%M")


def format_member_code(member_id):
    return f"CUS{member_id:06d}"


def get_member_status_label(status):
    mapping = {
        "HOAT_DONG": ("Hoạt động", "badge-green"),
        "NGUNG_HOAT_DONG": ("Ngừng hoạt động", "badge-gray"),
    }

    return mapping.get(status, ("Chưa rõ", "badge-gray"))


def get_checkin_type_label(value):
    mapping = {
        "TU_DO": "Tự do",
        "THEO_LICH_PT": "Theo lịch PT",
    }

    return mapping.get(value, value or "-")


def build_checkin_index(keyword=None):
    sync_registration_service_statuses()
    auto_close_old_open_checkins(GYM_CLOSING_TIME)
    keyword = (keyword or "").strip()

    members = []
    if keyword:
        raw_members = search_members_for_checkin(keyword)

        for item in raw_members:
            status_text, status_class = get_member_status_label(item.get("trang_thai"))
            open_checkin = get_open_checkin_by_member(item.get("ma_hoi_vien"))
            valid_registrations = get_active_registrations_for_checkin(item.get("ma_hoi_vien"))

            members.append({
                "ma_hoi_vien": item.get("ma_hoi_vien"),
                "ma_khach_hang": format_member_code(item.get("ma_hoi_vien")),
                "ho_ten": item.get("ho_ten"),
                "so_dien_thoai": item.get("so_dien_thoai"),
                "email": item.get("email") or "-",
                "status_text": status_text,
                "status_class": status_class,
                "is_currently_training": open_checkin is not None,
                "can_checkin": (
                    item.get("trang_thai") == "HOAT_DONG"
                    and open_checkin is None
                    and len(valid_registrations) > 0
                ),
                "open_check_id": open_checkin.get("ma_check") if open_checkin else None,
                "current_package": open_checkin.get("ten_goi_tap") if open_checkin else "-",
                "valid_package_count": len(valid_registrations),
            })

    current_members = build_current_training_rows()

    return {
        "keyword": keyword,
        "members": members,
        "current_members": current_members,
    }


def build_current_training_rows():
    raw_rows = get_current_training_members()
    rows = []

    for item in raw_rows:
        rows.append({
            "ma_check": item.get("ma_check"),
            "ma_hoi_vien": item.get("ma_hoi_vien"),
            "ma_khach_hang": format_member_code(item.get("ma_hoi_vien")),
            "ho_ten": item.get("ho_ten"),
            "so_dien_thoai": item.get("so_dien_thoai"),
            "ten_goi_tap": item.get("ten_goi_tap") or "-",
            "thoi_gian_check_in": format_datetime(item.get("thoi_gian_check_in")),
            "loai_checkin": get_checkin_type_label(item.get("loai_checkin")),
        })

    return rows


def build_member_checkin_form(member_id):
    sync_registration_service_statuses()
    auto_close_old_open_checkins_by_member(member_id, GYM_CLOSING_TIME)
    member = get_member_for_checkin(member_id)

    if not member:
        return None

    status_text, status_class = get_member_status_label(member.get("trang_thai"))
    open_checkin = get_open_checkin_by_member(member_id)
    registrations = get_active_registrations_for_checkin(member_id)

    package_rows = []
    for item in registrations:
        package_rows.append({
            "ma_dang_ky": item.get("ma_dang_ky"),
            "ten_goi_tap": item.get("ten_goi_tap"),
            "loai_goi": "Có PT" if item.get("loai_goi") == "CO_PT" else "Không PT",
            "loai_goi_raw": item.get("loai_goi"),
            "ngay_bat_dau": item.get("ngay_bat_dau").strftime("%d/%m/%Y") if item.get("ngay_bat_dau") else "",
            "ngay_ket_thuc": item.get("ngay_ket_thuc").strftime("%d/%m/%Y") if item.get("ngay_ket_thuc") else "",
            "so_buoi_pt_con_lai": item.get("so_buoi_pt_con_lai") or 0,
            "so_buoi_pt_ban_dau": item.get("so_buoi_pt_ban_dau") or 0,
        })

    return {
        "member": {
            "ma_hoi_vien": member.get("ma_hoi_vien"),
            "ma_khach_hang": format_member_code(member.get("ma_hoi_vien")),
            "ho_ten": member.get("ho_ten"),
            "so_dien_thoai": member.get("so_dien_thoai"),
            "email": member.get("email") or "-",
            "trang_thai": member.get("trang_thai"),
            "status_text": status_text,
            "status_class": status_class,
        },
        "open_checkin": open_checkin,
        "registrations": package_rows,
    }


def pick_checkin_type_and_schedule(member_id, registration_id, selected_registration):
    package_type = selected_registration.get("loai_goi")

    if package_type == "KHONG_PT":
        return "TU_DO", None

    if package_type == "CO_PT":
        today_schedules = get_today_available_pt_schedules(
            member_id=member_id,
            registration_id=registration_id
        )

        if not today_schedules:
            raise ValueError(
                "Gói PT cần có lịch tập PT trong hôm nay mới được check-in theo PT."
            )

        schedule_id = today_schedules[0].get("ma_lich_tap")
        return "THEO_LICH_PT", schedule_id

    raise ValueError("Loại gói không hợp lệ.")


def perform_checkin(member_id, form_data):
    sync_registration_service_statuses()
    auto_close_old_open_checkins_by_member(member_id, GYM_CLOSING_TIME)
    member = get_member_for_checkin(member_id)

    if not member:
        raise ValueError("Không tìm thấy hội viên.")

    if member.get("trang_thai") != "HOAT_DONG":
        raise ValueError("Hội viên không ở trạng thái hoạt động, không thể check-in.")

    open_checkin = get_open_checkin_by_member(member_id)
    if open_checkin:
        raise ValueError("Hội viên đang ở trong phòng, cần check-out trước khi check-in mới.")

    registration_id = form_data.get("ma_dang_ky")
    note = form_data.get("ghi_chu", "").strip()

    if not registration_id:
        raise ValueError("Vui lòng chọn gói sử dụng để check-in.")

    registrations = get_active_registrations_for_checkin(member_id)
    selected_registration = None

    for item in registrations:
        if str(item.get("ma_dang_ky")) == str(registration_id):
            selected_registration = item
            break

    if not selected_registration:
        raise ValueError("Gói được chọn không hợp lệ hoặc chưa đủ điều kiện check-in.")

    final_checkin_type, schedule_id = pick_checkin_type_and_schedule(
        member_id=member_id,
        registration_id=registration_id,
        selected_registration=selected_registration
    )

    insert_checkin(
        member_id=member_id,
        registration_id=registration_id,
        schedule_id=schedule_id,
        checkin_type=final_checkin_type,
        note=note
    )

    return member_id


def perform_checkout(check_id, form_data):
    note = form_data.get("ghi_chu", "").strip()

    current_rows = get_current_training_members()
    target = None

    for row in current_rows:
        if int(row.get("ma_check")) == int(check_id):
            target = row
            break

    if not target:
        raise ValueError("Không tìm thấy lượt check-in đang mở.")

    update_checkout(check_id, note)

    return target.get("ma_hoi_vien")