import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def _get_config():
    return {
        "server":   os.getenv("MAIL_SERVER", "smtp.gmail.com"),
        "port":     int(os.getenv("MAIL_PORT", 587)),
        "username": os.getenv("MAIL_USERNAME"),
        "password": os.getenv("MAIL_PASSWORD"),
        "sender":   os.getenv("MAIL_DEFAULT_SENDER"),
    }


def send_email(to: str, subject: str, html_body: str) -> bool:
    
    cfg = _get_config()

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = cfg["sender"]
    msg["To"]      = to
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    try:
        with smtplib.SMTP(cfg["server"], cfg["port"]) as smtp:
            smtp.ehlo()
            smtp.starttls()          
            smtp.login(cfg["username"], cfg["password"])
            smtp.sendmail(cfg["sender"], to, msg.as_string())
        return True
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")
        return False


def send_reset_email(to: str, fullname: str, reset_url: str) -> bool:
    
    subject = "Restablece tu contraseña — Investigación Digital 2026"

    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head><meta charset="UTF-8"></head>
    <body style="margin:0;padding:0;background:#f4f6f9;font-family:'Segoe UI',Arial,sans-serif;">
      <table width="100%" cellpadding="0" cellspacing="0"
             style="background:#f4f6f9;padding:40px 20px;">
        <tr><td align="center">
          <table width="560" cellpadding="0" cellspacing="0"
                 style="background:#ffffff;border-radius:12px;
                        box-shadow:0 4px 24px rgba(26,58,92,.10);
                        overflow:hidden;max-width:560px;">

            <!-- Header -->
            <tr>
              <td style="background:#1a3a5c;padding:28px 40px;">
                <p style="margin:0;color:#e8a020;font-size:13px;
                           font-weight:600;letter-spacing:.06em;
                           text-transform:uppercase;">
                  Investigación Digital · Colombia 2026
                </p>
              </td>
            </tr>

            <!-- Body -->
            <tr>
              <td style="padding:36px 40px;">
                <h1 style="margin:0 0 12px;font-size:22px;
                            color:#1a3a5c;font-weight:600;">
                  Hola, {fullname}
                </h1>
                <p style="margin:0 0 24px;font-size:15px;
                           color:#4a5a6a;line-height:1.7;">
                  Recibimos una solicitud para restablecer la contraseña
                  de tu cuenta. Haz clic en el botón para continuar.
                  Este enlace es válido por <strong>1 hora</strong>.
                </p>

                <!-- Botón -->
                <table cellpadding="0" cellspacing="0">
                  <tr>
                    <td style="background:#1a3a5c;border-radius:8px;">
                      <a href="{reset_url}"
                         style="display:inline-block;padding:14px 32px;
                                color:#ffffff;font-size:15px;
                                font-weight:600;text-decoration:none;">
                        Restablecer contraseña →
                      </a>
                    </td>
                  </tr>
                </table>

                <p style="margin:24px 0 0;font-size:13px;color:#8898aa;line-height:1.6;">
                  Si no solicitaste este cambio, ignora este mensaje.
                  Tu contraseña no cambiará.
                </p>
                <p style="margin:12px 0 0;font-size:12px;color:#b0bec5;">
                  O copia este enlace en tu navegador:<br>
                  <span style="color:#2b5f8e;word-break:break-all;">
                    {reset_url}
                  </span>
                </p>
              </td>
            </tr>

            <!-- Footer -->
            <tr>
              <td style="background:#f4f6f9;padding:20px 40px;
                          border-top:1px solid #dde3ec;">
                <p style="margin:0;font-size:12px;color:#8898aa;text-align:center;">
                  Este es un mensaje automático — no respondas a este correo.
                </p>
              </td>
            </tr>

          </table>
        </td></tr>
      </table>
    </body>
    </html>
    """

    return send_email(to, subject, html)