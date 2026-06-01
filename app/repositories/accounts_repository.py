from app.db import fetch_all, fetch_one, execute


def get_accounts(filters=None):
    filters = filters or {}

    sql = """
        SELECT
            tk.ma_tai_khoan,
            tk.ten_dang_nhap,
            tk.ho_ten,
            tk.so_dien_thoai,
            tk.email,
            tk.trang_thai,
            tk.created_at,
            tk.lan_dang_nhap_cuoi,
            tk.ma_vai_tro,

            vt.ten_vai_tro,
            vt.mo_ta AS mo_ta_vai_tro,

            pt.ma_pt,
            pt.ho_ten AS ten_pt,
            pt.trang_thai_lam_viec
        FROM TaiKhoan tk
        JOIN VaiTro vt ON tk.ma_vai_tro = vt.ma_vai_tro
        LEFT JOIN PT pt ON tk.ma_tai_khoan = pt.ma_tai_khoan
        WHERE 1 = 1
    """

    params = []

    if filters.get("keyword"):
        sql += """
            AND (
                tk.ten_dang_nhap LIKE %s
                OR tk.ho_ten LIKE %s
                OR tk.so_dien_thoai LIKE %s
                OR tk.email LIKE %s
            )
        """
        keyword = f"%{filters['keyword']}%"
        params.extend([keyword, keyword, keyword, keyword])

    if filters.get("role"):
        sql += " AND vt.ten_vai_tro = %s"
        params.append(filters["role"])

    if filters.get("status"):
        sql += " AND tk.trang_thai = %s"
        params.append(filters["status"])

    sql += """
        ORDER BY tk.ma_tai_khoan ASC
    """

    return fetch_all(sql, tuple(params))


def get_account_by_id(account_id):
    sql = """
        SELECT
            tk.ma_tai_khoan,
            tk.ten_dang_nhap,
            tk.mat_khau,
            tk.ho_ten,
            tk.so_dien_thoai,
            tk.email,
            tk.trang_thai,
            tk.ma_vai_tro,
            tk.created_at,
            tk.lan_dang_nhap_cuoi,

            vt.ten_vai_tro,

            pt.ma_pt,
            pt.ho_ten AS ten_pt,
            pt.trang_thai_lam_viec
        FROM TaiKhoan tk
        JOIN VaiTro vt ON tk.ma_vai_tro = vt.ma_vai_tro
        LEFT JOIN PT pt ON tk.ma_tai_khoan = pt.ma_tai_khoan
        WHERE tk.ma_tai_khoan = %s
        LIMIT 1
    """
    return fetch_one(sql, (account_id,))


def get_account_by_username(username):
    sql = """
        SELECT
            ma_tai_khoan,
            ten_dang_nhap
        FROM TaiKhoan
        WHERE ten_dang_nhap = %s
        LIMIT 1
    """
    return fetch_one(sql, (username,))


def get_roles():
    sql = """
        SELECT
            ma_vai_tro,
            ten_vai_tro,
            mo_ta
        FROM VaiTro
        ORDER BY ma_vai_tro ASC
    """
    return fetch_all(sql)


def get_role_by_id(role_id):
    sql = """
        SELECT
            ma_vai_tro,
            ten_vai_tro,
            mo_ta
        FROM VaiTro
        WHERE ma_vai_tro = %s
        LIMIT 1
    """
    return fetch_one(sql, (role_id,))


def get_role_by_name(role_name):
    sql = """
        SELECT
            ma_vai_tro,
            ten_vai_tro,
            mo_ta
        FROM VaiTro
        WHERE ten_vai_tro = %s
        LIMIT 1
    """
    return fetch_one(sql, (role_name,))


def get_pts_available_for_account(current_account_id=None):
    sql = """
        SELECT
            ma_pt,
            ho_ten,
            so_dien_thoai,
            chuyen_mon,
            trang_thai_lam_viec,
            ma_tai_khoan
        FROM PT
        WHERE trang_thai_lam_viec = 'DANG_LAM_VIEC'
          AND (
                ma_tai_khoan IS NULL
    """

    params = []

    if current_account_id:
        sql += " OR ma_tai_khoan = %s"
        params.append(current_account_id)

    sql += """
          )
        ORDER BY ho_ten ASC
    """

    return fetch_all(sql, tuple(params))


def get_pt_by_id(pt_id):
    sql = """
        SELECT
            ma_pt,
            ho_ten,
            so_dien_thoai,
            trang_thai_lam_viec,
            ma_tai_khoan
        FROM PT
        WHERE ma_pt = %s
        LIMIT 1
    """
    return fetch_one(sql, (pt_id,))


def insert_account(data):
    sql = """
        INSERT INTO TaiKhoan (
            ten_dang_nhap,
            mat_khau,
            ho_ten,
            so_dien_thoai,
            email,
            trang_thai,
            ma_vai_tro
        )
        VALUES (%s, %s, %s, %s, %s, 'HOAT_DONG', %s)
    """
    return execute(sql, (
        data["ten_dang_nhap"],
        data["mat_khau"],
        data["ho_ten"],
        data["so_dien_thoai"],
        data["email"],
        data["ma_vai_tro"],
    ))


def get_latest_account_id_by_username(username):
    sql = """
        SELECT ma_tai_khoan
        FROM TaiKhoan
        WHERE ten_dang_nhap = %s
        ORDER BY ma_tai_khoan DESC
        LIMIT 1
    """
    row = fetch_one(sql, (username,))
    return row.get("ma_tai_khoan") if row else None


def update_account(account_id, data):
    sql = """
        UPDATE TaiKhoan
        SET
            ho_ten = %s,
            so_dien_thoai = %s,
            email = %s,
            ma_vai_tro = %s
        WHERE ma_tai_khoan = %s
    """
    return execute(sql, (
        data["ho_ten"],
        data["so_dien_thoai"],
        data["email"],
        data["ma_vai_tro"],
        account_id,
    ))


def update_account_status(account_id, status):
    sql = """
        UPDATE TaiKhoan
        SET trang_thai = %s
        WHERE ma_tai_khoan = %s
    """
    return execute(sql, (status, account_id))


def update_account_password(account_id, new_password):
    sql = """
        UPDATE TaiKhoan
        SET mat_khau = %s
        WHERE ma_tai_khoan = %s
    """
    return execute(sql, (new_password, account_id))


def clear_pt_account_link(account_id):
    sql = """
        UPDATE PT
        SET ma_tai_khoan = NULL
        WHERE ma_tai_khoan = %s
    """
    return execute(sql, (account_id,))


def link_pt_to_account(pt_id, account_id):
    sql = """
        UPDATE PT
        SET ma_tai_khoan = %s
        WHERE ma_pt = %s
    """
    return execute(sql, (account_id, pt_id))

def count_active_admin_accounts():
    sql = """
        SELECT COUNT(*) AS total_admin
        FROM TaiKhoan tk
        JOIN VaiTro vt ON tk.ma_vai_tro = vt.ma_vai_tro
        WHERE vt.ten_vai_tro = 'ADMIN'
          AND tk.trang_thai = 'HOAT_DONG'
    """
    row = fetch_one(sql)
    return row.get("total_admin", 0) if row else 0