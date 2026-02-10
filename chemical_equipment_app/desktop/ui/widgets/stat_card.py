"""
Stat Card Widget
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from config.settings import COLORS, SPACING
from ui.icons import get_icon


class StatCard(QFrame):
    """Statistic card widget"""
    
    def __init__(self, title, value='--', icon=''):
        super().__init__()
        self.title = title
        self.icon = icon
        self.init_ui(value)
    
    def init_ui(self, value):
        """Initialize UI"""
        self.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLORS['surface']}, stop:1 {COLORS['surface_secondary']});
                border: 1px solid {COLORS['border_light']};
                border-radius: 12px;
                padding: 20px;
            }}
            QFrame:hover {{
                border-color: {COLORS['border']};
                background: {COLORS['surface']};
            }}
        """)
        self.setMinimumHeight(100)
        
        layout = QVBoxLayout()
        layout.setSpacing(SPACING['xs'])
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Header with icon
        header_layout = QHBoxLayout()
        
        # Icon
        icon_label = QLabel()
        icon_pixmap = get_icon(self.icon, 18).pixmap(18, 18)
        icon_label.setPixmap(icon_pixmap)
        header_layout.addWidget(icon_label)
        
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Title
        title_label = QLabel(self.title)
        title_label.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        """)
        layout.addWidget(title_label)
        
        # Value
        self.value_label = QLabel(value)
        self.value_label.setFont(QFont('Arial', 20, QFont.Bold))
        self.value_label.setStyleSheet(f"color: {COLORS['text_primary']};")
        layout.addWidget(self.value_label)
        
        layout.addStretch()
        
        self.setLayout(layout)
    
    def set_value(self, value):
        """Set card value"""
        self.value_label.setText(str(value))
