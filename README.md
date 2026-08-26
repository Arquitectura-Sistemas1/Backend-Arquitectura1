# Backend-Arquitectura1
Repositorio dedicado para el backend del primer proyecto de arquitectura de sistemas 1

## Integración de Resend en Python

Resend se utiliza en este proyecto para enviar correos con códigos de registro, verificación y recuperación de contraseña. La implementación actual está hecha en Python y se encuentra en `app/externalservices/msjresend.py`.

Este módulo no contiene endpoints de FastAPI. Está pensado para que otro integrante del equipo lo importe posteriormente desde el backend y lo conecte al flujo que corresponda.

Para instalar la dependencia necesaria:

```bash
pip install -r requirements.txt
```

Variables de entorno requeridas:

```env
RESEND_API_KEY=
RESEND_FROM_EMAIL=
```

`RESEND_API_KEY` debe contener la API key real de Resend en el entorno local o de despliegue. `RESEND_FROM_EMAIL` debe contener el remitente autorizado en Resend. Las credenciales reales nunca deben subirse a GitHub; usa `.env` local y conserva `.env.example` solo como referencia.

Ejemplo demostrativo para registro o verificación:

```python
from app.externalservices.msjresend import enviar_correo

respuesta = enviar_correo(
    nombre_original="Usuario",
    correo_destino="usuario@ejemplo.com",
    code="123456",
    tipo="registro",
)
```

Ejemplo demostrativo para recuperación de contraseña:

```python
from app.externalservices.msjresend import enviar_correo

respuesta = enviar_correo(
    nombre_original="Usuario",
    correo_destino="usuario@ejemplo.com",
    code="654321",
    tipo="recuperacion",
)
```

Cuando `tipo` es `"recuperacion"`, el mensaje se redacta para restablecer contraseña. Para `"registro"` o cualquier otro valor, el mensaje se redacta como código de registro o verificación. Estos ejemplos son solo demostrativos y no se ejecutan automáticamente.
