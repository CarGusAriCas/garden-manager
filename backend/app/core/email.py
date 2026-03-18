"""
Cliente de email para GardenManager.
Usa Mailtrap en desarrollo y Gmail en producción.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings


def send_email(to: str, subject: str, html_content: str) -> bool:
    """Envía un email via SMTP."""
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = f"{settings.mail_from_name} <{settings.mail_from}>"
        msg["To"]      = to

        msg.attach(MIMEText(html_content, "html"))

        with smtplib.SMTP(settings.mail_server, settings.mail_port) as server:
            server.starttls()
            server.login(settings.mail_username, settings.mail_password)
            server.sendmail(settings.mail_from, to, msg.as_string())

        return True
    except Exception as e:
        print(f"❌ Error enviando email: {type(e).__name__}: {e}")
        return False


def send_activation_email(to: str, nombre: str, token: str) -> bool:
    """
    Envía email de activación con link para crear contraseña.

    Args:
        to: Email del nuevo usuario
        nombre: Nombre del empleado
        token: Token JWT de activación (24h)

    Returns:
        True si se envió correctamente
    """
    activation_url = f"{settings.frontend_url}?activate={token}"

    html = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">

        <div style="background: #1B4332; padding: 20px; border-radius: 8px; text-align: center;">
            <h1 style="color: white; margin: 0;">🌿 GardenManager</h1>
        </div>

        <div style="padding: 30px 0;">
            <h2>Hola {nombre},</h2>
            <p>Tu cuenta en GardenManager ha sido creada.</p>
            <p>Haz clic en el botón para activar tu cuenta y crear tu contraseña:</p>

            <div style="text-align: center; margin: 30px 0;">
                <a href="{activation_url}"
                   style="background: #2D6A4F; color: white; padding: 14px 28px;
                          text-decoration: none; border-radius: 6px; font-size: 16px;">
                    ✅ Activar mi cuenta
                </a>
            </div>

            <p style="color: #666; font-size: 14px;">
                Este enlace expira en 24 horas.<br>
                Si no esperabas este email, ignóralo.
            </p>
        </div>

        <div style="border-top: 1px solid #eee; padding-top: 20px;
                    color: #999; font-size: 12px; text-align: center;">
            GardenManager · Sistema de gestión de jardinería
        </div>

    </body>
    </html>
    """
    return send_email(to, "Activa tu cuenta en GardenManager", html)


def send_password_reset_email(to: str, nombre: str, token: str) -> bool:
    """
    Envía email para resetear contraseña.
    """
    reset_url = f"{settings.frontend_url}?reset={token}"

    html = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">

        <div style="background: #1B4332; padding: 20px; border-radius: 8px; text-align: center;">
            <h1 style="color: white; margin: 0;">🌿 GardenManager</h1>
        </div>

        <div style="padding: 30px 0;">
            <h2>Hola {nombre},</h2>
            <p>Hemos recibido una solicitud para restablecer tu contraseña.</p>

            <div style="text-align: center; margin: 30px 0;">
                <a href="{reset_url}"
                   style="background: #2D6A4F; color: white; padding: 14px 28px;
                          text-decoration: none; border-radius: 6px; font-size: 16px;">
                    🔑 Restablecer contraseña
                </a>
            </div>

            <p style="color: #666; font-size: 14px;">
                Este enlace expira en 24 horas.<br>
                Si no solicitaste este cambio, ignora este email.
            </p>
        </div>

        <div style="border-top: 1px solid #eee; padding-top: 20px;
                    color: #999; font-size: 12px; text-align: center;">
            GardenManager · Sistema de gestión de jardinería
        </div>

    </body>
    </html>
    """
    return send_email(to, "Restablece tu contraseña en GardenManager", html)