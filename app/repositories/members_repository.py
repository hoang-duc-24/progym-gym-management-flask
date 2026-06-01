from app.db import fetch_all
from app.db import fetch_one
from app.db import execute

def build_member_filter_sql(filters=None):
    filters = filters or {}

    conditions = []
    params = []

    keyword = filters.get("keyword")
    payment_status = filters.get("payment_status")
    member_status = filters.get("member_status")
    package_type = filters.get("package_type")
    service_status = filters.get("service_status")
    expire_days = filters.get("expire_days") or "3"

    if keyword:
        conditions.append("""
            (
                hv.ho_ten LIKE %s
                OR hv.so_dien_thoai LIKE %s
                OR CAST(hv.ma_hoi_vien AS CHAR) LIKE %s
            )
        """)
        keyword_like = f"%{keyword}%"
        params.extend([keyword_like, keyword_like, keyword_like])

    if payment_status == "DA_THANH_TOAN":
        conditions.append("dkg.trang_thai_thanh_toan = 'DA_THANH_TOAN'")

    elif payment_status == "CON_NO":
        conditions.append("""
            dkg.ma_dang_ky IS NOT NULL
            AND dkg.trang_thai_thanh_toan <> 'DA_THANH_TOAN'
        """)

    if member_status:
        conditions.append("hv.trang_thai = %s")
        params.append(member_status)

    if package_type:
        conditions.append("gt.loai_goi = %s")
        params.append(package_type)

    if service_status == "DANG_HIEU_LUC":
        conditions.append("""
            dkg.ma_dang_ky IS NOT NULL
            AND dkg.trang_thai_thanh_toan = 'DA_THANH_TOAN'
            AND dkg.ngay_bat_dau <= CURDATE()
            AND dkg.ngay_ket_thuc >= CURDATE()
            AND (
                gt.loai_goi <> 'CO_PT'
                OR dkg.so_buoi_pt_con_lai > 0
            )
        """)

    elif service_status == "HET_HAN":
        conditions.append("""
            dkg.ma_dang_ky IS NOT NULL
            AND (
                dkg.ngay_ket_thuc < CURDATE()
                OR dkg.trang_thai_hieu_luc = 'HET_HAN'
                OR (
                    gt.loai_goi = 'CO_PT'
                    AND dkg.so_buoi_pt_con_lai <= 0
                )
            )
        """)

    elif service_status == "SAP_HET_HAN":
        conditions.append("""
            dkg.ma_dang_ky IS NOT NULL
            AND dkg.ngay_ket_thuc >= CURDATE()
            AND dkg.ngay_ket_thuc <= DATE_ADD(CURDATE(), INTERVAL 7 DAY)
        """)

    elif service_status == "HET_HAN_TRONG":
        try:
            expire_days_int = int(expire_days)
        except ValueError:
            expire_days_int = 3

        conditions.append("""
            dkg.ma_dang_ky IS NOT NULL
            AND dkg.ngay_ket_thuc >= CURDATE()
            AND dkg.ngay_ket_thuc <= DATE_ADD(CURDATE(), INTERVAL %s DAY)
        """)
        params.append(expire_days_int)

    where_sql = ""

    if conditions:
        where_sql = "WHERE " + " AND ".join(conditions)

    return where_sql, params


def count_members_with_current_package(filters=None):
    where_sql, params = build_member_filter_sql(filters)

    sql = f"""
        SELECT COUNT(*) AS total
        FROM HoiVien hv
        LEFT JOIN DangKyGoiTap dkg
            ON dkg.ma_dang_ky = (
                SELECT dkg2.ma_dang_ky
                FROM DangKyGoiTap dkg2
                WHERE dkg2.ma_hoi_vien = hv.ma_hoi_vien
                ORDER BY dkg2.ngay_dang_ky DESC, dkg2.ma_dang_ky DESC
                LIMIT 1
            )
        LEFT JOIN GoiTap gt
            ON dkg.ma_goi_tap = gt.ma_goi_tap
        {where_sql}
    """

    result = fetch_one(sql, tuple(params))

    if not result:
        return 0

    return result.get("total", 0)


