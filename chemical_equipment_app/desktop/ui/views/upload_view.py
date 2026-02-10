"""
Upload View
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFileDialog, QFrame, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from config.settings import COLORS, SPACING
from ui.styles import get_button_style
from services.api_service import api_service


class UploadView(QWidget):
    """Upload CSV view"""
    
    upload_success = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.selected_file = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(SPACING['xl'])
        
        # Header
        header_layout = QVBoxLayout()
        header_layout.setSpacing(SPACING['xs'])
        
        title = QLabel('Upload Equipment Data')
        title.setFont(QFont('Arial', 24, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['text_primary']};")
        header_layout.addWidget(title)
        
        subtitle = QLabel('Import CSV files containing chemical equipment parameters')
        subtitle.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 14px;")
        header_layout.addWidget(subtitle)
        
        layout.addLayout(header_layout)
        
        # Upload card
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border_light']};
                border-radius: 12px;
                padding: 30px;
            }}
        """)
        card.setMaximumWidth(800)
        
        card_layout = QVBoxLayout()
        card_layout.setSpacing(SPACING['lg'])
        
        # Instructions
        instructions = QLabel(
            '📋 Upload a CSV file with columns:\n'
            'Equipment Name, Type, Flowrate, Pressure, Temperature'
        )
        instructions.setStyleSheet(f"""
            padding: 20px;
            background-color: {COLORS['surface_secondary']};
            border-radius: 8px;
            color: {COLORS['text_secondary']};
            font-size: 13px;
        """)
        instructions.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(instructions)
        
        # File selection
        file_layout = QHBoxLayout()
        file_layout.setSpacing(SPACING['md'])
        
        self.file_label = QLabel('No file selected')
        self.file_label.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            font-size: 14px;
            padding: 12px;
            background-color: {COLORS['surface_secondary']};
            border-radius: 6px;
        """)
        file_layout.addWidget(self.file_label, 1)
        
        browse_btn = QPushButton('Browse')
        browse_btn.setStyleSheet(get_button_style('secondary'))
        browse_btn.setFixedWidth(120)
        browse_btn.clicked.connect(self.browse_file)
        browse_btn.setCursor(Qt.PointingHandCursor)
        file_layout.addWidget(browse_btn)
        
        card_layout.addLayout(file_layout)
        
        # Upload button
        self.upload_btn = QPushButton('📤 Upload and Analyze')
        self.upload_btn.setStyleSheet(get_button_style('success'))
        self.upload_btn.setEnabled(False)
        self.upload_btn.setMinimumHeight(50)
        self.upload_btn.clicked.connect(self.upload_file)
        self.upload_btn.setCursor(Qt.PointingHandCursor)
        card_layout.addWidget(self.upload_btn)
        
        # Status message
        self.status_label = QLabel('')
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet("font-size: 13px; padding: 10px;")
        card_layout.addWidget(self.status_label)
        
        card.setLayout(card_layout)
        layout.addWidget(card, alignment=Qt.AlignTop)
        
        # Requirements info
        info_card = QFrame()
        info_card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['primary_light']};
                border-left: 4px solid {COLORS['primary']};
                border-radius: 8px;
                padding: 20px;
            }}
        """)
        info_card.setMaximumWidth(800)
        
        info_layout = QVBoxLayout()
        
        info_title = QLabel('ℹ️ File Requirements')
        info_title.setFont(QFont('Arial', 13, QFont.Bold))
        info_title.setStyleSheet(f"color: {COLORS['primary']};")
        info_layout.addWidget(info_title)
        
        requirements = QLabel(
            '• CSV format only\n'
            '• Required columns: Equipment Name, Type, Flowrate, Pressure, Temperature\n'
            '• Numeric values for Flowrate, Pressure, and Temperature\n'
            '• Maximum file size: 10MB'
        )
        requirements.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 13px; line-height: 1.6;")
        info_layout.addWidget(requirements)
        
        info_card.setLayout(info_layout)
        layout.addWidget(info_card, alignment=Qt.AlignTop)
        
        layout.addStretch()
        
        self.setLayout(layout)
    
    def browse_file(self):
        """Browse for CSV file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            'Select CSV File',
            '',
            'CSV Files (*.csv);;All Files (*.*)'
        )
        
        if file_path:
            self.selected_file = file_path
            import os
            filename = os.path.basename(file_path)
            self.file_label.setText(f'📄 {filename}')
            self.upload_btn.setEnabled(True)
            self.status_label.setText('')
    
    def upload_file(self):
        """Upload CSV file"""
        if not self.selected_file:
            return
        
        try:
            self.upload_btn.setEnabled(False)
            self.upload_btn.setText('⏳ Processing...')
            self.status_label.setText('')
            
            # Upload file
            data = api_service.upload_csv(self.selected_file)
            
            # Success
            self.status_label.setStyleSheet(f"color: {COLORS['success']}; font-size: 14px;")
            self.status_label.setText('✅ File uploaded successfully!')
            
            # Emit signal
            self.upload_success.emit(data)
            
            # Reset
            self.selected_file = None
            self.file_label.setText('No file selected')
            self.upload_btn.setText('📤 Upload and Analyze')
            
        except Exception as e:
            error_msg = str(e)
            self.status_label.setStyleSheet(f"color: {COLORS['danger']}; font-size: 14px;")
            
            if 'Missing required columns' in error_msg:
                self.status_label.setText('❌ Invalid file format. Check required columns.')
            elif 'File must be CSV' in error_msg:
                self.status_label.setText('❌ Please upload a CSV file.')
            else:
                self.status_label.setText(f'❌ Upload failed: {error_msg}')
            
            self.upload_btn.setEnabled(True)
            self.upload_btn.setText('📤 Upload and Analyze')