from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort

from app.services.pts_service import (
    build_pts_index,
    build_pt_form_context,
    build_pt_detail,
    create_pt,
    update_pt_info,
    get_pt_future_schedule_warning,
)


pts_bp = Blueprint("pts", __name__, url_prefix="/pts")


@pts_bp.route("/", methods=["GET"])
def index():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    filters = {
        "trang_thai_lam_viec": request.args.get("trang_thai_lam_viec", "").strip(),
        "keyword": request.args.get("keyword", "").strip(),
    }

    context = build_pts_index(filters)

    return render_template(
        "pts/index.html",
        context=context
    )


@pts_bp.route("/create", methods=["GET", "POST"])
def create():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    context = build_pt_form_context()

    if request.method == "POST":
        try:
            pt_id = create_pt(request.form)
            flash("Thêm huấn luyện viên thành công.", "success")
            return redirect(url_for("pts.index"))

        except ValueError as error:
            flash(str(error), "error")
            return redirect(url_for("pts.index"))
        
    return render_template(
        "pts/create.html",
        context=context
    )


@pts_bp.route("/<int:pt_id>", methods=["GET"])
def detail(pt_id):
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    context = build_pt_detail(pt_id)

    if not context:
        abort(404)

    return render_template(
        "pts/detail.html",
        context=context
    )


@pts_bp.route("/<int:pt_id>/edit", methods=["GET", "POST"])
def edit(pt_id):
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    context = build_pt_form_context(pt_id)

    if not context:
        abort(404)

    if request.method == "POST":
        try:
            warning = get_pt_future_schedule_warning(
                pt_id,
                request.form.get("trang_thai_lam_viec")
            )

            update_pt_info(pt_id, request.form)

            flash("Cập nhật thông tin huấn luyện viên thành công.", "success")

            if warning:
                flash(warning, "warning")

            next_url = request.form.get("next") or url_for("pts.detail", pt_id=pt_id)
            return redirect(next_url)

        except ValueError as error:
            flash(str(error), "error")
            next_url = request.form.get("next") or url_for("pts.detail", pt_id=pt_id)
            return redirect(next_url)

    return render_template(
        "pts/edit.html",
        context=context
    )