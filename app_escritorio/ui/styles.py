from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor
from config import UI_CONFIG

def apply_stylesheet(window):
    """Aplicar estilos a la aplicación"""
    app = QApplication.instance()
    
    # Estilo base
    style = f"""
        QMainWindow {{
            background-color: #f0f0f0;
        }}
        
        QTabWidget::pane {{
            border: 1px solid #cccccc;
            background-color: white;
        }}
        
        QTabWidget::tab-bar {{
            left: 5px;
        }}
        
        QTabBar::tab {{
            background-color: #e1e1e1;
            border: 1px solid #cccccc;
            padding: {UI_CONFIG['padding']}px;
            margin-right: 2px;
        }}
        
        QTabBar::tab:selected {{
            background-color: white;
            border-bottom-color: white;
        }}
        
        QTabBar::tab:!selected {{
            margin-top: 2px;
        }}
        
        QPushButton {{
            background-color: #0078d4;
            color: white;
            border: none;
            padding: 5px 15px;
            border-radius: 3px;
            min-width: {UI_CONFIG['button_width']}px;
            min-height: {UI_CONFIG['button_height']}px;
        }}
        
        QPushButton:hover {{
            background-color: #106ebe;
        }}
        
        QPushButton:pressed {{
            background-color: #005a9e;
        }}
        
        QPushButton:disabled {{
            background-color: #cccccc;
        }}
        
        QLineEdit {{
            padding: 5px;
            border: 1px solid #cccccc;
            border-radius: 3px;
        }}
        
        QLineEdit:focus {{
            border: 1px solid #0078d4;
        }}
        
        QComboBox {{
            padding: 5px;
            border: 1px solid #cccccc;
            border-radius: 3px;
            min-width: 100px;
        }}
        
        QComboBox:focus {{
            border: 1px solid #0078d4;
        }}
        
        QTableWidget {{
            border: 1px solid #cccccc;
            gridline-color: #e1e1e1;
        }}
        
        QTableWidget::item {{
            padding: 5px;
        }}
        
        QTableWidget::item:selected {{
            background-color: #0078d4;
            color: white;
        }}
        
        QHeaderView::section {{
            background-color: #f0f0f0;
            padding: 5px;
            border: 1px solid #cccccc;
            font-weight: bold;
        }}
        
        QLabel {{
            color: #333333;
        }}
        
        QMessageBox {{
            background-color: white;
        }}
        
        QMessageBox QPushButton {{
            min-width: 80px;
        }}
    """
    
    # Aplicar estilo
    app.setStyleSheet(style)
    
    # Configurar paleta de colores
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor("#f0f0f0"))
    palette.setColor(QPalette.ColorRole.WindowText, QColor("#333333"))
    palette.setColor(QPalette.ColorRole.Base, QColor("white"))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#f5f5f5"))
    palette.setColor(QPalette.ColorRole.Text, QColor("#333333"))
    palette.setColor(QPalette.ColorRole.Button, QColor("#e1e1e1"))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor("#333333"))
    palette.setColor(QPalette.ColorRole.Link, QColor("#0078d4"))
    palette.setColor(QPalette.ColorRole.Highlight, QColor("#0078d4"))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("white"))
    
    app.setPalette(palette)
    
    # Configurar fuente
    font = app.font()
    font.setFamily(UI_CONFIG['font_family'])
    font.setPointSize(UI_CONFIG['font_size'])
    app.setFont(font) 