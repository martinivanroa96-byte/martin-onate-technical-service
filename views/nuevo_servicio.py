from datetime import datetime

import flet as ft

from components.buscador_vehiculo import BuscadorVehiculo
from components.cliente_card import ClienteCard
from components.estado_card import EstadoCard
from components.fotos_card import FotosCard
from components.tipo_servicio_card import TipoServicioCard
from components.vehiculo_card import VehiculoCard

from services.camera_service import CameraService
from services.foto_service import (
    copiar_foto_desde_archivo,
    guardar_foto_bytes,
)
from services.pdf.pdf_service import generar_informe_pdf


COLOR_FONDO = "#0B1723"
COLOR_CARD = "#142739"
COLOR_PRIMARIO = "#1F6AA5"
COLOR_LINEA = "#2D6A8A"


def nuevo_servicio_view(page: ft.Page, cambiar_vista):
    cliente_card = ClienteCard()
    vehiculo_card = VehiculoCard()
    tipo_servicio_card = TipoServicioCard()
    estado_card = EstadoCard()

    codigo_orden = datetime.now().strftime(
        "OT-%Y%m%d-%H%M%S"
    )

    mensaje = ft.Text(
        "",
        color="#8EC5E8",
        size=12,
    )

    observaciones = ft.TextField(
        label="Observaciones / hallazgos",
        multiline=True,
        min_lines=3,
        max_lines=6,
        border_color=COLOR_LINEA,
        focused_border_color="#8EC5E8",
    )

    recomendaciones = ft.TextField(
        label="Recomendaciones",
        multiline=True,
        min_lines=3,
        max_lines=6,
        border_color=COLOR_LINEA,
        focused_border_color="#8EC5E8",
    )

    file_picker = ft.FilePicker()
    camera_service = CameraService(page)

    def mostrar_mensaje(texto):
        mensaje.value = texto
        page.update()

    def cargar_vehiculo(datos):
        if datos:
            cliente_card.cargar(datos)
            vehiculo_card.cargar(datos)
        else:
            cliente_card.limpiar()
            vehiculo_card.limpiar()

        page.update()

    buscador = BuscadorVehiculo(
        page,
        cargar_vehiculo,
    )

    buscador.bgcolor = COLOR_CARD
    buscador.border_radius = 18
    buscador.padding = 18
    buscador.margin = ft.Margin(0, 0, 0, 15)

    async def seleccionar_archivo_windows(tipo):
        try:
            archivos = await file_picker.pick_files(
                allow_multiple=False,
                file_type=ft.FilePickerFileType.IMAGE,
            )

            if not archivos:
                mostrar_mensaje(
                    "No se seleccionó ninguna fotografía."
                )
                return

            archivo = archivos[0]

            if not archivo.path:
                mostrar_mensaje(
                    "No se pudo obtener la ruta de la imagen."
                )
                return

            ruta_guardada = copiar_foto_desde_archivo(
                codigo_orden=codigo_orden,
                tipo=tipo,
                ruta_origen=archivo.path,
            )

            fotos_card.agregar_foto(
                tipo,
                ruta_guardada,
            )

            mostrar_mensaje(
                f"Fotografía agregada en {tipo.upper()}."
            )

        except Exception as error:
            mostrar_mensaje(
                f"Error al seleccionar fotografía: {error}"
            )

    async def tomar_foto_android(tipo):
        try:
            if not camera_service.inicializada:
                correcto, detalle = (
                    await camera_service.inicializar()
                )

                if not correcto:
                    mostrar_mensaje(detalle)
                    return

            foto_bytes = await camera_service.tomar_foto()

            ruta_guardada = guardar_foto_bytes(
                codigo_orden=codigo_orden,
                tipo=tipo,
                contenido=foto_bytes,
                extension=".jpg",
            )

            fotos_card.agregar_foto(
                tipo,
                ruta_guardada,
            )

            mostrar_mensaje(
                f"Fotografía capturada en {tipo.upper()}."
            )

        except Exception as error:
            mostrar_mensaje(
                f"Error al utilizar la cámara: {error}"
            )

    def solicitar_foto(tipo):
        plataforma = str(page.platform).lower()

        if "android" in plataforma:
            page.run_task(
                tomar_foto_android,
                tipo,
            )
        else:
            page.run_task(
                seleccionar_archivo_windows,
                tipo,
            )

    fotos_card = FotosCard(
        on_tomar_foto=solicitar_foto,
    )

    def tarjeta(titulo, controles):
        return ft.Container(
            bgcolor=COLOR_CARD,
            border_radius=18,
            padding=16,
            margin=ft.Margin(0, 0, 0, 12),
            content=ft.Column(
                spacing=12,
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

    def generar_pdf_click(e):
        try:
            datos = {}

            datos.update(
                cliente_card.obtener_datos()
            )

            datos.update(
                vehiculo_card.obtener_datos()
            )

            datos["codigo_orden"] = codigo_orden

            datos["tipo_servicio"] = (
                tipo_servicio_card.obtener_tipo_servicio()
            )

            datos["trabajos"] = (
                tipo_servicio_card.obtener_trabajos()
            )

            datos["otro_trabajo"] = ""
            datos["hallazgos"] = []

            datos["observaciones"] = (
                observaciones.value or ""
            )

            datos["recomendaciones"] = []

            datos["recomendacion_adicional"] = (
                recomendaciones.value or ""
            )

            datos.update(
                estado_card.obtener_datos()
            )

            datos.update(
                fotos_card.obtener_datos()
            )

            ruta_pdf = generar_informe_pdf(datos)

            mensaje.value = (
                f"Informe creado correctamente: {ruta_pdf}"
            )

            page.snack_bar = ft.SnackBar(
                ft.Text(
                    "Informe generado correctamente."
                )
            )

            page.snack_bar.open = True
            page.update()

        except Exception as error:
            mostrar_mensaje(
                f"Error al generar el PDF: {error}"
            )

    ancho_contenido = 780

    if page.width:
        ancho_contenido = min(
            max(page.width - 24, 300),
            780,
        )

    alto_disponible = 700

    if page.height:
        alto_disponible = max(
            page.height - 24,
            400,
        )

    encabezado = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Column(
                spacing=3,
                expand=True,
                controls=[
                    ft.Text(
                        "Nueva Orden de Trabajo",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color="white",
                    ),
                    ft.Text(
                        f"Orden: {codigo_orden}",
                        color="#8EC5E8",
                        size=12,
                    ),
                ],
            ),
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_color="white",
                tooltip="Volver",
                on_click=lambda e: cambiar_vista(
                    "home"
                ),
            ),
        ],
    )

    boton_generar = ft.ElevatedButton(
        "GENERAR INFORME PDF",
        icon=ft.Icons.PICTURE_AS_PDF,
        height=58,
        bgcolor=COLOR_PRIMARIO,
        color="white",
        on_click=generar_pdf_click,
    )

    contenido_principal = ft.Container(
        width=ancho_contenido,
        content=ft.Column(
            spacing=10,
            controls=[
                encabezado,

                buscador,

                cliente_card,

                vehiculo_card,

                tipo_servicio_card,

                tarjeta(
                    "Observaciones y recomendaciones",
                    [
                        observaciones,
                        recomendaciones,
                    ],
                ),

                fotos_card,

                estado_card,

                boton_generar,

                mensaje,

                ft.Container(
                    height=30,
                ),
            ],
        ),
    )

    lista_desplazable = ft.ListView(
        expand=True,
        spacing=0,
        padding=0,
        controls=[
            ft.Container(
                width=ancho_contenido,
                alignment=ft.Alignment(
                    0,
                    -1,
                ),
                content=contenido_principal,
            ),
        ],
    )

    return ft.SafeArea(
        content=ft.Container(
            expand=True,
            bgcolor=COLOR_FONDO,
            padding=12,
            alignment=ft.Alignment(
                0,
                -1,
            ),
            content=ft.Container(
                width=ancho_contenido,
                height=alto_disponible,
                content=lista_desplazable,
            ),
        )
    )