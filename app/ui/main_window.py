from PySide6.QtWidgets import QMainWindow, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CV Manager")
        self.setGeometry(100, 100, 800, 600)

        label = QLabel("Welcome to CV Manager!", self)
        label.setGeometry(20, 20, 300, 40)
