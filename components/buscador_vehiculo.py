import flet as ft
from services.data_service import buscar_por_patente


class BuscadorVehiculo(ft.Container):
    def __init__(self, page, callback):
        super().__init__()
        self.page_ref = page
        self.callback = callback

        self.patente = ft.TextField(
            label="Patente",
            hint_text="Ej: ABCD12",
            expand=True,
        )
        self.mensaje = ft.Text("", color="#8EC5E8")

        self.bgcolor = "#142739"
        self.border_radius = 18
        self.padding = 18
        self.margin = ft.Margin(0, 0, 0, 15)

        self.content = ft.Column(
            spacing=12,
            controls=[
                ft.Text("Buscar Vehículo", size=18, weight="bold", color="white"),
                ft.Divider(color="#2D6A8A"),
                ft.Row(
                    controls=[
                        self.patente,
                        ft.ElevatedButton(
                            "Buscar",
                            icon=ft.Icons.SEARCH,
                            on_click=self.buscar,
                            bgcolor="#1F6AA5",
                            color="white",
                        ),
                    ]
                ),
                self.mensaje,
            ],
        )

    def buscar(self, e):
        datos = buscar_por_patente(self.patente.value)
        if datos:
            self.mensaje.value = "Vehículo encontrado. Datos cargados."
            self.callback(datos)
        else:
            self.mensaje.value = "Patente no registrada. Completa los datos."
            self.callback(None)
        self.page_ref.update()
