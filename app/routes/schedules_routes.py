from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort

from app.services.schedules_service import (
    build_schedules_index,
    build_schedule_create_assignment_index,
)

from app.services.members_service import (
    build_create_schedule_form,
    create_training_schedule_from_assignment,
    build_update_schedule_form,
    update_training_schedule_status,
)


schedules_bp = Blueprint("schedules", __name__, url_prefix="/schedules")


@schedules_bp.route("/", methods=["GET"])
def index():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    filters = {
        "ngay_tap": request.args.get("ngay_tap", "").strip(),
        "ma_pt": request.args.get("ma_pt", "").strip(),
        "trang_thai_buoi_tap": request.args.get("trang_thai_buoi_tap", "").strip(),
        "keyword": request.args.get("keyword", "").strip(),
    }

    context = build_schedules_index(
        filters=filters,
        current_role=session.get("role"),
        current_user_id=session.get("user_id")
    )

    return render_template("schedules/index.html", context=context)


@schedules_bp.route("/create", methods=["GET"])
def create():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    filters = {
        "ma_pt": request.args.get("ma_pt", "").strip(),
        "trang_thai_hieu_luc": request.args.get("trang_thai_hieu_luc", "").strip(),
        "keyword": request.args.get("keyword", "").strip(),
    }

    context = build_schedule_create_assignment_index(filters)

    return render_template("schedules/create_from_assignment.html", context=context)


@schedules_bp.route("/assignments/<int:assignment_id>/create", methods=["GET", "POST"])
def create_from_assignment(assignment_id):
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    next_url = request.args.get("next") or request.form.get("next")

    try:
        form_context = build_create_schedule_form(assignment_id)
    except ValueError as error:
        flash(str(error), "error")
        return redirect(next_url or url_for("schedules.index"))

    if not form_context:
        abort(404)

    if request.method == "POST":
        try:
            create_training_schedule_from_assignment(
                assignment_id=assignment_id,
                form_data=request.form
            )

            flash("Tạo lịch tập PT thành công.", "success")
            return redirect(next_url or url_for("schedules.index"))

        except ValueError as error:
            flash(str(error), "error")

    return render_template(
        "schedules/create_schedule.html",
        form_context=form_context,
        next_url=next_url or url_for("schedules.index")
    )


@schedules_bp.route("/<int:schedule_id>/update-status", methods=["GET", "POST"])
def update_status(schedule_id):
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    next_url = request.args.get("next") or request.form.get("next")

    try:
        form_context = build_update_schedule_form(
            schedule_id=schedule_id,
            current_user_id=session.get("user_id"),
            current_role=session.get("role")
        )
    except ValueError as error:
        flash(str(error), "error")
        return redirect(next_url or url_for("schedules.index"))

    if not form_context:
        abort(404)

    if request.method == "POST":
        try:
            update_training_schedule_status(
                schedule_id=schedule_id,
                form_data=request.form,
                current_user_id=session.get("user_id"),
                current_role=session.get("role")
            )

            flash("Cập nhật trạng thái buổi tập thành công.", "success")
            return redirect(next_url or url_for("schedules.index"))

        except ValueError as error:
            flash(str(error), "error")

    return render_template(
        "schedules/update_schedule_status.html",
        form_context=form_context,
        next_url=next_url or url_for("schedules.index")
    )