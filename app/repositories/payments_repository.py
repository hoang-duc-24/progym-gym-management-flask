from app.db import fetch_one, execute


def get_registration_for_payment(registration_id):
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

            hv.ho_ten AS ten_hoi_vien,
            hv.so_dien_thoai,

            gt.ten_goi_tap,
            gt.loai_goi
        FROM DangKyGoiTap dkg
        JOIN HoiVien hv ON dkg.ma_hoi_vien = hv.ma_hoi_vien
        JOIN GoiTap gt ON dkg.ma_goi_tap = gt.ma_goi_tap
        WHERE dkg.ma_dang_ky = %s
        LIMIT 1
    """
    return fetch_one(sql, (registration_id,))


def get_total_paid_by_registration(registration_id):
    sql = """
        SELECT COALESCE(SUM(so_tien), 0) AS total_paid
        FROM ThanhToan
        WHERE ma_dang_ky = %s
          AND trang_thai_thanh_toan = 'DA_THANH_TOAN'
    """
    result = fetch_one(sql, (registration_id,))
    return result["total_paid"] if result else 0


def insert_payment(registration_id, account_id, amount, payment_method, note):
    sql = """
        INSERT INTO ThanhToan (
            ma_dang_ky,
            ma_tai_khoan_tao,
            ngay_thanh_toan,
            so_tien,
            hinh_thuc_thanh_toan,
            trang_thai_thanh_toan,
            ghi_chu
        )
        VALUES (%s, %s, NOW(), %s, %s, 'DA_THANH_TOAN', %s)
    """
    return execute(sql, (
        registration_id,
        account_id,
        # payment_date,
        amount,
        payment_method,
        note
    ))


def update_registration_payment_status(registration_id, payment_status, service_status):
    sql = """
        UPDATE DangKyGoiTap
        SET
            trang_thai_thanh_toan = %s,
            trang_thai_hieu_luc = %s
        WHERE ma_dang_ky = %s
    """
    return execute(sql, (
        payment_status,
        service_status,
        registration_id
    ))