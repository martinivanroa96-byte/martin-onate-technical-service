import flet as ft
import flet_camera as fc
import flet_permission_handler as fph


class CameraService:

    def __init__(self, page: ft.Page):
        self.page = page
        self.inicializada = False
        self.camara_seleccionada = None

        self.permission_handler = fph.PermissionHandler()

        # La cámara de Flet funciona en Android, iOS y web,
        # pero no en la aplicación de escritorio para Windows.
        if page.platform == ft.PagePlatform.ANDROID:
            self.camera = fc.Camera(
                expand=True,
                preview_enabled=True,
            )
        else:
            self.camera = None

    def disponible_en_dispositivo(self):
        return self.camera is not None

    async def inicializar(self):
        if not self.disponible_en_dispositivo():
            return False, "La cámara directa estará disponible en Android."

        permiso = await self.permission_handler.request(
            fph.Permission.CAMERA
        )

        if permiso != fph.PermissionStatus.GRANTED:
            return False, "No se concedió permiso para utilizar la cámara."

        camaras = await self.camera.get_available_cameras()

        if not camaras:
            return False, "No se encontró ninguna cámara disponible."

        # Busca preferentemente la cámara trasera.
        camara_trasera = next(
            (
                camara
                for camara in camaras
                if getattr(
                    camara.lens_direction,
                    "value",
                    "",
                ).lower() == "back"
            ),
            None,
        )

        self.camara_seleccionada = camara_trasera or camaras[0]

        await self.camera.initialize(
            description=self.camara_seleccionada,
            resolution_preset=fc.ResolutionPreset.MEDIUM,
            enable_audio=False,
            image_format_group=fc.ImageFormatGroup.JPEG,
        )

        try:
            await self.camera.lock_capture_orientation()
        except RuntimeError:
            pass

        self.inicializada = True

        return True, "Cámara lista."

    async def tomar_foto(self):
        if not self.inicializada or self.camera is None:
            raise RuntimeError("La cámara todavía no está inicializada.")

        foto_bytes = await self.camera.take_picture()

        if not foto_bytes:
            raise RuntimeError("La cámara no devolvió una fotografía.")

        return foto_bytes