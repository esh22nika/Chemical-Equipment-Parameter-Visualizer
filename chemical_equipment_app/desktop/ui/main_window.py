"""
Main Application Window
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QPushButton, QFrame, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from config.settings import COLORS, WINDOW_WIDTH, WINDOW_HEIGHT, APP_VERSION
from ui.styles import get_button_style
from ui.icons import get_icon
from ui.views.dashboard_view import DashboardView
from ui.views.upload_view import UploadView
from ui.views.data_view import DataView
from ui.views.history_view import HistoryView
from ui.views.report_view import ReportView


class MainWindow(QMainWindow):
    """Main Application Window"""
    
    def __init__(self, token, user):
        super().__init__()
        self.token = token
        self.user = user
        self.current_dataset = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle('ChemFlow Analytics')
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: none;
                background-color: {COLORS['surface_secondary']};
            }}
            QTabBar::tab {{
                background-color: {COLORS['surface']};
                color: {COLORS['text_secondary']};
                padding: 12px 24px;
                margin-right: 4px;
                border: 1px solid {COLORS['border']};
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-size: 12px;
                font-weight: 500;
                min-width: 130px;
            }}
            QTabBar::tab:selected {{
                background-color: {COLORS['surface_secondary']};
                color: {COLORS['primary']};
                font-weight: 600;
            }}
            QTabBar::tab:hover {{
                background-color: {COLORS['surface_secondary']};
            }}
        """)
        
        # Create views
        self.dashboard_view = DashboardView()
        self.upload_view = UploadView()
        self.data_view = DataView()
        self.history_view = HistoryView()
        self.report_view = ReportView()
        
        # Connect signals
        self.upload_view.upload_complete.connect(self.on_dataset_uploaded)
        self.history_view.dataset_selected.connect(self.on_dataset_selected)
        
        # Add tabs
        self.tabs.addTab(self.dashboard_view, get_icon('dashboard'), 'Dashboard')
        self.tabs.addTab(self.upload_view, get_icon('upload'), 'Upload Data')
        self.tabs.addTab(self.data_view, get_icon('data_table'), 'Data Table')
        self.tabs.addTab(self.history_view, get_icon('history'), 'History')
        self.tabs.addTab(self.report_view, get_icon('report'), 'Report')
        
        main_layout.addWidget(self.tabs)
        
        central_widget.setLayout(main_layout)
    
    def create_header(self):
        """Create header"""
        header = QFrame()
        header.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface']};
                border-bottom: 1px solid {COLORS['border_light']};
            }}
        """)
        header.setFixedHeight(72)
        
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(24, 16, 24, 16)
        header_layout.setSpacing(16)
        
        # Logo and title
        title_layout = QVBoxLayout()
        title_layout.setSpacing(2)
        
        title = QLabel('ChemFlow')
        title.setFont(QFont('Arial', 18, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['primary']};")
        title_layout.addWidget(title)
        
        subtitle = QLabel('Equipment Analytics')
        subtitle.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 11px;")
        title_layout.addWidget(subtitle)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        # Version badge
        version_label = QLabel(f'v{APP_VERSION}')
        version_label.setStyleSheet(f"""
            background-color: {COLORS['primary_light']};
            color: {COLORS['primary']};
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
        """)
        header_layout.addWidget(version_label)
        
        # User info
        user_label = QLabel(f"User: {self.user['username']}")
        user_label.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            font-size: 14px;
            padding: 8px 16px;
            background-color: {COLORS['surface_secondary']};
            border-radius: 8px;
        """)
        header_layout.addWidget(user_label)
        
        # Logout button
        logout_btn = QPushButton('Logout')
        logout_btn.setStyleSheet(get_button_style('secondary'))
        logout_btn.setFixedWidth(100)
        logout_btn.clicked.connect(self.handle_logout)
        logout_btn.setCursor(Qt.PointingHandCursor)
        header_layout.addWidget(logout_btn)
        
        header.setLayout(header_layout)
        return header
    
    def handle_logout(self):
        """Handle logout"""
        reply = QMessageBox.question(
            self,
            'Logout',
            'Are you sure you want to logout',
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.close()
    
    def on_dataset_uploaded(self, dataset):
        """Handle successful dataset upload"""
        self.current_dataset = dataset
        self.dashboard_view.load_dataset(dataset)
        self.data_view.load_dataset(dataset)
        self.report_view.load_dataset(dataset)
        self.tabs.setCurrentIndex(0)  # Switch to dashboard
    
    def on_dataset_selected(self, dataset):
        """Handle dataset selection from history"""
        self.current_dataset = dataset
        self.dashboard_view.load_dataset(dataset)
        self.data_view.load_dataset(dataset)
        self.report_view.load_dataset(dataset)
        self.tabs.setCurrentIndex(0)  # Switch to dashboard
