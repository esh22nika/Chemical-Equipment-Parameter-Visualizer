from PyQt5.QtWidgets import QPushButton

class ModernButton(QPushButton):
    def __init__(self, text, variant="primary"):
        super().__init__(text)
        self.setFixedHeight(44)

        if variant == "primary":
            self.setStyleSheet("""
                QPushButton {
                    background-color: #2563eb;
                    color: white;
                    border-radius: 8px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #1d4ed8;
                }
            """)
