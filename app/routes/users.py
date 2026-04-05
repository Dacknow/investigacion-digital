from flask import (
    Blueprint, render_template, redirect,
    url_for, request, flash, session
)
from app.models.UserModel import UserModel
from app.routes.decorators import admin_required

users_bp = Blueprint("users", __name__)

ROLES_DISPONIBLES = ["admin", "viewer"]


# ── Listar ──────────────────────────────────────────────────────────────────

@users_bp.route("/")
@admin_required
def show():
    users = UserModel.get_all_users()
    return render_template(
        "users/show.html",
        users=users,
        current_user_id=session.get("user_id"),
        roles=ROLES_DISPONIBLES,
    )


# ── Crear ────────────────────────────────────────────────────────────────────

@users_bp.route("/crear", methods=["GET", "POST"])
@admin_required
def create():
    error = None

    if request.method == "POST":
        fullname = request.form.get("fullname", "").strip()
        username = request.form.get("username", "").strip()
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        role     = request.form.get("role", "viewer")

        # Validaciones básicas
        if not all([fullname, username, email, password]):
            error = "Todos los campos son obligatorios."
        elif len(password) < 8:
            error = "La contraseña debe tener al menos 8 caracteres."
        elif role not in ROLES_DISPONIBLES:
            error = "Rol inválido."
        else:
            from app.models.entities.User import User
            from app import db
            email_taken    = User.query.filter_by(email=email.lower()).first()
            username_taken = User.query.filter_by(username=username).first()

            if email_taken:
                error = "Ese correo ya está registrado."
            elif username_taken:
                error = "Ese nombre de usuario ya está en uso."
            else:
                UserModel.create_user(fullname=fullname, username=username,
                                      email=email, password=password, role=role)
                flash(f"Usuario '{username}' creado correctamente.", "success")
                return redirect(url_for("users.show"))

    return render_template("users/form.html",
                           titulo="Crear usuario", accion="create",
                           roles=ROLES_DISPONIBLES, error=error, user=None)


# ── Editar ───────────────────────────────────────────────────────────────────

@users_bp.route("/<int:user_id>/editar", methods=["GET", "POST"])
@admin_required
def edit(user_id):
    user = UserModel.get_by_id(user_id)
    if not user:
        flash("Usuario no encontrado.", "danger")
        return redirect(url_for("users.show"))

    error = None

    if request.method == "POST":
        fullname = request.form.get("fullname", "").strip()
        username = request.form.get("username", "").strip()
        email    = request.form.get("email", "").strip()
        role     = request.form.get("role", "viewer")
        new_pwd  = request.form.get("new_password", "").strip()

        if not all([fullname, username, email]):
            error = "Nombre, usuario y correo son obligatorios."
        elif role not in ROLES_DISPONIBLES:
            error = "Rol inválido."
        else:
            user, err = UserModel.update_user(user_id, fullname, email,
                                                  username, role)
            if err:
                error = err
            else:
                # Cambiar contraseña solo si el admin escribió una nueva
                if new_pwd:
                    if len(new_pwd) < 8:
                        error = "La nueva contraseña debe tener al menos 8 caracteres."
                    else:
                        UserModel.change_password(user_id, new_pwd)

                if not error:
                    flash(f"Usuario '{user.username}' actualizado.", "success")
                    return redirect(url_for("users.show"))

    return render_template("users/form.html",
                           titulo="Editar usuario", accion="edit",
                           roles=ROLES_DISPONIBLES, error=error, user=user)


# ── Eliminar ─────────────────────────────────────────────────────────────────

@users_bp.route("/<int:user_id>/eliminar", methods=["POST"])
@admin_required
def delete(user_id):
    ok, err = UserModel.delete_user(user_id, session.get("user_id"))
    if ok:
        flash("Usuario eliminado.", "success")
    else:
        flash(err, "danger")
    return redirect(url_for("users.show"))


# ── Activar / Desactivar ─────────────────────────────────────────────────────

@users_bp.route("/<int:user_id>/toggle", methods=["POST"])
@admin_required
def toggle_active(user_id):
    ok, err = UserModel.toggle_active(user_id, session.get("user_id"))
    if not ok:
        flash(err, "danger")
    return redirect(url_for("users.show"))