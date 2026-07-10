import flet as ft

from views.detalle_orden import detalle_orden_view
from views.editar_orden import editar_orden_view
from views.historial import historial_view
from views.home import home_view
from views.nuevo_servicio import nuevo_servicio_view


def main(page: ft.Page):
    page.title = "Martín Oñate Technical Service"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0B1723"
    page.padding = 0

    def cambiar_vista(nombre_vista, datos=None):
        page.clean()

        if nombre_vista == "home":
            page.add(
                home_view(
                    page,
                    cambiar_vista,
                )
            )

        elif nombre_vista == "nuevo_servicio":
            page.add(
                nuevo_servicio_view(
                    page,
                    cambiar_vista,
                )
            )

        elif nombre_vista == "historial":
            page.add(
                historial_view(
                    page,
                    cambiar_vista,
                )
            )

        elif nombre_vista == "detalle_orden":
            codigo_orden = datos or ""

            page.add(
                detalle_orden_view(
                    page,
                    cambiar_vista,
                    codigo_orden,
                )
            )

        elif nombre_vista == "editar_orden":
            codigo_orden = datos or ""

            page.add(
                editar_orden_view(
                    page,
                    cambiar_vista,
                    codigo_orden,
                )
            )

        else:
            page.add(
                home_view(
                    page,
                    cambiar_vista,
                )
            )

        page.update()

    cambiar_vista("home")


if __name__ == "__main__":
    ft.run(main)