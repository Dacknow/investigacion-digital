"""
Modelos de base de datos para el sistema de investigación.

Tablas:
- ConsentimientoLog : registro de aceptación de cookies y política de datos
- Participante      : datos demográficos del encuestado
- HabitosDigitales  : uso de redes sociales y plataformas
- ConsecuenciasVividas : experiencias de riesgo digital
"""
from datetime import datetime, timezone
from app import db


# ──────────────────────────────────────────────────────────────────────────────
#  CONSENTIMIENTO Y COOKIES
# ──────────────────────────────────────────────────────────────────────────────

class ConsentimientoLog(db.Model):
    """
    Registra cada vez que un usuario acepta el consentimiento informado.
    Cumple con Ley 1581/2012 (habeas data) y políticas de cookies.
    """
    __tablename__ = "consentimiento_log"

    id = db.Column(db.Integer, primary_key=True)
    session_token = db.Column(db.String(64), unique=True, nullable=False, index=True)

    # Qué aceptó exactamente
    acepto_tratamiento_datos = db.Column(db.Boolean, nullable=False, default=False)
    acepto_cookies_funcionales = db.Column(db.Boolean, nullable=False, default=False)
    acepto_cookies_analiticas = db.Column(db.Boolean, nullable=False, default=False)

    # Metadatos legales
    ip_anonimizada = db.Column(db.String(20))          # Solo primeros 3 octetos
    user_agent = db.Column(db.String(300))
    fecha_consentimiento = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    version_politica = db.Column(db.String(10), default="1.0")

    # Relación con el participante (puede ser nula si no completa la encuesta)
    participante = db.relationship("Participante", back_populates="consentimiento", uselist=False)

    def __repr__(self):
        return f"<Consentimiento {self.session_token[:8]}... @ {self.fecha_consentimiento}>"


# ──────────────────────────────────────────────────────────────────────────────
#  DATOS DEMOGRÁFICOS
# ──────────────────────────────────────────────────────────────────────────────

class Participante(db.Model):
    """
    Datos demográficos básicos del participante.
    Vinculado 1-a-1 con el consentimiento para trazabilidad legal.
    """
    __tablename__ = "participante"

    id = db.Column(db.Integer, primary_key=True)
    consentimiento_id = db.Column(
        db.Integer,
        db.ForeignKey("consentimiento_log.id"),
        nullable=False,
        unique=True
    )

    # Datos demográficos
    edad = db.Column(db.Integer, nullable=False)
    genero = db.Column(db.String(30), nullable=False)   # hombre / mujer / no binario / prefiero no decir
    ciudad = db.Column(db.String(80), nullable=False)
    departamento = db.Column(db.String(80))
    nivel_educativo = db.Column(db.String(60))           # bachillerato, técnico, universitario, posgrado
    ocupacion = db.Column(db.String(60))                 # estudiante, empleado, independiente, desempleado

    # Metadatos de la respuesta
    fecha_respuesta = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    completado = db.Column(db.Boolean, default=False)   # True solo cuando finaliza todas las secciones

    # Relaciones
    consentimiento = db.relationship("ConsentimientoLog", back_populates="participante")
    habitos = db.relationship("HabitosDigitales", back_populates="participante", uselist=False)
    consecuencias = db.relationship("ConsecuenciasVividas", back_populates="participante", uselist=False)

    def __repr__(self):
        return f"<Participante {self.id} | {self.ciudad} | {self.edad} años>"


# ──────────────────────────────────────────────────────────────────────────────
#  HÁBITOS DIGITALES
# ──────────────────────────────────────────────────────────────────────────────

