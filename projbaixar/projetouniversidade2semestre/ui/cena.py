# cena.py
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt6.QtGui import QPixmap
from autocarro import Autocarro
from passageiro import Passageiro
from tabuleiro import Tabuleiro 
from plataforma import Plataforma
import random

#Criação da classe Cena que herda de QGraphicsView
# Esta classe representa a cena do jogo, onde os autocarros, passageiros e plataformas são exibidos.
class Cena(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setGeometry(100, 100, 800, 600)
    
        tabuleiro = Tabuleiro("imagens/tabuleiro.png")
        tabuleiro.add_to_scene(self.scene)

        #variável de controle
        self.max_por_cor = {
        "red": 0,
        "blue": 0,
        "yellow": 0,
        "green": 0
        }  

        #variável de controle
        self.passageiros_atuais = {
            "red": 4,
            "blue": 4,
            "yellow": 3,
            "green": 0,
        }
        
        # Lista para armazenar autocarros estacionados
        self.autocarros_estacionados = []

        # Inicializa as plataformas, passageiros e autocarros
        self.inicializar_plataformas()
        self.inicializar_passageiros()
        self.inicializar_autocarros()

    # Função para Inicializa as plataformas
    def inicializar_plataformas(self):    
         
        self.platforms = [
            {"item": Plataforma(10, 290, 80, 20, "beige", 1), "ocupada": False},
            {"item": Plataforma(150, 290, 80, 20, "beige", 2), "ocupada": False},
            {"item": Plataforma(290, 290, 80, 20, "beige", 3), "ocupada": False},
            {"item": Plataforma(430, 290, 80, 20, "beige", 4), "ocupada": False},
        ]

        for platform in self.platforms:
            self.scene.addItem(platform["item"])
    
    # Função para Inicializar os passageiros
    def inicializar_passageiros(self):
            cores_finais = (
                ["yellow"] * 3 +  
                ["red"] * 4 +     
                ["blue"] * 4     
            )

            random.shuffle(cores_finais)  # Embaralha a ordem

            self.passageiros = [] # Lista para armazenar passageiros criados

            for i, cor in enumerate(cores_finais):
                posicao = i + 1
                x = 10 + (posicao - 1) * 30  
                passageiro = {
                    "item": Passageiro(x, 170, cor),
                    "embarcado": False,
                    "posicao": posicao
                }
                self.passageiros.append(passageiro)
                self.scene.addItem(passageiro["item"])



    # Função para Inicializar os autocarros
    def inicializar_autocarros(self):
        # Remove autocarros antigos da cena (se existirem)
        if hasattr(self, "autocarro_parado"):
            for autocarro in self.autocarro_parado:
                self.scene.removeItem(autocarro["item"])

        # Define o posicionamento dos autocarros em ângulos específicos
        ROTACOES_POR_DIRECAO = {
            "cima_direita": 45,
            "baixo_direita": 135,
            "baixo_esquerda": 225,
            "cima_esquerda": 315
        }

        # Define as posições dos autocarros e suas cores na cena
        posicoes = [
            (50, 440, "cima_esquerda"), (170, 460, "cima_esquerda"),
            (250, 440, "cima_direita"), (350, 440, "cima_direita"),
            (450, 440, "cima_direita"), (80, 525, "cima_esquerda"),
            (180, 525, "cima_esquerda"), (280, 525, "cima_direita"),
            (380, 525, "cima_direita"), (480, 525, "cima_direita"),
            (20, 600, "baixo_esquerda"), (120, 600, "baixo_esquerda"),
            (220, 600, "baixo_direita"), (320, 600, "baixo_direita"),
            (420, 600, "baixo_direita"), (40, 700, "baixo_esquerda"),
            (140, 700, "baixo_esquerda"), (240, 700, "baixo_direita"),
            (340, 700, "baixo_direita"), (440, 700, "baixo_direita"),
        ]

        # Define as cores possíveis e suas capacidades
        cores_possiveis = (
            ["yellow"] * 4 + ["red"] * 9 + ["blue"] * 5 + ["green"] * 2
        )
        random.shuffle(cores_possiveis)

        capacidades_por_cor = {
            "yellow": [4, 12],
            "red": [4, 8],
            "blue": [4, 6],
            "green": [4, 6],
        }

        # Inicializa a lista de autocarros e a capacidade total por cor
        self.autocarro_parado = []
        self.max_por_cor = {cor: 0 for cor in capacidades_por_cor}  # total por cor
        self.contagem_cores = {cor: 0 for cor in capacidades_por_cor}  # passageiros que estão a ser gerados com base nas necessidades

        # Cria os autocarros e adiciona à cena
        for i, (x, y, direcao) in enumerate(posicoes):
            cor = cores_possiveis[i % len(cores_possiveis)]
            capacidade = random.choice(capacidades_por_cor[cor])
            rotacao = ROTACOES_POR_DIRECAO.get(direcao, 0)

            autocarro = Autocarro(x, y, cor, self, capacidade, direcao)
            autocarro.setTransformOriginPoint(autocarro.boundingRect().center())
            autocarro.setRotation(rotacao)

            self.scene.addItem(autocarro)
            self.autocarro_parado.append({"item": autocarro})

            
            self.max_por_cor[cor] += capacidade

        # Calcula o restante de vagas por cor
        self.restante_por_cor = {
            cor: self.max_por_cor.get(cor, 0) - self.passageiros_atuais.get(cor, 0)
            for cor in self.max_por_cor
        }


    # Função para gerar um novo passageiro se houver vagas por preencher
    def gerar_passageiro(self):
        
        
        cores_disponiveis = [
            cor for cor in self.restante_por_cor
            if self.contagem_cores.get(cor, 0) < self.restante_por_cor.get(cor, 0) # Verifica se ainda há vagas disponíveis para passageiros
        ]

        if not cores_disponiveis:
            return None  

        
        nova_cor = random.choice(cores_disponiveis) # Escolhe aleatoriamente uma cor disponível

        
        novo_passageiro = {
            "item": Passageiro(310, 170, nova_cor), # Cria o passageiro
            "embarcado": False,
            "posicao": 11
        }

        
        self.contagem_cores[nova_cor] += 1 # Cria o passageiro

        
        self.passageiros.append(novo_passageiro)
        self.scene.addItem(novo_passageiro["item"])      
        return novo_passageiro

    
    # Função para reiniciar a cena, limpando todos os itens e reinicializando o estado do jogo      
    def reiniciar(self):
    
        self.scene.clear()

    
        self.max_por_cor = {
        "yellow": 0,  
        "blue": 0,                  # Redefine as nossa variável de controle
        "red": 0,
        "green": 0     
    }

        self.contagem_cores = {
        "yellow": 0,                   # Redefine as nossa variável de controle
        "blue": 0,
        "red": 0
    }

    
        self.autocarros_estacionados = []
        self.autocarro_parado = []
        self.passageiros = []                   # Limpa quaisquer estruturas de controle adicionais
        self.platforms = []

    
        tabuleiro = Tabuleiro("imagens/tabuleiro.png")
        tabuleiro.add_to_scene(self.scene)
        self.inicializar_plataformas()
        self.inicializar_autocarros()                   # Recria todos os elementos do jogo
        self.inicializar_passageiros()

    


