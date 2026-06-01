from app.db import fetch_all, fetch_one, execute


def get_equipment_list(filters=None):
    filters = filters or {}

    sql = """
        SELECT
            tb.ma_thiet_bi,
            tb.ten_thiet_bi,
            tb.loai_thiet_bi,
            tb.vi_tri,
            tb.ngay_mua,
            tb.tinh_trang,
            tb.ghi_chu,
            tb.hinh_anh,
            COUNT(bt.ma_bao_tri) AS so_lan_bao_tri,
            SUM(CASE 
                WHEN bt.trang_thai_bao_tri = 'CHO_XU_LY' THEN 1 
                ELSE 0 
            END) AS so_bao_tri_dang_mo
        FROM TrangThietBi tb
        LEFT JOIN BaoTriThietBi bt ON tb.ma_thiet_bi = bt.ma_thiet_bi
        WHERE 1 = 1
    """

    params = []

    if filters.get("tinh_trang"):
        sql += " AND tb.tinh_trang = %s"
        params.append(filters["tinh_trang"])

    if filters.get("loai_thiet_bi"):
        sql += " AND tb.loai_thiet_bi LIKE %s"
        params.append(f"%{filters['loai_thiet_bi']}%")

    if filters.get("keyword"):
        sql += """
            AND (
                tb.ten_thiet_bi LIKE %s
                OR tb.loai_thiet_bi LIKE %s
                OR tb.vi_tri LIKE %s
                OR tb.ghi_chu LIKE %s
            )
        """
        keyword = f"%{filters['keyword']}%"
        params.extend([keyword, keyword, keyword, keyword])

    sql += """
        GROUP BY
            tb.ma_thiet_bi,
            tb.ten_thiet_bi,
            tb.loai_thiet_bi,
            tb.vi_tri,
            tb.ngay_mua,
            tb.tinh_trang,
            tb.ghi_chu,
            tb.hinh_anh
        ORDER BY tb.ma_thiet_bi DESC
    """

    return fetch_all(sql, tuple(params))


def get_equipment_by_id(equipment_id):
    sql = """
        SELECT
            ma_thiet_bi,
            ten_thiet_bi,
            loai_thiet_bi,
            vi_tri,
            ngay_mua,
            tinh_trang,
            ghi_chu,
            hinh_anh
        FROM TrangThietBi
        WHERE ma_thiet_bi = %s
        LIMIT 1
    """
    return fetch_one(sql, (equipment_id,))


def insert_equipment(data):
    sql = """
        INSERT INTO TrangThietBi (
            ten_thiet_bi,
            loai_thiet_bi,
            vi_tri,
            ngay_mua,
            tinh_trang,
            ghi_chu,
            hinh_anh
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    return execute(sql, (
        data["ten_thiet_bi"],
        data["loai_thiet_bi"],
        data["vi_tri"],
        data["ngay_mua"],
        data["tinh_trang"],
        data["ghi_chu"],
        data["hinh_anh"],
    ))


def update_equipment(equipment_id, data):
    sql = """
        UPDATE TrangThietBi
        SET
            ten_thiet_bi = %s,
            loai_thiet_bi = %s,
            vi_tri = %s,
            ngay_mua = %s,
            tinh_trang = %s,
            ghi_chu = %s,
            hinh_anh = %s
        WHERE ma_thiet_bi = %s
    """
    return execute(sql, (
        data["ten_thiet_bi"],
        data["loai_thiet_bi"],
        data["vi_tri"],
        data["ngay_mua"],
        data["tinh_trang"],
        data["ghi_chu"],
        data["hinh_anh"],
        equipment_id,
    ))


def update_equipment_status(equipment_id, status):
    sql = """
        UPDATE TrangThietBi
        SET tinh_trang = %s
        WHERE ma_thiet_bi = %s
    """
    return execute(sql, (status, equipment_id))


def get_maintenance_by_equipment(equipment_id):
    sql = """
        SELECT
            ma_bao_tri,
            ma_thiet_bi,
            ngay_ghi_nhan,
            noi_dung,
            trang_thai_bao_tri,
            ngay_hoan_thanh,
            ghi_chu
        FROM BaoTriThietBi
        WHERE ma_thiet_bi = %s
        ORDER BY ngay_ghi_nhan DESC, ma_bao_tri DESC
    """
    return fetch_all(sql, (equipment_id,))


def get_maintenance_by_id(maintenance_id):
    sql = """
        SELECT
            ma_bao_tri,
            ma_thiet_bi,
            ngay_ghi_nhan,
            noi_dung,
            trang_thai_bao_tri,
            ngay_hoan_thanh,
            ghi_chu
        FROM BaoTriThietBi
        WHERE ma_bao_tri = %s
        LIMIT 1
    """
    return fetch_one(sql, (maintenance_id,))


def insert_maintenance(data):
    sql = """
        INSERT INTO BaoTriThietBi (
            ma_thiet_bi,
            ngay_ghi_nhan,
            noi_dung,
            trang_thai_bao_tri,
            ngay_hoan_thanh,
            ghi_chu
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    return execute(sql, (
        data["ma_thiet_bi"],
        data["ngay_ghi_nhan"],
        data["noi_dung"],
        data["trang_thai_bao_tri"],
        data["ngay_hoan_thanh"],
        data["ghi_chu"],
    ))


def update_maintenance_status(maintenance_id, data):
    sql = """
        UPDATE BaoTriThietBi
        SET
            trang_thai_bao_tri = %s,
            ngay_hoan_thanh = %s,
            ghi_chu = %s
        WHERE ma_bao_tri = %s
    """
    return execute(sql, (
        data["trang_thai_bao_tri"],
        data["ngay_hoan_thanh"],
        data["ghi_chu"],
        maintenance_id,
    ))


def count_open_maintenance_by_equipment(equipment_id):
    sql = """
        SELECT COUNT(*) AS total_open
        FROM BaoTriThietBi
        WHERE ma_thiet_bi = %s
          AND trang_thai_bao_tri = 'CHO_XU_LY'
    """
    row = fetch_one(sql, (equipment_id,))
    return row.get("total_open", 0) if row else 0


def get_open_maintenance_by_equipment(equipment_id):
    sql = """
        SELECT
            ma_bao_tri,
            ma_thiet_bi,
            ngay_ghi_nhan,
            noi_dung,
            trang_thai_bao_tri,
            ngay_hoan_thanh,
            ghi_chu
        FROM BaoTriThietBi
        WHERE ma_thiet_bi = %s
          AND trang_thai_bao_tri = 'CHO_XU_LY'
        ORDER BY ngay_ghi_nhan DESC, ma_bao_tri DESC
        LIMIT 1
    """
    return fetch_one(sql, (equipment_id,))