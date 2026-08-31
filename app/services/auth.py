from datetime import date
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.core.database import ejecutar_sp, ejecutar_sp_commit
from app.core.security import hasher, comparar_hash, crear_token_acceso
from app.externalservices.msjresend import enviar_correo
from app.schemas.auth import LoginReq, SolicitudUsuarioReq, ConfirmaRegistroReq
from app.utils.codesgen import generar_codigo_verificacion

"""aca recordar que crud.auth.py solo es la funcion que manda a llamar los procedimientos almacenados
services los convierte en logica de creacion en db y negocio
endpoints solo llaman a las funciones que hacen toda esta logica
vamos a usar schemas para no andar referenciando el gran cuerpo de datos a cada rato
"""



def login_usuario(datos: LoginReq, db: Session):
    try:
        # 1 Buscar en la tabla de usuarios
        resultados_usuario = ejecutar_sp(db, "sp_ObtenerCredencialUsuario", Login=datos.usuario)
        
        if resultados_usuario:
            credencial = resultados_usuario[0]
            if not comparar_hash(datos.psswd, credencial['HashContrasena']):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Contraseña incorrecta."
                )
            token = crear_token_acceso(data={
                "sub": str(credencial["UsuarioID"]),
                "usuario": credencial["Usuario"],
                "tipo_cuenta": "Usuario"
            })
            return {
                "message": "Inicio de sesión exitoso",
                "usuario": {
                    "usuario_id": credencial["UsuarioID"], # o UsuarioID
                    "usuario": credencial["Usuario"],
                    "tipo_cuenta": "Usuario"
                }
            }, token

        # 2 Si no existe como usuario, buscar en la tabla de empleados
        resultados_empleado = ejecutar_sp(db, "sp_ObtenerCredencialEmpleado", Login=datos.usuario)
        
        if resultados_empleado:
            credencial = resultados_empleado[0]
            if not comparar_hash(datos.psswd, credencial['HashContrasena']):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Contraseña incorrecta."
                )
            token = crear_token_acceso(data={
                "sub": str(credencial["UsuarioID"]),
                "usuario": credencial["Usuario"],
                "tipo_cuenta": "Empleado"
            })
            return {
                "message": "Inicio de sesión exitoso",
                        "usuario": {
                            "usuario_id": credencial["UsuarioID"], # o UsuarioID
                            "usuario": credencial["Usuario"],
                            "tipo_cuenta": "Empleado"
                }
            }, token

        # 3 Si no existe en ninguno
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuario o correo no encontrado en el sistema."
        )

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error BD en consulta de credenciales: {str(e.__dict__.get('orig', e))}"
        )




def solicitud_usuario(db: Session, datos: SolicitudUsuarioReq, minutos_validez: int = 10, max_intentos: int = 5,):
    try:
        hash_password = hasher(datos.password)
        codigo = generar_codigo_verificacion()
        resultado = ejecutar_sp_commit(
        db,
        "sp_CrearSolicitudRegistro",
        Nombres=datos.nombres,
        Apellidos=datos.apellidos,
        FechaNacimiento=datos.fecha_nacimiento,
        Telefono=datos.telefono,
        Correo=datos.correo,
        PaisID=datos.pais_id,
        Usuario=datos.usuario,
        HashContrasena=hash_password,
        Codigo=codigo,
        MinutosValidez=minutos_validez,
        MaxIntentos=max_intentos,
        SolicitudRegistroID=None,  # Parametro OUTPUT en SQL Server
        CodigoRegistroID=None,     # Parametro OUTPUT en SQL Server
    )

        # 3 Validar resultado de BD ANTES de enviar correo
        if not resultado:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pudo crear la solicitud de registro."
            )

        # 4 Enviar correo solo si la inserción en BD fue exitosa
        try:
            enviar_correo(datos.nombres, datos.correo, codigo, "registro")
        except Exception as mail_err:
            print(f"[WARNING] No se pudo enviar el correo a {datos.correo}: {str(mail_err)}")
        res = resultado[0] if isinstance(resultado, list) else resultado
        return {
            "message": "Solicitud de registro creada exitosamente.",
            "data": {
                "solicitud_registro_id": res["SolicitudRegistroID"],
                "codigo_registro_id": res["CodigoRegistroID"]}
        }

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error BD al crear solicitud: {str(e.__dict__.get('orig', e))}"
        )




def verificar_y_completar_registro(datos: ConfirmaRegistroReq, db: Session):
    try:
        # 1. Validar el código de verificación (OTP)
        res_validacion = ejecutar_sp_commit(
            db,
            "sp_ValidarCodigoRegistro",
            Login=datos.usuario,
            Codigo=datos.codigo,
            SolicitudRegistroID=None,  # OUTPUT
            EsValido=None,             # OUTPUT
            IntentosRestantes=None      # OUTPUT
        )

        if not res_validacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario o correo no encontrado."
            )

        validacion = res_validacion[0]

        # 2. Verificar si el código ingresado fue correcto
        if not validacion.get("EsValido"):
            intentos = validacion.get("IntentosRestantes", 0)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Código de verificación incorrecto o expirado. Intentos restantes: {intentos}"
            )

        solicitud_id = validacion.get("SolicitudRegistroID")
        if not solicitud_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se obtuvo una solicitud válida."
            )

        # 3. Migrar/Confirmar la cuenta en la base de datos
        res_confirmacion = ejecutar_sp_commit(
            db,
            "sp_ConfirmarRegistroUsuario",
            SolicitudRegistroID=solicitud_id,
            UsuarioID=None  # OUTPUT
        )

        if not res_confirmacion:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pudo completar el registro de la cuenta."
            )

        confirmacion = res_confirmacion[0]

        return {
            "message": "Registro verificado y usuario creado exitosamente.",
            "data": {
                "usuario_id": confirmacion["UsuarioID"],
                "solicitud_registro_id": solicitud_id
            }
        }

    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error BD al verificar el registro: {str(e.__dict__.get('orig', e))}"
        )
