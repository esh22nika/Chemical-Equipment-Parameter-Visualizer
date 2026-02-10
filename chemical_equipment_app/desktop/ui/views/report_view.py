"""
Report View - Preview and download PDF reports
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QPushButton, QScrollArea, QFileDialog,
    QMessageBox, QTextEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from config.settings import COLORS, SPACING
from ui.styles import get_button_style, get_card_style
from services.api_service import api_service


class ReportView(QWidget):
    """Report preview and download view"""
    
    def __init__(self):
        super().__init__()
        self.dataset = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(40, 40, 40, 40)
        content_layout.setSpacing(SPACING['xl'])
        
        # Header
        header_layout = QHBoxLayout()
        
        title_layout = QVBoxLayout()
        title_layout.setSpacing(SPACING['xs'])
        
        self.title_label = QLabel('Report Preview')
        self.title_label.setFont(QFont('Arial', 24, QFont.Bold))
        self.title_label.setStyleSheet(f"color: {COLORS['text_primary']};")
        title_layout.addWidget(self.title_label)
        
        self.subtitle_label = QLabel('No dataset loaded')
        self.subtitle_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 14px;")
        title_layout.addWidget(self.subtitle_label)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        # Download button
        self.download_btn = QPushButton('📄 Download PDF Report')
        self.download_btn.setStyleSheet(get_button_style('success'))
        self.download_btn.setEnabled(False)
        self.download_btn.setMinimumHeight(45)
        self.download_btn.clicked.connect(self.download_pdf)
        self.download_btn.setCursor(Qt.PointingHandCursor)
        header_layout.addWidget(self.download_btn)
        
        content_layout.addLayout(header_layout)
        
        # Report preview container
        self.preview_container = QWidget()
        self.preview_layout = QVBoxLayout()
        self.preview_layout.setSpacing(SPACING['lg'])
        self.preview_container.setLayout(self.preview_layout)
        self.preview_container.hide()
        
        content_layout.addWidget(self.preview_container)
        
        # Empty state
        self.empty_state = self.create_empty_state()
        content_layout.addWidget(self.empty_state)
        
        content_layout.addStretch()
        
        content_widget.setLayout(content_layout)
        scroll.setWidget(content_widget)
        
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
    
    def create_empty_state(self):
        """Create empty state"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(SPACING['lg'])
        
        icon = QLabel('📄')
        icon.setFont(QFont('Arial', 64))
        icon.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon)
        
        title = QLabel('No Report Available')
        title.setFont(QFont('Arial', 20, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['text_primary']};")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        desc = QLabel('Upload a dataset to generate and view reports')
        desc.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 14px;")
        desc.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc)
        
        widget.setLayout(layout)
        return widget
    
    def load_dataset(self, dataset):
        """Load dataset and generate preview"""
        self.dataset = dataset
        
        if not dataset:
            self.show_empty_state()
            return
        
        # Update header
        self.subtitle_label.setText(f"Report for {dataset['filename']}")
        self.download_btn.setEnabled(True)
        
        # Hide empty state, show preview
        self.empty_state.hide()
        self.preview_container.show()
        
        # Clear previous preview
        for i in reversed(range(self.preview_layout.count())):
            widget = self.preview_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # Build preview
        self.build_preview()
    
    def build_preview(self):
        """Build report preview"""
        if not self.dataset:
            return
        
        # Dataset Information Section
        info_section = self.create_section(
            'Dataset Information',
            self.get_dataset_info_html()
        )
        self.preview_layout.addWidget(info_section)
        
        # Summary Statistics Section
        summary_section = self.create_section(
            'Summary Statistics',
            self.get_summary_stats_html()
        )
        self.preview_layout.addWidget(summary_section)
        
        # Equipment Type Distribution Section
        dist_section = self.create_section(
            'Equipment Type Distribution',
            self.get_distribution_html()
        )
        self.preview_layout.addWidget(dist_section)
        
        # Data Preview Section (first 10 items)
        data_section = self.create_section(
            'Equipment Data Preview',
            self.get_data_preview_html()
        )
        self.preview_layout.addWidget(data_section)
    
    def create_section(self, title, content_html):
        """Create a report section"""
        section = QFrame()
        section.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border_light']};
                border-radius: 12px;
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(SPACING['lg'], SPACING['lg'], SPACING['lg'], SPACING['lg'])
        layout.setSpacing(SPACING['md'])
        
        # Section title
        title_label = QLabel(title)
        title_label.setFont(QFont('Arial', 16, QFont.Bold))
        title_label.setStyleSheet(f"color: {COLORS['text_primary']};")
        layout.addWidget(title_label)
        
        # Section content
        content = QLabel(content_html)
        content.setTextFormat(Qt.RichText)
        content.setWordWrap(True)
        content.setStyleSheet("font-size: 13px;")
        layout.addWidget(content)
        
        section.setLayout(layout)
        return section
    
    def get_dataset_info_html(self):
        """Get dataset information HTML"""
        return f"""
        <table style="width: 100%; border-collapse: collapse;">
            <tr>
                <td style="padding: 8px; font-weight: 600; color: {COLORS['text_secondary']};">Filename:</td>
                <td style="padding: 8px;">{self.dataset['filename']}</td>
            </tr>
            <tr>
                <td style="padding: 8px; font-weight: 600; color: {COLORS['text_secondary']};">Upload Date:</td>
                <td style="padding: 8px;">{self.dataset['upload_date']}</td>
            </tr>
            <tr>
                <td style="padding: 8px; font-weight: 600; color: {COLORS['text_secondary']};">Total Equipment:</td>
                <td style="padding: 8px;">{self.dataset['total_count']}</td>
            </tr>
        </table>
        """
    
    def get_summary_stats_html(self):
        """Get summary statistics HTML"""
        return f"""
        <table style="width: 100%; border-collapse: collapse; border: 1px solid {COLORS['border_light']};">
            <tr style="background-color: {COLORS['surface_secondary']}; font-weight: 600;">
                <td style="padding: 10px; border: 1px solid {COLORS['border_light']};">Metric</td>
                <td style="padding: 10px; border: 1px solid {COLORS['border_light']};">Value</td>
            </tr>
            <tr>
                <td style="padding: 10px; border: 1px solid {COLORS['border_light']};">Average Flowrate</td>
                <td style="padding: 10px; border: 1px solid {COLORS['border_light']};">{self.dataset['avg_flowrate']:.2f} L/min</td>
            </tr>
            <tr>
                <td style="padding: 10px; border: 1px solid {COLORS['border_light']};">Average Pressure</td>
                <td style="padding: 10px; border: 1px solid {COLORS['border_light']};">{self.dataset['avg_pressure']:.2f} bar</td>
            </tr>
            <tr>
                <td style="padding: 10px; border: 1px solid {COLORS['border_light']};">Average Temperature</td>
                <td style="padding: 10px; border: 1px solid {COLORS['border_light']};">{self.dataset['avg_temperature']:.2f} °C</td>
            </tr>
        </table>
        """
    
    def get_distribution_html(self):
        """Get equipment type distribution HTML"""
        rows = ""
        for eq_type, count in self.dataset.get('equipment_type_distribution', {}).items():
            rows += f"""
            <tr>
                <td style="padding: 10px; border: 1px solid {COLORS['border_light']};">{eq_type}</td>
                <td style="padding: 10px; border: 1px solid {COLORS['border_light']};">{count}</td>
            </tr>
            """
        
        return f"""
        <table style="width: 100%; border-collapse: collapse; border: 1px solid {COLORS['border_light']};">
            <tr style="background-color: {COLORS['surface_secondary']}; font-weight: 600;">
                <td style="padding: 10px; border: 1px solid {COLORS['border_light']};">Equipment Type</td>
                <td style="padding: 10px; border: 1px solid {COLORS['border_light']};">Count</td>
            </tr>
            {rows}
        </table>
        """
    
    def get_data_preview_html(self):
        """Get data preview HTML (first 10 items)"""
        data = self.dataset.get('data', [])[:10]
        
        rows = ""
        for item in data:
            rows += f"""
            <tr>
                <td style="padding: 8px; border: 1px solid {COLORS['border_light']};">{item['Equipment Name']}</td>
                <td style="padding: 8px; border: 1px solid {COLORS['border_light']};">{item['Type']}</td>
                <td style="padding: 8px; border: 1px solid {COLORS['border_light']};">{item['Flowrate']:.2f}</td>
                <td style="padding: 8px; border: 1px solid {COLORS['border_light']};">{item['Pressure']:.2f}</td>
                <td style="padding: 8px; border: 1px solid {COLORS['border_light']};">{item['Temperature']:.2f}</td>
            </tr>
            """
        
        return f"""
        <table style="width: 100%; border-collapse: collapse; border: 1px solid {COLORS['border_light']}; font-size: 12px;">
            <tr style="background-color: {COLORS['surface_secondary']}; font-weight: 600;">
                <td style="padding: 8px; border: 1px solid {COLORS['border_light']};">Name</td>
                <td style="padding: 8px; border: 1px solid {COLORS['border_light']};">Type</td>
                <td style="padding: 8px; border: 1px solid {COLORS['border_light']};">Flowrate</td>
                <td style="padding: 8px; border: 1px solid {COLORS['border_light']};">Pressure</td>
                <td style="padding: 8px; border: 1px solid {COLORS['border_light']};">Temp</td>
            </tr>
            {rows}
        </table>
        <p style="margin-top: 10px; color: {COLORS['text_tertiary']}; font-size: 12px;">
            Showing first 10 of {len(self.dataset.get('data', []))} records
        </p>
        """
    
    def download_pdf(self):
        """Download PDF report"""
        if not self.dataset:
            return
        
        try:
            # Ask where to save
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                'Save PDF Report',
                f"report_{self.dataset['filename']}_{self.dataset['id']}.pdf",
                'PDF Files (*.pdf)'
            )
            
            if file_path:
                # Show progress
                self.download_btn.setEnabled(False)
                self.download_btn.setText('⏳ Downloading...')
                
                # Download PDF
                pdf_content = api_service.download_pdf(self.dataset['id'])
                
                # Save to file
                with open(file_path, 'wb') as f:
                    f.write(pdf_content)
                
                # Reset button
                self.download_btn.setEnabled(True)
                self.download_btn.setText('📄 Download PDF Report')
                
                # Show success
                QMessageBox.information(
                    self,
                    'Success',
                    'PDF report downloaded successfully!'
                )
                
        except Exception as e:
            self.download_btn.setEnabled(True)
            self.download_btn.setText('📄 Download PDF Report')
            QMessageBox.warning(
                self,
                'Error',
                f'Failed to download PDF: {str(e)}'
            )
    
    def show_empty_state(self):
        """Show empty state"""
        self.preview_container.hide()
        self.empty_state.show()
        self.subtitle_label.setText('No dataset loaded')
        self.download_btn.setEnabled(False)