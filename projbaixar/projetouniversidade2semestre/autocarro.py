from PyQt6.QtWidgets import QGraphicsPixmapItem, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer, QPointF
from passageiro import Passageiro
import random
import os

class Autocarro(QGraphicsPixmapItem):
    def __init__(self, x, y, cor, cena, capacidade, angulo=135):
        super().__init__()
        self.setPos(x, y)
        self.cor = cor
        self.cena = cena
        self.capacidade = capacidade
        self.plataforma = None

        # 🧭 Converte string de direção para ângulo se necessário
        if isinstance(angulo, str):
            direcoes_para_angulo = {
                "cima": 0,
                "direita": 90,
                "baixo": 180,
                "esquerda": 270
            }
            angulo = direcoes_para_angulo.get(angulo, 135)  # padrão 135° (diagonal)

        # 📁 Caminhos das imagens por cor
        caminhos = {
            "blue": "carro_azul.png",
            "red": "carro_vermelho.png",
            "yellow": "carro_amarelo.png"
        }
        caminho_img = caminhos.get(cor, "carro_azul.png")

        # 🖼️ Carregamento do carro
        pixmap = QPixmap(caminho_img)
        if pixmap.isNull():
            print(f"❌ Erro ao carregar imagem: {caminho_img}")
            return

        pixmap = pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio)
        self.setPixmap(pixmap)

        # 🌀 Rotaciona estilo isométrico
        self.setTransformOriginPoint(pixmap.width() / 2, pixmap.height() / 2)
        self.setRotation(angulo)

        # ⬆️ Adiciona seta branca por cima
        seta_pixmap = QPixmap("seta_branca.png")
        if not seta_pixmap.isNull():
            seta_pixmap = seta_pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio)
            self.seta = QGraphicsPixmapItem(seta_pixmap, self)
            self.seta.setOffset((pixmap.width() - seta_pixmap.width()) / 2,
                                (pixmap.height() - seta_pixmap.height()) / 2)

    def mousePressEvent(self, event):
        if not self.verificar_bloqueio():
            self.move_to_platform()
        else:
            print("❌ Não é possível mover: há um autocarro bloqueando!")

    def verificar_bloqueio(self):
        for autocarro in self.cena.autocarro_parado:
            if self != autocarro["item"]:
                if abs(self.x() - autocarro["item"].x()) < 10 and abs(self.y() - autocarro["item"].y()) < 10:
                    return True
        return False

    def move_to_platform(self):
        for platform in self.cena.platforms:
            if not platform["ocupada"]:
                platform_y = 400
                platform_x = platform["item"].x()
                self.setPos(platform_x, platform_y - self.pixmap().height())
                platform["ocupada"] = True
                self.plataforma = platform
                self.cena.autocarros_estacionados.append(self)
                self.embarcar_passageiro()
                break

    def embarcar_passageiro(self):
        if self.capacidade > 0 and self.cena.passageiros:
            for passageiro in list(self.cena.passageiros):
                if not passageiro["embarcado"]:
                    autocarro_correto = None
                    for autocarro in self.cena.autocarros_estacionados:
                        if passageiro["item"].cor == autocarro.cor and autocarro.capacidade > 0:
                            autocarro_correto = autocarro
                            break
                    if autocarro_correto and passageiro["posicao"] == 1:
                        autocarro_correto.animar_passageiro(passageiro)
                        autocarro_correto.capacidade -= 1
                        passageiro["embarcado"] = True
                        self.atualizar_posicoes()
                        self.verificar_vitoria()
                        if autocarro_correto.capacidade > 0:
                            autocarro_correto.verificar_proximo_passageiro()
                        else:
                            QTimer.singleShot(500, autocarro_correto.partir)
                            autocarro_correto.verificar_proximo_passageiro()
                        return

    def verificar_proximo_passageiro(self):
        for passageiro in self.cena.passageiros:
            if not passageiro["embarcado"]:
                for autocarro in self.cena.autocarros_estacionados:
                    if (passageiro["item"].cor == autocarro.cor and
                        passageiro["posicao"] == 1 and
                        autocarro.capacidade > 0):
                        autocarro.embarcar_passageiro()
                        return

    def partir(self):
        if self in self.cena.autocarros_estacionados:
            self.cena.autocarros_estacionados.remove(self)
        if self.plataforma:
            self.plataforma["ocupada"] = False
        if self.scene() is not None:
            self.cena.scene.removeItem(self)

    def gerar_passageiro(self):
        cores = ["yellow", "blue", "red"]
        nova_cor = random.choice(cores)
        novo_passageiro = {"item": Passageiro(160, 500, nova_cor), "embarcado": False}
        self.cena.passageiros.append(novo_passageiro)
        self.cena.scene.addItem(novo_passageiro["item"])
        self.embarcar_passageiro()

    def animar_passageiro(self, passageiro):
        passageiro_item = passageiro["item"]
        destino = QPointF(self.x(), self.y())
        timer = QTimer()

        def mover():
            pos_atual = passageiro_item.pos()
            step_x = (destino.x() - pos_atual.x()) * 0.1
            step_y = (destino.y() - pos_atual.y()) * 0.1
            nova_posicao = QPointF(pos_atual.x() + step_x, pos_atual.y() + step_y)
            passageiro_item.setPos(nova_posicao)
            if abs(nova_posicao.x() - destino.x()) < 2 and abs(nova_posicao.y() - destino.y()) < 2:
                passageiro_item.setPos(destino)
                passageiro["embarcado"] = True
                timer.stop()

        timer.timeout.connect(mover)
        timer.start(20)

    def atualizar_posicoes(self):
        passageiros_restantes = []
        for passageiro in self.cena.passageiros:
            if not passageiro["embarcado"]:
                passageiro["posicao"] -= 1
                passageiros_restantes.append(passageiro)
            else:
                if passageiro["item"].scene() is not None:
                    self.cena.scene.removeItem(passageiro["item"])
        self.cena.passageiros = passageiros_restantes

    def verificar_vitoria(self):
        if not self.cena.passageiros:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Vitória!")
            msg.setText("Parabéns! Todos os passageiros foram transportados!")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
