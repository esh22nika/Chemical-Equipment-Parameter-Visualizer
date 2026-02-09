"""
Chemical Equipment Parameter Visualizer - Desktop Application
Modern PyQt5 Desktop App matching React UI design
"""

import sys
import requests
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QFileDialog, QTableWidget,
    QTableWidgetItem, QTabWidget, QMessageBox, QStackedWidget,
    QGroupBox, QGridLayout, QHeaderView, QFrame
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# API Configuration
API_BASE_URL = 'http://localhost:8000/api'

# Modern Color Scheme (matching React app)
COLORS = {
    'primary': '#0A6EBD',
    'primary_dark': '#084F87',
    'accent': '#00D4AA',
    'surface': '#FFFFFF',
    'surface_secondary': '#F8FAFB',
    'text_primary': '#0F1419',
    'text_secondary': '#536471',
    'border': '#E1E8ED',
    'success': '#059669',
    'error': '#DC2626'
}


def set_modern_style(app):
    """Apply modern styling to the application"""
    app.setStyle('Fusion')
    
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(COLORS['surface_secondary']))
    palette.setColor(QPalette.WindowText, QColor(COLORS['text_primary']))
    palette.setColor(QPalette.Base, QColor(COLORS['surface']))
    palette.setColor(QPalette.AlternateBase, QColor(COLORS['surface_secondary']))
    palette.setColor(QPalette.ToolTipBase, QColor(COLORS['text_primary']))
    palette.setColor(QPalette.ToolTipText, QColor(COLORS['surface']))
    palette.setColor(QPalette.Text, QColor(COLORS['text_primary']))
    palette.setColor(QPalette.Button, QColor(COLORS['surface']))
    palette.setColor(QPalette.ButtonText, QColor(COLORS['text_primary']))
    palette.setColor(QPalette.Highlight, QColor(COLORS['primary']))
    palette.setColor(QPalette.HighlightedText, QColor(COLORS['surface']))
    
    app.setPalette(palette)


