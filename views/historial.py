import os
from datetime import datetime
from pathlib import Path

import flet as ft

from services.orden_service import (
    eliminar_orden,
    listar_ordenes,
)


COLOR_FONDO = "#0B1723"
COLOR_CARD = "#142739"
COLOR_PRIMARIO = "#1F6AA5"
COLOR_VER_DETALLE = "#0E8A5A"
COLOR_EDITAR = "#D98C00"
COLOR_ELIMINAR = "#B3261E"
COLOR_LINEA = "#2D6A8A"
COLOR_TEXTO = "#B8C7D1"
COLOR_EXITO = "#8FD694"
COLOR_ERROR = "#FF8A80"


def historial_view(
    page: ft.Page,
    cambiar_vista,
):
    # =====================================================
    # TAMAÑOS RESPONSIVE
    # =====================================================

    ancho_pagina = page.width or 1000
    alto_pagina = page.height or 700

    ancho_contenido = min(
        max(
            ancho_pagina - 30,
            300,
        ),
        950,
    )

    alto_lista = max(
        alto_pagina - 220,
        300,
    )

    # =====================================================
    # SERVICIOS
    # =====================================================

    share_service = ft.Share()

    # =====================================================
    # CONTROLES PRINCIPALES
    # =====================================================

    buscador = ft.TextField(
        label="Buscar",
        hint_text="Patente, cliente u orden",
        prefix_icon=ft.Icons.SEARCH,
        border_color=COLOR_LINEA,
        focused_border_color="#8EC5E8",
    )

    mensaje = ft.Text(
        "",
        color="#8EC5E8",
        size=12,
        selectable=True,
    )

    lista = ft.ListView(
        height=alto_lista,
        spacing=15,
        padding=0,
        auto_scroll=False,
    )

    ordenes = []

    # =====================================================
    # MENSAJES
    # =====================================================

    def mostrar_mensaje(
        texto,
        color="#8EC5E8",
    ):
        mensaje.value = texto
        mensaje.color = color
        page.update()

    def mostrar_snackbar(texto):
        page.show_dialog(
            ft.SnackBar(
                content=ft.Text(texto),
            )
        )

    # =====================================================
    # PLATAFORMA
    # =====================================================

    def es_windows():
        plataforma = str(
            page.platform
        ).lower()

        return (
            "windows" in plataforma
            or os.name == "nt"
        )

    # =====================================================
    # ABRIR O COMPARTIR PDF
    # =====================================================

    async def abrir_o_compartir_pdf(
        ruta,
    ):
        if not ruta:
            mostrar_mensaje(
                "La orden no tiene un PDF registrado.",
                COLOR_ERROR,
            )
            return

        archivo_pdf = Path(ruta)

        if not archivo_pdf.exists():
            mostrar_mensaje(
                (
                    "No se encontró el archivo PDF. "
                    "Puede haber sido eliminado."
                ),
                COLOR_ERROR,
            )
            return

        try:
            if es_windows():
                os.startfile(
                    str(archivo_pdf)
                )

                mostrar_mensaje(
                    "PDF abierto correctamente.",
                    COLOR_EXITO,
                )

                return

            await share_service.share_files(
                [
                    ft.ShareFile.from_path(
                        str(archivo_pdf),
                        name=archivo_pdf.name,
                    )
                ],
                title="Compartir informe técnico",
                subject="Informe técnico de servicio",
                text=(
                    "Informe técnico generado por "
                    "Martín Oñate Technical Service."
                ),
            )

            mostrar_mensaje(
                "Menú para compartir abierto.",
                COLOR_EXITO,
            )

        except Exception as error:
            mostrar_mensaje(
                (
                    "No se pudo abrir o compartir "
                    f"el PDF: {error}"
                ),
                COLOR_ERROR,
            )

    def ejecutar_pdf(ruta):
        page.run_task(
            abrir_o_compartir_pdf,
            ruta,
        )

    # =====================================================
    # FECHA
    # =====================================================

    def formatear_fecha(fecha):
        if not fecha:
            return "Sin fecha"

        try:
            return datetime.fromisoformat(
                str(fecha)
            ).strftime(
                "%d-%m-%Y %H:%M"
            )

        except ValueError:
            return str(fecha)

    # =====================================================
    # ELIMINAR ORDEN
    # =====================================================

    def cerrar_dialogo():
        page.pop_dialog()

    def confirmar_eliminacion(
        codigo_orden,
    ):
        def eliminar_confirmado(e):
            correcto, detalle = eliminar_orden(
                codigo_orden
            )

            cerrar_dialogo()

            mensaje.value = detalle

            if correcto:
                mensaje.color = COLOR_EXITO
                cargar_ordenes()
            else:
                mensaje.color = COLOR_ERROR
                page.update()

        dialogo = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                "Eliminar orden",
                weight=ft.FontWeight.BOLD,
            ),
            content=ft.Text(
                (
                    f"¿Seguro que deseas eliminar "
                    f"{codigo_orden}?\n\n"
                    "Se borrarán sus datos, PDF, "
                    "fotografías y firmas."
                )
            ),
            actions=[
                ft.TextButton(
                    "Cancelar",
                    on_click=lambda e: (
                        cerrar_dialogo()
                    ),
                ),
                ft.ElevatedButton(
                    "Eliminar",
                    bgcolor=COLOR_ELIMINAR,
                    color="white",
                    on_click=eliminar_confirmado,
                ),
            ],
            actions_alignment=(
                ft.MainAxisAlignment.END
            ),
        )

        page.show_dialog(
            dialogo
        )

    # =====================================================
    # TARJETA DE ORDEN
    # =====================================================

    def crear_tarjeta(orden):
        cliente = (
            orden.get("cliente")
            or orden.get("nombre_cliente")
            or "Sin nombre"
        )

        codigo_orden = str(
            orden.get(
                "codigo_orden",
                "",
            )
        )

        patente = str(
            orden.get(
                "patente",
                "",
            )
        ).upper()

        ruta_pdf = orden.get(
            "ruta_pdf",
            "",
        )

        fecha = formatear_fecha(
            orden.get(
                "fecha_informe",
                orden.get(
                    "fecha_guardado",
                    "",
                ),
            )
        )

        texto_boton_pdf = (
            "Abrir PDF"
            if es_windows()
            else "Compartir PDF"
        )

        icono_boton_pdf = (
            ft.Icons.PICTURE_AS_PDF
            if es_windows()
            else ft.Icons.SHARE
        )

        boton_detalle = ft.ElevatedButton(
            "Ver detalle",
            icon=ft.Icons.VISIBILITY,
            bgcolor=COLOR_VER_DETALLE,
            color="white",
            height=50,
            on_click=lambda e, codigo=codigo_orden: (
                cambiar_vista(
                    "detalle_orden",
                    codigo,
                )
            ),
        )

        boton_editar = ft.ElevatedButton(
            "Editar",
            icon=ft.Icons.EDIT,
            bgcolor=COLOR_EDITAR,
            color="white",
            height=50,
            on_click=lambda e, codigo=codigo_orden: (
                cambiar_vista(
                    "editar_orden",
                    codigo,
                )
            ),
        )

        boton_pdf = ft.ElevatedButton(
            texto_boton_pdf,
            icon=icono_boton_pdf,
            bgcolor=COLOR_PRIMARIO,
            color="white",
            height=50,
            disabled=not bool(ruta_pdf),
            on_click=lambda e, ruta=ruta_pdf: (
                ejecutar_pdf(
                    ruta
                )
            ),
        )

        boton_eliminar = ft.ElevatedButton(
            "Eliminar",
            icon=ft.Icons.DELETE,
            bgcolor=COLOR_ELIMINAR,
            color="white",
            height=50,
            on_click=lambda e, codigo=codigo_orden: (
                confirmar_eliminacion(
                    codigo
                )
            ),
        )

        botones = ft.ResponsiveRow(
            spacing=10,
            run_spacing=10,
            controls=[
                ft.Container(
                    col={
                        "xs": 6,
                        "sm": 3,
                    },
                    content=boton_detalle,
                ),
                ft.Container(
                    col={
                        "xs": 6,
                        "sm": 3,
                    },
                    content=boton_editar,
                ),
                ft.Container(
                    col={
                        "xs": 6,
                        "sm": 3,
                    },
                    content=boton_pdf,
                ),
                ft.Container(
                    col={
                        "xs": 6,
                        "sm": 3,
                    },
                    content=boton_eliminar,
                ),
            ],
        )

        return ft.Container(
            bgcolor=COLOR_CARD,
            border_radius=15,
            padding=15,
            content=ft.Column(
                spacing=8,
                controls=[
                    ft.Text(
                        codigo_orden,
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color="white",
                    ),

                    ft.Divider(
                        color=COLOR_LINEA,
                    ),

                    ft.Text(
                        f"Cliente: {cliente}",
                        color="white",
                    ),

                    ft.Text(
                        f"Patente: {patente}",
                        color="white",
                    ),

                    ft.Text(
                        f"Fecha: {fecha}",
                        color=COLOR_TEXTO,
                    ),

                    botones,
                ],
            ),
        )

    # =====================================================
    # MOSTRAR Y CARGAR ÓRDENES
    # =====================================================

    def mostrar(
        ordenes_filtradas,
    ):
        lista.controls.clear()

        if not ordenes_filtradas:
            lista.controls.append(
                ft.Container(
                    bgcolor=COLOR_CARD,
                    border_radius=15,
                    padding=20,
                    content=ft.Text(
                        "No existen órdenes.",
                        color="white",
                    ),
                )
            )

        else:
            for orden in ordenes_filtradas:
                lista.controls.append(
                    crear_tarjeta(
                        orden
                    )
                )

        page.update()

    def cargar_ordenes():
        nonlocal ordenes

        ordenes = listar_ordenes()

        mostrar(
            ordenes
        )

    # =====================================================
    # BUSCADOR
    # =====================================================

    def buscar(e):
        texto = str(
            buscador.value or ""
        ).strip().lower()

        if not texto:
            mostrar(
                ordenes
            )
            return

        resultados = []

        for orden in ordenes:
            cliente = str(
                orden.get(
                    "cliente",
                    orden.get(
                        "nombre_cliente",
                        "",
                    ),
                )
            ).lower()

            patente = str(
                orden.get(
                    "patente",
                    "",
                )
            ).lower()

            codigo = str(
                orden.get(
                    "codigo_orden",
                    "",
                )
            ).lower()

            if (
                texto in cliente
                or texto in patente
                or texto in codigo
            ):
                resultados.append(
                    orden
                )

        mostrar(
            resultados
        )

    buscador.on_change = buscar

    cargar_ordenes()

    # =====================================================
    # INTERFAZ
    # =====================================================

    encabezado = ft.Row(
        alignment=(
            ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        vertical_alignment=(
            ft.CrossAxisAlignment.CENTER
        ),
        controls=[
            ft.Text(
                "Historial de Órdenes",
                size=26,
                weight=ft.FontWeight.BOLD,
                color="white",
                expand=True,
            ),

            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_color="white",
                tooltip="Volver",
                on_click=lambda e: cambiar_vista(
                    "home"
                ),
            ),
        ],
    )

    contenido = ft.Container(
        width=ancho_contenido,
        content=ft.Column(
            spacing=10,
            controls=[
                encabezado,

                ft.Divider(
                    color=COLOR_LINEA,
                ),

                buscador,

                mensaje,

                lista,
            ],
        ),
    )

    return ft.SafeArea(
        content=ft.Container(
            expand=True,
            bgcolor=COLOR_FONDO,
            padding=15,
            alignment=ft.Alignment(
                0,
                -1,
            ),
            content=contenido,
        )
    )