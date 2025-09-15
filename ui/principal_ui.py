from PyQt6.QtGui import QGuiApplication, QFont
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QMessageBox, QGroupBox
)
from PyQt6.QtCore import Qt
from ui.historial_ui import VentanaHistorial
from services.motor_service import MotorService
from services.led_service import LedService
from services.serial_listener_service import SerialListener


def centrar_ventana(ventana):
    """Centra una ventana en la pantalla principal."""
    pantalla = QGuiApplication.primaryScreen().geometry()
    tamaño = ventana.frameGeometry()
    tamaño.moveCenter(pantalla.center())
    ventana.move(tamaño.topLeft())


class VentanaPrincipal(QMainWindow):
    def __init__(self, usuario_id, usuario):
        super().__init__()
        self.usuario_id = usuario_id
        self.usuario = usuario

        self.setWindowTitle("Control del Motor DC y LEDs")
        self.setFixedSize(450, 550)
        centrar_ventana(self)

        # ======================
        #   SERVICIOS
        # ======================
        self.motor_service = MotorService()
        self.led_service = LedService(self.motor_service.arduino)

        if self.motor_service.arduino:
            self.serial_listener = SerialListener(
                self.motor_service.arduino, self, self.usuario_id
            )
            self.serial_listener.start()

        # ======================
        #   LABEL DE BIENVENIDA
        # ======================
        self.label_bienvenida = QLabel(f"Bienvenido, {usuario}")
        self.label_bienvenida.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.label_bienvenida.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ======================
        #   MOTOR
        # ======================
        self.label_estado_motor = QLabel("............")
        self.label_estado_motor.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.boton_on = QPushButton("Encender")
        self.boton_off = QPushButton("Apagar")
        self.boton_on.clicked.connect(self.encender_motor)
        self.boton_off.clicked.connect(self.apagar_motor)

        motor_layout = QVBoxLayout()
        motor_layout.addWidget(self.label_estado_motor)
        botones_motor = QHBoxLayout()
        botones_motor.addWidget(self.boton_on)
        botones_motor.addWidget(self.boton_off)
        motor_layout.addLayout(botones_motor)

        motor_box = QGroupBox("⚙️ Motor")
        motor_box.setLayout(motor_layout)

        # ======================
        #   LED VERDE
        # ======================
        self.label_led_verde = QLabel("............")
        self.label_led_verde.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.boton_led_verde_on = QPushButton("Encender")
        self.boton_led_verde_off = QPushButton("Apagar")
        self.boton_led_verde_on.clicked.connect(self.encender_led_verde)
        self.boton_led_verde_off.clicked.connect(self.apagar_led_verde)

        led_verde_layout = QVBoxLayout()
        led_verde_layout.addWidget(self.label_led_verde)
        botones_verde = QHBoxLayout()
        botones_verde.addWidget(self.boton_led_verde_on)
        botones_verde.addWidget(self.boton_led_verde_off)
        led_verde_layout.addLayout(botones_verde)

        led_verde_box = QGroupBox("🟢 LED Verde")
        led_verde_box.setLayout(led_verde_layout)

        # ======================
        #   LED ROJO
        # ======================
        self.label_led_rojo = QLabel("............")
        self.label_led_rojo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.boton_led_rojo_on = QPushButton("Encender")
        self.boton_led_rojo_off = QPushButton("Apagar")
        self.boton_led_rojo_on.clicked.connect(self.encender_led_rojo)
        self.boton_led_rojo_off.clicked.connect(self.apagar_led_rojo)

        led_rojo_layout = QVBoxLayout()
        led_rojo_layout.addWidget(self.label_led_rojo)
        botones_rojo = QHBoxLayout()
        botones_rojo.addWidget(self.boton_led_rojo_on)
        botones_rojo.addWidget(self.boton_led_rojo_off)
        led_rojo_layout.addLayout(botones_rojo)

        led_rojo_box = QGroupBox("🔴 LED Rojo")
        led_rojo_box.setLayout(led_rojo_layout)

        # ======================
        #   HISTORIAL
        # ======================
        self.boton_historial = QPushButton("📜 Ver historial")
        self.boton_historial.clicked.connect(self.abrir_historial)

        # ======================
        #   LAYOUT GENERAL
        # ======================
        central = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(15)

        layout.addWidget(self.label_bienvenida)
        layout.addWidget(motor_box)
        layout.addWidget(led_verde_box)
        layout.addWidget(led_rojo_box)
        layout.addSpacing(15)
        layout.addWidget(self.boton_historial, alignment=Qt.AlignmentFlag.AlignCenter)

        central.setLayout(layout)
        self.setCentralWidget(central)

    def encender_motor(self):
        try:
            self.motor_service.encender(self.usuario_id)
            self.actualizar_estado_motor("ENCENDIDO")
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"No se pudo encender el motor: {e}")

    def apagar_motor(self):
        try:
            self.motor_service.apagar(self.usuario_id)
            self.actualizar_estado_motor("APAGADO")
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"No se pudo apagar el motor: {e}")

    def encender_led_verde(self):
        try:
            self.led_service.encender_verde(self.usuario_id)
            self.actualizar_estado_led_verde("ENCENDIDO")
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"No se pudo encender LED verde: {e}")

    def apagar_led_verde(self):
        try:
            self.led_service.apagar_verde(self.usuario_id)
            self.actualizar_estado_led_verde("APAGADO")
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"No se pudo apagar LED verde: {e}")

    def encender_led_rojo(self):
        try:
            self.led_service.encender_rojo(self.usuario_id)
            self.actualizar_estado_led_rojo("ENCENDIDO")
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"No se pudo encender LED rojo: {e}")

    def apagar_led_rojo(self):
        try:
            self.led_service.apagar_rojo(self.usuario_id)
            self.actualizar_estado_led_rojo("APAGADO")
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"No se pudo apagar LED rojo: {e}")

    # =========================
    #   Funciones Auxiliares
    # =========================
    def actualizar_estado_motor(self, texto_estado):
        self.label_estado_motor.setText(texto_estado)

    def actualizar_estado_led_verde(self, texto_estado):
        self.label_led_verde.setText(texto_estado)

    def actualizar_estado_led_rojo(self, texto_estado):
        self.label_led_rojo.setText(texto_estado)

    def abrir_historial(self):
        self.ventana_historial = VentanaHistorial(self.usuario_id)
        self.ventana_historial.show()
