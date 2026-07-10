from datetime import datetime
from pathlib import Path
import shutil


CARPETA_FOTOS = Path("fotos")
TIPOS_VALIDOS = ("antes", "durante", "despues")


def normalizar_codigo_orden(codigo_orden: str) -> str:
    codigo = str(codigo_orden or "").strip()

    if not codigo:
        codigo = datetime.now().strftime("OT-%Y%m%d-%H%M%S")

    caracteres_validos = []

    for caracter in codigo:
        if caracter.isalnum() or caracter in ("-", "_"):
            caracteres_validos.append(caracter)

    codigo_limpio = "".join(caracteres_validos)

    return codigo_limpio or datetime.now().strftime("OT-%Y%m%d-%H%M%S")


def crear_estructura_orden(codigo_orden: str) -> dict:
    codigo = normalizar_codigo_orden(codigo_orden)
    carpeta_orden = CARPETA_FOTOS / codigo

    rutas = {
        "orden": carpeta_orden,
    }

    for tipo in TIPOS_VALIDOS:
        carpeta_tipo = carpeta_orden / tipo
        carpeta_tipo.mkdir(parents=True, exist_ok=True)
        rutas[tipo] = carpeta_tipo

    return rutas


def obtener_siguiente_nombre(carpeta: Path, extension: str = ".jpg") -> str:
    archivos = list(carpeta.glob(f"*{extension}"))
    siguiente_numero = len(archivos) + 1

    return f"{siguiente_numero:03d}{extension}"


def guardar_foto_bytes(
    codigo_orden: str,
    tipo: str,
    contenido: bytes,
    extension: str = ".jpg",
) -> str:
    tipo = str(tipo or "").strip().lower()

    if tipo not in TIPOS_VALIDOS:
        raise ValueError(
            "Tipo de fotografía inválido. Usa: antes, durante o despues."
        )

    if not contenido:
        raise ValueError("La fotografía no contiene datos.")

    if not extension.startswith("."):
        extension = f".{extension}"

    rutas = crear_estructura_orden(codigo_orden)
    carpeta_destino = rutas[tipo]

    nombre_archivo = obtener_siguiente_nombre(
        carpeta_destino,
        extension,
    )

    ruta_destino = carpeta_destino / nombre_archivo
    ruta_destino.write_bytes(contenido)

    return str(ruta_destino)


def copiar_foto_desde_archivo(
    codigo_orden: str,
    tipo: str,
    ruta_origen: str,
) -> str:
    tipo = str(tipo or "").strip().lower()
    origen = Path(ruta_origen)

    if tipo not in TIPOS_VALIDOS:
        raise ValueError(
            "Tipo de fotografía inválido. Usa: antes, durante o despues."
        )

    if not origen.exists() or not origen.is_file():
        raise FileNotFoundError(
            f"No se encontró la imagen seleccionada: {ruta_origen}"
        )

    extension = origen.suffix.lower() or ".jpg"

    rutas = crear_estructura_orden(codigo_orden)
    carpeta_destino = rutas[tipo]

    nombre_archivo = obtener_siguiente_nombre(
        carpeta_destino,
        extension,
    )

    destino = carpeta_destino / nombre_archivo
    shutil.copy2(origen, destino)

    return str(destino)


def listar_fotos(codigo_orden: str) -> dict:
    rutas = crear_estructura_orden(codigo_orden)

    resultado = {}

    for tipo in TIPOS_VALIDOS:
        archivos = sorted(
            archivo
            for archivo in rutas[tipo].iterdir()
            if archivo.is_file()
        )

        resultado[tipo] = [
            str(archivo)
            for archivo in archivos
        ]

    return resultado