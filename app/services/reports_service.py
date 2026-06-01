import csv
import io
from decimal import Decimal
from datetime import date, timedelta

from app.repositories.reports_repository import (
    get_member_registrations_by_day,
    get_member_registration_details,
    get_revenue_by_day,
    get_revenue_details,
    get_schedules_by_status,
    get_schedule_details,
    get_equipment_by_status,
    get_equipment_details,
    get_checkin_by_day,
    get_checkin_details,
)


REPORT_DATA_TYPES = [
    {"value": "members", "label": "Hội viên"},
    {"value": "revenue", "label": "Doanh thu"},
    {"value": "checkin", "label": "Check-in"},
    {"value": "schedules", "label": "Lịch tập PT"},
    {"value": "equipment", "label": "Thiết bị"},
]


VALID_REPORT_TYPES = {"members", "revenue", "checkin", "schedules", "equipment"}


def get_default_date_range():
    today = date.today()
    start_date = today - timedelta(days=30)
    return start_date.isoformat(), today.isoformat()


def normalize_date_value(value, fallback):
    value = (value or "").strip()

    if not value:
        return fallback

    try:
        date.fromisoformat(value)
        return value
    except ValueError:
        return fallback


def format_date(value):
    if not value:
        return "-"

    if isinstance(value, str):
        return value

    return value.strftime("%d/%m/%Y")


def format_datetime(value):
    if not value:
        return "-"

    if isinstance(value, str):
        return value

    return value.strftime("%d/%m/%Y %H:%M")


def format_money(value):
    if value is None:
        return "0 đ"

    return f"{Decimal(str(value)):,.0f} đ"


def format_time(value):
    if not value:
        return ""

    if isinstance(value, str):
        return value[:5]

    total_seconds = int(value.total_seconds()) if hasattr(value, "total_seconds") else None
    if total_seconds is not None:
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{hours:02d}:{minutes:02d}"

    return value.strftime("%H:%M")


def member_status_label(value):
    mapping = {
        "HOAT_DONG": "Hoạt động",
        "TAM_KHOA": "Tạm khóa",
        "NGUNG_THEO_DOI": "Ngừng theo dõi",
    }
    return mapping.get(value, value or "-")


def service_status_label(value):
    mapping = {
        "CHUA_KICH_HOAT": "Chưa kích hoạt",
        "DANG_HIEU_LUC": "Đang hiệu lực",
        "SAP_HET_HAN": "Sắp hết hạn",
        "HET_HAN": "Hết hạn",
        "TAM_DUNG": "Tạm dừng",
        "DA_HUY": "Đã hủy",
    }
    return mapping.get(value, value or "-")


def payment_method_label(value):
    mapping = {
        "TIEN_MAT": "Tiền mặt",
        "CHUYEN_KHOAN": "Chuyển khoản",
        "THE": "Thẻ",
        "KHAC": "Khác",
    }
    return mapping.get(value, value or "-")


def schedule_status_label(value):
    mapping = {
        "DA_LEN_LICH": "Đã lên lịch",
        "HOAN_THANH": "Hoàn thành",
        "HUY": "Hủy",

        # Giá trị cũ nếu database còn dữ liệu cũ
        "HOAN": "Hủy",
        "VANG_MAT": "Hủy",
    }
    return mapping.get(value, value or "-")


def equipment_status_label(value):
    mapping = {
        "TOT": "Đang sử dụng",
        "CAN_BAO_TRI": "Cần bảo trì",
        "DANG_BAO_TRI": "Đang bảo trì",
        "NGUNG_SU_DUNG": "Ngừng sử dụng",

        # Giá trị cũ nếu database còn dữ liệu cũ
        "HONG": "Ngừng sử dụng",
    }
    return mapping.get(value, value or "-")


def checkin_type_label(value):
    mapping = {
        "TU_DO": "Tự do",
        "THEO_LICH_PT": "Theo lịch PT",
    }
    return mapping.get(value, value or "-")


def checkin_status_label(value):
    mapping = {
        "DANG_CHECKIN": "Đang trong phòng",
        "DA_CHECKOUT": "Đã check-out",
        "HUY": "Hủy",
    }
    return mapping.get(value, value or "-")


