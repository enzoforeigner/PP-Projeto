# plataforma.py
from PyQt6.QtWidgets import QGraphicsRectItem
from PyQt6.QtGui import QBrush, QPen
from PyQt6.QtCore import Qt

class Plataforma(QGraphicsRectItem):
    def __init__(self, x, y, largura, altura, cor, posicao):
        super().__init__(0, 0, largura, altura)
        self.setPos(x, y)

        # Plataforma invisível: sem preenchimento e sem contorno
        self.setBrush(QBrush(Qt.BrushStyle.NoBrush))
        self.setPen(QPen(Qt.PenStyle.NoPen))

        self.posicao = posicao
