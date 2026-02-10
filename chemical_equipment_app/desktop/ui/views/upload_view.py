"""
Upload View - Fixed Version
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFileDialog, QMessageBox, QProgressBar
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from config.settings import COLORS, SPACING
from ui.styles import get_button_style
from ui.icons import get_icon
from services.api_service import api_service


class UploadWorker(QThread):
    """Worker thread for file upload"""
    
    progress = pyqtSignal(int)
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
    
    def run(self):
        """Upload file in background"""
        try:
            # Simulate progress
            self.progress.emit(20)
            
            # Upload file
            result = api_service.upload_dataset(self.file_path)
            
            self.progress.emit(100)
            self.finished.emit(result)
            
        except Exception as e:
            self.error.emit(str(e))


class UploadView(QWidget):
    """Upload data view"""
    
    upload_complete = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.upload_worker = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(SPACING['xl'])
        
        # Header
        header = QVBoxLayout()
        header.setSpacing(SPACING['sm'])
        
        title = QLabel('Upload Equipment Data')
        title.setFont(QFont('Arial', 24, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['text_primary']};")
        header.addWidget(title)
        
        subtitle = QLabel('Import CSV files containing chemical equipment parameters')
        subtitle.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 14px;")
        header.addWidget(subtitle)
        
        layout.addLayout(header)
        layout.addSpacing(20)
        
        # Upload area
        upload_area = QWidget()
        upload_area.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['background']};
                border: 2px dashed {COLORS['border']};
                border-radius: 16px;
                padding: 60px;
            }}
        """)
        
        upload_layout = QVBoxLayout()
        upload_layout.setAlignment(Qt.AlignCenter)
        upload_layout.setSpacing(SPACING['lg'])
        
        # Icon
        icon = QLabel()
        icon.setPixmap(get_icon('upload', 64).pixmap(64, 64))
        icon.setAlignment(Qt.AlignCenter)
        upload_layout.addWidget(icon)
        
        # Upload button
        self.upload_btn = QPushButton('Upload and Analyze')
        self.upload_btn.setStyleSheet(get_button_style('success'))
        self.upload_btn.setIcon(get_icon('upload'))
        self.upload_btn.setMinimumHeight(60)
        self.upload_btn.setFont(QFont('Arial', 14, QFont.Bold))
        self.upload_btn.clicked.connect(self.select_file)
        self.upload_btn.setCursor(Qt.PointingHandCursor)
        upload_layout.addWidget(self.upload_btn)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 2px solid {COLORS['border']};
                border-radius: 8px;
                text-align: center;
                height: 30px;
                background-color: white;
            }}
            QProgressBar::chunk {{
                background-color: {COLORS['success']};
                border-radius: 6px;
            }}
        """)
        self.progress_bar.setVisible(False)
        upload_layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel('')
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 14px;")
        upload_layout.addWidget(self.status_label)
        
        upload_area.setLayout(upload_layout)
        layout.addWidget(upload_area)
        
        # File requirements
        requirements = QWidget()
        requirements.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['info_light']};
                border-left: 4px solid {COLORS['info']};
                border-radius: 8px;
                padding: 20px;
            }}
        """)
        
        req_layout = QVBoxLayout()
        req_layout.setSpacing(SPACING['md'])
        
        req_title = QLabel('File Requirements')
        req_title.setFont(QFont('Arial', 14, QFont.Bold))
        req_title.setStyleSheet(f"color: {COLORS['info']};")
        req_layout.addWidget(req_title)
        
        requirements_text = [
            '- CSV format only',
            '- Required columns: equipment_id, equipment_type, timestamp',
            '- Recommended columns: flowrate, pressure, temperature, efficiency',
            '- Maximum file size: 50 MB',
            '- Date format: YYYY-MM-DD HH:MM:SS'
        ]
        
        for req in requirements_text:
            req_label = QLabel(req)
            req_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 13px;")
            req_layout.addWidget(req_label)
        
        requirements.setLayout(req_layout)
        layout.addWidget(requirements)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def select_file(self):
        """Open file dialog"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            'Select CSV File',
            '',
            'CSV Files (*.csv);;All Files (*)'
        )
        
        if file_path:
            self.upload_file(file_path)
    
    def upload_file(self, file_path):
        """Upload selected file"""
        try:
            # Reset UI
            self.progress_bar.setValue(0)
            self.progress_bar.setVisible(True)
            self.upload_btn.setEnabled(False)
            self.status_label.setText('Uploading file...')
            self.status_label.setStyleSheet(f"color: {COLORS['info']}; font-size: 14px;")
            
            # Create worker
            self.upload_worker = UploadWorker(file_path)
            self.upload_worker.progress.connect(self.update_progress)
            self.upload_worker.finished.connect(self.upload_success)
            self.upload_worker.error.connect(self.upload_error)
            
            # Start upload
            self.upload_worker.start()
            
        except Exception as e:
            self.upload_error(str(e))
    
    def update_progress(self, value):
        """Update progress bar"""
        self.progress_bar.setValue(value)
    
    def upload_success(self, result):
        """Handle successful upload"""
        self.progress_bar.setVisible(False)
        self.upload_btn.setEnabled(True)
        
        filename = result.get('filename', 'Unknown')
        total_count = result.get('total_count', 0)
        
        self.status_label.setText(f'Upload successful: {filename} ({total_count} records)')
        self.status_label.setStyleSheet(f"color: {COLORS['success']}; font-size: 14px; font-weight: 600;")
        
        # Show success dialog
        QMessageBox.information(
            self,
            'Upload Successful',
            f'File uploaded successfully!\n\n'
            f'Filename: {filename}\n'
            f'Total records: {total_count}\n\n'
            f'You can now view the data in the Dashboard.'
        )
        
        # Emit signal
        self.upload_complete.emit(result)
    
    def upload_error(self, error_msg):
        """Handle upload error"""
        self.progress_bar.setVisible(False)
        self.upload_btn.setEnabled(True)
        
        self.status_label.setText('Upload failed')
        self.status_label.setStyleSheet(f"color: {COLORS['danger']}; font-size: 14px; font-weight: 600;")
        
        # Show detailed error
        if 'Connection' in error_msg:
            QMessageBox.warning(
                self,
                'Connection Error',
                'Cannot connect to the server.\n\n'
                'Please make sure:\n'
                '1. Django backend is running (python manage.py runserver)\n'
                '2. Server is accessible at http://localhost:8000\n\n'
                f'Error: {error_msg}'
            )
        elif '400' in error_msg or 'Bad Request' in error_msg:
            QMessageBox.warning(
                self,
                'Invalid File',
                'The uploaded file is invalid.\n\n'
                'Please check:\n'
                '1. File is in CSV format\n'
                '2. Required columns are present\n'
                '3. Data format is correct\n\n'
                f'Error: {error_msg}'
            )
        elif '413' in error_msg:
            QMessageBox.warning(
                self,
                'File Too Large',
                'The file is too large.\n\n'
                'Maximum file size: 50 MB\n\n'
                f'Error: {error_msg}'
            )
        else:
            QMessageBox.warning(
                self,
                'Upload Error',
                f'Failed to upload file:\n\n{error_msg[:300]}'
            )
