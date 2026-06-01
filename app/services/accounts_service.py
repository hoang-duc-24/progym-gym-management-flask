from app.repositories.accounts_repository import (
    get_accounts,
    get_account_by_id,
    get_account_by_username,
    get_roles,
    get_role_by_id,
    get_role_by_name,
    get_pts_available_for_account,
    get_pt_by_id,
    insert_account,
    get_latest_account_id_by_username,
    update_account,
    update_account_status,
    update_account_password,
    clear_pt_account_link,
    link_pt_to_account,
    count_active_admin_accounts,
)


ROLE_ADMIN = "ADMIN"
ROLE_RECEPTIONIST = "LE_TAN"
ROLE_PT = "PT"

STATUS_ACTIVE = "HOAT_DONG"
STATUS_LOCKED = "TAM_KHOA"


def get_role_label(role):
    mapping = {
        ROLE_ADMIN: ("Admin", "badge-blue"),
        ROLE_RECEPTIONIST: ("Lễ tân", "badge-green"),
        ROLE_PT: ("PT", "badge-gray"),
    }

    return mapping.get(role, ("Chưa rõ", "badge-gray"))


def get_status_label(status):
    mapping = {
        STATUS_ACTIVE: ("Hoạt động", "badge-green"),
        STATUS_LOCKED: ("Tạm khóa", "badge-red"),
    }

    return mapping.get(status, ("Chưa rõ", "badge-gray"))


def format_datetime(value):
    if not value:
        return ""

    if isinstance(value, str):
        return value

    return value.strftime("%d/%m/%Y %H:%M")


def build_account_rows(raw_rows, current_account_id=None):
    rows = []

    for item in raw_rows:
        role_text, role_class = get_role_label(item.get("ten_vai_tro"))
        status_text, status_class = get_status_label(item.get("trang_thai"))

        account_id = item.get("ma_tai_khoan")

        rows.append({
            "ma_tai_khoan": account_id,
            "ten_dang_nhap": item.get("ten_dang_nhap"),
            "ho_ten": item.get("ho_ten"),
            "so_dien_thoai": item.get("so_dien_thoai") or "-",
            "email": item.get("email") or "-",
            "trang_thai": item.get("trang_thai"),
            "status_text": status_text,
            "status_class": status_class,

            "ten_vai_tro": item.get("ten_vai_tro"),
            "role_text": role_text,
            "role_class": role_class,

            "ma_pt": item.get("ma_pt"),
            "ten_pt": item.get("ten_pt"),
            "trang_thai_lam_viec": item.get("trang_thai_lam_viec"),

            "created_at": format_datetime(item.get("created_at")),
            "lan_dang_nhap_cuoi": format_datetime(item.get("lan_dang_nhap_cuoi")),
            "is_current_account": str(account_id) == str(current_account_id),
            "can_lock": (
                item.get("trang_thai") == STATUS_ACTIVE
                and str(account_id) != str(current_account_id)
            ),
            "can_unlock": item.get("trang_thai") == STATUS_LOCKED,
        })

    return rows


def build_accounts_index(filters, current_account_id=None):
    raw_rows = get_accounts(filters)

    return {
        "filters": filters,
        "accounts": build_account_rows(raw_rows, current_account_id),
        "total": len(raw_rows),
        "role_options": [
            {"value": ROLE_ADMIN, "label": "Admin"},
            {"value": ROLE_RECEPTIONIST, "label": "Lễ tân"},
            {"value": ROLE_PT, "label": "PT"},
        ],
        "status_options": [
            {"value": STATUS_ACTIVE, "label": "Hoạt động"},
            {"value": STATUS_LOCKED, "label": "Tạm khóa"},
        ],
    }


def build_account_form(account_id=None):
    account = None

    if account_id:
        account = get_account_by_id(account_id)

        if not account:
            return None

    return {
        "account": account,
        "roles": get_roles(),
        "available_pts": get_pts_available_for_account(account_id),
    }


def parse_common_account_form(form_data, current_account_id=None):
    ho_ten = form_data.get("ho_ten", "").strip()
    so_dien_thoai = form_data.get("so_dien_thoai", "").strip()
    email = form_data.get("email", "").strip()
    role_id = form_data.get("ma_vai_tro", "").strip()
    pt_id = form_data.get("ma_pt", "").strip()

    if not ho_ten:
        raise ValueError("Vui lòng nhập họ tên tài khoản.")

    if not role_id:
        raise ValueError("Vui lòng chọn vai trò.")

    role = get_role_by_id(role_id)

    if not role:
        raise ValueError("Vai trò không hợp lệ.")

    role_name = role.get("ten_vai_tro")

    if role_name == ROLE_PT:
        if not pt_id:
            raise ValueError("Tài khoản vai trò PT phải được gắn với hồ sơ PT.")

        pt = get_pt_by_id(pt_id)

        if not pt:
            raise ValueError("Hồ sơ PT không hợp lệ.")

        if pt.get("trang_thai_lam_viec") != "DANG_LAM_VIEC":
            raise ValueError("Chỉ được gắn tài khoản với PT đang làm việc.")

        linked_account_id = pt.get("ma_tai_khoan")

        if linked_account_id and str(linked_account_id) != str(current_account_id or ""):
            raise ValueError("Hồ sơ PT này đã được gắn với tài khoản khác.")
    else:
        pt_id = None

    return {
        "ho_ten": ho_ten,
        "so_dien_thoai": so_dien_thoai or None,
        "email": email or None,
        "ma_vai_tro": int(role_id),
        "role_name": role_name,
        "ma_pt": int(pt_id) if pt_id else None,
    }


