from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QPushButton, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QLabel, QFrame)
from PyQt6.QtCore import Qt
from database.database import SessionLocal
from database.models import Person, PersonAlias, PersonCase, Case
from sqlalchemy import or_

class SearchWindow(QWidget):
    def __init__(self, main_app=None):
        super().__init__(main_app)
        self.main_app = main_app
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        # 1. HEADER & NAVIGATION
        header = QHBoxLayout()
        
        btn_back = QPushButton("⬅ Back to Capture")
        btn_back.setFixedWidth(150)
        btn_back.setStyleSheet("padding: 5px; font-weight: bold;")
        btn_back.clicked.connect(self.go_back)
        
        title = QLabel("Records")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        
        header.addWidget(btn_back)
        header.addStretch()
        header.addWidget(title)
        self.layout.addLayout(header)

        # 2. UNIVERSAL SEARCH BAR
        search_frame = QFrame()
        search_frame.setStyleSheet("background: #f1f2f6; border-radius: 8px; border: 1px solid #dcdde1;")
        search_layout = QHBoxLayout(search_frame)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by Name, Alias, NIN, BVN, or Case Number...")
        self.search_input.setStyleSheet("padding: 8px; font-size: 14px; background: dark gray;")
        self.search_input.returnPressed.connect(self.perform_search)
        
        btn_run_search = QPushButton("Run Search")
        btn_run_search.setFixedWidth(120)
        btn_run_search.setFixedHeight(40)
        btn_run_search.setStyleSheet("""
            QPushButton { background: #3498db; color: white; font-weight: bold; border-radius: 4px; }
            QPushButton:hover { background: #2980b9; }
        """)
        btn_run_search.clicked.connect(self.perform_search)
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(btn_run_search)
        self.layout.addWidget(search_frame)

        # 3. RESULTS TABLE
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(5)
        self.results_table.setHorizontalHeaderLabels(["Full Name", "Known Aliases", "NIN / ID", "Recent Case", "Status"])
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.results_table.setAlternatingRowColors(True)
        self.results_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.results_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        self.layout.addWidget(self.results_table)

    def perform_search(self):
        query_text = self.search_input.text().strip()
        if not query_text:
            return

        db = SessionLocal()
        try:
            search_val = f"%{query_text}%"
            
            # Joins allow us to search through aliases and cases simultaneously
            results = db.query(Person).outerjoin(PersonAlias).outerjoin(PersonCase).outerjoin(Case).filter(
                or_(
                    Person.first_name.ilike(search_val),
                    Person.last_name.ilike(search_val),
                    Person.national_id_number.ilike(search_val),
                    Person.bvn.ilike(search_val),
                    PersonAlias.alias_name.ilike(search_val),
                    Case.case_number.ilike(search_val)
                )
            ).distinct().all()

            self.update_table(results)
        except Exception as e:
            print(f"Search Error: {e}")
        finally:
            db.close()

    def update_table(self, results):
        self.results_table.setRowCount(0)
        for person in results:
            row_idx = self.results_table.rowCount()
            self.results_table.insertRow(row_idx)
            
            # Combine aliases into a string
            alias_str = ", ".join([a.alias_name for a in person.aliases]) if person.aliases else "None"
            
            # Get case number
            case_str = "No Record"
            if person.cases:
                # person.cases is a list of PersonCase objects; person.cases[0].case is the Case object
                case_str = person.cases[0].case.case_number

            self.results_table.setItem(row_idx, 0, QTableWidgetItem(f"{person.first_name} {person.last_name}"))
            self.results_table.setItem(row_idx, 1, QTableWidgetItem(alias_str))
            self.results_table.setItem(row_idx, 2, QTableWidgetItem(person.national_id_number or "N/A"))
            self.results_table.setItem(row_idx, 3, QTableWidgetItem(case_str))
            self.results_table.setItem(row_idx, 4, QTableWidgetItem("Active"))

    def go_back(self):
        # Dynamically find the CaptureWindow index instead of guessing 0
        for i in range(self.main_app.count()):
            widget = self.main_app.widget(i)
            # This checks the class name of the widget
            if widget.__class__.__name__ == "CaptureWindow":
                self.main_app.setCurrentIndex(i)
                return