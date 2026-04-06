"""
Fábrica de la aplicación Flask.
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-key-insegura")

    # Railway genera 'postgresql://' pero SQLAlchemy necesita 'postgresql+psycopg2://'
    database_url = os.getenv("DATABASE_URL", "")
    if database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+psycopg2://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url or \
        "postgresql+psycopg2://postgres:password@localhost:5432/investigacion_digital"
    
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["WTF_CSRF_ENABLED"] = True
    app.config["INVESTIGACION"] = {
        "titulo": os.getenv("INVESTIGACION_TITULO", "Investigación Datos Personales 2026"),
        "responsable": os.getenv("INVESTIGACION_RESPONSABLE", "Investigador Principal"),
        "institucion": os.getenv("INVESTIGACION_INSTITUCION", "Institución Educativa"),
        "contacto": os.getenv("INVESTIGACION_CONTACTO", "contacto@institucion.edu.co"),
    }

    db.init_app(app)
    migrate.init_app(app, db)

    # Importar modelos ANTES de registrar blueprints
    with app.app_context():
        from app.models import Models  # noqa: F401
        from app.models.entities.User import User

    from app.routes.auth import auth_bp         
    from app.routes.main import main_bp
    from app.routes.encuesta import encuesta_bp
    from app.routes.admin import admin_bp
    from app.routes.users import users_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(main_bp)
    app.register_blueprint(encuesta_bp, url_prefix="/encuesta")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(users_bp, url_prefix="/admin/users")

    @app.context_processor
    def inject_investigacion():
        return {"investigacion": app.config["INVESTIGACION"]}
    
    @app.context_processor
    def inject_current_user():
        from app.models.UserModel import UserModel
        return {"current_user": UserModel.get_current_user()}

    return app