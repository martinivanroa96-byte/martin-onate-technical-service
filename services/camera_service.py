import flet as ft
import flet_camera as fc
import flet_permission_handler as fph


class CameraService:

    def __init__(self, page: ft.Page):
        self.page = page

        self.inicializada = False
        self.inicializando = False
        self.camara_seleccionada = None

        self.permission_handler = None
        self.camera = None

        if self.es_android():
            self.permission_handler = fph.PermissionHandler()

            self.camera = fc.Camera(
                preview_enabled=True,
                width=360,
                height=480,
            )

            self.agregar_servicio_permisos()

    def es_android(self) -> bool:
        return (
            self.page.platform
            == ft.PagePlatform.ANDROID
        )

    def agregar_servicio_permisos(self):
        """
        PermissionHandler es un servicio de Flet, por lo que
        debe agregarse a page.services y no a page.overlay.
        """
        if not self.es_android():
            return

        if self.permission_handler is None:
            return

        if (
            self.permission_handler
            not in self.page.services
        ):
            self.page.services.append(
                self.permission_handler
            )

            self.page.update()

    def obtener_preview(self):
        """
        Devuelve el control Camera para colocarlo dentro
        de la ventana de vista previa.

        Importante:
        nuevo_servicio.py debe mostrar este control en la
        página antes de llamar a inicializar().
        """
        return self.camera

    def disponible_en_dispositivo(self) -> bool:
        return (
            self.es_android()
            and self.camera is not None
            and self.permission_handler is not None
        )

    async def solicitar_permiso(self):
        if not self.disponible_en_dispositivo():
            return (
                False,
                "La cámara directa solo está disponible en Android.",
            )

        try:
            self.agregar_servicio_permisos()

            permiso = (
                await self.permission_handler.request(
                    fph.Permission.CAMERA
                )
            )

            if permiso == fph.PermissionStatus.GRANTED:
                return (
                    True,
                    "Permiso de cámara concedido.",
                )

            if (
                permiso
                == fph.PermissionStatus.PERMANENTLY_DENIED
            ):
                return (
                    False,
                    (
                        "El permiso de cámara fue bloqueado. "
                        "Debes habilitarlo desde la configuración "
                        "de aplicaciones de Android."
                    ),
                )

            return (
                False,
                "No se concedió permiso para utilizar la cámara.",
            )

        except Exception as error:
            return (
                False,
                f"No se pudo solicitar el permiso: {error}",
            )

    async def inicializar(self):
        """
        Inicializa la cámara.

        El control obtenido mediante obtener_preview()
        debe estar visible y agregado a la página antes
        de ejecutar este método.
        """
        if not self.disponible_en_dispositivo():
            return (
                False,
                "La cámara directa solo está disponible en Android.",
            )

        if self.inicializada:
            return (
                True,
                "Cámara lista.",
            )

        if self.inicializando:
            return (
                False,
                "La cámara se está inicializando.",
            )

        self.inicializando = True

        try:
            permiso_correcto, detalle = (
                await self.solicitar_permiso()
            )

            if not permiso_correcto:
                return (
                    False,
                    detalle,
                )

            camaras = (
                await self.camera.get_available_cameras()
            )

            if not camaras:
                return (
                    False,
                    "No se encontró ninguna cámara disponible.",
                )

            camara_trasera = next(
                (
                    camara
                    for camara in camaras
                    if self.es_camara_trasera(camara)
                ),
                None,
            )

            self.camara_seleccionada = (
                camara_trasera
                if camara_trasera is not None
                else camaras[0]
            )

            await self.camera.initialize(
                description=self.camara_seleccionada,
                resolution_preset=(
                    fc.ResolutionPreset.MEDIUM
                ),
                enable_audio=False,
                image_format_group=(
                    fc.ImageFormatGroup.JPEG
                ),
            )

            try:
                await self.camera.lock_capture_orientation()
            except Exception:
                # Algunos dispositivos no permiten bloquear
                # la orientación. No impide tomar fotografías.
                pass

            self.inicializada = True

            return (
                True,
                "Cámara lista.",
            )

        except Exception as error:
            self.inicializada = False

            return (
                False,
                (
                    "No se pudo inicializar la cámara: "
                    f"{error}"
                ),
            )

        finally:
            self.inicializando = False

    def es_camara_trasera(self, camara) -> bool:
        try:
            direccion = getattr(
                camara,
                "lens_direction",
                "",
            )

            valor = getattr(
                direccion,
                "value",
                direccion,
            )

            texto = str(valor).lower()

            return texto in (
                "back",
                "camera_lens_direction.back",
            )

        except Exception:
            return False

    async def tomar_foto(self):
        if self.camera is None:
            raise RuntimeError(
                "La cámara no está disponible en este dispositivo."
            )

        if not self.inicializada:
            raise RuntimeError(
                "La cámara todavía no está inicializada."
            )

        foto_bytes = await self.camera.take_picture()

        if not foto_bytes:
            raise RuntimeError(
                "La cámara no devolvió una fotografía."
            )

        return foto_bytes

    async def cerrar(self):
        """
        Libera la cámara cuando ya no se utilizará.
        """
        if self.camera is None:
            return

        try:
            if self.inicializada:
                await self.camera.dispose()

        except Exception:
            pass

        finally:
            self.inicializada = False
            self.inicializando = False
            self.camara_seleccionada = None