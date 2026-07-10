from pathlib import Path

import flet as ft


class FotosCard(ft.Container):

    def __init__(self, on_tomar_foto):
        super().__init__()

        self.on_tomar_foto = on_tomar_foto

        self.fotos = {
            "antes": [],
            "durante": [],
            "despues": [],
        }

        self.vistas_previas = {
            "antes": ft.Row(
                wrap=True,
                spacing=10,
                run_spacing=10,
            ),
            "durante": ft.Row(
                wrap=True,
                spacing=10,
                run_spacing=10,
            ),
            "despues": ft.Row(
                wrap=True,
                spacing=10,
                run_spacing=10,
            ),
        }

        self.mensajes_vacios = {
            "antes": ft.Text(
                "Sin fotografías registradas",
                size=12,
                color="#B8C7D1",
            ),
            "durante": ft.Text(
                "Sin fotografías registradas",
                size=12,
                color="#B8C7D1",
            ),
            "despues": ft.Text(
                "Sin fotografías registradas",
                size=12,
                color="#B8C7D1",
            ),
        }

        self.bgcolor = "#142739"
        self.border_radius = 18
        self.padding = 18
        self.margin = ft.Margin(0, 0, 0, 15)

        self.content = ft.Column(
            spacing=16,
            controls=[
                ft.Text(
                    "Evidencia Fotográfica",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color="white",
                ),

                ft.Divider(
                    color="#2D6A8A",
                ),

                self.crear_seccion(
                    titulo="ANTES",
                    tipo="antes",
                ),

                ft.Divider(
                    color="#2D6A8A",
                ),

                self.crear_seccion(
                    titulo="DURANTE",
                    tipo="durante",
                ),

                ft.Divider(
                    color="#2D6A8A",
                ),

                self.crear_seccion(
                    titulo="DESPUÉS",
                    tipo="despues",
                ),
            ],
        )

    def crear_seccion(self, titulo, tipo):
        return ft.Column(
            spacing=10,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            titulo,
                            size=15,
                            weight=ft.FontWeight.BOLD,
                            color="#8EC5E8",
                        ),

                        ft.ElevatedButton(
                            "Tomar foto",
                            icon=ft.Icons.CAMERA_ALT,
                            bgcolor="#1F6AA5",
                            color="white",
                            on_click=lambda e, categoria=tipo: (
                                self.on_tomar_foto(categoria)
                            ),
                        ),
                    ],
                ),

                self.mensajes_vacios[tipo],

                self.vistas_previas[tipo],
            ],
        )

    def crear_miniatura(self, tipo, ruta_foto):
        imagen = ft.Container(
            width=115,
            height=90,
            border_radius=10,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            content=ft.Image(
                src=ruta_foto,
                width=115,
                height=90,
                fit=ft.BoxFit.COVER,
            ),
        )

        tarjeta_foto = ft.Container(
            width=125,
            padding=5,
            border_radius=12,
            bgcolor="#24384A",
        )

        boton_eliminar = ft.IconButton(
            icon=ft.Icons.DELETE,
            icon_color="#FF6B6B",
            tooltip="Eliminar fotografía",
            on_click=lambda e: self.eliminar_foto(
                tipo,
                ruta_foto,
                tarjeta_foto,
            ),
        )

        tarjeta_foto.content = ft.Column(
            spacing=2,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                imagen,
                boton_eliminar,
            ],
        )

        return tarjeta_foto

    def agregar_foto(self, tipo, foto):
        if tipo not in self.fotos:
            return

        if not foto:
            return

        self.fotos[tipo].append(foto)

        miniatura = self.crear_miniatura(
            tipo,
            foto,
        )

        self.vistas_previas[tipo].controls.append(
            miniatura
        )

        self.mensajes_vacios[tipo].visible = False

        if self.page:
            self.update()

    def eliminar_foto(
        self,
        tipo,
        ruta_foto,
        control_miniatura,
    ):
        if tipo not in self.fotos:
            return

        try:
            archivo = Path(ruta_foto)

            if archivo.exists() and archivo.is_file():
                archivo.unlink()

        except OSError as error:
            if self.page:
                self.page.snack_bar = ft.SnackBar(
                    ft.Text(
                        f"No se pudo eliminar el archivo: {error}"
                    )
                )
                self.page.snack_bar.open = True
                self.page.update()

            return

        if ruta_foto in self.fotos[tipo]:
            self.fotos[tipo].remove(
                ruta_foto
            )

        if control_miniatura in self.vistas_previas[tipo].controls:
            self.vistas_previas[tipo].controls.remove(
                control_miniatura
            )

        self.mensajes_vacios[tipo].visible = (
            len(self.fotos[tipo]) == 0
        )

        if self.page:
            self.page.snack_bar = ft.SnackBar(
                ft.Text(
                    "Fotografía eliminada correctamente."
                )
            )
            self.page.snack_bar.open = True
            self.update()

    def obtener_datos(self):
        return {
            "fotos_antes": list(
                self.fotos["antes"]
            ),
            "fotos_durante": list(
                self.fotos["durante"]
            ),
            "fotos_despues": list(
                self.fotos["despues"]
            ),
        }

    def limpiar(self):
        for tipo in self.fotos:
            self.fotos[tipo].clear()
            self.vistas_previas[tipo].controls.clear()
            self.mensajes_vacios[tipo].visible = True

        if self.page:
            self.update()