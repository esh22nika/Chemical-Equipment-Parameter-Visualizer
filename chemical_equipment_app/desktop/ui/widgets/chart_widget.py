"""
Chart Widget - Matplotlib integration
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from config.settings import COLORS, SPACING


class ChartWidget(QFrame):
    """Chart widget with matplotlib"""
    
    def __init__(self, title='Chart', description=''):
        super().__init__()
        self.title_text = title
        self.description_text = description
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border_light']};
                border-radius: 12px;
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = QWidget()
        header.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {COLORS['surface']}, stop:1 {COLORS['surface_secondary']});
            border-bottom: 1px solid {COLORS['border_light']};
        """)
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(SPACING['lg'], SPACING['md'], SPACING['lg'], SPACING['md'])
        header_layout.setSpacing(2)
        
        title = QLabel(self.title_text)
        title.setFont(QFont('Arial', 13, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['text_primary']};")
        header_layout.addWidget(title)
        
        if self.description_text:
            desc = QLabel(self.description_text)
            desc.setStyleSheet(f"color: {COLORS['text_tertiary']}; font-size: 11px;")
            header_layout.addWidget(desc)
        
        header.setLayout(header_layout)
        layout.addWidget(header)
        
        # Chart canvas
        self.figure = Figure(figsize=(6.5, 3.0), dpi=100)
        self.figure.patch.set_facecolor('white')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background-color: white;")
        
        layout.addWidget(self.canvas)
        
        self.setLayout(layout)
    
    def clear_chart(self):
        """Clear the chart"""
        self.figure.clear()
        self.canvas.draw()
    
    def create_pie_chart(self, labels, values, colors):
        """Create pie chart"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Create pie chart
        wedges, texts, autotexts = ax.pie(
            values,
            labels=labels,
            autopct='%1.1f%%',
            colors=colors,
            startangle=90,
            textprops={'fontsize': 10}
        )
        
        # Make percentage text bold
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(9)
        
        # Equal aspect ratio
        ax.axis('equal')
        
        self.figure.tight_layout(pad=2)
        self.canvas.draw()
    
    def create_bar_chart(self, labels, values, colors):
        """Create bar chart"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Create bars
        bars = ax.bar(labels, values, color=colors, width=0.6)
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.,
                height,
                f'{height:.1f}',
                ha='center',
                va='bottom',
                fontweight='bold',
                fontsize=10
            )
        
        # Styling
        ax.set_ylabel('Value', fontsize=10, fontweight='bold')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        
        self.figure.tight_layout(pad=2)
        self.canvas.draw()
    
    def create_line_chart(self, labels, datasets):
        """Create line chart with multiple datasets
        
        Args:
            labels: X-axis labels
            datasets: List of tuples (name, values, color)
        """
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Plot each dataset
        for name, values, color in datasets:
            ax.plot(
                labels,
                values,
                marker='o',
                linewidth=2,
                markersize=5,
                label=name,
                color=color,
                alpha=0.8
            )
            
            # Fill area under curve
            ax.fill_between(
                range(len(labels)),
                values,
                alpha=0.1,
                color=color
            )
        
        # Styling
        ax.set_xlabel('Equipment', fontsize=10, fontweight='bold')
        ax.set_ylabel('Value', fontsize=10, fontweight='bold')
        ax.legend(loc='upper right', framealpha=0.9, fontsize=9)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        
        # Rotate x labels
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Remove top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        self.figure.tight_layout(pad=2)
        self.canvas.draw()
