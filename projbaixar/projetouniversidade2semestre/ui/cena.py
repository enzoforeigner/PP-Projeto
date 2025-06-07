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


        # Quatro plataformas no topo
        self.platforms = [
            {"item": Plataforma(100, 150, 80, 20, "lightblue", 1), "ocupada": False},
            {"item": Plataforma(200, 150, 80, 20, "lightblue", 2), "ocupada": False},
            {"item": Plataforma(300, 150, 80, 20, "lightblue", 3), "ocupada": False},
            {"item": Plataforma(400, 150, 80, 20, "lightblue", 4), "ocupada": False},
        ]


        for p in self.platforms:
            self.scene.addItem(p["item"])

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
