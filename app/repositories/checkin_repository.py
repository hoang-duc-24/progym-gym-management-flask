from app.db import fetch_all, fetch_one, execute


def auto_close_old_open_checkins(close_time="22:00:00"):
    sql = """
        UPDATE CheckInOut
        SET
            thoi_gian_check_out = GREATEST(
                STR_TO_DATE(
                    CONCAT(DATE(thoi_gian_check_in), ' ', %s),
                    '%%Y-%%m-%%d %%H:%%i:%%s'
                ),
                DATE_ADD(thoi_gian_check_in, INTERVAL 1 MINUTE)
            ),
            trang_thai = 'DA_CHECKOUT',
            ghi_chu = CASE
                WHEN ghi_chu IS NULL OR TRIM(ghi_chu) = ''
                    THEN 'Tự động đóng do hội viên quên check-out.'
                ELSE CONCAT(ghi_chu, ' | Tự động đóng do hội viên quên check-out.')
            END
        WHERE thoi_gian_check_out IS NULL
          AND trang_thai = 'DANG_CHECKIN'
          AND DATE(thoi_gian_check_in) < CURDATE()
    """
    return execute(sql, (close_time,))


def auto_close_old_open_checkins_by_member(member_id, close_time="22:00:00"):
    sql = """
        UPDATE CheckInOut
        SET
            thoi_gian_check_out = GREATEST(
                STR_TO_DATE(
                    CONCAT(DATE(thoi_gian_check_in), ' ', %s),
                    '%%Y-%%m-%%d %%H:%%i:%%s'
                ),
                DATE_ADD(thoi_gian_check_in, INTERVAL 1 MINUTE)
            ),
            trang_thai = 'DA_CHECKOUT',
            ghi_chu = CASE
                WHEN ghi_chu IS NULL OR TRIM(ghi_chu) = ''
                    THEN 'Tự động đóng do hội viên quên check-out.'
                ELSE CONCAT(ghi_chu, ' | Tự động đóng do hội viên quên check-out.')
            END
        WHERE ma_hoi_vien = %s
          AND thoi_gian_check_out IS NULL
          AND trang_thai = 'DANG_CHECKIN'
          AND DATE(thoi_gian_check_in) < CURDATE()
    """
    return execute(sql, (close_time, member_id))


def search_members_for_checkin(keyword):
    sql = """
        SELECT
            ma_hoi_vien,
            ho_ten,
            so_dien_thoai,
            email,
            trang_thai
        FROM HoiVien
        WHERE ho_ten LIKE %s
           OR so_dien_thoai LIKE %s
        ORDER BY ma_hoi_vien DESC
        LIMIT 20
    """
    like_keyword = f"%{keyword}%"
    return fetch_all(sql, (like_keyword, like_keyword))


def get_member_for_checkin(member_id):
    sql = """
        SELECT
            ma_hoi_vien,
            ho_ten,
            so_dien_thoai,
            email,
            trang_thai
        FROM HoiVien
        WHERE ma_hoi_vien = %s
        LIMIT 1
    """
    return fetch_one(sql, (member_id,))


