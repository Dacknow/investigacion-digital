from flask_wtf import FlaskForm
from wtforms import (
    BooleanField, IntegerField, RadioField, SelectField,
    SelectMultipleField, StringField, TextAreaField,
    SubmitField, widgets
)
from wtforms.validators import (
    DataRequired, NumberRange, Optional, Length
)


# ── Widget para checkboxes múltiples con estilo personalizable ─────────────────
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


# ──────────────────────────────────────────────────────────────────────────────
#  SECCIÓN 0: CONSENTIMIENTO
# ──────────────────────────────────────────────────────────────────────────────

class ConsentimientoForm(FlaskForm):
    acepto_tratamiento_datos = BooleanField(
        "Autorizo el tratamiento de mis datos personales con fines académicos de investigación, "
        "conforme a la Ley 1581 de 2012 y el Decreto 1377 de 2013.",
        validators=[DataRequired(message="Debes aceptar el tratamiento de datos para continuar.")]
    )
    acepto_cookies_funcionales = BooleanField(
        "Acepto el uso de cookies funcionales necesarias para el correcto funcionamiento del formulario."
    )
    acepto_cookies_analiticas = BooleanField(
        "Acepto el uso de cookies analíticas para mejorar la experiencia del usuario (opcional)."
    )
    submit = SubmitField("Acepto y deseo participar")


# ──────────────────────────────────────────────────────────────────────────────
#  SECCIÓN 1: DATOS DEMOGRÁFICOS
# ──────────────────────────────────────────────────────────────────────────────

DEPARTAMENTOS_CO = [
    ("", "— Selecciona —"),
    ("Amazonas", "Amazonas"), ("Antioquia", "Antioquia"), ("Arauca", "Arauca"),
    ("Atlántico", "Atlántico"), ("Bolívar", "Bolívar"), ("Boyacá", "Boyacá"),
    ("Caldas", "Caldas"), ("Caquetá", "Caquetá"), ("Casanare", "Casanare"),
    ("Cauca", "Cauca"), ("Cesar", "Cesar"), ("Chocó", "Chocó"),
    ("Córdoba", "Córdoba"), ("Cundinamarca", "Cundinamarca"), ("Guainía", "Guainía"),
    ("Guaviare", "Guaviare"), ("Huila", "Huila"), ("La Guajira", "La Guajira"),
    ("Magdalena", "Magdalena"), ("Meta", "Meta"), ("Nariño", "Nariño"),
    ("Norte de Santander", "Norte de Santander"), ("Putumayo", "Putumayo"),
    ("Quindío", "Quindío"), ("Risaralda", "Risaralda"),
    ("San Andrés y Providencia", "San Andrés y Providencia"),
    ("Santander", "Santander"), ("Sucre", "Sucre"), ("Tolima", "Tolima"),
    ("Valle del Cauca", "Valle del Cauca"), ("Vaupés", "Vaupés"), ("Vichada", "Vichada"),
    ("Bogotá D.C.", "Bogotá D.C."),
]


class DemograficosForm(FlaskForm):
    edad = IntegerField(
        "¿Cuántos años tienes?",
        validators=[
            DataRequired(message="Campo obligatorio."),
            NumberRange(min=18, max=35, message="La investigación se enfoca en adultos jóvenes (18-35 años).")
        ]
    )
    genero = RadioField(
        "¿Con qué género te identificas?",
        choices=[
            ("hombre", "Hombre"),
            ("mujer", "Mujer"),
            ("no_binario", "No binario / género diverso"),
            ("prefiero_no_decir", "Prefiero no decirlo"),
        ],
        validators=[DataRequired(message="Por favor selecciona una opción.")]
    )
    ciudad = StringField(
        "Ciudad de residencia actual",
        validators=[DataRequired(message="Campo obligatorio."), Length(max=80)]
    )
    departamento = SelectField(
        "Departamento",
        choices=DEPARTAMENTOS_CO,
        validators=[DataRequired(message="Por favor selecciona tu departamento.")]
    )
    nivel_educativo = RadioField(
        "Nivel educativo más alto alcanzado",
        choices=[
            ("bachillerato", "Bachillerato"),
            ("tecnico_tecnologo", "Técnico / Tecnólogo"),
            ("universitario_en_curso", "Universitario (en curso)"),
            ("universitario_graduado", "Universitario (graduado)"),
            ("posgrado", "Posgrado"),
        ],
        validators=[DataRequired(message="Por favor selecciona una opción.")]
    )
    ocupacion = RadioField(
        "Ocupación principal actual",
        choices=[
            ("estudiante", "Estudiante"),
            ("empleado", "Empleado / trabajador dependiente"),
            ("independiente", "Independiente / freelancer"),
            ("desempleado", "Desempleado"),
            ("otro", "Otro"),
        ],
        validators=[DataRequired(message="Por favor selecciona una opción.")]
    )
    submit = SubmitField("Continuar →")


