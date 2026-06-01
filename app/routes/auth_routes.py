from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.db import fetch_one, execute
from app.utils.permissions import get_default_page_for_role

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/", methods=["GET"])
def root():
    if session.get("user_id"):
        default_endpoint = get_default_page_for_role(session.get("role"))
        return redirect(url_for(default_endpoint))

    return redirect(url_for("auth.login"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            flash("Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.", "error")
            return render_template("auth/login.html")

        sql = """
            SELECT 
                tk.ma_tai_khoan,
                tk.ten_dang_nhap,
                tk.mat_khau,
                tk.ho_ten,
                tk.trang_thai,
                vt.ten_vai_tro
            FROM TaiKhoan tk
            JOIN VaiTro vt ON tk.ma_vai_tro = vt.ma_vai_tro
            WHERE tk.ten_dang_nhap = %s
            LIMIT 1
        """
        user = fetch_one(sql, (username,))

        if not user:
            flash("Tên đăng nhập không tồn tại.", "error")
            return render_template("auth/login.html")

        if user["trang_thai"] != "HOAT_DONG":
            flash("Tài khoản đang bị khóa hoặc không còn hoạt động.", "error")
            return render_template("auth/login.html")

        if user["mat_khau"] != password:
            flash("Mật khẩu không chính xác.", "error")
            return render_template("auth/login.html")

        execute(
            """
            UPDATE TaiKhoan
            SET lan_dang_nhap_cuoi = NOW()
            WHERE ma_tai_khoan = %s
            """,
            (user["ma_tai_khoan"],)
        )

        session["user_id"] = user["ma_tai_khoan"]
        session["username"] = user["ten_dang_nhap"]
        session["full_name"] = user["ho_ten"]
        session["role"] = user["ten_vai_tro"]

        default_endpoint = get_default_page_for_role(user["ten_vai_tro"])
        return redirect(url_for(default_endpoint))

    return render_template("auth/login.html")

@auth_bp.route("/change-password", methods=["POST"])
def change_password():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    current_password = request.form.get("current_password", "").strip()
    new_password = request.form.get("new_password", "").strip()
    confirm_password = request.form.get("confirm_password", "").strip()

    if not current_password or not new_password or not confirm_password:
        flash("Vui lòng nhập đầy đủ thông tin đổi mật khẩu.", "error")
        return redirect(request.referrer or url_for(get_default_page_for_role(session.get("role"))))

    if len(new_password) < 6:
        flash("Mật khẩu mới phải có tối thiểu 6 ký tự.", "error")
        return redirect(request.referrer or url_for(get_default_page_for_role(session.get("role"))))

    if new_password != confirm_password:
        flash("Mật khẩu xác nhận không khớp.", "error")
        return redirect(request.referrer or url_for(get_default_page_for_role(session.get("role"))))

    user = fetch_one(
        """
        SELECT ma_tai_khoan, mat_khau
        FROM TaiKhoan
        WHERE ma_tai_khoan = %s
        LIMIT 1
        """,
        (session.get("user_id"),)
    )

    if not user:
        session.clear()
        flash("Phiên đăng nhập không còn hợp lệ. Vui lòng đăng nhập lại.", "error")
        return redirect(url_for("auth.login"))

    if user["mat_khau"] != current_password:
        flash("Mật khẩu hiện tại không chính xác.", "error")
        return redirect(request.referrer or url_for(get_default_page_for_role(session.get("role"))))

    if new_password == current_password:
        flash("Mật khẩu mới không được trùng với mật khẩu hiện tại.", "error")
        return redirect(request.referrer or url_for(get_default_page_for_role(session.get("role"))))

    execute(
        """
        UPDATE TaiKhoan
        SET mat_khau = %s
        WHERE ma_tai_khoan = %s
        """,
        (new_password, session.get("user_id"))
    )

    flash("Đổi mật khẩu thành công. Vui lòng sử dụng mật khẩu mới ở lần đăng nhập tiếp theo.", "success")
    return redirect(request.referrer or url_for(get_default_page_for_role(session.get("role"))))


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))