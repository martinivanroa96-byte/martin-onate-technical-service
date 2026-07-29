from html import escape

from reportlab.lib.styles import ParagraphStyle
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


ANCHO_CONTENIDO = 168 * mm


ESTILO_TEXTO_EXTENSO = ParagraphStyle(
    name="TextoTecnicoExtenso",
    parent=ESTILO_TEXTO_NORMAL,
    leftIndent=10,
    rightIndent=10,
    firstLineIndent=0,
    spaceBefore=10,
    spaceAfter=10,
    leading=16,
    backColor=GRIS_FONDO,
    borderColor=GRIS_BORDE,
    borderWidth=0.7,
    borderPadding=10,
    splitLongWords=True,
    allowWidows=1,
    allowOrphans=1,
)


def preparar_texto(contenido):
    """
    Prepara el texto ingresado por el usuario para incluirlo
    de forma segura dentro del PDF.

    Conserva los saltos de línea y evita que caracteres como
    <, > o & sean interpretados como etiquetas de ReportLab.
    """
    if contenido is None:
        contenido = ""

    texto = str(contenido).strip()

    if texto == "":
        texto = "Sin información registrada."

    texto_seguro = escape(texto)

    return texto_seguro.replace("\n", "<br/>")


def crear_titulo_bloque(titulo):
    titulo_tabla = Table(
        [
            [
                Paragraph(
                    titulo,
                    ESTILO_TITULO_SECCION,
                )
            ]
        ],
        colWidths=[ANCHO_CONTENIDO],
    )

    titulo_tabla.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    AZUL_CARD,
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, -1),
                    BLANCO,
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    # Evita que el título quede solo al final de una página.
    titulo_tabla.keepWithNext = True

    return titulo_tabla


def crear_bloque(titulo, contenido):
    titulo_tabla = crear_titulo_bloque(titulo)

    texto_preparado = preparar_texto(contenido)

    contenido_parrafo = Paragraph(
        texto_preparado,
        ESTILO_TEXTO_EXTENSO,
    )

    return [
        titulo_tabla,
        contenido_parrafo,
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