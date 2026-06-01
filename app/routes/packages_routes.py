from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort, jsonify

from app.services.packages_service import (
    build_packages_index,
    build_package_form,
    create_package,
    edit_package,
    stop_package,
    activate_package,
)


packages_bp = Blueprint("packages", __name__, url_prefix="/packages")


@packages_bp.route("/", methods=["GET"])
def index():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    filters = {
        "keyword": request.args.get("keyword", "").strip(),
        "loai_goi": request.args.get("loai_goi", "").strip(),
        "trang_thai_ap_dung": request.args.get("trang_thai_ap_dung", "").strip(),
    }

    context = build_packages_index(filters)

    return render_template(
        "packages/index.html",
        context=context
    )


@packages_bp.route("/create", methods=["GET", "POST"])
def create():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    form_context = build_package_form()

    if request.method == "POST":
        try:
            create_package(request.form)
            flash("Tạo gói tập thành công.", "success")
            return redirect(url_for("packages.index"))

        except ValueError as error:
            flash(str(error), "error")

    return render_template(
        "packages/form.html",
        form_context=form_context,
        mode="create"
    )


@packages_bp.route("/<int:package_id>/edit", methods=["GET", "POST"])
def edit(package_id):
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    next_url = request.args.get("next") or request.form.get("next")

    if next_url and not next_url.startswith("/packages"):
        next_url = None

    form_context = build_package_form(package_id)

    if not form_context:
        abort(404)

    if request.method == "POST":
        try:
            edit_package(package_id, request.form)
            flash("Cập nhật gói tập thành công.", "success")

            if next_url:
                return redirect(next_url)

            return redirect(url_for("packages.index"))

        except ValueError as error:
            flash(str(error), "error")

            if next_url:
                return redirect(next_url)

    return render_template(
        "packages/form.html",
        form_context=form_context,
        mode="edit"
    )

@packages_bp.route("/<int:package_id>/edit-data")
def edit_data(package_id):
    if not session.get("user_id"):
        return jsonify({
            "success": False,
            "message": "Phiên đăng nhập đã hết hạn."
        }), 401

    form_context = build_package_form(package_id)

    if not form_context:
        return jsonify({
            "success": False,
            "message": "Không tìm thấy gói tập."
        }), 404

    package = form_context["package"]

    return jsonify({
        "success": True,
        "package": {
            "ma_goi_tap": package.get("ma_goi_tap"),
            "ma_goi_hien_thi": f"GT{package.get('ma_goi_tap'):06d}",
            "ten_goi_tap": package.get("ten_goi_tap") or "",
            "loai_goi": package.get("loai_goi") or "KHONG_PT",
            "gia_goi": int(package.get("gia_goi") or 0),
            "thoi_han_ngay": package.get("thoi_han_ngay") or "",
            "so_buoi_pt": package.get("so_buoi_pt") or 0,
            "mo_ta": package.get("mo_ta") or "",
            "registration_count": form_context["registration_count"],
            "has_registrations": form_context["has_registrations"],
        }
    })


@packages_bp.route("/<int:package_id>/stop", methods=["POST"])
def stop(package_id):
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    try:
        stop_package(package_id)
        flash("Đã ngừng áp dụng gói tập.", "success")

    except ValueError as error:
        flash(str(error), "error")

    return redirect(url_for("packages.index"))


@packages_bp.route("/<int:package_id>/activate", methods=["POST"])
def activate(package_id):
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    try:
        activate_package(package_id)
        flash("Đã áp dụng lại gói tập.", "success")

    except ValueError as error:
        flash(str(error), "error")

    return redirect(url_for("packages.index"))