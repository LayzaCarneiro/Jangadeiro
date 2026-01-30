# app/scenes/instructions.py
# -*- coding: utf-8 -*-
"""
Tela de instruções do jogo "Jangada das Estrelas".
Visualmente mais bonita, usando set_pixel, bresenham e scanline.
"""

import pygame
import math
from app.scenes.auxiliary_functions import draw_button, ponto_em_retangulo, draw_text
from engine.raster.line import bresenham
from engine.fill.scanline import scanline_fill
from engine.raster.circle import draw_circle

# =====================
# Cores
# =====================
BG_TOP = (28, 44, 92)          # Gradiente céu (topo)
BG_BOTTOM = (12, 18, 64)       # Gradiente céu (inferior)
TEXT = (240, 240, 240)
TITLE_COLOR = (255, 204, 92)
BOX_BG = (0, 120, 170)
BOX_BORDER = (255, 204, 92)
BTN_FILL = (255, 204, 92)
BTN_BORDER = (180, 140, 50)
BTN_TEXT = (40, 50, 100)
WAVE_COLOR = (90, 180, 200)
DECOR_COLOR = (255, 215, 0)

# =====================
# Funções auxiliares
# =====================
def draw_gradient_bg(surf, top_color, bottom_color):
    """Cria um gradiente vertical de cima para baixo"""
    w, h = surf.get_size()
    for y in range(h):
        ratio = y / h
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        pygame.draw.line(surf, (r, g, b), (0, y), (w, y))

def draw_waves_bottom(surf, altura, largura, offset=0):
    """Desenha ondas decorativas na parte inferior"""
    for i in range(altura - 100, altura, 15):
        for x in range(0, largura, 30):
            y_offset = int(10 * math.sin((x + offset) * 0.05))
            bresenham(surf, x, i + y_offset, x + 20, i + y_offset, WAVE_COLOR)

def draw_decor_peixes(surf, largura, altura):
    """Peixinhos decorativos ao lado das instruções"""
    positions = [(largura - 100, altura//3), (largura - 150, altura//2), (largura - 80, altura*2//3)]
    for px, py in positions:
        draw_circle(surf, px, py, 8, DECOR_COLOR)
        draw_circle(surf, px, py, 4, TEXT)

# =====================
# Tela de instruções
# =====================
def run_instructions(superficie):
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
        draw_gradient_bg(superficie, BG_TOP, BG_BOTTOM)
        draw_waves_bottom(superficie, h, w, offset=frame)
        draw_decor_peixes(superficie, w, h)

        # ----------------------
        # Título
        # ----------------------
        titulo = "COMO JOGAR"
        tw_approx = len(titulo) * 6 * 2
        draw_text(superficie, titulo, (w - tw_approx)//2, 40, TITLE_COLOR, scale=3)

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
            scanline_fill(superficie, pts, BOX_BG)
            # Borda
            bresenham(superficie, 50, start_y, 50 + box_w, start_y, BOX_BORDER)
            bresenham(superficie, 50 + box_w, start_y, 50 + box_w, start_y + box_h, BOX_BORDER)
            bresenham(superficie, 50 + box_w, start_y + box_h, 50, start_y + box_h, BOX_BORDER)
            bresenham(superficie, 50, start_y + box_h, 50, start_y, BOX_BORDER)
            # Texto
            draw_text(superficie, titulo_box, 60, start_y + 10, TITLE_COLOR, scale=2)
            for i, linha in enumerate(linhas):
                draw_text(superficie, linha, 70, start_y + 40 + i*25, TEXT, scale=2)
            start_y += box_h + 30

        # ----------------------
        # Botão voltar
        # ----------------------
        draw_button(superficie, bx, by_voltar, bw, bh, "VOLTAR", BTN_FILL, BTN_BORDER, BTN_TEXT)

        pygame.display.flip()
        frame += 1
        pygame.time.Clock().tick(60)