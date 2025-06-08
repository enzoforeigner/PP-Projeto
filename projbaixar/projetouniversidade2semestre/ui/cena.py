# cena.py
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt6.QtGui import QPixmap
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
    
        tabuleiro = Tabuleiro("imagens/tabuleiro.png")
        tabuleiro.add_to_scene(self.scene)

        self.max_por_cor = {
            "yellow": 13,
            "blue": 16,
            "red": 32,
            "green": 8  # Adicionando verde como cor adicional
        }
        self.contagem_cores = {
            "yellow": 0,
            "blue": 0,
            "red": 0,
            "green": 0  # Inicializando contagem para verde
        }
        self.autocarros_estacionados = []
        self.inicializar_plataformas()
        self.inicializar_passageiros()
        self.inicializar_autocarros()

    def inicializar_plataformas(self):    
         # Criando plataformas na parte superior do tabuleiro
        self.platforms = [
            {"item": Plataforma(10, 250, 80, 20, "lightblue", 1), "ocupada": False},
            {"item": Plataforma(150, 250, 80, 20, "lightblue", 2), "ocupada": False},
            {"item": Plataforma(290, 250, 80, 20, "lightblue", 3), "ocupada": False},
            {"item": Plataforma(430, 250, 80, 20, "lightblue", 4), "ocupada": False},
        ]

        for platform in self.platforms:
            self.scene.addItem(platform["item"])

    def inicializar_passageiros(self):
            cores_finais = (
                ["yellow"] * 3 +  # 3 amarelos
                ["red"] * 4 +     # 4 vermelhos
                ["blue"] * 4     # 4 azuis  # 4 verdes
            )

            random.shuffle(cores_finais)  # Embaralha a ordem

            self.passageiros = []

            for i, cor in enumerate(cores_finais):
                posicao = i + 1
                x = 10 + (posicao - 1) * 30  # Define posição horizontal na fila
                passageiro = {
                    "item": Passageiro(x, 170, cor),
                    "embarcado": False,
                    "posicao": posicao
                }
                self.passageiros.append(passageiro)
                self.scene.addItem(passageiro["item"])


    def inicializar_autocarros(self):
    # Remove autocarros antigos da cena (se existirem)
        if hasattr(self, "autocarro_parado"):
            for autocarro in self.autocarro_parado:
                self.scene.removeItem(autocarro["item"])

    # Define lista de autocarros com rotações personalizadas
        self.autocarro_parado = [
            {"item": Autocarro(50, 440, "red", self, 4, "cima_esquerda"), "rotacao": 315},
            {"item": Autocarro(170, 440, "blue", self, 4, "cima_esquerda"), "rotacao": 315},
            {"item": Autocarro(250, 440, "red", self, 4, "cima_direita"), "rotacao": 45},
            {"item": Autocarro(350, 440, "blue", self, 4, "cima_direita"), "rotacao": 45},
            {"item": Autocarro(450, 440, "yellow", self, 4, "cima_direita"), "rotacao": 45},
            {"item": Autocarro(80, 525, "red", self, 4, "cima_esquerda"), "rotacao": 315},
            {"item": Autocarro(180, 525, "green", self, 4, "cima_esquerda"), "rotacao": 315},
            {"item": Autocarro(280, 525, "red", self, 4, "cima_direita"), "rotacao": 45},
            {"item": Autocarro(380, 525, "blue", self, 4, "cima_direita"), "rotacao": 45},
            {"item": Autocarro(480, 525, "yellow", self, 4, "cima_direita"), "rotacao": 45},
            {"item": Autocarro(20, 600, "red", self, 4, "baixo_esquerda"), "rotacao": 225},
            {"item": Autocarro(120, 600, "blue", self, 4, "baixo_esquerda"), "rotacao": 225},
            {"item": Autocarro(220, 600, "red", self, 4, "baixo_direita"), "rotacao": 135},
            {"item": Autocarro(320, 600, "yellow", self, 4, "baixo_direita"), "rotacao": 135},
            {"item": Autocarro(420, 600, "red", self, 4, "baixo_direita"), "rotacao": 135},
            {"item": Autocarro(40, 700, "blue", self, 4, "baixo_esquerda"), "rotacao": 225},
            {"item": Autocarro(140, 700, "red", self, 4, "baixo_esquerda"), "rotacao": 225},
            {"item": Autocarro(240, 700, "green", self, 4, "baixo_direita"), "rotacao": 135},
            {"item": Autocarro(340, 700, "yellow", self, 4, "baixo_direita"), "rotacao": 135},
            {"item": Autocarro(440, 700, "red", self, 4, "baixo_direita"), "rotacao": 135},
        ]

        # Aplica rotação e adiciona à cena
        for autocarro_dict in self.autocarro_parado:
            autocarro = autocarro_dict["item"]
            rotacao = autocarro_dict.get("rotacao", 0)

            # Define ponto de rotação no centro do item
            autocarro.setTransformOriginPoint(autocarro.boundingRect().center())
            autocarro.setRotation(rotacao)

            self.scene.addItem(autocarro)




      


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
            "item": Passageiro(310, 170, nova_cor),
            "embarcado": False,
            "posicao": 11
        }

    # Atualiza a contagem
        self.contagem_cores[nova_cor] += 1

    # Adiciona à lista e à cena
        self.passageiros.append(novo_passageiro)
        self.scene.addItem(novo_passageiro["item"])


        return   # Retorna o passageiro criado (opcional)


       
    def reiniciar(self):
    # Limpa completamente a cena — remove todos os QGraphicsItems com segurança
        self.scene.clear()

    # Redefine contadores de passageiros por cor
        self.max_por_cor = {
        "yellow": 9,  # Suporte a até 3 amarelos × 3 passageiros
        "blue": 12,   # 4 autocarros × 3
        "red": 12     # 4 autocarros × 3
    }

        self.contagem_cores = {
        "yellow": 0,
        "blue": 0,
        "red": 0
    }

    # Limpa quaisquer estruturas de controle adicionais
        self.autocarros_estacionados = []
        self.autocarro_parado = []
        self.passageiros = []
        self.platforms = []

    # Recria todos os elementos do jogo
        tabuleiro = Tabuleiro("imagens/tabuleiro.png")
        tabuleiro.add_to_scene(self.scene)
        self.inicializar_plataformas()
        self.inicializar_autocarros()
        self.inicializar_passageiros()

    


