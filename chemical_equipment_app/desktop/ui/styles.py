"""
Global Styles and Theme
"""

from PyQt5.QtGui import QPalette, QColor
from config.settings import COLORS


def apply_global_styles(app):
    """Apply global application styles"""
    
    # Set palette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(COLORS['surface_secondary']))
    palette.setColor(QPalette.WindowText, QColor(COLORS['text_primary']))
    palette.setColor(QPalette.Base, QColor(COLORS['surface']))
    palette.setColor(QPalette.AlternateBase, QColor(COLORS['surface_secondary']))
    palette.setColor(QPalette.Text, QColor(COLORS['text_primary']))
    palette.setColor(QPalette.Button, QColor(COLORS['surface']))
    palette.setColor(QPalette.ButtonText, QColor(COLORS['text_primary']))
    palette.setColor(QPalette.Highlight, QColor(COLORS['primary']))
    palette.setColor(QPalette.HighlightedText, QColor(COLORS['surface']))
    
    app.setPalette(palette)
    
    # Set global stylesheet
    stylesheet = f"""
        QWidget {{
            font-family: 'Segoe UI', 'Arial', sans-serif;
            font-size: 9pt;
        }}
        
        QMainWindow {{
            background-color: {COLORS['surface_secondary']};
        }}
        
        QScrollArea {{
            border: none;
            background-color: transparent;
        }}
        
        QScrollBar:vertical {{
            background: {COLORS['surface_secondary']};
            width: 12px;
            margin: 0px;
        }}
        
        QScrollBar::handle:vertical {{
            background: {COLORS['border']};
            border-radius: 6px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background: {COLORS['text_tertiary']};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        
        QScrollBar:horizontal {{
            background: {COLORS['surface_secondary']};
            height: 12px;
            margin: 0px;
        }}
        
        QScrollBar::handle:horizontal {{
            background: {COLORS['border']};
            border-radius: 6px;
            min-width: 20px;
        }}
        
        QScrollBar::handle:horizontal:hover {{
            background: {COLORS['text_tertiary']};
        }}
        
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}
        
        QToolTip {{
            background-color: {COLORS['text_primary']};
            color: {COLORS['surface']};
            border: 1px solid {COLORS['border']};
            border-radius: 4px;
            padding: 4px;
        }}
    """
    
    app.setStyleSheet(stylesheet)


def get_button_style(variant='primary'):
    """Get button stylesheet"""
    
    if variant == 'primary':
        return f"""
            QPushButton {{
                background-color: {COLORS['primary']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {COLORS['primary_dark']};
            }}
            QPushButton:pressed {{
                background-color: {COLORS['primary_dark']};
            }}
            QPushButton:disabled {{
                background-color: #CBD5E1;
                color: #94A3B8;
            }}
        """
    elif variant == 'secondary':
        return f"""
            QPushButton {{
                background-color: {COLORS['surface']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {COLORS['surface_secondary']};
                border-color: {COLORS['primary']};
            }}
            QPushButton:pressed {{
                background-color: {COLORS['surface_tertiary']};
            }}
            QPushButton:disabled {{
                opacity: 0.5;
            }}
        """
    elif variant == 'danger':
        return f"""
            QPushButton {{
                background-color: {COLORS['danger']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: #B91C1C;
            }}
        """
    elif variant == 'success':
        return f"""
            QPushButton {{
                background-color: {COLORS['success']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: #047857;
            }}
        """


def get_card_style():
    """Get card stylesheet"""
    return f"""
        QFrame {{
            background-color: {COLORS['surface']};
            border: 1px solid {COLORS['border_light']};
            border-radius: 12px;
        }}
    """


def get_input_style():
    """Get input field stylesheet"""
    return f"""
        QLineEdit {{
            padding: 12px;
            border: 1px solid {COLORS['border']};
            border-radius: 6px;
            font-size: 14px;
            background-color: {COLORS['surface']};
        }}
        QLineEdit:focus {{
            border: 2px solid {COLORS['primary']};
        }}
    """