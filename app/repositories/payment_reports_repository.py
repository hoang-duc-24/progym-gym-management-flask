from app.db import fetch_all


def get_payment_transactions(filters=None):
    filters = filters or {}

    sql = """
        SELECT
            tt.ma_thanh_toan,
            tt.ngay_thanh_toan,
            tt.so_tien,
            tt.hinh_thuc_thanh_toan,
            tt.trang_thai_thanh_toan,
            tt.ghi_chu,

            dkg.ma_dang_ky,
            dkg.tong_tien_phai_tra,
            dkg.trang_thai_thanh_toan AS trang_thai_dang_ky,
            dkg.trang_thai_hieu_luc,

            hv.ma_hoi_vien,
            hv.ho_ten AS ten_hoi_vien,
            hv.so_dien_thoai,

            gt.ma_goi_tap,
            gt.ten_goi_tap,
            gt.loai_goi
        FROM ThanhToan tt
        JOIN DangKyGoiTap dkg ON tt.ma_dang_ky = dkg.ma_dang_ky
        JOIN HoiVien hv ON dkg.ma_hoi_vien = hv.ma_hoi_vien
        JOIN GoiTap gt ON dkg.ma_goi_tap = gt.ma_goi_tap
        WHERE 1 = 1
    """

    params = []

    if filters.get("date_from"):
        sql += " AND DATE(tt.ngay_thanh_toan) >= %s"
        params.append(filters["date_from"])

    if filters.get("date_to"):
        sql += " AND DATE(tt.ngay_thanh_toan) <= %s"
        params.append(filters["date_to"])

    if filters.get("hinh_thuc_thanh_toan"):
        sql += " AND tt.hinh_thuc_thanh_toan = %s"
        params.append(filters["hinh_thuc_thanh_toan"])

    if filters.get("trang_thai_thanh_toan"):
        sql += " AND tt.trang_thai_thanh_toan = %s"
        params.append(filters["trang_thai_thanh_toan"])

    if filters.get("keyword"):
        sql += """
            AND (
                hv.ho_ten LIKE %s
                OR hv.so_dien_thoai LIKE %s
                OR gt.ten_goi_tap LIKE %s
            )
        """
        keyword = f"%{filters['keyword']}%"
        params.extend([keyword, keyword, keyword])

    sql += """
        ORDER BY tt.ngay_thanh_toan DESC, tt.ma_thanh_toan DESC
    """

    return fetch_all(sql, tuple(params))


def get_payment_summary(filters=None):
    filters = filters or {}

    sql = """
        SELECT
            COUNT(*) AS so_giao_dich,
            COALESCE(SUM(CASE
                WHEN tt.trang_thai_thanh_toan = 'DA_THANH_TOAN'
                THEN tt.so_tien
                ELSE 0
            END), 0) AS tong_tien
        FROM ThanhToan tt
        JOIN DangKyGoiTap dkg ON tt.ma_dang_ky = dkg.ma_dang_ky
        JOIN HoiVien hv ON dkg.ma_hoi_vien = hv.ma_hoi_vien
        JOIN GoiTap gt ON dkg.ma_goi_tap = gt.ma_goi_tap
        WHERE 1 = 1
    """

    params = []

    if filters.get("date_from"):
        sql += " AND DATE(tt.ngay_thanh_toan) >= %s"
        params.append(filters["date_from"])

    if filters.get("date_to"):
        sql += " AND DATE(tt.ngay_thanh_toan) <= %s"
        params.append(filters["date_to"])

    if filters.get("hinh_thuc_thanh_toan"):
        sql += " AND tt.hinh_thuc_thanh_toan = %s"
        params.append(filters["hinh_thuc_thanh_toan"])

    if filters.get("trang_thai_thanh_toan"):
        sql += " AND tt.trang_thai_thanh_toan = %s"
        params.append(filters["trang_thai_thanh_toan"])

    if filters.get("keyword"):
        sql += """
            AND (
                hv.ho_ten LIKE %s
                OR hv.so_dien_thoai LIKE %s
                OR gt.ten_goi_tap LIKE %s
            )
        """
        keyword = f"%{filters['keyword']}%"
        params.extend([keyword, keyword, keyword])

    return fetch_all(sql, tuple(params))[0]


def get_payment_summary_by_method(filters=None):
    filters = filters or {}

    sql = """
        SELECT
            tt.hinh_thuc_thanh_toan,
            COUNT(*) AS so_giao_dich,
            COALESCE(SUM(CASE
                WHEN tt.trang_thai_thanh_toan = 'DA_THANH_TOAN'
                THEN tt.so_tien
                ELSE 0
            END), 0) AS tong_tien
        FROM ThanhToan tt
        JOIN DangKyGoiTap dkg ON tt.ma_dang_ky = dkg.ma_dang_ky
        JOIN HoiVien hv ON dkg.ma_hoi_vien = hv.ma_hoi_vien
        JOIN GoiTap gt ON dkg.ma_goi_tap = gt.ma_goi_tap
        WHERE 1 = 1
    """

    params = []

    if filters.get("date_from"):
        sql += " AND DATE(tt.ngay_thanh_toan) >= %s"
        params.append(filters["date_from"])

    if filters.get("date_to"):
        sql += " AND DATE(tt.ngay_thanh_toan) <= %s"
        params.append(filters["date_to"])

    if filters.get("trang_thai_thanh_toan"):
        sql += " AND tt.trang_thai_thanh_toan = %s"
        params.append(filters["trang_thai_thanh_toan"])

    if filters.get("keyword"):
        sql += """
            AND (
                hv.ho_ten LIKE %s
                OR hv.so_dien_thoai LIKE %s
                OR gt.ten_goi_tap LIKE %s
            )
        """
        keyword = f"%{filters['keyword']}%"
        params.extend([keyword, keyword, keyword])

    sql += """
        GROUP BY tt.hinh_thuc_thanh_toan
        ORDER BY tong_tien DESC
    """

    return fetch_all(sql, tuple(params))