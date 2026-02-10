"""
ChemFlow Analytics - Desktop Application
Main Entry Point
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from config.settings import APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT
from ui.styles import apply_global_styles
from ui.login_window import LoginWindow
from ui.main_window import MainWindow


def main():
    """Application entry point"""
    app = QApplication(sys.argv)
    
    # Set application metadata
    app.setApplicationName(APP_NAME)
    app.setStyle('Fusion')
    
    # Set default font
    font = QFont('Segoe UI', 9)
    app.setFont(font)
    
    # Apply global styles
    apply_global_styles(app)
    
    # Store main window reference
    main_window_ref = {'window': None}
    
    # Show login window
    login_window = LoginWindow()
    
    def on_login_success(token, user):
        """Handle successful login"""
        main_window_ref['window'] = MainWindow(token, user)
        main_window_ref['window'].show()
    
    login_window.login_success.connect(on_login_success)
    login_window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()