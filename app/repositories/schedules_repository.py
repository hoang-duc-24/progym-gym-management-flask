from app.db import fetch_all


def get_all_pts(account_id=None):
    sql = """
        SELECT
            ma_pt,
            ho_ten,
            so_dien_thoai,
            chuyen_mon,
            trang_thai_lam_viec
        FROM PT
        WHERE trang_thai_lam_viec = 'DANG_LAM_VIEC'
    """

    params = []

    if account_id:
        sql += " AND ma_tai_khoan = %s"
        params.append(account_id)

    sql += """
        ORDER BY ho_ten
    """

    return fetch_all(sql, tuple(params))


def get_schedules(filters):
    sql = """
        SELECT
            lt.ma_lich_tap,
            lt.ngay_tap,
            lt.gio_bat_dau,
            lt.gio_ket_thuc,
            lt.trang_thai_buoi_tap,
            lt.ghi_chu,

            pc.ma_phan_cong,
            pc.trang_thai AS trang_thai_phan_cong,

            hv.ma_hoi_vien,
            hv.ho_ten AS ten_hoi_vien,
            hv.so_dien_thoai AS sdt_hoi_vien,

            pt.ma_pt,
            pt.ho_ten AS ten_pt,
            pt.so_dien_thoai AS sdt_pt,

            gt.ten_goi_tap,
            gt.loai_goi,

            dkg.ma_dang_ky,
            dkg.so_buoi_pt_ban_dau,
            dkg.so_buoi_pt_con_lai,
            dkg.trang_thai_thanh_toan,
            dkg.trang_thai_hieu_luc
        FROM LichTap lt
        JOIN PhanCongPT pc ON lt.ma_phan_cong = pc.ma_phan_cong
        JOIN DangKyGoiTap dkg ON pc.ma_dang_ky = dkg.ma_dang_ky
        JOIN HoiVien hv ON dkg.ma_hoi_vien = hv.ma_hoi_vien
        JOIN PT pt ON pc.ma_pt = pt.ma_pt
        JOIN GoiTap gt ON dkg.ma_goi_tap = gt.ma_goi_tap
        WHERE 1 = 1
    """

    params = []

    if filters.get("pt_account_id"):
        sql += """
            AND pt.ma_tai_khoan = %s
            AND pt.trang_thai_lam_viec = 'DANG_LAM_VIEC'
        """
        params.append(filters["pt_account_id"])

    if filters.get("ngay_tap"):
        sql += " AND lt.ngay_tap = %s"
        params.append(filters["ngay_tap"])

    if filters.get("ma_pt"):
        sql += " AND pt.ma_pt = %s"
        params.append(filters["ma_pt"])

    if filters.get("trang_thai_buoi_tap"):
        sql += " AND lt.trang_thai_buoi_tap = %s"
        params.append(filters["trang_thai_buoi_tap"])

    if filters.get("keyword"):
        sql += """
            AND (
                hv.ho_ten LIKE %s
                OR hv.so_dien_thoai LIKE %s
                OR pt.ho_ten LIKE %s
            )
        """
        keyword = f"%{filters['keyword']}%"
        params.extend([keyword, keyword, keyword])

    sql += """
        ORDER BY lt.ngay_tap DESC, lt.gio_bat_dau DESC, lt.ma_lich_tap DESC
    """

    return fetch_all(sql, tuple(params))

def get_schedulable_assignments(filters):
    sql = """
        SELECT
            pc.ma_phan_cong,
            pc.ma_dang_ky,
            pc.ma_pt,
            pc.ngay_phan_cong,
            pc.ngay_ket_thuc,
            pc.trang_thai AS trang_thai_phan_cong,

            hv.ma_hoi_vien,
            hv.ho_ten AS ten_hoi_vien,
            hv.so_dien_thoai AS sdt_hoi_vien,
            hv.trang_thai AS trang_thai_hoi_vien,
            
            pt.ho_ten AS ten_pt,
            pt.so_dien_thoai AS sdt_pt,
            pt.trang_thai_lam_viec,

            gt.ten_goi_tap,
            gt.loai_goi,

            dkg.ngay_bat_dau,
            dkg.ngay_ket_thuc AS ngay_ket_thuc_goi,
            dkg.so_buoi_pt_ban_dau,
            dkg.so_buoi_pt_con_lai,
            dkg.trang_thai_thanh_toan,
            dkg.trang_thai_hieu_luc
        FROM PhanCongPT pc
        JOIN DangKyGoiTap dkg ON pc.ma_dang_ky = dkg.ma_dang_ky
        JOIN HoiVien hv ON dkg.ma_hoi_vien = hv.ma_hoi_vien
        JOIN PT pt ON pc.ma_pt = pt.ma_pt
        JOIN GoiTap gt ON dkg.ma_goi_tap = gt.ma_goi_tap
        WHERE pc.trang_thai = 'DANG_PHU_TRACH'
          AND hv.trang_thai = 'HOAT_DONG'
          AND pt.trang_thai_lam_viec = 'DANG_LAM_VIEC'
          AND gt.loai_goi = 'CO_PT'
          AND dkg.trang_thai_thanh_toan = 'DA_THANH_TOAN'
          AND dkg.trang_thai_hieu_luc IN ('DANG_HIEU_LUC', 'CHUA_KICH_HOAT')
          AND dkg.so_buoi_pt_con_lai > 0
    """

    params = []

    if filters.get("ma_pt"):
        sql += " AND pt.ma_pt = %s"
        params.append(filters["ma_pt"])

    if filters.get("trang_thai_hieu_luc"):
        sql += " AND dkg.trang_thai_hieu_luc = %s"
        params.append(filters["trang_thai_hieu_luc"])

    if filters.get("keyword"):
        sql += """
            AND (
                hv.ho_ten LIKE %s
                OR hv.so_dien_thoai LIKE %s
                OR pt.ho_ten LIKE %s
                OR gt.ten_goi_tap LIKE %s
            )
        """
        keyword = f"%{filters['keyword']}%"
        params.extend([keyword, keyword, keyword, keyword])

    sql += """
        ORDER BY
            dkg.trang_thai_hieu_luc ASC,
            pc.ngay_phan_cong DESC,
            pc.ma_phan_cong DESC
    """

    return fetch_all(sql, tuple(params))