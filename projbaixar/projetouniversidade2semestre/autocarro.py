  # autocarro.py
from PyQt6.QtWidgets import QGraphicsRectItem, QGraphicsPolygonItem, QMessageBox
from PyQt6.QtGui import QColor, QPolygonF, QBrush, QColor
from PyQt6.QtCore import Qt, QTimer, QPointF, QPropertyAnimation
from passageiro import Passageiro
from plataforma import Plataforma
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
            # Verifica se o autocarro está na mesma coluna e acima
                if self.direcao_saida == 'cima':
                    if (self.y() + self.rect().height() >= autocarro["item"].y() and
                        self.x() == autocarro["item"].x()):
                        return True
            
            # Verifica se o autocarro está na mesma coluna e abaixo
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
        plataforma_livre = False
    # Itera sobre a lista de plataformas para verificar se está ocupada
        for platform in self.cena.platforms:
            if not platform["ocupada"]:
                plataforma_livre = True
            # Move o autocarro para a posição da plataforma
                platform["ocupada"] = True  # Marca a plataforma como ocupada
                self.plataforma = platform  # Armazena a referência da plataforma ocupada
                self.cena.autocarros_estacionados.append(self)  # Adiciona o autocarro à lista de autocarros estacionados
                platform["item"].animar_autocarro(self)  # Anima o autocarro até a plataforma             
                break
        
        if not plataforma_livre:
        # Sem plataformas livres, verifica derrota
            self.verificar_derrota()
    
    

    def embarcar_passageiro(self):
        self.verificar_derrota()
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
                        autocarro_correto.animar_passageiro(passageiro)  # Anima o passageiro até a seta do autocarro
                        autocarro_correto.capacidade -= 1
                        passageiro["embarcado"] = True  

                        self.atualizar_posicoes()                        
                        self.verificar_vitoria()
                        self.cena.gerar_passageiro()

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

    # 🔴 Remove passageiros embarcados
        for passageiro in list(self.cena.passageiros):  # Cópia da lista para evitar conflitos
            if passageiro.get("embarcado"):
                item = passageiro["item"]
                if item.scene() is not None:
                    self.cena.scene.removeItem(item)
                self.cena.passageiros.remove(passageiro)  # Remove da lista principal

    # 🔴 Remove o autocarro da lista de estacionados
        if self in self.cena.autocarros_estacionados:
            self.cena.autocarros_estacionados.remove(self)

    # 🔴 Libera a plataforma
        if self.plataforma:
            self.plataforma["ocupada"] = False

    # 🔴 Remove o autocarro da cena
        if self.scene() is not None:
            self.cena.scene.removeItem(self)

    

        

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
                timer.stop()  # Para a animação
                

    # Conecta o timer à função de movimento e inicia
        timer.timeout.connect(mover)
        timer.start(20)  # Atualiza a posição a cada 20ms para suavizar o movimento

    




    def atualizar_posicoes(self):
        for passageiro in self.cena.passageiros:
            if not passageiro["embarcado"]:  
                passageiro["posicao"] -= 1  # Atualiza posição´
                if passageiro["posicao"] >= 1:
                    pos_atual = passageiro["item"].pos()
                    novo_x = pos_atual.x() - 30  # ou +30 se quiser mover para a direita
                    novo_y = pos_atual.y()       # mantém o mesmo Y
                    passageiro["item"].setPos(novo_x, novo_y)

                    
                
        
                

    def verificar_vitoria(self):
        """Exibe uma mensagem de vitória se todos os autocarros tiverem partido."""
    # Verifica se todos os autocarros já partiram
        todos_autocarros_partiram = len(self.cena.autocarros_estacionados) == 0

        if todos_autocarros_partiram:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Vitória!")
            msg.setText("Parabéns! Todos os autocarros completaram sua missão!")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()

    def verificar_derrota(self):
        """Exibe uma mensagem de derrota se todas as plataformas estiverem ocupadas."""
    # Verifica se todas as plataformas estão ocupadas
        todas_ocupadas = all(platform["ocupada"] for platform in self.cena.platforms)

        if todas_ocupadas:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Derrota!")
            msg.setText("Todas as plataformas estão ocupadas! Você perdeu!")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()

