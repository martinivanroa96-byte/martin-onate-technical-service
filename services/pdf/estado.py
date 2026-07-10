from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

from services.pdf.styles import (
    AMARILLO_ESTADO,
    AZUL_CARD,
    BLANCO,
    ESTILO_ESTADO,
    ESTILO_TEXTO_NORMAL,
    ESTILO_TITULO_SECCION,
    GRIS_BORDE,
    GRIS_FONDO,
    NARANJO_ESTADO,
    ROJO_ESTADO,
    VERDE_ESTADO,
)


def color_estado(estado):
    estado_normalizado = str(estado or "").strip().lower()

    if estado_normalizado == "operativo":
        return VERDE_ESTADO

    if estado_normalizado == "operativo con observaciones":
        return AMARILLO_ESTADO

    if estado_normalizado == "pendiente":
        return NARANJO_ESTADO

    if estado_normalizado == "no operativo":
        return ROJO_ESTADO

    return AZUL_CARD


def crear_seccion_estado(datos):
    elementos = []

    estado = str(
        datos.get("estado_final", "No especificado")
    ).strip() or "No especificado"

    observacion_estado = str(
        datos.get("observacion_estado", "")
    ).strip()

    titulo = Table(
        [[Paragraph("ESTADO FINAL", ESTILO_TITULO_SECCION)]],
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

    tabla_estado = Table(
        [
            [
                Paragraph(
                    estado.upper(),
                    ESTILO_ESTADO,
                )
            ]
        ],
        colWidths=[168 * mm],
    )

    tabla_estado.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    color_estado(estado),
                ),
                ("TEXTCOLOR", (0, 0), (-1, -1), BLANCO),
                ("BOX", (0, 0), (-1, -1), 0.7, GRIS_BORDE),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 12),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ]
        )
    )

    elementos.append(titulo)
    elementos.append(tabla_estado)

    if observacion_estado:
        tabla_observacion = Table(
            [
                [
                    Paragraph(
                        "<b>Observaciones del estado final</b>",
                        ESTILO_TEXTO_NORMAL,
                    )
                ],
                [
                    Paragraph(
                        observacion_estado.replace("\n", "<br/>"),
                        ESTILO_TEXTO_NORMAL,
                    )
                ],
            ],
            colWidths=[168 * mm],
        )

        tabla_observacion.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), GRIS_FONDO),
                    ("BOX", (0, 0), (-1, -1), 0.7, GRIS_BORDE),
                    ("INNERGRID", (0, 0), (-1, -1), 0.4, GRIS_BORDE),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

        elementos.append(tabla_observacion)

    elementos.append(Spacer(1, 12))

    return elementos