def get_members_with_current_package(filters=None, limit=10, offset=0):
    where_sql, params = build_member_filter_sql(filters)

    sql = f"""
        SELECT
            hv.ma_hoi_vien,
            hv.ho_ten,
            hv.so_dien_thoai,
            hv.trang_thai AS trang_thai_hoi_vien,

            dkg.ma_dang_ky,
            dkg.ngay_bat_dau,
            dkg.ngay_ket_thuc,
            dkg.so_buoi_pt_ban_dau,
            dkg.so_buoi_pt_con_lai,
            dkg.trang_thai_thanh_toan,
            dkg.trang_thai_hieu_luc,

            gt.ten_goi_tap,
            gt.loai_goi
        FROM HoiVien hv
        LEFT JOIN DangKyGoiTap dkg
            ON dkg.ma_dang_ky = (
                SELECT dkg2.ma_dang_ky
                FROM DangKyGoiTap dkg2
                WHERE dkg2.ma_hoi_vien = hv.ma_hoi_vien
                ORDER BY dkg2.ngay_dang_ky DESC, dkg2.ma_dang_ky DESC
                LIMIT 1
            )
        LEFT JOIN GoiTap gt
            ON dkg.ma_goi_tap = gt.ma_goi_tap
        {where_sql}
        ORDER BY hv.ma_hoi_vien DESC
        LIMIT %s OFFSET %s
    """

    params.extend([limit, offset])

    return fetch_all(sql, tuple(params))

def get_member_by_id(member_id):
    sql = """
        SELECT
            ma_hoi_vien,
            ho_ten,
            ngay_sinh,
            gioi_tinh,
            so_dien_thoai,
            email,
            dia_chi,
            ngay_tham_gia,
            trang_thai,
            ghi_chu
        FROM HoiVien
        WHERE ma_hoi_vien = %s
        LIMIT 1
    """
    return fetch_one(sql, (member_id,))


