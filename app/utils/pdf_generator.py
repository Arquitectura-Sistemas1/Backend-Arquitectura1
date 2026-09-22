from typing import Any
from fpdf import FPDF


def generar_pdf_factura(datos_factura: dict[str, Any]) -> bytes:
    """
    Genera un archivo PDF simple de factura en texto usando FPDF y retorna los bytes.
    """
    pdf = FPDF()
    pdf.add_page()

    # Encabezado principal
    pdf.set_font("Helvetica", style="B", size=14)
    pdf.cell(0, 10, text="FACTURA ELECTRÓNICA", new_x="LMARGIN", new_y="NEXT", align="C")
    
    pdf.set_font("Helvetica", size=10)
    pdf.cell(0, 5, text=f"Número de Factura: {datos_factura.get('numero_factura', '')}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, text=f"Referencia de Pago: {datos_factura.get('referencia_externa', '')}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, text=f"Fecha: {datos_factura.get('fecha', '')}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    # Datos del cliente
    pdf.set_font("Helvetica", style="B", size=11)
    pdf.cell(0, 6, text="DATOS DEL CLIENTE", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", size=10)
    pdf.cell(0, 5, text=f"Nombre: {datos_factura.get('nombre_cliente', '')}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, text=f"NIT: {datos_factura.get('nit_cliente', '')}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    # Detalle de productos / ítems
    pdf.set_font("Helvetica", style="B", size=11)
    pdf.cell(0, 6, text="DETALLE DEL PEDIDO", new_x="LMARGIN", new_y="NEXT")
    
    # Encabezado de la tabla de ítems
    pdf.set_font("Helvetica", style="B", size=9)
    pdf.cell(75, 6, text="Producto", border=1)
    pdf.cell(25, 6, text="Tipo", border=1, align="C")
    pdf.cell(30, 6, text="Precio", border=1, align="R")
    pdf.cell(30, 6, text="Descuento", border=1, align="R")
    pdf.cell(30, 6, text="Subtotal", border=1, align="R", new_x="LMARGIN", new_y="NEXT")

    # Filas de la tabla
    pdf.set_font("Helvetica", size=9)
    items = datos_factura.get("items", [])
    for item in items:
        prod_nombre = str(item.get("Videojuego", "Producto"))[:35]
        tipo = str(item.get("TipoItem", ""))
        precio = f"${float(item.get('Precio', 0)):.2f}"
        desc = f"${float(item.get('Descuento', 0)):.2f}"
        subt = f"${float(item.get('Subtotal', 0)):.2f}"

        pdf.cell(75, 6, text=prod_nombre, border=1)
        pdf.cell(25, 6, text=tipo, border=1, align="C")
        pdf.cell(30, 6, text=precio, border=1, align="R")
        pdf.cell(30, 6, text=desc, border=1, align="R")
        pdf.cell(30, 6, text=subt, border=1, align="R", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(5)

    # Resumen de totales
    pdf.set_font("Helvetica", style="B", size=10)
    subtotal = float(datos_factura.get("subtotal", 0))
    descuento_total = float(datos_factura.get("descuento_total", 0))
    total = float(datos_factura.get("total", 0))

    pdf.cell(0, 6, text=f"Subtotal: ${subtotal:.2f}", new_x="LMARGIN", new_y="NEXT", align="R")
    pdf.cell(0, 6, text=f"Descuento Total: -${descuento_total:.2f}", new_x="LMARGIN", new_y="NEXT", align="R")
    pdf.set_font("Helvetica", style="B", size=11)
    pdf.cell(0, 7, text=f"TOTAL PAGADO: ${total:.2f}", new_x="LMARGIN", new_y="NEXT", align="R")

    return bytes(pdf.output())

