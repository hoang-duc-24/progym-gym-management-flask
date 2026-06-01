from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort

from app.services.equipment_service import (
    build_equipment_index,
    build_equipment_form_context,
    build_equipment_detail,
    build_maintenance_form_context,
    create_equipment,
    update_equipment_info,
    record_maintenance,
    build_resolve_maintenance_context,
    resolve_maintenance,
)


equipment_bp = Blueprint("equipment", __name__, url_prefix="/equipment")


@equipment_bp.route("/", methods=["GET"])
def index():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    filters = {
        "tinh_trang": request.args.get("tinh_trang", "").strip(),
        "loai_thiet_bi": request.args.get("loai_thiet_bi", "").strip(),
        "keyword": request.args.get("keyword", "").strip(),
    }

    context = build_equipment_index(filters)

    return render_template(
        "equipment/index.html",
        context=context
    )


@equipment_bp.route("/create", methods=["GET", "POST"])
def create():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    context = build_equipment_form_context()

    if request.method == "POST":
        try:
            equipment_id = create_equipment(
                form_data=request.form,
                image_file=request.files.get("hinh_anh")
            )

            flash("Thêm thiết bị thành công.", "success")
            return redirect(url_for("equipment.detail", equipment_id=equipment_id))

        except ValueError as error:
            flash(str(error), "error")

    return render_template(
        "equipment/create.html",
        context=context
    )


@equipment_bp.route("/<int:equipment_id>", methods=["GET"])
def detail(equipment_id):
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    context = build_equipment_detail(equipment_id)

    if not context:
        abort(404)

    return render_template(
        "equipment/detail.html",
        context=context
    )


@equipment_bp.route("/<int:equipment_id>/edit", methods=["GET", "POST"])
def edit(equipment_id):
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    context = build_equipment_form_context(equipment_id)

    if not context:
        abort(404)

    if request.method == "POST":
        try:
            update_equipment_info(
                equipment_id=equipment_id,
                form_data=request.form,
                image_file=request.files.get("hinh_anh")
            )

            flash("Cập nhật thiết bị thành công.", "success")
            return redirect(url_for("equipment.detail", equipment_id=equipment_id))

        except ValueError as error:
            flash(str(error), "error")

    return render_template(
        "equipment/edit.html",
        context=context
    )


@equipment_bp.route("/<int:equipment_id>/maintenance/create", methods=["GET", "POST"])
def create_maintenance(equipment_id):
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    context = build_maintenance_form_context(equipment_id)

    if not context:
        abort(404)

    if request.method == "POST":
        try:
            record_maintenance(equipment_id, request.form)
            flash("Ghi nhận bảo trì thiết bị thành công.", "success")
            return redirect(url_for("equipment.detail", equipment_id=equipment_id))

        except ValueError as error:
            flash(str(error), "error")

    return render_template(
        "equipment/create_maintenance.html",
        context=context
    )

@equipment_bp.route("/<int:equipment_id>/maintenance/<int:maintenance_id>/resolve", methods=["GET", "POST"])
def resolve_maintenance_view(equipment_id, maintenance_id):
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    try:
        context = build_resolve_maintenance_context(equipment_id, maintenance_id)
    except ValueError as error:
        flash(str(error), "error")
        return redirect(url_for("equipment.detail", equipment_id=equipment_id))

    if not context:
        abort(404)

    if request.method == "POST":
        try:
            resolve_maintenance(equipment_id, maintenance_id, request.form)
            flash("Cập nhật kết quả bảo trì thành công.", "success")
            return redirect(url_for("equipment.detail", equipment_id=equipment_id))

        except ValueError as error:
            flash(str(error), "error")

    return render_template(
        "equipment/resolve_maintenance.html",
        context=context
    )