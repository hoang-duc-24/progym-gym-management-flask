from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort

from app.services.accounts_service import (
    build_accounts_index,
    build_account_form,
    create_account,
    edit_account,
    lock_account,
    unlock_account,
    reset_password,
)


accounts_bp = Blueprint("accounts", __name__, url_prefix="/accounts")


@accounts_bp.route("/", methods=["GET"])
def index():
    filters = {
        "keyword": request.args.get("keyword", "").strip(),
        "role": request.args.get("role", "").strip(),
        "status": request.args.get("status", "").strip(),
    }

    page_data = build_accounts_index(
        filters=filters,
        current_account_id=session.get("user_id")
    )

    return render_template(
        "accounts/index.html",
        page_data=page_data,
        form_context=build_account_form()
    )


@accounts_bp.route("/create", methods=["GET", "POST"])
def create():
    form_context = build_account_form()

    if request.method == "POST":
        try:
            create_account(request.form)

            flash("Tạo tài khoản thành công.", "success")
            return redirect(url_for("accounts.index"))

        except ValueError as error:
            flash(str(error), "error")
            return redirect(url_for("accounts.index"))

    return render_template(
        "accounts/create.html",
        form_context=form_context
    )


@accounts_bp.route("/<int:account_id>/edit", methods=["GET", "POST"])
def edit(account_id):
    form_context = build_account_form(account_id)

    if not form_context:
        abort(404)

    if request.method == "POST":
        try:
            edit_account(account_id, request.form)

            flash("Cập nhật tài khoản thành công.", "success")
            return redirect(url_for("accounts.index"))

        except ValueError as error:
            flash(str(error), "error")
            return redirect(url_for("accounts.index"))

    return render_template(
        "accounts/edit.html",
        form_context=form_context
    )


@accounts_bp.route("/<int:account_id>/lock", methods=["POST"])
def lock(account_id):
    try:
        lock_account(
            account_id=account_id,
            current_account_id=session.get("user_id")
        )

        flash("Khóa tài khoản thành công.", "success")

    except ValueError as error:
        flash(str(error), "error")

    return redirect(url_for("accounts.index"))


@accounts_bp.route("/<int:account_id>/unlock", methods=["POST"])
def unlock(account_id):
    try:
        unlock_account(account_id)

        flash("Mở khóa tài khoản thành công.", "success")

    except ValueError as error:
        flash(str(error), "error")

    return redirect(url_for("accounts.index"))


@accounts_bp.route("/<int:account_id>/reset-password", methods=["GET", "POST"])
def reset_password_view(account_id):
    form_context = build_account_form(account_id)

    if not form_context:
        abort(404)

    if request.method == "POST":
        try:
            reset_password(account_id, request.form)

            flash("Đặt lại mật khẩu thành công.", "success")
            return redirect(url_for("accounts.index"))

        except ValueError as error:
            flash(str(error), "error")
            return redirect(url_for("accounts.index"))

    return render_template(
        "accounts/reset_password.html",
        form_context=form_context
    )