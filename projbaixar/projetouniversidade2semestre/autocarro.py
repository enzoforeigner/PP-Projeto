from PyQt6.QtWidgets import QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer, QPointF
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
    def __init__(self, x, y, cor, cena, capacidade=4, direcao_saida="cima_direita"):
        super().__init__()
        self.setPos(x, y)
        self.cor = cor
        self.cena = cena
        self.capacidade = capacidade
        self.embarcados = 0
        self.direcao_saida = direcao_saida
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

        # Rotação conforme direção
        direcao_para_angulo = {
            "cima_direita": 315,
            "cima_esquerda": 45,
            "baixo_direita": 225,
            "baixo_esquerda": 135
        }
        angulo = direcao_para_angulo.get(direcao_saida, 0)

        pixmap = pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio)
        self.setPixmap(pixmap)
        self.setTransformOriginPoint(pixmap.width() / 2, pixmap.height() / 2)
        self.setRotation(angulo)

        # Seta no meio do carro
        seta = QPixmap("seta_branca.png")
        if not seta.isNull():
            seta = seta.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio)
            self.seta = QGraphicsPixmapItem(seta, self)
            self.seta.setOffset((pixmap.width() - seta.width()) / 2,
                                (pixmap.height() - seta.height()) / 2)
            self.seta.setRotation(0)

    def mousePressEvent(self, event):
        if not self.verificar_bloqueio():
            self.move_to_platform()
        else:
            print("❌ Caminho bloqueado para frente.")

    def verificar_bloqueio(self) -> bool:
        """
        Verifica se há outro carro na célula à frente na direção atual usando o grid.
        """
        if self not in self.cena.grid_posicoes:
            return False  # Já saiu do grid

        direcoes_para_offset = {
            "cima_direita": (1, -1),
            "cima_esquerda": (-1, -1),
            "baixo_direita": (1, 1),
            "baixo_esquerda": (-1, 1)
        }

        dx, dy = direcoes_para_offset.get(self.direcao_saida, (0, 0))

        linha_atual, coluna_atual = self.cena.grid_posicoes[self]
        nova_linha = linha_atual + dy
        nova_coluna = coluna_atual + dx

        # Verifica se está dentro dos limites do grid
        if 0 <= nova_linha < 4 and 0 <= nova_coluna < 4:
            if self.cena.grid[nova_linha][nova_coluna] is not None:
                print("🟥 Caminho bloqueado por carro no grid.")
                return True

        return False


    def move_to_platform(self):
        for plataforma in self.cena.platforms:
            if not plataforma["ocupada"]:
                self.setPos(plataforma["item"].x(), plataforma["item"].y())

                # Mantém rotação original
                self.setRotation(self.rotation())

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
        passageiros_ordenados = sorted(
            [p for p in self.cena.passageiros if not p["embarcado"]],
            key=lambda p: p["posicao"]
        )

        for passageiro in passageiros_ordenados:
            if passageiro["item"].cor == self.cor:
                self.embarcados += 1
                passageiro["embarcado"] = True
                self.animar_passageiro(passageiro)
                self.cena.gerar_passageiro()

                if self.embarcados >= self.capacidade:
                    break
            else:
                break  # Bloqueia a fila se o da frente não for da mesma cor

        # Só parte se estiver cheio
        if self.embarcados >= self.capacidade:
            QTimer.singleShot(600, self.partir)


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
                self.cena.reorganizar_fila()

        timer.timeout.connect(mover)
        timer.start(20)

    def partir(self):
        if self.verificar_bloqueio():
            print("🟥 Caminho bloqueado. Não pode partir ainda.")
            QTimer.singleShot(1000, self.partir)
            return

        if self in self.cena.autocarros_estacionados:
            self.cena.autocarros_estacionados.remove(self)
        if self in self.cena.autocarro_parado:
            self.cena.autocarro_parado.remove(self)

        if self.plataforma:
            self.plataforma["ocupada"] = False

        if self.scene():
            self.scene().removeItem(self)

        print(f"🟢 Autocarro {self.cor} partiu com {self.embarcados} passageiros.")


