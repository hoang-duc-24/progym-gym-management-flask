from flask import Blueprint, render_template, request, redirect, url_for, session

from app.services.payment_reports_service import build_payment_report_index


payment_reports_bp = Blueprint(
    "payment_reports",
    __name__,
    url_prefix="/payment-reports"
)


@payment_reports_bp.route("/", methods=["GET"])
def index():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    filters = {
        "date_from": request.args.get("date_from", "").strip(),
        "date_to": request.args.get("date_to", "").strip(),
        "hinh_thuc_thanh_toan": request.args.get("hinh_thuc_thanh_toan", "").strip(),
        "trang_thai_thanh_toan": request.args.get("trang_thai_thanh_toan", "").strip(),
        "keyword": request.args.get("keyword", "").strip(),
    }

    context = build_payment_report_index(filters)

    return render_template(
        "payment_reports/index.html",
        context=context
    )