def build_member_report(filters):
    summary_raw = get_member_registrations_by_day(filters["start_date"], filters["end_date"])
    detail_raw = get_member_registration_details(filters["start_date"], filters["end_date"])

    summary_rows = []
    chart_labels = []
    chart_values = []

    for row in summary_raw:
        label = format_date(row.get("ngay"))
        value = int(row.get("so_luong") or 0)

        chart_labels.append(label)
        chart_values.append(value)

        summary_rows.append({
            "label": label,
            "value": value,
        })

    detail_rows = []
    for row in detail_raw:
        detail_rows.append({
            "ma": f"CUS{row.get('ma_hoi_vien'):06d}",
            "ho_ten": row.get("ho_ten"),
            "so_dien_thoai": row.get("so_dien_thoai"),
            "email": row.get("email") or "-",
            "ngay": format_date(row.get("ngay_tham_gia")),
            "goi": row.get("ten_goi_tap") or "-",
            "trang_thai": member_status_label(row.get("trang_thai")),
            "trang_thai_phu": service_status_label(row.get("trang_thai_hieu_luc")),
        })

    return {
        "title": "Số lượng hội viên đăng ký theo ngày",
        "total_label": "Số lượng hội viên mới",
        "total_value": sum(chart_values),
        "chart_label": "Hội viên mới",
        "chart_labels": chart_labels,
        "chart_values": chart_values,
        "summary_headers": ["Ngày", "Đăng ký mới"],
        "summary_rows": summary_rows,
        "detail_headers": ["Mã HV", "Hội viên", "SĐT", "Email", "Ngày tham gia", "Gói đang dùng", "Trạng thái HV", "Trạng thái dịch vụ"],
        "detail_rows": detail_rows,
    }


def build_revenue_report(filters):
    summary_raw = get_revenue_by_day(filters["start_date"], filters["end_date"])
    detail_raw = get_revenue_details(filters["start_date"], filters["end_date"])

    summary_rows = []
    chart_labels = []
    chart_values = []

    for row in summary_raw:
        label = format_date(row.get("ngay"))
        value = float(row.get("so_tien") or 0)

        chart_labels.append(label)
        chart_values.append(value)

        summary_rows.append({
            "label": label,
            "value": format_money(value),
        })

    detail_rows = []
    for row in detail_raw:
        detail_rows.append({
            "ma": f"TT{row.get('ma_thanh_toan'):06d}",
            "ho_ten": row.get("ho_ten"),
            "so_dien_thoai": row.get("so_dien_thoai"),
            "ngay": format_datetime(row.get("ngay_thanh_toan")),
            "goi": row.get("ten_goi_tap"),
            "so_tien": format_money(row.get("so_tien")),
            "hinh_thuc": payment_method_label(row.get("hinh_thuc_thanh_toan")),
            "ghi_chu": row.get("ghi_chu") or "-",
        })

    return {
        "title": "Doanh thu theo ngày",
        "total_label": "Tổng doanh thu",
        "total_value": format_money(sum(chart_values)),
        "chart_label": "Doanh thu",
        "chart_labels": chart_labels,
        "chart_values": chart_values,
        "summary_headers": ["Ngày", "Doanh thu"],
        "summary_rows": summary_rows,
        "detail_headers": ["Mã TT", "Hội viên", "SĐT", "Thời gian", "Gói tập", "Số tiền", "Hình thức", "Ghi chú"],
        "detail_rows": detail_rows,
    }


def build_checkin_report(filters):
    summary_raw = get_checkin_by_day(filters["start_date"], filters["end_date"])
    detail_raw = get_checkin_details(filters["start_date"], filters["end_date"])

    summary_rows = []
    chart_labels = []
    chart_values = []

    for row in summary_raw:
        label = format_date(row.get("ngay"))
        total = int(row.get("tong_luot_checkin") or 0)
        checked_out = int(row.get("da_checkout") or 0)
        in_room = int(row.get("dang_trong_phong") or 0)

        chart_labels.append(label)
        chart_values.append(total)

        summary_rows.append({
            "label": label,
            "value": total,
        })

    detail_rows = []
    for row in detail_raw:
        detail_rows.append({
            "ma": f"CI{row.get('ma_check'):06d}",
            "hoi_vien": row.get("ho_ten"),
            "sdt": row.get("so_dien_thoai"),
            "goi": row.get("ten_goi_tap"),
            "gio_vao": format_datetime(row.get("thoi_gian_check_in")),
            "gio_ra": format_datetime(row.get("thoi_gian_check_out")),
            "loai": checkin_type_label(row.get("loai_checkin")),
            "trang_thai": checkin_status_label(row.get("trang_thai")),
            "ghi_chu": row.get("ghi_chu") or "-",
        })

    return {
        "title": "Lượt check-in theo ngày",
        "total_label": "Tổng lượt check-in",
        "total_value": sum(chart_values),
        "chart_label": "Lượt check-in",
        "chart_labels": chart_labels,
        "chart_values": chart_values,
        "summary_headers": ["Ngày", "Lượt check-in"],
        "summary_rows": summary_rows,
        "detail_headers": ["Mã check", "Hội viên", "SĐT", "Gói sử dụng", "Giờ vào", "Giờ ra", "Loại check-in", "Trạng thái", "Ghi chú"],
        "detail_rows": detail_rows,
    }


