import io
from typing import Any
from PIL import Image, ImageDraw, ImageFont


def generar_imagen_factura(datos_factura: dict[str, Any]) -> bytes:
    """
    Genera una imagen PNG limpia de la factura comercial usando Pillow y retorna los bytes.
    """
    width, height = 750, 950
    image = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Cargar fuentes por defecto
    try:
        font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 22)
        font_header = ImageFont.truetype("DejaVuSans-Bold.ttf", 15)
        font_bold = ImageFont.truetype("DejaVuSans-Bold.ttf", 13)
        font_regular = ImageFont.truetype("DejaVuSans.ttf", 13)
    except Exception:
        font_title = ImageFont.load_default()
        font_header = font_title
        font_bold = font_title
        font_regular = font_title

    # Encabezado principal (Banda Superior)
    draw.rectangle([(0, 0), (width, 75)], fill=(30, 41, 59))
    draw.text((25, 22), "COMPROBANTE DE PAGO / FACTURA", fill=(255, 255, 255), font=font_title)

    y = 95
    # Info de Factura y Referencia
    draw.text((25, y), f"Número de Factura: {datos_factura.get('numero_factura', '')}", fill=(15, 23, 42), font=font_bold)
    y += 24
    draw.text((25, y), f"Referencia Pago: {datos_factura.get('referencia_externa', '')}", fill=(51, 65, 85), font=font_regular)
    y += 22
    draw.text((25, y), f"Fecha: {datos_factura.get('fecha', '')}", fill=(100, 116, 139), font=font_regular)
    y += 35

    # Cuadro Datos Cliente
    draw.rectangle([(25, y), (width - 25, y + 65)], fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.text((40, y + 12), f"Cliente: {datos_factura.get('nombre_cliente', '')}", fill=(15, 23, 42), font=font_bold)
    draw.text((40, y + 36), f"NIT / Cédula: {datos_factura.get('nit_cliente', '')}", fill=(51, 65, 85), font=font_regular)
    y += 85

    # Título Tabla
    draw.text((25, y), "DETALLE DEL PEDIDO", fill=(15, 23, 42), font=font_header)
    y += 28

    # Cabecera Tabla
    draw.rectangle([(25, y), (width - 25, y + 32)], fill=(226, 232, 240))
    draw.text((35, y + 8), "Producto / Juego", fill=(15, 23, 42), font=font_bold)
    draw.text((310, y + 8), "Tipo", fill=(15, 23, 42), font=font_bold)
    draw.text((410, y + 8), "Precio Base", fill=(15, 23, 42), font=font_bold)
    draw.text((520, y + 8), "Descuento", fill=(15, 23, 42), font=font_bold)
    draw.text((630, y + 8), "Subtotal", fill=(15, 23, 42), font=font_bold)
    y += 38

    # Filas de Productos
    items = datos_factura.get("items", [])
    for item in items:
        prod_nombre = str(item.get("Videojuego", "Producto"))[:24]
        tipo = str(item.get("TipoItem", ""))
        precio = f"${float(item.get('Precio', 0)):.2f}"
        desc_val = float(item.get('Descuento', 0))
        desc_str = f"-${desc_val:.2f}" if desc_val > 0 else "$0.00"
        subt = f"${float(item.get('Subtotal', 0)):.2f}"

        draw.text((35, y), prod_nombre, fill=(15, 23, 42), font=font_regular)
        draw.text((310, y), tipo, fill=(51, 65, 85), font=font_regular)
        draw.text((410, y), precio, fill=(51, 65, 85), font=font_regular)
        draw.text((520, y), desc_str, fill=(220, 38, 38) if desc_val > 0 else (51, 65, 85), font=font_regular)
        draw.text((630, y), subt, fill=(15, 23, 42), font=font_bold)
        y += 28
        draw.line([(25, y - 6), (width - 25, y - 6)], fill=(241, 245, 249), width=1)


    y += 25
    # Cuadro Resumen Totales
    subtotal = float(datos_factura.get("subtotal", 0))
    descuento_total = float(datos_factura.get("descuento_total", 0))
    total = float(datos_factura.get("total", 0))
    cupon_codigo = datos_factura.get("cupon_codigo")
    cupon_tipo = datos_factura.get("cupon_tipo")
    cupon_valor = datos_factura.get("cupon_valor")

    draw.text((380, y), f"Subtotal Items: ${subtotal:.2f}", fill=(71, 85, 105), font=font_regular)
    y += 24

    if cupon_codigo:
        simbolo = "%" if str(cupon_tipo).upper() == "PORCENTAJE" else "$"
        valor_str = f"{float(cupon_valor):.0f}" if float(cupon_valor or 0).is_integer() else f"{float(cupon_valor):.2f}"
        linea_desc = f"Cupón [{cupon_codigo}] ({valor_str}{simbolo}): -${descuento_total:.2f}"
    else:
        linea_desc = f"Descuento Cupón: -${descuento_total:.2f}"

    draw.text((380, y), linea_desc, fill=(71, 85, 105), font=font_regular)
    y += 32
    draw.rectangle([(380, y - 6), (width - 25, y + 36)], fill=(30, 41, 59))
    draw.text((400, y + 8), f"TOTAL PAGADO: ${total:.2f}", fill=(255, 255, 255), font=font_bold)


    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format="PNG")
    return img_byte_arr.getvalue()

