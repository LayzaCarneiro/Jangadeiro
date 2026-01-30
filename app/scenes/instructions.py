# app/scenes/instructions.py
# -*- coding: utf-8 -*-
"""
Tela de instruções do jogo "Jangada das Estrelas".

Inclui:
- Gradiente de fundo
- Ondas decorativas
- Peixinhos decorativos
- Caixas de instruções com título e texto
- Botão "VOLTAR" interativo
"""

import pygame
import math
import assets.colors as color
from app.scenes.auxiliary_functions import draw_button, ponto_em_retangulo, draw_text
from engine.raster.line import bresenham
from engine.fill.scanline import scanline_fill
from engine.raster.circle import draw_circle

def draw_gradient_bg(surf, top_color, bottom_color):
    """
    Desenha um gradiente vertical do topo para a base da superfície.

    Args:
        surf: pygame.Surface onde desenhar.
        top_color: RGB da cor superior.
        bottom_color: RGB da cor inferior.
    """
    w, h = surf.get_size()
    for y in range(h):
        ratio = y / h
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        pygame.draw.line(surf, (r, g, b), (0, y), (w, y))


def draw_waves_bottom(surf, altura, largura, offset=0):
    """
    Desenha ondas decorativas na parte inferior da tela.

    Args:
        surf: pygame.Surface onde desenhar.
        altura: altura total da superfície.
        largura: largura total da superfície.
        offset: deslocamento horizontal para animação.
    """
    for i in range(altura - 100, altura, 15):
        for x in range(0, largura, 30):
            y_offset = int(10 * math.sin((x + offset) * 0.05))
            bresenham(surf, x, i + y_offset, x + 20, i + y_offset, color.WAVE_COLOR)


def draw_decor_peixes(surf, largura, altura):
    """
    Desenha peixinhos decorativos próximos das instruções.

    Args:
        surf: pygame.Surface onde desenhar.
        largura: largura da tela.
        altura: altura da tela.
    """
    positions = [(largura - 100, altura//3), (largura - 150, altura//2), (largura - 80, altura*2//3)]
    for px, py in positions:
        draw_circle(surf, px, py, 8, color.DECOR_COLOR)
        draw_circle(surf, px, py, 4, color.TEXT)


def run_instructions(superficie):
    """
    Executa a tela de instruções do jogo.
    
    Args:
        superficie: pygame.Surface principal do jogo.
    """
    w, h = superficie.get_size()

    # Botão voltar
    bw, bh = 150, 50
    bx = (w - bw) // 2
    by_voltar = int(h * 0.85)

    frame = 0
    running = True
    while running:
        # Eventos
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mx, my = e.pos
                if ponto_em_retangulo(mx, my, bx, by_voltar, bw, bh):
                    return
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return

        # ----------------------
        # Fundo
        # ----------------------
        draw_gradient_bg(superficie, color.BG_TOP, color.BG_BOTTOM)
        draw_waves_bottom(superficie, h, w, offset=frame)
        draw_decor_peixes(superficie, w, h)

        # ----------------------
        # Título
        # ----------------------
        titulo = "COMO JOGAR"
        tw_approx = len(titulo) * 6 * 2
        draw_text(superficie, titulo, (w - tw_approx)//2, 40, color.TITLE_COLOR, scale=3)

        # ----------------------
        # Caixas de instruções
        # ----------------------
        instrucoes = [
            ("OBJETIVO", ["- Coletar peixes e navegar", "- Evitar pedras"]),
            ("CONTROLES", ["- W A S D: mover jangadeiro", "- ESC: sair do jogo"])
        ]

        start_y = 150
        box_w, box_h = w - 100, 120
        for titulo_box, linhas in instrucoes:
            # Caixa de fundo
            pts = [(50, start_y), (50 + box_w, start_y), (50 + box_w, start_y + box_h), (50, start_y + box_h)]
            scanline_fill(superficie, pts, color.BOX_BG)
            # Borda
            bresenham(superficie, 50, start_y, 50 + box_w, start_y, color.BOX_BORDER)
            bresenham(superficie, 50 + box_w, start_y, 50 + box_w, start_y + box_h, color.BOX_BORDER)
            bresenham(superficie, 50 + box_w, start_y + box_h, 50, start_y + box_h, color.BOX_BORDER)
            bresenham(superficie, 50, start_y + box_h, 50, start_y, color.BOX_BORDER)
            # Texto
            draw_text(superficie, titulo_box, 60, start_y + 10, color.TITLE_COLOR, scale=2)
            for i, linha in enumerate(linhas):
                draw_text(superficie, linha, 70, start_y + 40 + i*25, color.TEXT, scale=2)
            start_y += box_h + 30

        # ----------------------
        # Botão voltar
        # ----------------------
        draw_button(superficie, bx, by_voltar, bw, bh, "VOLTAR", color.BTN_FILL, color.BTN_BORDER, color.BTN_TEXT)

        pygame.display.flip()
        frame += 1
        pygame.time.Clock().tick(60)