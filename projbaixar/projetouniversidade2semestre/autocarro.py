  # autocarro.py
from PyQt6.QtWidgets import QGraphicsRectItem, QGraphicsPolygonItem, QMessageBox, QGraphicsPixmapItem
from PyQt6.QtGui import QColor, QPolygonF, QBrush, QColor, QPixmap
from PyQt6.QtCore import Qt, QTimer, QPointF, QPropertyAnimation
from passageiro import Passageiro
from plataforma import Plataforma
import math 
import random
from time import sleep

class Autocarro(QGraphicsPixmapItem):
    def __init__(self, x, y, cor, cena, capacidade, direcao_saida):
        super().__init__()  # Largura x Altura do autocarro
        self.cor = cor # Cor do autocarro
        self.cena = cena  # Referência à cena para saber onde mover
        self.capacidade = capacidade  # Capacidade máxima de passageiros 
        self.direcao_saida = direcao_saida  # Direção de saída
        self.plataforma = None  # Atributo para armazenar a plataforma ocupada

        imagens_por_cor = {
            "red": "imagens/carro_vermelho.png",
            "yellow": "imagens/carro_amarelo.png",
            "blue": "imagens/carro_azul.png",
            "green": "imagens/carro_verde.png",
        }
        caminho_imagem = imagens_por_cor.get(cor, "autocarro_default.png")

        pixmap = QPixmap(caminho_imagem)
        if pixmap.isNull():
            print(f"Erro: imagem do autocarro não encontrada em {caminho_imagem}")
        else:
            largura, altura = 100, 80  # ou outro tamanho que desejar
            pixmap = pixmap.scaled(largura, altura, Qt.AspectRatioMode.KeepAspectRatio)
            self.setPixmap(pixmap)

        self.setPos(x, y)

        # Carrega a imagem da seta e cria o item da seta como filho
        pixmap_seta = QPixmap("imagens/seta.png")
        if not pixmap_seta.isNull():
            pixmap_seta = pixmap_seta.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio)
            self.seta = QGraphicsPixmapItem(pixmap_seta, self)
            # Inicialmente, offset zero; vamos posicionar no atualizar_seta()
            self.seta.setOffset(0, 0)
            self.seta.setRotation(0)

        self.atualizar_seta()

    def atualizar_seta(self):
        if not hasattr(self, "seta"):
            return

        # Pega o retângulo do autocarro
        rect = self.boundingRect()
        cx, cy = rect.center().x(), rect.center().y()

        # Posiciona a seta no centro do autocarro, corrigindo pelo offset da imagem da seta
        pixmap_rect = self.seta.boundingRect()
        offset_x = pixmap_rect.width() / 2
        offset_y = pixmap_rect.height() / 2

        self.seta.setPos(cx - offset_x, cy - offset_y)

        # Rotaciona a seta conforme a rotação do autocarro
        self.seta.setRotation(self.rotation())

        # Garante que a seta fique no topo visualmente
        self.seta.setZValue(self.zValue() + 1)



    def verificar_bloqueio(self) -> bool:
        # Direções possíveis (vetores normalizados)
        vetores_direcao = {
            "cima_direita": (math.sqrt(0.5), -math.sqrt(0.5)),
            "cima_esquerda": (-math.sqrt(0.5), -math.sqrt(0.5)),
            "baixo_direita": (math.sqrt(0.5), math.sqrt(0.5)),
            "baixo_esquerda": (-math.sqrt(0.5), math.sqrt(0.5)),
        }

        # Pega vetor de direção baseado em self.direcao_saida
        dir_x, dir_y = vetores_direcao.get(self.direcao_saida, (0, 0))
        
        if dir_x == 0 and dir_y == 0:
            return False  # Direção inválida, não bloqueia

        # Tamanho para determinar distância segura
        self_size = max(self.boundingRect().width(), self.boundingRect().height())
        limite_distancia = self_size * 1.5
        limite_angular = math.radians(30)  # 60° de abertura frontal

        for autocarro_dict in self.cena.autocarro_parado:
            outro = autocarro_dict["item"]
            if outro == self:
                continue

            # Vetor entre este e o outro autocarro
            rel_x = outro.x() - self.x()
            rel_y = outro.y() - self.y()
            distancia = math.hypot(rel_x, rel_y)

            if distancia > limite_distancia * 2:
                continue

            if distancia > 0:
                cos_theta = (dir_x * rel_x + dir_y * rel_y) / distancia
                theta = math.acos(max(min(cos_theta, 1), -1))
            else:
                return True  # Mesmo ponto → bloqueado

            if abs(theta) <= limite_angular:
                return True  # Outro autocarro está à frente

        return False  # Nenhum bloqueio à frente



     

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
        self.verificar_vitoria()
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
        self.verificar_derrota()


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
        
        self.verificar_vitoria()

    

        

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
        todos_passageiros_partiram = len(self.cena.passageiros) == 0

        if todos_passageiros_partiram:
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

