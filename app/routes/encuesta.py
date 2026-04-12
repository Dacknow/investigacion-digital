import secrets
import hashlib
from flask import (
    Blueprint, render_template, redirect, url_for,
    session, request, flash, abort
)
from app import db
from app.models import ConsentimientoLog, Participante, HabitosDigitales, ConsecuenciasVividas
from app.routes.forms import ConsentimientoForm, DemograficosForm, HabitosForm, ConsecuenciasForm

encuesta_bp = Blueprint("encuesta", __name__)


# ── Helpers ────────────────────────────────────────────────────────────────────

def _anonimizar_ip(ip: str) -> str:
    
    if ip and "." in ip:
        partes = ip.split(".")
        return ".".join(partes[:3]) + ".0"
    return "0.0.0.0"


def _str_to_bool(valor: str) -> bool:
    return valor == "True"


def _get_participante_activo():
    
    pid = session.get("participante_id")
    if pid:
        return db.session.get(Participante, pid)
    return None


# ── PASO 0: Consentimiento ─────────────────────────────────────────────────────

@encuesta_bp.route("/consentimiento", methods=["GET", "POST"])
def consentimiento():
    # Si ya dio consentimiento en esta sesión, avanzar
    if session.get("consentimiento_id"):
        return redirect(url_for("encuesta.demograficos"))

    form = ConsentimientoForm()

    if form.validate_on_submit():
        token = secrets.token_hex(32)
        ip_raw = request.headers.get("X-Forwarded-For", request.remote_addr)
        ip_anon = _anonimizar_ip(ip_raw.split(",")[0].strip())

        log = ConsentimientoLog(
            session_token=token,
            acepto_tratamiento_datos=form.acepto_tratamiento_datos.data,
            acepto_cookies_funcionales=form.acepto_cookies_funcionales.data,
            acepto_cookies_analiticas=form.acepto_cookies_analiticas.data,
            ip_anonimizada=ip_anon,
            user_agent=request.user_agent.string[:300],
        )
        db.session.add(log)
        db.session.commit()

        session["consentimiento_id"] = log.id
        session["session_token"] = token
        session.permanent = True

        return redirect(url_for("encuesta.demograficos"))

    return render_template("encuesta/consentimiento.html", form=form)


# ── PASO 1: Datos demográficos ─────────────────────────────────────────────────

@encuesta_bp.route("/demograficos", methods=["GET", "POST"])
def demograficos():
    if not session.get("consentimiento_id"):
        flash("Primero debes aceptar el consentimiento informado.", "warning")
        return redirect(url_for("encuesta.consentimiento"))

    # Si ya existe participante en sesión, redirigir al siguiente paso
    if session.get("participante_id"):
        return redirect(url_for("encuesta.habitos"))

    form = DemograficosForm()

    if form.validate_on_submit():
        participante = Participante(
            consentimiento_id=session["consentimiento_id"],
            edad=form.edad.data,
            genero=form.genero.data,
            ciudad=form.ciudad.data,
            departamento=form.departamento.data,
            nivel_educativo=form.nivel_educativo.data,
            ocupacion=form.ocupacion.data,
        )
        db.session.add(participante)
        db.session.commit()

        session["participante_id"] = participante.id
        return redirect(url_for("encuesta.habitos"))

    return render_template("encuesta/demograficos.html", form=form, paso=1, total_pasos=3)


# ── PASO 2: Hábitos digitales ──────────────────────────────────────────────────

