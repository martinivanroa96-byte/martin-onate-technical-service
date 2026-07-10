from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

from services.pdf.styles import (
    AZUL_CARD,
    BLANCO,
    ESTILO_ETIQUETA,
    ESTILO_TITULO_SECCION,
    ESTILO_VALOR,
    GRIS_BORDE,
    GRIS_FONDO,
)


def crear_seccion_cliente(datos):
    elementos = []

    titulo = Table(
        [[Paragraph("INFORMACIÓN DEL CLIENTE", ESTILO_TITULO_SECCION)]],
        colWidths=[168 * mm],
    )

    titulo.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), AZUL_CARD),
                ("TEXTCOLOR", (0, 0), (-1, -1), BLANCO),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    tabla_datos = Table(
        [
            [
                Paragraph("Nombre", ESTILO_ETIQUETA),
                Paragraph(str(datos.get("cliente", "") or "-"), ESTILO_VALOR),
            ],
            [
                Paragraph("Teléfono", ESTILO_ETIQUETA),
                Paragraph(str(datos.get("telefono", "") or "-"), ESTILO_VALOR),
            ],
            [
                Paragraph("Correo", ESTILO_ETIQUETA),
                Paragraph(str(datos.get("correo", "") or "-"), ESTILO_VALOR),
            ],
        ],
        colWidths=[
            38 * mm,
            130 * mm,
        ],
    )

    tabla_datos.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), GRIS_FONDO),
                ("BOX", (0, 0), (-1, -1), 0.7, GRIS_BORDE),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, GRIS_BORDE),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    elementos.append(titulo)
    elementos.append(tabla_datos)
    elementos.append(Spacer(1, 12))

    return elementos