from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet


# =========================================================
# COLORES CORPORATIVOS
# =========================================================

AZUL_OSCURO = colors.HexColor("#0B1723")
AZUL_CARD = colors.HexColor("#142739")
AZUL_PRINCIPAL = colors.HexColor("#1F6AA5")
AZUL_CLARO = colors.HexColor("#8EC5E8")

GRIS_FONDO = colors.HexColor("#F2F4F6")
GRIS_BORDE = colors.HexColor("#C7D0D9")
GRIS_TEXTO = colors.HexColor("#4A5560")

BLANCO = colors.white
NEGRO = colors.black

VERDE_ESTADO = colors.HexColor("#2E8B57")
AMARILLO_ESTADO = colors.HexColor("#D99A00")
NARANJO_ESTADO = colors.HexColor("#D96C00")
ROJO_ESTADO = colors.HexColor("#B3261E")


# =========================================================
# TAMAÑOS GENERALES
# =========================================================

MARGEN_IZQUIERDO = 36
MARGEN_DERECHO = 36
MARGEN_SUPERIOR = 36
MARGEN_INFERIOR = 42

ESPACIO_SECCION = 12
ESPACIO_INTERNO = 8


# =========================================================
# ESTILOS DE TEXTO
# =========================================================

_estilos_base = getSampleStyleSheet()


ESTILO_TITULO_EMPRESA = ParagraphStyle(
    name="TituloEmpresa",
    parent=_estilos_base["Heading1"],
    fontName="Helvetica-Bold",
    fontSize=20,
    leading=23,
    textColor=BLANCO,
    alignment=TA_LEFT,
    spaceAfter=2,
)


ESTILO_SUBTITULO_EMPRESA = ParagraphStyle(
    name="SubtituloEmpresa",
    parent=_estilos_base["Normal"],
    fontName="Helvetica",
    fontSize=11,
    leading=14,
    textColor=AZUL_CLARO,
    alignment=TA_LEFT,
)


ESTILO_TITULO_DOCUMENTO = ParagraphStyle(
    name="TituloDocumento",
    parent=_estilos_base["Heading1"],
    fontName="Helvetica-Bold",
    fontSize=15,
    leading=18,
    textColor=BLANCO,
    alignment=TA_LEFT,
)


ESTILO_TITULO_SECCION = ParagraphStyle(
    name="TituloSeccion",
    parent=_estilos_base["Heading2"],
    fontName="Helvetica-Bold",
    fontSize=11,
    leading=14,
    textColor=BLANCO,
    alignment=TA_LEFT,
)


ESTILO_ETIQUETA = ParagraphStyle(
    name="Etiqueta",
    parent=_estilos_base["Normal"],
    fontName="Helvetica-Bold",
    fontSize=9,
    leading=12,
    textColor=AZUL_OSCURO,
)


ESTILO_VALOR = ParagraphStyle(
    name="Valor",
    parent=_estilos_base["Normal"],
    fontName="Helvetica",
    fontSize=9,
    leading=12,
    textColor=NEGRO,
)


ESTILO_TEXTO_NORMAL = ParagraphStyle(
    name="TextoNormal",
    parent=_estilos_base["Normal"],
    fontName="Helvetica",
    fontSize=9.5,
    leading=13,
    textColor=NEGRO,
    alignment=TA_LEFT,
)


ESTILO_ITEM = ParagraphStyle(
    name="Item",
    parent=ESTILO_TEXTO_NORMAL,
    leftIndent=10,
    firstLineIndent=-7,
    bulletIndent=0,
    spaceAfter=3,
)


ESTILO_ESTADO = ParagraphStyle(
    name="Estado",
    parent=_estilos_base["Normal"],
    fontName="Helvetica-Bold",
    fontSize=12,
    leading=15,
    textColor=NEGRO,
    alignment=TA_CENTER,
)


ESTILO_PIE_PAGINA = ParagraphStyle(
    name="PiePagina",
    parent=_estilos_base["Normal"],
    fontName="Helvetica",
    fontSize=7.5,
    leading=9,
    textColor=GRIS_TEXTO,
    alignment=TA_CENTER,
)


ESTILO_CODIGO_ORDEN = ParagraphStyle(
    name="CodigoOrden",
    parent=_estilos_base["Normal"],
    fontName="Helvetica-Bold",
    fontSize=9,
    leading=12,
    textColor=BLANCO,
    alignment=TA_LEFT,
)