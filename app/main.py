# app/main.py
import sys
from PySide6.QtWidgets import QApplication
from app.ui.main_window import MainWindow
from app.core.database import init_db

def main():
    # Ensure DB exists before UI uses it
    db_file = init_db()
    print(f"[DB] Using database at: {db_file}")

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
