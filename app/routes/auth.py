from flask import (
    Blueprint, render_template, redirect,
    url_for, request, flash, session
)
from app.models.UserModel import UserModel
from app.services.email_service import send_reset_email

auth_bp = Blueprint("auth", __name__)


# ── Login ───────────────────────────────────────────────────────────────────

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if UserModel.is_logged_in():
        return redirect(url_for("admin.dashboard"))

    error = None

    if request.method == "POST":
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        user = UserModel.login(email, password)

        if user:
            flash(f"Bienvenido, {user.fullname}.", "success")
            return redirect(url_for("admin.dashboard"))
        else:
            error = "Correo o contraseña incorrectos."

    return render_template("auth/login.html", error=error)


# ── Logout ──────────────────────────────────────────────────────────────────

@auth_bp.route("/logout")
def logout():
    UserModel.logout()
    flash("Sesión cerrada correctamente.", "success")
    return redirect(url_for("auth.login"))


# ── Solicitar reset ─────────────────────────────────────────────────────────

@auth_bp.route("/reset", methods=["GET", "POST"])
def request_reset():
    message = None

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        user, token = UserModel.request_password_reset(email)

        if user and token:
            reset_url = url_for("auth.do_reset", token=token, _external=True)
            enviado = send_reset_email(
                to=user.email,
                fullname=user.fullname,
                reset_url=reset_url
            )
            if not enviado:
                print(f"[DEV] Falló el email. Enlace manual:\n{reset_url}")

        # Siempre el mismo mensaje por seguridad
        message = "Si el correo existe, recibirás un enlace para restablecer tu contraseña."

    return render_template("auth/request_reset.html", message=message)


# ── Ejecutar reset ──────────────────────────────────────────────────────────

@auth_bp.route("/reset/<token>", methods=["GET", "POST"])
def do_reset(token):
    error = None

    if request.method == "POST":
        pwd1 = request.form.get("password", "")
        pwd2 = request.form.get("password_confirm", "")

        if pwd1 != pwd2:
            error = "Las contraseñas no coinciden."
        elif len(pwd1) < 8:
            error = "La contraseña debe tener al menos 8 caracteres."
        else:
            ok = UserModel.reset_password(token, pwd1)
            if ok:
                flash("Contraseña actualizada. Inicia sesión.", "success")
                return redirect(url_for("auth.login"))
            else:
                error = "El enlace es inválido o ya expiró."

    return render_template("auth/do_reset.html", token=token, error=error)