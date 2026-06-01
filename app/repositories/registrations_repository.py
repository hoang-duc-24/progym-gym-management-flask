from app.db import fetch_all, fetch_one


def get_registrations(filters=None):
    filters = filters or {}

    sql = """
        SELECT
            dkg.ma_dang_ky,
            dkg.ma_hoi_vien,
            dkg.ma_goi_tap,
            dkg.ngay_dang_ky,
            dkg.ngay_bat_dau,
            dkg.ngay_ket_thuc,
            dkg.so_buoi_pt_ban_dau,
            dkg.so_buoi_pt_con_lai,
            dkg.tong_tien_phai_tra,
            dkg.trang_thai_thanh_toan,
            dkg.trang_thai_hieu_luc,
            dkg.ghi_chu,
            dkg.created_at,

            hv.ho_ten AS ten_hoi_vien,
            hv.so_dien_thoai,
            hv.email,
            hv.trang_thai AS trang_thai_hoi_vien,

            gt.ten_goi_tap,
            gt.loai_goi,
            gt.thoi_han_ngay,

            COALESCE(payment_summary.da_thanh_toan, 0) AS da_thanh_toan,
            COALESCE(payment_summary.so_giao_dich, 0) AS so_giao_dich,
            COALESCE(assignment_summary.so_phan_cong, 0) AS so_phan_cong,
            COALESCE(schedule_summary.so_lich_tap, 0) AS so_lich_tap,
            COALESCE(checkin_summary.so_luot_checkin, 0) AS so_luot_checkin

        FROM DangKyGoiTap dkg
        JOIN HoiVien hv ON dkg.ma_hoi_vien = hv.ma_hoi_vien
        JOIN GoiTap gt ON dkg.ma_goi_tap = gt.ma_goi_tap

        LEFT JOIN (
            SELECT
                ma_dang_ky,
                SUM(CASE
                    WHEN trang_thai_thanh_toan = 'DA_THANH_TOAN'
                    THEN so_tien
                    ELSE 0
                END) AS da_thanh_toan,
                COUNT(*) AS so_giao_dich
            FROM ThanhToan
            GROUP BY ma_dang_ky
        ) payment_summary
            ON dkg.ma_dang_ky = payment_summary.ma_dang_ky

        LEFT JOIN (
            SELECT
                ma_dang_ky,
                COUNT(*) AS so_phan_cong
            FROM PhanCongPT
            GROUP BY ma_dang_ky
        ) assignment_summary
            ON dkg.ma_dang_ky = assignment_summary.ma_dang_ky

        LEFT JOIN (
            SELECT
                pc.ma_dang_ky,
                COUNT(*) AS so_lich_tap
            FROM PhanCongPT pc
            JOIN LichTap lt ON pc.ma_phan_cong = lt.ma_phan_cong
            GROUP BY pc.ma_dang_ky
        ) schedule_summary
            ON dkg.ma_dang_ky = schedule_summary.ma_dang_ky

        LEFT JOIN (
            SELECT
                ma_dang_ky,
                COUNT(*) AS so_luot_checkin
            FROM CheckInOut
            GROUP BY ma_dang_ky
        ) checkin_summary
            ON dkg.ma_dang_ky = checkin_summary.ma_dang_ky

        WHERE 1 = 1
    """

    params = []

    if filters.get("keyword"):
        sql += """
            AND (
                hv.ho_ten LIKE %s
                OR hv.so_dien_thoai LIKE %s
                OR gt.ten_goi_tap LIKE %s
                OR CAST(dkg.ma_dang_ky AS CHAR) LIKE %s
            )
        """
        keyword = f"%{filters['keyword']}%"
        params.extend([keyword, keyword, keyword, keyword])

    if filters.get("loai_goi"):
        sql += " AND gt.loai_goi = %s"
        params.append(filters["loai_goi"])

    if filters.get("trang_thai_thanh_toan"):
        sql += " AND dkg.trang_thai_thanh_toan = %s"
        params.append(filters["trang_thai_thanh_toan"])

    if filters.get("trang_thai_hieu_luc"):
        sql += " AND dkg.trang_thai_hieu_luc = %s"
        params.append(filters["trang_thai_hieu_luc"])

    if filters.get("start_date"):
        sql += " AND dkg.ngay_dang_ky >= %s"
        params.append(filters["start_date"])

    if filters.get("end_date"):
        sql += " AND dkg.ngay_dang_ky <= %s"
        params.append(filters["end_date"])

    if filters.get("near_expiry") == "1":
        sql += """
            AND dkg.trang_thai_hieu_luc = 'DANG_HIEU_LUC'
            AND dkg.ngay_ket_thuc BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY)
        """

    sql += """
        ORDER BY dkg.ma_dang_ky DESC
    """

    return fetch_all(sql, tuple(params))


