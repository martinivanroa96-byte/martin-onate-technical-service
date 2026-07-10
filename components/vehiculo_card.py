import flet as ft


class VehiculoCard(ft.Container):
    def __init__(self):
        super().__init__()
        self.marca = ft.TextField(label="Marca")
        self.modelo = ft.TextField(label="Modelo")
        self.anio = ft.TextField(label="Año")
        self.patente = ft.TextField(label="Patente")
        self.kilometraje = ft.TextField(label="Kilometraje")
        self.vin = ft.TextField(label="VIN / Número de serie")

        self.bgcolor = "#142739"
        self.border_radius = 18
        self.padding = 18
        self.margin = ft.Margin(0, 0, 0, 15)
        self.content = ft.Column(
            spacing=12,
            controls=[
                ft.Text("Información del Vehículo", size=18, weight="bold", color="white"),
                ft.Divider(color="#2D6A8A"),
                self.patente,
                ft.Row(controls=[self.marca, self.modelo]),
                ft.Row(controls=[self.anio, self.kilometraje]),
                self.vin,
            ],
        )

    def cargar(self, datos):
        if not datos:
            return
        self.marca.value = datos.get("marca", "")
        self.modelo.value = datos.get("modelo", "")
        self.anio.value = datos.get("anio", "")
        self.patente.value = datos.get("patente", "")
        self.kilometraje.value = datos.get("kilometraje", "")
        self.vin.value = datos.get("vin", "")

    def limpiar(self):
        self.marca.value = ""
        self.modelo.value = ""
        self.anio.value = ""
        self.patente.value = ""
        self.kilometraje.value = ""
        self.vin.value = ""

    def obtener_datos(self):
        return {
            "marca": self.marca.value,
            "modelo": self.modelo.value,
            "anio": self.anio.value,
            "patente": self.patente.value,
            "kilometraje": self.kilometraje.value,
            "vin": self.vin.value,
        }
