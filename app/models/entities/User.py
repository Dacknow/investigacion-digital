import secrets
from datetime import datetime, timezone, timedelta
from app import db


class User(db.Model):
    __tablename__ = "users"

    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(50), unique=True, nullable=False)
    fullname      = db.Column(db.String(120), nullable=False)
    email         = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role          = db.Column(db.String(30), default="viewer", nullable=False)
    # ^ "viewer" o "admin" por ahora — fácil de ampliar con roles más adelante

    is_active     = db.Column(db.Boolean, default=True, nullable=False)
    created_at    = db.Column(db.DateTime(timezone=True),
                              default=lambda: datetime.now(timezone.utc))
    last_login    = db.Column(db.DateTime(timezone=True), nullable=True)

    # ── Recuperación de contraseña ──────────────────────────────────────────
    reset_token            = db.Column(db.String(100), nullable=True, index=True)
    reset_token_expires_at = db.Column(db.DateTime(timezone=True), nullable=True)

    def generate_reset_token(self):
        """Genera un token seguro de 48 chars válido por 1 hora."""
        self.reset_token = secrets.token_urlsafe(36)
        self.reset_token_expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
        return self.reset_token

    def reset_token_is_valid(self, token: str) -> bool:
        """Verifica que el token exista y no haya expirado."""
        if not self.reset_token or self.reset_token != token:
            return False
        return datetime.now(timezone.utc) < self.reset_token_expires_at

    def clear_reset_token(self):
        self.reset_token = None
        self.reset_token_expires_at = None

    def __repr__(self):
        return f"<User {self.username} | role={self.role}>"
