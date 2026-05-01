from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, 
                             QGroupBox, QScrollArea, QMessageBox, QComboBox)
from PyQt6.QtCore import Qt
from database.database import SessionLocal
from database.models import Person

class CaptureWindow(QWidget):
    def __init__(self, main_app=None):
        super().__init__(main_app)
        self.main_app = main_app
        self.init_ui()

    def open_search(self):
        from ui.search_window import SearchWindow
        self.search_screen = SearchWindow(self.main_app)
        self.main_app.addWidget(self.search_screen)
        self.main_app.setCurrentWidget(self.search_screen)       

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        # Navigation Bar
        nav_layout = QHBoxLayout()
        self.btn_goto_search = QPushButton("View/Search Database")
        self.btn_goto_search.clicked.connect(self.open_search)
        nav_layout.addWidget(self.btn_goto_search)
        main_layout.addLayout(nav_layout)
        
        # Scroll Area for long forms
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        form_layout = QVBoxLayout(content)
        
        # 1. Identification Section
        id_group = QGroupBox("Primary Identification (KYC)")
        id_form = QFormLayout()
        self.nin_input = QLineEdit()
        self.nin_input.setPlaceholderText("11-digit NIN")
        self.bvn_input = QLineEdit()
        self.bvn_input.setPlaceholderText("11-digit BVN")
        id_form.addRow("National ID (NIN):", self.nin_input)
        id_form.addRow("Bank Ver. Number (BVN):", self.bvn_input)
        id_group.setLayout(id_form)
        form_layout.addWidget(id_group)

        # 2. Personal Details Section
        bio_group = QGroupBox("Biographic Details")
        bio_form = QFormLayout()
        self.first_name = QLineEdit()
        self.last_name = QLineEdit()
        self.middle_name = QLineEdit()
        self.gender = QComboBox()
        self.gender.addItems(["Male", "Female", "Other"])
        
        bio_form.addRow("First Name:", self.first_name)
        bio_form.addRow("Last Name:", self.last_name)
        bio_form.addRow("Middle Name(s):", self.middle_name)
        bio_form.addRow("Gender:", self.gender)
        bio_group.setLayout(bio_form)
        form_layout.addWidget(bio_group)

        # 3. Origin Details
        origin_group = QGroupBox("State of Origin")
        origin_form = QFormLayout()
        self.state_input = QLineEdit() # Later we can make this a dropdown
        self.lga_input = QLineEdit()
        origin_form.addRow("State:", self.state_input)
        origin_form.addRow("LGA:", self.lga_input)
        origin_group.setLayout(origin_form)
        form_layout.addWidget(origin_group)

        # Save Button
        self.save_btn = QPushButton("Save to Local Database")
        self.save_btn.setFixedHeight(50)
        self.save_btn.setStyleSheet("background-color: #28a745; color: white; font-weight: bold;")
        self.save_btn.clicked.connect(self.save_person)
        form_layout.addWidget(self.save_btn)

        scroll.setWidget(content)
        main_layout.addWidget(scroll)

    def save_person(self):
        # Basic validation
        if not self.first_name.text() or not self.last_name.text():
            QMessageBox.warning(self, "Input Error", "First and Last name are required.")
            return

        db = SessionLocal()
        try:
            new_person = Person(
                national_id_number=self.nin_input.text(),
                bvn=self.bvn_input.text(),
                first_name=self.first_name.text(),
                last_name=self.last_name.text(),
                middle_names=self.middle_name.text(),
                gender=self.gender.currentText(),
                state_of_origin=self.state_input.text(),
                lga=self.lga_input.text()
            )
            db.add(new_person)
            db.commit()
            QMessageBox.information(self, "Success", "Suspect data committed to mvp.db")
            self.clear_form()
        except Exception as e:
            db.rollback()
            QMessageBox.critical(self, "Database Error", f"Could not save: {str(e)}")
        finally:
            db.close()

    def clear_form(self):
        self.nin_input.clear()
        self.bvn_input.clear()
        self.first_name.clear()
        self.last_name.clear()
        self.middle_name.clear()
        self.state_input.clear()
        self.lga_input.clear()


     