# ──────────────────────────────────────────────────────────────────────────────
#  SECCIÓN 2: HÁBITOS DIGITALES
# ──────────────────────────────────────────────────────────────────────────────

class HabitosForm(FlaskForm):
    horas_diarias_internet = RadioField(
        "¿Cuántas horas al día usas internet aproximadamente?",
        choices=[
            ("menos_1h", "Menos de 1 hora"),
            ("1_3h", "Entre 1 y 3 horas"),
            ("3_6h", "Entre 3 y 6 horas"),
            ("mas_6h", "Más de 6 horas"),
        ],
        validators=[DataRequired(message="Por favor selecciona una opción.")]
    )
    redes_sociales = MultiCheckboxField(
        "¿Qué redes sociales usas regularmente? (Selecciona todas las que apliquen)",
        choices=[
            ("facebook", "Facebook"),
            ("instagram", "Instagram"),
            ("tiktok", "TikTok"),
            ("twitter_x", "Twitter / X"),
            ("youtube", "YouTube"),
            ("linkedin", "LinkedIn"),
            ("whatsapp", "WhatsApp"),
            ("snapchat", "Snapchat"),
            ("telegram", "Telegram"),
            ("ninguna", "No uso redes sociales"),
        ]
    )

    # Plataformas
    usa_banca_digital = BooleanField("Banca / fintech digital (Nequi, Daviplata, app bancaria)")
    usa_comercio_electronico = BooleanField("Comercio electrónico (Mercado Libre, Amazon, Rappi)")
    usa_apps_salud = BooleanField("Apps de salud o bienestar")
    usa_apps_transporte = BooleanField("Apps de transporte (InDriver, Uber, Cabify)")
    usa_servicios_gobierno = BooleanField("Servicios digitales del gobierno (Mi Colombia Digital, DIAN, etc.)")

    # Datos compartidos
    comparte_nombre_real = BooleanField("Nombre real")
    comparte_foto_perfil = BooleanField("Foto de perfil / imágenes personales")
    comparte_ubicacion = BooleanField("Ubicación / dirección")
    comparte_telefono = BooleanField("Número de teléfono")
    comparte_datos_financieros = BooleanField("Datos financieros o bancarios")
    comparte_informacion_laboral = BooleanField("Información laboral o académica")

    lee_terminos_condiciones = RadioField(
        "Cuando te registras en una nueva plataforma, ¿lees los términos y condiciones?",
        choices=[
            ("nunca", "Nunca los leo"),
            ("a_veces", "A veces los reviso por encima"),
            ("siempre", "Siempre los leo con atención"),
        ],
        validators=[DataRequired(message="Por favor selecciona una opción.")]
    )
    conoce_ley_datos_colombia = RadioField(
        "¿Conoces la Ley de Protección de Datos Personales en Colombia (Ley 1581 de 2012)?",
        choices=[("True", "Sí la conozco"), ("False", "No la conozco")],
        validators=[DataRequired(message="Por favor selecciona una opción.")]
    )
    nivel_preocupacion_privacidad = RadioField(
        "En una escala del 1 al 5, ¿qué tan preocupado/a estás por la privacidad de tus datos?",
        choices=[(str(i), str(i)) for i in range(1, 6)],
        validators=[DataRequired(message="Por favor selecciona una opción.")]
    )
    ha_cambiado_config_privacidad = RadioField(
        "¿Has cambiado la configuración de privacidad en alguna plataforma para proteger tus datos?",
        choices=[("True", "Sí lo he hecho"), ("False", "No lo he hecho")],
        validators=[DataRequired(message="Por favor selecciona una opción.")]
    )
    submit = SubmitField("Continuar →")


