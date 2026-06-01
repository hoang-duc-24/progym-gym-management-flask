import os
from uuid import uuid4
from datetime import date

from werkzeug.utils import secure_filename
from flask import current_app

from app.repositories.equipment_repository import (
    get_equipment_list,
    get_equipment_by_id,
    insert_equipment,
    update_equipment,
    get_maintenance_by_equipment,
    insert_maintenance,
    update_equipment_status,
    count_open_maintenance_by_equipment,
    get_open_maintenance_by_equipment,
    get_maintenance_by_id,
    update_maintenance_status,
)


EQUIPMENT_STATUS_OPTIONS = [
    {"value": "TOT", "label": "Đang sử dụng"},
    {"value": "DANG_BAO_TRI", "label": "Đang bảo trì"},
    {"value": "NGUNG_SU_DUNG", "label": "Ngừng sử dụng"},
]

EQUIPMENT_FORM_STATUS_OPTIONS = [
    {"value": "TOT", "label": "Đang sử dụng"},
    {"value": "NGUNG_SU_DUNG", "label": "Ngừng sử dụng"},
]

POST_MAINTENANCE_STATUS_OPTIONS = [
    {"value": "TOT", "label": "Đang sử dụng"},
    {"value": "NGUNG_SU_DUNG", "label": "Ngừng sử dụng"},
]

MAINTENANCE_STATUS_OPTIONS = [
    {"value": "CHO_XU_LY", "label": "Chờ xử lý"},
    {"value": "DA_HOAN_THANH", "label": "Đã hoàn thành"},
]

ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}


def format_date(value):
    if not value:
        return "-"

    if isinstance(value, str):
        return value

    return value.strftime("%d/%m/%Y")


def normalize_optional(value):
    value = (value or "").strip()
    return value if value else None


def get_equipment_status_label(status):
    mapping = {
        "TOT": ("Đang sử dụng", "badge-green"),
        "DANG_BAO_TRI": ("Đang bảo trì", "badge-orange"),
        "NGUNG_SU_DUNG": ("Ngừng sử dụng", "badge-gray"),

        # Giá trị cũ nếu database còn dữ liệu cũ
        "CAN_BAO_TRI": ("Đang bảo trì", "badge-orange"),
        "HONG": ("Ngừng sử dụng", "badge-gray"),
    }

    return mapping.get(status, ("Chưa rõ", "badge-gray"))


def get_maintenance_status_label(status):
    mapping = {
        "CHO_XU_LY": ("Chờ xử lý", "badge-orange"),
        "DA_HOAN_THANH": ("Đã hoàn thành", "badge-green"),

        # Giữ tạm để dữ liệu cũ không bị "Chưa rõ" nếu database còn sót.
        "DANG_XU_LY": ("Chờ xử lý", "badge-orange"),
        "HUY": ("Đã hủy", "badge-gray"),
    }

    return mapping.get(status, ("Chưa rõ", "badge-gray"))


def is_allowed_image(filename):
    if not filename or "." not in filename:
        return False

    ext = filename.rsplit(".", 1)[1].lower()
    return ext in ALLOWED_IMAGE_EXTENSIONS


def save_equipment_image(file_storage):
    if not file_storage or not file_storage.filename:
        return None

    if not is_allowed_image(file_storage.filename):
        raise ValueError("Ảnh thiết bị chỉ hỗ trợ định dạng jpg, jpeg, png hoặc webp.")

    original_name = secure_filename(file_storage.filename)
    ext = original_name.rsplit(".", 1)[1].lower()
    filename = f"{uuid4().hex}.{ext}"

    relative_dir = os.path.join("uploads", "equipment")
    absolute_dir = os.path.join(current_app.static_folder, relative_dir)
    os.makedirs(absolute_dir, exist_ok=True)

    absolute_path = os.path.join(absolute_dir, filename)
    file_storage.save(absolute_path)

    return f"uploads/equipment/{filename}"


