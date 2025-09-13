# run.py
from app.core import database
from app.ui.main_window import MainWindow
from PyQt6.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    # Ensure DB exists
    database.init_db()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