def get_active_registrations_for_checkin(member_id):
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

            gt.ten_goi_tap,
            gt.loai_goi
        FROM DangKyGoiTap dkg
        JOIN GoiTap gt ON dkg.ma_goi_tap = gt.ma_goi_tap
        WHERE dkg.ma_hoi_vien = %s
          AND dkg.trang_thai_thanh_toan = 'DA_THANH_TOAN'
          AND dkg.trang_thai_hieu_luc = 'DANG_HIEU_LUC'
          AND dkg.ngay_bat_dau <= CURDATE()
          AND dkg.ngay_ket_thuc >= CURDATE()
          AND (
              gt.loai_goi <> 'CO_PT'
              OR dkg.so_buoi_pt_con_lai > 0
          )
        ORDER BY dkg.ngay_ket_thuc ASC, dkg.ma_dang_ky DESC
    """
    return fetch_all(sql, (member_id,))


def get_today_available_pt_schedules(member_id, registration_id):
    sql = """
        SELECT
            lt.ma_lich_tap,
            lt.ngay_tap,
            lt.gio_bat_dau,
            lt.gio_ket_thuc,
            lt.trang_thai_buoi_tap,

            pt.ho_ten AS ten_pt
        FROM LichTap lt
        JOIN PhanCongPT pc ON lt.ma_phan_cong = pc.ma_phan_cong
        JOIN PT pt ON pc.ma_pt = pt.ma_pt
        JOIN DangKyGoiTap dkg ON pc.ma_dang_ky = dkg.ma_dang_ky
        WHERE dkg.ma_hoi_vien = %s
          AND dkg.ma_dang_ky = %s
          AND lt.ngay_tap = CURDATE()
          AND CURTIME() BETWEEN SUBTIME(lt.gio_bat_dau, '00:30:00') AND lt.gio_ket_thuc
          AND lt.trang_thai_buoi_tap = 'DA_LEN_LICH'
          AND pc.trang_thai = 'DANG_PHU_TRACH'
        ORDER BY lt.gio_bat_dau ASC
    """
    return fetch_all(sql, (member_id, registration_id))


def get_open_checkin_by_member(member_id):
    sql = """
        SELECT
            cio.ma_check,
            cio.ma_hoi_vien,
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
          AND cio.thoi_gian_check_out IS NULL
          AND cio.trang_thai = 'DANG_CHECKIN'
          AND DATE(cio.thoi_gian_check_in) = CURDATE()
        ORDER BY cio.thoi_gian_check_in DESC
        LIMIT 1
    """
    return fetch_one(sql, (member_id,))


def insert_checkin(member_id, registration_id, schedule_id, checkin_type, note):
    sql = """
        INSERT INTO CheckInOut (
            ma_hoi_vien,
            ma_dang_ky,
            ma_lich_tap,
            thoi_gian_check_in,
            thoi_gian_check_out,
            loai_checkin,
            trang_thai,
            ghi_chu
        )
        VALUES (%s, %s, %s, NOW(), NULL, %s, 'DANG_CHECKIN', %s)
    """
    return execute(sql, (
        member_id,
        registration_id,
        schedule_id,
        checkin_type,
        note
    ))


def update_checkout(check_id, note):
    sql = """
        UPDATE CheckInOut
        SET
            thoi_gian_check_out = NOW(),
            trang_thai = 'DA_CHECKOUT',
            ghi_chu = CASE
                WHEN %s IS NULL OR TRIM(%s) = '' THEN ghi_chu
                WHEN ghi_chu IS NULL OR TRIM(ghi_chu) = '' THEN %s
                ELSE CONCAT(ghi_chu, ' | Check-out: ', %s)
            END
        WHERE ma_check = %s
          AND thoi_gian_check_out IS NULL
    """
    return execute(sql, (note, note, note, note, check_id))


def get_current_training_members():
    sql = """
        SELECT
            cio.ma_check,
            cio.ma_hoi_vien,
            cio.ma_dang_ky,
            cio.ma_lich_tap,
            cio.thoi_gian_check_in,
            cio.loai_checkin,
            cio.trang_thai,

            hv.ho_ten,
            hv.so_dien_thoai,

            gt.ten_goi_tap
        FROM CheckInOut cio
        JOIN HoiVien hv ON cio.ma_hoi_vien = hv.ma_hoi_vien
        LEFT JOIN DangKyGoiTap dkg ON cio.ma_dang_ky = dkg.ma_dang_ky
        LEFT JOIN GoiTap gt ON dkg.ma_goi_tap = gt.ma_goi_tap
        WHERE cio.thoi_gian_check_out IS NULL
          AND cio.trang_thai = 'DANG_CHECKIN'
          AND DATE(cio.thoi_gian_check_in) = CURDATE()
        ORDER BY cio.thoi_gian_check_in DESC
    """
    return fetch_all(sql)