def build_equipment_rows(raw_rows):
    rows = []

    for item in raw_rows:
        open_maintenance_count = item.get("so_bao_tri_dang_mo") or 0

        if open_maintenance_count > 0:
            status_text, status_class = get_equipment_status_label("DANG_BAO_TRI")
        else:
            status_text, status_class = get_equipment_status_label(item.get("tinh_trang"))

        rows.append({
            "ma_thiet_bi": item.get("ma_thiet_bi"),
            "ma_hien_thi": f"TB{item.get('ma_thiet_bi'):06d}",
            "ten_thiet_bi": item.get("ten_thiet_bi"),
            "loai_thiet_bi": item.get("loai_thiet_bi"),
            "vi_tri": item.get("vi_tri") or "-",
            "ngay_mua": format_date(item.get("ngay_mua")),
            "ghi_chu": item.get("ghi_chu") or "-",
            "hinh_anh": item.get("hinh_anh"),
            "status_text": status_text,
            "status_class": status_class,
            "so_lan_bao_tri": item.get("so_lan_bao_tri") or 0,
            "so_bao_tri_dang_mo": open_maintenance_count,
        })

    return rows


def build_equipment_index(filters):
    raw_rows = get_equipment_list(filters)

    return {
        "filters": filters,
        "items": build_equipment_rows(raw_rows),
        "total": len(raw_rows),
        "status_options": EQUIPMENT_STATUS_OPTIONS,
        "form_status_options": EQUIPMENT_FORM_STATUS_OPTIONS,
    }


def validate_equipment_form(form_data, image_file=None, current_image=None):
    ten_thiet_bi = (form_data.get("ten_thiet_bi") or "").strip()
    loai_thiet_bi = (form_data.get("loai_thiet_bi") or "").strip()
    vi_tri = normalize_optional(form_data.get("vi_tri"))
    ngay_mua = normalize_optional(form_data.get("ngay_mua"))
    tinh_trang = (form_data.get("tinh_trang") or "TOT").strip()
    ghi_chu = normalize_optional(form_data.get("ghi_chu"))

    if not ten_thiet_bi:
        raise ValueError("Vui lòng nhập tên thiết bị.")

    if not loai_thiet_bi:
        raise ValueError("Vui lòng nhập loại thiết bị.")

    if tinh_trang not in [item["value"] for item in EQUIPMENT_FORM_STATUS_OPTIONS]:
        raise ValueError("Tình trạng thiết bị không hợp lệ.")

    image_path = current_image

    if image_file and image_file.filename:
        image_path = save_equipment_image(image_file)

    return {
        "ten_thiet_bi": ten_thiet_bi,
        "loai_thiet_bi": loai_thiet_bi,
        "vi_tri": vi_tri,
        "ngay_mua": ngay_mua,
        "tinh_trang": tinh_trang,
        "ghi_chu": ghi_chu,
        "hinh_anh": image_path,
    }


def create_equipment(form_data, image_file=None):
    data = validate_equipment_form(form_data, image_file=image_file)
    return insert_equipment(data)


def update_equipment_info(equipment_id, form_data, image_file=None):
    equipment = get_equipment_by_id(equipment_id)

    if not equipment:
        raise ValueError("Không tìm thấy thiết bị.")

    data = validate_equipment_form(
        form_data,
        image_file=image_file,
        current_image=equipment.get("hinh_anh")
    )

    open_maintenance_count = count_open_maintenance_by_equipment(equipment_id)

    if open_maintenance_count > 0:
        raise ValueError(
            "Thiết bị đang có phiếu bảo trì chưa hoàn thành. "
            "Vui lòng xử lý phiếu bảo trì hiện tại trước khi cập nhật thiết bị."
        )

    update_equipment(equipment_id, data)
    return equipment_id


def build_equipment_form_context(equipment_id=None):
    equipment = None

    if equipment_id:
        equipment = get_equipment_by_id(equipment_id)
        if not equipment:
            return None

    return {
        "equipment": equipment,
        "status_options": EQUIPMENT_FORM_STATUS_OPTIONS,
    }


