from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                            QTableWidget, QTableWidgetItem, QLabel, QLineEdit,
                            QFormLayout, QDialog, QComboBox)
from PyQt6.QtCore import Qt
from ..crud.models import Usuario

class UsuarioDialog(QDialog):
    def __init__(self, parent=None, usuario=None):
        super().__init__(parent)
        self.usuario = usuario
        self.setWindowTitle("Nuevo Usuario" if not usuario else "Editar Usuario")
        self.setMinimumWidth(400)
        
        layout = QFormLayout(self)
        
        # Campos
        self.username = QLineEdit()
        self.email = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.rol = QComboBox()
        self.rol.addItems(["Administrador", "Gestor de Proyectos", "Colaborador"])
        
        # Añadir campos al layout
        layout.addRow("Usuario:", self.username)
        layout.addRow("Email:", self.email)
        layout.addRow("Contraseña:", self.password)
        layout.addRow("Rol:", self.rol)
        
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
        if usuario:
            self.username.setText(usuario[1])
            self.email.setText(usuario[2])
            self.rol.setCurrentText(usuario[3])
            self.password.setPlaceholderText("Dejar en blanco para mantener la actual")

class UsuariosWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.usuario_model = Usuario()
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Botones de acción
        btn_layout = QHBoxLayout()
        self.btn_nuevo = QPushButton("Nuevo Usuario")
        self.btn_editar = QPushButton("Editar")
        self.btn_eliminar = QPushButton("Eliminar")
        
        btn_layout.addWidget(self.btn_nuevo)
        btn_layout.addWidget(self.btn_editar)
        btn_layout.addWidget(self.btn_eliminar)
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
        
        # Tabla
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Usuario", "Email", "Rol"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        
        layout.addWidget(self.table)
        
        # Conectar señales
        self.btn_nuevo.clicked.connect(self.nuevo_usuario)
        self.btn_editar.clicked.connect(self.editar_usuario)
        self.btn_eliminar.clicked.connect(self.eliminar_usuario)

    def load_data(self):
        usuarios = self.usuario_model.obtener_todos()
        self.table.setRowCount(len(usuarios))
        
        for i, usuario in enumerate(usuarios):
            for j, valor in enumerate(usuario):
                item = QTableWidgetItem(str(valor))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(i, j, item)
        
        self.table.resizeColumnsToContents()

    def nuevo_usuario(self):
        dialog = UsuarioDialog(self)
        if dialog.exec():
            self.usuario_model.crear(
                dialog.username.text(),
                dialog.email.text(),
                dialog.password.text(),
                dialog.rol.currentText()
            )
            self.load_data()

    def editar_usuario(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            return
        
        usuario = [self.table.item(current_row, i).text() for i in range(4)]
        dialog = UsuarioDialog(self, usuario)
        
        if dialog.exec():
            password = dialog.password.text()
            if not password:  # Si la contraseña está vacía, mantener la actual
                password = None
            
            self.usuario_model.actualizar(
                int(usuario[0]),
                dialog.username.text(),
                dialog.email.text(),
                password,
                dialog.rol.currentText()
            )
            self.load_data()

    def eliminar_usuario(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            return
        
        usuario_id = int(self.table.item(current_row, 0).text())
        if self.parent().show_question("Confirmar", "¿Está seguro de eliminar este usuario?"):
            self.usuario_model.eliminar(usuario_id)
            self.load_data() 