import secrets
def generar_codigo_verificacion() -> str:
    codigo_completo = "".join(str(secrets.randbelow(10)) for _ in range(8))
    return codigo_completo