def get_registration_by_id(registration_id):
    sql = """
        SELECT
            dkg.ma_dang_ky,
            dkg.ma_hoi_vien,
            dkg.ma_goi_tap,
            dkg.ngay_dang_ky,
            dkg.ngay_bat_dau,
            dkg.ngay_ket_thuc,
            dkg.so_buoi_pt_ban_dau,
            dkg.so_buoi_pt_con_lai,
            dkg.tong_tien_phai_tra,
            dkg.trang_thai_thanh_toan,
            dkg.trang_thai_hieu_luc,
            dkg.ghi_chu,
            dkg.created_at,

            hv.ho_ten AS ten_hoi_vien,
            hv.so_dien_thoai,
            hv.email,
            hv.ngay_sinh,
            hv.gioi_tinh,
            hv.dia_chi,
            hv.trang_thai AS trang_thai_hoi_vien,

            gt.ten_goi_tap,
            gt.loai_goi,
            gt.gia_goi,
            gt.thoi_han_ngay,
            gt.so_buoi_pt,
            gt.trang_thai_ap_dung

        FROM DangKyGoiTap dkg
        JOIN HoiVien hv ON dkg.ma_hoi_vien = hv.ma_hoi_vien
        JOIN GoiTap gt ON dkg.ma_goi_tap = gt.ma_goi_tap
        WHERE dkg.ma_dang_ky = %s
        LIMIT 1
    """
    return fetch_one(sql, (registration_id,))


def get_payments_by_registration(registration_id):
    sql = """
        SELECT
            tt.ma_thanh_toan,
            tt.ngay_thanh_toan,
            tt.so_tien,
            tt.hinh_thuc_thanh_toan,
            tt.trang_thai_thanh_toan,
            tt.ghi_chu
        FROM ThanhToan tt
        WHERE tt.ma_dang_ky = %s
        ORDER BY tt.ngay_thanh_toan DESC, tt.ma_thanh_toan DESC
    """
    return fetch_all(sql, (registration_id,))


def get_assignments_by_registration(registration_id):
    sql = """
        SELECT
            pc.ma_phan_cong,
            pc.ngay_phan_cong,
            pc.ngay_ket_thuc,
            pc.trang_thai,
            pc.ghi_chu,

            pt.ma_pt,
            pt.ho_ten AS ten_pt,
            pt.so_dien_thoai AS sdt_pt,
            pt.trang_thai_lam_viec
        FROM PhanCongPT pc
        JOIN PT pt ON pc.ma_pt = pt.ma_pt
        WHERE pc.ma_dang_ky = %s
        ORDER BY
            CASE WHEN pc.trang_thai = 'DANG_PHU_TRACH' THEN 1 ELSE 2 END,
            pc.ngay_phan_cong DESC,
            pc.ma_phan_cong DESC
    """
    return fetch_all(sql, (registration_id,))


