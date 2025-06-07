from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene
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


                        # Coordenadas ajustadas para alinhar com os 4 slots cinza no topo
        slots = [
            (70, 250),  # Slot 1 (mais à esquerda)
            (160, 250),  # Slot 2
            (250, 250),  # Slot 3
            (340, 250),  # Slot 4 (mais à direita)
        ]

        largura_slot = 60
        altura_slot = 100  # ou 90 se quiser mais justo

        self.platforms = []
        for i, (x, y) in enumerate(slots):
            plataforma = Plataforma(x, y, largura_slot, altura_slot, "transparent", i)
            self.scene.addItem(plataforma)
            self.platforms.append({
                "item": plataforma,
                "ocupada": False,
                "posicao": i
            })

        self.passageiros = []
        cores = ["red", "blue", "yellow", "green"]
        for i in range(8):
            cor = random.choice(cores)
            p = {"item": Passageiro(160 + i * 30, 100, cor), "embarcado": False}
            self.passageiros.append(p)
            self.scene.addItem(p["item"])

        self.autocarro_parado = []
        angulos = [45, 135, 225, 315]
        x0, y0 = 120, 480
        espaco_x, espaco_y = 90, 70

        for linha in range(4):
            for coluna in range(4):
                if self.grid[linha][coluna] is None:
                    x = x0 + coluna * espaco_x
                    y = y0 + linha * espaco_y + coluna * 10
                    cor = random.choice(cores)
                    angulo = random.choice(angulos)
                    carro = Autocarro(x, y, cor, self, 4, angulo)
                    self.grid[linha][coluna] = carro
                    self.grid_posicoes[carro] = (linha, coluna)
                    self.autocarro_parado.append({"item": carro})
                    self.scene.addItem(carro)

    def add_tabuleiro(self):
        self.tabuleiro = Tabuleiro("background.png")
        self.tabuleiro.add_to_scene(self.scene)
