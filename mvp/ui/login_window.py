from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QFrame, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class LoginWindow(QWidget):
    def __init__(self, main_app=None):
        super().__init__(main_app)
        self.main_app = main_app
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        container = QFrame()
        container.setFixedWidth(400)
        container.setStyleSheet("QFrame { background-color: #1A1A40; border-radius: 10px; padding: 20px; }")
        
        container_layout = QVBoxLayout(container)

        title = QLabel("MVP DATABASE LOGIN")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(title)

        self.badge_input = QLineEdit()
        self.badge_input.setPlaceholderText("User Credentials")
        self.badge_input.setFixedHeight(35)
        container_layout.addWidget(self.badge_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedHeight(35)
        container_layout.addWidget(self.password_input)

        login_btn = QPushButton("Login")
        login_btn.setFixedHeight(40)
        login_btn.setStyleSheet("QPushButton { background-color: #00A8E8; color: blue; font-weight: bold; }")
        login_btn.clicked.connect(self.handle_login)
        container_layout.addWidget(login_btn)

        layout.addWidget(container)
        self.setLayout(layout)

    def handle_login(self):
        badge = self.badge_input.text()
        password = self.password_input.text()

        if badge == "admin" and password == "123":
            # 1. Create the next screen
            from ui.capture_window import CaptureWindow
            self.capture_screen = CaptureWindow(self.main_app)
            
            # 2. Add it to the manager (MVP_App)
            self.main_app.addWidget(self.capture_screen)
            
            # 3. Tell the manager to show it
            self.main_app.setCurrentWidget(self.capture_screen)
        else:
            QMessageBox.warning(self, "Error", "Invalid Credentials")        


        