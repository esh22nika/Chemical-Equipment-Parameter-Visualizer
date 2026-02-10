''' 
from PyQt5.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
from widgets.modern_button import ModernButton
from services.pdf_service import generate_pdf

class DataTab(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)

        content = QWidget()
        layout = QVBoxLayout(content)

        self.table = QTableWidget(10, 5)
        self.table.setHorizontalHeaderLabels(
            ["Name", "Type", "Flowrate", "Pressure", "Temperature"]
        )

        layout.addWidget(self.table)

        pdf_btn = ModernButton("📄 Download PDF Report", "primary")
        pdf_btn.clicked.connect(generate_pdf)

        layout.addWidget(pdf_btn)
        layout.addStretch()

        self.setWidget(content)
'''