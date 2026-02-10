"""
Login Window
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QFrame, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap
from config.settings import COLORS
from ui.styles import get_button_style, get_input_style
from services.api_service import api_service


class LoginWindow(QWidget):
    """Login/Register Window"""
    
    login_success = pyqtSignal(str, dict)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle('ChemFlow Analytics - Login')
        self.setFixedSize(500, 600)
        self.setStyleSheet(f"background-color: {COLORS['surface_secondary']};")
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Logo and Title
        title_layout = QVBoxLayout()
        title_layout.setAlignment(Qt.AlignCenter)
        title_layout.setSpacing(8)
        
        title = QLabel('ChemFlow')
        title.setFont(QFont('Arial', 32, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['primary']};")
        title.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title)
        
        subtitle = QLabel('Equipment Analytics Platform')
        subtitle.setFont(QFont('Arial', 13))
        subtitle.setStyleSheet(f"color: {COLORS['text_secondary']};")
        subtitle.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(subtitle)
        
        layout.addLayout(title_layout)
        layout.addSpacing(20)
        
        # Login Card
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border_light']};
                border-radius: 12px;
                padding: 20px;
            }}
        """)
        card_layout = QVBoxLayout()
        card_layout.setSpacing(16)
        
        # Card Title
        card_title = QLabel('Welcome Back')
        card_title.setFont(QFont('Arial', 18, QFont.Bold))
        card_title.setStyleSheet(f"color: {COLORS['text_primary']};")
        card_title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(card_title)
        
        card_subtitle = QLabel('Sign in to access your analytics')
        card_subtitle.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 13px;")
        card_subtitle.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(card_subtitle)
        
        card_layout.addSpacing(10)
        
        # Username
        username_label = QLabel('Username')
        username_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-weight: 600; font-size: 14px;")
        card_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter your username')
        self.username_input.setStyleSheet(get_input_style())
        card_layout.addWidget(self.username_input)
        
        # Password
        password_label = QLabel('Password')
        password_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-weight: 600; font-size: 14px;")
        card_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Enter your password')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(get_input_style())
        self.password_input.returnPressed.connect(self.handle_login)
        card_layout.addWidget(self.password_input)
        
        # Buttons
        self.login_btn = QPushButton('Sign In')
        self.login_btn.setStyleSheet(get_button_style('primary'))
        self.login_btn.clicked.connect(self.handle_login)
        self.login_btn.setCursor(Qt.PointingHandCursor)
        card_layout.addWidget(self.login_btn)
        
        self.register_btn = QPushButton('Create Account')
        self.register_btn.setStyleSheet(get_button_style('secondary'))
        self.register_btn.clicked.connect(self.handle_register)
        self.register_btn.setCursor(Qt.PointingHandCursor)
        card_layout.addWidget(self.register_btn)
        
        # Status label
        self.status_label = QLabel('')
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet("font-size: 13px; padding: 10px;")
        card_layout.addWidget(self.status_label)
        
        card.setLayout(card_layout)
        layout.addWidget(card)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def handle_login(self):
        """Handle login"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            self.show_error('Please enter username and password')
            return
        
        try:
            self.login_btn.setEnabled(False)
            self.login_btn.setText('Signing in...')
            
            data = api_service.login(username, password)
            api_service.set_token(data['token'])
            
            self.login_success.emit(data['token'], data['user'])
            self.close()
            
        except Exception as e:
            error_msg = str(e)
            if 'Invalid credentials' in error_msg or '401' in error_msg:
                self.show_error('Invalid username or password')
            else:
                self.show_error(f'Connection error: {error_msg}')
        finally:
            self.login_btn.setEnabled(True)
            self.login_btn.setText('Sign In')
    
    def handle_register(self):
        """Handle registration"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            self.show_error('Please enter username and password')
            return
        
        try:
            self.register_btn.setEnabled(False)
            self.register_btn.setText('Creating account...')
            
            email = f'{username}@example.com'
            data = api_service.register(username, email, password)
            api_service.set_token(data['token'])
            
            self.login_success.emit(data['token'], data['user'])
            self.close()
            
        except Exception as e:
            error_msg = str(e)
            if 'username' in error_msg.lower():
                self.show_error('Username already taken')
            else:
                self.show_error(f'Registration failed: {error_msg}')
        finally:
            self.register_btn.setEnabled(True)
            self.register_btn.setText('Create Account')
    
    def show_error(self, message):
        """Show error message"""
        self.status_label.setStyleSheet(f"color: {COLORS['danger']}; font-size: 13px; padding: 10px;")
        self.status_label.setText(f'❌ {message}')