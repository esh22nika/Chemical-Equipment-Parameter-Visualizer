"""
History View
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QPushButton, QScrollArea, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from config.settings import COLORS, SPACING
from ui.styles import get_button_style
from services.api_service import api_service
from datetime import datetime


class HistoryView(QWidget):
    """Upload history view"""
    
    dataset_selected = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_history()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(SPACING['lg'])
        
        # Header
        header_layout = QHBoxLayout()
        
        title_layout = QVBoxLayout()
        title_layout.setSpacing(SPACING['xs'])
        
        title = QLabel('Upload History')
        title.setFont(QFont('Arial', 24, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['text_primary']};")
        title_layout.addWidget(title)
        
        subtitle = QLabel('Last 5 uploaded datasets')
        subtitle.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 14px;")
        title_layout.addWidget(subtitle)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        # Refresh button
        refresh_btn = QPushButton('🔄 Refresh')
        refresh_btn.setStyleSheet(get_button_style('secondary'))
        refresh_btn.clicked.connect(self.load_history)
        refresh_btn.setCursor(Qt.PointingHandCursor)
        header_layout.addWidget(refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Scroll area for history cards
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.history_container = QWidget()
        self.history_layout = QVBoxLayout()
        self.history_layout.setSpacing(SPACING['lg'])
        self.history_container.setLayout(self.history_layout)
        
        scroll.setWidget(self.history_container)
        layout.addWidget(scroll)
        
        # Status label
        self.status_label = QLabel('')
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 14px;")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
    
    def load_history(self):
        """Load upload history"""
        try:
            self.status_label.setText('Loading...')
            
            # Clear existing cards
            for i in reversed(range(self.history_layout.count())):
                widget = self.history_layout.itemAt(i).widget()
                if widget:
                    widget.deleteLater()
            
            # Fetch history
            history = api_service.get_history()
            
            if not history:
                self.status_label.setText('No upload history found')
                return
            
            self.status_label.setText('')
            
            # Create card for each dataset
            for dataset in history:
                card = self.create_history_card(dataset)
                self.history_layout.addWidget(card)
            
            # Add stretch at end
            self.history_layout.addStretch()
            
        except Exception as e:
            self.status_label.setText(f'Error loading history: {str(e)}')
    
    def create_history_card(self, dataset):
        """Create history card widget"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border_light']};
                border-radius: 12px;
                padding: 20px;
            }}
            QFrame:hover {{
                border-color: {COLORS['border']};
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(SPACING['md'])
        
        # Header
        header_layout = QHBoxLayout()
        
        # File icon and name
        file_layout = QHBoxLayout()
        file_layout.setSpacing(SPACING['sm'])
        
        icon = QLabel('📊')
        icon.setFont(QFont('Arial', 20))
        file_layout.addWidget(icon)
        
        file_info = QVBoxLayout()
        file_info.setSpacing(4)
        
        filename = QLabel(dataset['filename'])
        filename.setFont(QFont('Arial', 14, QFont.Bold))
        filename.setStyleSheet(f"color: {COLORS['text_primary']};")
        file_info.addWidget(filename)
        
        # Format date
        try:
            date_obj = datetime.fromisoformat(dataset['upload_date'].replace('Z', '+00:00'))
            date_str = date_obj.strftime('%b %d, %Y %I:%M %p')
        except:
            date_str = dataset['upload_date']
        
        date_label = QLabel(date_str)
        date_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        file_info.addWidget(date_label)
        
        file_layout.addLayout(file_info)
        
        header_layout.addLayout(file_layout)
        header_layout.addStretch()
        
        # Dataset ID badge
        id_badge = QLabel(f"ID: {dataset['id']}")
        id_badge.setStyleSheet(f"""
            background-color: {COLORS['primary']};
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
        """)
        header_layout.addWidget(id_badge)
        
        layout.addLayout(header_layout)
        
        # Statistics grid
        stats_grid = QHBoxLayout()
        stats_grid.setSpacing(SPACING['lg'])
        
        stats = [
            ('📦 Count', dataset['total_count']),
            ('💧 Flowrate', f"{dataset['avg_flowrate']:.1f}"),
            ('⚡ Pressure', f"{dataset['avg_pressure']:.1f}"),
            ('🌡️ Temp', f"{dataset['avg_temperature']:.1f}")
        ]
        
        for label, value in stats:
            stat_widget = QVBoxLayout()
            stat_widget.setSpacing(4)
            
            stat_label = QLabel(label)
            stat_label.setStyleSheet(f"color: {COLORS['text_tertiary']}; font-size: 11px;")
            stat_widget.addWidget(stat_label)
            
            stat_value = QLabel(str(value))
            stat_value.setFont(QFont('Arial', 14, QFont.Bold))
            stat_value.setStyleSheet(f"color: {COLORS['text_primary']};")
            stat_widget.addWidget(stat_value)
            
            stats_grid.addLayout(stat_widget)
        
        stats_grid.addStretch()
        layout.addLayout(stats_grid)
        
        # Equipment types
        if dataset.get('equipment_type_distribution'):
            types_layout = QVBoxLayout()
            types_layout.setSpacing(SPACING['sm'])
            
            types_label = QLabel('Equipment Types:')
            types_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px; font-weight: 600;")
            types_layout.addWidget(types_label)
            
            badges_layout = QHBoxLayout()
            badges_layout.setSpacing(SPACING['sm'])
            
            for eq_type, count in dataset['equipment_type_distribution'].items():
                badge = QLabel(f"{eq_type}: {count}")
                badge.setStyleSheet(f"""
                    background-color: {COLORS['primary_light']};
                    color: {COLORS['primary']};
                    padding: 4px 10px;
                    border-radius: 12px;
                    font-size: 11px;
                    font-weight: 600;
                """)
                badges_layout.addWidget(badge)
            
            badges_layout.addStretch()
            types_layout.addLayout(badges_layout)
            layout.addLayout(types_layout)
        
        # Actions
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(SPACING['sm'])
        
        view_btn = QPushButton('👁️ View Details')
        view_btn.setStyleSheet(get_button_style('primary'))
        view_btn.clicked.connect(lambda: self.view_dataset(dataset['id']))
        view_btn.setCursor(Qt.PointingHandCursor)
        actions_layout.addWidget(view_btn, 1)
        
        delete_btn = QPushButton('🗑️ Delete')
        delete_btn.setStyleSheet(get_button_style('danger'))
        delete_btn.clicked.connect(lambda: self.delete_dataset(dataset['id']))
        delete_btn.setCursor(Qt.PointingHandCursor)
        actions_layout.addWidget(delete_btn, 0)
        
        layout.addLayout(actions_layout)
        
        card.setLayout(layout)
        return card
    
    def view_dataset(self, dataset_id):
        """View dataset details"""
        try:
            dataset = api_service.get_dataset(dataset_id)
            self.dataset_selected.emit(dataset)
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to load dataset: {str(e)}')
    
    def delete_dataset(self, dataset_id):
        """Delete dataset"""
        reply = QMessageBox.question(
            self,
            'Confirm Delete',
            'Are you sure you want to delete this dataset?',
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                api_service.delete_dataset(dataset_id)
                self.load_history()
                QMessageBox.information(self, 'Success', 'Dataset deleted successfully')
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'Failed to delete dataset: {str(e)}')