# passageiro.py
from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsItemGroup
from PyQt6.QtGui import QColor, QPen
from PyQt6.QtCore import Qt

class Passageiro(QGraphicsItemGroup):
    def __init__(self, x, y, cor, autocarro=None):
        super().__init__()
        self.cor = cor
        self.autocarro = autocarro

        cor_qt = QColor(cor)
        sem_borda = QPen(Qt.PenStyle.NoPen)

        # Cabeça
        cabeca = QGraphicsEllipseItem(6, 0, 28, 28)
        cabeca.setBrush(cor_qt)
        cabeca.setPen(sem_borda)
        self.addToGroup(cabeca)

        # Tronco
        tronco = QGraphicsRectItem(13, 26, 14, 18)
        tronco.setBrush(cor_qt)
        tronco.setPen(sem_borda)
        self.addToGroup(tronco)

        # Braços
        braco_esq = QGraphicsRectItem(7, 26, 6, 14)
        braco_esq.setBrush(cor_qt)
        braco_esq.setPen(sem_borda)
        self.addToGroup(braco_esq)

        braco_dir = QGraphicsRectItem(27, 26, 6, 14)
        braco_dir.setBrush(cor_qt)
        braco_dir.setPen(sem_borda)
        self.addToGroup(braco_dir)

        # Pernas
        perna_esq = QGraphicsRectItem(13, 44, 6, 14)
        perna_esq.setBrush(cor_qt)
        perna_esq.setPen(sem_borda)
        self.addToGroup(perna_esq)

        perna_dir = QGraphicsRectItem(21, 44, 6, 14)
        perna_dir.setBrush(cor_qt)
        perna_dir.setPen(sem_borda)
        self.addToGroup(perna_dir)

        # Posiciona o boneco
        self.setPos(x, y)

    def tentar_embarcar(self):
        if self.autocarro and self.autocarro.embarcar_passageiro(self):
            print("✅ Passageiro embarcou com sucesso!")
        else:
            print("❌ Autocarro lotado ou indisponível.")
