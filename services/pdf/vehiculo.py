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


def crear_seccion_vehiculo(datos):

    elementos = []

    titulo = Table(
        [[Paragraph("INFORMACIÓN DEL VEHÍCULO", ESTILO_TITULO_SECCION)]],
        colWidths=[168 * mm],
    )

    titulo.setStyle(
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

    tabla = Table(
        [
            [
                Paragraph("<b>Marca</b>", ESTILO_ETIQUETA),
                Paragraph(str(datos.get("marca", "-")), ESTILO_VALOR),

                Paragraph("<b>Modelo</b>", ESTILO_ETIQUETA),
                Paragraph(str(datos.get("modelo", "-")), ESTILO_VALOR),
            ],

            [
                Paragraph("<b>Año</b>", ESTILO_ETIQUETA),
                Paragraph(
                    str(
                        datos.get(
                            "año",
                            datos.get(
                                "anio",
                                datos.get("ano", "-"),
                            ),
                        )
                    ),
                    ESTILO_VALOR,
                ),

                Paragraph("<b>Patente</b>", ESTILO_ETIQUETA),
                Paragraph(str(datos.get("patente", "-")), ESTILO_VALOR),
            ],

            [
                Paragraph("<b>Kilometraje</b>", ESTILO_ETIQUETA),
                Paragraph(str(datos.get("kilometraje", "-")), ESTILO_VALOR),

                Paragraph("<b>VIN / Serie</b>", ESTILO_ETIQUETA),
                Paragraph(str(datos.get("vin", "-")), ESTILO_VALOR),
            ],
        ],
        colWidths=[
            25 * mm,
            59 * mm,
            25 * mm,
            59 * mm,
        ],
    )

    tabla.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), GRIS_FONDO),
                ("BACKGROUND", (2, 0), (2, -1), GRIS_FONDO),

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
    elementos.append(tabla)
    elementos.append(Spacer(1, 12))

    return elementos