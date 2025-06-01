from PyQt6.QtWidgets import QGraphicsPixmapItem, QGraphicsScene
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt  # Necessário para manter proporção

class Tabuleiro(QGraphicsPixmapItem):
    def __init__(self, imagem_path):
        super().__init__()
        pixmap = QPixmap(imagem_path)
        if pixmap.isNull():
            print(f"❌ Erro: Imagem não encontrada -> {imagem_path}")
        else:
            print(f"✅ Imagem carregada: {imagem_path}")
            
            # 🔽 Redimensionar a imagem aqui
            largura = 1200   # Defina o tamanho desejado (exemplo)
            altura = 800
            pixmap = pixmap.scaled(largura, altura, Qt.AspectRatioMode.KeepAspectRatio)

            self.setPixmap(pixmap)
            self.setPos(0, 0)

    def add_to_scene(self, scene: QGraphicsScene):
        scene.addItem(self)
