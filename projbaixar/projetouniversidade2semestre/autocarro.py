  # autocarro.py
from PyQt6.QtWidgets import QGraphicsRectItem, QGraphicsPolygonItem, QMessageBox
from PyQt6.QtGui import QColor, QPolygonF, QBrush, QColor
from PyQt6.QtCore import Qt, QTimer, QPointF, QPropertyAnimation
from passageiro import Passageiro
import random
from time import sleep

class Autocarro(QGraphicsRectItem):
    def __init__(self, x, y, cor, cena, capacidade, direcao_saida):
        super().__init__(0, 0, 80, 40)  # Largura x Altura do autocarro
        self.setPos(x, y)   # Posição inicial do autocarro
        self.setBrush(QColor(cor))  # Define a cor do autocarro
        self.cor = cor # Cor do autocarro
        self.cena = cena  # Referência à cena para saber onde mover
        self.capacidade = capacidade  # Capacidade máxima de passageiros 
        self.direcao_saida = direcao_saida  # Direção de saída
        self.plataforma = None  # Atributo para armazenar a plataforma ocupada
        self.seta = QGraphicsPolygonItem(self)
        self.atualizar_seta()

    def atualizar_seta(self):
        """Atualiza a direção da seta com base na direção do autocarro"""
        largura = self.rect().width()
        altura = self.rect().height()

        # Centro do autocarro
        cx, cy = largura / 2, altura / 2

        # Criar pontos para formar um triângulo (seta)
        if self.direcao_saida == 'direita':   # Direita →
            pontos = [QPointF(cx - 10, cy - 10), QPointF(cx + 10, cy), QPointF(cx - 10, cy + 10)]
        elif self.direcao_saida == 'esquerda':   # Esquerda ←
            pontos = [QPointF(cx + 10, cy - 10), QPointF(cx - 10, cy), QPointF(cx + 10, cy + 10)]
        elif self.direcao_saida == 'baixo':  # Baixo ↓
            pontos = [QPointF(cx - 10, cy - 10), QPointF(cx, cy + 10), QPointF(cx + 10, cy - 10)]
        elif self.direcao_saida == 'cima':  # Cima ↑
            pontos = [QPointF(cx - 10, cy + 10), QPointF(cx, cy - 10), QPointF(cx + 10, cy + 10)]
        else:
            return  # Sem direção

        self.seta.setPolygon(QPolygonF(pontos))
        self.seta.setBrush(QBrush(QColor("black")))  # Cor da seta

    def verificar_bloqueio(self):
        for autocarro in self.cena.autocarro_parado:
            if self != autocarro["item"]:  # Não verificar o próprio autocarro
            # Verifica se o autocarro está na mesma coluna e abaixo
                if self.direcao_saida == 'cima':
                    if (self.y() + self.rect().height() >= autocarro["item"].y() and
                        self.x() == autocarro["item"].x()):
                        return True
            
            # Verifica se o autocarro está na mesma coluna e acima
                elif self.direcao_saida == 'baixo':
                    if (self.y() <= autocarro["item"].y() + autocarro["item"].rect().height() and
                        self.x() == autocarro["item"].x()):
                        return True
            
            # Verifica se o autocarro está na mesma linha e à direita
                elif self.direcao_saida == 'esquerda': 
                    if (self.x() + self.rect().width() >= autocarro["item"].x() and
                        autocarro["item"].y() == self.y()):
                        return True
            
            # Verifica se o autocarro está na mesma linha e à esquerda
                elif self.direcao_saida == 'direita':
                    if (self.x() <= autocarro["item"].x() + autocarro["item"].rect().width() and
                        autocarro["item"].y() == self.y()):
                        return True
        return False


     

    def mousePressEvent(self, event):
        # Move o autocarro para cima da plataforma
        if not self.verificar_bloqueio():
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

                        self.atualizar_posicoes()
                        self.verificar_vitoria()

                    # 🔴 Se ainda há capacidade, verifica o próximo passageiro
                        if autocarro_correto.capacidade > 0:
                            autocarro_correto.verificar_proximo_passageiro()
                        else:
                        # 🔴 Se o autocarro está cheio, esperar um pouco antes de partir
                            QTimer.singleShot(500, autocarro_correto.partir)  # Espera 0.5s antes de partir
                            autocarro_correto.verificar_proximo_passageiro()
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

    def animar_passageiro(self, passageiro, destino):
        passageiro_item = passageiro["item"]
        

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
                timer.stop()  # Para a animação

    # Conecta o timer à função de movimento e inicia
        timer.timeout.connect(mover)
        timer.start(20)  # Atualiza a posição a cada 20ms para suavizar o movimento


    def atualizar_posicoes(self):
        passageiros_restantes = []  # Nova lista para armazenar os passageiros que ainda não embarcaram

        for passageiro in self.cena.passageiros:
            if not passageiro["embarcado"]:  
                passageiro["posicao"] -= 1  # Atualiza posição
                passageiros_restantes.append(passageiro)  # Mantém apenas os não embarcados
            else:
                 if passageiro["item"].scene() is not None:  # Verifica se ainda está na cena
                    self.cena.scene.removeItem(passageiro["item"])  # Remove o passageiro da cena
                

        # Atualiza a lista de passageiros removendo os já embarcados
            self.cena.passageiros = passageiros_restantes
        
                

    def verificar_vitoria(self):
        """Exibe uma mensagem de vitória se todos os passageiros forem transportados."""
        if not self.cena.passageiros:  # Se não houver mais passageiros na cena
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Information)  # Correto para PyQt6
            msg.setWindowTitle("Vitória!")
            msg.setText("Parabéns! Todos os passageiros foram transportados!")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)  # PyQt6 requer StandardButton
            msg.exec()  # PyQt6 usa exec(), não exec_()            