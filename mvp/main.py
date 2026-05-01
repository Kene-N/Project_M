import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget
from database.database import init_db
from ui.login_window import LoginWindow
from ui.capture_window import CaptureWindow

class MVP_App(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MVP Database System")
        self.setMinimumSize(1000, 700)
        
        # Initialize Login Screen
        self.login_screen = LoginWindow(self)
        self.addWidget(self.login_screen)
        
        # This is where we will add the Capture/Dashboard later
        # self.dashboard = MainDashboard(self)
        # self.addWidget(self.dashboard)

if __name__ == "__main__":
    # Ensure database is ready
    init_db()
    
    app = QApplication(sys.argv)
    window = MVP_App()
    window.show()
    sys.exit(app.exec())


   