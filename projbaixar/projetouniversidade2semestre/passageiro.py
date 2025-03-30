# passageiro.py
from PyQt6.QtWidgets import QGraphicsEllipseItem
from PyQt6.QtGui import QColor

class Passageiro(QGraphicsEllipseItem):
    def __init__(self, x, y, cor, autocarro=None):
        super().__init__(0, 0, 20, 20)  # Tamanho do passageiro (círculo)
        self.setPos(x, y)
        self.setBrush(QColor(cor))  # Define a cor do passageiro
        self.cor = cor
        self.autocarro = autocarro  # Referência ao autocarro (se houver)

    def tentar_embarcar(self):
        if self.autocarro and self.autocarro.embarcar_passageiro(self):
            print("Passageiro embarcou com sucesso!")
        else:
            print("Autocarro lotado ou não disponível.")