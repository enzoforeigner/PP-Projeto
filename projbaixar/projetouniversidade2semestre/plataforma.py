# plataforma.py
from PyQt6.QtWidgets import QGraphicsRectItem
from PyQt6.QtGui import QColor

class Plataforma(QGraphicsRectItem):
    def __init__(self, x, y, largura, altura, cor, posicao):
        super().__init__(0, 0, largura, altura)  # Define o tamanho da plataforma
        self.setPos(x, y)  # Posição da plataforma
        self.setBrush(QColor(cor))  # Define a cor da plataforma
        self.posicao = posicao # Posição da plataforma na cena