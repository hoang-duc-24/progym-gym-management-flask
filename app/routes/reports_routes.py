from flask import Blueprint, render_template, redirect, url_for, session, request, Response

from app.services.reports_service import build_report_page, export_report_csv


reports_bp = Blueprint("reports", __name__, url_prefix="/reports")


@reports_bp.route("/", methods=["GET"])
def index():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    context = build_report_page(request.args)

    return render_template(
        "reports/index.html",
        context=context
    )


@reports_bp.route("/export", methods=["GET"])
def export():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    csv_content = export_report_csv(request.args)

    return Response(
        csv_content,
        mimetype="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": "attachment; filename=progym_report.csv"
        }
    )