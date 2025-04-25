from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QLineEdit, QMessageBox, QDialog, QFormLayout,
    QTextEdit, QComboBox, QSpinBox, QDateEdit, QGroupBox, QCheckBox,
    QScrollArea, QFrame, QSplitter, QTabWidget, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt, QDate, QSize
from PyQt6.QtGui import QFont, QColor, QIcon
from typing import Dict, Any, List, Optional
from ui.database import DatabaseManager
from scrapers.scraper import scrape_infojobs, scrape_linkedin, guardar_ofertas

class JobOfferDialog(QDialog):
    def __init__(self, parent=None, job_data: Dict[str, Any] = None):
        super().__init__(parent)
        self.job_data = job_data
        self.setup_ui()
        
        # Ajustar tamaño de la ventana
        self.setMinimumWidth(500)
        self.setMinimumHeight(600)
        
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
        self.setWindowTitle("Nueva Oferta de Empleo" if not self.job_data else "Editar Oferta de Empleo")
        
        layout = QFormLayout()
        
        # Title
        self.title = QLineEdit()
        if self.job_data:
            self.title.setText(self.job_data.get('title', ''))
        layout.addRow("Título:", self.title)
        
        # Company
        self.company = QLineEdit()
        if self.job_data:
            self.company.setText(self.job_data.get('company', ''))
        layout.addRow("Empresa:", self.company)
        
        # Location
        self.location = QLineEdit()
        if self.job_data:
            self.location.setText(self.job_data.get('location', ''))
        layout.addRow("Ubicación:", self.location)
        
        # Salary Range
        salary_layout = QHBoxLayout()
        self.min_salary = QLineEdit()
        self.max_salary = QLineEdit()
        if self.job_data:
            self.min_salary.setText(str(self.job_data.get('min_salary', '')))
            self.max_salary.setText(str(self.job_data.get('max_salary', '')))
        salary_layout.addWidget(QLabel("Min:"))
        salary_layout.addWidget(self.min_salary)
        salary_layout.addWidget(QLabel("Max:"))
        salary_layout.addWidget(self.max_salary)
        layout.addRow("Rango Salarial:", salary_layout)
        
        # Job Type
        self.job_type = QComboBox()
        self.job_type.addItems(["Tiempo completo", "Tiempo parcial", "Contrato", "Freelance", "Remoto", "Híbrido", "Presencial"])
        if self.job_data:
            self.job_type.setCurrentText(self.job_data.get('job_type', ''))
        layout.addRow("Tipo de Trabajo:", self.job_type)
        
        # Fuente
        self.fuente = QComboBox()
        self.fuente.addItems(["InfoJobs", "Tecnoempleo", "LinkedIn", "Manual"])
        if self.job_data:
            self.fuente.setCurrentText(self.job_data.get('fuente', 'Manual'))
        layout.addRow("Fuente:", self.fuente)
        
        # Description
        self.description = QTextEdit()
        self.description.setMinimumHeight(100)
        if self.job_data:
            self.description.setText(self.job_data.get('description', ''))
        layout.addRow("Descripción:", self.description)
        
        # Requirements
        self.requirements = QTextEdit()
        self.requirements.setMinimumHeight(100)
        if self.job_data:
            self.requirements.setText(self.job_data.get('requirements', ''))
        layout.addRow("Requisitos:", self.requirements)
        
        # Habilidades
        habilidades_layout = QVBoxLayout()
        self.habilidades_list = QListWidget()
        self.habilidades_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        
        # Cargar habilidades disponibles
        try:
            habilidades = self.parent().db_manager.get_table_data('habilidades')
            for habilidad in habilidades:
                item = QListWidgetItem(habilidad['nombre'])
                self.habilidades_list.addItem(item)
                
                # Si estamos editando, seleccionar las habilidades existentes
                if self.job_data and 'habilidades' in self.job_data:
                    if habilidad['nombre'] in self.job_data['habilidades']:
                        item.setSelected(True)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al cargar habilidades: {str(e)}")
        
        habilidades_layout.addWidget(self.habilidades_list)
        layout.addRow("Habilidades:", habilidades_layout)
        
        # Publication Date
        self.pub_date = QDateEdit()
        self.pub_date.setCalendarPopup(True)
        self.pub_date.setDate(QDate.currentDate())
        if self.job_data:
            self.pub_date.setDate(QDate.fromString(self.job_data.get('publication_date', ''), Qt.DateFormat.ISODate))
        layout.addRow("Fecha de Publicación:", self.pub_date)
        
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
    
    def get_job_data(self) -> Dict[str, Any]:
        """Retorna los datos del formulario como un diccionario"""
        # Obtener habilidades seleccionadas
        habilidades_seleccionadas = []
        for i in range(self.habilidades_list.count()):
            item = self.habilidades_list.item(i)
            if item.isSelected():
                habilidades_seleccionadas.append(item.text())
        
        return {
            'title': self.title.text(),
            'company': self.company.text(),
            'location': self.location.text(),
            'min_salary': int(self.min_salary.text() or 0),
            'max_salary': int(self.max_salary.text() or 0),
            'job_type': self.job_type.currentText(),
            'fuente': self.fuente.currentText(),
            'description': self.description.toPlainText(),
            'requirements': self.requirements.toPlainText(),
            'publication_date': self.pub_date.date().toString(Qt.DateFormat.ISODate),
            'habilidades': habilidades_seleccionadas
        }

class ImportarOfertasDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
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
        self.setWindowTitle("Importar Ofertas de Empleo")
        
        layout = QVBoxLayout()
        
        # Fuente
        fuente_layout = QHBoxLayout()
        fuente_layout.addWidget(QLabel("Fuente:"))
        self.fuente = QComboBox()
        self.fuente.addItems(["Tecnoempleo", "InfoJobs", "LinkedIn"])
        fuente_layout.addWidget(self.fuente)
        layout.addLayout(fuente_layout)
        
        # Título
        titulo_layout = QHBoxLayout()
        titulo_layout.addWidget(QLabel("Título:"))
        self.titulo = QLineEdit()
        titulo_layout.addWidget(self.titulo)
        layout.addLayout(titulo_layout)
        
        # Ubicación
        ubicacion_layout = QHBoxLayout()
        ubicacion_layout.addWidget(QLabel("Ubicación:"))
        self.ubicacion = QLineEdit()
        ubicacion_layout.addWidget(self.ubicacion)
        layout.addLayout(ubicacion_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        importar_button = QPushButton("Importar")
        importar_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(importar_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def get_import_data(self) -> Dict[str, str]:
        """Retorna los datos del formulario como un diccionario"""
        return {
            'fuente': self.fuente.currentText(),
            'titulo': self.titulo.text(),
            'ubicacion': self.ubicacion.text()
        }

class OfertasTab(QWidget):
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.db_manager = db_manager
        self.setup_ui()
        self.load_job_offers()
    
    def setup_ui(self):
        main_layout = QVBoxLayout()
        
        # Crear un QTabWidget para organizar las pestañas
        tab_widget = QTabWidget()
        
        # Pestaña de Lista de Ofertas
        lista_tab = QWidget()
        lista_layout = QVBoxLayout()
        
        # Search and Filter Section
        filter_group = QGroupBox("Filtros de Búsqueda")
        filter_layout = QVBoxLayout()
        
        # Primera fila de filtros
        filter_row1 = QHBoxLayout()
        
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Buscar ofertas...")
        self.search_edit.textChanged.connect(self.filter_job_offers)
        filter_row1.addWidget(QLabel("Título/Empresa:"))
        filter_row1.addWidget(self.search_edit)
        
        self.location_filter = QLineEdit()
        self.location_filter.setPlaceholderText("Ubicación...")
        self.location_filter.textChanged.connect(self.filter_job_offers)
        filter_row1.addWidget(QLabel("Ubicación:"))
        filter_row1.addWidget(self.location_filter)
        
        filter_layout.addLayout(filter_row1)
        
        # Segunda fila de filtros
        filter_row2 = QHBoxLayout()
        
        self.job_type_filter = QComboBox()
        self.job_type_filter.addItems(["Todos", "Tiempo completo", "Tiempo parcial", "Contrato", "Freelance", "Remoto", "Híbrido", "Presencial"])
        self.job_type_filter.currentTextChanged.connect(self.filter_job_offers)
        filter_row2.addWidget(QLabel("Tipo de Trabajo:"))
        filter_row2.addWidget(self.job_type_filter)
        
        self.fuente_filter = QComboBox()
        self.fuente_filter.addItems(["Todas", "InfoJobs", "Tecnoempleo", "LinkedIn", "Manual"])
        self.fuente_filter.currentTextChanged.connect(self.filter_job_offers)
        filter_row2.addWidget(QLabel("Fuente:"))
        filter_row2.addWidget(self.fuente_filter)
        
        filter_layout.addLayout(filter_row2)
        
        # Tercera fila de filtros - Habilidades
        filter_row3 = QHBoxLayout()
        
        self.habilidades_filter = QListWidget()
        self.habilidades_filter.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.habilidades_filter.setMaximumHeight(100)
        self.habilidades_filter.itemSelectionChanged.connect(self.filter_job_offers)
        
        # Cargar habilidades disponibles
        try:
            habilidades = self.db_manager.get_table_data('habilidades')
            for habilidad in habilidades:
                item = QListWidgetItem(habilidad['nombre'])
                self.habilidades_filter.addItem(item)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al cargar habilidades: {str(e)}")
        
        filter_row3.addWidget(QLabel("Habilidades:"))
        filter_row3.addWidget(self.habilidades_filter)
        
        filter_layout.addLayout(filter_row3)
        
        # Botones de filtro
        filter_buttons = QHBoxLayout()
        clear_filter_button = QPushButton("Limpiar Filtros")
        clear_filter_button.clicked.connect(self.clear_filters)
        filter_buttons.addWidget(clear_filter_button)
        filter_layout.addLayout(filter_buttons)
        
        filter_group.setLayout(filter_layout)
        lista_layout.addWidget(filter_group)
        
        # Job Offers Table
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Título", "Empresa", "Ubicación", "Rango Salarial",
            "Tipo", "Fuente", "Fecha", "Acciones"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        lista_layout.addWidget(self.table)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        add_button = QPushButton("Nueva Oferta")
        add_button.clicked.connect(self.add_job_offer)
        button_layout.addWidget(add_button)
        
        importar_button = QPushButton("Importar Ofertas")
        importar_button.clicked.connect(self.importar_ofertas)
        button_layout.addWidget(importar_button)
        
        refresh_button = QPushButton("Actualizar")
        refresh_button.clicked.connect(self.load_job_offers)
        button_layout.addWidget(refresh_button)
        
        lista_layout.addLayout(button_layout)
        lista_tab.setLayout(lista_layout)
        
        # Pestaña de Estadísticas
        stats_tab = QWidget()
        stats_layout = QVBoxLayout()
        
        # Estadísticas generales
        stats_group = QGroupBox("Estadísticas Generales")
        stats_group_layout = QVBoxLayout()
        
        try:
            # Total de ofertas
            total_ofertas = len(self.db_manager.get_table_data('job_offers'))
            total_label = QLabel(f"Total de Ofertas: {total_ofertas}")
            total_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            stats_group_layout.addWidget(total_label)
            
            # Ofertas por tipo de trabajo
            ofertas_por_tipo = {}
            ofertas = self.db_manager.get_table_data('job_offers')
            for oferta in ofertas:
                tipo = oferta.get('job_type', 'No especificado')
                ofertas_por_tipo[tipo] = ofertas_por_tipo.get(tipo, 0) + 1
            
            tipo_label = QLabel("Ofertas por Tipo de Trabajo:")
            tipo_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            stats_group_layout.addWidget(tipo_label)
            
            for tipo, count in ofertas_por_tipo.items():
                tipo_item = QLabel(f"{tipo}: {count}")
                stats_group_layout.addWidget(tipo_item)
            
            # Ofertas por fuente
            ofertas_por_fuente = {}
            for oferta in ofertas:
                fuente = oferta.get('fuente', 'No especificada')
                ofertas_por_fuente[fuente] = ofertas_por_fuente.get(fuente, 0) + 1
            
            fuente_label = QLabel("Ofertas por Fuente:")
            fuente_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            stats_group_layout.addWidget(fuente_label)
            
            for fuente, count in ofertas_por_fuente.items():
                fuente_item = QLabel(f"{fuente}: {count}")
                stats_group_layout.addWidget(fuente_item)
            
        except Exception as e:
            error_label = QLabel(f"Error al cargar estadísticas: {str(e)}")
            error_label.setStyleSheet("color: red;")
            stats_group_layout.addWidget(error_label)
        
        stats_group.setLayout(stats_group_layout)
        stats_layout.addWidget(stats_group)
        
        # Habilidades más demandadas
        habilidades_group = QGroupBox("Habilidades más Demandadas")
        habilidades_layout = QVBoxLayout()
        
        try:
            # Obtener habilidades y contar su frecuencia
            habilidades_count = {}
            ofertas = self.db_manager.get_table_data('job_offers')
            for oferta in ofertas:
                if 'habilidades' in oferta:
                    for habilidad in oferta['habilidades']:
                        habilidades_count[habilidad] = habilidades_count.get(habilidad, 0) + 1
            
            # Ordenar por frecuencia
            habilidades_ordenadas = sorted(habilidades_count.items(), key=lambda x: x[1], reverse=True)
            
            for habilidad, count in habilidades_ordenadas[:10]:  # Top 10 habilidades
                habilidad_item = QLabel(f"{habilidad}: {count} ofertas")
                habilidades_layout.addWidget(habilidad_item)
            
        except Exception as e:
            error_label = QLabel(f"Error al cargar habilidades: {str(e)}")
            error_label.setStyleSheet("color: red;")
            habilidades_layout.addWidget(error_label)
        
        habilidades_group.setLayout(habilidades_layout)
        stats_layout.addWidget(habilidades_group)
        
        stats_tab.setLayout(stats_layout)
        
        # Agregar pestañas al widget
        tab_widget.addTab(lista_tab, "Lista de Ofertas")
        tab_widget.addTab(stats_tab, "Estadísticas")
        
        main_layout.addWidget(tab_widget)
        self.setLayout(main_layout)
    
    def clear_filters(self):
        """Limpia todos los filtros aplicados"""
        self.search_edit.clear()
        self.location_filter.clear()
        self.job_type_filter.setCurrentText("Todos")
        self.fuente_filter.setCurrentText("Todas")
        self.habilidades_filter.clearSelection()
        self.filter_job_offers()
    
    def load_job_offers(self):
        try:
            job_offers = self.db_manager.get_table_data(
                'job_offers',
                order_by='publication_date DESC'
            )
            
            self.table.setRowCount(len(job_offers))
            for i, job in enumerate(job_offers):
                self.table.setItem(i, 0, QTableWidgetItem(job['title']))
                self.table.setItem(i, 1, QTableWidgetItem(job['company']))
                self.table.setItem(i, 2, QTableWidgetItem(job['location']))
                self.table.setItem(i, 3, QTableWidgetItem(
                    f"${job['min_salary']:,} - ${job['max_salary']:,}"
                ))
                self.table.setItem(i, 4, QTableWidgetItem(job['job_type']))
                self.table.setItem(i, 5, QTableWidgetItem(job.get('fuente', 'Manual')))
                self.table.setItem(i, 6, QTableWidgetItem(job['publication_date']))
                
                # Action buttons
                action_widget = QWidget()
                action_layout = QHBoxLayout()
                action_layout.setContentsMargins(0, 0, 0, 0)
                
                edit_button = QPushButton("Editar")
                edit_button.clicked.connect(lambda checked, j=job: self.edit_job_offer(j))
                action_layout.addWidget(edit_button)
                
                delete_button = QPushButton("Eliminar")
                delete_button.clicked.connect(lambda checked, j=job: self.delete_job_offer(j))
                action_layout.addWidget(delete_button)
                
                action_widget.setLayout(action_layout)
                self.table.setCellWidget(i, 7, action_widget)
            
            self.table.resizeColumnsToContents()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar ofertas: {str(e)}")
    
    def filter_job_offers(self):
        search_text = self.search_edit.text().lower()
        location_text = self.location_filter.text().lower()
        job_type = self.job_type_filter.currentText()
        fuente = self.fuente_filter.currentText()
        
        # Obtener habilidades seleccionadas
        habilidades_seleccionadas = []
        for i in range(self.habilidades_filter.count()):
            item = self.habilidades_filter.item(i)
            if item.isSelected():
                habilidades_seleccionadas.append(item.text())
        
        for i in range(self.table.rowCount()):
            title = self.table.item(i, 0).text().lower()
            company = self.table.item(i, 1).text().lower()
            location = self.table.item(i, 2).text().lower()
            tipo = self.table.item(i, 4).text()
            fuente_item = self.table.item(i, 5).text()
            
            # Aplicar filtros
            show_row = (
                (search_text in title or search_text in company) and
                (not location_text or location_text in location) and
                (job_type == "Todos" or job_type == tipo) and
                (fuente == "Todas" or fuente == fuente_item)
            )
            
            # Filtrar por habilidades si hay alguna seleccionada
            if show_row and habilidades_seleccionadas:
                try:
                    # Obtener las habilidades de la oferta
                    job_id = self.table.item(i, 0).data(Qt.ItemDataRole.UserRole)
                    job_habilidades = self.db_manager.get_job_habilidades(job_id)
                    
                    # Verificar si todas las habilidades seleccionadas están en la oferta
                    show_row = all(h in job_habilidades for h in habilidades_seleccionadas)
                except Exception as e:
                    print(f"Error al obtener habilidades de la oferta: {str(e)}")
                    show_row = False
            
            self.table.setRowHidden(i, not show_row)
    
    def add_job_offer(self):
        dialog = JobOfferDialog(self)
        if dialog.exec():
            try:
                job_data = dialog.get_job_data()
                
                # Guardar habilidades seleccionadas
                habilidades = job_data.pop('habilidades')
                
                # Insertar la oferta
                job_id = self.db_manager.insert_data('job_offers', job_data)
                
                # Guardar las habilidades asociadas
                for habilidad_nombre in habilidades:
                    # Buscar o crear la habilidad
                    habilidad_data = {'nombre': habilidad_nombre}
                    habilidad_id = self.db_manager.insert_data('habilidades', habilidad_data)
                    
                    # Asociar la habilidad con la oferta
                    self.db_manager.execute_query(
                        "INSERT INTO job_offers_habilidades (job_offers_id, habilidades_id) VALUES (%s, %s)",
                        (job_id, habilidad_id)
                    )
                
                self.load_job_offers()
                QMessageBox.information(self, "Éxito", "Oferta de empleo creada exitosamente")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al crear oferta: {str(e)}")
    
    def edit_job_offer(self, job_data: Dict[str, Any]):
        dialog = JobOfferDialog(self, job_data)
        if dialog.exec():
            try:
                updated_data = dialog.get_job_data()
                
                # Guardar habilidades seleccionadas
                habilidades = updated_data.pop('habilidades')
                
                # Actualizar la oferta
                self.db_manager.update_data(
                    'job_offers',
                    updated_data,
                    'id = %s',
                    (job_data['id'],)
                )
                
                # Eliminar asociaciones anteriores
                self.db_manager.execute_query(
                    "DELETE FROM job_offers_habilidades WHERE job_offers_id = %s",
                    (job_data['id'],)
                )
                
                # Guardar las nuevas habilidades asociadas
                for habilidad_nombre in habilidades:
                    # Buscar o crear la habilidad
                    habilidad_data = {'nombre': habilidad_nombre}
                    habilidad_id = self.db_manager.insert_data('habilidades', habilidad_data)
                    
                    # Asociar la habilidad con la oferta
                    self.db_manager.execute_query(
                        "INSERT INTO job_offers_habilidades (job_offers_id, habilidades_id) VALUES (%s, %s)",
                        (job_data['id'], habilidad_id)
                    )
                
                self.load_job_offers()
                QMessageBox.information(self, "Éxito", "Oferta de empleo actualizada exitosamente")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al actualizar oferta: {str(e)}")
    
    def delete_job_offer(self, job_data: Dict[str, Any]):
        reply = QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Está seguro de eliminar la oferta '{job_data['title']}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                # Eliminar asociaciones con habilidades
                self.db_manager.execute_query(
                    "DELETE FROM job_offers_habilidades WHERE job_offers_id = %s",
                    (job_data['id'],)
                )
                
                # Eliminar la oferta
                self.db_manager.delete_data(
                    'job_offers',
                    'id = %s',
                    (job_data['id'],)
                )
                
                self.load_job_offers()
                QMessageBox.information(self, "Éxito", "Oferta de empleo eliminada exitosamente")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al eliminar oferta: {str(e)}")
    
    def importar_ofertas(self):
        """
        Importa ofertas de trabajo desde diferentes fuentes
        """
        try:
            # Scrapear ofertas de diferentes fuentes
            todas_las_ofertas = []
            
            # InfoJobs
            ofertas_infojobs = scrape_infojobs()
            if ofertas_infojobs:
                todas_las_ofertas.extend(ofertas_infojobs)
                QMessageBox.information(self, "Éxito", f"Se importaron {len(ofertas_infojobs)} ofertas de InfoJobs")
            
            # LinkedIn
            ofertas_linkedin = scrape_linkedin()
            if ofertas_linkedin:
                todas_las_ofertas.extend(ofertas_linkedin)
                QMessageBox.information(self, "Éxito", f"Se importaron {len(ofertas_linkedin)} ofertas de LinkedIn")
            
            # Guardar todas las ofertas
            if todas_las_ofertas:
                guardar_ofertas(todas_las_ofertas, self.db_manager.conn)
                QMessageBox.information(self, "Éxito", f"Se importaron {len(todas_las_ofertas)} ofertas en total")
                self.load_job_offers()  # Recargar la tabla
            else:
                QMessageBox.warning(self, "Advertencia", "No se encontraron ofertas para importar")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al importar ofertas: {str(e)}") 