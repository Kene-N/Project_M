from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QPushButton, QTableWidget, QTableWidgetItem, 
                             QLabel, QHeaderView) 
from PyQt6.QtCore import Qt
from database.database import SessionLocal
from database.models import Person

class SearchWindow(QWidget):
    def __init__(self, main_app=None):
        super().__init__(main_app)
        self.main_app = main_app 
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.main_app.setCurrentIndex(1)

        # 1. Top Navigation & Search
        top_layout = QHBoxLayout()
        
        self.btn_back = QPushButton("← Back to Capture")
        self.btn_back.clicked.connect(self.back_to_capture)
        top_layout.addWidget(self.btn_back)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by Name or NIN...")
        self.search_input.setFixedHeight(40)
        self.search_input.textChanged.connect(self.run_search)
        top_layout.addWidget(self.search_input)
        
        layout.addLayout(top_layout)

        # 2. Results Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["NIN", "First Name", "Last Name", "Gender"])
        
        # Corrected Header Logic
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)

        # Initial Load
        self.run_search()

    def run_search(self):
        search_term = self.search_input.text()
        db = SessionLocal()
        
        query = db.query(Person)
        if search_term:
            query = query.filter(
                (Person.national_id_number.contains(search_term)) |
                (Person.first_name.contains(search_term)) |
                (Person.last_name.contains(search_term))
            )
        
        results = query.all()
        db.close()

        self.table.setRowCount(0)
        for row_idx, person in enumerate(results):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(person.national_id_number or "")))
            self.table.setItem(row_idx, 1, QTableWidgetItem(str(person.first_name or "")))
            self.table.setItem(row_idx, 2, QTableWidgetItem(str(person.last_name or "")))
            self.table.setItem(row_idx, 3, QTableWidgetItem(str(person.gender or "")))

    def back_to_capture(self):
        # This takes the user back to the Capture Screen
        self.main_app.setCurrentIndex(1) # Index 1 is the Capture screen in our stack