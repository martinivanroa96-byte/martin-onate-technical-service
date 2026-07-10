from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

from services.pdf.styles import (
    ESTILO_TEXTO_NORMAL,
    GRIS_BORDE,
    GRIS_TEXTO,
)


def crear_seccion_firmas(datos):
    nombre_tecnico = str(
        datos.get("nombre_tecnico", "Martín Oñate")
    ).strip() or "Martín Oñate"

    nombre_cliente = str(
        datos.get("cliente", "")
    ).strip() or "Cliente"

    tabla = Table(
        [
            [
                "",
                "",
            ],
            [
                Paragraph(
                    f"<b>{nombre_tecnico}</b><br/>Firma del técnico",
                    ESTILO_TEXTO_NORMAL,
                ),
                Paragraph(
                    f"<b>{nombre_cliente}</b><br/>Firma conforme del cliente",
                    ESTILO_TEXTO_NORMAL,
                ),
            ],
        ],
        colWidths=[
            79 * mm,
            79 * mm,
        ],
        rowHeights=[
            24 * mm,
            None,
        ],
    )

    tabla.setStyle(
        TableStyle(
            [
                ("LINEBELOW", (0, 0), (0, 0), 0.8, GRIS_BORDE),
                ("LINEBELOW", (1, 0), (1, 0), 0.8, GRIS_BORDE),

                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),

                ("TEXTCOLOR", (0, 1), (-1, -1), GRIS_TEXTO),

                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),

                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    return [
        Spacer(1, 18),
        tabla,
        Spacer(1, 8),
    ]