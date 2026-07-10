import flet as ft

from services.orden_service import (
    cargar_datos_orden,
    guardar_datos_orden,
)
from services.pdf.pdf_service import generar_informe_pdf


COLOR_FONDO = "#0B1723"
COLOR_CARD = "#142739"
COLOR_PRIMARIO = "#1F6AA5"
COLOR_LINEA = "#2D6A8A"
COLOR_TEXTO = "#B8C7D1"


def editar_orden_view(
    page: ft.Page,
    cambiar_vista,
    codigo_orden,
):
    datos = cargar_datos_orden(codigo_orden) or {}

    cliente = ft.TextField(
        label="Nombre del cliente",
        value=datos.get("cliente", ""),
    )

    telefono = ft.TextField(
        label="Teléfono",
        value=datos.get("telefono", ""),
    )

    correo = ft.TextField(
        label="Correo",
        value=datos.get("correo", ""),
    )

    marca = ft.TextField(
        label="Marca",
        value=datos.get("marca", ""),
    )

    modelo = ft.TextField(
        label="Modelo",
        value=datos.get("modelo", ""),
    )

    anio = ft.TextField(
        label="Año",
        value=datos.get(
            "año",
            datos.get(
                "anio",
                datos.get("ano", ""),
            ),
        ),
    )

    patente = ft.TextField(
        label="Patente",
        value=datos.get("patente", ""),
    )

    kilometraje = ft.TextField(
        label="Kilometraje",
        value=datos.get("kilometraje", ""),
    )

    vin = ft.TextField(
        label="VIN / Número de serie",
        value=datos.get("vin", ""),
    )

    observaciones = ft.TextField(
        label="Observaciones / hallazgos",
        value=datos.get("observaciones", ""),
        multiline=True,
        min_lines=3,
    )

    recomendaciones = ft.TextField(
        label="Recomendaciones",
        value=datos.get(
            "recomendacion_adicional",
            "",
        ),
        multiline=True,
        min_lines=3,
    )

    estado = ft.Dropdown(
        label="Estado final",
        value=datos.get(
            "estado_final",
            "Operativo",
        ),
        options=[
            ft.DropdownOption("Operativo"),
            ft.DropdownOption(
                "Operativo con observaciones"
            ),
            ft.DropdownOption("Pendiente"),
            ft.DropdownOption("No operativo"),
        ],
    )

    observacion_estado = ft.TextField(
        label="Observaciones del estado final",
        value=datos.get(
            "observacion_estado",
            "",
        ),
        multiline=True,
        min_lines=3,
        visible=(
            datos.get("estado_final", "")
            == "Operativo con observaciones"
        ),
    )

    mensaje = ft.Text(
        "",
        color="#8EC5E8",
    )

    def cambiar_estado(e):
        mostrar = (
            estado.value
            == "Operativo con observaciones"
        )

        observacion_estado.visible = mostrar

        if not mostrar:
            observacion_estado.value = ""

        page.update()

    estado.on_select = cambiar_estado

    def tarjeta(titulo, controles):
        return ft.Container(
            bgcolor=COLOR_CARD,
            border_radius=16,
            padding=16,
            margin=ft.Margin(0, 0, 0, 12),
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Text(
                        titulo,
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color="white",
                    ),
                    ft.Divider(
                        color=COLOR_LINEA,
                    ),
                    *controles,
                ],
            ),
        )

    def guardar_cambios(e):
        try:
            datos_actualizados = dict(datos)

            datos_actualizados.update(
                {
                    "codigo_orden": codigo_orden,
                    "cliente": cliente.value or "",
                    "telefono": telefono.value or "",
                    "correo": correo.value or "",
                    "marca": marca.value or "",
                    "modelo": modelo.value or "",
                    "año": anio.value or "",
                    "patente": patente.value or "",
                    "kilometraje": (
                        kilometraje.value or ""
                    ),
                    "vin": vin.value or "",
                    "observaciones": (
                        observaciones.value or ""
                    ),
                    "recomendacion_adicional": (
                        recomendaciones.value or ""
                    ),
                    "estado_final": (
                        estado.value or "Operativo"
                    ),
                    "observacion_estado": (
                        observacion_estado.value or ""
                    ),
                }
            )

            guardar_datos_orden(
                codigo_orden,
                datos_actualizados,
            )

            ruta_pdf = generar_informe_pdf(
                datos_actualizados
            )

            mensaje.value = (
                f"Orden actualizada correctamente: {ruta_pdf}"
            )

            page.snack_bar = ft.SnackBar(
                ft.Text(
                    "Orden actualizada correctamente."
                )
            )
            page.snack_bar.open = True
            page.update()

        except Exception as error:
            mensaje.value = (
                f"No se pudo actualizar la orden: {error}"
            )
            page.update()

    return ft.Container(
        expand=True,
        bgcolor=COLOR_FONDO,
        padding=20,
        content=ft.Column(
            scroll=ft.ScrollMode.AUTO,
            spacing=10,
            controls=[
                ft.Row(
                    alignment=(
                        ft.MainAxisAlignment
                        .SPACE_BETWEEN
                    ),
                    controls=[
                        ft.Text(
                            "Editar Orden",
                            size=26,
                            weight=ft.FontWeight.BOLD,
                            color="white",
                        ),
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            icon_color="white",
                            on_click=lambda e: cambiar_vista(
                                "historial"
                            ),
                        ),
                    ],
                ),

                ft.Text(
                    codigo_orden,
                    color="#8EC5E8",
                    size=14,
                ),

                tarjeta(
                    "Cliente",
                    [
                        cliente,
                        telefono,
                        correo,
                    ],
                ),

                tarjeta(
                    "Vehículo",
                    [
                        patente,
                        ft.Row(
                            wrap=True,
                            controls=[
                                marca,
                                modelo,
                            ],
                        ),
                        ft.Row(
                            wrap=True,
                            controls=[
                                anio,
                                kilometraje,
                            ],
                        ),
                        vin,
                    ],
                ),

                tarjeta(
                    "Observaciones y recomendaciones",
                    [
                        observaciones,
                        recomendaciones,
                    ],
                ),

                tarjeta(
                    "Estado final",
                    [
                        estado,
                        observacion_estado,
                    ],
                ),

                ft.ElevatedButton(
                    "GUARDAR CAMBIOS Y REGENERAR PDF",
                    height=58,
                    bgcolor=COLOR_PRIMARIO,
                    color="white",
                    on_click=guardar_cambios,
                ),

                mensaje,
            ],
        ),
    )