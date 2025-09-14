from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from ui.historial_ui import VentanaHistorial
from services.motor_service import MotorService
from services.led_service import LedService


class VentanaPrincipal(QMainWindow):
    def __init__(self, usuario_id, usuario):
        super().__init__()
        self.usuario_id = usuario_id
        self.usuario = usuario

        self.setWindowTitle("Control del Motor DC y LEDs")
        self.setGeometry(250, 250, 400, 500)

        # Instanciar servicios
        self.motor_service = MotorService()
        self.led_service = LedService(self.motor_service.arduino)

        # Widgets
        self.label_bienvenida = QLabel(f"Bienvenido, {usuario}")
        self.label_estado_motor = QLabel("Estado MOTOR: ............")
        self.label_led_verde = QLabel("Estado LED VERDE: ............")
        self.label_led_rojo = QLabel("Estado LED ROJO: ............")

        # Botones Motor
        self.boton_on = QPushButton("Encender motor")
        self.boton_off = QPushButton("Apagar motor")
        self.boton_on.clicked.connect(self.encender_motor)
        self.boton_off.clicked.connect(self.apagar_motor)

        # Botones LED Verde
        self.boton_led_verde_on = QPushButton("Encender LED Verde")
        self.boton_led_verde_off = QPushButton("Apagar LED Verde")
        self.boton_led_verde_on.clicked.connect(self.encender_led_verde)
        self.boton_led_verde_off.clicked.connect(self.apagar_led_verde)

        # Botones LED Rojo
        self.boton_led_rojo_on = QPushButton("Encender LED Rojo")
        self.boton_led_rojo_off = QPushButton("Apagar LED Rojo")
        self.boton_led_rojo_on.clicked.connect(self.encender_led_rojo)
        self.boton_led_rojo_off.clicked.connect(self.apagar_led_rojo)

        # Botón Historial
        self.boton_historial = QPushButton("Ver historial")
        self.boton_historial.clicked.connect(self.abrir_historial)

        # Layout
        central = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.label_bienvenida)
        layout.addWidget(self.label_estado_motor)
        layout.addWidget(self.label_led_verde)
        layout.addWidget(self.label_led_rojo)
        layout.addWidget(self.boton_on)
        layout.addWidget(self.boton_off)
        layout.addWidget(self.boton_led_verde_on)
        layout.addWidget(self.boton_led_verde_off)
        layout.addWidget(self.boton_led_rojo_on)
        layout.addWidget(self.boton_led_rojo_off)
        layout.addWidget(self.boton_historial)
        central.setLayout(layout)
        self.setCentralWidget(central)

    # =========================
    #   MÉTODOS MOTOR
    # =========================
    def encender_motor(self):
        try:
            self.motor_service.encender(self.usuario_id)
            self.actualizar_estado_motor("ENCENDIDO")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo encender el motor: {e}")

    def apagar_motor(self):
        try:
            self.motor_service.apagar(self.usuario_id)
            self.actualizar_estado_motor("APAGADO")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo apagar el motor: {e}")

    # =========================
    #   MÉTODOS LED
    # =========================
    def encender_led_verde(self):
        try:
            self.led_service.encender_verde(self.usuario_id)
            self.actualizar_estado_led_verde("ENCENDIDO")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo encender LED verde: {e}")

    def apagar_led_verde(self):
        try:
            self.led_service.apagar_verde(self.usuario_id)
            self.actualizar_estado_led_verde("APAGADO")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo apagar LED verde: {e}")

    def encender_led_rojo(self):
        try:
            self.led_service.encender_rojo(self.usuario_id)
            self.actualizar_estado_led_rojo("ENCENDIDO")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo encender LED rojo: {e}")

    def apagar_led_rojo(self):
        try:
            self.led_service.apagar_rojo(self.usuario_id)
            self.actualizar_estado_led_rojo("APAGADO")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo apagar LED rojo: {e}")

    # =========================
    #   Funciones Auxiliares
    # =========================
    def actualizar_estado_motor(self, texto_estado):
        """Permite que servicios actualicen el estado mostrado en UI."""
        self.label_estado_motor.setText(f"Estado MOTOR: {texto_estado}")

    def actualizar_estado_led_verde(self, texto_estado):
        """Permite que servicios actualicen el estado mostrado en UI."""
        self.label_led_verde.setText(f"Estado LED VERDE: {texto_estado}")

    def actualizar_estado_led_rojo(self, texto_estado):
        """Permite que servicios actualicen el estado mostrado en UI."""
        self.label_led_rojo.setText(f"Estado LED ROJO: {texto_estado}")

    def abrir_historial(self):
        self.ventana_historial = VentanaHistorial(self.usuario_id)
        self.ventana_historial.show()
