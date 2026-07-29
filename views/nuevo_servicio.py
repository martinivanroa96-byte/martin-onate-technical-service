from datetime import datetime
from pathlib import Path

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
COLOR_TEXTO_SECUNDARIO = "#8EC5E8"
COLOR_ERROR = "#FF8A80"
COLOR_EXITO = "#8FD694"


def nuevo_servicio_view(
    page: ft.Page,
    cambiar_vista,
):
    cliente_card = ClienteCard()
    vehiculo_card = VehiculoCard()
    tipo_servicio_card = TipoServicioCard()
    estado_card = EstadoCard()

    codigo_orden = datetime.now().strftime(
        "OT-%Y%m%d-%H%M%S"
    )

    ruta_pdf_generado = {
        "ruta": None,
    }

    tipo_foto_actual = {
        "tipo": None,
    }

    capturando_foto = {
        "valor": False,
    }

    mensaje = ft.Text(
        "",
        color=COLOR_TEXTO_SECUNDARIO,
        size=12,
        selectable=True,
    )

    observaciones = ft.TextField(
        label="Observaciones / hallazgos",
        multiline=True,
        min_lines=3,
        max_lines=6,
        border_color=COLOR_LINEA,
        focused_border_color=COLOR_TEXTO_SECUNDARIO,
    )

    recomendaciones = ft.TextField(
        label="Recomendaciones",
        multiline=True,
        min_lines=3,
        max_lines=6,
        border_color=COLOR_LINEA,
        focused_border_color=COLOR_TEXTO_SECUNDARIO,
    )

    file_picker = ft.FilePicker()
    camera_service = CameraService(page)
    share_service = ft.Share()

    def mostrar_mensaje(
        texto,
        color=COLOR_TEXTO_SECUNDARIO,
    ):
        mensaje.value = texto
        mensaje.color = color
        page.update()

    def mostrar_snackbar(
        texto,
    ):
        page.show_dialog(
            ft.SnackBar(
                content=ft.Text(texto),
            )
        )

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
    buscador.margin = ft.Margin(
        0,
        0,
        0,
        15,
    )

    async def seleccionar_archivo_windows(
        tipo,
    ):
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
                    "No se pudo obtener la ruta de la imagen.",
                    COLOR_ERROR,
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
                (
                    "Fotografía agregada correctamente "
                    f"en {tipo.upper()}."
                ),
                COLOR_EXITO,
            )

        except Exception as error:
            mostrar_mensaje(
                (
                    "Error al seleccionar fotografía: "
                    f"{error}"
                ),
                COLOR_ERROR,
            )

    texto_estado_camara = ft.Text(
        "Preparando cámara...",
        color=COLOR_TEXTO_SECUNDARIO,
        size=12,
        text_align=ft.TextAlign.CENTER,
    )

    indicador_camara = ft.ProgressRing(
        width=28,
        height=28,
        stroke_width=3,
        color=COLOR_TEXTO_SECUNDARIO,
    )

    boton_capturar = ft.ElevatedButton(
        "CAPTURAR",
        icon=ft.Icons.CAMERA_ALT,
        bgcolor=COLOR_PRIMARIO,
        color="white",
        disabled=True,
    )

    boton_cancelar_camara = ft.OutlinedButton(
        "CANCELAR",
        icon=ft.Icons.CLOSE,
    )

    preview_camara = camera_service.obtener_preview()

    if preview_camara is not None:
        preview_camara.width = 310
        preview_camara.height = 410
        preview_camara.preview_enabled = True

        contenido_preview = ft.Container(
            width=310,
            height=410,
            bgcolor="black",
            border_radius=14,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            alignment=ft.Alignment.CENTER,
            content=preview_camara,
        )
    else:
        contenido_preview = ft.Container(
            width=310,
            height=410,
            bgcolor="#101010",
            border_radius=14,
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=(
                    ft.CrossAxisAlignment.CENTER
                ),
                controls=[
                    ft.Icon(
                        ft.Icons.NO_PHOTOGRAPHY,
                        color="white",
                        size=44,
                    ),
                    ft.Text(
                        "Cámara no disponible",
                        color="white",
                    ),
                ],
            ),
        )

    dialogo_camara = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Text(
            "Tomar fotografía",
            color="white",
            weight=ft.FontWeight.BOLD,
        ),
        content=ft.Column(
            tight=True,
            spacing=12,
            horizontal_alignment=(
                ft.CrossAxisAlignment.CENTER
            ),
            controls=[
                contenido_preview,
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=(
                        ft.CrossAxisAlignment.CENTER
                    ),
                    controls=[
                        indicador_camara,
                        texto_estado_camara,
                    ],
                ),
            ],
        ),
        actions=[
            boton_cancelar_camara,
            boton_capturar,
        ],
        actions_alignment=(
            ft.MainAxisAlignment.SPACE_BETWEEN
        ),
    )

    def cerrar_dialogo_camara(
        e=None,
    ):
        if capturando_foto["valor"]:
            return

        tipo_foto_actual["tipo"] = None
        page.pop_dialog()

    boton_cancelar_camara.on_click = (
        cerrar_dialogo_camara
    )

    async def abrir_camara_android(
        tipo,
    ):
        try:
            tipo_foto_actual["tipo"] = tipo

            texto_estado_camara.value = (
                "Solicitando permiso e iniciando cámara..."
            )

            texto_estado_camara.color = (
                COLOR_TEXTO_SECUNDARIO
            )

            indicador_camara.visible = True
            boton_capturar.disabled = True
            boton_cancelar_camara.disabled = False

            page.show_dialog(
                dialogo_camara
            )

            page.update()

            correcto, detalle = (
                await camera_service.inicializar()
            )

            if not correcto:
                texto_estado_camara.value = detalle
                texto_estado_camara.color = COLOR_ERROR
                indicador_camara.visible = False
                boton_capturar.disabled = True

                page.update()
                return

            texto_estado_camara.value = (
                "Cámara lista. Encuadra la imagen "
                "y presiona CAPTURAR."
            )

            texto_estado_camara.color = COLOR_EXITO
            indicador_camara.visible = False
            boton_capturar.disabled = False

            page.update()

        except Exception as error:
            texto_estado_camara.value = (
                "No se pudo abrir la cámara: "
                f"{error}"
            )

            texto_estado_camara.color = COLOR_ERROR
            indicador_camara.visible = False
            boton_capturar.disabled = True

            page.update()

    async def capturar_foto_android(
        e=None,
    ):
        tipo = tipo_foto_actual["tipo"]

        if not tipo:
            mostrar_mensaje(
                "No se pudo determinar el tipo de fotografía.",
                COLOR_ERROR,
            )
            return

        if capturando_foto["valor"]:
            return

        capturando_foto["valor"] = True

        try:
            boton_capturar.disabled = True
            boton_cancelar_camara.disabled = True
            indicador_camara.visible = True

            texto_estado_camara.value = (
                "Capturando fotografía..."
            )

            texto_estado_camara.color = (
                COLOR_TEXTO_SECUNDARIO
            )

            page.update()

            foto_bytes = (
                await camera_service.tomar_foto()
            )

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

            page.pop_dialog()

            mostrar_mensaje(
                (
                    "Fotografía capturada correctamente "
                    f"en {tipo.upper()}."
                ),
                COLOR_EXITO,
            )

            mostrar_snackbar(
                "Fotografía guardada correctamente."
            )

        except Exception as error:
            texto_estado_camara.value = (
                "Error al capturar la fotografía: "
                f"{error}"
            )

            texto_estado_camara.color = COLOR_ERROR
            indicador_camara.visible = False
            boton_capturar.disabled = False
            boton_cancelar_camara.disabled = False

            page.update()

        finally:
            capturando_foto["valor"] = False

    boton_capturar.on_click = (
        capturar_foto_android
    )

    def solicitar_foto(
        tipo,
    ):
        plataforma = str(
            page.platform
        ).lower()

        if "android" in plataforma:
            page.run_task(
                abrir_camara_android,
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

    def tarjeta(
        titulo,
        controles,
    ):
        return ft.Container(
            bgcolor=COLOR_CARD,
            border_radius=18,
            padding=16,
            margin=ft.Margin(
                0,
                0,
                0,
                12,
            ),
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

    boton_compartir = ft.ElevatedButton(
        "COMPARTIR INFORME",
        icon=ft.Icons.SHARE,
        height=54,
        bgcolor="#287A53",
        color="white",
        visible=False,
    )

    async def compartir_pdf_click(
        e=None,
    ):
        ruta_pdf = ruta_pdf_generado["ruta"]

        if not ruta_pdf:
            mostrar_mensaje(
                "Primero debes generar el informe PDF.",
                COLOR_ERROR,
            )
            return

        archivo_pdf = Path(ruta_pdf)

        if not archivo_pdf.exists():
            mostrar_mensaje(
                (
                    "No se encontró el archivo PDF. "
                    "Genera nuevamente el informe."
                ),
                COLOR_ERROR,
            )
            return

        try:
            boton_compartir.disabled = True
            boton_compartir.text = "ABRIENDO MENÚ..."
            page.update()

            await share_service.share_files(
                [
                    ft.ShareFile.from_path(
                        str(archivo_pdf),
                        name=archivo_pdf.name,
                    )
                ],
                title="Compartir informe técnico",
                subject="Informe técnico de servicio",
                text=(
                    "Informe técnico generado por "
                    "Martín Oñate Technical Service."
                ),
            )

            mostrar_mensaje(
                "Menú para compartir abierto.",
                COLOR_EXITO,
            )

        except Exception as error:
            mostrar_mensaje(
                (
                    "No se pudo compartir el informe: "
                    f"{error}"
                ),
                COLOR_ERROR,
            )

        finally:
            boton_compartir.disabled = False
            boton_compartir.text = "COMPARTIR INFORME"
            page.update()

    boton_compartir.on_click = (
        compartir_pdf_click
    )

    async def generar_pdf_click(
        e=None,
    ):
        try:
            boton_generar.disabled = True
            boton_generar.text = "GENERANDO INFORME..."
            mensaje.value = "Generando informe PDF..."
            mensaje.color = COLOR_TEXTO_SECUNDARIO
            page.update()

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

            ruta_pdf = generar_informe_pdf(
                datos
            )

            ruta_pdf_generado["ruta"] = ruta_pdf

            boton_compartir.visible = True

            mensaje.value = (
                "Informe generado correctamente. "
                "Ahora puedes compartirlo."
            )

            mensaje.color = COLOR_EXITO

            mostrar_snackbar(
                "Informe PDF generado correctamente."
            )

            page.update()

        except Exception as error:
            mostrar_mensaje(
                (
                    "Error al generar el PDF: "
                    f"{error}"
                ),
                COLOR_ERROR,
            )

        finally:
            boton_generar.disabled = False
            boton_generar.text = (
                "GENERAR INFORME PDF"
            )
            page.update()

    ancho_contenido = 780

    if page.width:
        ancho_contenido = min(
            max(
                page.width - 24,
                300,
            ),
            780,
        )

    alto_disponible = 700

    if page.height:
        alto_disponible = max(
            page.height - 24,
            400,
        )

    encabezado = ft.Row(
        alignment=(
            ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        vertical_alignment=(
            ft.CrossAxisAlignment.CENTER
        ),
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
                        color=COLOR_TEXTO_SECUNDARIO,
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

    botones_informe = ft.ResponsiveRow(
        spacing=10,
        run_spacing=10,
        controls=[
            ft.Container(
                col={
                    "xs": 12,
                    "sm": 6,
                },
                content=boton_generar,
            ),
            ft.Container(
                col={
                    "xs": 12,
                    "sm": 6,
                },
                content=boton_compartir,
            ),
        ],
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
                botones_informe,
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