def build_maintenance_rows(raw_rows):
    rows = []

    for item in raw_rows:
        status_text, status_class = get_maintenance_status_label(item.get("trang_thai_bao_tri"))

        rows.append({
            "ma_bao_tri": item.get("ma_bao_tri"),
            "ma_hien_thi": f"BT{item.get('ma_bao_tri'):06d}",
            "ngay_ghi_nhan": format_date(item.get("ngay_ghi_nhan")),
            "noi_dung": item.get("noi_dung"),
            "status_text": status_text,
            "status_class": status_class,
            "ngay_hoan_thanh": format_date(item.get("ngay_hoan_thanh")),
            "ghi_chu": item.get("ghi_chu") or "-",
        })

    return rows


def build_equipment_detail(equipment_id):
    equipment = get_equipment_by_id(equipment_id)

    if not equipment:
        return None

    maintenance_rows = get_maintenance_by_equipment(equipment_id)
    open_maintenance = get_open_maintenance_by_equipment(equipment_id)

    if open_maintenance:
        status_text, status_class = get_equipment_status_label("DANG_BAO_TRI")
    else:
        status_text, status_class = get_equipment_status_label(equipment.get("tinh_trang"))

    return {
        "equipment": {
            "ma_thiet_bi": equipment.get("ma_thiet_bi"),
            "ma_hien_thi": f"TB{equipment.get('ma_thiet_bi'):06d}",
            "ten_thiet_bi": equipment.get("ten_thiet_bi"),
            "loai_thiet_bi": equipment.get("loai_thiet_bi"),
            "vi_tri": equipment.get("vi_tri") or "-",
            "ngay_mua": format_date(equipment.get("ngay_mua")),
            "ghi_chu": equipment.get("ghi_chu") or "-",
            "hinh_anh": equipment.get("hinh_anh"),
            "status_text": status_text,
            "status_class": status_class,
        },
        "maintenance": build_maintenance_rows(maintenance_rows),
        "total_maintenance": len(maintenance_rows),
        "open_maintenance": open_maintenance,
    }


def build_maintenance_form_context(equipment_id):
    equipment = get_equipment_by_id(equipment_id)

    if not equipment:
        return None

    open_maintenance = get_open_maintenance_by_equipment(equipment_id)

    return {
        "equipment": equipment,
        "open_maintenance": open_maintenance,
        "maintenance_status_options": MAINTENANCE_STATUS_OPTIONS,
        "post_maintenance_status_options": POST_MAINTENANCE_STATUS_OPTIONS,
    }


def record_maintenance(equipment_id, form_data):
    equipment = get_equipment_by_id(equipment_id)

    if not equipment:
        raise ValueError("Không tìm thấy thiết bị.")

    open_maintenance = get_open_maintenance_by_equipment(equipment_id)

    if open_maintenance:
        raise ValueError(
            "Thiết bị này đang có phiếu bảo trì chưa hoàn thành. "
            "Vui lòng xử lý phiếu hiện tại trước khi tạo phiếu mới."
        )

    noi_dung = (form_data.get("noi_dung") or "").strip()
    ngay_ghi_nhan = normalize_optional(form_data.get("ngay_ghi_nhan")) or date.today().isoformat()
    trang_thai_bao_tri = (form_data.get("trang_thai_bao_tri") or "CHO_XU_LY").strip()
    ngay_hoan_thanh = normalize_optional(form_data.get("ngay_hoan_thanh"))
    ghi_chu = normalize_optional(form_data.get("ghi_chu"))
    tinh_trang_sau_bao_tri = normalize_optional(form_data.get("tinh_trang_sau_bao_tri"))

    if not noi_dung:
        raise ValueError("Vui lòng nhập nội dung bảo trì.")

    if trang_thai_bao_tri not in [item["value"] for item in MAINTENANCE_STATUS_OPTIONS]:
        raise ValueError("Trạng thái bảo trì không hợp lệ.")

    if trang_thai_bao_tri == "DA_HOAN_THANH":
        if not ngay_hoan_thanh:
            raise ValueError("Vui lòng nhập ngày hoàn thành khi bảo trì đã hoàn thành.")
        
        if str(ngay_hoan_thanh) < str(ngay_ghi_nhan):
            raise ValueError("Ngày hoàn thành không được nhỏ hơn ngày ghi nhận bảo trì.")

        if not tinh_trang_sau_bao_tri:
            raise ValueError("Vui lòng chọn tình trạng thiết bị sau bảo trì.")

        if tinh_trang_sau_bao_tri not in [item["value"] for item in POST_MAINTENANCE_STATUS_OPTIONS]:
            raise ValueError("Tình trạng thiết bị sau bảo trì không hợp lệ.")

    if trang_thai_bao_tri == "CHO_XU_LY" and ngay_hoan_thanh:
        raise ValueError("Chỉ nhập ngày hoàn thành khi trạng thái bảo trì là đã hoàn thành.")

    data = {
        "ma_thiet_bi": equipment_id,
        "ngay_ghi_nhan": ngay_ghi_nhan,
        "noi_dung": noi_dung,
        "trang_thai_bao_tri": trang_thai_bao_tri,
        "ngay_hoan_thanh": ngay_hoan_thanh,
        "ghi_chu": ghi_chu,
    }

    insert_maintenance(data)

    if trang_thai_bao_tri == "CHO_XU_LY":
        update_equipment_status(equipment_id, "DANG_BAO_TRI")

    if trang_thai_bao_tri == "DA_HOAN_THANH":
        update_equipment_status(equipment_id, tinh_trang_sau_bao_tri)

    return equipment_id


