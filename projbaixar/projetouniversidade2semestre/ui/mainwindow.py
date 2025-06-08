# ui/main_window.py
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton
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

        botao_reiniciar = QPushButton("🔁 Reiniciar Jogo")
        botao_reiniciar.clicked.connect(self.cena.reiniciar)  # Conectando à função que você criará na Cena
        layout.addWidget(botao_reiniciar)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)