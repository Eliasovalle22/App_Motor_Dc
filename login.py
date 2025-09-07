import sys
import bcrypt
import mysql.connector
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QMessageBox, QMainWindow
)

# -------- Ventana principal --------
class VentanaPrincipal(QMainWindow):
    def __init__(self, usuario):
        super().__init__()
        self.setWindowTitle("Menú Principal")
        self.setGeometry(250, 250, 500, 300)

        label = QLabel(f"Bienvenido, {usuario}", self)
        label.setGeometry(50, 50, 300, 40)

# -------- Ventana de login --------
class Login(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login - Mi App")
        self.setGeometry(200, 200, 300, 150)

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
                password="root",
                database="app_motor"
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

    # Cargar CSS
    with open("estilos.qss", "r") as archivo:
        app.setStyleSheet(archivo.read())
        
    ventana = Login()
    ventana.show()
    sys.exit(app.exec())
