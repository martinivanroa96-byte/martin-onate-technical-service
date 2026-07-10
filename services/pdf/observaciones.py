from reportlab.lib.units import mm
from reportlab.platypus import (
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from services.pdf.styles import (
    AZUL_CARD,
    BLANCO,
    ESTILO_TEXTO_NORMAL,
    ESTILO_TITULO_SECCION,
    GRIS_BORDE,
    GRIS_FONDO,
)


def crear_bloque(titulo, contenido):

    titulo_tabla = Table(
        [[Paragraph(titulo, ESTILO_TITULO_SECCION)]],
        colWidths=[168 * mm],
    )

    titulo_tabla.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), AZUL_CARD),
                ("TEXTCOLOR", (0, 0), (-1, -1), BLANCO),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    texto = contenido.strip()

    if texto == "":
        texto = "Sin información registrada."

    contenido_tabla = Table(
        [
            [
                Paragraph(
                    texto.replace("\n", "<br/>"),
                    ESTILO_TEXTO_NORMAL,
                )
            ]
        ],
        colWidths=[168 * mm],
    )

    contenido_tabla.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), GRIS_FONDO),

                ("BOX", (0, 0), (-1, -1), 0.7, GRIS_BORDE),

                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),

                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )

    return [
        titulo_tabla,
        contenido_tabla,
        Spacer(1, 10),
    ]


def crear_seccion_observaciones(datos):

    elementos = []

    observaciones = datos.get(
        "observaciones",
        "",
    )

    recomendaciones = datos.get(
        "recomendacion_adicional",
        "",
    )

    elementos.extend(
        crear_bloque(
            "HALLAZGOS Y OBSERVACIONES",
            observaciones,
        )
    )

    elementos.extend(
        crear_bloque(
            "RECOMENDACIONES",
            recomendaciones,
        )
    )

    return elementos