from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QFrame, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from database.database import SessionLocal
from database.models import User
from auth.auth_handler import get_password_hash, verify_password

class LoginWindow(QWidget):
    def __init__(self, main_app=None):
        super().__init__(main_app)
        self.main_app = main_app
        self.is_setup = False  # Flag for first-run initialization
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.container = QFrame()
        self.container.setFixedWidth(400)
        self.container.setStyleSheet("QFrame { background-color: #1A1A40; border-radius: 10px; padding: 20px; }")
        
        container_layout = QVBoxLayout(self.container)

        self.title = QLabel("MVP Database LOGIN")
        self.title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.title.setStyleSheet("color: white;")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(self.title)

        self.badge_input = QLineEdit()
        self.badge_input.setPlaceholderText("Username")
        self.badge_input.setFixedHeight(35)
        self.badge_input.setStyleSheet("padding: 5px; border-radius: 3px;")
        container_layout.addWidget(self.badge_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedHeight(35)
        self.password_input.setStyleSheet("padding: 5px; border-radius: 3px;")
        self.password_input.returnPressed.connect(self.handle_login)
        container_layout.addWidget(self.password_input)

        self.login_btn = QPushButton("Login")
        self.login_btn.setFixedHeight(40)
        self.login_btn.setStyleSheet("""
            QPushButton { background-color: #00A8E8; color: white; font-weight: bold; border-radius: 5px; }
            QPushButton:hover { background-color: #007EA7; }
        """)
        self.login_btn.setDefault(True)
        self.login_btn.clicked.connect(self.handle_login)
        container_layout.addWidget(self.login_btn)


        layout.addWidget(self.container)
        self.setLayout(layout)


    def setup_mode(self):
        """Called by main.py if no admin exists in the database."""
        self.is_setup = True
        self.title.setText("SYSTEM INITIALIZATION")
        self.badge_input.setPlaceholderText("Create Master Admin Username")
        self.password_input.setPlaceholderText("Create Master Admin Password")
        self.login_btn.setText("Register Master Admin")
        self.login_btn.setStyleSheet("""
            QPushButton { background-color: #e67e22; color: white; font-weight: bold; border-radius: 5px; }
            QPushButton:hover { background-color: #d35400; }
        """)

    def handle_login(self):
        username = self.badge_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        if self.is_setup:
            self.perform_initial_setup(username, password)
        else:
            self.perform_standard_login(username, password)

    def perform_initial_setup(self, username, password):
        db = SessionLocal()
        try:
            hashed = get_password_hash(password)
            new_admin = User(username=username, password_hash=hashed, role='admin')
            db.add(new_admin)
            db.commit()
            
            QMessageBox.information(self, "Success", "Master Admin created successfully. System initialized.")
            
            # Revert UI to standard login
            self.is_setup = False
            self.title.setText("MVP LOGIN")
            self.badge_input.setPlaceholderText("Username")
            self.password_input.setPlaceholderText("Password")
            self.login_btn.setText("Login")
            self.login_btn.setStyleSheet("""
                QPushButton { background-color: #00A8E8; color: white; font-weight: bold; border-radius: 5px; }
                QPushButton:hover { background-color: #007EA7; }
            """)
            self.badge_input.clear()
            self.password_input.clear()
        except Exception as e:
            QMessageBox.critical(self, "Setup Error", f"Failed to initialize: {str(e)}")
        finally:
            db.close()

    def perform_standard_login(self, username, password):
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.username == username).first()
            if user and verify_password(password, user.password_hash):
                self.main_app.current_user_role = user.role
                self.main_app.current_username = user.username
                
                # Refresh Admin Panel visibility
                self.main_app.capture_screen.update_admin_visibility()
                
                # Switch to Capture screen
                self.main_app.setCurrentWidget(self.main_app.capture_screen)
                self.badge_input.clear()
                self.password_input.clear()
            else:
                QMessageBox.warning(self, "Access Denied", "Invalid credentials.")
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Connection failed: {str(e)}")
        finally:
            db.close()