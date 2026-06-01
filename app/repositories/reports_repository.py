from app.db import fetch_all


def get_member_registrations_by_day(start_date=None, end_date=None):
    sql = """
        SELECT
            hv.ngay_tham_gia AS ngay,
            COUNT(*) AS so_luong
        FROM HoiVien hv
        WHERE 1 = 1
    """
    params = []

    if start_date:
        sql += " AND hv.ngay_tham_gia >= %s"
        params.append(start_date)

    if end_date:
        sql += " AND hv.ngay_tham_gia <= %s"
        params.append(end_date)

    sql += """
        GROUP BY hv.ngay_tham_gia
        ORDER BY hv.ngay_tham_gia ASC
    """

    return fetch_all(sql, tuple(params))


def get_member_registration_details(start_date=None, end_date=None):
    sql = """
        SELECT
            hv.ma_hoi_vien,
            hv.ho_ten,
            hv.so_dien_thoai,
            hv.email,
            hv.ngay_tham_gia,
            hv.trang_thai,
            gt.ten_goi_tap,
            dkg.trang_thai_hieu_luc
        FROM HoiVien hv
        LEFT JOIN DangKyGoiTap dkg ON hv.ma_hoi_vien = dkg.ma_hoi_vien
        LEFT JOIN GoiTap gt ON dkg.ma_goi_tap = gt.ma_goi_tap
        WHERE 1 = 1
    """
    params = []

    if start_date:
        sql += " AND hv.ngay_tham_gia >= %s"
        params.append(start_date)

    if end_date:
        sql += " AND hv.ngay_tham_gia <= %s"
        params.append(end_date)

    sql += """
        ORDER BY hv.ngay_tham_gia DESC, hv.ma_hoi_vien DESC
    """

    return fetch_all(sql, tuple(params))


def get_revenue_by_day(start_date=None, end_date=None):
    sql = """
        SELECT
            DATE(tt.ngay_thanh_toan) AS ngay,
            COALESCE(SUM(tt.so_tien), 0) AS so_tien
        FROM ThanhToan tt
        WHERE tt.trang_thai_thanh_toan = 'DA_THANH_TOAN'
    """
    params = []

    if start_date:
        sql += " AND DATE(tt.ngay_thanh_toan) >= %s"
        params.append(start_date)

    if end_date:
        sql += " AND DATE(tt.ngay_thanh_toan) <= %s"
        params.append(end_date)

    sql += """
        GROUP BY DATE(tt.ngay_thanh_toan)
        ORDER BY DATE(tt.ngay_thanh_toan) ASC
    """

    return fetch_all(sql, tuple(params))


def get_revenue_details(start_date=None, end_date=None):
    sql = """
        SELECT
            tt.ma_thanh_toan,
            tt.ngay_thanh_toan,
            hv.ho_ten,
            hv.so_dien_thoai,
            gt.ten_goi_tap,
            tt.so_tien,
            tt.hinh_thuc_thanh_toan,
            tt.ghi_chu
        FROM ThanhToan tt
        JOIN DangKyGoiTap dkg ON tt.ma_dang_ky = dkg.ma_dang_ky
        JOIN HoiVien hv ON dkg.ma_hoi_vien = hv.ma_hoi_vien
        JOIN GoiTap gt ON dkg.ma_goi_tap = gt.ma_goi_tap
        WHERE tt.trang_thai_thanh_toan = 'DA_THANH_TOAN'
    """
    params = []

    if start_date:
        sql += " AND DATE(tt.ngay_thanh_toan) >= %s"
        params.append(start_date)

    if end_date:
        sql += " AND DATE(tt.ngay_thanh_toan) <= %s"
        params.append(end_date)

    sql += """
        ORDER BY tt.ngay_thanh_toan DESC, tt.ma_thanh_toan DESC
    """

    return fetch_all(sql, tuple(params))


def get_schedules_by_status(start_date=None, end_date=None):
    sql = """
        SELECT
            lt.trang_thai_buoi_tap AS trang_thai,
            COUNT(*) AS so_luong
        FROM LichTap lt
        WHERE 1 = 1
    """
    params = []

    if start_date:
        sql += " AND lt.ngay_tap >= %s"
        params.append(start_date)

    if end_date:
        sql += " AND lt.ngay_tap <= %s"
        params.append(end_date)

    sql += """
        GROUP BY lt.trang_thai_buoi_tap
        ORDER BY so_luong DESC
    """

    return fetch_all(sql, tuple(params))


