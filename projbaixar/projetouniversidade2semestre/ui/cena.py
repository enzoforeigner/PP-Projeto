# cena.py
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt6.QtCore import QTimer, QPointF
from autocarro import Autocarro
from passageiro import Passageiro
from tabuleiro import Tabuleiro
from plataforma import Plataforma
import random

class Cena(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.grid = [[None for _ in range(4)] for _ in range(4)]
        self.grid_posicoes = {}

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setGeometry(100, 100, 800, 600)
        self.add_tabuleiro()

        self.autocarros_estacionados = []

        self.max_por_cor = {
            "yellow": 9,
            "blue": 12,
            "red": 12
        }
        self.contagem_cores = {
            "yellow": 0,
            "blue": 0,
            "red": 0
        }

        slots = [
            (80, 250),
            (190, 250),
            (270, 250),
            (360, 250),
        ]

        largura_slot = 60
        altura_slot = 100

        self.platforms = []
        for i, (x, y) in enumerate(slots):
            plataforma = Plataforma(x, y, largura_slot, altura_slot, "transparent", i)
            self.scene.addItem(plataforma)
            self.platforms.append({
                "item": plataforma,
                "ocupada": False,
                "posicao": i
            })

        self.coordenadas_L = [
            (70, 210), (93, 210), (116, 210), (139, 210),
            (162, 210), (185, 210), (208, 210), (230, 210),
            (250, 210), (270, 210), (270, 175), (270, 140)
        ]

        self.passageiros = []
        cores = ["red", "blue", "yellow"]

        for i, (x, y) in enumerate(self.coordenadas_L):
            cor = random.choice(cores)
            passageiro = {
                "item": Passageiro(x, y, cor),
                "embarcado": False,
                "posicao": i
            }
            self.passageiros.append(passageiro)
            self.scene.addItem(passageiro["item"])
            if cor in self.contagem_cores:
                self.contagem_cores[cor] += 1

        self.autocarro_parado = []
        direcoes = ["cima_direita", "cima_esquerda", "baixo_direita", "baixo_esquerda"]

        x0, y0 = 100, 480
        espaco_x, espaco_y = 90, 70

        for linha in range(4):
            for coluna in range(4):
                if self.grid[linha][coluna] is None:
                    x = x0 + coluna * espaco_x
                    y = y0 + linha * espaco_y + coluna * 10
                    cor = random.choice(cores)
                    direcao = random.choice(direcoes)

                    carro = Autocarro(x, y, cor, self, 4, direcao)

                    self.grid[linha][coluna] = carro
                    self.grid_posicoes[carro] = (linha, coluna)
                    self.autocarro_parado.append(carro)
                    self.scene.addItem(carro)

    def add_tabuleiro(self):
        self.tabuleiro = Tabuleiro("background.png")
        self.tabuleiro.add_to_scene(self.scene)

    def angulo_para_direcao(self, angulo):
        if angulo == 45:
            return "cima_direita"
        elif angulo == 135:
            return "cima_esquerda"
        elif angulo == 225:
            return "baixo_esquerda"
        elif angulo == 315:
            return "baixo_direita"
        return "baixo"

    def gerar_passageiro(self, cor_especifica=None):
        # Verifica quantos ainda não embarcaram
        fila = [p for p in self.passageiros if not p["embarcado"]]
        if len(fila) >= 12:
            return

        # Define quais cores ainda podem ser geradas
        cores_disponiveis = [
            cor for cor, qtd in self.contagem_cores.items()
            if qtd < self.max_por_cor[cor]
        ]

        # Se uma cor foi pedida, verifica se ainda pode gerar
        if cor_especifica:
            if cor_especifica not in cores_disponiveis:
                print(f"⚠️ Cor {cor_especifica} atingiu o limite.")
                return
            nova_cor = cor_especifica
        else:
            if not cores_disponiveis:
                return
            nova_cor = random.choice(cores_disponiveis)

        # Define a próxima posição na fila (posição lógica + coordenada)
        nova_posicao = len(fila)
        if nova_posicao >= len(self.coordenadas_L):
            print("⚠️ Fila cheia.")
            return

        x, y = self.coordenadas_L[nova_posicao]

        passageiro = {
            "item": Passageiro(x, y, nova_cor),
            "embarcado": False,
            "posicao": nova_posicao
        }

        # Adiciona à lista, incrementa contagem, coloca na cena
        self.passageiros.append(passageiro)
        self.contagem_cores[nova_cor] += 1
        self.scene.addItem(passageiro["item"])

        # Verifica se pode embarcar automaticamente
        self.verificar_autocarros_para_embarcar()


    def reorganizar_fila(self):
        self.passageiros = [p for p in self.passageiros if not p["embarcado"]]
        passageiros_ativos = self.passageiros

        for nova_posicao, passageiro in enumerate(passageiros_ativos):
            if passageiro["posicao"] != nova_posicao:
                passageiro["posicao"] = nova_posicao
                x, y = self.coordenadas_L[nova_posicao]
                self.animar_passageiro_para(passageiro["item"], x, y)

    def animar_passageiro_para(self, item, x_destino, y_destino):
        destino = QPointF(x_destino, y_destino)
        timer = QTimer()

        def mover():
            pos_atual = item.pos()
            passo = QPointF((destino.x() - pos_atual.x()) * 0.2,
                            (destino.y() - pos_atual.y()) * 0.2)
            nova_pos = pos_atual + passo
            item.setPos(nova_pos)
            if (nova_pos - destino).manhattanLength() < 1:
                item.setPos(destino)
                timer.stop()

        timer.timeout.connect(mover)
        timer.start(20)

    def verificar_autocarros_para_embarcar(self):
        passageiros_ordenados = sorted(
            [p for p in self.passageiros if not p["embarcado"]],
            key=lambda p: p["posicao"]
        )

        if not passageiros_ordenados:
            return

        passageiro_da_frente = passageiros_ordenados[0]

        for autocarro in self.autocarros_estacionados:
            carro = autocarro
            if carro.embarcados < carro.capacidade and carro.cor == passageiro_da_frente["item"].cor:
                carro.embarcar_passageiros()
                break  # Apenas um carro embarca de cada vez
