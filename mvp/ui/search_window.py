from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QLineEdit, QPushButton, QLabel, QHeaderView)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt
from database.database import SessionLocal
from database.models import Person, Biometric, PersonCase, Case
import os


class SearchWindow(QWidget):
    def __init__(self, main_app=None):
        super().__init__(main_app)
        self.main_app = main_app
        self.init_ui()
        self.load_data() # Initial load

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Header / Navigation
        header_layout = QHBoxLayout()
        back_btn = QPushButton("← Back to Capture")
        back_btn.clicked.connect(self.go_back)
        header_layout.addWidget(back_btn)
        
        title = QLabel("Intelligence Database")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        header_layout.addStretch()
        header_layout.addWidget(title)
        layout.addLayout(header_layout)

        # Search Bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by Name, NIN, or Case Number...")
        self.search_input.textChanged.connect(self.load_data) # Real-time filtering
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # Results Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Photo", "Full Name", "NIN", "Gender", "Last Case", "Date Created"
        ])
        
        # Table Styling
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setDefaultSectionSize(80) # Space for the mugshot
        self.table.setIconSize(Qt.Size(70, 70))
        
        layout.addWidget(self.table)

    def load_data(self):
        query_text = self.search_input.text()
        db = SessionLocal()
        
        try:
            # Base Query
            query = db.query(Person).filter(Person.is_deleted == False)

            # Apply Filters if search text exists
            if query_text:
                search = f"%{query_text}%"
                query = query.filter(
                    (Person.first_name.ilike(search)) | 
                    (Person.last_name.ilike(search)) |
                    (Person.national_id_number.ilike(search))
                )

            results = query.all()
            self.table.setRowCount(len(results))

            for row, person in enumerate(results):
                # 1. Handle Photo (First Biometric)
                photo_item = QTableWidgetItem()
                if person.biometrics:
                    path = person.biometrics[0].file_path
                    if os.path.exists(path):
                        icon = QIcon(path)
                        photo_item.setIcon(icon)
                
                # 2. Get Recent Case
                case_text = "N/A"
                if person.cases:
                    # Get the most recent case linked
                    case_text = person.cases[-1].case.case_number

                # 3. Fill Table
                self.table.setItem(row, 0, photo_item)
                self.table.setItem(row, 1, QTableWidgetItem(f"{person.first_name} {person.last_name}"))
                self.table.setItem(row, 2, QTableWidgetItem(person.national_id_number or "N/A"))
                self.table.setItem(row, 3, QTableWidgetItem(person.gender))
                self.table.setItem(row, 4, QTableWidgetItem(case_text))
                self.table.setItem(row, 5, QTableWidgetItem(person.created_at.strftime("%Y-%m-%d")))

        except Exception as e:
            print(f"Search Error: {e}")
        finally:
            db.close()

    def go_back(self):
        self.main_app.setCurrentIndex(0) # Assuming Capture is index 0