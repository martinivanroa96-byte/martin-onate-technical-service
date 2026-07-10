import flet as ft
from datetime import datetime

from services.orden_service import listar_ordenes


COLOR_FONDO = "#0B1723"
COLOR_CARD = "#142739"
COLOR_PRIMARIO = "#1F6AA5"
COLOR_SECUNDARIO = "#24384A"
COLOR_LINEA = "#2D6A8A"
COLOR_TEXTO_SECUNDARIO = "#B8C7D1"


def home_view(page: ft.Page, cambiar_vista):
    fecha = datetime.now().strftime("%d-%m-%Y")

    ordenes = listar_ordenes()
    total_ordenes = len(ordenes)

    clientes = {
        str(orden.get("cliente", "")).strip().lower()
        for orden in ordenes
        if str(orden.get("cliente", "")).strip()
    }

    vehiculos = {
        str(orden.get("patente", "")).strip().upper()
        for orden in ordenes
        if str(orden.get("patente", "")).strip()
    }

    pendientes = sum(
        1
        for orden in ordenes
        if str(
            orden.get("estado_final", "")
        ).strip().lower()
        in (
            "pendiente",
            "no operativo",
            "operativo con observaciones",
        )
    )

    def menu_button(
        title,
        subtitle,
        active=True,
        action=None,
    ):
        return ft.Container(
            height=72,
            border_radius=18,
            bgcolor=(
                COLOR_PRIMARIO
                if active
                else COLOR_SECUNDARIO
            ),
            padding=16,
            on_click=action if active else None,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        spacing=3,
                        expand=True,
                        controls=[
                            ft.Text(
                                title,
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color="white",
                            ),
                            ft.Text(
                                subtitle,
                                size=12,
                                color=COLOR_TEXTO_SECUNDARIO,
                            ),
                        ],
                    ),
                    ft.Text(
                        ">",
                        size=22,
                        color="white",
                    ),
                ],
            ),
        )

    def indicador(titulo, valor):
        return ft.Container(
            expand=True,
            padding=12,
            border_radius=14,
            bgcolor=COLOR_SECUNDARIO,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=3,
                controls=[
                    ft.Text(
                        str(valor),
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color="white",
                    ),
                    ft.Text(
                        titulo,
                        size=11,
                        color=COLOR_TEXTO_SECUNDARIO,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
            ),
        )

    ancho_contenido = 430

    if page.width:
        ancho_contenido = min(
            max(page.width - 30, 280),
            430,
        )

    contenido_principal = ft.Container(
        width=ancho_contenido,
        padding=22,
        border_radius=24,
        bgcolor=COLOR_CARD,
        content=ft.Column(
            spacing=16,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Image(
                    src="assets/logo.png",
                    width=135,
                    fit=ft.BoxFit.CONTAIN,
                ),

                ft.Text(
                    "Martín Oñate",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color="white",
                    text_align=ft.TextAlign.CENTER,
                ),

                ft.Text(
                    "Technical Service",
                    size=17,
                    color="#8EC5E8",
                    text_align=ft.TextAlign.CENTER,
                ),

                ft.Text(
                    "Servicio técnico automotriz",
                    size=13,
                    color=COLOR_TEXTO_SECUNDARIO,
                    text_align=ft.TextAlign.CENTER,
                ),

                ft.Divider(
                    color=COLOR_LINEA,
                ),

                ft.Row(
                    spacing=8,
                    controls=[
                        indicador(
                            "Órdenes",
                            total_ordenes,
                        ),
                        indicador(
                            "Clientes",
                            len(clientes),
                        ),
                    ],
                ),

                ft.Row(
                    spacing=8,
                    controls=[
                        indicador(
                            "Vehículos",
                            len(vehiculos),
                        ),
                        indicador(
                            "Pendientes",
                            pendientes,
                        ),
                    ],
                ),

                menu_button(
                    "Nuevo Servicio",
                    "Crear informe técnico",
                    True,
                    lambda e: cambiar_vista(
                        "nuevo_servicio"
                    ),
                ),

                menu_button(
                    "Historial",
                    "Informes anteriores",
                    True,
                    lambda e: cambiar_vista(
                        "historial"
                    ),
                ),

                ft.Divider(
                    color=COLOR_LINEA,
                ),

                ft.Text(
                    f"Fecha: {fecha} | Versión 3.1",
                    size=11,
                    color=COLOR_TEXTO_SECUNDARIO,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
        ),
    )

    return ft.SafeArea(
        content=ft.Container(
            expand=True,
            bgcolor=COLOR_FONDO,
            padding=15,
            content=ft.ListView(
                expand=True,
                spacing=0,
                padding=0,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                        controls=[
                            contenido_principal,
                        ],
                    )
                ],
            ),
        )
    )