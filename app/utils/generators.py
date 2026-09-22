import uuid
from datetime import datetime


def generar_referencia_externa() -> str:
    """Genera una referencia externa única para la transacción de pago."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_str = uuid.uuid4().hex[:6].upper()
    return f"REF-{timestamp}-{random_str}"


def generar_numero_factura() -> str:
    """Genera un número de factura único."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_str = uuid.uuid4().hex[:6].upper()
    return f"FAC-{timestamp}-{random_str}"


def generar_sku(titulo: str, plataforma: str, region: str, secuencia: int = 1) -> str:
    """
    Genera un SKU en formato TITULO-PLATAFORMA-REGION.
    Si secuencia > 1, añade un sufijo numérico para diferenciar las distintas ofertas del videojuego.
    Ejemplo: NEBULA-PC-LATAM, NEBULA-PC-LATAM-002.
    """
    import re
    palabras = [w for w in re.split(r'[^A-Za-z0-9]+', titulo or "") if w]
    t = palabras[0].upper() if palabras else "GAME"
    
    p_clean = re.sub(r'[^A-Z0-9]+', '', (plataforma or "GEN").upper())
    r_clean = re.sub(r'[^A-Z0-9]+', '', (region or "GLOBAL").upper())

    base = f"{t}-{p_clean}-{r_clean}"
    if secuencia > 1:
        return f"{base}-{secuencia:03d}"
    return base


def generar_codigo_licencia(secuencia: int = 1) -> str:
    """
    Genera un código de licencia en formato PROD-KEY-XXX.
    Ejemplo: PROD-KEY-001, PROD-KEY-002.
    """
    return f"PROD-KEY-{secuencia:03d}"