class ModernButton(QPushButton):
    """Modern styled button component"""
    def __init__(self, text, variant='primary', parent=None):
        super().__init__(text, parent)
        self.variant = variant
        self.apply_style()
        
    def apply_style(self):
        if self.variant == 'primary':
            self.setStyleSheet(f"""
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
                QPushButton:disabled {{
                    background-color: #CBD5E1;
                    color: #94A3B8;
                }}
            """)
        elif self.variant == 'secondary':
            self.setStyleSheet(f"""
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
            """)
        elif self.variant == 'danger':
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['error']};
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 16px;
                    font-size: 14px;
                }}
                QPushButton:hover {{
                    background-color: #B91C1C;
                }}
            """)


class ModernCard(QFrame):
    """Modern card component"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
                padding: 20px;
            }}
        """)
        self.setFrameShape(QFrame.StyledPanel)


class LoginWindow(QWidget):
    """Modern Login/Register Window"""
    login_success = pyqtSignal(str, dict)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('ChemFlow Analytics - Login')
        self.setFixedSize(450, 550)
        self.setStyleSheet(f"background-color: {COLORS['surface_secondary']};")
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Logo and Title
        title_layout = QVBoxLayout()
        title_layout.setAlignment(Qt.AlignCenter)
        
        title = QLabel('ChemFlow')
        title.setFont(QFont('Arial', 28, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['primary']};")
        title.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title)
        
        subtitle = QLabel('Equipment Analytics Platform')
        subtitle.setFont(QFont('Arial', 12))
        subtitle.setStyleSheet(f"color: {COLORS['text_secondary']};")
        subtitle.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(subtitle)
        
        layout.addLayout(title_layout)
        layout.addSpacing(20)
        
        # Login Card
        card = ModernCard()
        card_layout = QVBoxLayout()
        card_layout.setSpacing(15)
        
        # Username
        username_label = QLabel('Username')
        username_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-weight: 600; font-size: 14px;")
        card_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter your username')
        self.username_input.setStyleSheet(f"""
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
        """)
        card_layout.addWidget(self.username_input)
        
        # Password
        password_label = QLabel('Password')
        password_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-weight: 600; font-size: 14px;")
        card_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Enter your password')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(f"""
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
        """)
        card_layout.addWidget(self.password_input)
        
        # Buttons
        self.login_btn = ModernButton('Sign In', 'primary')
        self.login_btn.clicked.connect(self.handle_login)
        card_layout.addWidget(self.login_btn)
        
        self.register_btn = ModernButton('Create Account', 'secondary')
        self.register_btn.clicked.connect(self.handle_register)
        card_layout.addWidget(self.register_btn)
        
        # Status label
        self.status_label = QLabel('')
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        card_layout.addWidget(self.status_label)
        
        card.setLayout(card_layout)
        layout.addWidget(card)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            self.show_error('Please enter username and password')
            return
        
        try:
            response = requests.post(
                f'{API_BASE_URL}/auth/login/',
                json={'username': username, 'password': password}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.login_success.emit(data['token'], data['user'])
                self.close()
            else:
                self.show_error('Invalid credentials')
        except Exception as e:
            self.show_error(f'Connection error: {str(e)}')
    
    def handle_register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            self.show_error('Please enter username and password')
            return
        
        try:
            response = requests.post(
                f'{API_BASE_URL}/auth/register/',
                json={
                    'username': username,
                    'password': password,
                    'email': f'{username}@example.com'
                }
            )
            
            if response.status_code == 201:
                data = response.json()
                self.login_success.emit(data['token'], data['user'])
                self.close()
            else:
                self.show_error('Registration failed - username may be taken')
        except Exception as e:
            self.show_error(f'Connection error: {str(e)}')
    
    def show_error(self, message):
        self.status_label.setStyleSheet(f"color: {COLORS['error']}; font-size: 13px; padding: 10px;")
        self.status_label.setText(f'❌ {message}')


class MplCanvas(FigureCanvas):
    """Matplotlib canvas for PyQt5"""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)


class MainWindow(QMainWindow):
    """Main Application Window - Modern Design"""
    
    def __init__(self, token, user):
        super().__init__()
        self.token = token
        self.user = user
        self.current_dataset = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('ChemFlow Analytics')
        self.setGeometry(100, 100, 1400, 900)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Header/Navbar
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Tab widget (styled)
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
                font-size: 14px;
                font-weight: 500;
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
        
        self.tabs.addTab(self.create_upload_tab(), '📤 Upload Data')
        self.tabs.addTab(self.create_dashboard_tab(), '📊 Dashboard')
        self.tabs.addTab(self.create_data_tab(), '📋 Data Table')
        self.tabs.addTab(self.create_history_tab(), '🕒 History')
        
        main_layout.addWidget(self.tabs)
        
        central_widget.setLayout(main_layout)
    
    def create_header(self):
        """Create modern header/navbar"""
        header = QFrame()
        header.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface']};
                border-bottom: 1px solid {COLORS['border']};
                padding: 16px 24px;
            }}
        """)
        header.setFixedHeight(72)
        
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # Logo and title
        title_layout = QVBoxLayout()
        title = QLabel('ChemFlow')
        title.setFont(QFont('Arial', 18, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['primary']};")
        title_layout.addWidget(title)
        
        subtitle = QLabel('Equipment Analytics')
        subtitle.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 11px;")
        title_layout.addWidget(subtitle)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        # User info
        user_label = QLabel(f'👤 {self.user["username"]}')
        user_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 14px; padding: 8px 16px;")
        header_layout.addWidget(user_label)
        
        # Logout button
        logout_btn = ModernButton('Logout', 'secondary')
        logout_btn.setFixedWidth(100)
        logout_btn.clicked.connect(self.handle_logout)
        header_layout.addWidget(logout_btn)
        
        header.setLayout(header_layout)
        return header
    
    def handle_logout(self):
        reply = QMessageBox.question(self, 'Logout', 'Are you sure you want to logout?',
                                      QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()
            # Show login window again
            login_window = LoginWindow()
            login_window.show()
    
    def create_upload_tab(self):
        """Create modern upload CSV tab"""
        widget = QWidget()
        widget.setStyleSheet(f"background-color: {COLORS['surface_secondary']};")
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Title
        title = QLabel('Upload Equipment Data')
        title.setFont(QFont('Arial', 24, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['text_primary']};")
        layout.addWidget(title)
        
        subtitle = QLabel('Import CSV files containing chemical equipment parameters for analysis')
        subtitle.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 14px;")
        layout.addWidget(subtitle)
        
        # Upload card
        card = ModernCard()
        card_layout = QVBoxLayout()
        
        # Instructions
        instructions = QLabel(
            'Upload a CSV file with columns:\n'
            'Equipment Name, Type, Flowrate, Pressure, Temperature'
        )
        instructions.setStyleSheet(f'padding: 16px; background-color: {COLORS["surface_secondary"]}; '
                                   f'border-radius: 8px; color: {COLORS["text_secondary"]}; font-size: 13px;')
        instructions.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(instructions)
        
        # File selection
        file_layout = QHBoxLayout()
        self.file_path_label = QLabel('No file selected')
        self.file_path_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 14px;")
        file_layout.addWidget(self.file_path_label)
        
        browse_btn = ModernButton('Browse', 'secondary')
        browse_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(browse_btn)
        
        card_layout.addLayout(file_layout)
        
        # Upload button
        self.upload_btn = ModernButton('Upload and Analyze', 'primary')
        self.upload_btn.clicked.connect(self.upload_file)
        self.upload_btn.setEnabled(False)
        card_layout.addWidget(self.upload_btn)
        
        # Status
        self.upload_status = QLabel('')
        self.upload_status.setAlignment(Qt.AlignCenter)
        self.upload_status.setWordWrap(True)
        card_layout.addWidget(self.upload_status)
        
        card.setLayout(card_layout)
        layout.addWidget(card)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_dashboard_tab(self):
        """Create dashboard with charts"""
        widget = QWidget()
        widget.setStyleSheet(f"background-color: {COLORS['surface_secondary']};")
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Title
        title = QLabel('Analytics Dashboard')
        title.setFont(QFont('Arial', 24, QFont.Bold))
        layout.addWidget(title)
        
        # Summary cards in grid
        summary_group = QGroupBox()
        summary_group.setStyleSheet("QGroupBox { border: none; }")
        summary_layout = QGridLayout()
        summary_layout.setSpacing(16)
        
        self.total_count_label = self.create_stat_card('Total Equipment', '--')
        self.avg_flowrate_label = self.create_stat_card('Avg Flowrate', '--')
        self.avg_pressure_label = self.create_stat_card('Avg Pressure', '--')
        self.avg_temp_label = self.create_stat_card('Avg Temperature', '--')
        
        summary_layout.addWidget(self.total_count_label, 0, 0)
        summary_layout.addWidget(self.avg_flowrate_label, 0, 1)
        summary_layout.addWidget(self.avg_pressure_label, 1, 0)
        summary_layout.addWidget(self.avg_temp_label, 1, 1)
        
        summary_group.setLayout(summary_layout)
        layout.addWidget(summary_group)
        
        # Charts
        charts_layout = QHBoxLayout()
        
        self.pie_canvas = MplCanvas(self, width=5, height=4, dpi=100)
        charts_layout.addWidget(self.pie_canvas)
        
        self.bar_canvas = MplCanvas(self, width=5, height=4, dpi=100)
        charts_layout.addWidget(self.bar_canvas)
        
        layout.addLayout(charts_layout)
        
        widget.setLayout(layout)
        return widget
    
    def create_stat_card(self, title, value):
        """Create a modern stat card"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLORS['surface']}, stop:1 {COLORS['surface_secondary']});
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
                padding: 20px;
            }}
        """)
        
        layout = QVBoxLayout()
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px; font-weight: 600;")
        layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setFont(QFont('Arial', 28, QFont.Bold))
        value_label.setStyleSheet(f"color: {COLORS['text_primary']};")
        layout.addWidget(value_label)
        
        card.setLayout(layout)
        card.value_label = value_label  # Store reference for updates
        return card
    
    def create_data_tab(self):
        """Create data table tab"""
        widget = QWidget()
        widget.setStyleSheet(f"background-color: {COLORS['surface_secondary']};")
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Title
        title = QLabel('Equipment Data')
        title.setFont(QFont('Arial', 24, QFont.Bold))
        layout.addWidget(title)
        
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(5)
        self.data_table.setHorizontalHeaderLabels([
            'Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'
        ])
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.data_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                gridline-color: {COLORS['border']};
            }}
            QHeaderView::section {{
                background-color: {COLORS['primary']};
                color: white;
                padding: 12px;
                border: none;
                font-weight: 600;
            }}
        """)
        
        layout.addWidget(self.data_table)
        
        # Download PDF button
        pdf_btn = ModernButton('📄 Download PDF Report', 'primary')
        pdf_btn.clicked.connect(self.download_pdf)
        layout.addWidget(pdf_btn)
        
        widget.setLayout(layout)
        return widget
    
    def create_history_tab(self):
        """Create history tab"""
        widget = QWidget()
        widget.setStyleSheet(f"background-color: {COLORS['surface_secondary']};")
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Title
        title = QLabel('Upload History')
        title.setFont(QFont('Arial', 24, QFont.Bold))
        layout.addWidget(title)
        
        # Refresh button
        refresh_btn = ModernButton('🔄 Refresh History', 'secondary')
        refresh_btn.clicked.connect(self.load_history)
        layout.addWidget(refresh_btn)
        
        # History table
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(6)
        self.history_table.setHorizontalHeaderLabels([
            'ID', 'Filename', 'Upload Date', 'Total Count', 'Avg Flowrate', 'Avg Pressure'
        ])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.history_table.cellDoubleClicked.connect(self.load_dataset_from_history)
        self.history_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
            }}
            QHeaderView::section {{
                background-color: {COLORS['primary']};
                color: white;
                padding: 12px;
                border: none;
                font-weight: 600;
            }}
        """)
        
        layout.addWidget(self.history_table)
        
        widget.setLayout(layout)
        return widget
    
    def browse_file(self):
        """Browse for CSV file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            'Select CSV File',
            '',
            'CSV Files (*.csv)'
        )
        
        if file_path:
            self.selected_file = file_path
            self.file_path_label.setText(file_path)
            self.upload_btn.setEnabled(True)
    
    def upload_file(self):
        """Upload CSV file to backend"""
        try:
            with open(self.selected_file, 'rb') as f:
                files = {'file': f}
                headers = {'Authorization': f'Token {self.token}'}
                
                response = requests.post(
                    f'{API_BASE_URL}/upload/',
                    files=files,
                    headers=headers
                )
                
                if response.status_code == 201:
                    self.current_dataset = response.json()
                    self.upload_status.setStyleSheet(f"color: {COLORS['success']}; font-size: 14px; padding: 10px;")
                    self.upload_status.setText('✅ File uploaded successfully!')
                    self.update_dashboard()
                    self.update_data_table()
                    self.tabs.setCurrentIndex(1)  # Switch to dashboard
                else:
                    error_msg = response.json().get('error', 'Upload failed')
                    self.upload_status.setStyleSheet(f"color: {COLORS['error']}; font-size: 14px;")
                    self.upload_status.setText(f'❌ Error: {error_msg}')
        
        except Exception as e:
            self.upload_status.setStyleSheet(f"color: {COLORS['error']}; font-size: 14px;")
            self.upload_status.setText(f'❌ Error: {str(e)}')
    
    def update_dashboard(self):
        """Update dashboard with current dataset"""
        if not self.current_dataset:
            return
        
        # Update summary cards
        self.total_count_label.value_label.setText(str(self.current_dataset["total_count"]))
        self.avg_flowrate_label.value_label.setText(f'{self.current_dataset["avg_flowrate"]:.2f}')
        self.avg_pressure_label.value_label.setText(f'{self.current_dataset["avg_pressure"]:.2f}')
        self.avg_temp_label.value_label.setText(f'{self.current_dataset["avg_temperature"]:.2f}')
        
        # Update pie chart
        self.pie_canvas.axes.clear()
        types = list(self.current_dataset['equipment_type_distribution'].keys())
        counts = list(self.current_dataset['equipment_type_distribution'].values())
        colors = ['#0A6EBD', '#00D4AA', '#F59E0B', '#DC2626', '#8B5CF6']
        self.pie_canvas.axes.pie(counts, labels=types, autopct='%1.1f%%', colors=colors)
        self.pie_canvas.axes.set_title('Equipment Type Distribution', fontsize=14, fontweight='bold')
        self.pie_canvas.draw()
        
        # Update bar chart
        self.bar_canvas.axes.clear()
        params = ['Flowrate', 'Pressure', 'Temperature']
        values = [
            self.current_dataset['avg_flowrate'],
            self.current_dataset['avg_pressure'],
            self.current_dataset['avg_temperature']
        ]
        bars = self.bar_canvas.axes.bar(params, values, color=['#0A6EBD', '#00D4AA', '#F59E0B'])
        self.bar_canvas.axes.set_title('Average Parameters', fontsize=14, fontweight='bold')
        self.bar_canvas.axes.set_ylabel('Value')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            self.bar_canvas.axes.text(bar.get_x() + bar.get_width()/2., height,
                                      f'{height:.1f}', ha='center', va='bottom')
        
        self.bar_canvas.draw()
    
    def update_data_table(self):
        """Update data table with current dataset"""
        if not self.current_dataset:
            return
        
        data = self.current_dataset.get('data', [])
        self.data_table.setRowCount(len(data))
        
        for row_idx, row_data in enumerate(data):
            self.data_table.setItem(row_idx, 0, QTableWidgetItem(row_data['Equipment Name']))
            self.data_table.setItem(row_idx, 1, QTableWidgetItem(row_data['Type']))
            self.data_table.setItem(row_idx, 2, QTableWidgetItem(f"{row_data['Flowrate']:.2f}"))
            self.data_table.setItem(row_idx, 3, QTableWidgetItem(f"{row_data['Pressure']:.2f}"))
            self.data_table.setItem(row_idx, 4, QTableWidgetItem(f"{row_data['Temperature']:.2f}"))
    
    def load_history(self):
        """Load upload history"""
        try:
            headers = {'Authorization': f'Token {self.token}'}
            response = requests.get(f'{API_BASE_URL}/history/', headers=headers)
            
            if response.status_code == 200:
                history = response.json()
                self.history_table.setRowCount(len(history))
                
                for row_idx, dataset in enumerate(history):
                    self.history_table.setItem(row_idx, 0, QTableWidgetItem(str(dataset['id'])))
                    self.history_table.setItem(row_idx, 1, QTableWidgetItem(dataset['filename']))
                    self.history_table.setItem(row_idx, 2, QTableWidgetItem(dataset['upload_date']))
                    self.history_table.setItem(row_idx, 3, QTableWidgetItem(str(dataset['total_count'])))
                    self.history_table.setItem(row_idx, 4, QTableWidgetItem(f"{dataset['avg_flowrate']:.2f}"))
                    self.history_table.setItem(row_idx, 5, QTableWidgetItem(f"{dataset['avg_pressure']:.2f}"))
        
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to load history: {str(e)}')
    
    def load_dataset_from_history(self, row, col):
        """Load dataset when double-clicked in history"""
        dataset_id = self.history_table.item(row, 0).text()
        
        try:
            headers = {'Authorization': f'Token {self.token}'}
            response = requests.get(f'{API_BASE_URL}/datasets/{dataset_id}/', headers=headers)
            
            if response.status_code == 200:
                self.current_dataset = response.json()
                self.update_dashboard()
                self.update_data_table()
                self.tabs.setCurrentIndex(1)  # Switch to dashboard
        
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to load dataset: {str(e)}')
    
    def download_pdf(self):
        """Download PDF report"""
        if not self.current_dataset:
            QMessageBox.warning(self, 'Warning', 'No dataset loaded')
            return
        
        try:
            headers = {'Authorization': f'Token {self.token}'}
            response = requests.get(
                f'{API_BASE_URL}/datasets/{self.current_dataset["id"]}/download_pdf/',
                headers=headers
            )
            
            if response.status_code == 200:
                file_path, _ = QFileDialog.getSaveFileName(
                    self,
                    'Save PDF Report',
                    f'report_{self.current_dataset["id"]}.pdf',
                    'PDF Files (*.pdf)'
                )
                
                if file_path:
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    QMessageBox.information(self, 'Success', 'PDF downloaded successfully!')
        
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to download PDF: {str(e)}')


def main():
    app = QApplication(sys.argv)
    set_modern_style(app)
    
    # Store reference to main window to prevent garbage collection
    main_window_ref = {'window': None}
    
    # Show login window
    login_window = LoginWindow()
    
    def on_login_success(token, user):
        main_window_ref['window'] = MainWindow(token, user)
        main_window_ref['window'].show()
    
    login_window.login_success.connect(on_login_success)
    login_window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()