# ──────────────────────────────────────────────────────────────────────────────
#  SECCIÓN 3: CONSECUENCIAS VIVIDAS
# ──────────────────────────────────────────────────────────────────────────────

class ConsecuenciasForm(FlaskForm):
    # Experiencias de riesgo
    experimento_suplantacion = BooleanField("Suplantación de identidad")
    experimento_ciberacoso = BooleanField("Ciberacoso o acoso en línea")
    experimento_fraude_financiero = BooleanField("Fraude financiero o estafa digital")
    experimento_perdida_privacidad = BooleanField("Filtración o pérdida de información privada")
    experimento_robo_cuenta = BooleanField("Robo o hackeo de una cuenta digital")
    experimento_spam_publicidad = BooleanField("Recepción masiva de spam o publicidad no deseada")
    experimento_discriminacion_laboral = BooleanField("Discriminación o perjuicio laboral por información en internet")
    ninguna_experiencia_negativa = BooleanField("No he tenido ninguna experiencia negativa")

    impacto_emocional = RadioField(
        "¿Cuál fue el impacto emocional de estas experiencias en tu vida?",
        choices=[
            ("ninguno", "Ningún impacto emocional"),
            ("leve", "Leve (preocupación pasajera)"),
            ("moderado", "Moderado (afectó mi estado de ánimo por un tiempo)"),
            ("severo", "Severo (generó ansiedad, miedo o afectación psicológica importante)"),
        ],
        validators=[DataRequired(message="Por favor selecciona una opción.")]
    )
    cambio_comportamiento_digital = RadioField(
        "¿Alguna experiencia negativa te llevó a cambiar tu comportamiento en internet?",
        choices=[("True", "Sí, cambié mi forma de actuar en línea"), ("False", "No, sigo igual")],
        validators=[DataRequired(message="Por favor selecciona una opción.")]
    )
    descripcion_cambio = TextAreaField(
        "Si cambiaste tu comportamiento, ¿puedes describir brevemente qué cambió? (opcional)",
        validators=[Optional(), Length(max=500)]
    )

    afecto_relaciones_sociales = RadioField(
        "¿La exposición de tus datos ha afectado tus relaciones sociales o personales?",
        choices=[("True", "Sí"), ("False", "No")],
        validators=[DataRequired(message="Por favor selecciona una opción.")]
    )
    afecto_oportunidades_laborales = RadioField(
        "¿Crees que tu información en internet ha afectado (o podría afectar) tus oportunidades laborales?",
        choices=[("True", "Sí"), ("False", "No")],
        validators=[DataRequired(message="Por favor selecciona una opción.")]
    )
    afecto_acceso_credito = RadioField(
        "¿Has tenido alguna situación en la que tus datos digitales afectaron tu acceso a crédito o servicios financieros?",
        choices=[("True", "Sí"), ("False", "No")],
        validators=[DataRequired(message="Por favor selecciona una opción.")]
    )

    siente_control_datos = RadioField(
        "¿Qué tan en control te sientes de tu información personal en internet? (1 = nada, 5 = completamente)",
        choices=[(str(i), str(i)) for i in range(1, 6)],
        validators=[DataRequired(message="Por favor selecciona una opción.")]
    )
    confianza_plataformas = RadioField(
        "¿Qué tanta confianza tienes en las plataformas digitales para proteger tus datos? (1 = ninguna, 5 = mucha)",
        choices=[(str(i), str(i)) for i in range(1, 6)],
        validators=[DataRequired(message="Por favor selecciona una opción.")]
    )
    submit = SubmitField("Finalizar encuesta ✓")