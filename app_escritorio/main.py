import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
                           QLabel, QLineEdit, QComboBox, QMessageBox, QTabWidget)
from PyQt6.QtCore import Qt
import psycopg2
from datetime import datetime

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Datos del Mercado Laboral")
        self.setGeometry(100, 100, 1200, 800)
        
        # Conexión a la base de datos
        self.conn = psycopg2.connect(
            dbname="appwebmercado",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        
        # Widget principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Layout principal
        layout = QVBoxLayout()
        main_widget.setLayout(layout)
        
        # Tabs para diferentes entidades
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # Tab de Ofertas de Empleo
        tab_ofertas = QWidget()
        tabs.addTab(tab_ofertas, "Ofertas de Empleo")
        self.setup_ofertas_tab(tab_ofertas)
        
        # Tab de Habilidades
        tab_habilidades = QWidget()
        tabs.addTab(tab_habilidades, "Habilidades")
        self.setup_habilidades_tab(tab_habilidades)
        
        # Tab de Usuarios
        tab_usuarios = QWidget()
        tabs.addTab(tab_usuarios, "Usuarios")
        self.setup_usuarios_tab(tab_usuarios)
        
    def setup_ofertas_tab(self, tab):
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Formulario
        form_layout = QHBoxLayout()
        layout.addLayout(form_layout)
        
        # Campos del formulario
        self.titulo_edit = QLineEdit()
        self.empresa_edit = QLineEdit()
        self.ubicacion_edit = QLineEdit()
        self.tipo_trabajo_edit = QLineEdit()
        self.salario_min_edit = QLineEdit()
        self.salario_max_edit = QLineEdit()
        
        form_layout.addWidget(QLabel("Título:"))
        form_layout.addWidget(self.titulo_edit)
        form_layout.addWidget(QLabel("Empresa:"))
        form_layout.addWidget(self.empresa_edit)
        form_layout.addWidget(QLabel("Ubicación:"))
        form_layout.addWidget(self.ubicacion_edit)
        
        # Botones
        buttons_layout = QHBoxLayout()
        layout.addLayout(buttons_layout)
        
        add_button = QPushButton("Añadir")
        add_button.clicked.connect(self.add_oferta)
        buttons_layout.addWidget(add_button)
        
        update_button = QPushButton("Actualizar")
        update_button.clicked.connect(self.update_oferta)
        buttons_layout.addWidget(update_button)
        
        delete_button = QPushButton("Eliminar")
        delete_button.clicked.connect(self.delete_oferta)
        buttons_layout.addWidget(delete_button)
        
        # Tabla
        self.ofertas_table = QTableWidget()
        layout.addWidget(self.ofertas_table)
        self.load_ofertas()
        
    def setup_habilidades_tab(self, tab):
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Formulario
        form_layout = QHBoxLayout()
        layout.addLayout(form_layout)
        
        self.habilidad_nombre_edit = QLineEdit()
        self.habilidad_categoria_edit = QLineEdit()
        
        form_layout.addWidget(QLabel("Nombre:"))
        form_layout.addWidget(self.habilidad_nombre_edit)
        form_layout.addWidget(QLabel("Categoría:"))
        form_layout.addWidget(self.habilidad_categoria_edit)
        
        # Botones
        buttons_layout = QHBoxLayout()
        layout.addLayout(buttons_layout)
        
        add_button = QPushButton("Añadir")
        add_button.clicked.connect(self.add_habilidad)
        buttons_layout.addWidget(add_button)
        
        update_button = QPushButton("Actualizar")
        update_button.clicked.connect(self.update_habilidad)
        buttons_layout.addWidget(update_button)
        
        delete_button = QPushButton("Eliminar")
        delete_button.clicked.connect(self.delete_habilidad)
        buttons_layout.addWidget(delete_button)
        
        # Tabla
        self.habilidades_table = QTableWidget()
        layout.addWidget(self.habilidades_table)
        self.load_habilidades()
        
    def setup_usuarios_tab(self, tab):
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Formulario
        form_layout = QHBoxLayout()
        layout.addLayout(form_layout)
        
        self.usuario_nombre_edit = QLineEdit()
        self.usuario_email_edit = QLineEdit()
        self.usuario_rol_combo = QComboBox()
        self.usuario_rol_combo.addItems(['admin', 'gestor', 'colaborador'])
        
        form_layout.addWidget(QLabel("Nombre:"))
        form_layout.addWidget(self.usuario_nombre_edit)
        form_layout.addWidget(QLabel("Email:"))
        form_layout.addWidget(self.usuario_email_edit)
        form_layout.addWidget(QLabel("Rol:"))
        form_layout.addWidget(self.usuario_rol_combo)
        
        # Botones
        buttons_layout = QHBoxLayout()
        layout.addLayout(buttons_layout)
        
        add_button = QPushButton("Añadir")
        add_button.clicked.connect(self.add_usuario)
        buttons_layout.addWidget(add_button)
        
        update_button = QPushButton("Actualizar")
        update_button.clicked.connect(self.update_usuario)
        buttons_layout.addWidget(update_button)
        
        delete_button = QPushButton("Eliminar")
        delete_button.clicked.connect(self.delete_usuario)
        buttons_layout.addWidget(delete_button)
        
        # Tabla
        self.usuarios_table = QTableWidget()
        layout.addWidget(self.usuarios_table)
        self.load_usuarios()
        
    def load_ofertas(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, titulo, empresa, ubicacion, tipo_trabajo, salario_min, salario_max FROM analisis_mercado_ofertaempleo")
        ofertas = cursor.fetchall()
        
        self.ofertas_table.setColumnCount(7)
        self.ofertas_table.setHorizontalHeaderLabels(["ID", "Título", "Empresa", "Ubicación", "Tipo Trabajo", "Salario Min", "Salario Max"])
        
        self.ofertas_table.setRowCount(len(ofertas))
        for i, oferta in enumerate(ofertas):
            for j, value in enumerate(oferta):
                item = QTableWidgetItem(str(value))
                self.ofertas_table.setItem(i, j, item)
                
    def load_habilidades(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, nombre, categoria FROM analisis_mercado_habilidad")
        habilidades = cursor.fetchall()
        
        self.habilidades_table.setColumnCount(3)
        self.habilidades_table.setHorizontalHeaderLabels(["ID", "Nombre", "Categoría"])
        
        self.habilidades_table.setRowCount(len(habilidades))
        for i, habilidad in enumerate(habilidades):
            for j, value in enumerate(habilidad):
                item = QTableWidgetItem(str(value))
                self.habilidades_table.setItem(i, j, item)
                
    def load_usuarios(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, username, email, rol FROM usuarios_usuario")
        usuarios = cursor.fetchall()
        
        self.usuarios_table.setColumnCount(4)
        self.usuarios_table.setHorizontalHeaderLabels(["ID", "Nombre", "Email", "Rol"])
        
        self.usuarios_table.setRowCount(len(usuarios))
        for i, usuario in enumerate(usuarios):
            for j, value in enumerate(usuario):
                item = QTableWidgetItem(str(value))
                self.usuarios_table.setItem(i, j, item)
                
    def add_oferta(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO analisis_mercado_ofertaempleo 
                (titulo, empresa, ubicacion, tipo_trabajo, salario_min, salario_max, fecha_publicacion)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                self.titulo_edit.text(),
                self.empresa_edit.text(),
                self.ubicacion_edit.text(),
                self.tipo_trabajo_edit.text(),
                float(self.salario_min_edit.text()) if self.salario_min_edit.text() else None,
                float(self.salario_max_edit.text()) if self.salario_max_edit.text() else None,
                datetime.now()
            ))
            self.conn.commit()
            self.load_ofertas()
            QMessageBox.information(self, "Éxito", "Oferta añadida correctamente")
        except Exception as e:
            self.conn.rollback()
            QMessageBox.critical(self, "Error", f"Error al añadir oferta: {str(e)}")
            
    def add_habilidad(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO analisis_mercado_habilidad (nombre, categoria)
                VALUES (%s, %s)
            """, (self.habilidad_nombre_edit.text(), self.habilidad_categoria_edit.text()))
            self.conn.commit()
            self.load_habilidades()
            QMessageBox.information(self, "Éxito", "Habilidad añadida correctamente")
        except Exception as e:
            self.conn.rollback()
            QMessageBox.critical(self, "Error", f"Error al añadir habilidad: {str(e)}")
            
    def add_usuario(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO usuarios_usuario (username, email, rol)
                VALUES (%s, %s, %s)
            """, (self.usuario_nombre_edit.text(), self.usuario_email_edit.text(), self.usuario_rol_combo.currentText()))
            self.conn.commit()
            self.load_usuarios()
            QMessageBox.information(self, "Éxito", "Usuario añadido correctamente")
        except Exception as e:
            self.conn.rollback()
            QMessageBox.critical(self, "Error", f"Error al añadir usuario: {str(e)}")
            
    def update_oferta(self):
        selected = self.ofertas_table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Advertencia", "Por favor, seleccione una oferta para actualizar")
            return
            
        row = selected[0].row()
        id_oferta = self.ofertas_table.item(row, 0).text()
        
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                UPDATE analisis_mercado_ofertaempleo 
                SET titulo = %s, empresa = %s, ubicacion = %s, tipo_trabajo = %s,
                    salario_min = %s, salario_max = %s
                WHERE id = %s
            """, (
                self.titulo_edit.text(),
                self.empresa_edit.text(),
                self.ubicacion_edit.text(),
                self.tipo_trabajo_edit.text(),
                float(self.salario_min_edit.text()) if self.salario_min_edit.text() else None,
                float(self.salario_max_edit.text()) if self.salario_max_edit.text() else None,
                id_oferta
            ))
            self.conn.commit()
            self.load_ofertas()
            QMessageBox.information(self, "Éxito", "Oferta actualizada correctamente")
        except Exception as e:
            self.conn.rollback()
            QMessageBox.critical(self, "Error", f"Error al actualizar oferta: {str(e)}")
            
    def update_habilidad(self):
        selected = self.habilidades_table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Advertencia", "Por favor, seleccione una habilidad para actualizar")
            return
            
        row = selected[0].row()
        id_habilidad = self.habilidades_table.item(row, 0).text()
        
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                UPDATE analisis_mercado_habilidad 
                SET nombre = %s, categoria = %s
                WHERE id = %s
            """, (self.habilidad_nombre_edit.text(), self.habilidad_categoria_edit.text(), id_habilidad))
            self.conn.commit()
            self.load_habilidades()
            QMessageBox.information(self, "Éxito", "Habilidad actualizada correctamente")
        except Exception as e:
            self.conn.rollback()
            QMessageBox.critical(self, "Error", f"Error al actualizar habilidad: {str(e)}")
            
    def update_usuario(self):
        selected = self.usuarios_table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Advertencia", "Por favor, seleccione un usuario para actualizar")
            return
            
        row = selected[0].row()
        id_usuario = self.usuarios_table.item(row, 0).text()
        
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                UPDATE usuarios_usuario 
                SET username = %s, email = %s, rol = %s
                WHERE id = %s
            """, (self.usuario_nombre_edit.text(), self.usuario_email_edit.text(), self.usuario_rol_combo.currentText(), id_usuario))
            self.conn.commit()
            self.load_usuarios()
            QMessageBox.information(self, "Éxito", "Usuario actualizado correctamente")
        except Exception as e:
            self.conn.rollback()
            QMessageBox.critical(self, "Error", f"Error al actualizar usuario: {str(e)}")
            
    def delete_oferta(self):
        selected = self.ofertas_table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Advertencia", "Por favor, seleccione una oferta para eliminar")
            return
            
        row = selected[0].row()
        id_oferta = self.ofertas_table.item(row, 0).text()
        
        reply = QMessageBox.question(self, 'Confirmar eliminación',
                                   '¿Está seguro de que desea eliminar esta oferta?',
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            cursor = self.conn.cursor()
            try:
                cursor.execute("DELETE FROM analisis_mercado_ofertaempleo WHERE id = %s", (id_oferta,))
                self.conn.commit()
                self.load_ofertas()
                QMessageBox.information(self, "Éxito", "Oferta eliminada correctamente")
            except Exception as e:
                self.conn.rollback()
                QMessageBox.critical(self, "Error", f"Error al eliminar oferta: {str(e)}")
                
    def delete_habilidad(self):
        selected = self.habilidades_table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Advertencia", "Por favor, seleccione una habilidad para eliminar")
            return
            
        row = selected[0].row()
        id_habilidad = self.habilidades_table.item(row, 0).text()
        
        reply = QMessageBox.question(self, 'Confirmar eliminación',
                                   '¿Está seguro de que desea eliminar esta habilidad?',
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            cursor = self.conn.cursor()
            try:
                cursor.execute("DELETE FROM analisis_mercado_habilidad WHERE id = %s", (id_habilidad,))
                self.conn.commit()
                self.load_habilidades()
                QMessageBox.information(self, "Éxito", "Habilidad eliminada correctamente")
            except Exception as e:
                self.conn.rollback()
                QMessageBox.critical(self, "Error", f"Error al eliminar habilidad: {str(e)}")
                
    def delete_usuario(self):
        selected = self.usuarios_table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Advertencia", "Por favor, seleccione un usuario para eliminar")
            return
            
        row = selected[0].row()
        id_usuario = self.usuarios_table.item(row, 0).text()
        
        reply = QMessageBox.question(self, 'Confirmar eliminación',
                                   '¿Está seguro de que desea eliminar este usuario?',
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            cursor = self.conn.cursor()
            try:
                cursor.execute("DELETE FROM usuarios_usuario WHERE id = %s", (id_usuario,))
                self.conn.commit()
                self.load_usuarios()
                QMessageBox.information(self, "Éxito", "Usuario eliminado correctamente")
            except Exception as e:
                self.conn.rollback()
                QMessageBox.critical(self, "Error", f"Error al eliminar usuario: {str(e)}")
                
    def closeEvent(self, event):
        self.conn.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())