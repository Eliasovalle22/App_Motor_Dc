import serial
from models.accion_model import Accion


class MotorService:
    def __init__(self, port="COM5", baudrate=9600):
        try:
            self.arduino = serial.Serial(port, baudrate)
        except Exception as e:
            print(f"⚠️ No se pudo conectar al puerto {port}: {e}")
            self.arduino = None

    def encender(self, usuario_id):
        if self.arduino:
            self.arduino.write(b"ON\n")
        Accion.registrar(usuario_id, "MOTOR", "ENCENDER")

    def apagar(self, usuario_id):
        if self.arduino:
            self.arduino.write(b"OFF\n")
        Accion.registrar(usuario_id, "MOTOR", "APAGAR")
