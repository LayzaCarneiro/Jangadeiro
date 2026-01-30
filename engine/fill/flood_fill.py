# -*- coding: utf-8 -*-
"""
Flood Fill iterativo (4-conectado) usando set_pixel.

Esta função preenche uma área contida por uma cor de borda (`cor_borda`) 
com uma cor de preenchimento (`cor_preenchimento`) em uma superfície Pygame.

O algoritmo é baseado em pilha (DFS iterativo) e considera somente os 
vizinhos 4-direcionais: cima, baixo, esquerda, direita.
"""

from engine.framebuffer import set_pixel

# =========================
# Flood Fill (4-conectado)
# =========================

def flood_fill_iterativo(superficie, x, y, cor_preenchimento, cor_borda):    
    """
    Preenche recursivamente uma área com cor, evitando ultrapassar bordas.

    Args:
        superficie (pygame.Surface): Superfície onde o preenchimento será feito.
        x (int): Coordenada x inicial do ponto de partida.
        y (int): Coordenada y inicial do ponto de partida.
        cor_preenchimento (tuple): Cor RGB usada para preencher a área.
        cor_borda (tuple): Cor RGB que delimita a área (não deve ser preenchida).

    Exemplo:
        flood_fill_iterativo(tela, 100, 50, (255, 0, 0), (0, 0, 0))
    """
    largura = superficie.get_width()
    altura = superficie.get_height()

    pilha = [(x, y)]

    while pilha:
        x, y = pilha.pop()

        if not (0 <= x < largura and 0 <= y < altura):
            continue

        cor_atual = superficie.get_at((x, y))[:3]

        if cor_atual == cor_borda or cor_atual == cor_preenchimento:
            continue

        set_pixel(superficie, x, y, cor_preenchimento)

        pilha.append((x + 1, y))
        pilha.append((x - 1, y))
        pilha.append((x, y + 1))
        pilha.append((x, y - 1))