@encuesta_bp.route("/habitos", methods=["GET", "POST"])
def habitos():
    participante = _get_participante_activo()
    if not participante:
        return redirect(url_for("encuesta.consentimiento"))

    if participante.habitos:
        return redirect(url_for("encuesta.consecuencias"))

    form = HabitosForm()

    if form.validate_on_submit():
        redes = ",".join(form.redes_sociales.data) if form.redes_sociales.data else ""

        habito = HabitosDigitales(
            participante_id=participante.id,
            horas_diarias_internet=form.horas_diarias_internet.data,
            redes_sociales=redes,
            usa_banca_digital=form.usa_banca_digital.data,
            usa_comercio_electronico=form.usa_comercio_electronico.data,
            usa_apps_salud=form.usa_apps_salud.data,
            usa_apps_transporte=form.usa_apps_transporte.data,
            usa_servicios_gobierno=form.usa_servicios_gobierno.data,
            comparte_nombre_real=form.comparte_nombre_real.data,
            comparte_foto_perfil=form.comparte_foto_perfil.data,
            comparte_ubicacion=form.comparte_ubicacion.data,
            comparte_telefono=form.comparte_telefono.data,
            comparte_datos_financieros=form.comparte_datos_financieros.data,
            comparte_informacion_laboral=form.comparte_informacion_laboral.data,
            lee_terminos_condiciones=form.lee_terminos_condiciones.data,
            conoce_ley_datos_colombia=_str_to_bool(form.conoce_ley_datos_colombia.data),
            nivel_preocupacion_privacidad=int(form.nivel_preocupacion_privacidad.data),
            ha_cambiado_config_privacidad=_str_to_bool(form.ha_cambiado_config_privacidad.data),
        )
        db.session.add(habito)
        db.session.commit()

        return redirect(url_for("encuesta.consecuencias"))

    return render_template("encuesta/habitos.html", form=form, paso=2, total_pasos=3)


# ── PASO 3: Consecuencias vividas ──────────────────────────────────────────────

@encuesta_bp.route("/consecuencias", methods=["GET", "POST"])
def consecuencias():
    participante = _get_participante_activo()
    if not participante:
        return redirect(url_for("encuesta.consentimiento"))

    if not participante.habitos:
        return redirect(url_for("encuesta.habitos"))

    if participante.consecuencias:
        return redirect(url_for("encuesta.gracias"))

    form = ConsecuenciasForm()

    if form.validate_on_submit():
        consecuencia = ConsecuenciasVividas(
            participante_id=participante.id,
            experimento_suplantacion=form.experimento_suplantacion.data,
            experimento_ciberacoso=form.experimento_ciberacoso.data,
            experimento_fraude_financiero=form.experimento_fraude_financiero.data,
            experimento_perdida_privacidad=form.experimento_perdida_privacidad.data,
            experimento_robo_cuenta=form.experimento_robo_cuenta.data,
            experimento_spam_publicidad=form.experimento_spam_publicidad.data,
            experimento_discriminacion_laboral=form.experimento_discriminacion_laboral.data,
            ninguna_experiencia_negativa=form.ninguna_experiencia_negativa.data,
            impacto_emocional=form.impacto_emocional.data,
            cambio_comportamiento_digital=_str_to_bool(form.cambio_comportamiento_digital.data),
            descripcion_cambio=form.descripcion_cambio.data or None,
            afecto_relaciones_sociales=_str_to_bool(form.afecto_relaciones_sociales.data),
            afecto_oportunidades_laborales=_str_to_bool(form.afecto_oportunidades_laborales.data),
            afecto_acceso_credito=_str_to_bool(form.afecto_acceso_credito.data),
            siente_control_datos=int(form.siente_control_datos.data),
            confianza_plataformas=int(form.confianza_plataformas.data),
        )
        db.session.add(consecuencia)

        # Marcar participante como completado
        participante.completado = True
        db.session.commit()

        # Limpiar datos de sesión (no necesitamos seguir el progreso)
        session.pop("participante_id", None)
        session.pop("consentimiento_id", None)

        return redirect(url_for("encuesta.gracias"))

    return render_template("encuesta/consecuencias.html", form=form, paso=3, total_pasos=3)


# ── PASO FINAL: Gracias ────────────────────────────────────────────────────────

@encuesta_bp.route("/gracias")
def gracias():
    return render_template("encuesta/gracias.html")