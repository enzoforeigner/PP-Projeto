# passageiro.py
from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class Passageiro(QGraphicsPixmapItem):
    def __init__(self, x, y, cor, largura=34, altura=34, autocarro=None):
        super().__init__()
        
        # Mapeia cor para imagem
        imagens_por_cor = {
            "yellow": "imagens/boneco_amarelo.png",
            "red": "imagens/boneco_vermelho.png",
            "blue": "imagens/boneco_azul.png",
            "green": "imagens/boneco_verde.png",
        }
        
        caminho_imagem = imagens_por_cor.get(cor)  # fallback caso cor desconhecida
        pixmap = QPixmap(caminho_imagem)
        
        if pixmap.isNull():
            print(f"Erro: imagem não encontrada no caminho {caminho_imagem}")
        else:
            pixmap = pixmap.scaled(largura, altura, Qt.AspectRatioMode.KeepAspectRatio)
            self.setPixmap(pixmap)
        
        self.setPos(x, y)
        self.autocarro = autocarro
        self.cor = cor

    def tentar_embarcar(self):
        if self.autocarro and self.autocarro.embarcar_passageiro(self):
            print("Passageiro embarcou com sucesso!")
        else:
            print("Autocarro lotado ou não disponível.")