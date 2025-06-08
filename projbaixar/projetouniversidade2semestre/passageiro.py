# passageiro.py
from PyQt6.QtWidgets import QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

# Dicionário que associa cores às imagens
imagens_passageiro = {
    "red": "boneco_vermelho.png",
    "green": "boneco_verde.png",
    "yellow": "boneco_amarelo.png",
    "blue": "boneco_azul.png"
}

class Passageiro(QGraphicsPixmapItem):
    def __init__(self, x, y, cor, autocarro=None):
        super().__init__()
        self.cor = cor
        self.autocarro = autocarro

        caminho_imagem = imagens_passageiro.get(cor)
        if not caminho_imagem:
            print(f"❌ Cor inválida: {cor}")
            return

        pixmap = QPixmap(caminho_imagem)
        if pixmap.isNull():
            print(f"❌ Erro ao carregar imagem: {caminho_imagem}")
            return

        # Ajuste o tamanho se necessário (ex: 40x40)
        pixmap = pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

        self.setPixmap(pixmap)
        self.setPos(x, y)

    def tentar_embarcar(self):
        if self.autocarro and self.autocarro.embarcar_passageiro(self):
            print("✅ Passageiro embarcou com sucesso!")
        else:
            print("❌ Autocarro lotado ou indisponível.")
