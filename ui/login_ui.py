from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)

from services.auth_service import AuthService
from ui.principal_ui import VentanaPrincipal


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login - Mi App")
        self.setGeometry(200, 200, 300, 250)

        # Logo
        self.logo_label = QLabel()
        pixmap = QPixmap("static/img/logo.png")
        pixmap = pixmap.scaled(
            80, 80,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Widgets usuario/contraseña
        self.label_user = QLabel("Usuario:")
        self.input_user = QLineEdit()

        self.label_pass = QLabel("Contraseña:")
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.EchoMode.Password)

        # Botón login
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
        usuario = self.input_user.text().strip()
        clave = self.input_pass.text().strip()

        if not usuario or not clave:
            QMessageBox.warning(self, "Error", "Debes ingresar usuario y contraseña.")
            return

        try:
            auth_service = AuthService()
            usuario_id = auth_service.login(usuario, clave)

            if usuario_id:
                QMessageBox.information(self, "Éxito", "¡Login exitoso!")
                self.abrir_menu(usuario_id, usuario)
            else:
                QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo verificar login:\n{e}")

    def abrir_menu(self, usuario_id, usuario):
        """Oculta la ventana de login y abre la ventana principal"""
        self.hide()
        self.ventana_principal = VentanaPrincipal(usuario_id, usuario)
        self.ventana_principal.show()