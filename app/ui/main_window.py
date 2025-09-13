# app/ui/main_window.py
import os
import subprocess
import sys
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QTableWidget, QTableWidgetItem, QMessageBox,
    QHeaderView, QHBoxLayout, QLineEdit, QLabel, QDateEdit
)
from app.core import file_manager, database
from app.ui.import_dialog import ImportDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CV Manager")
        self.resize(800, 600)

        container = QWidget()
        layout = QVBoxLayout()

        # Buttons row
        buttons_layout = QHBoxLayout()

        self.import_button = QPushButton("Import CV")
        self.import_button.clicked.connect(self.import_cv)
        buttons_layout.addWidget(self.import_button)

        self.open_button = QPushButton("Open CV")
        self.open_button.setEnabled(False)  # only active if row selected
        self.open_button.clicked.connect(self.open_selected_file)
        buttons_layout.addWidget(self.open_button)

        layout.addLayout(buttons_layout)

        # Filter row
        filter_layout = QHBoxLayout()

        filter_layout.addWidget(QLabel("Search:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Company, Role, Notes...")
        self.search_input.textChanged.connect(self.refresh_table)
        filter_layout.addWidget(self.search_input)

        filter_layout.addWidget(QLabel("From date:"))
        self.date_filter = QDateEdit()
        self.date_filter.setCalendarPopup(True)
        self.date_filter.setDisplayFormat("yyyy-MM-dd")
        self.date_filter.setSpecialValueText("Any")   # show 'Any' when no date
        self.date_filter.setDateRange(QDate(1900, 1, 1), QDate(9999, 12, 31))
        self.date_filter.setDate(self.date_filter.minimumDate())  # start as 'Any'
        self.date_filter.dateChanged.connect(self.refresh_table)
        filter_layout.addWidget(self.date_filter)


        self.clear_filter_btn = QPushButton("Clear Filters")
        self.clear_filter_btn.clicked.connect(self.clear_filters)
        filter_layout.addWidget(self.clear_filter_btn)

        layout.addLayout(filter_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Company", "Role", "Date", "Notes", "File Path"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setWordWrap(True)

        # Double-click to open
        self.table.cellDoubleClicked.connect(self.open_selected_file)

        # Track selection to enable/disable "Open CV"
        self.table.itemSelectionChanged.connect(self._update_open_button)

        layout.addWidget(self.table)
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.refresh_table()

    def refresh_table(self):
        apps = database.fetch_all_applications()

        # Apply filters
        search_term = self.search_input.text().strip().lower()

        # Only apply date filter if it's not "Any"
        date_value = self.date_filter.date()
        min_date = None
        if date_value != self.date_filter.minimumDate():
            min_date = date_value.toString("yyyy-MM-dd")

        filtered = []
        for app in apps:
            # Search term filter
            if search_term and not (
                search_term in app["company"].lower()
                or search_term in (app["role"] or "").lower()
                or search_term in (app["notes"] or "").lower()
            ):
                continue

            # Date filter only if set
            if min_date and app["date_applied"] < min_date:
                continue

            filtered.append(app)

        self.table.setRowCount(len(filtered))

        for row_idx, app in enumerate(filtered):
            self.table.setItem(row_idx, 0, QTableWidgetItem(app["company"]))
            self.table.setItem(row_idx, 1, QTableWidgetItem(app["role"]))
            self.table.setItem(row_idx, 2, QTableWidgetItem(app["date_applied"]))
            self.table.setItem(row_idx, 3, QTableWidgetItem(app["notes"]))
            self.table.setItem(row_idx, 4, QTableWidgetItem(app["file_path"]))


    def clear_filters(self):
        self.search_input.clear()
        self.date_filter.setDate(self.date_filter.minimumDate())  # reset to 'Any'
        self.refresh_table()


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

    def _update_open_button(self):
        self.open_button.setEnabled(bool(self.table.selectedItems()))

    def open_selected_file(self):
        selected = self.table.currentRow()
        if selected < 0:
            return

        file_path_item = self.table.item(selected, 4)
        if not file_path_item:
            return

        file_path = file_path_item.text()
        if not os.path.exists(file_path):
            QMessageBox.warning(self, "File Missing", f"The file does not exist:\n{file_path}")
            return

        # Cross-platform open
        try:
            if os.name == "nt":  # Windows
                os.startfile(file_path)
            elif sys.platform == "darwin":  # macOS
                subprocess.run(["open", file_path])
            else:  # Linux/Unix
                subprocess.run(["xdg-open", file_path])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open file:\n{e}")
