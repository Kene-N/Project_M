import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget
from database.database import init_db, SessionLocal
from database.models import User 
from ui.login_window import LoginWindow
from ui.capture_window import CaptureWindow


class MVP_App(QStackedWidget):
    def __init__(self):
        super().__init__()
<<<<<<< HEAD
        self.setWindowTitle("MVP Database v.1.0.0")
=======
        self.setWindowTitle("Melian Intelligence System")
>>>>>>> 77c5813b6edf98dffee25940548d900144937ba7
        self.setMinimumSize(1000, 700)
        
        # 1. User Session Data
        self.current_user_role = None
        self.current_username = None

<<<<<<< HEAD
        # 2. Initialize Screens 
=======
        # 2. Initialize Screens (MUST happen before the DB check)
>>>>>>> 77c5813b6edf98dffee25940548d900144937ba7
        self.login_screen = LoginWindow(self)
        self.capture_screen = CaptureWindow(self)
        
        # 3. Add to Stack
        self.addWidget(self.login_screen)
        self.addWidget(self.capture_screen)
        
        # 4. First-Run Admin Check
        db = SessionLocal()
        try:
            admin_exists = db.query(User).filter(User.role == 'admin').first()
            if not admin_exists:
                # If no admin, trigger the setup mode
                self.setCurrentWidget(self.login_screen)
                self.login_screen.setup_mode() 
            else:
                self.setCurrentWidget(self.login_screen)
        except Exception as e:
            print(f"Database Initialization Error: {e}")
            self.setCurrentWidget(self.login_screen)
        finally:
            db.close()

    def logout(self):
        self.current_user_role = None
        self.current_username = None
        self.login_screen.badge_input.clear()
        self.login_screen.password_input.clear()
        
        # Reset the login screen back to standard login (in case it was in setup mode)
        self.login_screen.is_setup = False
<<<<<<< HEAD
        self.login_screen.title.setText("MVP Database LOGIN")
=======
        self.login_screen.title.setText("MELIAN SYSTEM LOGIN")
>>>>>>> 77c5813b6edf98dffee25940548d900144937ba7
        self.login_screen.login_btn.setText("Login")
        
        self.setCurrentWidget(self.login_screen)    

if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    window = MVP_App()
    window.show()
    sys.exit(app.exec())