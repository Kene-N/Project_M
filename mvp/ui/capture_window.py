import os
import shutil
from uuid import uuid4
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QFormLayout, QGroupBox, QScrollArea, 
                             QMessageBox, QComboBox, QTextEdit, QFileDialog, QFrame, 
                             QCheckBox, QDialog, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QSize
from database.database import SessionLocal
from database.models import (Person, Biometric, Case, PersonCase, 
                             PersonAlias, PersonContact, Organization, PersonAffiliation, User)
from auth.auth_handler import get_password_hash


class CaptureWindow(QWidget):
    def __init__(self, main_app=None):
        super().__init__(main_app)
        self.main_app = main_app
        self.selected_photos = [None] * 4
        self.labels = ["Front View", "Left Side", "Right Side", "Back View"]
        self.init_ui()

    def open_search(self):
        from ui.search_window import SearchWindow
        self.search_screen = SearchWindow(self.main_app)
        self.main_app.addWidget(self.search_screen)
        self.main_app.setCurrentWidget(self.search_screen)

    def init_ui(self):
        # Master Layout
        self.master_layout = QVBoxLayout(self)
        self.master_layout.setSpacing(10)
        
        
        # 1. NAVIGATION (Pinned)
        nav = QHBoxLayout()
        btn_search = QPushButton("🔍 Search Records")
        btn_search.setFixedHeight(35)
        btn_search.setStyleSheet("background-color: #34495e; color: white; font-weight: bold;")
        btn_search.clicked.connect(self.open_search)
        nav.addWidget(btn_search)

        nav.addStretch() # Pushes the logout button to the far right

        # ADD LOGOUT BUTTON
        btn_logout = QPushButton("Logout")
        btn_logout.setFixedWidth(80)
        btn_logout.setStyleSheet("background-color: #c0392b; color: white; border-radius: 4px;")
        btn_logout.clicked.connect(self.main_app.logout) # Calls the function we just made
        nav.addWidget(btn_logout)

        self.master_layout.addLayout(nav)

        # 2. PINNED MUGSHOT GALLERY
        gallery_group = QGroupBox("Mugshots")
        gallery_group.setFixedHeight(240)
        gallery_layout = QHBoxLayout()
        self.photo_slots = []
        
        for i, label_text in enumerate(self.labels):
            container = QFrame()
            container.setFixedWidth(160)
            container.setStyleSheet("background: #F4F6F9; border: 1px solid #ddd; border-radius: 4px;")
            vbox = QVBoxLayout(container)
            
            lbl = QLabel(label_text)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("font-weight: bold; font-size: 10px; color: #2c3e50;")
            
            img = QLabel("No Image")
            img.setFixedSize(140, 140)
            img.setStyleSheet("border: 2px dashed #ccc; background: white; color: #7f8c8d;")
            img.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            btn = QPushButton("Browse")
            btn.setStyleSheet("color: #2c3e50;")
            btn.clicked.connect(lambda chk, idx=i: self.browse_photo(idx))
            
            vbox.addWidget(lbl)
            vbox.addWidget(img)
            vbox.addWidget(btn)
            gallery_layout.addWidget(container)
            self.photo_slots.append(img)
            
        gallery_group.setLayout(gallery_layout)
        self.master_layout.addWidget(gallery_group)

        # 3. SCROLLABLE FORM AREA
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background-color: transparent;")
        content = QWidget()
        form = QVBoxLayout(content)

        # --- A. PRIMARY IDENTITY & RESIDENCE ---
        grp_bio = QGroupBox("1. Primary Identity & Current Residence")
        f_bio = QFormLayout()
        self.first_name = QLineEdit()
        self.last_name = QLineEdit()
        self.middle_names = QLineEdit()
        self.dob = QLineEdit()
        self.dob.setPlaceholderText("YYYY-MM-DD")
        self.gender = QComboBox()
        self.gender.addItems(["Male", "Female", "Other"])
        self.current_address = QLineEdit()
        self.current_address.setPlaceholderText("Current Full Residential Address")
        self.stay_duration = QLineEdit()
        
        f_bio.addRow("First Name *", self.first_name)
        f_bio.addRow("Last Name *", self.last_name)
        f_bio.addRow("Middle Name(s)", self.middle_names)
        f_bio.addRow("Date of Birth", self.dob)
        f_bio.addRow("Gender", self.gender)
        f_bio.addRow("Current Address *", self.current_address)
        f_bio.addRow("Stay Duration", self.stay_duration)
        grp_bio.setLayout(f_bio)
        form.addWidget(grp_bio)

        # --- B. RESIDENCY HISTORY (5 PREVIOUS) ---
        grp_history = QGroupBox("2. Residency History (Previous 5 Locations)")
        history_layout = QVBoxLayout()
        self.prev_addresses = []
        for i in range(5):
            row = QHBoxLayout()
            addr = QLineEdit()
            addr.setPlaceholderText(f"Previous Address {i+1}")
            dur = QLineEdit()
            dur.setFixedWidth(150)
            dur.setPlaceholderText("Duration")
            row.addWidget(addr)
            row.addWidget(dur)
            history_layout.addLayout(row)
            self.prev_addresses.append((addr, dur))
        grp_history.setLayout(history_layout)
        form.addWidget(grp_history)

        # --- C. HERITAGE & KYC ---
        grp_heritage = QGroupBox("3. Heritage & Verification")
        f_her = QFormLayout()
        self.nationality = QLineEdit("Nigerian")
        self.state = QLineEdit()
        self.lga = QLineEdit()
        self.f_name = QLineEdit()
        self.m_name = QLineEdit()
        self.m_maiden = QLineEdit()
        self.nin = QLineEdit()
        self.nin_verified = QCheckBox("NIN Verified")
        self.bvn = QLineEdit()
        
        f_her.addRow("Nationality", self.nationality)
        f_her.addRow("State of Origin", self.state)
        f_her.addRow("LGA", self.lga)
        f_her.addRow("Father's Name", self.f_name)
        f_her.addRow("Mother's Name", self.m_name)
        f_her.addRow("Mother's Maiden", self.m_maiden)
        f_her.addRow("National ID (NIN)", self.nin)
        f_her.addRow(self.nin_verified)
        f_her.addRow("Bank Ver. Number (BVN)", self.bvn)
        grp_heritage.setLayout(f_her)
        form.addWidget(grp_heritage)

        # --- D. PHYSICALS, CONTACTS & ALIASES ---
        grp_phys = QGroupBox("4. Physicals, Contacts & Aliases")
        f_phys = QFormLayout()
        self.height = QLineEdit()
        self.marks = QTextEdit()
        self.marks.setMaximumHeight(60)
        self.aliases = QLineEdit()
        self.aliases.setPlaceholderText("Comma separated street names")
        self.phone = QLineEdit()
        self.email = QLineEdit()
        
        f_phys.addRow("Height (cm)", self.height)
        f_phys.addRow("Distinguishing Marks", self.marks)
        f_phys.addRow("Aliases", self.aliases)
        f_phys.addRow("Phone Number", self.phone)
        f_phys.addRow("Email Address", self.email)
        grp_phys.setLayout(f_phys)
        form.addWidget(grp_phys)

        # --- E. ORGANIZATIONAL AFFILIATION ---
        grp_org = QGroupBox("5. Organizations/Affiliation")
        f_org = QFormLayout()
        self.org_name = QLineEdit()
        self.org_type = QComboBox()
        self.org_type.addItems(["School", "Cult", "NGO", "Political", "Business"])
        self.org_role = QLineEdit()
        self.org_active = QCheckBox("Currently Active")
        
        f_org.addRow("Organization Name", self.org_name)
        f_org.addRow("Type", self.org_type)
        f_org.addRow("Subject's Role", self.org_role)
        f_org.addRow(self.org_active)
        grp_org.setLayout(f_org)
        form.addWidget(grp_org)

        # --- F. ARREST & CASE DETAILS ---
        grp_case = QGroupBox("6. Case & Arrest Intelligence")
        f_case = QFormLayout()
        self.case_no = QLineEdit()
        self.offense = QLineEdit()
        self.arrest_date = QLineEdit()
        self.arrest_date.setPlaceholderText("YYYY-MM-DD")
        self.arrest_addr = QLineEdit()
        self.officer_id = QLineEdit()
        self.case_desc = QTextEdit()
        self.case_desc.setMaximumHeight(60)
        
        f_case.addRow("Case Number *", self.case_no)
        f_case.addRow("Offense Type", self.offense)
        f_case.addRow("Arrest Date", self.arrest_date)
        f_case.addRow("Arrest Location", self.arrest_addr)
        f_case.addRow("Arresting Officer ID", self.officer_id)
        f_case.addRow("Case Description", self.case_desc)
        grp_case.setLayout(f_case)
        form.addWidget(grp_case)

        scroll.setWidget(content)
        self.master_layout.addWidget(scroll, stretch=1)

        # 4. FOOTER CONTROLS
        self.btn_save = QPushButton("SAVE RECORD")
        self.btn_save.setFixedHeight(50)
        self.btn_save.setStyleSheet("""
            QPushButton { background-color: #28a745; color: white; font-weight: bold; border-radius: 5px; }
            QPushButton:hover { background-color: #218838; }
        """)
        self.btn_save.clicked.connect(self.save_person)
        self.master_layout.addWidget(self.btn_save)

        # --- ADMIN TOOLS PANEL ---
        self.admin_panel = QGroupBox("System Administration")
        self.admin_layout = QHBoxLayout()
        self.btn_create_user = QPushButton("➕ Create New User Account")
        self.btn_create_user.setFixedHeight(40)
        self.btn_create_user.setStyleSheet("background-color: #e67e22; color: white; font-weight: bold;")
        self.btn_create_user.clicked.connect(self.show_user_creation_dialog)
        self.admin_layout.addWidget(self.btn_create_user)
        self.admin_panel.setLayout(self.admin_layout)
        self.master_layout.addWidget(self.admin_panel)
        
        # Hide by default, revealed in showEvent
        self.admin_panel.setVisible(False)

    def update_admin_visibility(self):
        """Refreshes the Admin Panel visibility based on the current session role."""
        # Get role safely from main_app
        role = getattr(self.main_app, 'current_user_role', 'user')
        
        # Ensure the panel exists before trying to hide/show it
        if hasattr(self, 'admin_panel'):
            self.admin_panel.setVisible(role == "admin")

    def showEvent(self, event):
        """Triggered whenever the screen is shown."""
        super().showEvent(event)
        self.update_admin_visibility()

    def show_user_creation_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Personnel Management")
        dialog.setMinimumWidth(400)
        master_layout = QVBoxLayout(dialog)
        
        # --- TOP: List of Existing Users ---
        master_layout.addWidget(QLabel("<b>Existing System Users:</b>"))
        user_table = QTableWidget()
        user_table.setColumnCount(2)
        user_table.setHorizontalHeaderLabels(["Username", "Access Level"])
        user_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        user_table.setFixedHeight(150)
        
        # Populate the table
        db = SessionLocal()
        users = db.query(User).all()
        user_table.setRowCount(len(users))
        for row, u in enumerate(users):
            user_table.setItem(row, 0, QTableWidgetItem(u.username))
            user_table.setItem(row, 1, QTableWidgetItem(u.role))
        db.close()
        master_layout.addWidget(user_table)

        # --- BOTTOM: Create New User Form ---
        form_group = QGroupBox("Add New Personnel")
        layout = QFormLayout(form_group)
        name_in = QLineEdit()
        pass_in = QLineEdit()
        pass_in.setEchoMode(QLineEdit.EchoMode.Password)
        role_in = QComboBox()
        role_in.addItems(["user", "admin"])
        
        layout.addRow("Username:", name_in)
        layout.addRow("Password:", pass_in)
        layout.addRow("Role:", role_in)
        
        btn = QPushButton("Commit to System")
        btn.setStyleSheet("background-color: #28a745; color: white; font-weight: bold;")
        btn.clicked.connect(dialog.accept)
        layout.addWidget(btn)
        
        master_layout.addWidget(form_group)
        
        if dialog.exec():
            self.process_new_user(name_in.text(), pass_in.text(), role_in.currentText())

    def process_new_user(self, username, password, role):
        if not username or not password: return
        db = SessionLocal()
        try:
            # THE FIX: We MUST hash the password here
            hashed_pw = get_password_hash(password)
            new_user = User(username=username, password_hash=hashed_pw, role=role)
            db.add(new_user)
            db.commit()
            QMessageBox.information(self, "Success", f"Credentials for {username} are now active.")
        except Exception as e:
            db.rollback()
            QMessageBox.critical(self, "Error", f"Failed to create user: {str(e)}")
        finally:
            db.close()


        if not username or not password: return
        db = SessionLocal()
        try:
            hashed = get_password_hash(password)
            new_user = User(username=username, password_hash=password, role=role)
            db.add(new_user)
            db.commit()
            QMessageBox.information(self, "Success", f"User {username} created.")
        except Exception as e:
            db.rollback()
            QMessageBox.critical(self, "Error", f"Could not create user: {str(e)}")
        finally:
            db.close()

    def browse_photo(self, index):
        path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.jpg *.png)")
        if path:
            self.selected_photos[index] = path
            pix = QPixmap(path).scaled(140, 140, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.photo_slots[index].setPixmap(pix)
            self.photo_slots[index].setStyleSheet("border: 2px solid #28a745; background: white;")

    def save_person(self):
        if not self.first_name.text() or not self.last_name.text() or not self.case_no.text():
            QMessageBox.warning(self, "Required Fields", "Names and Case Number are mandatory.")
            return

        db = SessionLocal()
        try:
            history_log = f"CURRENT ADDR: {self.current_address.text()} ({self.stay_duration.text()})\n"
            history_log += "RESIDENCY HISTORY:\n"
            for addr, dur in self.prev_addresses:
                if addr.text():
                    history_log += f"- {addr.text()} (Stay: {dur.text()})\n"

            p = Person(
                first_name=self.first_name.text(), last_name=self.last_name.text(),
                middle_names=self.middle_names.text(), date_of_birth=self.dob.text(),
                gender=self.gender.currentText(), nationality=self.nationality.text(),
                state_of_origin=self.state.text(), lga=self.lga.text(),
                fathers_name=self.f_name.text(), mothers_name=self.m_name.text(),
                mothers_maiden_name=self.m_maiden.text(), national_id_number=self.nin.text(),
                nin_verified=self.nin_verified.isChecked(), bvn=self.bvn.text(),
                height_cm=int(self.height.text()) if self.height.text().isdigit() else None,
                distinguishing_marks=f"{history_log}\nMARKS: {self.marks.toPlainText()}"
            )
            db.add(p)
            db.flush()

            if self.aliases.text():
                for a in self.aliases.text().split(","):
                    db.add(PersonAlias(person_id=p.person_id, alias_name=a.strip()))

            if self.phone.text():
                db.add(PersonContact(person_id=p.person_id, contact_type="Phone", contact_value=self.phone.text()))

            if self.org_name.text():
                org = db.query(Organization).filter_by(name=self.org_name.text()).first()
                if not org:
                    org = Organization(name=self.org_name.text(), org_type=self.org_type.currentText())
                    db.add(org)
                    db.flush()
                db.add(PersonAffiliation(person_id=p.person_id, org_id=org.org_id, 
                                         role=self.org_role.text(), is_active=self.org_active.isChecked()))

            asset_dir = "mvp/assets/photos"
            os.makedirs(asset_dir, exist_ok=True)
            for i, path in enumerate(self.selected_photos):
                if path:
                    fname = f"mug_{p.person_id}_{i}_{uuid4().hex[:6]}.jpg"
                    fpath = os.path.join(asset_dir, fname)
                    shutil.copy(path, fpath)
                    db.add(Biometric(person_id=p.person_id, biometric_type=self.labels[i], file_path=fpath))

            c = db.query(Case).filter_by(case_number=self.case_no.text()).first()
            if not c:
                c = Case(
                    case_number=self.case_no.text(), offense_type=self.offense.text(),
                    arrest_address=self.arrest_addr.text(), arresting_officer_id=int(self.officer_id.text() or 0),
                    description=self.case_desc.toPlainText(), formation_id=1
                )
                db.add(c)
                db.flush()
            db.add(PersonCase(person_id=p.person_id, case_id=c.case_id, role="Suspect"))

            db.commit()
            QMessageBox.information(self, "Saved", f"Profile for {p.first_name} committed successfully.")
            self.clear_form()
            
        except Exception as e:
            db.rollback()
            QMessageBox.critical(self, "Error", f"Save failed: {str(e)}")
        finally:
            db.close()

    def clear_form(self):
        for w in self.findChildren(QLineEdit): w.clear()
        for w in self.findChildren(QTextEdit): w.clear()
        for slot in self.photo_slots: 
            slot.clear()
            slot.setText("No Image")
            slot.setStyleSheet("border: 2px dashed #ccc; background: white; color: #7f8c8d;")
        for addr, dur in self.prev_addresses: 
            addr.clear()
            dur.clear()
        self.selected_photos = [None] * 4


   