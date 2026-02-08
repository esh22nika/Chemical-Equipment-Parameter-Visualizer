"""
Chemical Equipment Parameter Visualizer - Desktop Application
PyQt5 Desktop App that connects to Django Backend
"""

import sys
import requests
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QFileDialog, QTableWidget,
    QTableWidgetItem, QTabWidget, QMessageBox, QStackedWidget,
    QGroupBox, QGridLayout, QHeaderView
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# API Configuration
API_BASE_URL = 'http://localhost:8000/api'


class LoginWindow(QWidget):
    """Login/Register Window"""
    login_success = pyqtSignal(str, dict)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Chemical Equipment Analyzer - Login')
        self.setGeometry(100, 100, 400, 300)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel('Chemical Equipment Analyzer')
        title.setFont(QFont('Arial', 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Username')
        layout.addWidget(QLabel('Username:'))
        layout.addWidget(self.username_input)
        
        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel('Password:'))
        layout.addWidget(self.password_input)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.login_btn = QPushButton('Login')
        self.login_btn.clicked.connect(self.handle_login)
        btn_layout.addWidget(self.login_btn)
        
        self.register_btn = QPushButton('Register')
        self.register_btn.clicked.connect(self.handle_register)
        btn_layout.addWidget(self.register_btn)
        
        layout.addLayout(btn_layout)
        
        # Status label
        self.status_label = QLabel('')
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
    
    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            self.status_label.setText('Please enter username and password')
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
                self.status_label.setText('Invalid credentials')
        except Exception as e:
            self.status_label.setText(f'Error: {str(e)}')
    
    def handle_register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            self.status_label.setText('Please enter username and password')
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
                self.status_label.setText('Registration failed')
        except Exception as e:
            self.status_label.setText(f'Error: {str(e)}')


class MplCanvas(FigureCanvas):
    """Matplotlib canvas for PyQt5"""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)


class MainWindow(QMainWindow):
    """Main Application Window"""
    
    def __init__(self, token, user):
        super().__init__()
        self.token = token
        self.user = user
        self.current_dataset = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Chemical Equipment Parameter Visualizer')
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Header
        header = QLabel(f'Chemical Equipment Analyzer - Welcome, {self.user["username"]}')
        header.setFont(QFont('Arial', 16, QFont.Bold))
        header.setStyleSheet('padding: 10px; background-color: #3b82f6; color: white;')
        main_layout.addWidget(header)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_upload_tab(), 'Upload CSV')
        self.tabs.addTab(self.create_dashboard_tab(), 'Dashboard')
        self.tabs.addTab(self.create_data_tab(), 'Data Table')
        self.tabs.addTab(self.create_history_tab(), 'History')
        
        main_layout.addWidget(self.tabs)
        
        central_widget.setLayout(main_layout)
    
    def create_upload_tab(self):
        """Create upload CSV tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Instructions
        instructions = QLabel(
            'Upload a CSV file with columns:\n'
            'Equipment Name, Type, Flowrate, Pressure, Temperature'
        )
        instructions.setStyleSheet('padding: 10px; background-color: #e0f2fe; border-radius: 5px;')
        layout.addWidget(instructions)
        
        # File selection
        file_layout = QHBoxLayout()
        self.file_path_label = QLabel('No file selected')
        file_layout.addWidget(self.file_path_label)
        
        browse_btn = QPushButton('Browse')
        browse_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(browse_btn)
        
        layout.addLayout(file_layout)
        
        # Upload button
        self.upload_btn = QPushButton('Upload and Analyze')
        self.upload_btn.clicked.connect(self.upload_file)
        self.upload_btn.setEnabled(False)
        self.upload_btn.setStyleSheet(
            'QPushButton { background-color: #3b82f6; color: white; padding: 10px; font-size: 14px; }'
            'QPushButton:disabled { background-color: #cbd5e1; }'
        )
        layout.addWidget(self.upload_btn)
        
        # Status
        self.upload_status = QLabel('')
        self.upload_status.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.upload_status)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_dashboard_tab(self):
        """Create dashboard with charts"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Summary cards
        summary_group = QGroupBox('Summary Statistics')
        summary_layout = QGridLayout()
        
        self.total_count_label = QLabel('Total: --')
        self.avg_flowrate_label = QLabel('Avg Flowrate: --')
        self.avg_pressure_label = QLabel('Avg Pressure: --')
        self.avg_temp_label = QLabel('Avg Temperature: --')
        
        for label in [self.total_count_label, self.avg_flowrate_label, 
                      self.avg_pressure_label, self.avg_temp_label]:
            label.setStyleSheet('font-size: 14px; padding: 10px; background-color: #f1f5f9; border-radius: 5px;')
        
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
    
    def create_data_tab(self):
        """Create data table tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(5)
        self.data_table.setHorizontalHeaderLabels([
            'Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'
        ])
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.data_table)
        
        # Download PDF button
        pdf_btn = QPushButton('Download PDF Report')
        pdf_btn.clicked.connect(self.download_pdf)
        pdf_btn.setStyleSheet('background-color: #10b981; color: white; padding: 10px;')
        layout.addWidget(pdf_btn)
        
        widget.setLayout(layout)
        return widget
    
    def create_history_tab(self):
        """Create history tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Refresh button
        refresh_btn = QPushButton('Refresh History')
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
                    self.upload_status.setText('✅ File uploaded successfully!')
                    self.update_dashboard()
                    self.update_data_table()
                    self.tabs.setCurrentIndex(1)  # Switch to dashboard
                else:
                    error_msg = response.json().get('error', 'Upload failed')
                    self.upload_status.setText(f'❌ Error: {error_msg}')
        
        except Exception as e:
            self.upload_status.setText(f'❌ Error: {str(e)}')
    
    def update_dashboard(self):
        """Update dashboard with current dataset"""
        if not self.current_dataset:
            return
        
        # Update summary labels
        self.total_count_label.setText(f'Total: {self.current_dataset["total_count"]}')
        self.avg_flowrate_label.setText(f'Avg Flowrate: {self.current_dataset["avg_flowrate"]:.2f}')
        self.avg_pressure_label.setText(f'Avg Pressure: {self.current_dataset["avg_pressure"]:.2f}')
        self.avg_temp_label.setText(f'Avg Temperature: {self.current_dataset["avg_temperature"]:.2f}')
        
        # Update pie chart - Equipment Type Distribution
        self.pie_canvas.axes.clear()
        types = list(self.current_dataset['equipment_type_distribution'].keys())
        counts = list(self.current_dataset['equipment_type_distribution'].values())
        self.pie_canvas.axes.pie(counts, labels=types, autopct='%1.1f%%')
        self.pie_canvas.axes.set_title('Equipment Type Distribution')
        self.pie_canvas.draw()
        
        # Update bar chart - Average Parameters
        self.bar_canvas.axes.clear()
        params = ['Flowrate', 'Pressure', 'Temperature']
        values = [
            self.current_dataset['avg_flowrate'],
            self.current_dataset['avg_pressure'],
            self.current_dataset['avg_temperature']
        ]
        self.bar_canvas.axes.bar(params, values, color=['#3b82f6', '#10b981', '#f59e0b'])
        self.bar_canvas.axes.set_title('Average Parameters')
        self.bar_canvas.axes.set_ylabel('Value')
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
    
    # Show login window
    login_window = LoginWindow()
    
    def on_login_success(token, user):
        main_window = MainWindow(token, user)
        main_window.show()
    
    login_window.login_success.connect(on_login_success)
    login_window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()