def get_schedule_details(start_date=None, end_date=None):
    sql = """
        SELECT
            lt.ma_lich_tap,
            lt.ngay_tap,
            lt.gio_bat_dau,
            lt.gio_ket_thuc,
            hv.ho_ten AS ten_hoi_vien,
            hv.so_dien_thoai,
            pt.ho_ten AS ten_pt,
            gt.ten_goi_tap,
            lt.trang_thai_buoi_tap,
            lt.ghi_chu
        FROM LichTap lt
        JOIN PhanCongPT pc ON lt.ma_phan_cong = pc.ma_phan_cong
        JOIN PT pt ON pc.ma_pt = pt.ma_pt
        JOIN DangKyGoiTap dkg ON pc.ma_dang_ky = dkg.ma_dang_ky
        JOIN HoiVien hv ON dkg.ma_hoi_vien = hv.ma_hoi_vien
        JOIN GoiTap gt ON dkg.ma_goi_tap = gt.ma_goi_tap
        WHERE 1 = 1
    """
    params = []

    if start_date:
        sql += " AND lt.ngay_tap >= %s"
        params.append(start_date)

    if end_date:
        sql += " AND lt.ngay_tap <= %s"
        params.append(end_date)

    sql += """
        ORDER BY lt.ngay_tap DESC, lt.gio_bat_dau DESC
    """

    return fetch_all(sql, tuple(params))


def get_equipment_by_status():
    sql = """
        SELECT
            tinh_trang AS trang_thai,
            COUNT(*) AS so_luong
        FROM TrangThietBi
        GROUP BY tinh_trang
        ORDER BY so_luong DESC
    """
    return fetch_all(sql)


def get_equipment_details():
    sql = """
        SELECT
            ma_thiet_bi,
            ten_thiet_bi,
            loai_thiet_bi,
            vi_tri,
            ngay_mua,
            tinh_trang,
            ghi_chu
        FROM TrangThietBi
        ORDER BY ma_thiet_bi DESC
    """
    return fetch_all(sql)

def get_checkin_by_day(start_date=None, end_date=None):
    sql = """
        SELECT
            DATE(cio.thoi_gian_check_in) AS ngay,
            COUNT(*) AS tong_luot_checkin,
            SUM(CASE WHEN cio.trang_thai = 'DA_CHECKOUT' THEN 1 ELSE 0 END) AS da_checkout,
            SUM(CASE WHEN cio.trang_thai = 'DANG_CHECKIN' THEN 1 ELSE 0 END) AS dang_trong_phong
        FROM CheckInOut cio
        WHERE 1 = 1
    """
    params = []

    if start_date:
        sql += " AND DATE(cio.thoi_gian_check_in) >= %s"
        params.append(start_date)

    if end_date:
        sql += " AND DATE(cio.thoi_gian_check_in) <= %s"
        params.append(end_date)

    sql += """
        GROUP BY DATE(cio.thoi_gian_check_in)
        ORDER BY DATE(cio.thoi_gian_check_in) ASC
    """

    return fetch_all(sql, tuple(params))


def get_checkin_details(start_date=None, end_date=None):
    sql = """
        SELECT
            cio.ma_check,
            cio.thoi_gian_check_in,
            cio.thoi_gian_check_out,
            cio.loai_checkin,
            cio.trang_thai,
            cio.ghi_chu,

            hv.ma_hoi_vien,
            hv.ho_ten,
            hv.so_dien_thoai,

            gt.ten_goi_tap
        FROM CheckInOut cio
        JOIN HoiVien hv ON cio.ma_hoi_vien = hv.ma_hoi_vien
        JOIN DangKyGoiTap dkg ON cio.ma_dang_ky = dkg.ma_dang_ky
        JOIN GoiTap gt ON dkg.ma_goi_tap = gt.ma_goi_tap
        WHERE 1 = 1
    """
    params = []

    if start_date:
        sql += " AND DATE(cio.thoi_gian_check_in) >= %s"
        params.append(start_date)

    if end_date:
        sql += " AND DATE(cio.thoi_gian_check_in) <= %s"
        params.append(end_date)

    sql += """
        ORDER BY cio.thoi_gian_check_in DESC, cio.ma_check DESC
    """

    return fetch_all(sql, tuple(params))