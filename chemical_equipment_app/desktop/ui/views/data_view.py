"""
Data Table View
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QFrame, QPushButton
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from config.settings import COLORS, SPACING
from ui.styles import get_button_style
from services.api_service import api_service


class DataView(QWidget):
    """Data table view"""
    
    def __init__(self):
        super().__init__()
        self.dataset = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(SPACING['lg'])
        
        # Header
        header_layout = QHBoxLayout()
        
        title_layout = QVBoxLayout()
        title_layout.setSpacing(SPACING['xs'])
        
        self.title_label = QLabel('Equipment Data')
        self.title_label.setFont(QFont('Arial', 24, QFont.Bold))
        self.title_label.setStyleSheet(f"color: {COLORS['text_primary']};")
        title_layout.addWidget(self.title_label)
        
        self.subtitle_label = QLabel('No data loaded')
        self.subtitle_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 14px;")
        title_layout.addWidget(self.subtitle_label)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        # Download PDF button
        self.pdf_btn = QPushButton('📄 Download PDF Report')
        self.pdf_btn.setStyleSheet(get_button_style('primary'))
        self.pdf_btn.setEnabled(False)
        self.pdf_btn.clicked.connect(self.download_pdf)
        self.pdf_btn.setCursor(Qt.PointingHandCursor)
        header_layout.addWidget(self.pdf_btn)
        
        layout.addLayout(header_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            '#', 'Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'
        ])
        
        # Table styling
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border_light']};
                border-radius: 8px;
                gridline-color: {COLORS['border_light']};
            }}
            QHeaderView::section {{
                background-color: {COLORS['primary']};
                color: white;
                padding: 12px;
                border: none;
                font-weight: 600;
                font-size: 13px;
            }}
            QTableWidget::item {{
                padding: 8px;
                border-bottom: 1px solid {COLORS['border_light']};
            }}
            QTableWidget::item:selected {{
                background-color: {COLORS['primary_light']};
                color: {COLORS['text_primary']};
            }}
        """)
        
        # Column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        
        layout.addWidget(self.table)
        
        # Empty state
        self.empty_label = QLabel('No data available. Please upload a CSV file.')
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            font-size: 16px;
            padding: 60px;
        """)
        layout.addWidget(self.empty_label)
        
        self.table.hide()
        
        self.setLayout(layout)
    
    def load_dataset(self, dataset):
        """Load dataset into table"""
        self.dataset = dataset
        
        if not dataset or 'data' not in dataset:
            self.show_empty_state()
            return
        
        # Update subtitle
        self.subtitle_label.setText(
            f"Showing {dataset['total_count']} records from {dataset['filename']}"
        )
        
        # Enable PDF button
        self.pdf_btn.setEnabled(True)
        
        # Hide empty state, show table
        self.empty_label.hide()
        self.table.show()
        
        # Populate table
        data = dataset['data']
        self.table.setRowCount(len(data))
        
        for row_idx, row_data in enumerate(data):
            # Index
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(row_idx + 1)))
            
            # Equipment Name
            self.table.setItem(row_idx, 1, QTableWidgetItem(row_data['Equipment Name']))
            
            # Type
            self.table.setItem(row_idx, 2, QTableWidgetItem(row_data['Type']))
            
            # Flowrate
            self.table.setItem(row_idx, 3, QTableWidgetItem(f"{row_data['Flowrate']:.2f}"))
            
            # Pressure
            self.table.setItem(row_idx, 4, QTableWidgetItem(f"{row_data['Pressure']:.2f}"))
            
            # Temperature
            self.table.setItem(row_idx, 5, QTableWidgetItem(f"{row_data['Temperature']:.2f}"))
            
            # Center align numeric columns
            for col in [0, 3, 4, 5]:
                item = self.table.item(row_idx, col)
                if item:
                    item.setTextAlignment(Qt.AlignCenter)
    
    def show_empty_state(self):
        """Show empty state"""
        self.table.hide()
        self.empty_label.show()
        self.subtitle_label.setText('No data loaded')
        self.pdf_btn.setEnabled(False)
    
    def download_pdf(self):
        """Download PDF report"""
        if not self.dataset:
            return
        
        try:
            from PyQt5.QtWidgets import QFileDialog
            
            # Ask where to save
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                'Save PDF Report',
                f"report_{self.dataset['filename']}_{self.dataset['id']}.pdf",
                'PDF Files (*.pdf)'
            )
            
            if file_path:
                # Download PDF
                pdf_content = api_service.download_pdf(self.dataset['id'])
                
                # Save to file
                with open(file_path, 'wb') as f:
                    f.write(pdf_content)
                
                # Show success message
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.information(
                    self,
                    'Success',
                    'PDF report downloaded successfully!'
                )
                
        except Exception as e:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                'Error',
                f'Failed to download PDF: {str(e)}'
            )