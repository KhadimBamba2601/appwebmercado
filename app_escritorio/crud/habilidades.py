from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QLineEdit, QMessageBox, QDialog, QFormLayout,
    QTextEdit, QComboBox
)
from PyQt6.QtCore import Qt
from typing import Optional, List, Dict, Any
from ui.database import DatabaseManager

class HabilidadDialog(QDialog):
    def __init__(self, parent=None, habilidad_data: Dict[str, Any] = None):
        super().__init__(parent)
        self.habilidad_data = habilidad_data
        self.setup_ui()
        
        # Ajustar tamaño de la ventana
        self.setMinimumWidth(400)
        self.setMinimumHeight(200)
        
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
        self.setWindowTitle("Nueva Habilidad" if not self.habilidad_data else "Editar Habilidad")
        
        layout = QFormLayout()
        
        # Nombre
        self.nombre = QLineEdit()
        if self.habilidad_data:
            self.nombre.setText(self.habilidad_data.get('nombre', ''))
        layout.addRow("Nombre:", self.nombre)
        
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
    
    def get_habilidad_data(self) -> Dict[str, str]:
        """Retorna los datos del formulario como un diccionario"""
        return {
            'nombre': self.nombre.text()
        }

class HabilidadesTab(QWidget):
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.db_manager = db_manager
        self.setup_ui()
        self.load_habilidades()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Search section
        search_layout = QHBoxLayout()
        search_label = QLabel("Buscar:")
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.filter_habilidades)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)
        
        # Buttons
        button_layout = QHBoxLayout()
        add_button = QPushButton("Añadir Habilidad")
        add_button.clicked.connect(self.add_habilidad)
        refresh_button = QPushButton("Actualizar")
        refresh_button.clicked.connect(self.load_habilidades)
        button_layout.addWidget(add_button)
        button_layout.addWidget(refresh_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def load_habilidades(self):
        """Carga las habilidades desde la base de datos"""
        try:
            habilidades = self.db_manager.get_table_data('habilidades')
            self.table.setRowCount(len(habilidades))
            
            for i, habilidad in enumerate(habilidades):
                id_item = QTableWidgetItem(str(habilidad['id']))
                nombre_item = QTableWidgetItem(habilidad['nombre'])
                
                self.table.setItem(i, 0, id_item)
                self.table.setItem(i, 1, nombre_item)
            
            self.table.resizeColumnsToContents()
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al cargar habilidades: {str(e)}")
    
    def filter_habilidades(self):
        """Filtra las habilidades según el texto de búsqueda"""
        search_text = self.search_input.text().lower()
        
        for i in range(self.table.rowCount()):
            nombre = self.table.item(i, 1).text().lower()
            self.table.setRowHidden(i, search_text not in nombre)
    
    def add_habilidad(self):
        """Añade una nueva habilidad"""
        dialog = HabilidadDialog(self)
        if dialog.exec():
            try:
                habilidad_data = dialog.get_habilidad_data()
                self.db_manager.insert_data('habilidades', habilidad_data)
                self.load_habilidades()
                QMessageBox.information(self, "Éxito", "Habilidad añadida correctamente.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error al añadir habilidad: {str(e)}")
    
    def edit_habilidad(self, habilidad_data: Dict[str, Any]):
        """Edita una habilidad existente"""
        dialog = HabilidadDialog(self, habilidad_data)
        if dialog.exec():
            try:
                new_data = dialog.get_habilidad_data()
                self.db_manager.update_data('habilidades', new_data, {'id': habilidad_data['id']})
                self.load_habilidades()
                QMessageBox.information(self, "Éxito", "Habilidad actualizada correctamente.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error al actualizar habilidad: {str(e)}")
    
    def delete_habilidad(self, habilidad_data: Dict[str, Any]):
        """Elimina una habilidad"""
        reply = QMessageBox.question(
            self,
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar la habilidad '{habilidad_data['nombre']}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db_manager.delete_data('habilidades', {'id': habilidad_data['id']})
                self.load_habilidades()
                QMessageBox.information(self, "Éxito", "Habilidad eliminada correctamente.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error al eliminar habilidad: {str(e)}") 