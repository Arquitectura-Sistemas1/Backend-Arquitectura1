import os
import resend
from app.config import settings


resend.api_key = settings.RESEND_KEY
if not resend.api_key:
    raise ValueError("RESEND_KEY no está configurada.")


def enviar_correo(nombre_original, correo_destino, code, tipo="registro"):
    if tipo == "recuperacion":
        subject = f"Restablecer contraseña: {code} - NexusGames"
        motivo = "restablecer la contraseña de tu cuenta en la plataforma"
        texto_plano = f"¡Hola {nombre_original}! Tu código para restablecer tu contraseña en la plataforma NexusGames es: {code}. Saludos, Desarrolladores de NexusGames."
    else:
        subject = f"Código de verificación: {code} - NexusGames"
        motivo = "ingresar o registrarte en la plataforma"
        texto_plano = f"¡Hola {nombre_original}! Tu código de verificación para la plataforma NexusGames es: {code}. Saludos, Desarrolladores de NexusGames."

    # correo para el Usuario
    params_user = {
        
        "from": '"NexusGames" <noreply@arturomaldonado.space>',
        "to": correo_destino,
        "subject": subject,
        
        "text": texto_plano,
        
        "html": f"""
            <div style="font-family: sans-serif; color: #333; max-width: 600px; margin: 0 auto;">
                <h2>¡Hola, {nombre_original}!</h2>
                <p>Has recibido este correo porque se solicitó un código de verificación para {motivo} <strong>NexusGames</strong>.</p>
                <div style="background-color: #f4f4f4; padding: 15px; text-align: center; font-size: 24px; font-weight: bold; letter-spacing: 5px; margin: 20px 0; border-radius: 5px;">
                    {code}
                </div>
                <p style="font-size: 12px; color: #666;">Este es un correo automático generado por el sistema de soporte del proyecto. Por favor no respondas a este mensaje.</p>
                <hr style="border: 0; border-top: 1px solid #eee;" />
                <p style="font-size: 14px; line-height: 1.3; margin: 0;">
                    Saludos,<br>
                <strong>Equipo Desarrollador.</strong><br>
                    NexusGames
                </p>
            </div>
        """,
    }
    resend.Emails.send(params_user)

    return True
