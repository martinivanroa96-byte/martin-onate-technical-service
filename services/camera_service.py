import flet as ft
import flet_camera as fc
import flet_permission_handler as fph


class CameraService:

    def __init__(self, page: ft.Page):
        self.page = page
        self.inicializada = False
        self.controles_agregados = False
        self.camara_seleccionada = None

        # Los controles nativos de cámara y permisos se crean
        # únicamente cuando la aplicación se ejecuta en Android.
        if page.platform == ft.PagePlatform.ANDROID:
            self.permission_handler = fph.PermissionHandler()

            self.camera = fc.Camera(
                preview_enabled=True,
            )
        else:
            self.permission_handler = None
            self.camera = None

        self.agregar_controles_a_pagina()

    def agregar_controles_a_pagina(self):
        """
        Agrega Camera y PermissionHandler al árbol de controles.

        Los controles deben estar agregados a la página antes de utilizar
        sus métodos nativos en Android.
        """
        if self.controles_agregados:
            return

        # En Windows no se agrega ningún control nativo.
        if self.page.platform != ft.PagePlatform.ANDROID:
            self.controles_agregados = True
            return

        if (
            self.permission_handler is not None
            and self.permission_handler not in self.page.overlay
        ):
            self.page.overlay.append(
                self.permission_handler
            )

        if (
            self.camera is not None
            and self.camera not in self.page.overlay
        ):
            self.page.overlay.append(
                self.camera
            )

        self.controles_agregados = True
        self.page.update()

    def disponible_en_dispositivo(self):
        return (
            self.page.platform == ft.PagePlatform.ANDROID
            and self.camera is not None
            and self.permission_handler is not None
        )

    async def inicializar(self):
        if not self.disponible_en_dispositivo():
            return (
                False,
                "La cámara directa solo está disponible en Android.",
            )

        try:
            # Garantiza que los controles estén montados.
            self.agregar_controles_a_pagina()

            permiso = await self.permission_handler.request(
                fph.Permission.CAMERA
            )

            if permiso != fph.PermissionStatus.GRANTED:
                return (
                    False,
                    "No se concedió permiso para utilizar la cámara.",
                )

            camaras = await self.camera.get_available_cameras()

            if not camaras:
                return (
                    False,
                    "No se encontró ninguna cámara disponible.",
                )

            # Selecciona preferentemente la cámara trasera.
            camara_trasera = next(
                (
                    camara
                    for camara in camaras
                    if str(
                        getattr(
                            camara.lens_direction,
                            "value",
                            camara.lens_direction,
                        )
                    ).lower()
                    in (
                        "back",
                        "camera_lens_direction.back",
                    )
                ),
                None,
            )

            self.camara_seleccionada = (
                camara_trasera
                or camaras[0]
            )

            await self.camera.initialize(
                description=self.camara_seleccionada,
                resolution_preset=fc.ResolutionPreset.MEDIUM,
                enable_audio=False,
                image_format_group=fc.ImageFormatGroup.JPEG,
            )

            try:
                await self.camera.lock_capture_orientation()
            except Exception:
                # Algunos dispositivos no permiten bloquear la orientación.
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
                f"No se pudo inicializar la cámara: {error}",
            )

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
        Libera los recursos utilizados por la cámara.
        """
        if self.camera is None:
            return

        try:
            if self.inicializada:
                await self.camera.dispose()
        except Exception:
            pass

        self.inicializada = False