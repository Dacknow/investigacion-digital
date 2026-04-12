# Investigación Digital 2026

> **Influencia de la información de datos personales compartida en internet**
> **sobre la vida de adultos jóvenes en Colombia durante el año 2026**

Sistema web académico para recolección de datos mediante formularios con consentimiento informado y cookies autorizadas, en cumplimiento de la **Ley 1581 de 2012** (Habeas Data).

 **Producción:** https://investigacion-digital-production.up.railway.app

---

## Estructura del proyecto

```
investigacion_digital/
├── run.py                            ← Punto de entrada
├── requirements.txt                  ← Dependencias Python
├── Procfile                          ← Configuración Railway
├── .env.example                      ← Plantilla de variables de entorno
├── .gitignore
│
├── app/
│   ├── __init__.py                   ← Application Factory (Flask + SQLAlchemy)
│   │
│   ├── models/
│   │   ├── models.py                 ← Tablas de la encuesta (4 modelos)
│   │   ├── user_model.py             ← Lógica de autenticación y CRUD
│   │   └── entities/
│   │       └── user.py               ← Entidad User (tabla users)
│   │
│   ├── routes/
│   │   ├── decorators.py             ← @login_required, @admin_required
│   │   ├── main.py                   ← Página de inicio
│   │   ├── auth.py                   ← Login, logout, recuperación de contraseña
│   │   ├── encuesta.py               ← Flujo de la encuesta (4 pasos)
│   │   ├── admin.py                  ← Dashboard, respuestas, exportación
│   │   ├── users.py               ← CRUD de usuarios
│   │   └── forms.py                  ← Formularios WTForms validados
│   │
│   ├── services/
│   │   └── email_service.py          ← Envío de emails vía Gmail SMTP
│   │
│   └── templates/
│       ├── base.html                 ← Layout principal con CSS
│       ├── index.html                ← Landing page pública
│       ├── auth/
│       │   ├── login.html
│       │   ├── request_reset.html
│       │   └── do_reset.html
│       ├── encuesta/
│       │   ├── consentimiento.html   ← Paso 0: consentimiento + cookies
│       │   ├── demograficos.html     ← Paso 1: datos demográficos
│       │   ├── habitos.html          ← Paso 2: hábitos digitales
│       │   ├── consecuencias.html    ← Paso 3: experiencias e impacto
│       │   └── gracias.html
│       ├── admin/
│       │   ├── dashboard.html        ← Estadísticas en tiempo real
│       │   └── respuestas.html       ← Tabla paginada de respuestas
│       └── usuarios/
│           ├── show.html           ← Lista de usuarios del sistema
│           └── form.html             ← Formulario crear / editar usuario
│
└── scripts/
    ├── init_db.py                    ← Inicializa las tablas en PostgreSQL
    └── exportar_excel.py             ← Exporta datos a .xlsx
```

## URLs del sistema

### Públicas (encuesta)

| URL                        | Descripción                                         |
| -------------------------- | --------------------------------------------------- |
| `/`                        | Landing page — entrada principal para participantes |
| `/encuesta/consentimiento` | Inicio de la encuesta                               |

### Panel de administración

| URL                           | Descripción                  | Rol requerido  |
| ----------------------------- | ---------------------------- | -------------- |
| `/auth/login`                 | Inicio de sesión             | —              |
| `/auth/logout`                | Cerrar sesión                | —              |
| `/auth/reset`                 | Recuperar contraseña         | —              |
| `/admin`                      | Dashboard con estadísticas   | viewer / admin |
| `/admin/respuestas`           | Tabla paginada de respuestas | viewer / admin |
| `/admin/exportar/csv`         | Exportar datos en CSV        | viewer / admin |
| `/admin/usuarios`             | Gestión de usuarios          | admin          |
| `/admin/usuarios/crear`       | Crear nuevo usuario          | admin          |
| `/admin/usuarios/<id>/editar` | Editar usuario               | admin          |

---

## Modelo de datos

### Tablas de la encuesta

| Tabla                   | Descripción                                                       |
| ----------------------- | ----------------------------------------------------------------- |
| `consentimiento_log`    | Registro legal de aceptación (IP anonimizada, timestamp, versión) |
| `participante`          | Datos demográficos: edad, género, ciudad, departamento, educación |
| `habitos_digitales`     | Redes usadas, datos compartidos, conciencia sobre privacidad      |
| `consecuencias_vividas` | Experiencias negativas, impacto emocional, social y laboral       |

### Tabla de usuarios del sistema

| Campo                    | Tipo     | Descripción                         |
| ------------------------ | -------- | ----------------------------------- |
| `username`               | String   | Nombre de usuario único             |
| `fullname`               | String   | Nombre completo                     |
| `email`                  | String   | Correo único, usado para login      |
| `password_hash`          | String   | Contraseña hasheada (werkzeug)      |
| `role`                   | String   | `admin` o `viewer`                  |
| `is_active`              | Boolean  | Permite desactivar sin eliminar     |
| `reset_token`            | String   | Token de recuperación de contraseña |
| `reset_token_expires_at` | DateTime | Expiración del token (1 hora)       |

---

## Roles del sistema

| Rol      | Dashboard | Respuestas | Exportar | Usuarios |
| -------- | --------- | ---------- | -------- | -------- |
| `admin`  | si        | si         | si       | si       |
| `viewer` | si        | si         | si       | no       |

---

## Exportación de datos

### CSV (desde el panel)

Disponible en `/admin/exportar/csv` — descarga inmediata con todas las respuestas completas.

### Excel (script local)

Genera un `.xlsx` con 3 hojas:

- **Resumen** — métricas clave para el investigador
- **Datos crudos** — una fila por participante (compatible con SPSS, R, Excel)
- **Frecuencias** — tablas de distribución por variable

---

## Cumplimiento legal

- **Ley 1581 de 2012** — Protección de datos personales (Colombia)
- **Decreto 1377 de 2013** — Reglamentación del habeas data
- IPs anonimizadas antes de almacenarse (solo primeros 3 octetos)
- Consentimiento explícito registrado con timestamp antes de cualquier recolección
- Cookies diferenciadas: funcionales (necesarias) vs. analíticas (opcionales)
- Contraseñas hasheadas con `werkzeug.security` (PBKDF2-SHA256)
- Tokens de recuperación de contraseña con expiración de 1 hora

---

## Tecnologías

| Componente          | Tecnología                             |
| ------------------- | -------------------------------------- |
| Backend             | Python 3.12 + Flask 3.0                |
| Base de datos       | PostgreSQL + SQLAlchemy ORM            |
| Migraciones         | Flask-Migrate (Alembic)                |
| Formularios         | Flask-WTF + WTForms                    |
| Autenticación       | Sesiones Flask + werkzeug hashing      |
| Email               | smtplib nativo + Gmail SMTP            |
| Servidor producción | Gunicorn                               |
| Hosting             | Railway                                |
| Exportación         | openpyxl (Excel) + csv (nativo)        |
| Frontend            | HTML5 + CSS3 (sin frameworks externos) |
