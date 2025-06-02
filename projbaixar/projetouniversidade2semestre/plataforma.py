# plataforma.py
from PyQt6.QtWidgets import QGraphicsRectItem
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt, QTimer, QPointF, QPropertyAnimation

class Plataforma(QGraphicsRectItem):
    def __init__(self, x, y, largura, altura, cor, posicao):
        super().__init__(0, 0, largura, altura)  # Define o tamanho da plataforma
        self.setPos(x, y)  # Posição da plataforma
        self.setBrush(QColor(cor))  # Define a cor da plataforma
        self.posicao = posicao # Posição da plataforma na cena

    def animar_autocarro(self, autocarro):
        destino = self.pos()
        timer = QTimer()

        def mover():
            pos_atual = autocarro.pos()
            step_x = (destino.x() - pos_atual.x()) * 0.1
            step_y = (destino.y() - pos_atual.y()) * 0.1
            nova_posicao = QPointF(pos_atual.x() + step_x, pos_atual.y() + step_y)
            autocarro.setPos(nova_posicao)

            if abs(nova_posicao.x() - destino.x()) < 2 and abs(nova_posicao.y() - destino.y()) < 2:
                autocarro.setPos(destino)
                timer.stop()
                autocarro.embarcar_passageiro()

        timer.timeout.connect(mover)
        timer.start(20)