def build_resolve_maintenance_context(equipment_id, maintenance_id):
    equipment = get_equipment_by_id(equipment_id)
    maintenance = get_maintenance_by_id(maintenance_id)

    if not equipment or not maintenance:
        return None

    if maintenance.get("ma_thiet_bi") != equipment_id:
        return None

    if maintenance.get("trang_thai_bao_tri") != "CHO_XU_LY":
        raise ValueError("Phiếu bảo trì này đã được xử lý.")

    return {
        "equipment": equipment,
        "maintenance": maintenance,
        "post_maintenance_status_options": POST_MAINTENANCE_STATUS_OPTIONS,
    }


def resolve_maintenance(equipment_id, maintenance_id, form_data):
    equipment = get_equipment_by_id(equipment_id)
    maintenance = get_maintenance_by_id(maintenance_id)

    if not equipment or not maintenance:
        raise ValueError("Không tìm thấy phiếu bảo trì.")

    if maintenance.get("ma_thiet_bi") != equipment_id:
        raise ValueError("Phiếu bảo trì không thuộc thiết bị này.")

    if maintenance.get("trang_thai_bao_tri") != "CHO_XU_LY":
        raise ValueError("Phiếu bảo trì này đã được xử lý.")

    ket_qua_xu_ly = (form_data.get("ket_qua_xu_ly") or "").strip()
    ngay_hoan_thanh = normalize_optional(form_data.get("ngay_hoan_thanh"))
    tinh_trang_sau_bao_tri = normalize_optional(form_data.get("tinh_trang_sau_bao_tri"))
    ghi_chu = normalize_optional(form_data.get("ghi_chu"))

    if ket_qua_xu_ly != "DA_HOAN_THANH":
        raise ValueError("Kết quả xử lý bảo trì không hợp lệ.")

    if ket_qua_xu_ly == "DA_HOAN_THANH":
        if not ngay_hoan_thanh:
            raise ValueError("Vui lòng nhập ngày hoàn thành.")
        
        ngay_ghi_nhan = maintenance.get("ngay_ghi_nhan")

        if str(ngay_hoan_thanh) < str(ngay_ghi_nhan):
            raise ValueError("Ngày hoàn thành không được nhỏ hơn ngày ghi nhận bảo trì.")

        if not tinh_trang_sau_bao_tri:
            raise ValueError("Vui lòng chọn tình trạng thiết bị sau bảo trì.")

        if tinh_trang_sau_bao_tri not in [item["value"] for item in POST_MAINTENANCE_STATUS_OPTIONS]:
            raise ValueError("Tình trạng thiết bị sau bảo trì không hợp lệ.")

        update_maintenance_status(maintenance_id, {
            "trang_thai_bao_tri": "DA_HOAN_THANH",
            "ngay_hoan_thanh": ngay_hoan_thanh,
            "ghi_chu": ghi_chu,
        })

        update_equipment_status(equipment_id, tinh_trang_sau_bao_tri)
        return equipment_id


    return equipment_id