# app/ui/import_dialog.py
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QLabel,
    QPushButton, QDateEdit, QTextEdit, QHBoxLayout, QFrame,
    QGraphicsDropShadowEffect
)
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QColor, QFont


class ModernLineEdit(QLineEdit):
    """Custom line edit with modern styling"""
    def __init__(self, placeholder=""):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setStyleSheet("""
            QLineEdit {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                background-color: white;
                color: #333333;
                min-height: 16px;
            }
            QLineEdit:focus {
                border: 2px solid #4A90E2;
                background-color: #FAFBFC;
            }
            QLineEdit:hover {
                border: 2px solid #B0B0B0;
            }
        """)


class ModernDateEdit(QDateEdit):
    """Custom date edit with modern styling"""
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QDateEdit {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                background-color: white;
                color: #333333;
                min-height: 16px;
            }
            QDateEdit:focus {
                border: 2px solid #4A90E2;
                background-color: #FAFBFC;
            }
            QDateEdit:hover {
                border: 2px solid #B0B0B0;
            }
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 24px;
                border-left-width: 1px;
                border-left-color: #C0C0C0;
                border-left-style: solid;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #F8F8F8, stop: 1 #E8E8E8);
            }
            QDateEdit::drop-down:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #FFFFFF, stop: 1 #F0F0F0);
            }
            QDateEdit::drop-down:pressed {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #E0E0E0, stop: 1 #D0D0D0);
            }
            QDateEdit::down-arrow {
                image: none;
                border: none;
                width: 0px;
                height: 0px;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 7px solid #666666;
                margin: 2px;
            }
            QCalendarWidget {
                background-color: white;
                color: #333333;
            }
            QCalendarWidget QWidget {
                alternate-background-color: #F5F5F5;
                color: #333333;
            }
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: #4A7BA7;
                color: white;
            }
            QCalendarWidget QToolButton {
                color: white;
                background-color: transparent;
                font-weight: bold;
            }
            QCalendarWidget QAbstractItemView:enabled {
                color: #333333;
                background-color: white;
                selection-background-color: #4A90E2;
                selection-color: white;
            }
            QCalendarWidget QMenu {
                color: #333333;
                background-color: white;
            }
            QCalendarWidget QSpinBox {
                color: #333333;
                background-color: white;
            }
            QCalendarWidget QTableView {
                color: #333333;
                background-color: white;
                gridline-color: #E0E0E0;
            }
        """)


class ModernTextEdit(QTextEdit):
    """Custom text edit with modern styling"""
    def __init__(self, placeholder=""):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setStyleSheet("""
            QTextEdit {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                background-color: white;
                color: #333333;
                min-height: 60px;
                max-height: 120px;
            }
            QTextEdit:focus {
                border: 2px solid #4A90E2;
                background-color: #FAFBFC;
            }
            QTextEdit:hover {
                border: 2px solid #B0B0B0;
            }
        """)


class ModernButton(QPushButton):
    """Custom button with modern macOS styling"""
    def __init__(self, text, button_type="primary"):
        super().__init__(text)
        self.button_type = button_type
        self._setup_style()
    
    def _setup_style(self):
        if self.button_type == "primary":
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                              stop: 0 #4A90E2, stop: 1 #357ABD);
                    border: 1px solid #2E5A8A;
                    border-radius: 8px;
                    color: white;
                    font-weight: 600;
                    font-size: 13px;
                    padding: 12px 24px;
                    min-width: 80px;
                    min-height: 20px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                              stop: 0 #5BA0F2, stop: 1 #408ACD);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                              stop: 0 #3A80D2, stop: 1 #2D6AAD);
                }
            """)
        else:  # secondary
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                              stop: 0 #F8F8F8, stop: 1 #E8E8E8);
                    border: 1px solid #C0C0C0;
                    border-radius: 8px;
                    color: #333333;
                    font-weight: 500;
                    font-size: 13px;
                    padding: 12px 24px;
                    min-width: 80px;
                    min-height: 20px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                              stop: 0 #FFFFFF, stop: 1 #F0F0F0);
                    border: 1px solid #A0A0A0;
                }
                QPushButton:pressed {
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                              stop: 0 #E0E0E0, stop: 1 #D0D0D0);
                }
            """)


class ImportDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_dialog()
        self._setup_ui()

    def _setup_dialog(self):
        """Configure dialog properties"""
        self.setWindowTitle("Import CV Metadata")
        self.setFixedSize(500, 600)
        self.setModal(True)
        
        # Apply modern dialog styling
        self.setStyleSheet("""
            QDialog {
                background-color: #F5F5F7;
            }
        """)

    def _setup_ui(self):
        """Initialize and layout all UI components"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(24, 24, 24, 24)

        # Create main content frame
        content_frame = QFrame()
        content_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E0E0E0;
            }
            QLabel {
                background: transparent;
                border: none;
                font-weight: 600;
                font-size: 14px;
                color: #404040;
                margin-bottom: 6px;
            }
        """)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setOffset(0, 4)
        content_frame.setGraphicsEffect(shadow)

        content_layout = QVBoxLayout(content_frame)
        content_layout.setSpacing(24)
        content_layout.setContentsMargins(24, 24, 24, 20)

        # Title
        title_label = QLabel("Import CV Metadata")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: 700;
                color: #1F1F1F;
                background: transparent;
                border: none;
                margin-bottom: 12px;
            }
        """)
        content_layout.addWidget(title_label)

        # Form fields
        self._create_form_fields(content_layout)

        # Buttons
        self._create_buttons(content_layout)

        main_layout.addWidget(content_frame)

    def _create_form_fields(self, layout):
        """Create form input fields"""
        # Company field
        company_layout = QVBoxLayout()
        company_layout.setSpacing(4)
        company_layout.addWidget(QLabel("Company:"))
        self.company_input = ModernLineEdit("Enter company name")
        company_layout.addWidget(self.company_input)
        layout.addLayout(company_layout)

        # Role field
        role_layout = QVBoxLayout()
        role_layout.setSpacing(4)
        role_layout.addWidget(QLabel("Role:"))
        self.role_input = ModernLineEdit("Enter job title/role")
        role_layout.addWidget(self.role_input)
        layout.addLayout(role_layout)

        # Date field
        date_layout = QVBoxLayout()
        date_layout.setSpacing(4)
        date_layout.addWidget(QLabel("Date Applied:"))
        self.date_input = ModernDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        date_layout.addWidget(self.date_input)
        layout.addLayout(date_layout)

        # Notes field
        notes_layout = QVBoxLayout()
        notes_layout.setSpacing(4)
        notes_layout.addWidget(QLabel("Notes:"))
        self.notes_input = ModernTextEdit("Optional notes about this application...")
        notes_layout.addWidget(self.notes_input)
        layout.addLayout(notes_layout)

    def _create_buttons(self, layout):
        """Create dialog action buttons"""
        # Add significant space before buttons
        layout.addSpacing(20)
        
        # Create a separate frame for buttons to ensure proper positioning
        button_frame = QFrame()
        button_frame.setStyleSheet("""
            QFrame {
                background: transparent;
                border: none;
            }
        """)
        
        button_layout = QHBoxLayout(button_frame)
        button_layout.setSpacing(12)
        button_layout.setContentsMargins(0, 12, 0, 0)
        button_layout.addStretch()

        self.cancel_button = ModernButton("Cancel", "secondary")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        self.ok_button = ModernButton("Import", "primary")
        self.ok_button.clicked.connect(self.accept)
        self.ok_button.setDefault(True)  # Make this the default button
        button_layout.addWidget(self.ok_button)

        layout.addWidget(button_frame)

    def get_data(self, existing_notes: str = "") -> dict:
        """
        Collect data from the dialog form fields.
        If notes are empty, preserve existing_notes.
        """
        notes_value = self.notes_input.toPlainText().strip()
        if not notes_value and existing_notes:
            notes_value = existing_notes

        return {
            "company": self.company_input.text().strip(),
            "role": self.role_input.text().strip(),
            "date": self.date_input.date().toString("yyyy-MM-dd"),
            "notes": notes_value,
        }