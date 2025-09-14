from models.accion_model import Accion


class LedService:
    def __init__(self, arduino):
        self.arduino = arduino

    def encender_verde(self, usuario_id):
        if self.arduino:
            self.arduino.write(b"LED_VERDE_ON\n")
        Accion.registrar(usuario_id, "LED_VERDE", "ENCENDER")

    def apagar_verde(self, usuario_id):
        if self.arduino:
            self.arduino.write(b"LED_VERDE_OFF\n")
        Accion.registrar(usuario_id, "LED_VERDE", "APAGAR")

    def encender_rojo(self, usuario_id):
        if self.arduino:
            self.arduino.write(b"LED_ROJO_ON\n")
        Accion.registrar(usuario_id, "LED_ROJO", "ENCENDER")

    def apagar_rojo(self, usuario_id):
        if self.arduino:
            self.arduino.write(b"LED_ROJO_OFF\n")
        Accion.registrar(usuario_id, "LED_ROJO", "APAGAR")
