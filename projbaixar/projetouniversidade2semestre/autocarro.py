from PyQt6.QtWidgets import QMessageBox, QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer, QPointF
from passageiro import Passageiro
from plataforma import Plataforma
import math 
import random



# Nossa classe Autocarro representa um autocarro que pode ser movido, embarcar passageiros e verificar bloqueios.
class Autocarro(QGraphicsPixmapItem):
    def __init__(self, x, y, cor, cena, capacidade, direcao_saida):
        super().__init__()  
        self.cor = cor 
        self.cena = cena  
        self.capacidade = capacidade  
        self.direcao_saida = direcao_saida  
        self.plataforma = None 

        # Mapeia cor e capacidade para  as imagens certas
        imagens_por_cor_e_capacidade = {
        ("red", 4): "imagens/carro_vermelho.png",
        ("red", 8): "imagens/carro_vermelho6.png",
        ("yellow", 4): "imagens/carro_amarelo.png",
        ("yellow", 12): "imagens/carro_amarelo12.png",
        ("blue", 4): "imagens/carro_azul.png",
        ("blue", 6): "imagens/carro_azul6.png",
        ("green", 4): "imagens/carro_verde.png",
        ("green", 6): "imagens/carro_verde6.png",
    }

        caminho_imagem = imagens_por_cor_e_capacidade.get((cor, capacidade), "autocarro_default.png")
        pixmap = QPixmap(caminho_imagem)

        if pixmap.isNull():
            print(f"Erro: imagem do autocarro não encontrada em {caminho_imagem}")
            return

        # Definir tamanho da imagem conforme capacidade
        if capacidade == 4:
            largura, altura = 55, 55
        elif capacidade == 6:
            largura, altura = 100, 75
        elif capacidade == 8:
            largura, altura = 140, 75
        elif capacidade == 12:
            largura, altura = 100, 85
        else:
            largura, altura = 100, 80  # padrão

        pixmap = pixmap.scaled(largura, altura, Qt.AspectRatioMode.KeepAspectRatio)
        self.setPixmap(pixmap)
        self.setPos(x, y)

        # Carrega a imagem da seta e cria o item da seta como filho da nossa classe
        pixmap_seta = QPixmap("imagens/seta.png")
        if not pixmap_seta.isNull():
            pixmap_seta = pixmap_seta.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio)
            self.seta = QGraphicsPixmapItem(pixmap_seta, self)
            self.seta.setOffset(0, 0) # Ajusta o offset para centralizar a seta
            self.seta.setRotation(0) 

        self.atualizar_seta()

    # Define a seta com base na rotação do autocarro e direção de saída
    def atualizar_seta(self):
        if not hasattr(self, "seta"):
            return

        
        rect = self.boundingRect()    # Pega o retângulo do autocarro
        cx, cy = rect.center().x(), rect.center().y()

        
        pixmap_rect = self.seta.boundingRect()
        offset_x = pixmap_rect.width() / 2          # Posiciona a seta no centro do autocarro, corrigindo pelo offset da imagem da seta
        offset_y = pixmap_rect.height() / 2

        self.seta.setPos(cx - offset_x, cy - offset_y)

       
        self.seta.setRotation(self.rotation())       # Rotaciona a seta conforme a rotação do autocarro

        
        self.seta.setZValue(self.zValue() + 1)      # Garante que a seta fique no topo visualmente


    # Função responsável por verificar se há bloqueio na direção de saída do autocarro
    def verificar_bloqueio(self) -> bool:
        
        vetores_direcao = {
            "cima_direita": (math.sqrt(0.5), -math.sqrt(0.5)),      # Direções possíveis (vetores normalizados)
            "cima_esquerda": (-math.sqrt(0.5), -math.sqrt(0.5)), 
            "baixo_direita": (math.sqrt(0.5), math.sqrt(0.5)),
            "baixo_esquerda": (-math.sqrt(0.5), math.sqrt(0.5)),
        }

       
        dir_x, dir_y = vetores_direcao.get(self.direcao_saida, (0, 0))  # Pega vetor de direção baseado em self.direcao_saida
        
        if dir_x == 0 and dir_y == 0:
            return False                    # Se direção for inválida, então não há bloqueio

        self_size = max(self.boundingRect().width(), self.boundingRect().height()) # Tamanho para determinar distância segura
        limite_distancia = self_size * 1.5
        limite_angular = math.radians(30)  # 60° de abertura frontal

        for autocarro_dict in self.cena.autocarro_parado:
            outro = autocarro_dict["item"]
            if outro == self:
                continue

            
            rel_x = outro.x() - self.x()        # Vetor entre este e o outro autocarro
            rel_y = outro.y() - self.y()
            distancia = math.hypot(rel_x, rel_y)

            if distancia > limite_distancia * 2:
                continue

            if distancia > 0:
                cos_theta = (dir_x * rel_x + dir_y * rel_y) / distancia
                theta = math.acos(max(min(cos_theta, 1), -1))
            else:
                return True  # Mesmo ponto então está bloqueado

            if abs(theta) <= limite_angular:
                return True  # Outro autocarro está à frente

        return False  # Nenhum bloqueio à frente

    # Função mousePressEvent que é chamada quando o autocarro é clicado
    def mousePressEvent(self, event):
        # Move o autocarro para cima da plataforma
        if not self.verificar_bloqueio():
            self.move_to_platform()
        else:
            print("Não é possível mover: há um autocarro bloqueando!")
   
    # Função que move o autocarro para a plataforma livre
    def move_to_platform(self):
        plataforma_livre = False
        for platform in self.cena.platforms:  # Itera sobre a lista de plataformas para verificar se está ocupada
            if not platform["ocupada"]:
                plataforma_livre = True
                platform["ocupada"] = True  
                self.plataforma = platform  
                self.cena.autocarros_estacionados.append(self)  
                platform["item"].animar_autocarro(self)           
                break
        
        if not plataforma_livre:
            self.verificar_derrota() # Exibe mensagem de derrota se não houver plataformas livres
    
    # Função que embarca o passageiro no autocarro
    def embarcar_passageiro(self):
        self.verificar_vitoria()
        if self.capacidade > 0 and self.cena.passageiros: # Verifica se há passageiros e se o autocarro tem capacidade
            for passageiro in list(self.cena.passageiros):  # Evita erro ao remover da lista
                if not passageiro["embarcado"]: 
                    autocarro_correto = None
                    for autocarro in self.cena.autocarros_estacionados:
                        if passageiro["item"].cor == autocarro.cor and autocarro.capacidade > 0:
                            autocarro_correto = autocarro
                            break  # Para assim que encontrar um autocarro válido

                    if autocarro_correto and passageiro["posicao"] == 1:
                        autocarro_correto.animar_passageiro(passageiro)  # Anima o passageiro até a seta do autocarro
                        autocarro_correto.capacidade -= 1
                        passageiro["embarcado"] = True  

                        self.atualizar_posicoes() #Atualiza as posições dos passageiros na cena e nas listas                        
                        self.verificar_vitoria() #Verifica se todos os passageiros embarcaram
                        self.cena.gerar_passageiro() # Gera um novo passageiro se houver vagas
                                               
                        if autocarro_correto.capacidade > 0:    #Se ainda há capacidade, verifica o próximo passageiro
                            autocarro_correto.verificar_proximo_passageiro()    
                        else:
                            QTimer.singleShot(500, autocarro_correto.partir)  # Se o autocarro estiver cheio, então parte, Espera 0.5s antes de partir                            
                            autocarro_correto.verificar_proximo_passageiro()
                        return  
        
        self.verificar_vitoria()
        self.verificar_derrota()

    # Função que verifica se há passageiros á seguir para embarcar
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

    # Função que remove o autocarro e os passageiros embarcados da cena                  
    def partir(self):
        for passageiro in list(self.cena.passageiros):  # Cópia da lista para evitar conflitos
            if passageiro.get("embarcado"):
                item = passageiro["item"]
                if item.scene() is not None:
                    self.cena.scene.removeItem(item)
                self.cena.passageiros.remove(passageiro)  # Remove da lista principal

        if self in self.cena.autocarros_estacionados: #Remove o autocarro da lista de estacionados
            self.cena.autocarros_estacionados.remove(self)

        if self.plataforma: #Libera a plataforma
            self.plataforma["ocupada"] = False

        if self.scene() is not None: #Remove o autocarro da cena
            self.cena.scene.removeItem(self)
        
        self.verificar_vitoria()

    # Função que anima o passageiro até a posição do autocarro
    def animar_passageiro(self, passageiro):
        passageiro_item = passageiro["item"]
        destino = QPointF(self.x(), self.y())  # Posição do autocarro
        
        timer = QTimer() # Timer para animar o passageiro como o professor pediu
    
        def mover():
           
            pos_atual = passageiro_item.pos() # Obtém a posição atual
        
            step_x = (destino.x() - pos_atual.x()) * 0.1  # Calcula o próximo passo (movimento gradual)# 
            step_y = (destino.y() - pos_atual.y()) * 0.1  #10% do caminho a cada atualização
        
            nova_posicao = QPointF(pos_atual.x() + step_x, pos_atual.y() + step_y) # Move o passageiro suavemente
            passageiro_item.setPos(nova_posicao)
        
            if abs(nova_posicao.x() - destino.x()) < 2 and abs(nova_posicao.y() - destino.y()) < 2: # Verifica se o passageiro chegou ao destino 
                passageiro_item.setPos(destino)  # Garante que fique exatamente no destino
                timer.stop()  # Para a animação
                  
        timer.timeout.connect(mover) # Conecta o timer à função de movimento e inicia
        timer.start(20)  # Atualiza a posição a cada 20ms para suavizar o movimento

    # Função que atualiza as posições dos passageiros na cena e nas listas para facilitar embarque e identificações
    def atualizar_posicoes(self):
        for passageiro in self.cena.passageiros:
            if not passageiro["embarcado"]:  
                passageiro["posicao"] -= 1  # Atualiza posição´
                if passageiro["posicao"] >= 1:
                    pos_atual = passageiro["item"].pos()
                    novo_x = pos_atual.x() - 30  # ou +30 se quiser mover para a direita
                    novo_y = pos_atual.y()       # mantém o mesmo Y
                    passageiro["item"].setPos(novo_x, novo_y)


    # Função que verifica se todos os passageiros partiram e assim decretar vitória
    def verificar_vitoria(self):          
        todos_passageiros_partiram = len(self.cena.passageiros) == 0 # Verifica se todos os passageiros já partiram

        if todos_passageiros_partiram:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Vitória!")
            msg.setText("Parabéns! Todos os autocarros completaram sua missão!")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()

    # Função que verifica se todas as plataformas estão ocupadas e exibe mensagem de derrota
    def verificar_derrota(self):
        todas_ocupadas = all(platform["ocupada"] for platform in self.cena.platforms) # Verifica se todas as plataformas estão ocupadas

        if todas_ocupadas:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Derrota!")
            msg.setText("Todas as plataformas estão ocupadas! Você perdeu!")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()

