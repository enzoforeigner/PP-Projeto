from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton
from ui.cena import Cena

# nossa classe principal MainWindow 
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Park Out")

        
        self.init_ui() # Configurar a interface

    def init_ui(self):
        layout = QVBoxLayout()

        
        self.cena = Cena()          # Adiciona o cenário
        layout.addWidget(self.cena)

        botao_reiniciar = QPushButton("🔁 Reiniciar Jogo")
        botao_reiniciar.clicked.connect(self.cena.reiniciar)  # Conecta com a minha função de reiniciar
        layout.addWidget(botao_reiniciar)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)