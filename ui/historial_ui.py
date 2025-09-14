from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QHeaderView, QTableWidgetItem
from models.accion_model import Accion


class VentanaHistorial(QWidget):
    def __init__(self, usuario_id):
        super().__init__()
        self.usuario_id = usuario_id

        self.setWindowTitle("Historial de acciones")
        self.setGeometry(300, 300, 700, 500)

        # Tabla
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["ID", "Dispositivo", "Acción", "Fecha/Hora"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.tabla)
        self.setLayout(layout)

        # Cargar datos desde el modelo
        self.cargar_datos()

    def cargar_datos(self):
        """Obtiene el historial de la BD y lo carga en la tabla."""
        try:
            filas = Accion.obtener_por_usuario(self.usuario_id)

            self.tabla.setRowCount(len(filas))
            for row_idx, fila in enumerate(filas):
                self.tabla.setItem(row_idx, 0, QTableWidgetItem(str(fila.get("id", ""))))
                self.tabla.setItem(row_idx, 1, QTableWidgetItem(str(fila.get("dispositivo", ""))))
                self.tabla.setItem(row_idx, 2, QTableWidgetItem(str(fila.get("accion", ""))))
                self.tabla.setItem(row_idx, 3, QTableWidgetItem(str(fila.get("fecha_hora", ""))))
        except Exception as e:
            print(f"Error cargando historial: {e}")
