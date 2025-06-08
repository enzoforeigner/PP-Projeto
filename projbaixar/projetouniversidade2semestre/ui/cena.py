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

        cores_finais = (
            ["yellow"] * 3 +  # 3 amarelos
            ["red"] * 4 +     # 4 vermelhos
            ["blue"] * 4      # 4 azuis
        )

        random.shuffle(cores_finais)  # Embaralha a ordem

        self.passageiros = []

        for i, cor in enumerate(cores_finais):
            posicao = i + 1
            x = 160 + (posicao - 1) * 30  # Define posição horizontal na fila
            passageiro = {
                "item": Passageiro(x, 500, cor),
                "embarcado": False,
                "posicao": posicao
            }
            self.passageiros.append(passageiro)
            self.scene.addItem(passageiro["item"])

        self.autocarro_parado = [
            {"item": Autocarro(50, 50, "red", self, 4, "direita")},  # Direção direita
            {"item": Autocarro(150, 50, "blue", self, 4, "cima")},  # Direção esquerda
            {"item": Autocarro(250, 50, "red", self, 4, "cima")},  # Direção para baixo
            {"item": Autocarro(250, 150, "blue", self, 4, "baixo")},  # Direção para cima
            {"item": Autocarro(350, 50, "yellow", self, 4, "direita")},  # Direção direita
            {"item": Autocarro(450, 50, "yellow", self, 4, "direita")},  # Direção esquerda
            {"item": Autocarro(60, 100, "red", self, 4, "baixo")},  # Direção para baixo
            {"item": Autocarro(150, 100, "blue", self, 4, "baixo")},  # Direção para cima
            {"item": Autocarro(250, 100, "red", self, 4, "direita")},  # Direção direita  
            {"item": Autocarro(360, 100, "blue", self, 4, "baixo")},  # Direção esquerda   
            {"item": Autocarro(450, 100, "yellow", self, 4, "baixo")},  # Direção para baixo
        ]

        for autocarro in self.autocarro_parado:
            self.scene.addItem(autocarro["item"])

    def add_tabuleiro(self):
        # Adiciona o tabuleiro à cena
        self.tabuleiro = Tabuleiro(600, 400)  # Largura e altura do tabuleiro
        self.tabuleiro.add_to_scene(self.scene)    


    def gerar_passageiro(self):
    # Filtra cores que ainda podem ter passageiros gerados
        cores_disponiveis = [
            cor for cor, qtd in self.contagem_cores.items() 
            if qtd < self.max_por_cor[cor]  # Verifica se ainda pode gerar dessa cor
        ]

        if not cores_disponiveis:
            return None  # Não gera mais passageiros

    # Escolhe aleatoriamente uma cor disponível
        nova_cor = random.choice(cores_disponiveis)

    # Cria o passageiro
        novo_passageiro = {
            "item": Passageiro(460, 500, nova_cor),
            "embarcado": False,
            "posicao": 11
        }

    # Atualiza a contagem
        self.contagem_cores[nova_cor] += 1

    # Adiciona à lista e à cena
        self.passageiros.append(novo_passageiro)
        self.scene.addItem(novo_passageiro["item"])


        return   # Retorna o passageiro criado (opcional)

       

