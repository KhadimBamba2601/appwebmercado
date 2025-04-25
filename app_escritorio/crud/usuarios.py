from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QLineEdit, QMessageBox, QDialog, QFormLayout,
    QComboBox, QCheckBox
)
from PyQt6.QtCore import Qt
from typing import Optional, List, Dict, Any
from ui.database import DatabaseManager

class UsuarioDialog(QDialog):
    def __init__(self, parent=None, usuario_data: Dict[str, Any] = None):
        super().__init__(parent)
        self.usuario_data = usuario_data
        self.setup_ui()
        
        # Ajustar tamaño de la ventana
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)
        
        # Centrar la ventana en la pantalla
        self.center_dialog()
    
    def center_dialog(self):
        """Centra el diálogo en la pantalla"""
        screen = self.screen().geometry()
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)
    
    def setup_ui(self):
        self.setWindowTitle("Nuevo Usuario" if not self.usuario_data else "Editar Usuario")
        
        layout = QFormLayout()
        
        # Username
        self.username = QLineEdit()
        if self.usuario_data:
            self.username.setText(self.usuario_data.get('username', ''))
        layout.addRow("Usuario:", self.username)
        
        # Password
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        if self.usuario_data:
            self.password.setPlaceholderText("Dejar en blanco para mantener la contraseña actual")
        layout.addRow("Contraseña:", self.password)
        
        # Email
        self.email = QLineEdit()
        if self.usuario_data:
            self.email.setText(self.usuario_data.get('email', ''))
        layout.addRow("Email:", self.email)
        
        # Role
        self.role = QComboBox()
        self.role.addItems(["admin", "user"])
        if self.usuario_data:
            self.role.setCurrentText(self.usuario_data.get('role', 'user'))
        layout.addRow("Rol:", self.role)
        
        # Active
        self.active = QCheckBox("Usuario activo")
        if self.usuario_data:
            self.active.setChecked(self.usuario_data.get('active', True))
        else:
            self.active.setChecked(True)
        layout.addRow("", self.active)
        
        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Guardar")
        save_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addRow("", button_layout)
        
        self.setLayout(layout)
    
    def get_usuario_data(self) -> Dict[str, Any]:
        """Retorna los datos del formulario como un diccionario"""
        data = {
            'username': self.username.text(),
            'email': self.email.text(),
            'role': self.role.currentText(),
            'active': self.active.isChecked()
        }
        
        # Solo incluir la contraseña si se ha proporcionado una nueva
        if self.password.text():
            data['password'] = self.password.text()
        
        return data

class UsuariosTab(QWidget):
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.db_manager = db_manager
        self.setup_ui()
        self.load_usuarios()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Search section
        search_layout = QHBoxLayout()
        search_label = QLabel("Buscar:")
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.filter_usuarios)
        
        role_label = QLabel("Rol:")
        self.role_filter = QComboBox()
        self.role_filter.addItems(["Todos", "admin", "user"])
        self.role_filter.currentTextChanged.connect(self.filter_usuarios)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(role_label)
        search_layout.addWidget(self.role_filter)
        layout.addLayout(search_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Usuario", "Email", "Rol", "Activo"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)
        
        # Buttons
        button_layout = QHBoxLayout()
        add_button = QPushButton("Añadir Usuario")
        add_button.clicked.connect(self.add_usuario)
        refresh_button = QPushButton("Actualizar")
        refresh_button.clicked.connect(self.load_usuarios)
        button_layout.addWidget(add_button)
        button_layout.addWidget(refresh_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def load_usuarios(self):
        """Carga los usuarios desde la base de datos"""
        try:
            usuarios = self.db_manager.get_table_data('usuarios')
            self.table.setRowCount(len(usuarios))
            
            for i, usuario in enumerate(usuarios):
                id_item = QTableWidgetItem(str(usuario['id']))
                username_item = QTableWidgetItem(usuario['username'])
                email_item = QTableWidgetItem(usuario['email'])
                role_item = QTableWidgetItem(usuario['role'])
                active_item = QTableWidgetItem("Sí" if usuario['active'] else "No")
                
                self.table.setItem(i, 0, id_item)
                self.table.setItem(i, 1, username_item)
                self.table.setItem(i, 2, email_item)
                self.table.setItem(i, 3, role_item)
                self.table.setItem(i, 4, active_item)
            
            self.table.resizeColumnsToContents()
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al cargar usuarios: {str(e)}")
    
    def filter_usuarios(self):
        """Filtra los usuarios según el texto de búsqueda y el rol seleccionado"""
        search_text = self.search_input.text().lower()
        role_filter = self.role_filter.currentText()
        
        for i in range(self.table.rowCount()):
            username = self.table.item(i, 1).text().lower()
            email = self.table.item(i, 2).text().lower()
            role = self.table.item(i, 3).text()
            
            # Aplicar filtros
            show_row = (search_text in username or search_text in email)
            if role_filter != "Todos":
                show_row = show_row and role == role_filter
            
            self.table.setRowHidden(i, not show_row)
    
    def add_usuario(self):
        """Añade un nuevo usuario"""
        dialog = UsuarioDialog(self)
        if dialog.exec():
            try:
                usuario_data = dialog.get_usuario_data()
                self.db_manager.insert_data('usuarios', usuario_data)
                self.load_usuarios()
                QMessageBox.information(self, "Éxito", "Usuario añadido correctamente.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error al añadir usuario: {str(e)}")
    
    def edit_usuario(self, usuario_data: Dict[str, Any]):
        """Edita un usuario existente"""
        dialog = UsuarioDialog(self, usuario_data)
        if dialog.exec():
            try:
                new_data = dialog.get_usuario_data()
                self.db_manager.update_data('usuarios', new_data, {'id': usuario_data['id']})
                self.load_usuarios()
                QMessageBox.information(self, "Éxito", "Usuario actualizado correctamente.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error al actualizar usuario: {str(e)}")
    
    def delete_usuario(self, usuario_data: Dict[str, Any]):
        """Elimina un usuario"""
        reply = QMessageBox.question(
            self,
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar el usuario '{usuario_data['username']}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db_manager.delete_data('usuarios', {'id': usuario_data['id']})
                self.load_usuarios()
                QMessageBox.information(self, "Éxito", "Usuario eliminado correctamente.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error al eliminar usuario: {str(e)}") 