from flask import Blueprint, render_template, request, redirect, url_for, session, abort

from app.services.service_status_service import sync_registration_service_statuses

from app.services.registrations_service import (
    build_registrations_index,
    build_registration_detail,
    build_registration_create_context,
)


registrations_bp = Blueprint("registrations", __name__, url_prefix="/registrations")


@registrations_bp.route("/", methods=["GET"])
def index():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))
    
    sync_registration_service_statuses()

    filters = {
        "keyword": request.args.get("keyword", "").strip(),
        "loai_goi": request.args.get("loai_goi", "").strip(),
        "trang_thai_thanh_toan": request.args.get("trang_thai_thanh_toan", "").strip(),
        "trang_thai_hieu_luc": request.args.get("trang_thai_hieu_luc", "").strip(),
        "start_date": request.args.get("start_date", "").strip(),
        "end_date": request.args.get("end_date", "").strip(),
        "near_expiry": request.args.get("near_expiry", "").strip(),
    }

    context = build_registrations_index(filters)

    return render_template(
        "registrations/index.html",
        context=context
    )

@registrations_bp.route("/create", methods=["GET"])
def create():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    keyword = request.args.get("keyword", "").strip()
    context = build_registration_create_context(keyword)

    return render_template(
        "registrations/create.html",
        context=context
    )


@registrations_bp.route("/<int:registration_id>", methods=["GET"])
def detail(registration_id):
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))
    
    sync_registration_service_statuses()

    context = build_registration_detail(registration_id)

    if not context:
        abort(404)

    return render_template(
        "registrations/detail.html",
        context=context
    )