class HabitosDigitales(db.Model):
    """
    Uso de plataformas digitales, tipos de datos compartidos
    y nivel de conciencia sobre privacidad.
    """
    __tablename__ = "habitos_digitales"

    id = db.Column(db.Integer, primary_key=True)
    participante_id = db.Column(
        db.Integer,
        db.ForeignKey("participante.id"),
        nullable=False,
        unique=True
    )

    # Frecuencia de uso de internet
    horas_diarias_internet = db.Column(db.String(20))    # <1h, 1-3h, 3-6h, >6h

    # Redes sociales usadas (almacenadas como lista separada por comas)
    redes_sociales = db.Column(db.Text)                  # facebook,instagram,tiktok,twitter,...

    # Plataformas donde comparte datos
    usa_banca_digital = db.Column(db.Boolean, default=False)
    usa_comercio_electronico = db.Column(db.Boolean, default=False)
    usa_apps_salud = db.Column(db.Boolean, default=False)
    usa_apps_transporte = db.Column(db.Boolean, default=False)
    usa_servicios_gobierno = db.Column(db.Boolean, default=False)

    # Tipos de datos que comparte
    comparte_nombre_real = db.Column(db.Boolean, default=False)
    comparte_foto_perfil = db.Column(db.Boolean, default=False)
    comparte_ubicacion = db.Column(db.Boolean, default=False)
    comparte_telefono = db.Column(db.Boolean, default=False)
    comparte_datos_financieros = db.Column(db.Boolean, default=False)
    comparte_informacion_laboral = db.Column(db.Boolean, default=False)

    # Conciencia sobre privacidad
    lee_terminos_condiciones = db.Column(db.String(30))  # nunca, a veces, siempre
    conoce_ley_datos_colombia = db.Column(db.Boolean)
    nivel_preocupacion_privacidad = db.Column(db.Integer)  # escala 1-5
    ha_cambiado_config_privacidad = db.Column(db.Boolean)

    participante = db.relationship("Participante", back_populates="habitos")

    def get_redes_lista(self):
        """Retorna las redes sociales como lista Python."""
        if self.redes_sociales:
            return [r.strip() for r in self.redes_sociales.split(",")]
        return []


# ──────────────────────────────────────────────────────────────────────────────
#  CONSECUENCIAS VIVIDAS
# ──────────────────────────────────────────────────────────────────────────────

class ConsecuenciasVividas(db.Model):
    """
    Experiencias negativas o de riesgo digital que el participante
    ha vivido en relación a sus datos personales.
    """
    __tablename__ = "consecuencias_vividas"

    id = db.Column(db.Integer, primary_key=True)
    participante_id = db.Column(
        db.Integer,
        db.ForeignKey("participante.id"),
        nullable=False,
        unique=True
    )

    # Experiencias de riesgo (sí/no)
    experimento_suplantacion = db.Column(db.Boolean, default=False)
    experimento_ciberacoso = db.Column(db.Boolean, default=False)
    experimento_fraude_financiero = db.Column(db.Boolean, default=False)
    experimento_perdida_privacidad = db.Column(db.Boolean, default=False)
    experimento_robo_cuenta = db.Column(db.Boolean, default=False)
    experimento_spam_publicidad = db.Column(db.Boolean, default=False)
    experimento_discriminacion_laboral = db.Column(db.Boolean, default=False)
    ninguna_experiencia_negativa = db.Column(db.Boolean, default=False)

    # Impacto psicológico
    impacto_emocional = db.Column(db.String(30))         # ninguno, leve, moderado, severo
    cambio_comportamiento_digital = db.Column(db.Boolean)  # ¿cambió su comportamiento por una mala experiencia?
    descripcion_cambio = db.Column(db.Text)              # campo abierto (opcional)

    # Impacto social / laboral
    afecto_relaciones_sociales = db.Column(db.Boolean)
    afecto_oportunidades_laborales = db.Column(db.Boolean)
    afecto_acceso_credito = db.Column(db.Boolean)

    # Percepción general
    siente_control_datos = db.Column(db.Integer)         # escala 1-5
    confianza_plataformas = db.Column(db.Integer)        # escala 1-5

    participante = db.relationship("Participante", back_populates="consecuencias")