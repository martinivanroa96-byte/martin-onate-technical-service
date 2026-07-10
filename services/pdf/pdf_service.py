from datetime import datetime
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate

from services.orden_service import (
    crear_estructura_orden,
    guardar_datos_orden,
    normalizar_codigo_orden,
)

from services.pdf.cliente import crear_seccion_cliente
from services.pdf.estado import crear_seccion_estado
from services.pdf.firmas import crear_seccion_firmas
from services.pdf.fotos import crear_seccion_fotos
from services.pdf.header import crear_encabezado
from services.pdf.observaciones import crear_seccion_observaciones
from services.pdf.servicio import crear_seccion_servicio
from services.pdf.styles import (
    GRIS_BORDE,
    GRIS_TEXTO,
    MARGEN_DERECHO,
    MARGEN_INFERIOR,
    MARGEN_IZQUIERDO,
    MARGEN_SUPERIOR,
)
from services.pdf.vehiculo import crear_seccion_vehiculo


def dibujar_pie_pagina(canvas, documento):
    canvas.saveState()

    ancho_pagina, _ = A4

    canvas.setStrokeColor(GRIS_BORDE)
    canvas.setLineWidth(0.5)

    canvas.line(
        MARGEN_IZQUIERDO,
        30,
        ancho_pagina - MARGEN_DERECHO,
        30,
    )

    canvas.setFillColor(GRIS_TEXTO)
    canvas.setFont("Helvetica", 7.5)

    canvas.drawString(
        MARGEN_IZQUIERDO,
        18,
        "Martín Oñate Technical Service · Informe generado digitalmente",
    )

    canvas.drawRightString(
        ancho_pagina - MARGEN_DERECHO,
        18,
        f"Página {documento.page}",
    )

    canvas.restoreState()


def limpiar_patente_para_archivo(patente):
    patente_limpia = str(patente or "").strip().upper()

    patente_limpia = (
        patente_limpia
        .replace(" ", "")
        .replace("-", "")
        .replace("/", "")
        .replace("\\", "")
    )

    return patente_limpia or "SIN_PATENTE"


def generar_informe_pdf(datos):
    fecha_actual = datetime.now()

    codigo_orden = normalizar_codigo_orden(
        datos.get("codigo_orden", "")
    )

    datos["codigo_orden"] = codigo_orden

    # Crea automáticamente toda la estructura de la orden.
    rutas_orden = crear_estructura_orden(codigo_orden)

    patente_archivo = limpiar_patente_para_archivo(
        datos.get("patente", "")
    )

    nombre_pdf = (
        f"{codigo_orden}_{patente_archivo}_informe.pdf"
    )

    ruta_pdf = Path(rutas_orden["pdf"]) / nombre_pdf

    documento = SimpleDocTemplate(
        str(ruta_pdf),
        pagesize=A4,
        rightMargin=MARGEN_DERECHO,
        leftMargin=MARGEN_IZQUIERDO,
        topMargin=MARGEN_SUPERIOR,
        bottomMargin=MARGEN_INFERIOR,
        title="Informe Técnico de Servicio",
        author="Martín Oñate Technical Service",
        subject="Orden de trabajo e informe técnico automotriz",
    )

    contenido = []

    contenido.extend(
        crear_encabezado(datos)
    )

    contenido.extend(
        crear_seccion_cliente(datos)
    )

    contenido.extend(
        crear_seccion_vehiculo(datos)
    )

    contenido.extend(
        crear_seccion_servicio(datos)
    )

    contenido.extend(
        crear_seccion_observaciones(datos)
    )

    contenido.extend(
        crear_seccion_fotos(datos)
    )

    contenido.extend(
        crear_seccion_estado(datos)
    )

    contenido.extend(
        crear_seccion_firmas(datos)
    )

    documento.build(
        contenido,
        onFirstPage=dibujar_pie_pagina,
        onLaterPages=dibujar_pie_pagina,
    )

    # Guardamos en el JSON la ubicación del PDF.
    datos["ruta_pdf"] = str(ruta_pdf)
    datos["fecha_informe"] = fecha_actual.isoformat(
        timespec="seconds"
    )

    guardar_datos_orden(
        codigo_orden,
        datos,
    )

    return str(ruta_pdf)