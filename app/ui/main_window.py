# app/ui/main_window.py
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QTableWidget, QTableWidgetItem, QMessageBox,
    QHeaderView, QLabel
)
from app.core import file_manager, database
from app.ui.import_dialog import ImportDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CV Manager")

        # ✅ Set a standard default size
        self.resize(800, 600)

        container = QWidget()
        layout = QVBoxLayout()

        # Import button only (removed dummy entry)
        self.import_button = QPushButton("Import CV")
        self.import_button.clicked.connect(self.import_cv)
        layout.addWidget(self.import_button)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Company", "Role", "Date", "Notes", "File Path"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # ✅ Better table look
        self.table.setAlternatingRowColors(True)
        self.table.setWordWrap(True)

        layout.addWidget(self.table)
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.refresh_table()

    def refresh_table(self):
        apps = database.fetch_all_applications()
        self.table.setRowCount(len(apps))

        if not apps:
            # ✅ Empty state message
            QMessageBox.information(self, "No Records", "No applications found in the database yet.")

        for row_idx, app in enumerate(apps):
            self.table.setItem(row_idx, 0, QTableWidgetItem(app["company"]))
            self.table.setItem(row_idx, 1, QTableWidgetItem(app["role"]))
            self.table.setItem(row_idx, 2, QTableWidgetItem(app["date_applied"]))
            self.table.setItem(row_idx, 3, QTableWidgetItem(app["notes"]))
            self.table.setItem(row_idx, 4, QTableWidgetItem(app["file_path"]))

    def import_cv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CV PDF", "", "PDF Files (*.pdf)")
        if not file_path:
            return

        dialog = ImportDialog(self)
        if dialog.exec() == dialog.DialogCode.Accepted:
            data = dialog.get_data()
            try:
                archived_path = file_manager.copy_to_archive(
                    file_path,
                    data["company"],
                    data["role"],
                    data["date"]
                )
                database.insert_application(
                    data["company"],
                    data["role"],
                    data["date"],
                    data["notes"],
                    archived_path
                )
                self.refresh_table()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to import CV: {e}")