def build_schedule_report(filters):
    summary_raw = get_schedules_by_status(filters["start_date"], filters["end_date"])
    detail_raw = get_schedule_details(filters["start_date"], filters["end_date"])

    grouped_summary = {}

    for row in summary_raw:
        label = schedule_status_label(row.get("trang_thai"))
        value = int(row.get("so_luong") or 0)

        grouped_summary[label] = grouped_summary.get(label, 0) + value

    summary_rows = []
    chart_labels = []
    chart_values = []

    for label, value in grouped_summary.items():
        chart_labels.append(label)
        chart_values.append(value)

        summary_rows.append({
            "label": label,
            "value": value,
        })

    detail_rows = []
    for row in detail_raw:
        detail_rows.append({
            "ma": f"LT{row.get('ma_lich_tap'):06d}",
            "ngay": format_date(row.get("ngay_tap")),
            "thoi_gian": f"{format_time(row.get('gio_bat_dau'))} - {format_time(row.get('gio_ket_thuc'))}",
            "hoi_vien": row.get("ten_hoi_vien"),
            "sdt": row.get("so_dien_thoai"),
            "pt": row.get("ten_pt"),
            "goi": row.get("ten_goi_tap"),
            "trang_thai": schedule_status_label(row.get("trang_thai_buoi_tap")),
            "ghi_chu": row.get("ghi_chu") or "-",
        })

    return {
        "title": "Lịch tập PT theo trạng thái",
        "total_label": "Tổng số buổi tập",
        "total_value": sum(chart_values),
        "chart_label": "Số buổi",
        "chart_labels": chart_labels,
        "chart_values": chart_values,
        "summary_headers": ["Trạng thái", "Số buổi"],
        "summary_rows": summary_rows,
        "detail_headers": ["Mã lịch", "Ngày tập", "Thời gian", "Hội viên", "SĐT", "PT", "Gói tập", "Trạng thái", "Ghi chú"],
        "detail_rows": detail_rows,
    }


def build_equipment_report(filters):
    summary_raw = get_equipment_by_status()
    detail_raw = get_equipment_details()

    summary_rows = []
    chart_labels = []
    chart_values = []

    for row in summary_raw:
        label = equipment_status_label(row.get("trang_thai"))
        value = int(row.get("so_luong") or 0)

        chart_labels.append(label)
        chart_values.append(value)

        summary_rows.append({
            "label": label,
            "value": value,
        })

    detail_rows = []
    for row in detail_raw:
        detail_rows.append({
            "ma": f"TB{row.get('ma_thiet_bi'):06d}",
            "ten": row.get("ten_thiet_bi"),
            "loai": row.get("loai_thiet_bi"),
            "vi_tri": row.get("vi_tri") or "-",
            "ngay_mua": format_date(row.get("ngay_mua")),
            "tinh_trang": equipment_status_label(row.get("tinh_trang")),
            "ghi_chu": row.get("ghi_chu") or "-",
        })

    return {
        "title": "Thiết bị theo tình trạng",
        "total_label": "Tổng số thiết bị",
        "total_value": sum(chart_values),
        "chart_label": "Số thiết bị",
        "chart_labels": chart_labels,
        "chart_values": chart_values,
        "summary_headers": ["Tình trạng", "Số thiết bị"],
        "summary_rows": summary_rows,
        "detail_headers": ["Mã TB", "Thiết bị", "Loại", "Vị trí", "Ngày mua", "Tình trạng", "Ghi chú"],
        "detail_rows": detail_rows,
    }


def normalize_filters(args):
    default_start, _ = get_default_date_range()
    today = date.today().isoformat()

    data_type = (args.get("data_type") or "members").strip()
    if data_type not in VALID_REPORT_TYPES:
        data_type = "members"

    start_date = normalize_date_value(args.get("start_date"), default_start)
    end_date = normalize_date_value(args.get("end_date"), today)

    if start_date > today:
        start_date = today

    if end_date > today:
        end_date = today

    if start_date > end_date:
        end_date = start_date

        if end_date > today:
            end_date = today
            start_date = today

    return {
        "data_type": data_type,
        "start_date": start_date,
        "end_date": end_date,
    }


def build_report_page(args):
    filters = normalize_filters(args)

    if filters["data_type"] == "revenue":
        report = build_revenue_report(filters)
    elif filters["data_type"] == "checkin":
        report = build_checkin_report(filters)
    elif filters["data_type"] == "schedules":
        report = build_schedule_report(filters)
    elif filters["data_type"] == "equipment":
        report = build_equipment_report(filters)
    else:
        report = build_member_report(filters)

    return {
        "filters": filters,
        "data_types": REPORT_DATA_TYPES,
        "report": report,
        "today": date.today().isoformat(),
    }


def export_report_csv(args):
    context = build_report_page(args)
    report = context["report"]

    output = io.StringIO()
    output.write("\ufeff")
    writer = csv.writer(output)

    writer.writerow([report["title"]])
    writer.writerow([report["total_label"], report["total_value"]])
    writer.writerow([])

    writer.writerow(["Bảng tổng hợp"])
    writer.writerow(report["summary_headers"])
    for row in report["summary_rows"]:
        writer.writerow(list(row.values()))

    writer.writerow([])
    writer.writerow(["Bảng chi tiết"])
    writer.writerow(report["detail_headers"])

    for row in report["detail_rows"]:
        writer.writerow(list(row.values()))

    return output.getvalue()