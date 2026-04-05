"""
UserModel — lógica de autenticación.
Aquí se maneja todo lo relacionado con usuarios: login, logout, creación, edición, roles y recuperación de contraseña.
"""
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from datetime import datetime, timezone
from app import db
from app.models.entities.User import User


class UserModel:

    # ── Registro ────────────────────────────────────────────────────────────
    @staticmethod
    def create_user(username, fullname, email, password, role="viewer"):
        """Crea un usuario nuevo con contraseña hasheada."""
        user = User(
            username=username,
            fullname=fullname,
            email=email.lower().strip(),
            password_hash=generate_password_hash(password),
            role=role,
        )
        db.session.add(user)
        db.session.commit()
        return user

    # ── Login ───────────────────────────────────────────────────────────────
    @staticmethod
    def login(email, password):
       
        user = User.query.filter_by(
            email=email.lower().strip(),
            is_active=True
        ).first()

        if user and check_password_hash(user.password_hash, password):
            # Guardar en sesión de Flask
            session["user_id"]   = user.id
            session["user_role"] = user.role
            session.permanent    = True

            # Registrar último login
            user.last_login = datetime.now(timezone.utc)
            db.session.commit()
            return user

        return None

    # ── Logout ──────────────────────────────────────────────────────────────
    @staticmethod
    def logout():
        session.pop("user_id", None)
        session.pop("user_role", None)

    # ── Usuario actual ──────────────────────────────────────────────────────
    @staticmethod
    def get_current_user():
        """Retorna el User de la sesión activa, o None."""
        uid = session.get("user_id")
        if uid:
            return db.session.get(User, uid)
        return None

    @staticmethod
    def is_logged_in():
        return "user_id" in session

    @staticmethod
    def is_admin():
        return session.get("user_role") == "admin"

    # ── Recuperación de contraseña ──────────────────────────────────────────
    @staticmethod
    def request_password_reset(email):
        
        user = User.query.filter_by(
            email=email.lower().strip(),
            is_active=True
        ).first()

        if user:
            token = user.generate_reset_token()
            db.session.commit()
            return user, token

        return None, None

    @staticmethod
    def reset_password(token, new_password):
        
        user = User.query.filter_by(reset_token=token).first()

        if not user or not user.reset_token_is_valid(token):
            return False

        user.password_hash = generate_password_hash(new_password)
        user.clear_reset_token()
        db.session.commit()
        return True
    
    # ── CRUD ────────────────────────────────────────────────────────────────

    @staticmethod
    def get_all_users():
        
        return User.query.order_by(User.created_at.desc()).all()

    @staticmethod
    def get_by_id(user_id):
        return db.session.get(User, user_id)

    @staticmethod
    def update_user(user_id, fullname, email, username, role):
        
        user = db.session.get(User, user_id)
        if not user:
            return None, "Usuario no encontrado."

        # Verificar que email y username no estén en uso por otro usuario
        email_taken = User.query.filter(
            User.email == email.lower().strip(),
            User.id != user_id
        ).first()
        if email_taken:
            return None, "Ese correo ya está en uso por otro usuario."

        username_taken = User.query.filter(
            User.username == username.strip(),
            User.id != user_id
        ).first()
        if username_taken:
            return None, "Ese nombre de usuario ya está en uso."

        user.fullname = fullname.strip()
        user.email    = email.lower().strip()
        user.username = username.strip()
        user.role     = role
        db.session.commit()
        return user, None

    @staticmethod
    def change_password(user_id, new_password):
        
        from werkzeug.security import generate_password_hash
        user = db.session.get(User, user_id)
        if not user:
            return False
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        return True

    @staticmethod
    def delete_user(user_id, current_user_id):
        
        if user_id == current_user_id:
            return False, "No puedes eliminar tu propia cuenta."

        user = db.session.get(User, user_id)
        if not user:
            return False, "Usuario no encontrado."

        db.session.delete(user)
        db.session.commit()
        return True, None

    @staticmethod
    def toggle_active(user_id, current_user_id):
        
        if user_id == current_user_id:
            return False, "No puedes desactivar tu propia cuenta."

        user = db.session.get(User, user_id)
        if not user:
            return False, "Usuario no encontrado."

        user.is_active = not user.is_active
        db.session.commit()
        return True, None