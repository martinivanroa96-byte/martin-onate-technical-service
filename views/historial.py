import os
from datetime import datetime

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


def historial_view(page: ft.Page, cambiar_vista):
    # =====================================================
    # TAMAÑOS RESPONSIVE
    # =====================================================

    ancho_pagina = page.width or 1000
    alto_pagina = page.height or 700

    ancho_contenido = min(
        max(ancho_pagina - 30, 300),
        950,
    )

    # Espacio reservado para título, buscador, mensaje y márgenes.
    alto_lista = max(
        alto_pagina - 220,
        300,
    )

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
    )

    # La altura explícita es lo que asegura el scroll.
    lista = ft.ListView(
        height=alto_lista,
        spacing=15,
        padding=0,
        auto_scroll=False,
    )

    ordenes = []

    # =====================================================
    # ABRIR PDF
    # =====================================================

    def abrir_pdf(ruta):
        if not ruta:
            mensaje.value = "La orden no tiene un PDF registrado."
            page.update()
            return

        if not os.path.exists(ruta):
            mensaje.value = "No se encontró el archivo PDF."
            page.update()
            return

        try:
            if os.name == "nt":
                os.startfile(ruta)
            else:
                mensaje.value = (
                    "La apertura del PDF en Android se configurará "
                    "durante la prueba móvil."
                )
                page.update()

        except OSError as error:
            mensaje.value = f"No se pudo abrir el PDF: {error}"
            page.update()

    # =====================================================
    # FECHA
    # =====================================================

    def formatear_fecha(fecha):
        if not fecha:
            return "Sin fecha"

        try:
            return datetime.fromisoformat(
                str(fecha)
            ).strftime("%d-%m-%Y %H:%M")

        except ValueError:
            return str(fecha)

    # =====================================================
    # ELIMINAR ORDEN
    # =====================================================

    def cerrar_dialogo():
        page.pop_dialog()

    def confirmar_eliminacion(codigo_orden):
        def eliminar_confirmado(e):
            correcto, detalle = eliminar_orden(
                codigo_orden
            )

            cerrar_dialogo()
            mensaje.value = detalle

            if correcto:
                cargar_ordenes()
            else:
                page.update()

        dialogo = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                "Eliminar orden",
                weight=ft.FontWeight.BOLD,
            ),
            content=ft.Text(
                (
                    f"¿Seguro que deseas eliminar {codigo_orden}?\n\n"
                    "Se borrarán sus datos, PDF, fotografías y firmas."
                )
            ),
            actions=[
                ft.TextButton(
                    "Cancelar",
                    on_click=lambda e: cerrar_dialogo(),
                ),
                ft.ElevatedButton(
                    "Eliminar",
                    bgcolor=COLOR_ELIMINAR,
                    color="white",
                    on_click=eliminar_confirmado,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.show_dialog(dialogo)

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
            orden.get("codigo_orden", "")
        )

        patente = str(
            orden.get("patente", "")
        ).upper()

        ruta_pdf = orden.get(
            "ruta_pdf",
            "",
        )

        fecha = formatear_fecha(
            orden.get(
                "fecha_informe",
                orden.get("fecha_guardado", ""),
            )
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

                    ft.Row(
                        wrap=True,
                        spacing=10,
                        run_spacing=10,
                        controls=[
                            ft.ElevatedButton(
                                "Ver detalle",
                                icon=ft.Icons.VISIBILITY,
                                bgcolor=COLOR_VER_DETALLE,
                                color="white",
                                on_click=lambda e, codigo=codigo_orden: (
                                    cambiar_vista(
                                        "detalle_orden",
                                        codigo,
                                    )
                                ),
                            ),

                            ft.ElevatedButton(
                                "Editar",
                                icon=ft.Icons.EDIT,
                                bgcolor=COLOR_EDITAR,
                                color="white",
                                on_click=lambda e, codigo=codigo_orden: (
                                    cambiar_vista(
                                        "editar_orden",
                                        codigo,
                                    )
                                ),
                            ),

                            ft.ElevatedButton(
                                "Abrir PDF",
                                icon=ft.Icons.PICTURE_AS_PDF,
                                bgcolor=COLOR_PRIMARIO,
                                color="white",
                                on_click=lambda e, ruta=ruta_pdf: (
                                    abrir_pdf(ruta)
                                ),
                            ),

                            ft.ElevatedButton(
                                "Eliminar",
                                icon=ft.Icons.DELETE,
                                bgcolor=COLOR_ELIMINAR,
                                color="white",
                                on_click=lambda e, codigo=codigo_orden: (
                                    confirmar_eliminacion(
                                        codigo
                                    )
                                ),
                            ),
                        ],
                    ),
                ],
            ),
        )

    # =====================================================
    # MOSTRAR Y CARGAR ÓRDENES
    # =====================================================

    def mostrar(ordenes_filtradas):
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
                    crear_tarjeta(orden)
                )

        page.update()

    def cargar_ordenes():
        nonlocal ordenes

        ordenes = listar_ordenes()
        mostrar(ordenes)

    # =====================================================
    # BUSCADOR
    # =====================================================

    def buscar(e):
        texto = str(
            buscador.value or ""
        ).strip().lower()

        if not texto:
            mostrar(ordenes)
            return

        resultados = []

        for orden in ordenes:
            cliente = str(
                orden.get("cliente", "")
            ).lower()

            patente = str(
                orden.get("patente", "")
            ).lower()

            codigo = str(
                orden.get("codigo_orden", "")
            ).lower()

            if (
                texto in cliente
                or texto in patente
                or texto in codigo
            ):
                resultados.append(orden)

        mostrar(resultados)

    buscador.on_change = buscar

    cargar_ordenes()

    # =====================================================
    # INTERFAZ
    # =====================================================

    encabezado = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text(
                "Historial de Órdenes",
                size=26,
                weight=ft.FontWeight.BOLD,
                color="white",
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