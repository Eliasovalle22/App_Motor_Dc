import threading
import time
from PyQt6.QtCore import QObject, pyqtSignal
from models.accion_model import Accion


class SerialListener(threading.Thread, QObject):
    motor_signal = pyqtSignal(str)
    led_verde_signal = pyqtSignal(str)
    led_rojo_signal = pyqtSignal(str)

    def __init__(self, arduino, ventana, usuario_id):
        threading.Thread.__init__(self, daemon=True)
        QObject.__init__(self)
        self.arduino = arduino
        self.ventana = ventana
        self.usuario_id = usuario_id

        # Conectar señales a la ventana
        self.motor_signal.connect(self.ventana.actualizar_estado_motor)
        self.led_verde_signal.connect(self.ventana.actualizar_estado_led_verde)
        self.led_rojo_signal.connect(self.ventana.actualizar_estado_led_rojo)

    def run(self):
        while True:
            try:
                if self.arduino and self.arduino.in_waiting > 0:
                    raw = self.arduino.readline()
                    mensaje = raw.decode("utf-8", errors="ignore").strip()

                    # Ignorar mensajes vacíos o basura
                    if not mensaje or ":" not in mensaje:
                        continue

                    self.procesar_mensaje(mensaje)

                time.sleep(0.1)

            except Exception as e:
                print(f"⚠️ Error en escucha serial: {e}")
                # No rompemos el bucle, seguimos escuchando
                continue

    def procesar_mensaje(self, mensaje):
        """Procesa mensajes del ESP32"""
        try:
            dispositivo, accion = mensaje.split(":")
        except ValueError:
            return  # Ignorar si no cumple formato esperado

        # Guardar en DB
        Accion.registrar(self.usuario_id, dispositivo, accion)

        # Emitir señal en lugar de tocar la UI directamente
        if dispositivo == "MOTOR":
            self.motor_signal.emit("ENCENDIDO" if accion == "ENCENDER" else "APAGADO")
        elif dispositivo == "LED_VERDE":
            self.led_verde_signal.emit("ENCENDIDO" if accion == "ENCENDER" else "APAGADO")
        elif dispositivo == "LED_ROJO":
            self.led_rojo_signal.emit("ENCENDIDO" if accion == "ENCENDER" else "APAGADO")
