from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                            QTableWidget, QTableWidgetItem, QLabel, QLineEdit,
                            QFormLayout, QDialog, QComboBox, QTextEdit)
from PyQt6.QtCore import Qt
from ..crud.models import OfertaEmpleo, Habilidad

class OfertaDialog(QDialog):
    def __init__(self, parent=None, oferta=None):
        super().__init__(parent)
        self.oferta = oferta
        self.setWindowTitle("Nueva Oferta" if not oferta else "Editar Oferta")
        self.setMinimumWidth(400)
        
        layout = QFormLayout(self)
        
        # Campos
        self.titulo = QLineEdit()
        self.empresa = QLineEdit()
        self.ubicacion = QLineEdit()
        self.tipo_trabajo = QComboBox()
        self.tipo_trabajo.addItems(["Tiempo completo", "Tiempo parcial", "Freelance", "Prácticas"])
        self.salario = QLineEdit()
        self.url = QLineEdit()
        self.habilidades = QTextEdit()
        
        # Añadir campos al layout
        layout.addRow("Título:", self.titulo)
        layout.addRow("Empresa:", self.empresa)
        layout.addRow("Ubicación:", self.ubicacion)
        layout.addRow("Tipo de trabajo:", self.tipo_trabajo)
        layout.addRow("Salario:", self.salario)
        layout.addRow("URL:", self.url)
        layout.addRow("Habilidades (una por línea):", self.habilidades)
        
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
        if oferta:
            self.titulo.setText(oferta[1])
            self.empresa.setText(oferta[2])
            self.ubicacion.setText(oferta[3])
            self.tipo_trabajo.setCurrentText(oferta[4])
            self.salario.setText(oferta[5])
            self.url.setText(oferta[6])
            self.habilidades.setText("\n".join(oferta[7] or []))

class OfertasWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.oferta_model = OfertaEmpleo()
        self.habilidad_model = Habilidad()
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Botones de acción
        btn_layout = QHBoxLayout()
        self.btn_nueva = QPushButton("Nueva Oferta")
        self.btn_editar = QPushButton("Editar")
        self.btn_eliminar = QPushButton("Eliminar")
        
        btn_layout.addWidget(self.btn_nueva)
        btn_layout.addWidget(self.btn_editar)
        btn_layout.addWidget(self.btn_eliminar)
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
        
        # Tabla
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Título", "Empresa", "Ubicación", "Tipo", "Salario", "URL", "Habilidades"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        
        layout.addWidget(self.table)
        
        # Conectar señales
        self.btn_nueva.clicked.connect(self.nueva_oferta)
        self.btn_editar.clicked.connect(self.editar_oferta)
        self.btn_eliminar.clicked.connect(self.eliminar_oferta)

    def load_data(self):
        ofertas = self.oferta_model.obtener_todas()
        self.table.setRowCount(len(ofertas))
        
        for i, oferta in enumerate(ofertas):
            for j, valor in enumerate(oferta):
                item = QTableWidgetItem(str(valor))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(i, j, item)
        
        self.table.resizeColumnsToContents()

    def nueva_oferta(self):
        dialog = OfertaDialog(self)
        if dialog.exec():
            habilidades = [h.strip() for h in dialog.habilidades.toPlainText().split("\n") if h.strip()]
            self.oferta_model.crear(
                dialog.titulo.text(),
                dialog.empresa.text(),
                dialog.ubicacion.text(),
                dialog.tipo_trabajo.currentText(),
                dialog.salario.text(),
                habilidades,
                dialog.url.text()
            )
            self.load_data()

    def editar_oferta(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            return
        
        oferta = [self.table.item(current_row, i).text() for i in range(8)]
        dialog = OfertaDialog(self, oferta)
        
        if dialog.exec():
            habilidades = [h.strip() for h in dialog.habilidades.toPlainText().split("\n") if h.strip()]
            self.oferta_model.actualizar(
                int(oferta[0]),
                dialog.titulo.text(),
                dialog.empresa.text(),
                dialog.ubicacion.text(),
                dialog.tipo_trabajo.currentText(),
                dialog.salario.text(),
                habilidades,
                dialog.url.text()
            )
            self.load_data()

    def eliminar_oferta(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            return
        
        oferta_id = int(self.table.item(current_row, 0).text())
        if self.parent().show_question("Confirmar", "¿Está seguro de eliminar esta oferta?"):
            self.oferta_model.eliminar(oferta_id)
            self.load_data() 