import sys
from PyQt6.QtWidgets import QApplication
from ui.login_ui import LoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Cargar estilos globales
    try:
        with open("static/styles/estilos.qss", "r") as archivo:
            app.setStyleSheet(archivo.read())
    except FileNotFoundError:
        print("⚠️ No se encontró el archivo de estilos. Continuando sin CSS...")

    # Lanzar ventana inicial
    ventana = LoginWindow()
    ventana.show()

    sys.exit(app.exec())
