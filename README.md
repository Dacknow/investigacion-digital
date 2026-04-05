# 🔐 Sistema de Recolección de Datos — Investigación Digital 2026

> **Influencia de la información de datos personales compartida en internet**  
> **sobre la vida de adultos jóvenes en Colombia durante el año 2026**

Sistema web en Python/Flask para recopilación de datos mediante formularios con consentimiento informado y cookies autorizadas por el usuario, en cumplimiento de la **Ley 1581 de 2012** (Habeas Data).

---

## 📁 Estructura del proyecto

```
investigacion_digital/
├── run.py                        ← Punto de entrada
├── requirements.txt              ← Dependencias Python
├── .env.example                  ← Plantilla de configuración
├── app/
│   ├── __init__.py               ← Application Factory
│   ├── models/
│   │   └── models.py             ← Tablas PostgreSQL (4 modelos)
│   └── routes/
│       ├── forms.py              ← Formularios WTForms validados
│       ├── encuesta.py           ← Flujo de la encuesta (4 pasos)
│       ├── admin.py              ← Panel de administración
│       └── main.py               ← Página de inicio
├── scripts/
│   ├── init_db.py                ← Inicializa la base de datos
│   └── exportar_excel.py         ← Exporta a .xlsx con estadísticas
└── app/templates/
    ├── base.html                 ← Layout principal
    ├── index.html                ← Landing page
    ├── encuesta/
    │   ├── consentimiento.html   ← Paso 0: consentimiento + cookies
    │   ├── demograficos.html     ← Paso 1: datos demográficos
    │   ├── habitos.html          ← Paso 2: hábitos digitales
    │   ├── consecuencias.html    ← Paso 3: experiencias e impacto
    │   └── gracias.html          ← Página final
    └── admin/
        ├── login.html            ← Acceso al panel
        ├── dashboard.html        ← Estadísticas generales
        └── respuestas.html       ← Tabla paginada de respuestas
```

---

## ⚡ Instalación rápida

### 1. Requisitos previos
- Python 3.10+
- PostgreSQL 14+
- pip

### 2. Clonar e instalar dependencias

```bash
cd investigacion_digital
pip install -r requirements.txt
```

### 3. Configurar el entorno

```bash
cp .env.example .env
```

Edita `.env` y ajusta:

```env
SECRET_KEY=una-clave-secreta-larga-y-aleatoria
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/investigacion_digital
ADMIN_PASSWORD=tu-contraseña-admin
INVESTIGACION_RESPONSABLE=Tu Nombre
INVESTIGACION_INSTITUCION=Tu Universidad
INVESTIGACION_CONTACTO=tu@correo.edu.co
```

### 4. Crear la base de datos en PostgreSQL

```sql
-- En psql o pgAdmin:
CREATE DATABASE investigacion_digital;
```

### 5. Inicializar las tablas

```bash
python scripts/init_db.py
```

### 6. Levantar el servidor

```bash
python run.py
```

Abre en el navegador: **http://localhost:5000**

---

## 🗺️ Flujo de la encuesta

```
/                          → Landing page
/encuesta/consentimiento   → Consentimiento + política de cookies  (Paso 0)
/encuesta/demograficos     → Datos demográficos                    (Paso 1)
/encuesta/habitos          → Hábitos digitales                     (Paso 2)
/encuesta/consecuencias    → Experiencias e impacto                (Paso 3)
/encuesta/gracias          → Página de agradecimiento
```

---

## 🔒 Panel de administración

Accede en: **http://localhost:5000/admin**

| Ruta | Función |
|------|---------|
| `/admin/login` | Inicio de sesión |
| `/admin/` | Dashboard con estadísticas |
| `/admin/respuestas` | Tabla paginada de respuestas |
| `/admin/exportar/csv` | Descarga CSV de todos los datos |

---

## 📊 Exportación a Excel

Para generar un reporte completo en `.xlsx`:

```bash
python scripts/exportar_excel.py
# o con nombre personalizado:
python scripts/exportar_excel.py --output resultados_junio_2026.xlsx
```

El archivo incluye **3 hojas**:
- **Resumen**: métricas clave para el investigador
- **Datos crudos**: una fila por participante (para SPSS, R, etc.)
- **Frecuencias**: tablas de distribución por variable

---

## 🗄️ Modelo de datos

| Tabla | Descripción |
|-------|-------------|
| `consentimiento_log` | Registro legal de aceptación (IP anonimizada, timestamp, versión de política) |
| `participante` | Datos demográficos: edad, género, ciudad, departamento, educación, ocupación |
| `habitos_digitales` | Redes usadas, datos compartidos, conciencia sobre privacidad |
| `consecuencias_vividas` | Experiencias negativas, impacto emocional, social y laboral |

---

## ⚖️ Cumplimiento legal

- **Ley 1581 de 2012** (Colombia) — Protección de datos personales
- **Decreto 1377 de 2013** — Reglamentación
- IPs anonimizadas (solo se guardan los primeros 3 octetos)
- Token de sesión único por participante
- Consentimiento explícito antes de cualquier recolección de datos
- Cookies diferenciadas: funcionales (necesarias) vs. analíticas (opcionales)

---

## 🛠 Tecnologías

| Componente | Tecnología |
|------------|------------|
| Backend | Python 3 + Flask 3 |
| Base de datos | PostgreSQL + SQLAlchemy ORM |
| Migraciones | Flask-Migrate (Alembic) |
| Formularios | Flask-WTF + WTForms |
| Protección CSRF | Flask-WTF (activado por defecto) |
| Exportación | openpyxl (Excel) + csv (nativo) |
| Frontend | HTML5 + CSS3 (sin frameworks externos) |