from functools import wraps
from flask import redirect, url_for, flash, session
from app.models.UserModel import UserModel


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not UserModel.is_logged_in():
            flash("Debes iniciar sesión para acceder.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not UserModel.is_logged_in():
            flash("Debes iniciar sesión.", "warning")
            return redirect(url_for("auth.login"))
        if not UserModel.is_admin():
            flash("No tienes permisos para acceder a esta sección.", "danger")
            return redirect(url_for("admin.dashboard"))
        return f(*args, **kwargs)
    return decorated