import flet as ft

from services.orden_service import cargar_datos_orden


COLOR_FONDO = "#0B1723"
COLOR_CARD = "#142739"
COLOR_LINEA = "#2D6A8A"
COLOR_TEXTO_SECUNDARIO = "#B8C7D1"


def detalle_orden_view(
    page: ft.Page,
    cambiar_vista,
    codigo_orden,
):
    datos = cargar_datos_orden(codigo_orden) or {}

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
                    ft.Divider(color=COLOR_LINEA),
                    *controles,
                ],
            ),
        )

    trabajos = datos.get("trabajos", []) or []

    controles_trabajos = []

    if trabajos:
        for trabajo in trabajos:
            controles_trabajos.append(
                ft.Text(
                    f"• {trabajo}",
                    color="white",
                )
            )
    else:
        controles_trabajos.append(
            ft.Text(
                "Sin trabajos registrados.",
                color=COLOR_TEXTO_SECUNDARIO,
            )
        )

    fotos_antes = datos.get("fotos_antes", []) or []
    fotos_durante = datos.get("fotos_durante", []) or []
    fotos_despues = datos.get("fotos_despues", []) or []

    def resumen_fotos(titulo, fotos):
        return ft.Text(
            f"{titulo}: {len(fotos)} fotografía(s)",
            color="white",
        )

    return ft.Container(
        expand=True,
        bgcolor=COLOR_FONDO,
        padding=20,
        content=ft.Column(
            scroll=ft.ScrollMode.AUTO,
            spacing=10,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(
                            "Detalle de la Orden",
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
                    datos.get("codigo_orden", codigo_orden),
                    size=16,
                    color="#8EC5E8",
                ),

                tarjeta(
                    "Cliente",
                    [
                        ft.Text(
                            f"Nombre: {datos.get('cliente', '-')}",
                            color="white",
                        ),
                        ft.Text(
                            f"Teléfono: {datos.get('telefono', '-')}",
                            color="white",
                        ),
                        ft.Text(
                            f"Correo: {datos.get('correo', '-')}",
                            color="white",
                        ),
                    ],
                ),

                tarjeta(
                    "Vehículo",
                    [
                        ft.Text(
                            f"Marca: {datos.get('marca', '-')}",
                            color="white",
                        ),
                        ft.Text(
                            f"Modelo: {datos.get('modelo', '-')}",
                            color="white",
                        ),
                        ft.Text(
                            f"Año: {datos.get('año', datos.get('anio', '-'))}",
                            color="white",
                        ),
                        ft.Text(
                            f"Patente: {datos.get('patente', '-')}",
                            color="white",
                        ),
                        ft.Text(
                            f"Kilometraje: {datos.get('kilometraje', '-')}",
                            color="white",
                        ),
                        ft.Text(
                            f"VIN: {datos.get('vin', '-')}",
                            color="white",
                        ),
                    ],
                ),

                tarjeta(
                    "Trabajos realizados",
                    controles_trabajos,
                ),

                tarjeta(
                    "Observaciones y recomendaciones",
                    [
                        ft.Text(
                            "Observaciones:",
                            weight=ft.FontWeight.BOLD,
                            color="white",
                        ),
                        ft.Text(
                            datos.get("observaciones", "")
                            or "Sin observaciones.",
                            color=COLOR_TEXTO_SECUNDARIO,
                        ),
                        ft.Text(
                            "Recomendaciones:",
                            weight=ft.FontWeight.BOLD,
                            color="white",
                        ),
                        ft.Text(
                            datos.get(
                                "recomendacion_adicional",
                                "",
                            )
                            or "Sin recomendaciones.",
                            color=COLOR_TEXTO_SECUNDARIO,
                        ),
                    ],
                ),

                tarjeta(
                    "Evidencia fotográfica",
                    [
                        resumen_fotos("Antes", fotos_antes),
                        resumen_fotos("Durante", fotos_durante),
                        resumen_fotos("Después", fotos_despues),
                    ],
                ),

                tarjeta(
                    "Estado final",
                    [
                        ft.Text(
                            datos.get(
                                "estado_final",
                                "No especificado",
                            ),
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color="white",
                        ),
                        ft.Text(
                            datos.get(
                                "observacion_estado",
                                "",
                            )
                            or "Sin observaciones del estado final.",
                            color=COLOR_TEXTO_SECUNDARIO,
                        ),
                    ],
                ),
            ],
        ),
    )