  # autocarro.py
from PyQt6.QtWidgets import QGraphicsRectItem
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt, QTimer, QPointF, QPropertyAnimation
from passageiro import Passageiro
import random
from time import sleep

class Autocarro(QGraphicsRectItem):
    def __init__(self, x, y, cor, cena, capacidade, direcao_x=1, direcao_y=0):
        super().__init__(0, 0, 80, 40)  # Largura x Altura do autocarro
        self.setPos(x, y)   # Posição inicial do autocarro
        self.setBrush(QColor(cor))  # Define a cor do autocarro
        self.cor = cor # Cor do autocarro
        self.cena = cena  # Referência à cena para saber onde mover
        self.capacidade = capacidade  # Capacidade máxima de passageiros 
        self.direcao_x = direcao_x  # Direção no eixo X
        self.direcao_y = direcao_y  # Direção no eixo Y 
        self.plataforma = None  # Atributo para armazenar a plataforma ocupada

    def verificar_obstaculos(self):
        """Verifica se há um bloqueio na direção do movimento do autocarro."""
        for autocarro in self.cena.autocarro_parado:  # Itera sobre os autocarros na cena
            if autocarro != self:  # Ignora o próprio autocarro
            # Verificação de bloqueio para direção X (esquerda/direita)
                if self.direcao_x > 0:  # Direção para a direita
                    if (self.x() + 100 > autocarro["item"].x()):
                        return True  # Bloqueio à direita

                elif self.direcao_x < 0:  # Direção para a esquerda
                    if (autocarro["item"].x() >= self.x() - 100):
                        return True  # Bloqueio à esquerda

            # Verificação de bloqueio para direção Y (cima/baixo)
                elif self.direcao_y > 0:  # Direção para baixo
                    if (self.y() + 50 >= autocarro["item"].y()):
                        return True  # Bloqueio para baixo

                elif self.direcao_y < 0:  # Direção para cima
                    if (autocarro["item"].y() > self.y() - 50):
                        return True  # Bloqueio para cima

        return False  # Nenhum bloqueio encontrado
     

    def mousePressEvent(self, event):
        # Move o autocarro para cima da plataforma
        if not self.verificar_obstaculos():
            self.move_to_platform()
        else:
            print("Não é possível mover: há um autocarro bloqueando!")

    def move_to_platform(self):
    # Itera sobre a lista de plataformas para verificar se está ocupada
        for platform in self.cena.platforms:
            if not platform["ocupada"]:
            # Move o autocarro para a posição da plataforma
                platform_y = 400  # Altura das plataforma
                platform_x = platform["item"].x()  # Posição x da plataforma
                self.setPos(platform_x, platform_y - self.rect().height())  # Move o autocarro acima da plataforma
                platform["ocupada"] = True  # Marca a plataforma como ocupada
                self.plataforma = platform  # Armazena a referência da plataforma ocupada
                self.cena.autocarros_estacionados.append(self)  # Adiciona o autocarro à lista de autocarros estacionados
                self.embarcar_passageiro()  # Embarca um passageiro
                break
    
    

    def embarcar_passageiro(self):
        if self.capacidade > 0 and self.cena.passageiros:
            for passageiro in list(self.cena.passageiros):  # Evita erro ao remover da lista
                if not passageiro["embarcado"]: 
                # Procuramos um autocarro específico para esse passageiro
                    autocarro_correto = None
                    for autocarro in self.cena.autocarros_estacionados:
                        if passageiro["item"].cor == autocarro.cor and autocarro.capacidade > 0:
                            autocarro_correto = autocarro
                            break  # Para assim que encontrar um autocarro válido

                    if autocarro_correto and passageiro["posicao"] == 1:
                        autocarro_correto.animar_passageiro(passageiro)
                        autocarro_correto.capacidade -= 1
                        passageiro["embarcado"] = True
                        passageiro["posicao"] = 0
                        self.atualizar_posicoes()

                    # 🔴 Se ainda há capacidade, verifica o próximo passageiro
                        if autocarro_correto.capacidade > 0:
                            autocarro_correto.verificar_proximo_passageiro()
                        else:
                        # 🔴 Se o autocarro está cheio, esperar um pouco antes de partir
                            QTimer.singleShot(500, autocarro_correto.partir)  # Espera 0.5s antes de partir
                        return  # Sai da função após embarcar um passageiro


    def verificar_proximo_passageiro(self):
        for passageiro in self.cena.passageiros:
            if not passageiro["embarcado"]:
                for autocarro in self.cena.autocarros_estacionados:
                    if (
                        passageiro["item"].cor == autocarro.cor
                        and passageiro["posicao"] == 1
                        and autocarro.capacidade > 0
                    ):
                        autocarro.embarcar_passageiro()  # Agora chamamos a função no autocarro correto!
                        return  # Para a verificação ao encontrar um autocarro válido

                        
    def partir(self):
        """Remove o autocarro e os passageiros embarcados da cena."""
    
    # Criar uma cópia da lista para evitar problemas ao remover elementos enquanto iteramos
        passageiros_embarcados = [
            passageiro for passageiro in list(self.cena.passageiros) if passageiro["embarcado"] 
        ]

    # Remove os passageiros da cena primeiro, se ainda estiverem nela
        for passageiro in passageiros_embarcados:
            if passageiro["item"].scene() is not None:  # Verifica se ainda está na cena
                self.cena.scene.removeItem(passageiro["item"])  # Remove o passageiro da cena
            self.cena.passageiros.remove(passageiro)  # Remove da lista de passageiros

    # Agora, remove o autocarro da cena se ele ainda estiver lá
        if self in self.cena.autocarros_estacionados:
            self.cena.autocarros_estacionados.remove(self)

        if self.plataforma:  # Verifica se o autocarro está estacionado em alguma plataforma
            self.plataforma["ocupada"] = False  # Libera a plataforma

        if self.scene() is not None:  # Verifica se o autocarro ainda está na cena
            self.cena.scene.removeItem(self)  



       


    
    def gerar_passageiro(self):
        cores = ["yellow", "blue", "red", "purple"] # Cores disponíveis para os passageiros
        nova_cor = random.choice(cores) # Escolhe uma cor aleatória
        novo_passageiro = {"item": Passageiro(160, 500, nova_cor), "embarcado": False} # Cria um novo passageiro
        self.cena.passageiros.append(novo_passageiro) # Adiciona o passageiro à lista de passageiros
        self.cena.scene.addItem(novo_passageiro["item"])  # Adiciona o passageiro à cena
        self.embarcar_passageiro()

    def animar_passageiro(self, passageiro):
        passageiro_item = passageiro["item"]
        destino = QPointF(self.x(), self.y())  # Posição do autocarro

    # Criamos um timer para animar o passageiro
        timer = QTimer()
    
        def mover():
            # Obtém a posição atual
            pos_atual = passageiro_item.pos()
        
        # Calcula o próximo passo (movimento gradual)
            step_x = (destino.x() - pos_atual.x()) * 0.1  # 10% do caminho a cada atualização
            step_y = (destino.y() - pos_atual.y()) * 0.1  
        
        # Move o passageiro suavemente
            nova_posicao = QPointF(pos_atual.x() + step_x, pos_atual.y() + step_y)
            passageiro_item.setPos(nova_posicao)
        
        # Verifica se o passageiro chegou ao destino (margem de erro < 2 pixels)
            if abs(nova_posicao.x() - destino.x()) < 2 and abs(nova_posicao.y() - destino.y()) < 2:
                passageiro_item.setPos(destino)  # Garante que fique exatamente no destino
                passageiro["embarcado"] = True
                timer.stop()  # Para a animação

    # Conecta o timer à função de movimento e inicia
        timer.timeout.connect(mover)
        timer.start(20)  # Atualiza a posição a cada 20ms para suavizar o movimento


    def atualizar_posicoes(self):
        for passageiro in self.cena.passageiros:
            if not passageiro["embarcado"]:
            # Atualiza a posição do passageiro
                passageiro["posicao"] -= 1  # O passageiro que está atrás ganha a posição4