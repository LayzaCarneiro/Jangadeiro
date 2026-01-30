# -*- coding: utf-8 -*-
"""
Cena de introdução do jogo.

Exibe:
- Céu e mar com gradiente e areia
- Jangada balançando suavemente
- Personagem andando em direção à jangada
- Transição suave para o menu
"""

import pygame
import math
import assets.colors as color
from engine.raster.line import desenhar_poligono
from engine.raster.circle import draw_circle
from engine.fill.flood_fill import flood_fill_iterativo
from engine.fill.scanline import scanline_fill
from engine.geometry.cohen_sutherland import draw_line_clipped
from app.scenes.menu import run_menu
 

# ======================================
# FUNÇÕES AUXILIARES
# ======================================
def draw_background(tela, largura, altura):
    """
    Desenha o céu, mar e areia como plano de fundo da cena.

    Args:
        tela: pygame.Surface onde desenhar.
        largura: largura da tela.
        altura: altura da tela.
    """
    # Céu
    tela.fill(color.SKY_DUSK_BLUE)

    # Mar
    mar = [
        (0, altura // 2),
        (largura, altura // 2),
        (largura, altura),
        (0, altura)
    ]
    scanline_fill(tela, mar, color.SEA_COLOR)

    # Areia
    areia = [
        (0, altura // 2 + 120),
        (largura, altura // 2 + 120),
        (largura, altura),
        (0, altura)
    ]
    scanline_fill(tela, areia, color.SUN_ORANGE)


def draw_character_clipped(tela, cx, cy, dx, dy, viewport):
    """
    Desenha o personagem com clipping no viewport.

    Args:
        tela: pygame.Surface onde desenhar.
        cx, cy: posição central do personagem.
        dx, dy: deslocamentos do personagem.
        viewport: tupla (xmin, ymin, xmax, ymax) para clipping.
    """
    x = cx + dx
    y = cy + dy

    # Cabeça (continua sem clipping, porque usamos fill)
    draw_circle(tela, x, y, 12, color.DETAIL_COLOR)
    flood_fill_iterativo(tela, x, y, color.SKIN, color.DETAIL_COLOR)

    # Corpo
    draw_line_clipped(tela, x, y + 12, x, y + 40, color.DETAIL_COLOR, viewport)

    # Braços
    draw_line_clipped(tela, x, y + 20, x - 15, y + 30, color.DETAIL_COLOR, viewport)
    draw_line_clipped(tela, x, y + 20, x + 15, y + 30, color.DETAIL_COLOR, viewport)

    # Pernas
    draw_line_clipped(tela, x, y + 40, x - 10, y + 60, color.DETAIL_COLOR, viewport)
    draw_line_clipped(tela, x, y + 40, x + 10, y + 60, color.DETAIL_COLOR, viewport)


def draw_raft_translated(tela, largura, altura, dx):
    """
    Desenha a jangada com translação horizontal para simular balanço.

    Args:
        tela: pygame.Surface onde desenhar.
        largura, altura: dimensões da tela.
        dx: deslocamento horizontal da jangada.
    """
    base_x = largura // 2 - 60 + dx
    base_y = altura // 2 + 60

    jangada = [
        (base_x, base_y),
        (base_x + 120, base_y),
        (base_x + 100, base_y + 30),
        (base_x + 20, base_y + 30)
    ]

    scanline_fill(tela, jangada, color.WOOD)
    desenhar_poligono(tela, jangada, color.DETAIL_COLOR)


# ======================================
# FUNÇÃO PRINCIPAL
# ======================================
def run_intro(tela):
    """
    Executa a cena de introdução do jogo.

    Args:
        tela: pygame.Surface principal do jogo.

    Retorna:
        String indicando ação ou chama run_menu.
    """
    clock = pygame.time.Clock()
    frame = 0
    transition = False
    transition_frame = 0

    largura, altura = tela.get_size()
    viewport = (0, 0, largura, altura)  # xmin, ymin, xmax, ymax

    # posição inicial do jangadeiro (fora da tela à esquerda)
    dx = -330  # começa bem fora
    dy = 120

    # centro da “janela do mundo”
    cx = largura // 2 - 200
    cy = altura // 2 + 60

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "sair"

        tela.fill(color.SKY_DUSK_BLUE)

        draw_background(tela, largura, altura)

        # jangadeiro andando em direção ao mar
        if dx < 0:
            dx += 4

        # jangada balançando levemente
        amplitude = 6      # quanto a jangada se move (pixels)
        frequencia = 1   # quão rápido vai e volta

        raft_dx = int(amplitude * math.sin(frame * frequencia))
        draw_raft_translated(tela, largura, altura, raft_dx)

        # movimento do jangadeiro (areia -> jangada)
        vel_x = 3
        vel_y = -2

        if dx < 0:
            dx += vel_x
            dx = min(dx, 0)

        if dy > 0:
            dy += vel_y
            dy = max(dy, 0)

        draw_character_clipped(tela, cx, cy, dx, dy, viewport)

        # =====================
        # Transição para o menu
        # =====================
        if transition:
            transition_frame += 10

            # sobe o mar (translação vertical)
            mar_offset = min(transition_frame * 4, altura // 2)

            mar = [
                (0, altura // 2 - mar_offset),
                (largura, altura // 2 - mar_offset),
                (largura, altura),
                (0, altura)
            ]
            scanline_fill(tela, mar, color.SEA_COLOR)

            # fade escuro
            fade = pygame.Surface((largura, altura))
            fade.set_alpha(min(transition_frame * 5, 255))
            fade.fill((0, 0, 0))
            tela.blit(fade, (0, 0))

            if transition_frame >= 60:
                return run_menu(tela)

        # quando chegar na jangada → menu
        if dx >= 0 and not transition:
            transition = True
            transition_frame = 0

        pygame.display.flip()
        clock.tick(60)
        frame += 1

