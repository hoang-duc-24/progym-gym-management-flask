from app.db import fetch_all, fetch_one, execute


def get_pts(filters=None):
    filters = filters or {}

    sql = """
        SELECT
            pt.ma_pt,
            pt.ma_tai_khoan,
            pt.ho_ten,
            pt.so_dien_thoai,
            pt.email,
            pt.chuyen_mon,
            pt.kinh_nghiem,
            pt.trang_thai_lam_viec,
            pt.ghi_chu,

            COUNT(DISTINCT pc.ma_phan_cong) AS so_phan_cong,
            COUNT(DISTINCT CASE 
                WHEN pc.trang_thai = 'DANG_PHU_TRACH' THEN pc.ma_phan_cong 
            END) AS so_phan_cong_dang_phu_trach,
            COUNT(DISTINCT lt.ma_lich_tap) AS so_lich_tap
        FROM PT pt
        LEFT JOIN PhanCongPT pc ON pt.ma_pt = pc.ma_pt
        LEFT JOIN LichTap lt ON pc.ma_phan_cong = lt.ma_phan_cong
        WHERE 1 = 1
    """

    params = []

    if filters.get("trang_thai_lam_viec"):
        sql += " AND pt.trang_thai_lam_viec = %s"
        params.append(filters["trang_thai_lam_viec"])

    if filters.get("keyword"):
        sql += """
            AND (
                pt.ho_ten LIKE %s
                OR pt.so_dien_thoai LIKE %s
                OR pt.email LIKE %s
                OR pt.chuyen_mon LIKE %s
            )
        """
        keyword = f"%{filters['keyword']}%"
        params.extend([keyword, keyword, keyword, keyword])

    sql += """
        GROUP BY
            pt.ma_pt,
            pt.ma_tai_khoan,
            pt.ho_ten,
            pt.so_dien_thoai,
            pt.email,
            pt.chuyen_mon,
            pt.kinh_nghiem,
            pt.trang_thai_lam_viec,
            pt.ghi_chu
        ORDER BY pt.ma_pt DESC
    """

    return fetch_all(sql, tuple(params))


def get_pt_by_id(pt_id):
    sql = """
        SELECT
            ma_pt,
            ma_tai_khoan,
            ho_ten,
            so_dien_thoai,
            email,
            chuyen_mon,
            kinh_nghiem,
            trang_thai_lam_viec,
            ghi_chu
        FROM PT
        WHERE ma_pt = %s
        LIMIT 1
    """
    return fetch_one(sql, (pt_id,))


def get_pt_by_phone(phone):
    sql = """
        SELECT
            ma_pt,
            ho_ten,
            so_dien_thoai
        FROM PT
        WHERE so_dien_thoai = %s
        LIMIT 1
    """
    return fetch_one(sql, (phone,))


def insert_pt(data):
    sql = """
        INSERT INTO PT (
            ho_ten,
            so_dien_thoai,
            email,
            chuyen_mon,
            kinh_nghiem,
            trang_thai_lam_viec,
            ghi_chu
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    return execute(sql, (
        data["ho_ten"],
        data["so_dien_thoai"],
        data["email"],
        data["chuyen_mon"],
        data["kinh_nghiem"],
        data["trang_thai_lam_viec"],
        data["ghi_chu"],
    ))


def update_pt(pt_id, data):
    sql = """
        UPDATE PT
        SET
            ho_ten = %s,
            so_dien_thoai = %s,
            email = %s,
            chuyen_mon = %s,
            kinh_nghiem = %s,
            trang_thai_lam_viec = %s,
            ghi_chu = %s
        WHERE ma_pt = %s
    """
    return execute(sql, (
        data["ho_ten"],
        data["so_dien_thoai"],
        data["email"],
        data["chuyen_mon"],
        data["kinh_nghiem"],
        data["trang_thai_lam_viec"],
        data["ghi_chu"],
        pt_id,
    ))


def get_pt_assignments(pt_id):
    sql = """
        SELECT
            pc.ma_phan_cong,
            pc.ma_dang_ky,
            pc.ngay_phan_cong,
            pc.ngay_ket_thuc,
            pc.trang_thai,
            pc.ghi_chu,

            hv.ma_hoi_vien,
            hv.ho_ten AS ten_hoi_vien,
            hv.so_dien_thoai AS sdt_hoi_vien,

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
        JOIN GoiTap gt ON dkg.ma_goi_tap = gt.ma_goi_tap
        WHERE pc.ma_pt = %s
        ORDER BY
            CASE 
                WHEN pc.trang_thai = 'DANG_PHU_TRACH' THEN 1
                ELSE 2
            END,
            pc.ngay_phan_cong DESC,
            pc.ma_phan_cong DESC
    """
    return fetch_all(sql, (pt_id,))


def get_pt_schedules(pt_id):
    sql = """
        SELECT
            lt.ma_lich_tap,
            lt.ngay_tap,
            lt.gio_bat_dau,
            lt.gio_ket_thuc,
            lt.trang_thai_buoi_tap,
            lt.ghi_chu,

            hv.ma_hoi_vien,
            hv.ho_ten AS ten_hoi_vien,
            hv.so_dien_thoai AS sdt_hoi_vien,

            gt.ten_goi_tap
        FROM LichTap lt
        JOIN PhanCongPT pc ON lt.ma_phan_cong = pc.ma_phan_cong
        JOIN DangKyGoiTap dkg ON pc.ma_dang_ky = dkg.ma_dang_ky
        JOIN HoiVien hv ON dkg.ma_hoi_vien = hv.ma_hoi_vien
        JOIN GoiTap gt ON dkg.ma_goi_tap = gt.ma_goi_tap
        WHERE pc.ma_pt = %s
        ORDER BY lt.ngay_tap DESC, lt.gio_bat_dau DESC
    """
    return fetch_all(sql, (pt_id,))


def count_future_schedules_by_pt(pt_id):
    sql = """
        SELECT COUNT(*) AS total
        FROM LichTap lt
        JOIN PhanCongPT pc ON lt.ma_phan_cong = pc.ma_phan_cong
        WHERE pc.ma_pt = %s
          AND lt.ngay_tap >= CURDATE()
          AND lt.trang_thai_buoi_tap = 'DA_LEN_LICH'
    """
    result = fetch_one(sql, (pt_id,))
    return result["total"] if result else 0

def count_active_assignments_by_pt(pt_id):
    sql = """
        SELECT COUNT(*) AS total
        FROM PhanCongPT
        WHERE ma_pt = %s
          AND trang_thai = 'DANG_PHU_TRACH'
    """
    result = fetch_one(sql, (pt_id,))
    return result["total"] if result else 0