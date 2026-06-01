from flask import session, request, redirect, url_for, flash


ROLE_ADMIN = "ADMIN"
ROLE_RECEPTIONIST = "LE_TAN"
ROLE_PT = "PT"


ALL_ROLES = {ROLE_ADMIN, ROLE_RECEPTIONIST, ROLE_PT}
ADMIN_RECEPTIONIST = {ROLE_ADMIN, ROLE_RECEPTIONIST}
ADMIN_RECEPTIONIST_PT = {ROLE_ADMIN, ROLE_RECEPTIONIST, ROLE_PT}


EXACT_ENDPOINT_PERMISSIONS = {
    # Hội viên
    "members.index": ADMIN_RECEPTIONIST,
    "members.detail": ADMIN_RECEPTIONIST,
    "members.create": ADMIN_RECEPTIONIST,
    "members.register_package": ADMIN_RECEPTIONIST,
    "members.assign_pt": ADMIN_RECEPTIONIST,

    # Tạo lịch/cập nhật lịch đang nằm trong members_routes.py
    "members.create_schedule": ADMIN_RECEPTIONIST,
    "members.update_schedule_status_view": ADMIN_RECEPTIONIST_PT,

    # Gói tập
    "packages.index": ADMIN_RECEPTIONIST,
    "packages.create": {ROLE_ADMIN},
    "packages.edit": {ROLE_ADMIN},
    "packages.stop": {ROLE_ADMIN},
    "packages.activate": {ROLE_ADMIN},

    # Đăng ký gói
    "registrations.index": ADMIN_RECEPTIONIST,
    "registrations.create": ADMIN_RECEPTIONIST,
    "registrations.detail": ADMIN_RECEPTIONIST,

    # Thanh toán
    "payment_reports.index": ADMIN_RECEPTIONIST,
    "payments.create": ADMIN_RECEPTIONIST,

    # Check-in
    "checkin.index": ADMIN_RECEPTIONIST,
    "checkin.member_checkin": ADMIN_RECEPTIONIST,
    "checkin.checkout": ADMIN_RECEPTIONIST,

    # PT
    "pts.index": ADMIN_RECEPTIONIST,
    "pts.detail": ADMIN_RECEPTIONIST,
    "pts.create": {ROLE_ADMIN},
    "pts.edit": {ROLE_ADMIN},

    # Lịch tập
    # Lịch tập
    "schedules.index": ADMIN_RECEPTIONIST_PT,
    "schedules.create": ADMIN_RECEPTIONIST,
    "schedules.create_from_assignment": ADMIN_RECEPTIONIST,
    "schedules.update_status": ADMIN_RECEPTIONIST_PT,

    # Thiết bị
    "equipment.index": ADMIN_RECEPTIONIST,
    "equipment.create": {ROLE_ADMIN},
    "equipment.detail": ADMIN_RECEPTIONIST,
    "equipment.edit": {ROLE_ADMIN},
    "equipment.create_maintenance": ADMIN_RECEPTIONIST,

    # Báo cáo
    "reports.index": ADMIN_RECEPTIONIST,
    "reports.export": ADMIN_RECEPTIONIST,

    # Tài khoản
    "accounts.index": {ROLE_ADMIN},
    "accounts.create": {ROLE_ADMIN},
    "accounts.edit": {ROLE_ADMIN},
    "accounts.lock": {ROLE_ADMIN},
    "accounts.unlock": {ROLE_ADMIN},
    "accounts.reset_password_view": {ROLE_ADMIN},
    
}


def get_current_role():
    return session.get("role")


def get_default_page_for_role(role):
    if role == ROLE_PT:
        return "schedules.index"

    return "members.index"


def get_allowed_roles_for_endpoint(endpoint):
    if not endpoint:
        return set()

    if endpoint in EXACT_ENDPOINT_PERMISSIONS:
        return EXACT_ENDPOINT_PERMISSIONS[endpoint]

    # Nếu route mới phát sinh mà chưa khai báo quyền, mặc định chỉ ADMIN được vào.
    return {ROLE_ADMIN}


def permission_guard():
    endpoint = request.endpoint

    if endpoint is None:
        return None

    if endpoint == "static":
        return None

    if endpoint.startswith("auth."):
        return None

    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    role = get_current_role()
    allowed_roles = get_allowed_roles_for_endpoint(endpoint)

    if role not in allowed_roles:
        flash("Bạn không có quyền truy cập chức năng này.", "error")

        fallback_endpoint = get_default_page_for_role(role)

        if endpoint == fallback_endpoint:
            return redirect(url_for("auth.logout"))

        return redirect(url_for(fallback_endpoint))

    return None