import flet as ft


class EstadoCard(ft.Container):

    def __init__(self):
        super().__init__()

        self.observacion = ft.TextField(
            label="Observaciones del estado final",
            multiline=True,
            min_lines=3,
            visible=False,
        )

        self.estado = ft.RadioGroup(
            ft.Column(
                [
                    ft.Radio(
                        value="Operativo",
                        label="Operativo",
                    ),
                    ft.Radio(
                        value="Operativo con observaciones",
                        label="Operativo con observaciones",
                    ),
                    ft.Radio(
                        value="Pendiente",
                        label="Pendiente",
                    ),
                    ft.Radio(
                        value="No operativo",
                        label="No operativo",
                    ),
                ]
            ),
            value="Operativo",
            on_change=self.cambiar_estado,
        )

        self.bgcolor = "#142739"
        self.border_radius = 18
        self.padding = 18
        self.margin = ft.Margin(0, 0, 0, 15)

        self.content = ft.Column(
            spacing=12,
            controls=[
                ft.Text(
                    "Estado Final",
                    size=18,
                    weight="bold",
                    color="white",
                ),
                ft.Divider(),
                self.estado,
                self.observacion,
            ],
        )

    def cambiar_estado(self, e):
        requiere_observacion = (
            self.estado.value == "Operativo con observaciones"
        )

        self.observacion.visible = requiere_observacion

        if not requiere_observacion:
            self.observacion.value = ""

        if self.page:
            self.update()

    def obtener_datos(self):
        observacion_estado = ""

        if self.estado.value == "Operativo con observaciones":
            observacion_estado = self.observacion.value or ""

        return {
            "estado_final": self.estado.value,
            "observacion_estado": observacion_estado,
        }