def get_schedules_by_registration(registration_id):
    sql = """
        SELECT
            lt.ma_lich_tap,
            lt.ngay_tap,
            lt.gio_bat_dau,
            lt.gio_ket_thuc,
            lt.trang_thai_buoi_tap,
            lt.ghi_chu,

            pt.ho_ten AS ten_pt
        FROM LichTap lt
        JOIN PhanCongPT pc ON lt.ma_phan_cong = pc.ma_phan_cong
        JOIN PT pt ON pc.ma_pt = pt.ma_pt
        WHERE pc.ma_dang_ky = %s
        ORDER BY lt.ngay_tap DESC, lt.gio_bat_dau DESC
    """
    return fetch_all(sql, (registration_id,))


def get_checkins_by_registration(registration_id):
    sql = """
        SELECT
            cio.ma_check,
            cio.thoi_gian_check_in,
            cio.thoi_gian_check_out,
            cio.loai_checkin,
            cio.trang_thai,
            cio.ghi_chu
        FROM CheckInOut cio
        WHERE cio.ma_dang_ky = %s
        ORDER BY cio.thoi_gian_check_in DESC, cio.ma_check DESC
    """
    return fetch_all(sql, (registration_id,))


def get_registration_kpis():
    sql = """
        SELECT
            COUNT(*) AS tong_dang_ky,
            SUM(CASE WHEN trang_thai_hieu_luc = 'DANG_HIEU_LUC' THEN 1 ELSE 0 END) AS dang_hieu_luc,
            SUM(CASE WHEN trang_thai_hieu_luc = 'CHUA_KICH_HOAT' THEN 1 ELSE 0 END) AS chua_kich_hoat,
            SUM(CASE WHEN trang_thai_hieu_luc = 'HET_HAN' THEN 1 ELSE 0 END) AS het_han,
            SUM(CASE WHEN trang_thai_thanh_toan = 'DA_THANH_TOAN' THEN 1 ELSE 0 END) AS da_thanh_toan,
            SUM(CASE WHEN trang_thai_thanh_toan <> 'DA_THANH_TOAN' THEN 1 ELSE 0 END) AS chua_thanh_toan_du
        FROM DangKyGoiTap
    """
    return fetch_one(sql)

def search_members_for_registration(keyword=None):
    sql = """
        SELECT
            hv.ma_hoi_vien,
            hv.ho_ten,
            hv.so_dien_thoai,
            hv.email,
            hv.ngay_tham_gia,
            hv.trang_thai,

            dkg.ma_dang_ky,
            gt.ten_goi_tap,
            gt.loai_goi,
            dkg.ngay_bat_dau,
            dkg.ngay_ket_thuc,
            dkg.so_buoi_pt_ban_dau,
            dkg.so_buoi_pt_con_lai,
            dkg.trang_thai_thanh_toan,
            dkg.trang_thai_hieu_luc

        FROM HoiVien hv

        LEFT JOIN DangKyGoiTap dkg
            ON hv.ma_hoi_vien = dkg.ma_hoi_vien
           AND dkg.ma_dang_ky = (
                SELECT dkg2.ma_dang_ky
                FROM DangKyGoiTap dkg2
                WHERE dkg2.ma_hoi_vien = hv.ma_hoi_vien
                ORDER BY dkg2.ma_dang_ky DESC
                LIMIT 1
           )

        LEFT JOIN GoiTap gt ON dkg.ma_goi_tap = gt.ma_goi_tap

        WHERE 1 = 1
    """

    params = []

    if keyword:
        sql += """
            AND (
                hv.ho_ten LIKE %s
                OR hv.so_dien_thoai LIKE %s
                OR hv.email LIKE %s
                OR CAST(hv.ma_hoi_vien AS CHAR) LIKE %s
            )
        """
        keyword_like = f"%{keyword}%"
        params.extend([keyword_like, keyword_like, keyword_like, keyword_like])

    sql += """
        ORDER BY hv.ma_hoi_vien DESC
        LIMIT 30
    """

    return fetch_all(sql, tuple(params))