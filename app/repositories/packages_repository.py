from app.db import fetch_all, fetch_one, execute


def get_packages(filters=None):
    filters = filters or {}

    sql = """
        SELECT
            gt.ma_goi_tap,
            gt.ten_goi_tap,
            gt.loai_goi,
            gt.gia_goi,
            gt.thoi_han_ngay,
            gt.so_buoi_pt,
            gt.mo_ta,
            gt.trang_thai_ap_dung,
            COUNT(dkg.ma_dang_ky) AS so_luot_dang_ky
        FROM GoiTap gt
        LEFT JOIN DangKyGoiTap dkg ON gt.ma_goi_tap = dkg.ma_goi_tap
        WHERE 1 = 1
    """

    params = []

    if filters.get("keyword"):
        sql += " AND gt.ten_goi_tap LIKE %s"
        params.append(f"%{filters['keyword']}%")

    if filters.get("loai_goi"):
        sql += " AND gt.loai_goi = %s"
        params.append(filters["loai_goi"])

    if filters.get("trang_thai_ap_dung"):
        sql += " AND gt.trang_thai_ap_dung = %s"
        params.append(filters["trang_thai_ap_dung"])

    sql += """
        GROUP BY
            gt.ma_goi_tap,
            gt.ten_goi_tap,
            gt.loai_goi,
            gt.gia_goi,
            gt.thoi_han_ngay,
            gt.so_buoi_pt,
            gt.mo_ta,
            gt.trang_thai_ap_dung
        ORDER BY gt.ma_goi_tap
    """

    return fetch_all(sql, tuple(params))


def get_package_by_id(package_id):
    sql = """
        SELECT
            ma_goi_tap,
            ten_goi_tap,
            loai_goi,
            gia_goi,
            thoi_han_ngay,
            so_buoi_pt,
            mo_ta,
            trang_thai_ap_dung
        FROM GoiTap
        WHERE ma_goi_tap = %s
        LIMIT 1
    """
    return fetch_one(sql, (package_id,))


def count_registrations_by_package(package_id):
    sql = """
        SELECT COUNT(*) AS total
        FROM DangKyGoiTap
        WHERE ma_goi_tap = %s
    """
    row = fetch_one(sql, (package_id,))

    if not row:
        return 0

    return row.get("total") or 0


def insert_package(data):
    sql = """
        INSERT INTO GoiTap (
            ten_goi_tap,
            loai_goi,
            gia_goi,
            thoi_han_ngay,
            so_buoi_pt,
            mo_ta,
            trang_thai_ap_dung
        )
        VALUES (%s, %s, %s, %s, %s, %s, 'DANG_AP_DUNG')
    """
    return execute(sql, (
        data["ten_goi_tap"],
        data["loai_goi"],
        data["gia_goi"],
        data["thoi_han_ngay"],
        data["so_buoi_pt"],
        data["mo_ta"],
    ))


def update_package(package_id, data):
    sql = """
        UPDATE GoiTap
        SET
            ten_goi_tap = %s,
            loai_goi = %s,
            gia_goi = %s,
            thoi_han_ngay = %s,
            so_buoi_pt = %s,
            mo_ta = %s
        WHERE ma_goi_tap = %s
    """
    return execute(sql, (
        data["ten_goi_tap"],
        data["loai_goi"],
        data["gia_goi"],
        data["thoi_han_ngay"],
        data["so_buoi_pt"],
        data["mo_ta"],
        package_id,
    ))


def update_package_basic_info(package_id, data):
    sql = """
        UPDATE GoiTap
        SET
            ten_goi_tap = %s,
            mo_ta = %s
        WHERE ma_goi_tap = %s
    """
    return execute(sql, (
        data["ten_goi_tap"],
        data["mo_ta"],
        package_id,
    ))


def update_package_status(package_id, status):
    sql = """
        UPDATE GoiTap
        SET trang_thai_ap_dung = %s
        WHERE ma_goi_tap = %s
    """
    return execute(sql, (status, package_id))