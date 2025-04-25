"""
Ventana principal de la aplicación
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QLabel,
    QComboBox, QMessageBox, QTabWidget, QFormLayout,
    QLineEdit, QTextEdit, QDateEdit, QSpinBox, QDoubleSpinBox
)
from PyQt6.QtCore import Qt, QDate
import sys
import os
from datetime import datetime

# Añadir el directorio padre al path para importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import DatabaseManager
from models import (
    Usuario, Proyecto, Tarea, Habilidad, OfertaEmpleo,
    AnalisisMercado, PrediccionMercado
)
import logging

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.init_ui()

    def init_ui(self):
        """
        Inicializa la interfaz de usuario
        """
        # Crear widget central y layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Crear pestañas
        tabs = QTabWidget()
        layout.addWidget(tabs)

        # Añadir pestañas para cada entidad
        tabs.addTab(self.create_usuarios_tab(), "Usuarios")
        tabs.addTab(self.create_proyectos_tab(), "Proyectos")
        tabs.addTab(self.create_tareas_tab(), "Tareas")
        tabs.addTab(self.create_ofertas_tab(), "Ofertas")
        tabs.addTab(self.create_analisis_tab(), "Análisis")

    def create_usuarios_tab(self):
        """
        Crea la pestaña de usuarios
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Formulario
        form = QFormLayout()
        self.usuario_nombre = QLineEdit()
        self.usuario_email = QLineEdit()
        self.usuario_rol = QComboBox()
        self.usuario_rol.addItems(['ADMIN', 'GESTOR', 'COLABORADOR'])
        
        form.addRow("Nombre:", self.usuario_nombre)
        form.addRow("Email:", self.usuario_email)
        form.addRow("Rol:", self.usuario_rol)
        
        # Botones
        buttons = QHBoxLayout()
        btn_crear = QPushButton("Crear")
        btn_actualizar = QPushButton("Actualizar")
        btn_eliminar = QPushButton("Eliminar")
        
        buttons.addWidget(btn_crear)
        buttons.addWidget(btn_actualizar)
        buttons.addWidget(btn_eliminar)
        
        # Tabla
        self.tabla_usuarios = QTableWidget()
        self.tabla_usuarios.setColumnCount(4)
        self.tabla_usuarios.setHorizontalHeaderLabels(["ID", "Nombre", "Email", "Rol"])
        
        # Conectar señales
        btn_crear.clicked.connect(self.crear_usuario)
        btn_actualizar.clicked.connect(self.actualizar_usuario)
        btn_eliminar.clicked.connect(self.eliminar_usuario)
        
        # Añadir widgets al layout
        layout.addLayout(form)
        layout.addLayout(buttons)
        layout.addWidget(self.tabla_usuarios)
        
        return widget

    def create_proyectos_tab(self):
        """
        Crea la pestaña de proyectos
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Formulario
        form = QFormLayout()
        self.proyecto_titulo = QLineEdit()
        self.proyecto_descripcion = QTextEdit()
        self.proyecto_fecha_inicio = QDateEdit()
        self.proyecto_fecha_fin = QDateEdit()
        self.proyecto_gestor = QComboBox()
        
        form.addRow("Título:", self.proyecto_titulo)
        form.addRow("Descripción:", self.proyecto_descripcion)
        form.addRow("Fecha Inicio:", self.proyecto_fecha_inicio)
        form.addRow("Fecha Fin:", self.proyecto_fecha_fin)
        form.addRow("Gestor:", self.proyecto_gestor)
        
        # Botones
        buttons = QHBoxLayout()
        btn_crear = QPushButton("Crear")
        btn_actualizar = QPushButton("Actualizar")
        btn_eliminar = QPushButton("Eliminar")
        
        buttons.addWidget(btn_crear)
        buttons.addWidget(btn_actualizar)
        buttons.addWidget(btn_eliminar)
        
        # Tabla
        self.tabla_proyectos = QTableWidget()
        self.tabla_proyectos.setColumnCount(5)
        self.tabla_proyectos.setHorizontalHeaderLabels(
            ["ID", "Título", "Gestor", "Fecha Inicio", "Fecha Fin"]
        )
        
        # Conectar señales
        btn_crear.clicked.connect(self.crear_proyecto)
        btn_actualizar.clicked.connect(self.actualizar_proyecto)
        btn_eliminar.clicked.connect(self.eliminar_proyecto)
        
        # Añadir widgets al layout
        layout.addLayout(form)
        layout.addLayout(buttons)
        layout.addWidget(self.tabla_proyectos)
        
        return widget

    def create_tareas_tab(self):
        """
        Crea la pestaña de tareas
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Formulario
        form = QFormLayout()
        self.tarea_titulo = QLineEdit()
        self.tarea_descripcion = QTextEdit()
        self.tarea_proyecto = QComboBox()
        self.tarea_asignado = QComboBox()
        self.tarea_prioridad = QComboBox()
        self.tarea_prioridad.addItems(['BAJA', 'MEDIA', 'ALTA', 'URGENTE'])
        
        form.addRow("Título:", self.tarea_titulo)
        form.addRow("Descripción:", self.tarea_descripcion)
        form.addRow("Proyecto:", self.tarea_proyecto)
        form.addRow("Asignado a:", self.tarea_asignado)
        form.addRow("Prioridad:", self.tarea_prioridad)
        
        # Botones
        buttons = QHBoxLayout()
        btn_crear = QPushButton("Crear")
        btn_actualizar = QPushButton("Actualizar")
        btn_eliminar = QPushButton("Eliminar")
        
        buttons.addWidget(btn_crear)
        buttons.addWidget(btn_actualizar)
        buttons.addWidget(btn_eliminar)
        
        # Tabla
        self.tabla_tareas = QTableWidget()
        self.tabla_tareas.setColumnCount(6)
        self.tabla_tareas.setHorizontalHeaderLabels(
            ["ID", "Título", "Proyecto", "Asignado", "Prioridad", "Estado"]
        )
        
        # Conectar señales
        btn_crear.clicked.connect(self.crear_tarea)
        btn_actualizar.clicked.connect(self.actualizar_tarea)
        btn_eliminar.clicked.connect(self.eliminar_tarea)
        
        # Añadir widgets al layout
        layout.addLayout(form)
        layout.addLayout(buttons)
        layout.addWidget(self.tabla_tareas)
        
        return widget

    def create_ofertas_tab(self):
        """
        Crea la pestaña de ofertas
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Formulario
        form = QFormLayout()
        self.oferta_titulo = QLineEdit()
        self.oferta_empresa = QLineEdit()
        self.oferta_descripcion = QTextEdit()
        self.oferta_ubicacion = QLineEdit()
        self.oferta_salario_min = QDoubleSpinBox()
        self.oferta_salario_max = QDoubleSpinBox()
        
        form.addRow("Título:", self.oferta_titulo)
        form.addRow("Empresa:", self.oferta_empresa)
        form.addRow("Descripción:", self.oferta_descripcion)
        form.addRow("Ubicación:", self.oferta_ubicacion)
        form.addRow("Salario Mín:", self.oferta_salario_min)
        form.addRow("Salario Máx:", self.oferta_salario_max)
        
        # Botones
        buttons = QHBoxLayout()
        btn_crear = QPushButton("Crear")
        btn_actualizar = QPushButton("Actualizar")
        btn_eliminar = QPushButton("Eliminar")
        
        buttons.addWidget(btn_crear)
        buttons.addWidget(btn_actualizar)
        buttons.addWidget(btn_eliminar)
        
        # Tabla
        self.tabla_ofertas = QTableWidget()
        self.tabla_ofertas.setColumnCount(7)
        self.tabla_ofertas.setHorizontalHeaderLabels(
            ["ID", "Título", "Empresa", "Ubicación", "Salario Min", "Salario Max", "Fecha"]
        )
        
        # Conectar señales
        btn_crear.clicked.connect(self.crear_oferta)
        btn_actualizar.clicked.connect(self.actualizar_oferta)
        btn_eliminar.clicked.connect(self.eliminar_oferta)
        
        # Añadir widgets al layout
        layout.addLayout(form)
        layout.addLayout(buttons)
        layout.addWidget(self.tabla_ofertas)
        
        return widget

    def create_analisis_tab(self):
        """
        Crea la pestaña de análisis
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Gráficos y estadísticas
        self.grafico_habilidades = QLabel("Gráfico de Habilidades más Demandadas")
        self.grafico_salarios = QLabel("Gráfico de Salarios por Habilidad")
        self.grafico_tendencias = QLabel("Gráfico de Tendencias")
        
        layout.addWidget(self.grafico_habilidades)
        layout.addWidget(self.grafico_salarios)
        layout.addWidget(self.grafico_tendencias)
        
        return widget

    # Métodos CRUD para Usuarios
    def crear_usuario(self):
        """
        Crea un nuevo usuario
        """
        try:
            usuario = Usuario(
                nombre=self.usuario_nombre.text(),
                email=self.usuario_email.text(),
                rol=self.usuario_rol.currentText()
            )
            self.db.session.add(usuario)
            self.db.session.commit()
            self.actualizar_tabla_usuarios()
            QMessageBox.information(self, "Éxito", "Usuario creado correctamente")
        except Exception as e:
            logger.error(f"Error al crear usuario: {str(e)}")
            QMessageBox.critical(self, "Error", f"Error al crear usuario: {str(e)}")

    def actualizar_usuario(self):
        """
        Actualiza un usuario existente
        """
        try:
            id_usuario = self.tabla_usuarios.currentItem().text()
            usuario = self.db.session.query(Usuario).get(id_usuario)
            if usuario:
                usuario.nombre = self.usuario_nombre.text()
                usuario.email = self.usuario_email.text()
                usuario.rol = self.usuario_rol.currentText()
                self.db.session.commit()
                self.actualizar_tabla_usuarios()
                QMessageBox.information(self, "Éxito", "Usuario actualizado correctamente")
        except Exception as e:
            logger.error(f"Error al actualizar usuario: {str(e)}")
            QMessageBox.critical(self, "Error", f"Error al actualizar usuario: {str(e)}")

    def eliminar_usuario(self):
        """
        Elimina un usuario
        """
        try:
            id_usuario = self.tabla_usuarios.currentItem().text()
            usuario = self.db.session.query(Usuario).get(id_usuario)
            if usuario:
                self.db.session.delete(usuario)
                self.db.session.commit()
                self.actualizar_tabla_usuarios()
                QMessageBox.information(self, "Éxito", "Usuario eliminado correctamente")
        except Exception as e:
            logger.error(f"Error al eliminar usuario: {str(e)}")
            QMessageBox.critical(self, "Error", f"Error al eliminar usuario: {str(e)}")

    def actualizar_tabla_usuarios(self):
        """
        Actualiza la tabla de usuarios
        """
        try:
            usuarios = self.db.session.query(Usuario).all()
            self.tabla_usuarios.setRowCount(len(usuarios))
            for i, usuario in enumerate(usuarios):
                self.tabla_usuarios.setItem(i, 0, QTableWidgetItem(str(usuario.id)))
                self.tabla_usuarios.setItem(i, 1, QTableWidgetItem(usuario.nombre))
                self.tabla_usuarios.setItem(i, 2, QTableWidgetItem(usuario.email))
                self.tabla_usuarios.setItem(i, 3, QTableWidgetItem(usuario.rol))
        except Exception as e:
            logger.error(f"Error al actualizar tabla de usuarios: {str(e)}")

    # Métodos CRUD para Proyectos
    def crear_proyecto(self):
        """
        Crea un nuevo proyecto
        """
        try:
            proyecto = Proyecto(
                titulo=self.proyecto_titulo.text(),
                descripcion=self.proyecto_descripcion.toPlainText(),
                fecha_inicio=self.proyecto_fecha_inicio.date().toPyDate(),
                fecha_fin_estimada=self.proyecto_fecha_fin.date().toPyDate(),
                estado='ACTIVO',
                gestor_id=self.proyecto_gestor.currentData()
            )
            self.db.session.add(proyecto)
            self.db.session.commit()
            self.actualizar_tabla_proyectos()
            QMessageBox.information(self, "Éxito", "Proyecto creado correctamente")
        except Exception as e:
            logger.error(f"Error al crear proyecto: {str(e)}")
            QMessageBox.critical(self, "Error", f"Error al crear proyecto: {str(e)}")

    def actualizar_proyecto(self):
        """
        Actualiza un proyecto existente
        """
        try:
            id_proyecto = self.tabla_proyectos.currentItem().text()
            proyecto = self.db.session.query(Proyecto).get(id_proyecto)
            if proyecto:
                proyecto.titulo = self.proyecto_titulo.text()
                proyecto.descripcion = self.proyecto_descripcion.toPlainText()
                proyecto.fecha_inicio = self.proyecto_fecha_inicio.date().toPyDate()
                proyecto.fecha_fin_estimada = self.proyecto_fecha_fin.date().toPyDate()
                proyecto.gestor_id = self.proyecto_gestor.currentData()
                self.db.session.commit()
                self.actualizar_tabla_proyectos()
                QMessageBox.information(self, "Éxito", "Proyecto actualizado correctamente")
        except Exception as e:
            logger.error(f"Error al actualizar proyecto: {str(e)}")
            QMessageBox.critical(self, "Error", f"Error al actualizar proyecto: {str(e)}")

    def eliminar_proyecto(self):
        """
        Elimina un proyecto
        """
        try:
            id_proyecto = self.tabla_proyectos.currentItem().text()
            proyecto = self.db.session.query(Proyecto).get(id_proyecto)
            if proyecto:
                self.db.session.delete(proyecto)
                self.db.session.commit()
                self.actualizar_tabla_proyectos()
                QMessageBox.information(self, "Éxito", "Proyecto eliminado correctamente")
        except Exception as e:
            logger.error(f"Error al eliminar proyecto: {str(e)}")
            QMessageBox.critical(self, "Error", f"Error al eliminar proyecto: {str(e)}")

    def actualizar_tabla_proyectos(self):
        """
        Actualiza la tabla de proyectos
        """
        try:
            proyectos = self.db.session.query(Proyecto).all()
            self.tabla_proyectos.setRowCount(len(proyectos))
            for i, proyecto in enumerate(proyectos):
                self.tabla_proyectos.setItem(i, 0, QTableWidgetItem(str(proyecto.id)))
                self.tabla_proyectos.setItem(i, 1, QTableWidgetItem(proyecto.titulo))
                self.tabla_proyectos.setItem(i, 2, QTableWidgetItem(str(proyecto.gestor_id)))
                self.tabla_proyectos.setItem(i, 3, QTableWidgetItem(str(proyecto.fecha_inicio)))
                self.tabla_proyectos.setItem(i, 4, QTableWidgetItem(str(proyecto.fecha_fin_estimada)))
        except Exception as e:
            logger.error(f"Error al actualizar tabla de proyectos: {str(e)}")

    # Métodos CRUD para Tareas
    def crear_tarea(self):
        """
        Crea una nueva tarea
        """
        try:
            tarea = Tarea(
                titulo=self.tarea_titulo.text(),
                descripcion=self.tarea_descripcion.toPlainText(),
                proyecto_id=self.tarea_proyecto.currentData(),
                asignado_a_id=self.tarea_asignado.currentData(),
                prioridad=self.tarea_prioridad.currentText(),
                estado='PENDIENTE'
            )
            self.db.session.add(tarea)
            self.db.session.commit()
            self.actualizar_tabla_tareas()
            QMessageBox.information(self, "Éxito", "Tarea creada correctamente")
        except Exception as e:
            logger.error(f"Error al crear tarea: {str(e)}")
            QMessageBox.critical(self, "Error", f"Error al crear tarea: {str(e)}")

    def actualizar_tarea(self):
        """
        Actualiza una tarea existente
        """
        try:
            id_tarea = self.tabla_tareas.currentItem().text()
            tarea = self.db.session.query(Tarea).get(id_tarea)
            if tarea:
                tarea.titulo = self.tarea_titulo.text()
                tarea.descripcion = self.tarea_descripcion.toPlainText()
                tarea.proyecto_id = self.tarea_proyecto.currentData()
                tarea.asignado_a_id = self.tarea_asignado.currentData()
                tarea.prioridad = self.tarea_prioridad.currentText()
                self.db.session.commit()
                self.actualizar_tabla_tareas()
                QMessageBox.information(self, "Éxito", "Tarea actualizada correctamente")
        except Exception as e:
            logger.error(f"Error al actualizar tarea: {str(e)}")
            QMessageBox.critical(self, "Error", f"Error al actualizar tarea: {str(e)}")

    def eliminar_tarea(self):
        """
        Elimina una tarea
        """
        try:
            id_tarea = self.tabla_tareas.currentItem().text()
            tarea = self.db.session.query(Tarea).get(id_tarea)
            if tarea:
                self.db.session.delete(tarea)
                self.db.session.commit()
                self.actualizar_tabla_tareas()
                QMessageBox.information(self, "Éxito", "Tarea eliminada correctamente")
        except Exception as e:
            logger.error(f"Error al eliminar tarea: {str(e)}")
            QMessageBox.critical(self, "Error", f"Error al eliminar tarea: {str(e)}")

    def actualizar_tabla_tareas(self):
        """
        Actualiza la tabla de tareas
        """
        try:
            tareas = self.db.session.query(Tarea).all()
            self.tabla_tareas.setRowCount(len(tareas))
            for i, tarea in enumerate(tareas):
                self.tabla_tareas.setItem(i, 0, QTableWidgetItem(str(tarea.id)))
                self.tabla_tareas.setItem(i, 1, QTableWidgetItem(tarea.titulo))
                self.tabla_tareas.setItem(i, 2, QTableWidgetItem(str(tarea.proyecto_id)))
                self.tabla_tareas.setItem(i, 3, QTableWidgetItem(str(tarea.asignado_a_id)))
                self.tabla_tareas.setItem(i, 4, QTableWidgetItem(tarea.prioridad))
                self.tabla_tareas.setItem(i, 5, QTableWidgetItem(tarea.estado))
        except Exception as e:
            logger.error(f"Error al actualizar tabla de tareas: {str(e)}")

    # Métodos CRUD para Ofertas
    def crear_oferta(self):
        """
        Crea una nueva oferta
        """
        try:
            oferta = OfertaEmpleo(
                titulo=self.oferta_titulo.text(),
                empresa=self.oferta_empresa.text(),
                descripcion=self.oferta_descripcion.toPlainText(),
                ubicacion=self.oferta_ubicacion.text(),
                salario_min=self.oferta_salario_min.value(),
                salario_max=self.oferta_salario_max.value(),
                tipo_contrato='INDEFINIDO',
                fecha_publicacion=datetime.now()
            )
            self.db.session.add(oferta)
            self.db.session.commit()
            self.actualizar_tabla_ofertas()
            QMessageBox.information(self, "Éxito", "Oferta creada correctamente")
        except Exception as e:
            logger.error(f"Error al crear oferta: {str(e)}")
            QMessageBox.critical(self, "Error", f"Error al crear oferta: {str(e)}")

    def actualizar_oferta(self):
        """
        Actualiza una oferta existente
        """
        try:
            id_oferta = self.tabla_ofertas.currentItem().text()
            oferta = self.db.session.query(OfertaEmpleo).get(id_oferta)
            if oferta:
                oferta.titulo = self.oferta_titulo.text()
                oferta.empresa = self.oferta_empresa.text()
                oferta.descripcion = self.oferta_descripcion.toPlainText()
                oferta.ubicacion = self.oferta_ubicacion.text()
                oferta.salario_min = self.oferta_salario_min.value()
                oferta.salario_max = self.oferta_salario_max.value()
                self.db.session.commit()
                self.actualizar_tabla_ofertas()
                QMessageBox.information(self, "Éxito", "Oferta actualizada correctamente")
        except Exception as e:
            logger.error(f"Error al actualizar oferta: {str(e)}")
            QMessageBox.critical(self, "Error", f"Error al actualizar oferta: {str(e)}")

    def eliminar_oferta(self):
        """
        Elimina una oferta
        """
        try:
            id_oferta = self.tabla_ofertas.currentItem().text()
            oferta = self.db.session.query(OfertaEmpleo).get(id_oferta)
            if oferta:
                self.db.session.delete(oferta)
                self.db.session.commit()
                self.actualizar_tabla_ofertas()
                QMessageBox.information(self, "Éxito", "Oferta eliminada correctamente")
        except Exception as e:
            logger.error(f"Error al eliminar oferta: {str(e)}")
            QMessageBox.critical(self, "Error", f"Error al eliminar oferta: {str(e)}")

    def actualizar_tabla_ofertas(self):
        """
        Actualiza la tabla de ofertas
        """
        try:
            ofertas = self.db.session.query(OfertaEmpleo).all()
            self.tabla_ofertas.setRowCount(len(ofertas))
            for i, oferta in enumerate(ofertas):
                self.tabla_ofertas.setItem(i, 0, QTableWidgetItem(str(oferta.id)))
                self.tabla_ofertas.setItem(i, 1, QTableWidgetItem(oferta.titulo))
                self.tabla_ofertas.setItem(i, 2, QTableWidgetItem(oferta.empresa))
                self.tabla_ofertas.setItem(i, 3, QTableWidgetItem(oferta.ubicacion))
                self.tabla_ofertas.setItem(i, 4, QTableWidgetItem(str(oferta.salario_min)))
                self.tabla_ofertas.setItem(i, 5, QTableWidgetItem(str(oferta.salario_max)))
                self.tabla_ofertas.setItem(i, 6, QTableWidgetItem(str(oferta.fecha_publicacion)))
        except Exception as e:
            logger.error(f"Error al actualizar tabla de ofertas: {str(e)}") 