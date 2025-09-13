# app/ui/import_dialog.py
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QLabel,
    QPushButton, QDateEdit, QTextEdit, QHBoxLayout
)
from PyQt6.QtCore import QDate


class ImportDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Import CV Metadata")

        layout = QVBoxLayout()

        # Company
        layout.addWidget(QLabel("Company:"))
        self.company_input = QLineEdit()
        layout.addWidget(self.company_input)

        # Role
        layout.addWidget(QLabel("Role:"))
        self.role_input = QLineEdit()
        layout.addWidget(self.role_input)

        # Date
        layout.addWidget(QLabel("Date Applied:"))
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        layout.addWidget(self.date_input)

        # Notes
        layout.addWidget(QLabel("Notes:"))
        self.notes_input = QTextEdit()
        layout.addWidget(self.notes_input)

        # Buttons row
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def get_data(self):
        return {
            "company": self.company_input.text().strip(),
            "role": self.role_input.text().strip(),
            "date_applied": self.date_input.date().toString("yyyy-MM-dd"),
            "notes": self.notes_input.toPlainText().strip(),
        }
