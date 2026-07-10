from datetime import datetime
import os
import textwrap

from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


INFORMES_DIR = "informes"
LOGO_PATH = "assets/logo.png"

os.makedirs(INFORMES_DIR, exist_ok=True)


def generar_informe_pdf(datos):
    fecha_actual = datetime.now()
    codigo_orden = fecha_actual.strftime("%Y%m%d_%H%M%S")

    patente = str(datos.get("patente", "")).strip().upper()
    patente_archivo = patente.replace(" ", "").replace("-", "") or "SIN_PATENTE"

    nombre_pdf = f"{patente_archivo}_informe_{codigo_orden}.pdf"
    ruta_pdf = os.path.join(INFORMES_DIR, nombre_pdf)

    pdf = canvas.Canvas(ruta_pdf, pagesize=A4)
    ancho_pagina, alto_pagina = A4

    azul_oscuro = (0.043, 0.09, 0.137)
    azul_tarjeta = (0.078, 0.153, 0.224)
    azul_principal = (0.122, 0.416, 0.647)
    gris_texto = (0.25, 0.25, 0.25)
    gris_linea = (0.7, 0.7, 0.7)

    margen_izquierdo = 42
    margen_derecho = 42
    y = alto_pagina - 40
    numero_pagina = 1

    def pie_pagina():
        pdf.setStrokeColorRGB(*gris_linea)
        pdf.line(
            margen_izquierdo,
            38,
            ancho_pagina - margen_derecho,
            38,
        )

        pdf.setFont("Helvetica", 7.5)
        pdf.setFillColorRGB(0.4, 0.4, 0.4)

        pdf.drawString(
            margen_izquierdo,
            24,
            "Martín Oñate Technical Service · Informe generado digitalmente",
        )

        pdf.drawRightString(
            ancho_pagina - margen_derecho,
            24,
            f"Página {numero_pagina}",
        )

    def nueva_pagina():
        nonlocal y, numero_pagina

        pie_pagina()
        pdf.showPage()

        numero_pagina += 1
        y = alto_pagina - 45

    def validar_espacio(espacio_necesario=70):
        if y < espacio_necesario:
            nueva_pagina()

    def escribir(
        texto,
        tamano=10,
        negrita=False,
        x=margen_izquierdo + 12,
        ancho_linea=88,
        salto=15,
    ):
        nonlocal y

        contenido = "" if texto is None else str(texto)
        lineas = textwrap.wrap(
            contenido,
            width=ancho_linea,
            replace_whitespace=False,
        ) or [""]

        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont(
            "Helvetica-Bold" if negrita else "Helvetica",
            tamano,
        )

        for linea in lineas:
            validar_espacio(60)
            pdf.drawString(x, y, linea)
            y -= salto

    def seccion(titulo):
        nonlocal y

        validar_espacio(95)
        y -= 7

        pdf.setFillColorRGB(*azul_tarjeta)
        pdf.roundRect(
            margen_izquierdo,
            y - 7,
            ancho_pagina - margen_izquierdo - margen_derecho,
            27,
            6,
            fill=True,
            stroke=False,
        )

        pdf.setFillColorRGB(1, 1, 1)
        pdf.setFont("Helvetica-Bold", 11.5)
        pdf.drawString(margen_izquierdo + 13, y + 1, titulo)

        y -= 37

    def dato(etiqueta, valor):
        valor_mostrar = str(valor).strip() if valor is not None else ""
        escribir(
            f"{etiqueta}: {valor_mostrar or '-'}",
            ancho_linea=90,
        )

    def item_lista(texto):
        escribir(
            f"• {texto}",
            x=margen_izquierdo + 27,
            ancho_linea=82,
        )

    def encabezado():
        nonlocal y

        pdf.setFillColorRGB(*azul_oscuro)
        pdf.rect(
            0,
            alto_pagina - 118,
            ancho_pagina,
            118,
            fill=True,
            stroke=False,
        )

        if os.path.exists(LOGO_PATH):
            try:
                logo = ImageReader(LOGO_PATH)
                pdf.drawImage(
                    logo,
                    38,
                    alto_pagina - 105,
                    width=82,
                    height=82,
                    preserveAspectRatio=True,
                    mask="auto",
                )
            except Exception:
                pass

        pdf.setFillColorRGB(1, 1, 1)
        pdf.setFont("Helvetica-Bold", 20)
        pdf.drawString(137, alto_pagina - 47, "MARTÍN OÑATE")

        pdf.setFont("Helvetica", 12.5)
        pdf.drawString(137, alto_pagina - 68, "Technical Service")

        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(
            137,
            alto_pagina - 93,
            "INFORME TÉCNICO DE SERVICIO",
        )

        y = alto_pagina - 144

        pdf.setFillColorRGB(*azul_principal)
        pdf.roundRect(
            margen_izquierdo,
            y - 17,
            ancho_pagina - margen_izquierdo - margen_derecho,
            38,
            7,
            fill=True,
            stroke=False,
        )

        pdf.setFillColorRGB(1, 1, 1)
        pdf.setFont("Helvetica-Bold", 10)

        pdf.drawString(
            margen_izquierdo + 13,
            y + 5,
            f"Fecha: {fecha_actual.strftime('%d-%m-%Y %H:%M')}",
        )

        pdf.drawRightString(
            ancho_pagina - margen_derecho - 13,
            y + 5,
            f"Orden: {codigo_orden}",
        )

        y -= 54

    encabezado()

    # Datos del cliente
    seccion("Datos del Cliente")
    dato("Cliente", datos.get("cliente", ""))
    dato("Teléfono", datos.get("telefono", ""))
    dato("Correo", datos.get("correo", ""))

    # Datos del vehículo
    seccion("Datos del Vehículo")
    dato("Marca", datos.get("marca", ""))
    dato("Modelo", datos.get("modelo", ""))
    dato(
        "Año",
        datos.get(
            "anio",
            datos.get("ano", datos.get("año", "")),
        ),
    )
    dato("Patente", datos.get("patente", ""))
    dato("Kilometraje", datos.get("kilometraje", ""))
    dato("VIN / Número de serie", datos.get("vin", ""))

    # Servicio realizado
    seccion("Servicio Realizado")

    tipo_servicio = str(datos.get("tipo_servicio", "")).strip()
    dato(
        "Tipo de servicio",
        tipo_servicio or "No especificado",
    )

    trabajos = datos.get("trabajos", []) or []

    escribir("Trabajos realizados:", negrita=True)

    if trabajos:
        for trabajo in trabajos:
            item_lista(trabajo)
    else:
        item_lista("Sin trabajos seleccionados")

    otro_trabajo = str(datos.get("otro_trabajo", "")).strip()

    if otro_trabajo:
        item_lista(otro_trabajo)

    # Hallazgos
    seccion("Hallazgos y Observaciones")

    hallazgos = datos.get("hallazgos", []) or []
    observaciones = str(datos.get("observaciones", "")).strip()

    if hallazgos:
        for hallazgo in hallazgos:
            item_lista(hallazgo)

    if observaciones:
        escribir(observaciones, ancho_linea=90)

    if not hallazgos and not observaciones:
        escribir("Sin hallazgos u observaciones registrados.")

    # Recomendaciones
    seccion("Recomendaciones")

    recomendaciones = datos.get("recomendaciones", []) or []
    recomendacion_adicional = str(
        datos.get("recomendacion_adicional", "")
    ).strip()

    if recomendaciones:
        for recomendacion in recomendaciones:
            item_lista(recomendacion)

    if recomendacion_adicional:
        escribir(recomendacion_adicional, ancho_linea=90)

    if not recomendaciones and not recomendacion_adicional:
        escribir("Sin recomendaciones registradas.")

    # Estado final
    seccion("Estado Final")

    estado_final = str(
        datos.get("estado_final", "No especificado")
    ).strip()

    escribir(
        estado_final or "No especificado",
        tamano=12,
        negrita=True,
    )

    observacion_estado = str(
        datos.get("observacion_estado", "")
    ).strip()

    if observacion_estado:
        escribir(
            "Observaciones del estado final:",
            negrita=True,
        )
        escribir(
            observacion_estado,
            ancho_linea=90,
        )

    # Firmas
    validar_espacio(145)
    y -= 55

    pdf.setStrokeColorRGB(*gris_texto)
    pdf.setLineWidth(0.8)

    firma_ancho = 190
    firma_tecnico_x = 55
    firma_cliente_x = ancho_pagina - 55 - firma_ancho

    pdf.line(
        firma_tecnico_x,
        y,
        firma_tecnico_x + firma_ancho,
        y,
    )

    pdf.line(
        firma_cliente_x,
        y,
        firma_cliente_x + firma_ancho,
        y,
    )

    y -= 16

    pdf.setFillColorRGB(0, 0, 0)
    pdf.setFont("Helvetica", 9)

    pdf.drawCentredString(
        firma_tecnico_x + firma_ancho / 2,
        y,
        "Firma del técnico",
    )

    pdf.drawCentredString(
        firma_cliente_x + firma_ancho / 2,
        y,
        "Firma conforme del cliente",
    )

    pie_pagina()
    pdf.save()

    return ruta_pdf