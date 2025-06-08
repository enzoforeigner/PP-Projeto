from PyQt6.QtWidgets import QGraphicsPixmapItem, QGraphicsScene
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

# Class Tabuleiro que representa o fundo do jogo
class Tabuleiro(QGraphicsPixmapItem):
    def __init__(self, caminho_imagem):
        super().__init__()
        pixmap = QPixmap(caminho_imagem)
        largura = 1200  
        altura = 800
        pixmap = pixmap.scaled(largura, altura, Qt.AspectRatioMode.KeepAspectRatio)
        self.setPixmap(pixmap)
        self.setPos(0, 0)
        

    def add_to_scene(self, scene):
        scene.addItem(self)