def get_member_registrations(member_id):
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

            gt.ten_goi_tap,
            gt.loai_goi,
            gt.thoi_han_ngay,
            gt.so_buoi_pt,
            gt.gia_goi
        FROM DangKyGoiTap dkg
        JOIN GoiTap gt ON dkg.ma_goi_tap = gt.ma_goi_tap
        WHERE dkg.ma_hoi_vien = %s
        ORDER BY dkg.ngay_dang_ky DESC, dkg.ma_dang_ky DESC
    """
    return fetch_all(sql, (member_id,))


def get_member_payments(member_id):
    sql = """
        SELECT
            tt.ma_thanh_toan,
            tt.ma_dang_ky,
            tt.ngay_thanh_toan,
            tt.so_tien,
            tt.hinh_thuc_thanh_toan,
            tt.trang_thai_thanh_toan,
            tt.ghi_chu,

            gt.ten_goi_tap,
            tk.ho_ten AS nguoi_ghi_nhan
        FROM ThanhToan tt
        JOIN DangKyGoiTap dkg ON tt.ma_dang_ky = dkg.ma_dang_ky
        JOIN GoiTap gt ON dkg.ma_goi_tap = gt.ma_goi_tap
        LEFT JOIN TaiKhoan tk ON tt.ma_tai_khoan_tao = tk.ma_tai_khoan
        WHERE dkg.ma_hoi_vien = %s
        ORDER BY tt.ngay_thanh_toan DESC, tt.ma_thanh_toan DESC
    """
    return fetch_all(sql, (member_id,))


def get_member_checkins(member_id):
    sql = """
        SELECT
            cio.ma_check,
            cio.ma_dang_ky,
            cio.ma_lich_tap,
            cio.thoi_gian_check_in,
            cio.thoi_gian_check_out,
            cio.loai_checkin,
            cio.trang_thai,
            cio.ghi_chu,
            gt.ten_goi_tap
        FROM CheckInOut cio
        LEFT JOIN DangKyGoiTap dkg ON cio.ma_dang_ky = dkg.ma_dang_ky
        LEFT JOIN GoiTap gt ON dkg.ma_goi_tap = gt.ma_goi_tap
        WHERE cio.ma_hoi_vien = %s
        ORDER BY cio.thoi_gian_check_in DESC
    """
    return fetch_all(sql, (member_id,))


def get_member_schedules(member_id):
    sql = """
        SELECT
            lt.ma_lich_tap,
            lt.ngay_tap,
            lt.gio_bat_dau,
            lt.gio_ket_thuc,
            lt.trang_thai_buoi_tap,
            lt.ghi_chu,
            pt.ho_ten AS ten_pt,
            gt.ten_goi_tap
        FROM LichTap lt
        JOIN PhanCongPT pc ON lt.ma_phan_cong = pc.ma_phan_cong
        JOIN PT pt ON pc.ma_pt = pt.ma_pt
        JOIN DangKyGoiTap dkg ON pc.ma_dang_ky = dkg.ma_dang_ky
        JOIN GoiTap gt ON dkg.ma_goi_tap = gt.ma_goi_tap
        WHERE dkg.ma_hoi_vien = %s
        ORDER BY lt.ngay_tap DESC, lt.gio_bat_dau DESC
    """
    return fetch_all(sql, (member_id,))

def get_active_packages():
    sql = """
        SELECT
            ma_goi_tap,
            ten_goi_tap,
            loai_goi,
            gia_goi,
            thoi_han_ngay,
            so_buoi_pt
        FROM GoiTap
        WHERE trang_thai_ap_dung = 'DANG_AP_DUNG'
        ORDER BY loai_goi, gia_goi
    """
    return fetch_all(sql)


def get_package_by_id(package_id):
    sql = """
        SELECT
            ma_goi_tap,
            ten_goi_tap,
            loai_goi,
            gia_goi,
            thoi_han_ngay,
            so_buoi_pt
        FROM GoiTap
        WHERE ma_goi_tap = %s
          AND trang_thai_ap_dung = 'DANG_AP_DUNG'
        LIMIT 1
    """
    return fetch_one(sql, (package_id,))


def insert_member(data):
    sql = """
        INSERT INTO HoiVien (
            ho_ten,
            ngay_sinh,
            gioi_tinh,
            so_dien_thoai,
            email,
            dia_chi,
            ngay_tham_gia,
            trang_thai,
            ghi_chu
        )
        VALUES (%s, %s, %s, %s, %s, %s, CURDATE(), 'HOAT_DONG', %s)
    """
    return execute(sql, (
        data["ho_ten"],
        data["ngay_sinh"],
        data["gioi_tinh"],
        data["so_dien_thoai"],
        data["email"],
        data["dia_chi"],
        data["ghi_chu"],
    ))


def insert_registration(data):
    sql = """
        INSERT INTO DangKyGoiTap (
            ma_hoi_vien,
            ma_goi_tap,
            ngay_dang_ky,
            ngay_bat_dau,
            ngay_ket_thuc,
            so_buoi_pt_ban_dau,
            so_buoi_pt_con_lai,
            tong_tien_phai_tra,
            trang_thai_thanh_toan,
            trang_thai_hieu_luc,
            ghi_chu
        )
        VALUES (%s, %s, CURDATE(), %s, %s, %s, %s, %s, %s, %s, %s)
    """
    return execute(sql, (
        data["ma_hoi_vien"],
        data["ma_goi_tap"],
        data["ngay_bat_dau"],
        data["ngay_ket_thuc"],
        data["so_buoi_pt_ban_dau"],
        data["so_buoi_pt_con_lai"],
        data["tong_tien_phai_tra"],
        data["trang_thai_thanh_toan"],
        data["trang_thai_hieu_luc"],
        data["ghi_chu"],
    ))

def get_pt_registration_for_assignment(registration_id):
    sql = """
        SELECT
            dkg.ma_dang_ky,
            dkg.ma_hoi_vien,
            dkg.ma_goi_tap,
            dkg.ngay_bat_dau,
            dkg.ngay_ket_thuc,
            dkg.so_buoi_pt_ban_dau,
            dkg.so_buoi_pt_con_lai,
            dkg.trang_thai_thanh_toan,
            dkg.trang_thai_hieu_luc,

            hv.ho_ten AS ten_hoi_vien,
            hv.so_dien_thoai,
            hv.trang_thai AS trang_thai_hoi_vien,
            
            gt.ten_goi_tap,
            gt.loai_goi
        FROM DangKyGoiTap dkg
        JOIN HoiVien hv ON dkg.ma_hoi_vien = hv.ma_hoi_vien
        JOIN GoiTap gt ON dkg.ma_goi_tap = gt.ma_goi_tap
        WHERE dkg.ma_dang_ky = %s
        LIMIT 1
    """
    return fetch_one(sql, (registration_id,))


def get_active_pts():
    sql = """
        SELECT
            ma_pt,
            ho_ten,
            so_dien_thoai,
            email,
            chuyen_mon,
            kinh_nghiem,
            trang_thai_lam_viec
        FROM PT
        WHERE trang_thai_lam_viec = 'DANG_LAM_VIEC'
        ORDER BY ho_ten
    """
    return fetch_all(sql)


def get_active_assignment_by_registration(registration_id):
    sql = """
        SELECT
            pc.ma_phan_cong,
            pc.ma_dang_ky,
            pc.ma_pt,
            pc.ngay_phan_cong,
            pc.ngay_ket_thuc,
            pc.trang_thai,
            pt.ho_ten AS ten_pt
        FROM PhanCongPT pc
        JOIN PT pt ON pc.ma_pt = pt.ma_pt
        WHERE pc.ma_dang_ky = %s
          AND pc.trang_thai = 'DANG_PHU_TRACH'
        LIMIT 1
    """
    return fetch_one(sql, (registration_id,))


def insert_pt_assignment(data):
    sql = """
        INSERT INTO PhanCongPT (
            ma_dang_ky,
            ma_pt,
            ngay_phan_cong,
            ngay_ket_thuc,
            trang_thai,
            ghi_chu
        )
        VALUES (%s, %s, %s, %s, 'DANG_PHU_TRACH', %s)
    """
    return execute(sql, (
        data["ma_dang_ky"],
        data["ma_pt"],
        data["ngay_phan_cong"],
        data["ngay_ket_thuc"],
        data["ghi_chu"],
    ))


def close_current_assignment(registration_id):
    sql = """
        UPDATE PhanCongPT
        SET trang_thai = 'DA_KET_THUC',
            ngay_ket_thuc = CURDATE()
        WHERE ma_dang_ky = %s
          AND trang_thai = 'DANG_PHU_TRACH'
    """
    return execute(sql, (registration_id,))


def get_assignments_by_member(member_id):
    sql = """
        SELECT
            pc.ma_phan_cong,
            pc.ma_dang_ky,
            pc.ma_pt,
            pc.ngay_phan_cong,
            pc.ngay_ket_thuc,
            pc.trang_thai,
            pc.ghi_chu,

            pt.ho_ten AS ten_pt,
            pt.so_dien_thoai AS so_dien_thoai_pt,

            gt.ten_goi_tap
        FROM PhanCongPT pc
        JOIN PT pt ON pc.ma_pt = pt.ma_pt
        JOIN DangKyGoiTap dkg ON pc.ma_dang_ky = dkg.ma_dang_ky
        JOIN GoiTap gt ON dkg.ma_goi_tap = gt.ma_goi_tap
        WHERE dkg.ma_hoi_vien = %s
        ORDER BY pc.ngay_phan_cong DESC, pc.ma_phan_cong DESC
    """
    return fetch_all(sql, (member_id,))

def get_assignment_for_schedule(assignment_id):
    sql = """
        SELECT
            pc.ma_phan_cong,
            pc.ma_dang_ky,
            pc.ma_pt,
            pc.ngay_phan_cong,
            pc.ngay_ket_thuc,
            pc.trang_thai AS trang_thai_phan_cong,

            pt.ho_ten AS ten_pt,
            pt.so_dien_thoai AS so_dien_thoai_pt,
            pt.trang_thai_lam_viec AS trang_thai_lam_viec_pt,

            dkg.ma_hoi_vien,
            dkg.ngay_bat_dau,
            dkg.ngay_ket_thuc AS ngay_ket_thuc_goi,
            dkg.so_buoi_pt_ban_dau,
            dkg.so_buoi_pt_con_lai,
            dkg.trang_thai_thanh_toan,
            dkg.trang_thai_hieu_luc,

            hv.ho_ten AS ten_hoi_vien,
            hv.so_dien_thoai AS so_dien_thoai_hoi_vien,
            hv.trang_thai AS trang_thai_hoi_vien,

            gt.ten_goi_tap,
            gt.loai_goi
        FROM PhanCongPT pc
        JOIN PT pt ON pc.ma_pt = pt.ma_pt
        JOIN DangKyGoiTap dkg ON pc.ma_dang_ky = dkg.ma_dang_ky
        JOIN HoiVien hv ON dkg.ma_hoi_vien = hv.ma_hoi_vien
        JOIN GoiTap gt ON dkg.ma_goi_tap = gt.ma_goi_tap
        WHERE pc.ma_phan_cong = %s
        LIMIT 1
    """
    return fetch_one(sql, (assignment_id,))


def get_pt_schedule_conflict(pt_id, training_date, start_time, end_time):
    sql = """
        SELECT
            lt.ma_lich_tap,
            lt.ngay_tap,
            lt.gio_bat_dau,
            lt.gio_ket_thuc,
            hv.ho_ten AS ten_hoi_vien
        FROM LichTap lt
        JOIN PhanCongPT pc ON lt.ma_phan_cong = pc.ma_phan_cong
        JOIN DangKyGoiTap dkg ON pc.ma_dang_ky = dkg.ma_dang_ky
        JOIN HoiVien hv ON dkg.ma_hoi_vien = hv.ma_hoi_vien
        WHERE pc.ma_pt = %s
          AND lt.ngay_tap = %s
          AND lt.trang_thai_buoi_tap NOT IN ('HUY', 'HOAN')
          AND (
                (%s < lt.gio_ket_thuc)
            AND (%s > lt.gio_bat_dau)
          )
        LIMIT 1
    """
    return fetch_one(sql, (
        pt_id,
        training_date,
        start_time,
        end_time
    ))

def get_member_schedule_conflict(member_id, training_date, start_time, end_time):
    sql = """
        SELECT
            lt.ma_lich_tap,
            lt.ngay_tap,
            lt.gio_bat_dau,
            lt.gio_ket_thuc,
            pt.ho_ten AS ten_pt
        FROM LichTap lt
        JOIN PhanCongPT pc ON lt.ma_phan_cong = pc.ma_phan_cong
        JOIN DangKyGoiTap dkg ON pc.ma_dang_ky = dkg.ma_dang_ky
        JOIN PT pt ON pc.ma_pt = pt.ma_pt
        WHERE dkg.ma_hoi_vien = %s
          AND lt.ngay_tap = %s
          AND lt.trang_thai_buoi_tap NOT IN ('HUY', 'HOAN')
          AND (
                (%s < lt.gio_ket_thuc)
            AND (%s > lt.gio_bat_dau)
          )
        LIMIT 1
    """
    return fetch_one(sql, (
        member_id,
        training_date,
        start_time,
        end_time
    ))


def insert_training_schedule(data):
    sql = """
        INSERT INTO LichTap (
            ma_phan_cong,
            ngay_tap,
            gio_bat_dau,
            gio_ket_thuc,
            trang_thai_buoi_tap,
            ghi_chu
        )
        VALUES (%s, %s, %s, %s, 'DA_LEN_LICH', %s)
    """
    return execute(sql, (
        data["ma_phan_cong"],
        data["ngay_tap"],
        data["gio_bat_dau"],
        data["gio_ket_thuc"],
        data["ghi_chu"],
    ))

def get_schedule_for_update(schedule_id):
    sql = """
        SELECT
            lt.ma_lich_tap,
            lt.ma_phan_cong,
            lt.ngay_tap,
            lt.gio_bat_dau,
            lt.gio_ket_thuc,
            lt.trang_thai_buoi_tap,
            lt.ghi_chu,

            pc.ma_dang_ky,
            pc.ma_pt,

            dkg.ma_hoi_vien,
            dkg.so_buoi_pt_ban_dau,
            dkg.so_buoi_pt_con_lai,
            dkg.trang_thai_hieu_luc,

            hv.ho_ten AS ten_hoi_vien,
            hv.so_dien_thoai AS so_dien_thoai_hoi_vien,

            pt.ho_ten AS ten_pt,
            pt.ma_tai_khoan AS ma_tai_khoan_pt,
            pt.trang_thai_lam_viec AS trang_thai_lam_viec_pt,

            gt.ten_goi_tap
        FROM LichTap lt
        JOIN PhanCongPT pc ON lt.ma_phan_cong = pc.ma_phan_cong
        JOIN DangKyGoiTap dkg ON pc.ma_dang_ky = dkg.ma_dang_ky
        JOIN HoiVien hv ON dkg.ma_hoi_vien = hv.ma_hoi_vien
        JOIN PT pt ON pc.ma_pt = pt.ma_pt
        JOIN GoiTap gt ON dkg.ma_goi_tap = gt.ma_goi_tap
        WHERE lt.ma_lich_tap = %s
        LIMIT 1
    """
    return fetch_one(sql, (schedule_id,))


def update_schedule_status(schedule_id, status, note):
    sql = """
        UPDATE LichTap
        SET
            trang_thai_buoi_tap = %s,
            ghi_chu = %s
        WHERE ma_lich_tap = %s
    """
    return execute(sql, (status, note, schedule_id))


def decrease_remaining_pt_session(registration_id):
    sql = """
        UPDATE DangKyGoiTap
        SET so_buoi_pt_con_lai = so_buoi_pt_con_lai - 1
        WHERE ma_dang_ky = %s
          AND so_buoi_pt_con_lai > 0
    """
    return execute(sql, (registration_id,))


def increase_remaining_pt_session(registration_id):
    sql = """
        UPDATE DangKyGoiTap
        SET so_buoi_pt_con_lai = so_buoi_pt_con_lai + 1
        WHERE ma_dang_ky = %s
          AND so_buoi_pt_con_lai < so_buoi_pt_ban_dau
    """
    return execute(sql, (registration_id,))


def mark_registration_expired_if_no_sessions(registration_id):
    sql = """
        UPDATE DangKyGoiTap
        SET trang_thai_hieu_luc = 'HET_HAN'
        WHERE ma_dang_ky = %s
          AND so_buoi_pt_ban_dau > 0
          AND so_buoi_pt_con_lai <= 0
    """
    return execute(sql, (registration_id,))

def get_member_by_phone(phone):
    sql = """
        SELECT 
            ma_hoi_vien,
            ho_ten,
            so_dien_thoai
        FROM HoiVien
        WHERE so_dien_thoai = %s
        LIMIT 1
    """
    return fetch_one(sql, (phone,))


def get_member_for_edit(member_id):
    sql = """
        SELECT
            ma_hoi_vien,
            ho_ten,
            ngay_sinh,
            gioi_tinh,
            so_dien_thoai,
            email,
            dia_chi,
            ngay_tham_gia,
            trang_thai,
            ghi_chu
        FROM HoiVien
        WHERE ma_hoi_vien = %s
    """

    return fetch_one(sql, (member_id,))


def update_member_basic_info(member_id, data):
    sql = """
        UPDATE HoiVien
        SET
            ho_ten = %s,
            ngay_sinh = %s,
            gioi_tinh = %s,
            so_dien_thoai = %s,
            email = %s,
            dia_chi = %s,
            trang_thai = %s,
            ghi_chu = %s
        WHERE ma_hoi_vien = %s
    """

    params = (
        data["ho_ten"],
        data["ngay_sinh"],
        data["gioi_tinh"],
        data["so_dien_thoai"],
        data["email"],
        data["dia_chi"],
        data["trang_thai"],
        data["ghi_chu"],
        member_id,
    )

    return execute(sql, params)

def count_open_member_registrations(member_id):
    sql = """
        SELECT COUNT(*) AS total
        FROM DangKyGoiTap dkg
        JOIN GoiTap gt
            ON dkg.ma_goi_tap = gt.ma_goi_tap
        WHERE dkg.ma_hoi_vien = %s
          AND dkg.trang_thai_thanh_toan <> 'DA_HUY'
          AND dkg.trang_thai_hieu_luc NOT IN ('HET_HAN', 'DA_HUY')
          AND dkg.ngay_ket_thuc >= CURDATE()
          AND (
                gt.loai_goi = 'KHONG_PT'
                OR (
                    gt.loai_goi = 'CO_PT'
                    AND dkg.so_buoi_pt_con_lai > 0
                )
          )
    """

    result = fetch_one(sql, (member_id,))

    if not result:
        return 0

    return result.get("total", 0)

# Không cho cùng một hội viên đăng ký lại cùng một gói nếu đăng ký cũ của gói đó đang còn hiệu lực/chưa kết thúc.
def count_open_same_package_registration(member_id, package_id):
    sql = """
        SELECT COUNT(*) AS total
        FROM DangKyGoiTap dkg
        JOIN GoiTap gt ON dkg.ma_goi_tap = gt.ma_goi_tap
        WHERE dkg.ma_hoi_vien = %s
          AND dkg.ma_goi_tap = %s
          AND dkg.trang_thai_thanh_toan = 'DA_THANH_TOAN'
          AND dkg.trang_thai_hieu_luc IN ('DANG_HIEU_LUC', 'CHUA_KICH_HOAT')
          AND dkg.ngay_ket_thuc >= CURDATE()
          AND (
                gt.loai_goi <> 'CO_PT'
                OR dkg.so_buoi_pt_con_lai > 0
          )
    """

    result = fetch_one(sql, (member_id, package_id))

    if not result:
        return 0

    return result.get("total", 0)