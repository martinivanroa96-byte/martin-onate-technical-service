import flet as ft


class ClienteCard(ft.Container):
    def __init__(self):
        super().__init__()
        self.nombre = ft.TextField(label="Nombre del cliente")
        self.telefono = ft.TextField(label="Teléfono")
        self.correo = ft.TextField(label="Correo")

        self.bgcolor = "#142739"
        self.border_radius = 18
        self.padding = 18
        self.margin = ft.Margin(0, 0, 0, 15)
        self.content = ft.Column(
            spacing=12,
            controls=[
                ft.Text("Información del Cliente", size=18, weight="bold", color="white"),
                ft.Divider(color="#2D6A8A"),
                self.nombre,
                self.telefono,
                self.correo,
            ],
        )

    def cargar(self, datos):
        if not datos:
            return
        self.nombre.value = datos.get("cliente", "")
        self.telefono.value = datos.get("telefono", "")
        self.correo.value = datos.get("correo", "")

    def limpiar(self):
        self.nombre.value = ""
        self.telefono.value = ""
        self.correo.value = ""

    def obtener_datos(self):
        return {
            "cliente": self.nombre.value,
            "telefono": self.telefono.value,
            "correo": self.correo.value,
        }
