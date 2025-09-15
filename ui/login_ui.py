from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QGuiApplication
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)

from services.auth_service import AuthService
from ui.principal_ui import VentanaPrincipal


def centrar_ventana(ventana):
    """Centra una ventana en la pantalla principal."""
    pantalla = QGuiApplication.primaryScreen().geometry()
    tamaño = ventana.frameGeometry()
    tamaño.moveCenter(pantalla.center())
    ventana.move(tamaño.topLeft())


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login - Mi App")
        self.setFixedSize(350, 380)
        centrar_ventana(self)

        # ======================
        #   LOGO
        # ======================
        self.logo_label = QLabel()
        pixmap = QPixmap("static/img/logo.png")
        pixmap = pixmap.scaled(
            100, 100,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ======================
        #   CAMPOS LOGIN
        # ======================
        self.input_user = QLineEdit()
        self.input_user.setPlaceholderText("Ingrese su usuario")

        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_pass.setPlaceholderText("Ingrese su contraseña")

        # ======================
        #   BOTÓN LOGIN
        # ======================
        self.boton_login = QPushButton("Iniciar sesión")
        self.boton_login.clicked.connect(self.verificar_login)

        # ======================
        #   LAYOUT
        # ======================
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 25, 40, 25)  # margen interno

        layout.addWidget(
            self.logo_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.input_user)
        layout.addSpacing(10)
        layout.addWidget(self.input_pass)
        layout.addSpacing(20)
        layout.addWidget(self.boton_login)

        self.setLayout(layout)

    # ======================
    #   MÉTODOS
    # ======================
    def verificar_login(self):
        usuario = self.input_user.text().strip()
        clave = self.input_pass.text().strip()

        if not usuario or not clave:
            QMessageBox.warning(
                self, "Error", "Debes ingresar usuario y contraseña.")
            return

        try:
            auth_service = AuthService()
            usuario_id = auth_service.login(usuario, clave)

            if usuario_id:
                QMessageBox.information(self, "Éxito", "¡Login exitoso!")
                self.abrir_menu(usuario_id, usuario)
            else:
                QMessageBox.warning(
                    self, "Error", "Usuario o contraseña incorrectos.")
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"No se pudo verificar login:\n{e}")

    def abrir_menu(self, usuario_id, usuario):
        """Oculta la ventana de login y abre la ventana principal"""
        self.hide()
        self.ventana_principal = VentanaPrincipal(usuario_id, usuario)
        self.ventana_principal.show()
