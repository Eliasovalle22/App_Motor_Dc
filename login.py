import sys
import bcrypt
import mysql.connector
import serial
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QMessageBox, QMainWindow
)

# -------- Ventana principal (Control motor) --------
class VentanaPrincipal(QMainWindow):
    def __init__(self, usuario):
        super().__init__()
        self.setWindowTitle("Control del Motor DC")
        self.setGeometry(250, 250, 400, 300)

        # Conexión con Arduino/ESP32
        try:
            self.arduino = serial.Serial("COM3", 9600)  # ⚠️ Cambia COM3 por tu puerto
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo conectar al puerto serie: {e}")
            self.arduino = None

        # Widgets
        self.label_bienvenida = QLabel(f"Bienvenido, {usuario}")
        self.label_estado = QLabel("Estado del motor: Apagado")

        self.boton_on = QPushButton("Encender motor")
        self.boton_off = QPushButton("Apagar motor")

        # Eventos
        self.boton_on.clicked.connect(self.encender_motor)
        self.boton_off.clicked.connect(self.apagar_motor)

        # Layout
        central = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.label_bienvenida)
        layout.addWidget(self.label_estado)
        layout.addWidget(self.boton_on)
        layout.addWidget(self.boton_off)
        central.setLayout(layout)
        self.setCentralWidget(central)

    def encender_motor(self):
        if self.arduino:
            self.arduino.write(b"ON\n")
        self.label_estado.setText("Estado del motor: Encendido")

    def apagar_motor(self):
        if self.arduino:
            self.arduino.write(b"OFF\n")
        self.label_estado.setText("Estado del motor: Apagado")


# -------- Ventana de login --------
class Login(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login - Mi App")
        self.setGeometry(200, 200, 300, 250)

        # Logo
        self.logo_label = QLabel()
        pixmap = QPixmap("img/logo.png")
        pixmap = pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Widgets
        self.label_user = QLabel("Usuario:")
        self.input_user = QLineEdit()

        self.label_pass = QLabel("Contraseña:")
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.EchoMode.Password)

        self.boton_login = QPushButton("Iniciar sesión")
        self.boton_login.clicked.connect(self.verificar_login)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.logo_label)
        layout.addWidget(self.label_user)
        layout.addWidget(self.input_user)
        layout.addWidget(self.label_pass)
        layout.addWidget(self.input_pass)
        layout.addWidget(self.boton_login)

        self.setLayout(layout)

    def verificar_login(self):
        usuario = self.input_user.text()
        clave = self.input_pass.text().encode("utf-8")

        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="2805",     # 
                database="db_motor"
            )
            cursor = conexion.cursor()
            cursor.execute("SELECT password FROM usuarios WHERE username=%s", (usuario,))
            resultado = cursor.fetchone()

            if resultado and bcrypt.checkpw(clave, resultado[0].encode("utf-8")):
                QMessageBox.information(self, "Éxito", "¡Login exitoso!")
                self.abrir_menu(usuario)
            else:
                QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos.")

            cursor.close()
            conexion.close()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Error DB", f"Error conectando a MySQL: {err}")

    def abrir_menu(self, usuario):
        self.hide()
        self.ventana_principal = VentanaPrincipal(usuario)
        self.ventana_principal.show()


# -------- Main --------
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Cargar CSS externo
    with open("styles/estilos.qss", "r") as archivo:
        app.setStyleSheet(archivo.read())

    ventana = Login()
    ventana.show()
    sys.exit(app.exec())
