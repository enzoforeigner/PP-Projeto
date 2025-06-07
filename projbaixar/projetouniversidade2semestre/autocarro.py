from PyQt6.QtWidgets import QGraphicsPixmapItem, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer, QPointF
from passageiro import Passageiro
import math


def obter_direcao_grid(angulo):
    if angulo == 0:
        return (0, -1)
    elif angulo == 90:
        return (1, 0)
    elif angulo == 180:
        return (0, 1)
    elif angulo == 270:
        return (-1, 0)
    elif angulo == 45:
        return (1, -1)
    elif angulo == 135:
        return (-1, -1)
    elif angulo == 225:
        return (-1, 1)
    elif angulo == 315:
        return (1, 1)
    else:
        return (0, 0)


class Autocarro(QGraphicsPixmapItem):
    def __init__(self, x, y, cor, cena, capacidade=4, angulo=135):
        super().__init__()
        self.setPos(x, y)
        self.cor = cor
        self.cena = cena
        self.capacidade = capacidade
        self.angulo = angulo
        self.plataforma = None

        caminhos = {
            "blue": "carro_azul.png",
            "red": "carro_vermelho.png",
            "yellow": "carro_amarelo.png",
            "green": "carro_verde.png"
        }
        caminho_img = caminhos.get(cor, "carro_azul.png")
        pixmap = QPixmap(caminho_img)
        if pixmap.isNull():
            print(f"❌ Erro ao carregar imagem: {caminho_img}")
            return

        pixmap = pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio)
        self.setPixmap(pixmap)
        self.setTransformOriginPoint(pixmap.width() / 2, pixmap.height() / 2)
        self.setRotation(angulo)

        seta = QPixmap("seta_branca.png")
        if not seta.isNull():
            seta = seta.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio)
            self.seta = QGraphicsPixmapItem(seta, self)
            self.seta.setOffset((pixmap.width() - seta.width()) / 2,
                                (pixmap.height() - seta.height()) / 2)
            self.seta.setRotation(0)

    def mousePressEvent(self, event):
        if not self.bloqueado_frente():
            self.move_to_platform()
        else:
            print("❌ Caminho bloqueado para frente.")

    def bloqueado_frente(self):
        if not hasattr(self.cena, "grid") or self not in self.cena.grid_posicoes:
            return True

        linha, coluna = self.cena.grid_posicoes[self]
        dx, dy = obter_direcao_grid(self.angulo)
        grid = self.cena.grid

        linha += dy
        coluna += dx
        while 0 <= linha < len(grid) and 0 <= coluna < len(grid[0]):
            if grid[linha][coluna] is not None:
                return True
            linha += dy
            coluna += dx

        return False

    def move_to_platform(self):
        for plataforma in self.cena.platforms:
            if not plataforma["ocupada"]:
                self.setPos(plataforma["item"].x(), plataforma["item"].y())
                plataforma["ocupada"] = True
                self.plataforma = plataforma
                self.cena.autocarros_estacionados.append(self)

                if self in self.cena.grid_posicoes:
                    linha, coluna = self.cena.grid_posicoes[self]
                    self.cena.grid[linha][coluna] = None
                    del self.cena.grid_posicoes[self]

                QTimer.singleShot(200, self.embarcar_passageiros)
                return

    def embarcar_passageiros(self):
        if self.capacidade <= 0:
            return

        passageiros = [p for p in self.cena.passageiros if not p["embarcado"] and p["item"].cor == self.cor]
        for passageiro in passageiros[:self.capacidade]:
            self.capacidade -= 1
            passageiro["embarcado"] = True
            self.animar_passageiro(passageiro)
            if self.capacidade == 0:
                QTimer.singleShot(600, self.partir)
                break

    def animar_passageiro(self, passageiro):
        destino = QPointF(self.x(), self.y())
        passageiro_item = passageiro["item"]
        timer = QTimer()

        def mover():
            pos_atual = passageiro_item.pos()
            passo = QPointF((destino.x() - pos_atual.x()) * 0.1,
                            (destino.y() - pos_atual.y()) * 0.1)
            nova_pos = pos_atual + passo
            passageiro_item.setPos(nova_pos)
            if (nova_pos - destino).manhattanLength() < 2:
                passageiro_item.setPos(destino)
                if passageiro_item.scene():
                    self.cena.scene.removeItem(passageiro_item)
                timer.stop()

        timer.timeout.connect(mover)
        timer.start(20)

    def partir(self):
        if self in self.cena.autocarros_estacionados:
            self.cena.autocarros_estacionados.remove(self)
        if self.plataforma:
            self.plataforma["ocupada"] = False
        if self.scene():
            self.scene().removeItem(self)
