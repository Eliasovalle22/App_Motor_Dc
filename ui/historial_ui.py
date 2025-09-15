from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QHeaderView, QTableWidgetItem, QLineEdit
from PyQt6.QtGui import QGuiApplication
from datetime import datetime
import pytz
from models.accion_model import Accion


def centrar_ventana(ventana):
    """Centra una ventana en la pantalla principal."""
    pantalla = QGuiApplication.primaryScreen().geometry()
    tamaño = ventana.frameGeometry()
    tamaño.moveCenter(pantalla.center())
    ventana.move(tamaño.topLeft())


class VentanaHistorial(QWidget):
    def __init__(self, usuario_id):
        super().__init__()
        self.usuario_id = usuario_id

        self.setWindowTitle("Historial de acciones")
        self.setGeometry(300, 300, 700, 500)
        centrar_ventana(self)

        # Buscador
        self.buscador = QLineEdit()
        self.buscador.setPlaceholderText("🔍 Buscar en historial...")
        self.buscador.textChanged.connect(self.filtrar_tabla)

        # Tabla
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(
            ["ID", "Dispositivo", "Acción", "Fecha/Hora"]
        )
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Mejoras visuales
        self.tabla.setAlternatingRowColors(False)  # sin filas alternadas
        self.tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabla.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows)
        self.tabla.setSortingEnabled(True)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.buscador)
        layout.addWidget(self.tabla)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        self.setLayout(layout)

        # Cargar datos desde el modelo
        self.cargar_datos()

    def cargar_datos(self):
        """Obtiene el historial de la BD y lo carga en la tabla."""
        try:
            self.filas = Accion.obtener_por_usuario(
                self.usuario_id)  # guardar en memoria
            self.mostrar_datos(self.filas)
        except Exception as e:
            print(f"Error cargando historial: {e}")

    def mostrar_datos(self, filas):
        tz_Colombia = pytz.timezone("America/Bogota")
        self.tabla.setRowCount(len(filas))
        for row_idx, fila in enumerate(filas):
            # convertir fecha_hora a zona horaria Colombia
            fecha_utc = fila.get("fecha_hora", "")
            if isinstance(fecha_utc, datetime):
                fecha_local = fecha_utc.replace(tzinfo=pytz.UTC).astimezone(tz_Colombia)
                fecha_str = fecha_local.strftime("%d/%m/%Y %H:%M:%S")
            else:
                fecha_str = str(fecha_utc)

            self.tabla.setItem(row_idx, 0, QTableWidgetItem(str(fila.get("id", ""))))
            self.tabla.setItem(row_idx, 1, QTableWidgetItem(str(fila.get("dispositivo", ""))))
            self.tabla.setItem(row_idx, 2, QTableWidgetItem(str(fila.get("accion", ""))))
            self.tabla.setItem(row_idx, 3, QTableWidgetItem(fecha_str))

        self.tabla.resizeRowsToContents()

    def filtrar_tabla(self, texto):
        """Filtra las filas de la tabla por cualquier coincidencia con el texto."""
        texto = texto.lower()
        filtradas = [
            fila
            for fila in self.filas
            if texto in str(fila.get("id", "")).lower()
            or texto in str(fila.get("dispositivo", "")).lower()
            or texto in str(fila.get("accion", "")).lower()
            or texto in str(fila.get("fecha_hora", "")).lower()
        ]
        self.mostrar_datos(filtradas)
