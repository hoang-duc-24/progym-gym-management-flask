from flask import Blueprint, render_template, session, redirect, url_for, abort, request, flash, jsonify
from app.services.members_service import (
    build_member_rows,
    build_member_detail,
    build_member_create_form,
    create_member_with_registration,
    build_register_package_form,
    register_package_for_existing_member,
    build_assign_pt_form,
    assign_pt_to_registration,
    build_create_schedule_form,
    create_training_schedule_from_assignment,
    build_update_schedule_form,
    update_training_schedule_status,
    build_member_edit_form,
    update_member_info,
)

members_bp = Blueprint("members", __name__, url_prefix="/members")


@members_bp.route("/")
def index():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    filters = {
        "keyword": request.args.get("keyword", "").strip(),
        "payment_status": request.args.get("payment_status", "").strip(),
        "member_status": request.args.get("member_status", "").strip(),
        "package_type": request.args.get("package_type", "").strip(),
        "service_status": request.args.get("service_status", "").strip(),
        "expire_days": request.args.get("expire_days", "3").strip(),
    }

    try:
        page = int(request.args.get("page", 1))
    except ValueError:
        page = 1

    try:
        per_page = int(request.args.get("per_page", 10))
    except ValueError:
        per_page = 10

    if page < 1:
        page = 1

    if per_page not in [10, 50, 100]:
        per_page = 10

    result = build_member_rows(
        filters=filters,
        page=page,
        per_page=per_page
    )

    return render_template(
        "members/index.html",
        members=result["rows"],
        filters=filters,
        pagination=result["pagination"]
    )


@members_bp.route("/<int:member_id>")
def detail(member_id):
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    detail_data = build_member_detail(member_id)

    if not detail_data:
        abort(404)

    return render_template(
        "members/detail.html",
        detail=detail_data
    )

@members_bp.route("/<int:member_id>/edit-data")
def edit_data(member_id):
    if not session.get("user_id"):
        return jsonify({
            "success": False,
            "message": "Phiên đăng nhập đã hết hạn."
        }), 401

    form_context = build_member_edit_form(member_id)

    if not form_context:
        return jsonify({
            "success": False,
            "message": "Không tìm thấy hội viên."
        }), 404

    return jsonify({
        "success": True,
        "member": form_context
    })


@members_bp.route("/<int:member_id>/edit", methods=["GET", "POST"])
def edit(member_id):
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    next_url = request.args.get("next") or request.form.get("next")

    if next_url and not next_url.startswith("/members"):
        next_url = None

    form_context = build_member_edit_form(member_id)

    if not form_context:
        abort(404)

    if request.method == "POST":
        try:
            update_member_info(
                member_id=member_id,
                form_data=request.form
            )

            flash("Cập nhật thông tin hội viên thành công.", "success")

            if next_url:
                return redirect(next_url)

            return redirect(url_for("members.detail", member_id=member_id))

        except ValueError as error:
            flash(str(error), "error")

            if next_url:
                return redirect(next_url)

            form_context = {
                **form_context,
                "ho_ten": request.form.get("ho_ten", ""),
                "ngay_sinh": request.form.get("ngay_sinh", ""),
                "gioi_tinh": request.form.get("gioi_tinh", "NAM"),
                "so_dien_thoai": request.form.get("so_dien_thoai", ""),
                "email": request.form.get("email", ""),
                "dia_chi": request.form.get("dia_chi", ""),
                "trang_thai": request.form.get("trang_thai", "HOAT_DONG"),
                "ghi_chu": request.form.get("ghi_chu", ""),
            }

    return render_template(
        "members/edit.html",
        form_context=form_context,
        next_url=next_url
    )

@members_bp.route("/create", methods=["GET", "POST"])
def create():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    form_context = build_member_create_form()

    if request.method == "POST":
        try:
            member_id = create_member_with_registration(
                form_data=request.form,
                account_id=session.get("user_id")
            )

            flash("Tạo hội viên và đăng ký gói thành công.", "success")
            return redirect(url_for("members.detail", member_id=member_id))

        except ValueError as error:
            flash(str(error), "error")

    return render_template(
        "members/create.html",
        form_context=form_context
    )

@members_bp.route("/<int:member_id>/register-package", methods=["GET", "POST"])
def register_package(member_id):
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    try:
        form_context = build_register_package_form(member_id)
    except ValueError as error:
        flash(str(error), "error")
        return redirect(url_for("members.detail", member_id=member_id))

    if not form_context:
        abort(404)

    if request.method == "POST":
        try:
            register_package_for_existing_member(
                member_id=member_id,
                form_data=request.form,
                account_id=session.get("user_id")
            )

            flash("Đăng ký thêm gói cho hội viên thành công.", "success")
            return redirect(url_for("members.detail", member_id=member_id))

        except ValueError as error:
            flash(str(error), "error")

    return render_template(
        "members/register_package.html",
        form_context=form_context
    )

@members_bp.route("/registrations/<int:registration_id>/assign-pt", methods=["GET", "POST"])
def assign_pt(registration_id):
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    try:
        form_context = build_assign_pt_form(registration_id)
    except ValueError as error:
        flash(str(error), "error")
        return redirect(url_for("members.index"))

    if not form_context:
        abort(404)

    member_id = form_context["registration"]["ma_hoi_vien"]

    if request.method == "POST":
        try:
            assign_pt_to_registration(
                registration_id=registration_id,
                form_data=request.form
            )

            flash("Phân công PT thành công.", "success")
            return redirect(url_for("members.detail", member_id=member_id))

        except ValueError as error:
            flash(str(error), "error")

    return render_template(
        "members/assign_pt.html",
        form_context=form_context
    )

@members_bp.route("/assignments/<int:assignment_id>/create-schedule", methods=["GET", "POST"])
def create_schedule(assignment_id):
    next_url = request.args.get("next") or request.form.get("next")
    return redirect(
        url_for(
            "schedules.create_from_assignment",
            assignment_id=assignment_id,
            next=next_url or url_for("members.index")
        )
    )

@members_bp.route("/schedules/<int:schedule_id>/update-status", methods=["GET", "POST"])
def update_schedule_status_view(schedule_id):
    next_url = request.args.get("next") or request.form.get("next")
    return redirect(
        url_for(
            "schedules.update_status",
            schedule_id=schedule_id,
            next=next_url or url_for("members.index")
        )
    )

