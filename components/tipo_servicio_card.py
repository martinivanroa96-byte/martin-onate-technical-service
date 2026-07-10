import flet as ft


class TipoServicioCard(ft.Container):
    def __init__(self):
        super().__init__()
        self.categoria_actual = "Mantención"
        self.trabajos_por_categoria = {
            "Mantención": [
                "Cambio de aceite",
                "Cambio filtro de aceite",
                "Cambio filtro de aire",
                "Cambio filtro combustible",
                "Cambio filtro cabina",
                "Revisión de niveles",
                "Escaneo electrónico",
            ],
            "Diagnóstico": [
                "Escaneo electrónico",
                "Revisión códigos de falla",
                "Prueba de ruta",
                "Medición batería",
                "Revisión sistema de carga",
            ],
            "Frenos": [
                "Cambio de pastillas",
                "Cambio de discos",
                "Rectificado de discos",
                "Cambio líquido de frenos",
                "Limpieza sistema de frenos",
                "Prueba de frenado",
            ],
            "Suspensión": [
                "Cambio amortiguadores",
                "Cambio bieletas",
                "Cambio terminales",
                "Cambio rótulas",
                "Revisión tren delantero",
            ],
            "Electricidad": [
                "Revisión batería",
                "Revisión alternador",
                "Revisión motor de partida",
                "Revisión luces",
                "Revisión fusibles",
            ],
            "Motor": [
                "Cambio correa accesorios",
                "Cambio bomba de agua",
                "Cambio termostato",
                "Cambio empaquetaduras",
                "Regulación de válvulas",
            ],
            "Aire acondicionado": [
                "Carga de gas",
                "Detección de fugas",
                "Cambio compresor",
                "Cambio filtro habitáculo",
                "Limpieza evaporador",
            ],
            "Transmisión": [
                "Cambio aceite caja",
                "Cambio aceite diferencial",
                "Revisión embrague",
                "Cambio kit embrague",
            ],
            "Otro": ["Trabajo personalizado"],
        }

        self.checks = {}
        self.contador = ft.Text("Trabajos seleccionados: 0", color="#9BC8F5")
        self.botones = ft.Row(wrap=True, spacing=8, run_spacing=8)
        self.lista = ft.Column(spacing=5)

        self.bgcolor = "#142739"
        self.border_radius = 18
        self.padding = 18
        self.margin = ft.Margin(0, 0, 0, 15)
        self.content = ft.Column(
            spacing=12,
            controls=[
                ft.Text("Tipo de Servicio", size=18, weight="bold", color="white"),
                ft.Divider(color="#2D6A8A"),
                self.botones,
                self.contador,
                self.lista,
            ],
        )

        self.crear_botones()
        self.cargar_categoria_inicial()

    def crear_botones(self):
        self.botones.controls.clear()
        for categoria in self.trabajos_por_categoria:
            seleccionado = categoria == self.categoria_actual
            self.botones.controls.append(
                ft.ElevatedButton(
                    categoria,
                    bgcolor="#1F6AA5" if seleccionado else "#24384A",
                    color="white",
                    on_click=lambda e, c=categoria: self.mostrar_categoria(c),
                )
            )

    def obtener_checkbox(self, trabajo):
        if trabajo not in self.checks:
            self.checks[trabajo] = ft.Checkbox(
                label=trabajo,
                on_change=self.actualizar_contador,
            )
        return self.checks[trabajo]

    def cargar_categoria_inicial(self):
        self.lista.controls.clear()
        for trabajo in self.trabajos_por_categoria[self.categoria_actual]:
            self.lista.controls.append(self.obtener_checkbox(trabajo))

    def mostrar_categoria(self, categoria):
        self.categoria_actual = categoria
        self.crear_botones()
        self.lista.controls.clear()
        for trabajo in self.trabajos_por_categoria[categoria]:
            self.lista.controls.append(self.obtener_checkbox(trabajo))
        if self.page is not None:
            self.update()

    def actualizar_contador(self, e=None):
        total = sum(1 for chk in self.checks.values() if chk.value)
        self.contador.value = f"Trabajos seleccionados: {total}"
        if self.page is not None:
            self.update()

    def obtener_trabajos(self):
        return [nombre for nombre, chk in self.checks.items() if chk.value]

    def obtener_tipo_servicio(self):
        return self.categoria_actual
