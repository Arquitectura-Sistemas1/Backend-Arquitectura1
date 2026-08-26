"""Servicio reutilizable para enviar códigos por correo con Resend."""

from typing import Any

import resend

from app.config import get_resend_config


def _validar_datos_obligatorios(
    api_key: str,
    remitente: str,
    destinatario: str,
    codigo: str,
) -> None:
    if not api_key.strip():
        raise ValueError("Falta configurar RESEND_API_KEY.")

    if not remitente.strip():
        raise ValueError("Falta configurar RESEND_FROM_EMAIL.")

    if not destinatario.strip():
        raise ValueError("El correo de destino es obligatorio.")

    if not codigo.strip():
        raise ValueError("El código de verificación es obligatorio.")


def _crear_mensaje(nombre_original: str, codigo: str, tipo: str) -> tuple[str, str, str]:
    nombre = str(nombre_original).strip() or "usuario"

    if tipo == "recuperacion":
        asunto = "Código para restablecer tu contraseña"
        texto = (
            f"Hola {nombre}. Usa este código para restablecer tu contraseña: "
            f"{codigo}. Si no solicitaste este cambio, puedes ignorar este correo."
        )
        titulo = "Restablecimiento de contraseña"
        descripcion = "Recibimos una solicitud para recuperar el acceso a tu cuenta."
    else:
        asunto = "Código de verificación de cuenta"
        texto = (
            f"Hola {nombre}. Usa este código para completar tu registro o verificar "
            f"tu cuenta: {codigo}."
        )
        titulo = "Verificación de cuenta"
        descripcion = (
            "Usa el siguiente código para continuar con el proceso de verificación."
        )

    html = f"""
    <div style="font-family: Arial, sans-serif; color: #222;">
        <h2>{titulo}</h2>
        <p>Hola {nombre},</p>
        <p>{descripcion}</p>
        <p style="font-size: 24px; font-weight: bold; letter-spacing: 4px;">
            {codigo}
        </p>
        <p>Si no solicitaste este correo, no necesitas realizar ninguna acción.</p>
    </div>
    """

    return asunto, texto, html


def enviar_correo(
    nombre_original: str,
    correo_destino: str,
    code: str,
    tipo: str = "registro",
) -> Any:
    """Envía un código por correo usando Resend.

    Parámetros:
        nombre_original: nombre de la persona que recibirá el correo.
        correo_destino: dirección de correo del destinatario.
        code: código que debe mostrarse en el mensaje.
        tipo: define si el mensaje es de registro o recuperación.

    Devuelve:
        La respuesta producida por resend.Emails.send.
    """
    configuracion = get_resend_config()
    api_key = configuracion.api_key.strip()
    codigo = str(code).strip() if code is not None else ""
    destinatario = str(correo_destino).strip() if correo_destino is not None else ""
    remitente = configuracion.from_email.strip()

    _validar_datos_obligatorios(
        api_key=api_key,
        remitente=remitente,
        destinatario=destinatario,
        codigo=codigo,
    )

    asunto, texto, html = _crear_mensaje(
        nombre_original=nombre_original,
        codigo=codigo,
        tipo=tipo,
    )

    resend.api_key = api_key
    params = {
        "from": remitente,
        "to": destinatario,
        "subject": asunto,
        "text": texto,
        "html": html,
    }

    return resend.Emails.send(params)
