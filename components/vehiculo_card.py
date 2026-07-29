import flet as ft


class VehiculoCard(ft.Container):

    def __init__(self):
        super().__init__()

        self.marca = self.crear_campo("Marca")
        self.modelo = self.crear_campo("Modelo")
        self.anio = self.crear_campo("Año")
        self.patente = self.crear_campo("Patente")
        self.kilometraje = self.crear_campo("Kilometraje")
        self.vin = self.crear_campo(
            "VIN / Número de serie"
        )

        self.bgcolor = "#142739"
        self.border_radius = 18
        self.padding = 18
        self.margin = ft.Margin(0, 0, 0, 15)

        self.content = ft.Column(
            spacing=12,
            controls=[
                ft.Text(
                    "Información del Vehículo",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color="white",
                ),

                ft.Divider(
                    color="#2D6A8A",
                ),

                self.patente,

                ft.ResponsiveRow(
                    spacing=12,
                    run_spacing=12,
                    controls=[
                        ft.Container(
                            col={
                                "xs": 12,
                                "sm": 6,
                                "md": 6,
                            },
                            content=self.marca,
                        ),
                        ft.Container(
                            col={
                                "xs": 12,
                                "sm": 6,
                                "md": 6,
                            },
                            content=self.modelo,
                        ),
                    ],
                ),

                ft.ResponsiveRow(
                    spacing=12,
                    run_spacing=12,
                    controls=[
                        ft.Container(
                            col={
                                "xs": 12,
                                "sm": 6,
                                "md": 6,
                            },
                            content=self.anio,
                        ),
                        ft.Container(
                            col={
                                "xs": 12,
                                "sm": 6,
                                "md": 6,
                            },
                            content=self.kilometraje,
                        ),
                    ],
                ),

                self.vin,
            ],
        )

    def crear_campo(self, etiqueta):
        return ft.TextField(
            label=etiqueta,
            border_color="#2D6A8A",
            focused_border_color="#8EC5E8",
            expand=True,
        )

    def cargar(self, datos):
        if not datos:
            return

        self.marca.value = datos.get(
            "marca",
            "",
        )

        self.modelo.value = datos.get(
            "modelo",
            "",
        )

        self.anio.value = datos.get(
            "anio",
            "",
        )

        self.patente.value = datos.get(
            "patente",
            "",
        )

        self.kilometraje.value = datos.get(
            "kilometraje",
            "",
        )

        self.vin.value = datos.get(
            "vin",
            "",
        )

    def limpiar(self):
        self.marca.value = ""
        self.modelo.value = ""
        self.anio.value = ""
        self.patente.value = ""
        self.kilometraje.value = ""
        self.vin.value = ""

    def obtener_datos(self):
        return {
            "marca": self.marca.value or "",
            "modelo": self.modelo.value or "",
            "anio": self.anio.value or "",
            "patente": self.patente.value or "",
            "kilometraje": (
                self.kilometraje.value or ""
            ),
            "vin": self.vin.value or "",
        }