from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort

from app.services.checkin_service import (
    build_checkin_index,
    build_member_checkin_form,
    perform_checkin,
    perform_checkout,
)

checkin_bp = Blueprint("checkin", __name__, url_prefix="/checkin")


@checkin_bp.route("/", methods=["GET"])
def index():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    keyword = request.args.get("keyword", "")

    context = build_checkin_index(keyword)

    return render_template(
        "checkin/index.html",
        context=context
    )


@checkin_bp.route("/member/<int:member_id>", methods=["GET", "POST"])
def member_checkin(member_id):
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    context = build_member_checkin_form(member_id)

    if not context:
        abort(404)

    if request.method == "POST":
        try:
            perform_checkin(
                member_id=member_id,
                form_data=request.form
            )

            flash("Check-in hội viên thành công.", "success")
            return redirect(url_for("checkin.index"))

        except ValueError as error:
            flash(str(error), "error")

    return render_template(
        "checkin/member_checkin.html",
        context=context
    )


@checkin_bp.route("/checkout/<int:check_id>", methods=["POST"])
def checkout(check_id):
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    try:
        perform_checkout(
            check_id=check_id,
            form_data=request.form
        )

        flash("Check-out hội viên thành công.", "success")

    except ValueError as error:
        flash(str(error), "error")

    return redirect(url_for("checkin.index"))