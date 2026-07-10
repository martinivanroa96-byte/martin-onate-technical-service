from reportlab.lib.units import mm
from reportlab.platypus import (
    KeepTogether,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from services.pdf.styles import (
    AZUL_CARD,
    AZUL_PRINCIPAL,
    BLANCO,
    ESTILO_ITEM,
    ESTILO_TEXTO_NORMAL,
    ESTILO_TITULO_SECCION,
    GRIS_BORDE,
    GRIS_FONDO,
)


TRABAJOS_POR_CATEGORIA = {
    "Mantención": [
        "Cambio de aceite",
        "Cambio filtro de aceite",
        "Cambio filtro de aire",
        "Cambio filtro combustible",
        "Cambio filtro cabina",
        "Revisión de niveles",
        "Escaneo electrónico",
    ],
    "Diagnóstico": [
        "Escaneo electrónico",
        "Revisión códigos de falla",
        "Prueba de ruta",
        "Medición batería",
        "Revisión sistema de carga",
    ],
    "Frenos": [
        "Cambio de pastillas",
        "Cambio de discos",
        "Rectificado de discos",
        "Cambio líquido de frenos",
        "Limpieza sistema de frenos",
        "Prueba de frenado",
    ],
    "Suspensión": [
        "Cambio amortiguadores",
        "Cambio bieletas",
        "Cambio terminales",
        "Cambio rótulas",
        "Revisión tren delantero",
    ],
    "Electricidad": [
        "Revisión batería",
        "Revisión alternador",
        "Revisión motor de partida",
        "Revisión luces",
        "Revisión fusibles",
    ],
    "Motor": [
        "Cambio correa accesorios",
        "Cambio bomba de agua",
        "Cambio termostato",
        "Cambio empaquetaduras",
        "Regulación de válvulas",
    ],
    "Aire acondicionado": [
        "Carga de gas",
        "Detección de fugas",
        "Cambio compresor",
        "Cambio filtro habitáculo",
        "Limpieza evaporador",
    ],
    "Transmisión": [
        "Cambio aceite caja",
        "Cambio aceite diferencial",
        "Revisión embrague",
        "Cambio kit embrague",
    ],
    "Otro": [
        "Trabajo personalizado",
    ],
}


def obtener_trabajos_agrupados(trabajos_seleccionados):
    grupos = {}

    for categoria, trabajos_categoria in TRABAJOS_POR_CATEGORIA.items():
        seleccionados_categoria = []

        for trabajo in trabajos_categoria:
            if trabajo in trabajos_seleccionados:
                seleccionados_categoria.append(trabajo)

        if seleccionados_categoria:
            grupos[categoria] = seleccionados_categoria

    return grupos


def crear_titulo_seccion():
    titulo = Table(
        [[Paragraph("SERVICIOS REALIZADOS", ESTILO_TITULO_SECCION)]],
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

    return titulo


def crear_tabla_categorias(categorias):
    texto_categorias = " · ".join(categorias)

    tabla = Table(
        [
            [
                Paragraph(
                    "<b>Categorías intervenidas</b>",
                    ESTILO_TEXTO_NORMAL,
                )
            ],
            [
                Paragraph(
                    texto_categorias or "Sin categorías registradas",
                    ESTILO_TEXTO_NORMAL,
                )
            ],
        ],
        colWidths=[168 * mm],
    )

    tabla.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), GRIS_FONDO),
                ("BOX", (0, 0), (-1, -1), 0.7, GRIS_BORDE),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, GRIS_BORDE),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    return tabla


def crear_bloque_categoria(categoria, trabajos):
    titulo_categoria = Table(
        [
            [
                Paragraph(
                    categoria.upper(),
                    ESTILO_TITULO_SECCION,
                )
            ]
        ],
        colWidths=[168 * mm],
    )

    titulo_categoria.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), AZUL_PRINCIPAL),
                ("TEXTCOLOR", (0, 0), (-1, -1), BLANCO),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    filas = []

    for trabajo in trabajos:
        filas.append(
            [
                Paragraph(
                    f"• {trabajo}",
                    ESTILO_ITEM,
                )
            ]
        )

    tabla_trabajos = Table(
        filas,
        colWidths=[168 * mm],
    )

    tabla_trabajos.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.7, GRIS_BORDE),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, GRIS_BORDE),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )

    return KeepTogether(
        [
            titulo_categoria,
            tabla_trabajos,
            Spacer(1, 7),
        ]
    )


def crear_seccion_servicio(datos):
    elementos = []

    trabajos_seleccionados = datos.get("trabajos", []) or []
    trabajos_agrupados = obtener_trabajos_agrupados(
        trabajos_seleccionados
    )

    categorias = list(trabajos_agrupados.keys())

    elementos.append(crear_titulo_seccion())
    elementos.append(
        crear_tabla_categorias(categorias)
    )
    elementos.append(Spacer(1, 9))

    if trabajos_agrupados:
        for categoria, trabajos in trabajos_agrupados.items():
            elementos.append(
                crear_bloque_categoria(
                    categoria,
                    trabajos,
                )
            )
    else:
        tabla_vacia = Table(
            [
                [
                    Paragraph(
                        "No se registraron trabajos realizados.",
                        ESTILO_TEXTO_NORMAL,
                    )
                ]
            ],
            colWidths=[168 * mm],
        )

        tabla_vacia.setStyle(
            TableStyle(
                [
                    ("BOX", (0, 0), (-1, -1), 0.7, GRIS_BORDE),
                    ("BACKGROUND", (0, 0), (-1, -1), GRIS_FONDO),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

        elementos.append(tabla_vacia)

    otro_trabajo = str(
        datos.get("otro_trabajo", "")
    ).strip()

    if otro_trabajo:
        elementos.append(
            crear_bloque_categoria(
                "Trabajo adicional",
                [otro_trabajo],
            )
        )

    elementos.append(Spacer(1, 12))

    return elementos