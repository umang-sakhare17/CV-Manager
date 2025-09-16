# app/ui/main_window.py
import os
import subprocess
import sys
from PyQt6.QtCore import QDate, Qt, QPropertyAnimation, QRect, QEasingCurve
from PyQt6.QtGui import QKeySequence, QShortcut, QFont, QPalette, QColor, QIcon
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QFrame,
    QFileDialog, QTableWidget, QTableWidgetItem, QMessageBox,
    QHeaderView, QHBoxLayout, QLineEdit, QLabel, QDateEdit, QDialog, 
    QAbstractItemView, QSpacerItem, QSizePolicy, QGraphicsDropShadowEffect
)
from app.core import file_manager, database
from app.ui.import_dialog import ImportDialog


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
                    padding: 8px 16px;
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
                QPushButton:disabled {
                    background: #D3D3D3;
                    border: 1px solid #A9A9A9;
                    color: #808080;
                }
            """)
        elif self.button_type == "secondary":
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                              stop: 0 #F8F8F8, stop: 1 #E8E8E8);
                    border: 1px solid #C0C0C0;
                    border-radius: 8px;
                    color: #333333;
                    font-weight: 500;
                    font-size: 13px;
                    padding: 8px 16px;
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
                QPushButton:disabled {
                    background: #F5F5F5;
                    border: 1px solid #D0D0D0;
                    color: #A0A0A0;
                }
            """)
        elif self.button_type == "danger":
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                              stop: 0 #E74C3C, stop: 1 #C0392B);
                    border: 1px solid #A93226;
                    border-radius: 8px;
                    color: white;
                    font-weight: 600;
                    font-size: 13px;
                    padding: 8px 16px;
                    min-height: 20px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                              stop: 0 #F85C4C, stop: 1 #D0493B);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                              stop: 0 #D73C2C, stop: 1 #B0291B);
                }
            """)


class ModernLineEdit(QLineEdit):
    """Custom line edit with modern styling"""
    def __init__(self, placeholder=""):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setStyleSheet("""
            QLineEdit {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
                background-color: white;
                color: #333333;
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
                padding: 8px 12px;
                font-size: 13px;
                background-color: white;
                color: #333333;
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
                width: 20px;
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
                border-top: 6px solid #666666;
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


class ModernTable(QTableWidget):
    """Custom table with modern macOS styling"""
    def __init__(self):
        super().__init__()
        self._setup_style()
    
    def _setup_style(self):
        self.setStyleSheet("""
            QTableWidget {
                gridline-color: #E5E5E5;
                background-color: white;
                border: 1px solid #D0D0D0;
                border-radius: 10px;
                font-size: 13px;
                color: #333333;
            }
            QTableWidget::item {
                padding: 12px 8px;
                border-bottom: 1px solid #F0F0F0;
                color: #333333;
            }
            QTableWidget::item:selected {
                background-color: #D6EBFF;
                color: #1F1F1F;
            }
            QTableWidget::item:hover {
                background-color: #F0F8FF;
            }
            QHeaderView::section {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #FAFAFA, stop: 1 #E8E8E8);
                border: none;
                border-right: 1px solid #D0D0D0;
                border-bottom: 2px solid #C0C0C0;
                padding: 8px 12px;
                font-weight: 600;
                font-size: 12px;
                color: #404040;
            }
            QHeaderView::section:first {
                border-left: none;
                border-top-left-radius: 10px;
            }
            QHeaderView::section:last {
                border-right: none;
                border-top-right-radius: 10px;
            }
        """)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._setup_window()
        self._setup_ui()
        self._setup_shortcuts()
        self.refresh_table()

    def _setup_window(self):
        """Configure main window properties"""
        self.setWindowTitle("CV Manager")
        self.resize(1000, 700)
        self.setMinimumSize(800, 600)
        
        # Apply modern macOS window styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F5F5F7;
            }
        """)

    def _setup_ui(self):
        """Initialize and layout all UI components"""
        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Header section
        self._create_header_section(main_layout)
        
        # Action buttons section
        self._create_buttons_section(main_layout)
        
        # Filters section
        self._create_filters_section(main_layout)
        
        # Table section
        self._create_table_section(main_layout)
        
        self.setCentralWidget(container)

    def _create_header_section(self, layout):
        """Create application header"""
        header_frame = QFrame()
        header_frame.setFixedHeight(60)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        title_label = QLabel("CV Manager")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: 700;
                color: #1F1F1F;
            }
        """)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        layout.addWidget(header_frame)

    def _create_buttons_section(self, layout):
        """Create action buttons section"""
        buttons_frame = QFrame()
        buttons_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E0E0E0;
            }
        """)
        buttons_layout = QHBoxLayout(buttons_frame)
        buttons_layout.setContentsMargins(20, 16, 20, 16)
        buttons_layout.setSpacing(12)

        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 2)
        buttons_frame.setGraphicsEffect(shadow)

        self.import_button = ModernButton("Import CV", "primary")
        self.import_button.clicked.connect(self.import_cv)
        buttons_layout.addWidget(self.import_button)

        self.open_button = ModernButton("Open CV", "secondary")
        self.open_button.setEnabled(False)
        self.open_button.clicked.connect(self.open_selected_file)
        buttons_layout.addWidget(self.open_button)

        self.edit_button = ModernButton("Edit Metadata", "secondary")
        self.edit_button.setEnabled(False)
        self.edit_button.clicked.connect(self.edit_metadata)
        buttons_layout.addWidget(self.edit_button)

        buttons_layout.addStretch()

        self.delete_button = ModernButton("Delete Application", "danger")
        self.delete_button.clicked.connect(self.delete_application)
        buttons_layout.addWidget(self.delete_button)

        layout.addWidget(buttons_frame)

    def _create_filters_section(self, layout):
        """Create search and filter controls"""
        filter_frame = QFrame()
        filter_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E0E0E0;
            }
            QLabel {
                background: transparent;
                border: none;
                font-weight: 600;
                font-size: 13px;
                color: #404040;
            }
        """)
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setContentsMargins(20, 16, 20, 16)
        filter_layout.setSpacing(16)

        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 2)
        filter_frame.setGraphicsEffect(shadow)

        # Search section
        search_label = QLabel("Search:")
        filter_layout.addWidget(search_label)

        self.search_input = ModernLineEdit("Company, Role, Notes...")
        self.search_input.textChanged.connect(self.refresh_table)
        filter_layout.addWidget(self.search_input)

        # Date filter section
        date_label = QLabel("From Date:")
        filter_layout.addWidget(date_label)

        self.date_filter = ModernDateEdit()
        self.date_filter.setCalendarPopup(True)
        self.date_filter.setDisplayFormat("yyyy-MM-dd")
        self.date_filter.setSpecialValueText("Any")
        self.date_filter.setDateRange(QDate(1900, 1, 1), QDate(9999, 12, 31))
        self.date_filter.setDate(self.date_filter.minimumDate())
        self.date_filter.dateChanged.connect(self.refresh_table)
        filter_layout.addWidget(self.date_filter)

        filter_layout.addStretch()

        self.clear_filter_btn = ModernButton("Clear Filters", "secondary")
        self.clear_filter_btn.clicked.connect(self.clear_filters)
        filter_layout.addWidget(self.clear_filter_btn)

        layout.addWidget(filter_frame)

    def _create_table_section(self, layout):
        """Create main data table"""
        table_frame = QFrame()
        table_frame.setStyleSheet("""
            QFrame {
                background-color: transparent;
                border: none;
            }
        """)
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(0, 0, 0, 0)

        self.table = ModernTable()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Company", "Role", "Date Applied", "Notes", "File Path"])
        
        # Configure table properties
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # Company
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Role
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Date
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)           # Notes
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)           # File Path
        
        self.table.setAlternatingRowColors(True)
        self.table.setWordWrap(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        # Set minimum row height for better spacing
        self.table.verticalHeader().setDefaultSectionSize(50)
        self.table.verticalHeader().hide()

        # Connect table events
        self.table.cellDoubleClicked.connect(self.open_selected_file)
        self.table.itemSelectionChanged.connect(self._update_buttons)

        # Add shadow effect to table
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 4)
        self.table.setGraphicsEffect(shadow)

        table_layout.addWidget(self.table)
        layout.addWidget(table_frame)

    def _setup_shortcuts(self):
        """Configure keyboard shortcuts"""
        delete_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Delete), self.table)
        delete_shortcut.activated.connect(self.delete_application)

        backspace_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Backspace), self.table)
        backspace_shortcut.activated.connect(self.delete_application)

    def refresh_table(self):
        """Update table data with current filters applied"""
        apps = database.fetch_all_applications()

        # Apply search filter
        search_term = self.search_input.text().strip().lower()

        # Apply date filter
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

            # Date filter
            if min_date and app["date_applied"] < min_date:
                continue

            filtered.append(app)

        self._populate_table(filtered)

    def _populate_table(self, apps):
        """Populate table with application data"""
        self.table.setRowCount(len(apps))

        for row_idx, app in enumerate(apps):
            company_item = QTableWidgetItem(app["company"])
            company_item.setData(Qt.ItemDataRole.UserRole, app["id"])
            self.table.setItem(row_idx, 0, company_item)
            
            self.table.setItem(row_idx, 1, QTableWidgetItem(app["role"] or ""))
            self.table.setItem(row_idx, 2, QTableWidgetItem(app["date_applied"]))
            self.table.setItem(row_idx, 3, QTableWidgetItem(app["notes"] or ""))
            self.table.setItem(row_idx, 4, QTableWidgetItem(app["file_path"]))

    def clear_filters(self):
        """Reset all filters to default state"""
        self.search_input.clear()
        self.date_filter.setDate(self.date_filter.minimumDate())
        self.refresh_table()

    def import_cv(self):
        """Handle CV import process"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CV PDF", "", "PDF Files (*.pdf)"
        )
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
                    str(archived_path)
                )
                self.refresh_table()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to import CV: {e}")

    def _update_buttons(self):
        """Update button states based on table selection"""
        has_selection = bool(self.table.selectedItems())
        self.open_button.setEnabled(has_selection)
        self.edit_button.setEnabled(has_selection)

    def open_selected_file(self):
        """Open the selected CV file in default application"""
        selected = self.table.currentRow()
        if selected < 0:
            return

        file_path_item = self.table.item(selected, 4)
        if not file_path_item:
            return

        file_path = file_path_item.text()
        if not os.path.exists(file_path):
            QMessageBox.warning(
                self, "File Missing", f"The file does not exist:\n{file_path}"
            )
            return

        try:
            if os.name == "nt":  # Windows
                os.startfile(file_path)
            elif sys.platform == "darwin":  # macOS
                subprocess.run(["open", file_path])
            else:  # Linux/Unix
                subprocess.run(["xdg-open", file_path])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open file:\n{e}")
    
    def edit_metadata(self):
        """Edit metadata for selected application"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a row to edit.")
            return

        # Get application ID and current data
        company_item = self.table.item(row, 0)
        app_id = company_item.data(Qt.ItemDataRole.UserRole)

        role = self.table.item(row, 1).text()
        date_applied = self.table.item(row, 2).text()
        notes = self.table.item(row, 3).text()

        # Show edit dialog with current values
        dlg = ImportDialog(self)
        dlg.company_input.setText(company_item.text())
        dlg.role_input.setText(role)
        dlg.date_input.setDate(QDate.fromString(date_applied, "yyyy-MM-dd"))
        dlg.notes_input.setPlainText(notes)

        if dlg.exec() == QDialog.DialogCode.Accepted:
            data = dlg.get_data()
            try:
                new_path = file_manager.rename_file(
                    app_id,
                    data["company"],
                    data["role"],
                    data["date"],
                )

                # Update table immediately
                self.table.item(row, 0).setText(data["company"])
                self.table.item(row, 1).setText(data["role"])
                self.table.item(row, 2).setText(data["date"])
                self.table.item(row, 3).setText(data["notes"])
                self.table.item(row, 4).setText(new_path)

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not update metadata:\n{e}")

    def delete_application(self):
        """Delete selected application after confirmation"""
        selected = self.table.selectedItems()
        if not selected:
            return

        row = self.table.currentRow()
        if row < 0:
            return

        # Confirmation dialog
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this application?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            item = self.table.item(row, 0)
            if item:
                app_id = item.data(Qt.ItemDataRole.UserRole)
                if app_id:
                    try:
                        file_manager.delete_application_and_file(app_id)
                        self.refresh_table()
                    except Exception as e:
                        QMessageBox.critical(self, "Error", f"Failed to delete application: {e}")