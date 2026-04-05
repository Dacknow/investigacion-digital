"""
Script de inicialización de la base de datos.
Ejecutar UNA VEZ al configurar el proyecto por primera vez.

Uso:
    python scripts/init_db.py
"""
import sys
import os

# Asegura que el directorio raíz del proyecto esté en el path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app, db


def init_db():
    app = create_app()

    with app.app_context():
        print("🔧 Creando tablas en PostgreSQL...")
        db.create_all()
        print("✅ Tablas creadas exitosamente:")
        print("   · consentimiento_log")
        print("   · participante")
        print("   · habitos_digitales")
        print("   · consecuencias_vividas")
        print()
        print("🚀 Base de datos lista. Puedes iniciar el servidor con:")
        print("   flask run   ó   python run.py")


if __name__ == "__main__":
    init_db()