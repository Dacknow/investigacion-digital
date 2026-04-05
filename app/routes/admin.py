import io
import os
import csv
from datetime import datetime, timezone
from app.routes.decorators import login_required, admin_required

from flask import (
    Blueprint, render_template, redirect, url_for,
    session, request, flash, Response
)
from sqlalchemy import func
from app import db
from app.models import ConsentimientoLog, Participante, HabitosDigitales, ConsecuenciasVividas

admin_bp = Blueprint("admin", __name__)



# ── Dashboard ──────────────────────────────────────────────────────────────────

@admin_bp.route("/")
@login_required
def dashboard():
    total_consentimientos = db.session.query(func.count(ConsentimientoLog.id)).scalar()
    total_completos = db.session.query(func.count(Participante.id)).filter_by(completado=True).scalar()
    total_incompletos = db.session.query(func.count(Participante.id)).filter_by(completado=False).scalar()

    # Distribución por género
    generos = (
        db.session.query(Participante.genero, func.count(Participante.id))
        .filter_by(completado=True)
        .group_by(Participante.genero)
        .all()
    )

    # Distribución por departamento (top 10)
    departamentos = (
        db.session.query(Participante.departamento, func.count(Participante.id))
        .filter_by(completado=True)
        .group_by(Participante.departamento)
        .order_by(func.count(Participante.id).desc())
        .limit(10)
        .all()
    )

    # Experiencias más comunes
    consecuencias_stats = {}
    if total_completos > 0:
        campos_exp = [
            ("suplantación", "experimento_suplantacion"),
            ("ciberacoso", "experimento_ciberacoso"),
            ("fraude financiero", "experimento_fraude_financiero"),
            ("pérdida privacidad", "experimento_perdida_privacidad"),
            ("robo de cuenta", "experimento_robo_cuenta"),
            ("spam/publicidad", "experimento_spam_publicidad"),
            ("discriminación laboral", "experimento_discriminacion_laboral"),
        ]
        for etiqueta, campo in campos_exp:
            n = db.session.query(func.count(ConsecuenciasVividas.id)).filter(
                getattr(ConsecuenciasVividas, campo) == True
            ).scalar()
            consecuencias_stats[etiqueta] = round((n / total_completos) * 100, 1)

    return render_template(
        "admin/dashboard.html",
        total_consentimientos=total_consentimientos,
        total_completos=total_completos,
        total_incompletos=total_incompletos,
        generos=generos,
        departamentos=departamentos,
        consecuencias_stats=consecuencias_stats,
    )


# ── Lista de respuestas ────────────────────────────────────────────────────────

@admin_bp.route("/respuestas")
@login_required
def respuestas():
    pagina = request.args.get("pagina", 1, type=int)
    por_pagina = 20
    participantes = (
        Participante.query
        .filter_by(completado=True)
        .order_by(Participante.fecha_respuesta.desc())
        .paginate(page=pagina, per_page=por_pagina, error_out=False)
    )
    return render_template("admin/respuestas.html", participantes=participantes)


# ── Exportar CSV ───────────────────────────────────────────────────────────────

@admin_bp.route("/exportar/csv")
@login_required
def exportar_csv():
    participantes = (
        Participante.query
        .filter_by(completado=True)
        .join(HabitosDigitales)
        .join(ConsecuenciasVividas)
        .all()
    )

    output = io.StringIO()
    writer = csv.writer(output)

    # Encabezados
    writer.writerow([
        "id", "fecha_respuesta",
        # Demográficos
        "edad", "genero", "ciudad", "departamento", "nivel_educativo", "ocupacion",
        # Hábitos
        "horas_diarias_internet", "redes_sociales",
        "usa_banca", "usa_ecommerce", "usa_salud", "usa_transporte", "usa_gobierno",
        "comparte_nombre", "comparte_foto", "comparte_ubicacion",
        "comparte_telefono", "comparte_financiero", "comparte_laboral",
        "lee_terminos", "conoce_ley_1581", "nivel_preocupacion", "cambio_config_privacidad",
        # Consecuencias
        "exp_suplantacion", "exp_ciberacoso", "exp_fraude", "exp_privacidad",
        "exp_robo_cuenta", "exp_spam", "exp_discriminacion_laboral", "ninguna_exp",
        "impacto_emocional", "cambio_comportamiento", "descripcion_cambio",
        "afecto_relaciones", "afecto_empleo", "afecto_credito",
        "control_datos_1_5", "confianza_plataformas_1_5",
    ])

    for p in participantes:
        h = p.habitos
        c = p.consecuencias
        writer.writerow([
            p.id,
            p.fecha_respuesta.strftime("%Y-%m-%d %H:%M") if p.fecha_respuesta else "",
            p.edad, p.genero, p.ciudad, p.departamento, p.nivel_educativo, p.ocupacion,
            h.horas_diarias_internet, h.redes_sociales,
            h.usa_banca_digital, h.usa_comercio_electronico, h.usa_apps_salud,
            h.usa_apps_transporte, h.usa_servicios_gobierno,
            h.comparte_nombre_real, h.comparte_foto_perfil, h.comparte_ubicacion,
            h.comparte_telefono, h.comparte_datos_financieros, h.comparte_informacion_laboral,
            h.lee_terminos_condiciones, h.conoce_ley_datos_colombia,
            h.nivel_preocupacion_privacidad, h.ha_cambiado_config_privacidad,
            c.experimento_suplantacion, c.experimento_ciberacoso,
            c.experimento_fraude_financiero, c.experimento_perdida_privacidad,
            c.experimento_robo_cuenta, c.experimento_spam_publicidad,
            c.experimento_discriminacion_laboral, c.ninguna_experiencia_negativa,
            c.impacto_emocional, c.cambio_comportamiento_digital, c.descripcion_cambio or "",
            c.afecto_relaciones_sociales, c.afecto_oportunidades_laborales, c.afecto_acceso_credito,
            c.siente_control_datos, c.confianza_plataformas,
        ])

    filename = f"respuestas_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M')}.csv"
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )