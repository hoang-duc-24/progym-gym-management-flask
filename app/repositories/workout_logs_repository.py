from app.db import fetch_one, fetch_all, execute


def get_workout_log_by_schedule(schedule_id):
    sql = """
        SELECT
            ma_nhat_ky,
            ma_lich_tap,
            muc_tieu_buoi_tap,
            nhom_co_chinh,
            thoi_luong_phut,
            muc_do_hoan_thanh,
            tinh_trang_hoi_vien,
            nhan_xet_pt,
            ke_hoach_buoi_sau,
            ma_tai_khoan_tao,
            created_at,
            updated_at
        FROM NhatKyBuoiTap
        WHERE ma_lich_tap = %s
        LIMIT 1
    """
    return fetch_one(sql, (schedule_id,))


def get_exercise_details_by_log(log_id):
    sql = """
        SELECT
            ma_chi_tiet,
            ma_nhat_ky,
            ten_bai_tap,
            so_set,
            so_rep,
            muc_ta,
            don_vi_ta,
            thoi_gian_phut,
            ghi_chu,
            created_at
        FROM ChiTietBaiTap
        WHERE ma_nhat_ky = %s
        ORDER BY ma_chi_tiet ASC
    """
    return fetch_all(sql, (log_id,))


def get_workout_log_with_details_by_schedule(schedule_id):
    workout_log = get_workout_log_by_schedule(schedule_id)

    if not workout_log:
        return None

    workout_log["exercise_details"] = get_exercise_details_by_log(
        workout_log["ma_nhat_ky"]
    )

    return workout_log


def insert_workout_log(data):
    sql = """
        INSERT INTO NhatKyBuoiTap (
            ma_lich_tap,
            muc_tieu_buoi_tap,
            nhom_co_chinh,
            thoi_luong_phut,
            muc_do_hoan_thanh,
            tinh_trang_hoi_vien,
            nhan_xet_pt,
            ke_hoach_buoi_sau,
            ma_tai_khoan_tao
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    execute(sql, (
        data["ma_lich_tap"],
        data.get("muc_tieu_buoi_tap"),
        data.get("nhom_co_chinh"),
        data.get("thoi_luong_phut"),
        data.get("muc_do_hoan_thanh"),
        data.get("tinh_trang_hoi_vien"),
        data.get("nhan_xet_pt"),
        data.get("ke_hoach_buoi_sau"),
        data.get("ma_tai_khoan_tao"),
    ))

    row = fetch_one(
        """
            SELECT ma_nhat_ky
            FROM NhatKyBuoiTap
            WHERE ma_lich_tap = %s
            ORDER BY ma_nhat_ky DESC
            LIMIT 1
        """,
        (data["ma_lich_tap"],)
    )

    return row["ma_nhat_ky"] if row else None


def insert_exercise_detail(log_id, exercise):
    sql = """
        INSERT INTO ChiTietBaiTap (
            ma_nhat_ky,
            ten_bai_tap,
            so_set,
            so_rep,
            muc_ta,
            don_vi_ta,
            thoi_gian_phut,
            ghi_chu
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    return execute(sql, (
        log_id,
        exercise["ten_bai_tap"],
        exercise.get("so_set"),
        exercise.get("so_rep"),
        exercise.get("muc_ta"),
        exercise.get("don_vi_ta") or "kg",
        exercise.get("thoi_gian_phut"),
        exercise.get("ghi_chu"),
    ))


def insert_many_exercise_details(log_id, exercises):
    for exercise in exercises:
        insert_exercise_detail(log_id, exercise)


def get_member_workout_logs(member_id):
    sql = """
        SELECT
            nk.ma_nhat_ky,
            nk.ma_lich_tap,
            nk.muc_tieu_buoi_tap,
            nk.nhom_co_chinh,
            nk.thoi_luong_phut,
            nk.muc_do_hoan_thanh,
            nk.tinh_trang_hoi_vien,
            nk.nhan_xet_pt,
            nk.ke_hoach_buoi_sau,
            nk.created_at,
            nk.updated_at,

            lt.ngay_tap,
            lt.gio_bat_dau,
            lt.gio_ket_thuc,
            lt.trang_thai_buoi_tap,

            pt.ho_ten AS ten_pt,
            gt.ten_goi_tap
        FROM NhatKyBuoiTap nk
        JOIN LichTap lt ON nk.ma_lich_tap = lt.ma_lich_tap
        JOIN PhanCongPT pc ON lt.ma_phan_cong = pc.ma_phan_cong
        JOIN PT pt ON pc.ma_pt = pt.ma_pt
        JOIN DangKyGoiTap dkg ON pc.ma_dang_ky = dkg.ma_dang_ky
        JOIN GoiTap gt ON dkg.ma_goi_tap = gt.ma_goi_tap
        WHERE dkg.ma_hoi_vien = %s
        ORDER BY lt.ngay_tap DESC, lt.gio_bat_dau DESC, nk.ma_nhat_ky DESC
    """
    return fetch_all(sql, (member_id,))


def get_exercise_details_for_logs(log_ids):
    if not log_ids:
        return []

    placeholders = ", ".join(["%s"] * len(log_ids))

    sql = f"""
        SELECT
            ma_chi_tiet,
            ma_nhat_ky,
            ten_bai_tap,
            so_set,
            so_rep,
            muc_ta,
            don_vi_ta,
            thoi_gian_phut,
            ghi_chu
        FROM ChiTietBaiTap
        WHERE ma_nhat_ky IN ({placeholders})
        ORDER BY ma_nhat_ky ASC, ma_chi_tiet ASC
    """

    return fetch_all(sql, tuple(log_ids))