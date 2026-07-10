from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib.units import mm
from reportlab.platypus import (
    Image,
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
    ESTILO_TEXTO_NORMAL,
    ESTILO_TITULO_SECCION,
    GRIS_BORDE,
    GRIS_FONDO,
    GRIS_TEXTO,
)


ANCHO_MAX_IMAGEN = 72 * mm
ALTO_MAX_IMAGEN = 48 * mm


def obtener_tamano_proporcional(ruta_imagen):
    with PILImage.open(ruta_imagen) as imagen:
        ancho_original, alto_original = imagen.size

    if ancho_original <= 0 or alto_original <= 0:
        return ANCHO_MAX_IMAGEN, ALTO_MAX_IMAGEN

    escala_ancho = ANCHO_MAX_IMAGEN / ancho_original
    escala_alto = ALTO_MAX_IMAGEN / alto_original
    escala = min(escala_ancho, escala_alto)

    ancho_final = ancho_original * escala
    alto_final = alto_original * escala

    return ancho_final, alto_final


def crear_titulo_fotos():
    titulo = Table(
        [[Paragraph("EVIDENCIA FOTOGRÁFICA", ESTILO_TITULO_SECCION)]],
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


def crear_encabezado_categoria(titulo, cantidad):
    encabezado = Table(
        [
            [
                Paragraph(
                    f"{titulo} ({cantidad})",
                    ESTILO_TITULO_SECCION,
                )
            ]
        ],
        colWidths=[168 * mm],
    )

    encabezado.setStyle(
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

    return encabezado


def crear_celda_foto(ruta, numero):
    ancho, alto = obtener_tamano_proporcional(ruta)

    imagen = Image(
        ruta,
        width=ancho,
        height=alto,
    )

    etiqueta = Paragraph(
        f"<b>Foto {numero}</b>",
        ESTILO_TEXTO_NORMAL,
    )

    return Table(
        [
            [imagen],
            [etiqueta],
        ],
        colWidths=[78 * mm],
    )


def crear_bloque_categoria(titulo, rutas, numero_inicial):
    rutas_validas = []

    for ruta in rutas or []:
        archivo = Path(ruta)

        if archivo.exists() and archivo.is_file():
            rutas_validas.append(str(archivo))

    elementos = [
        crear_encabezado_categoria(
            titulo,
            len(rutas_validas),
        )
    ]

    if not rutas_validas:
        tabla_vacia = Table(
            [
                [
                    Paragraph(
                        "Sin fotografías registradas.",
                        ESTILO_TEXTO_NORMAL,
                    )
                ]
            ],
            colWidths=[168 * mm],
        )

        tabla_vacia.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), GRIS_FONDO),
                    ("BOX", (0, 0), (-1, -1), 0.7, GRIS_BORDE),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

        elementos.extend(
            [
                tabla_vacia,
                Spacer(1, 8),
            ]
        )

        return elementos, numero_inicial

    filas = []
    fila_actual = []
    numero_foto = numero_inicial

    for ruta in rutas_validas:
        fila_actual.append(
            crear_celda_foto(
                ruta,
                numero_foto,
            )
        )

        numero_foto += 1

        if len(fila_actual) == 2:
            filas.append(fila_actual)
            fila_actual = []

    if fila_actual:
        fila_actual.append("")
        filas.append(fila_actual)

    tabla_imagenes = Table(
        filas,
        colWidths=[
            84 * mm,
            84 * mm,
        ],
    )

    tabla_imagenes.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.7, GRIS_BORDE),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, GRIS_BORDE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("TEXTCOLOR", (0, 0), (-1, -1), GRIS_TEXTO),
            ]
        )
    )

    elementos.extend(
        [
            tabla_imagenes,
            Spacer(1, 8),
        ]
    )

    return elementos, numero_foto


def crear_seccion_fotos(datos):
    fotos_antes = datos.get("fotos_antes", []) or []
    fotos_durante = datos.get("fotos_durante", []) or []
    fotos_despues = datos.get("fotos_despues", []) or []

    if not fotos_antes and not fotos_durante and not fotos_despues:
        return []

    elementos = [
        crear_titulo_fotos(),
        Spacer(1, 8),
    ]

    numero_foto = 1

    bloque_antes, numero_foto = crear_bloque_categoria(
        "ANTES",
        fotos_antes,
        numero_foto,
    )
    elementos.extend(bloque_antes)

    bloque_durante, numero_foto = crear_bloque_categoria(
        "DURANTE",
        fotos_durante,
        numero_foto,
    )
    elementos.extend(bloque_durante)

    bloque_despues, numero_foto = crear_bloque_categoria(
        "DESPUÉS",
        fotos_despues,
        numero_foto,
    )
    elementos.extend(bloque_despues)

    elementos.append(Spacer(1, 12))

    return elementos