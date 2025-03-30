# cena.py
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene
from autocarro import Autocarro
from passageiro import Passageiro
from tabuleiro import Tabuleiro 
from plataforma import Plataforma
import random

class Cena(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setGeometry(100, 100, 800, 600)

        self.add_tabuleiro()

        self.autocarros_estacionados = []
        
         # Criando plataformas na parte superior do tabuleiro
        self.platforms = [
            {"item": Plataforma(50, 400, 100, 20, "lightblue", 1), "ocupada": False},
            {"item": Plataforma(200, 400, 100, 20, "lightblue", 2), "ocupada": False},
            {"item": Plataforma(350, 400, 100, 20, "lightblue", 3), "ocupada": False},
            {"item": Plataforma(500, 400, 100, 20, "lightblue", 4), "ocupada": False},
        ]

        for platform in self.platforms:
            self.scene.addItem(platform["item"])

        self.passageiros = [
            {"item": Passageiro(160, 500, "yellow"), "embarcado": False, "posicao": 1},
            {"item": Passageiro(190, 500, "yellow"), "embarcado": False, "posicao": 2},
            {"item": Passageiro(220, 500, "yellow"), "embarcado": False, "posicao": 3},
            {"item": Passageiro(250, 500, "red"), "embarcado": False, "posicao": 4},
            {"item": Passageiro(280, 500, "yellow"), "embarcado": False, "posicao": 5},
            {"item": Passageiro(310, 500, "red"), "embarcado": False, "posicao": 6},
            {"item": Passageiro(340, 500, "red"), "embarcado": False, "posicao": 7},
            {"item": Passageiro(370, 500, "red"), "embarcado": False, "posicao": 8},
            {"item": Passageiro(400, 500, "red"), "embarcado": False, "posicao": 9},
            {"item": Passageiro(430, 500, "blue"), "embarcado": False, "posicao": 10},
            {"item": Passageiro(460, 500, "yellow"), "embarcado": False, "posicao": 11},
        ]

        for passageiro in self.passageiros:
            self.scene.addItem(passageiro["item"])

        self.autocarro_parado = [
            {"item": Autocarro(50, 50, "red", self, 4, "direita")},  # Direção direita
            {"item": Autocarro(150, 50, "blue", self, 4, "esquerda")},  # Direção esquerda
            {"item": Autocarro(250, 50, "red", self, 4, "cima")},  # Direção para baixo
            {"item": Autocarro(250, 150, "blue", self, 4, "baixo")},  # Direção para cima
            {"item": Autocarro(350, 50, "yellow", self, 4, "direita")},  # Direção direita
            {"item": Autocarro(450, 50, "yellow", self, 4, "direita")},  # Direção esquerda
            {"item": Autocarro(50, 100, "red", self, 4, "baixo")},  # Direção para baixo
            {"item": Autocarro(150, 100, "blue", self, 4, "cima")},  # Direção para cima
            {"item": Autocarro(250, 100, "red", self, 4, "direita")},  # Direção direita  
            {"item": Autocarro(350, 100, "blue", self, 4, "esquerda")},  # Direção esquerda   
            {"item": Autocarro(450, 100, "yellow", self, 4, "baixo")},  # Direção para baixo
        ]

        for autocarro in self.autocarro_parado:
            self.scene.addItem(autocarro["item"])

    def add_tabuleiro(self):
        # Adiciona o tabuleiro à cena
        self.tabuleiro = Tabuleiro(600, 400)  # Largura e altura do tabuleiro
        self.tabuleiro.add_to_scene(self.scene)    

   

#Só falta os autocarros saírem em direção