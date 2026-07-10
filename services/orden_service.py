import json
import os
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any


def obtener_carpeta_base() -> Path:
    """
    En Android utiliza el almacenamiento persistente de la aplicación.
    En Windows utiliza la carpeta local datos/ordenes.
    """
    ruta_flet = os.getenv("FLET_APP_STORAGE_DATA")

    if ruta_flet:
        carpeta_base = Path(ruta_flet) / "ordenes"
    else:
        carpeta_base = Path("datos") / "ordenes"

    carpeta_base.mkdir(parents=True, exist_ok=True)

    return carpeta_base


def normalizar_codigo_orden(codigo_orden: str) -> str:
    codigo = str(codigo_orden or "").strip()

    if not codigo:
        codigo = datetime.now().strftime(
            "OT-%Y%m%d-%H%M%S"
        )

    codigo = re.sub(
        r"[^A-Za-z0-9_-]",
        "",
        codigo,
    )

    return codigo or datetime.now().strftime(
        "OT-%Y%m%d-%H%M%S"
    )


def crear_estructura_orden(
    codigo_orden: str,
) -> dict[str, Path]:
    codigo = normalizar_codigo_orden(
        codigo_orden
    )

    carpeta_orden = obtener_carpeta_base() / codigo

    rutas = {
        "orden": carpeta_orden,
        "fotos": carpeta_orden / "fotos",
        "antes": carpeta_orden / "fotos" / "antes",
        "durante": carpeta_orden / "fotos" / "durante",
        "despues": carpeta_orden / "fotos" / "despues",
        "firmas": carpeta_orden / "firmas",
        "pdf": carpeta_orden / "pdf",
    }

    for ruta in rutas.values():
        ruta.mkdir(
            parents=True,
            exist_ok=True,
        )

    return rutas


def convertir_a_json(valor: Any):
    if isinstance(valor, Path):
        return str(valor)

    if isinstance(valor, list):
        return [
            convertir_a_json(elemento)
            for elemento in valor
        ]

    if isinstance(valor, dict):
        return {
            clave: convertir_a_json(contenido)
            for clave, contenido in valor.items()
        }

    return valor


def guardar_datos_orden(
    codigo_orden: str,
    datos: dict,
) -> str:
    rutas = crear_estructura_orden(
        codigo_orden
    )

    datos_guardar = dict(datos)

    datos_guardar["codigo_orden"] = (
        normalizar_codigo_orden(
            codigo_orden
        )
    )

    datos_guardar["fecha_guardado"] = (
        datetime.now().isoformat(
            timespec="seconds"
        )
    )

    ruta_json = (
        rutas["orden"]
        / "datos.json"
    )

    with ruta_json.open(
        "w",
        encoding="utf-8",
    ) as archivo:
        json.dump(
            convertir_a_json(datos_guardar),
            archivo,
            ensure_ascii=False,
            indent=4,
        )

    return str(ruta_json)


def cargar_datos_orden(
    codigo_orden: str,
) -> dict | None:
    codigo = normalizar_codigo_orden(
        codigo_orden
    )

    ruta_json = (
        obtener_carpeta_base()
        / codigo
        / "datos.json"
    )

    if not ruta_json.exists():
        return None

    try:
        with ruta_json.open(
            "r",
            encoding="utf-8",
        ) as archivo:
            return json.load(archivo)

    except (OSError, json.JSONDecodeError):
        return None


def listar_ordenes() -> list[dict]:
    carpeta_base = obtener_carpeta_base()
    ordenes = []

    for carpeta in sorted(
        carpeta_base.iterdir(),
        reverse=True,
    ):
        if not carpeta.is_dir():
            continue

        ruta_json = carpeta / "datos.json"

        if not ruta_json.exists():
            continue

        try:
            with ruta_json.open(
                "r",
                encoding="utf-8",
            ) as archivo:
                ordenes.append(
                    json.load(archivo)
                )

        except (OSError, json.JSONDecodeError):
            continue

    return ordenes


def eliminar_orden(
    codigo_orden: str,
) -> tuple[bool, str]:
    """
    Elimina la carpeta completa de una orden:
    datos, PDF, fotografías y firmas.
    """
    codigo = normalizar_codigo_orden(
        codigo_orden
    )

    carpeta_orden = (
        obtener_carpeta_base()
        / codigo
    )

    if not carpeta_orden.exists():
        return (
            False,
            "La orden no existe o ya fue eliminada.",
        )

    if not carpeta_orden.is_dir():
        return (
            False,
            "La ruta de la orden no es válida.",
        )

    errores = []

    try:
        for raiz, carpetas, archivos in os.walk(
            carpeta_orden,
            topdown=False,
        ):
            for nombre_archivo in archivos:
                ruta_archivo = Path(raiz) / nombre_archivo

                try:
                    os.chmod(
                        ruta_archivo,
                        0o777,
                    )

                    ruta_archivo.unlink()

                except OSError as error:
                    errores.append(
                        f"{ruta_archivo}: {error}"
                    )

            for nombre_carpeta in carpetas:
                ruta_carpeta = Path(raiz) / nombre_carpeta

                try:
                    os.chmod(
                        ruta_carpeta,
                        0o777,
                    )

                    ruta_carpeta.rmdir()

                except OSError as error:
                    errores.append(
                        f"{ruta_carpeta}: {error}"
                    )

        os.chmod(
            carpeta_orden,
            0o777,
        )

        carpeta_orden.rmdir()

        return (
            True,
            f"Orden {codigo} eliminada correctamente.",
        )

    except OSError as error:
        errores.append(
            f"{carpeta_orden}: {error}"
        )

    detalle_error = errores[-1] if errores else "Error desconocido."

    return (
        False,
        (
            "No se pudo eliminar completamente la orden. "
            f"Detalle: {detalle_error}"
        ),
    )