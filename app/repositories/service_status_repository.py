from app.db import execute


def refresh_registration_service_statuses():
    sql = """
        UPDATE DangKyGoiTap
        SET trang_thai_hieu_luc = CASE
            WHEN trang_thai_thanh_toan <> 'DA_THANH_TOAN'
                THEN 'CHUA_KICH_HOAT'

            WHEN ngay_ket_thuc < CURDATE()
                THEN 'HET_HAN'

            WHEN so_buoi_pt_ban_dau > 0
             AND so_buoi_pt_con_lai <= 0
                THEN 'HET_HAN'

            WHEN ngay_bat_dau > CURDATE()
                THEN 'CHUA_KICH_HOAT'

            ELSE 'DANG_HIEU_LUC'
        END
        WHERE trang_thai_hieu_luc NOT IN ('TAM_DUNG', 'DA_HUY')
    """
    return execute(sql)