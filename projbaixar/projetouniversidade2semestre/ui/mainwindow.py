# ui/main_window.py
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from ui.cena import Cena

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Park Out")

        # Configurar a interface
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Adiciona o cenário
        self.cena = Cena()
        layout.addWidget(self.cena)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)