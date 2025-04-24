from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                            QTableWidget, QTableWidgetItem, QLabel, QLineEdit,
                            QFormLayout, QDialog, QTextEdit)
from PyQt6.QtCore import Qt
from ..crud.models import Habilidad

class HabilidadDialog(QDialog):
    def __init__(self, parent=None, habilidad=None):
        super().__init__(parent)
        self.habilidad = habilidad
        self.setWindowTitle("Nueva Habilidad" if not habilidad else "Editar Habilidad")
        self.setMinimumWidth(400)
        
        layout = QFormLayout(self)
        
        # Campos
        self.nombre = QLineEdit()
        self.descripcion = QTextEdit()
        
        # Añadir campos al layout
        layout.addRow("Nombre:", self.nombre)
        layout.addRow("Descripción:", self.descripcion)
        
        # Botones
        buttons = QHBoxLayout()
        self.btn_guardar = QPushButton("Guardar")
        self.btn_cancelar = QPushButton("Cancelar")
        
        buttons.addWidget(self.btn_guardar)
        buttons.addWidget(self.btn_cancelar)
        layout.addRow(buttons)
        
        # Conectar señales
        self.btn_guardar.clicked.connect(self.accept)
        self.btn_cancelar.clicked.connect(self.reject)
        
        # Si es edición, cargar datos
        if habilidad:
            self.nombre.setText(habilidad[1])
            self.descripcion.setText(habilidad[2])

class HabilidadesWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.habilidad_model = Habilidad()
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Botones de acción
        btn_layout = QHBoxLayout()
        self.btn_nueva = QPushButton("Nueva Habilidad")
        self.btn_editar = QPushButton("Editar")
        self.btn_eliminar = QPushButton("Eliminar")
        
        btn_layout.addWidget(self.btn_nueva)
        btn_layout.addWidget(self.btn_editar)
        btn_layout.addWidget(self.btn_eliminar)
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
        
        # Tabla
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Descripción"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        
        layout.addWidget(self.table)
        
        # Conectar señales
        self.btn_nueva.clicked.connect(self.nueva_habilidad)
        self.btn_editar.clicked.connect(self.editar_habilidad)
        self.btn_eliminar.clicked.connect(self.eliminar_habilidad)

    def load_data(self):
        habilidades = self.habilidad_model.obtener_todas()
        self.table.setRowCount(len(habilidades))
        
        for i, habilidad in enumerate(habilidades):
            for j, valor in enumerate(habilidad):
                item = QTableWidgetItem(str(valor))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(i, j, item)
        
        self.table.resizeColumnsToContents()

    def nueva_habilidad(self):
        dialog = HabilidadDialog(self)
        if dialog.exec():
            self.habilidad_model.crear(
                dialog.nombre.text(),
                dialog.descripcion.toPlainText()
            )
            self.load_data()

    def editar_habilidad(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            return
        
        habilidad = [self.table.item(current_row, i).text() for i in range(3)]
        dialog = HabilidadDialog(self, habilidad)
        
        if dialog.exec():
            self.habilidad_model.actualizar(
                int(habilidad[0]),
                dialog.nombre.text(),
                dialog.descripcion.toPlainText()
            )
            self.load_data()

    def eliminar_habilidad(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            return
        
        habilidad_id = int(self.table.item(current_row, 0).text())
        if self.parent().show_question("Confirmar", "¿Está seguro de eliminar esta habilidad?"):
            self.habilidad_model.eliminar(habilidad_id)
            self.load_data() 