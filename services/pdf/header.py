import os
from datetime import datetime

from reportlab.lib.units import mm
from reportlab.platypus import Image, Paragraph, Spacer, Table, TableStyle

from services.pdf.styles import (
    AZUL_OSCURO,
    AZUL_PRINCIPAL,
    BLANCO,
    ESTILO_CODIGO_ORDEN,
    ESTILO_SUBTITULO_EMPRESA,
    ESTILO_TITULO_DOCUMENTO,
    ESTILO_TITULO_EMPRESA,
)


LOGO_PATH = "assets/logo.png"


def crear_encabezado(datos):
    fecha_actual = datetime.now()
    codigo_orden = datos.get(
        "codigo_orden",
        fecha_actual.strftime("%Y%m%d_%H%M%S"),
    )

    elementos = []

    logo = Spacer(1, 1)

    if os.path.exists(LOGO_PATH):
        logo = Image(
            LOGO_PATH,
            width=32 * mm,
            height=32 * mm,
        )

    bloque_texto = [
        Paragraph(
            "MARTÍN OÑATE",
            ESTILO_TITULO_EMPRESA,
        ),
        Paragraph(
            "Technical Service",
            ESTILO_SUBTITULO_EMPRESA,
        ),
        Spacer(1, 4),
        Paragraph(
            "INFORME TÉCNICO DE SERVICIO",
            ESTILO_TITULO_DOCUMENTO,
        ),
    ]

    tabla_superior = Table(
        [
            [
                logo,
                bloque_texto,
            ]
        ],
        colWidths=[
            38 * mm,
            130 * mm,
        ],
    )

    tabla_superior.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), AZUL_OSCURO),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )

    tabla_orden = Table(
        [
            [
                Paragraph(
                    f"Fecha: {fecha_actual.strftime('%d-%m-%Y %H:%M')}",
                    ESTILO_CODIGO_ORDEN,
                ),
                Paragraph(
                    f"Orden: {codigo_orden}",
                    ESTILO_CODIGO_ORDEN,
                ),
            ]
        ],
        colWidths=[
            84 * mm,
            84 * mm,
        ],
    )

    tabla_orden.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), AZUL_PRINCIPAL),
                ("TEXTCOLOR", (0, 0), (-1, -1), BLANCO),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    elementos.append(tabla_superior)
    elementos.append(Spacer(1, 6))
    elementos.append(tabla_orden)
    elementos.append(Spacer(1, 12))

    return elementos