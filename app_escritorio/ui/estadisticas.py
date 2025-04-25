from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from typing import Dict, List, Any
import pyqtgraph as pg
from ui.database import DatabaseManager

class StatCard(QFrame):
    def __init__(self, title: str, value: str, icon: str = None):
        super().__init__()
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        layout.setContentsMargins(10, 10, 10, 10)
        
        if icon:
            icon_label = QLabel(icon)
            icon_label.setFont(QFont("Font Awesome 5 Free", 16))
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(icon_label)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 10))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        self.value_label = QLabel(str(value))
        self.value_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.value_label)
    
    def set_value(self, value: str):
        """Update the value displayed in the card"""
        self.value_label.setText(str(value))

class ChartCard(QFrame):
    def __init__(self, title: str):
        super().__init__()
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        layout.setContentsMargins(10, 10, 10, 10)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(title_label)
        
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        self.plot_widget.setMinimumHeight(150)
        layout.addWidget(self.plot_widget)

class EstadisticasView(QWidget):
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.db_manager = db_manager
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        # Crear scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #f5f6fa;
            }
        """)
        
        # Widget contenedor
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Título
        title = QLabel("Panel de Estadísticas")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Tarjetas de estadísticas
        stats_layout = QGridLayout()
        stats_layout.setSpacing(10)
        
        self.stat_cards = {
            'total_ofertas': StatCard("Total Ofertas", "0", "📊"),
            'empresas_unicas': StatCard("Empresas", "0", "🏢"),
            'habilidades_unicas': StatCard("Habilidades", "0", "⭐"),
            'ofertas_activas': StatCard("Ofertas Activas", "0", "📈")
        }
        
        for i, (key, card) in enumerate(self.stat_cards.items()):
            stats_layout.addWidget(card, 0, i)
        
        layout.addLayout(stats_layout)
        
        # Gráficos
        charts_layout = QGridLayout()
        charts_layout.setSpacing(10)
        
        self.chart_cards = {
            'fuentes': ChartCard("Distribución por Fuente"),
            'habilidades': ChartCard("Top 10 Habilidades"),
            'tipo_trabajo': ChartCard("Tipos de Trabajo"),
            'tendencias': ChartCard("Tendencias")
        }
        
        for i, (key, card) in enumerate(self.chart_cards.items()):
            charts_layout.addWidget(card, i // 2, i % 2)
        
        layout.addLayout(charts_layout)
        
        # Agregar el contenedor al scroll area
        scroll.setWidget(container)
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
    
    def load_data(self):
        try:
            # Cargar estadísticas
            stats = self.db_manager.execute_query("""
                SELECT 
                    COUNT(*) as total_ofertas,
                    COUNT(DISTINCT company) as empresas_unicas,
                    COUNT(DISTINCT h.nombre) as habilidades_unicas,
                    COUNT(*) FILTER (WHERE publication_date >= CURRENT_DATE - INTERVAL '30 days') as ofertas_activas
                FROM job_offers j
                LEFT JOIN job_offers_habilidades jh ON j.id = jh.job_offers_id
                LEFT JOIN habilidades h ON jh.habilidades_id = h.id
            """)[0]
            
            # Actualizar tarjetas
            self.stat_cards['total_ofertas'].set_value(stats['total_ofertas'])
            self.stat_cards['empresas_unicas'].set_value(stats['empresas_unicas'])
            self.stat_cards['habilidades_unicas'].set_value(stats['habilidades_unicas'])
            self.stat_cards['ofertas_activas'].set_value(stats['ofertas_activas'])
            
            # Cargar datos de gráficos
            self.load_fuentes_chart()
            self.load_habilidades_chart()
            self.load_tipo_trabajo_chart()
            self.load_tendencias_chart()
            
        except Exception as e:
            print(f"Error cargando estadísticas: {str(e)}")
    
    def load_fuentes_chart(self):
        data = self.db_manager.execute_query("""
            SELECT fuente, COUNT(*) as count
            FROM job_offers
            GROUP BY fuente
            ORDER BY count DESC
        """)
        
        if not data:
            return
        
        chart = self.chart_cards['fuentes'].plot_widget
        chart.clear()
        
        x = range(len(data))
        y = [d['count'] for d in data]
        labels = [d['fuente'] for d in data]
        
        bar = pg.BarGraphItem(x=x, height=y, width=0.6)
        chart.addItem(bar)
        
        ax = chart.getAxis('bottom')
        ax.setTicks([[(i, label) for i, label in enumerate(labels)]])
    
    def load_habilidades_chart(self):
        data = self.db_manager.execute_query("""
            SELECT h.nombre, COUNT(*) as count
            FROM habilidades h
            JOIN job_offers_habilidades jh ON h.id = jh.habilidades_id
            GROUP BY h.nombre
            ORDER BY count DESC
            LIMIT 10
        """)
        
        if not data:
            return
        
        chart = self.chart_cards['habilidades'].plot_widget
        chart.clear()
        
        x = range(len(data))
        y = [d['count'] for d in data]
        labels = [d['nombre'] for d in data]
        
        bar = pg.BarGraphItem(x=x, height=y, width=0.6)
        chart.addItem(bar)
        
        ax = chart.getAxis('bottom')
        ax.setTicks([[(i, label) for i, label in enumerate(labels)]])
    
    def load_tipo_trabajo_chart(self):
        data = self.db_manager.execute_query("""
            SELECT job_type, COUNT(*) as count
            FROM job_offers
            GROUP BY job_type
            ORDER BY count DESC
        """)
        
        if not data:
            return
        
        chart = self.chart_cards['tipo_trabajo'].plot_widget
        chart.clear()
        
        x = range(len(data))
        y = [d['count'] for d in data]
        labels = [d['job_type'] for d in data]
        
        bar = pg.BarGraphItem(x=x, height=y, width=0.6)
        chart.addItem(bar)
        
        ax = chart.getAxis('bottom')
        ax.setTicks([[(i, label) for i, label in enumerate(labels)]])
    
    def load_tendencias_chart(self):
        data = self.db_manager.execute_query("""
            SELECT 
                DATE_TRUNC('month', publication_date) as month,
                COUNT(*) as count
            FROM job_offers
            GROUP BY month
            ORDER BY month
        """)
        
        if not data:
            return
        
        chart = self.chart_cards['tendencias'].plot_widget
        chart.clear()
        
        x = range(len(data))
        y = [d['count'] for d in data]
        
        line = pg.PlotDataItem(x=x, y=y, pen='b')
        chart.addItem(line)
        
        ax = chart.getAxis('bottom')
        ax.setTicks([[(i, d['month'].strftime('%Y-%m')) for i, d in enumerate(data)]]) 