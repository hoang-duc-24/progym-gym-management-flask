from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort

from app.services.payments_service import (
    build_payment_form_data,
    record_payment,
)

payments_bp = Blueprint("payments", __name__, url_prefix="/payments")


@payments_bp.route("/create/<int:registration_id>", methods=["GET", "POST"])
def create(registration_id):
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    payment_data = build_payment_form_data(registration_id)

    if not payment_data:
        abort(404)

    if request.method == "POST":
        try:
            member_id = record_payment(
                registration_id=registration_id,
                account_id=session.get("user_id"),
                form_data=request.form
            )

            flash("Ghi nhận thanh toán thành công.", "success")
            return redirect(url_for("members.detail", member_id=member_id))

        except ValueError as error:
            flash(str(error), "error")

    return render_template(
        "payments/create.html",
        payment=payment_data
    )