def parse_create_account_form(form_data):
    ten_dang_nhap = form_data.get("ten_dang_nhap", "").strip()
    mat_khau = form_data.get("mat_khau", "").strip()
    xac_nhan_mat_khau = form_data.get("xac_nhan_mat_khau", "").strip()

    if not ten_dang_nhap:
        raise ValueError("Vui lòng nhập tên đăng nhập.")

    if len(ten_dang_nhap) < 4:
        raise ValueError("Tên đăng nhập phải có ít nhất 4 ký tự.")

    if get_account_by_username(ten_dang_nhap):
        raise ValueError("Tên đăng nhập đã tồn tại.")

    if not mat_khau:
        raise ValueError("Vui lòng nhập mật khẩu.")

    if len(mat_khau) < 6:
        raise ValueError("Mật khẩu phải có ít nhất 6 ký tự.")

    if mat_khau != xac_nhan_mat_khau:
        raise ValueError("Mật khẩu xác nhận không khớp.")

    data = parse_common_account_form(form_data, current_account_id=None)
    data["ten_dang_nhap"] = ten_dang_nhap
    data["mat_khau"] = mat_khau

    return data


def parse_edit_account_form(account_id, form_data):
    return parse_common_account_form(form_data, current_account_id=account_id)


def create_account(form_data):
    data = parse_create_account_form(form_data)

    insert_account(data)

    account_id = get_latest_account_id_by_username(data["ten_dang_nhap"])

    if data.get("role_name") == ROLE_PT and data.get("ma_pt"):
        clear_pt_account_link(account_id)
        link_pt_to_account(data["ma_pt"], account_id)

    return account_id


def edit_account(account_id, form_data):
    account = get_account_by_id(account_id)

    if not account:
        raise ValueError("Không tìm thấy tài khoản.")

    data = parse_edit_account_form(account_id, form_data)

    current_role = account.get("ten_vai_tro")
    new_role = data.get("role_name")

    if current_role == ROLE_ADMIN and new_role != ROLE_ADMIN:
        active_admin_count = count_active_admin_accounts()

        if active_admin_count <= 1 and account.get("trang_thai") == STATUS_ACTIVE:
            raise ValueError("Không thể đổi vai trò của Admin đang hoạt động cuối cùng.")

    update_account(account_id, data)

    clear_pt_account_link(account_id)

    if data.get("role_name") == ROLE_PT and data.get("ma_pt"):
        link_pt_to_account(data["ma_pt"], account_id)

    return account_id


def lock_account(account_id, current_account_id):
    account = get_account_by_id(account_id)

    if not account:
        raise ValueError("Không tìm thấy tài khoản.")

    if str(account_id) == str(current_account_id):
        raise ValueError("Không thể khóa chính tài khoản đang đăng nhập.")

    if account.get("trang_thai") == STATUS_LOCKED:
        raise ValueError("Tài khoản đã ở trạng thái tạm khóa.")

    if account.get("ten_vai_tro") == ROLE_ADMIN:
        active_admin_count = count_active_admin_accounts()

        if active_admin_count <= 1:
            raise ValueError("Không thể khóa Admin đang hoạt động cuối cùng.")

    update_account_status(account_id, STATUS_LOCKED)


def unlock_account(account_id):
    account = get_account_by_id(account_id)

    if not account:
        raise ValueError("Không tìm thấy tài khoản.")

    if account.get("trang_thai") == STATUS_ACTIVE:
        raise ValueError("Tài khoản đã ở trạng thái hoạt động.")

    update_account_status(account_id, STATUS_ACTIVE)


def reset_password(account_id, form_data):
    account = get_account_by_id(account_id)

    if not account:
        raise ValueError("Không tìm thấy tài khoản.")

    new_password = form_data.get("mat_khau_moi", "").strip()
    confirm_password = form_data.get("xac_nhan_mat_khau", "").strip()

    if not new_password:
        raise ValueError("Vui lòng nhập mật khẩu mới.")

    if len(new_password) < 6:
        raise ValueError("Mật khẩu mới phải có ít nhất 6 ký tự.")

    if new_password != confirm_password:
        raise ValueError("Mật khẩu xác nhận không khớp.")

    update_account_password(account_id, new_password)

    return account_id