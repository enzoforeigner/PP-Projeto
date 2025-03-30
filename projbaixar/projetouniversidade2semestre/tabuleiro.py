# tabuleiro.py
from PyQt6.QtWidgets import QGraphicsRectItem, QGraphicsScene
from PyQt6.QtGui import QColor

class Tabuleiro(QGraphicsRectItem):
    def __init__(self, largura, altura):
        super().__init__(0, 0, largura, altura)  # Define o tamanho do tabuleiro
        self.setBrush(QColor("lightgray"))  # Cor do tabuleiro
        self.setPos(0, 0)  # Posição do tabuleiro na cena

    def add_to_scene(self, scene: QGraphicsScene):
        scene.addItem(self)  # Adiciona o tabuleiro à cena