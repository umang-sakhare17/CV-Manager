# app/ui/main_window.py
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QPushButton, QFileDialog,
    QTableWidget, QTableWidgetItem, QDialog
)
import sys
from datetime import date

from app.core import file_manager, database
from app.ui.import_dialog import ImportDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CV Manager")

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        # Import button
        self.import_btn = QPushButton("Import CV")
        self.import_btn.clicked.connect(self.import_cv)
        layout.addWidget(self.import_btn)

        # Dummy insert button
        self.dummy_btn = QPushButton("Add Dummy Application")
        self.dummy_btn.clicked.connect(self.add_dummy)
        layout.addWidget(self.dummy_btn)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Company", "Role", "Date Applied", "Notes", "File Path"]
        )
        layout.addWidget(self.table)

        # Load initial data
        self.refresh_table()

    def refresh_table(self):
        applications = database.fetch_all_applications()
        self.table.setRowCount(len(applications))

        for row_idx, row in enumerate(applications):
            self.table.setItem(row_idx, 0, QTableWidgetItem(row.get("company", "")))
            self.table.setItem(row_idx, 1, QTableWidgetItem(row.get("role", "")))
            self.table.setItem(row_idx, 2, QTableWidgetItem(row.get("date_applied", "")))
            self.table.setItem(row_idx, 3, QTableWidgetItem(row.get("notes", "")))
            self.table.setItem(row_idx, 4, QTableWidgetItem(row.get("file_path", "")))

    def import_cv(self):
        # Step 1: pick file
        path, _ = QFileDialog.getOpenFileName(
            self, "Select CV PDF", "", "PDF Files (*.pdf)"
        )
        if not path:
            return

        # Step 2: metadata dialog
        dlg = ImportDialog(self)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return

        data = dlg.get_data()
        if not data["company"]:
            print("Company is required.")
            return

        # Step 3: copy file to archive (now with date)
        archived_path = file_manager.copy_to_archive(
            path, data["company"], data["role"], data["date_applied"]
        )

        # Step 4: insert into DB
        database.insert_application(
            data["company"],
            data["role"],
            data["date_applied"],
            data["notes"],
            str(archived_path),
        )

        # Step 5: refresh UI
        self.refresh_table()


    def add_dummy(self):
        today = date.today().isoformat()
        file_path = "/tmp/fake.pdf"  # placeholder
        database.insert_application(
            "DummyCo",
            "Test Role",
            today,
            "This is a dummy entry",
            file_path,
        )
        self.refresh_table()


def run():
    app = QApplication(sys.argv)
    database.init_db()
    win = MainWindow()
    win.resize(800, 600)
    win.show()
    sys.exit(app.exec_())
