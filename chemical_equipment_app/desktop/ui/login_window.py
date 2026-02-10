"""
Login Window - Fixed Version
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
        self.setFixedSize(600, 700)
        self.setStyleSheet(f"background-color: {COLORS['surface_secondary']};")
        
        layout = QVBoxLayout()
        layout.setSpacing(30)
        layout.setContentsMargins(50, 50, 50, 50)
        
        # Logo and Title
        title_layout = QVBoxLayout()
        title_layout.setAlignment(Qt.AlignCenter)
        title_layout.setSpacing(12)
        
        title = QLabel('ChemFlow')
        title.setFont(QFont('Arial', 36, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['primary']}; margin-bottom: 5px;")
        title.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title)
        
        subtitle = QLabel('Equipment Analytics Platform')
        subtitle.setFont(QFont('Arial', 14))
        subtitle.setStyleSheet(f"color: {COLORS['text_secondary']}; margin-bottom: 20px;")
        subtitle.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(subtitle)
        
        layout.addLayout(title_layout)
        
        # Login Card
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface']};
                border: 2px solid {COLORS['border']};
                border-radius: 16px;
                padding: 30px;
            }}
        """)
        card_layout = QVBoxLayout()
        card_layout.setSpacing(20)
        
        # Card Title
        card_title = QLabel('Welcome Back')
        card_title.setFont(QFont('Arial', 22, QFont.Bold))
        card_title.setStyleSheet(f"color: {COLORS['text_primary']}; margin-bottom: 5px;")
        card_title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(card_title)
        
        card_subtitle = QLabel('Sign in to access your analytics')
        card_subtitle.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 14px; margin-bottom: 20px;")
        card_subtitle.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(card_subtitle)
        
        # Username
        username_label = QLabel('Username')
        username_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-weight: 600; font-size: 15px;")
        card_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter your username')
        self.username_input.setMinimumHeight(45)
        self.username_input.setStyleSheet(f"""
            QLineEdit {{
                padding: 12px 15px;
                border: 2px solid {COLORS['border']};
                border-radius: 8px;
                font-size: 15px;
                background-color: white;
                color: {COLORS['text_primary']};
            }}
            QLineEdit:focus {{
                border: 2px solid {COLORS['primary']};
                background-color: white;
            }}
            QLineEdit::placeholder {{
                color: {COLORS['text_tertiary']};
            }}
        """)
        card_layout.addWidget(self.username_input)
        
        # Password
        password_label = QLabel('Password')
        password_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-weight: 600; font-size: 15px; margin-top: 10px;")
        card_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Enter your password')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(45)
        self.password_input.setStyleSheet(f"""
            QLineEdit {{
                padding: 12px 15px;
                border: 2px solid {COLORS['border']};
                border-radius: 8px;
                font-size: 15px;
                background-color: white;
                color: {COLORS['text_primary']};
            }}
            QLineEdit:focus {{
                border: 2px solid {COLORS['primary']};
                background-color: white;
            }}
            QLineEdit::placeholder {{
                color: {COLORS['text_tertiary']};
            }}
        """)
        self.password_input.returnPressed.connect(self.handle_login)
        card_layout.addWidget(self.password_input)
        
        # Buttons
        self.login_btn = QPushButton('Sign In')
        self.login_btn.setMinimumHeight(50)
        self.login_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['primary']};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: 600;
                margin-top: 10px;
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
        """)
        self.login_btn.clicked.connect(self.handle_login)
        self.login_btn.setCursor(Qt.PointingHandCursor)
        card_layout.addWidget(self.login_btn)
        
        self.register_btn = QPushButton('Create Account')
        self.register_btn.setMinimumHeight(50)
        self.register_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['surface']};
                color: {COLORS['text_primary']};
                border: 2px solid {COLORS['border']};
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: 600;
                margin-top: 5px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['surface_secondary']};
                border-color: {COLORS['primary']};
            }}
            QPushButton:pressed {{
                background-color: {COLORS['surface_tertiary']};
            }}
        """)
        self.register_btn.clicked.connect(self.handle_register)
        self.register_btn.setCursor(Qt.PointingHandCursor)
        card_layout.addWidget(self.register_btn)
        
        # Status label
        self.status_label = QLabel('')
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet("font-size: 14px; padding: 15px; margin-top: 10px;")
        self.status_label.setMinimumHeight(50)
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
            self.status_label.setStyleSheet(f"color: {COLORS['primary']}; font-size: 14px; padding: 15px;")
            self.status_label.setText('Connecting to server...')
            
            # Force process events to update UI
            from PyQt5.QtWidgets import QApplication
            QApplication.processEvents()
            
            data = api_service.login(username, password)
            api_service.set_token(data['token'])
            
            self.login_success.emit(data['token'], data['user'])
            self.close()
            
        except Exception as e:
            error_msg = str(e)
            print(f"Login error: {error_msg}")  # Debug print
            
            if 'Invalid credentials' in error_msg or '401' in error_msg:
                self.show_error('Invalid username or password')
            elif 'Connection' in error_msg or 'Failed to establish' in error_msg:
                self.show_error('Cannot connect to server.\nMake sure the backend is running on http://localhost:8000')
            elif '404' in error_msg:
                self.show_error('Server endpoint not found.\nCheck backend configuration.')
            else:
                self.show_error(f'Connection error:\n{error_msg[:100]}')
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
        
        if len(password) < 4:
            self.show_error('Password must be at least 4 characters')
            return
        
        try:
            self.register_btn.setEnabled(False)
            self.register_btn.setText('Creating account...')
            self.status_label.setStyleSheet(f"color: {COLORS['primary']}; font-size: 14px; padding: 15px;")
            self.status_label.setText('Connecting to server...')
            
            # Force process events to update UI
            from PyQt5.QtWidgets import QApplication
            QApplication.processEvents()
            
            email = f'{username}@example.com'
            data = api_service.register(username, email, password)
            api_service.set_token(data['token'])
            
            self.login_success.emit(data['token'], data['user'])
            self.close()
            
        except Exception as e:
            error_msg = str(e)
            print(f"Registration error: {error_msg}")  # Debug print
            
            if 'username' in error_msg.lower() and 'exists' in error_msg.lower():
                self.show_error('Username already taken')
            elif 'Connection' in error_msg or 'Failed to establish' in error_msg:
                self.show_error('Cannot connect to server.\nMake sure the backend is running on http://localhost:8000')
            else:
                self.show_error(f'Registration failed:\n{error_msg[:100]}')
        finally:
            self.register_btn.setEnabled(True)
            self.register_btn.setText('Create Account')
    
    def show_error(self, message):
        """Show error message"""
        self.status_label.setStyleSheet(f"""
            color: white;
            background-color: {COLORS['danger']};
            font-size: 14px;
            padding: 15px;
            border-radius: 8px;
            font-weight: 600;
        """)
        self.status_label.setText(f'Error: {message}')