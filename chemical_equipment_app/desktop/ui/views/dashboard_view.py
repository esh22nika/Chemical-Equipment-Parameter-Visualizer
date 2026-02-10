"""
Dashboard View - Main analytics display
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QGridLayout, QScrollArea, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from config.settings import COLORS, CHART_COLORS, SPACING
from ui.widgets.chart_widget import ChartWidget
from ui.icons import get_icon
from services.api_service import api_service
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class DashboardView(QWidget):
    """Dashboard view with statistics and charts"""
    
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
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setStyleSheet("QScrollArea { background-color: transparent; }")
        
        # Content widget
        self.content_widget = QWidget()
        self.content_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(16, 16, 16, 16)
        self.content_layout.setSpacing(SPACING['md'])
        self.content_layout.setAlignment(Qt.AlignTop)
        
        # Header
        header_layout = QVBoxLayout()
        header_layout.setSpacing(SPACING['xs'])
        
        self.title_label = QLabel('Analytics Dashboard')
        self.title_label.setFont(QFont('Arial', 24, QFont.Bold))
        self.title_label.setStyleSheet(f"color: {COLORS['text_primary']};")
        header_layout.addWidget(self.title_label)
        
        self.subtitle_label = QLabel('No data loaded')
        self.subtitle_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 14px;")
        header_layout.addWidget(self.subtitle_label)
        
        self.content_layout.addLayout(header_layout)
        
        # Summary text (no cards)
        stats_container = QWidget()
        stats_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.cards_layout = QGridLayout()
        self.cards_layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout.setHorizontalSpacing(SPACING['xl'])
        self.cards_layout.setVerticalSpacing(SPACING['md'])
        self.cards_layout.setColumnStretch(0, 1)
        self.cards_layout.setColumnStretch(1, 1)

        def make_stat(title):
            box = QWidget()
            box.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            box.setMinimumHeight(56)
            layout = QVBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(6)
            label = QLabel(title)
            label.setStyleSheet(f"color: {COLORS['text_tertiary']}; font-size: 12px;")
            value = QLabel('--')
            value.setFont(QFont('Arial', 18, QFont.Bold))
            value.setStyleSheet(f"color: {COLORS['text_primary']};")
            layout.addWidget(label)
            layout.addWidget(value)
            box.setLayout(layout)
            return box, value

        total_block, self.total_value_label = make_stat('Total Equipment')
        flow_block, self.flowrate_value_label = make_stat('Avg Flowrate')
        pressure_block, self.pressure_value_label = make_stat('Avg Pressure')
        temp_block, self.temp_value_label = make_stat('Avg Temperature')

        self.cards_layout.addWidget(total_block, 0, 0)
        self.cards_layout.addWidget(flow_block, 0, 1)
        self.cards_layout.addWidget(pressure_block, 1, 0)
        self.cards_layout.addWidget(temp_block, 1, 1)

        stats_container.setLayout(self.cards_layout)
        self.content_layout.addWidget(stats_container)
        
        # Charts container
        self.charts_container = QWidget()
        self.charts_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.charts_layout = QVBoxLayout()
        self.charts_layout.setSpacing(SPACING['lg'])
        
        # Row 1: Line chart (wide) + Pie chart (narrow)
        row1 = QHBoxLayout()
        row1.setSpacing(SPACING['lg'])
        
        self.line_chart = ChartWidget('Parameter Trends', 'Multi-parameter analysis')
        self.line_chart.setMinimumHeight(200)
        row1.addWidget(self.line_chart, 2)
        
        self.pie_chart = ChartWidget('Equipment Distribution', 'By type')
        self.pie_chart.setMinimumHeight(200)
        row1.addWidget(self.pie_chart, 1)
        
        self.charts_layout.addLayout(row1)
        
        # Row 2: Bar chart + Statistics table
        row2 = QHBoxLayout()
        row2.setSpacing(SPACING['lg'])
        
        self.bar_chart = ChartWidget('Average Parameters', 'Comparative analysis')
        self.bar_chart.setMinimumHeight(190)
        row2.addWidget(self.bar_chart, 1)
        
        self.stats_table = self.create_stats_table()
        row2.addWidget(self.stats_table, 1)
        
        self.charts_layout.addLayout(row2)
        
        self.charts_container.setLayout(self.charts_layout)
        self.charts_container.hide()  # Hidden until data loaded
        
        self.content_layout.addWidget(self.charts_container)
        
        # Empty state
        self.empty_state = self.create_empty_state()
        self.content_layout.addWidget(self.empty_state)
        
        
        self.content_widget.setLayout(self.content_layout)
        self.scroll.setWidget(self.content_widget)
        
        main_layout.addWidget(self.scroll)
        self.setLayout(main_layout)
    
    def create_empty_state(self):
        """Create empty state widget"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(SPACING['lg'])
        
        # Icon
        icon_label = QLabel()
        icon_label.setPixmap(get_icon('chart', 64).pixmap(64, 64))
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)
        
        # Title
        title = QLabel('Welcome to ChemFlow Analytics')
        title.setFont(QFont('Arial', 20, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['text_primary']};")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Description
        desc = QLabel('Upload equipment data to start analyzing parameters')
        desc.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 14px;")
        desc.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc)
        
        widget.setLayout(layout)
        return widget
    
    def create_stats_table(self):
        """Create statistics table"""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border_light']};
                border-radius: 12px;
            }}
        """)
        frame.setMinimumHeight(320)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(SPACING['lg'], SPACING['lg'], SPACING['lg'], SPACING['lg'])
        layout.setSpacing(SPACING['md'])
        
        # Header
        header = QLabel('Statistical Overview')
        header.setFont(QFont('Arial', 14, QFont.Bold))
        header.setStyleSheet(f"color: {COLORS['text_primary']};")
        layout.addWidget(header)
        
        desc = QLabel('Detailed parameter analysis')
        desc.setStyleSheet(f"color: {COLORS['text_tertiary']}; font-size: 11px;")
        layout.addWidget(desc)
        
        # Table (will be populated with actual data)
        self.stats_content = QLabel('No statistics available')
        self.stats_content.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 13px;")
        self.stats_content.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.stats_content)
        
        layout.addStretch()
        
        frame.setLayout(layout)
        return frame
    
    def load_dataset(self, dataset):
        """Load dataset and update dashboard"""
        self.dataset = dataset
        
        if not dataset:
            self.show_empty_state()
            return

        # If only summary data is provided, fetch the full dataset for charts
        if 'data' not in self.dataset or self.dataset.get('data') is None:
            try:
                dataset_id = self.dataset.get('id')
                if dataset_id:
                    self.dataset = api_service.get_dataset(dataset_id)
            except Exception as e:
                print(f"Dashboard full dataset fetch failed: {e}")
        
        # Update subtitle
        self.subtitle_label.setText(f"{self.dataset['filename']} - {self.dataset['total_count']} items")
        
        # Update cards
        self.total_value_label.setText(str(self.dataset['total_count']))
        self.flowrate_value_label.setText(f"{self.dataset['avg_flowrate']:.1f} L/min")
        self.pressure_value_label.setText(f"{self.dataset['avg_pressure']:.1f} bar")
        self.temp_value_label.setText(f"{self.dataset['avg_temperature']:.1f} C")
        
        # Show charts, hide empty state
        self.empty_state.hide()
        self.charts_container.show()
        
        # Update charts
        self.update_charts()
        QTimer.singleShot(0, self._refresh_scroll)
    
    def update_charts(self):
        """Update all charts"""
        if not self.dataset:
            return
        
        # Pie chart
        types = list(self.dataset['equipment_type_distribution'].keys())
        counts = list(self.dataset['equipment_type_distribution'].values())
        self.pie_chart.create_pie_chart(types, counts, CHART_COLORS[:len(types)])
        
        # Bar chart
        params = ['Flowrate', 'Pressure', 'Temperature']
        values = [
            self.dataset['avg_flowrate'],
            self.dataset['avg_pressure'],
            self.dataset['avg_temperature']
        ]
        self.bar_chart.create_bar_chart(params, values, CHART_COLORS[:3])
        
        # Line chart (first 15 items)
        data = self.dataset.get('data', [])[:15]
        if data:
            labels = [item['Equipment Name'][:10] for item in data]
            flowrates = [item['Flowrate'] for item in data]
            pressures = [item['Pressure'] for item in data]
            temps = [item['Temperature'] for item in data]
            
            datasets = [
                ('Flowrate', flowrates, CHART_COLORS[0]),
                ('Pressure', pressures, CHART_COLORS[1]),
                ('Temperature', temps, CHART_COLORS[2])
            ]
            self.line_chart.create_line_chart(labels, datasets)
        
        # Update stats table
        self.update_stats_table()
    
    def update_stats_table(self):
        """Update statistics table"""
        if not self.dataset or 'data' not in self.dataset:
            return

        data = self.dataset['data']

        # Calculate statistics
        flowrates = [item['Flowrate'] for item in data]
        pressures = [item['Pressure'] for item in data]
        temps = [item['Temperature'] for item in data]

        def calc_stats(values):
            import statistics
            return {
                'min': min(values),
                'max': max(values),
                'mean': statistics.mean(values),
                'stdev': statistics.stdev(values) if len(values) > 1 else 0
            }

        flow_stats = calc_stats(flowrates)
        pres_stats = calc_stats(pressures)
        temp_stats = calc_stats(temps)

        # Create HTML table
        html = f"""
        <table style="width: 100%; border-collapse: collapse; font-size: 12px;">
            <tr style="background-color: {COLORS['surface_secondary']}; font-weight: 600;">
                <td style="padding: 8px;">Parameter</td>
                <td style="padding: 8px;">Min</td>
                <td style="padding: 8px;">Max</td>
                <td style="padding: 8px;">Mean</td>
                <td style="padding: 8px;">Std Dev</td>
            </tr>
            <tr>
                <td style="padding: 8px; font-weight: 600;">Flowrate</td>
                <td style="padding: 8px;">{flow_stats['min']:.2f}</td>
                <td style="padding: 8px;">{flow_stats['max']:.2f}</td>
                <td style="padding: 8px;">{flow_stats['mean']:.2f}</td>
                <td style="padding: 8px;">{flow_stats['stdev']:.2f}</td>
            </tr>
            <tr style="background-color: {COLORS['surface_secondary']};">
                <td style="padding: 8px; font-weight: 600;">Pressure</td>
                <td style="padding: 8px;">{pres_stats['min']:.2f}</td>
                <td style="padding: 8px;">{pres_stats['max']:.2f}</td>
                <td style="padding: 8px;">{pres_stats['mean']:.2f}</td>
                <td style="padding: 8px;">{pres_stats['stdev']:.2f}</td>
            </tr>
            <tr>
                <td style="padding: 8px; font-weight: 600;">Temperature</td>
                <td style="padding: 8px;">{temp_stats['min']:.2f}</td>
                <td style="padding: 8px;">{temp_stats['max']:.2f}</td>
                <td style="padding: 8px;">{temp_stats['mean']:.2f}</td>
                <td style="padding: 8px;">{temp_stats['stdev']:.2f}</td>
            </tr>
        </table>
        """

        self.stats_content.setText(html)
        self.stats_content.setTextFormat(Qt.RichText)
        self.stats_content.setAlignment(Qt.AlignLeft | Qt.AlignTop)

    def _refresh_scroll(self):
        """Refresh scroll sizing after content changes."""
        # Let layout compute desired height, then enforce it for scrolling
        self.content_layout.invalidate()
        self.content_layout.activate()
        base_h = self.content_layout.sizeHint().height()
        min_h = self.scroll.viewport().height() + 200
        target_h = max(base_h, min_h)
        self.content_widget.setMinimumHeight(target_h)
        self.content_widget.adjustSize()
        self.content_widget.updateGeometry()

    def show_empty_state(self):
        """Show empty state"""
        self.charts_container.hide()
        self.empty_state.show()
        self.subtitle_label.setText('No data loaded')
