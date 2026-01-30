# app/scenes/instructions.py
# -*- coding: utf-8 -*-
"""
Tela de instruções do jogo "Jangada das Estrelas".
Usa set_pixel, bresenham, scanline e a fonte 5x7.
"""

import pygame
from app.scenes.auxiliary_functions import draw_button, ponto_em_retangulo, draw_text

# Cores
BG = (135, 206, 235)
TEXT = (40, 50, 100)
BTN_FILL = (255, 204, 92)
BTN_BORDER = (180, 140, 50)
BTN_TEXT = (60, 50, 40)

def run_instructions(superficie):
    """Roda a tela de instruções. Volta ao menu ao clicar em 'VOLTAR'."""
    w, h = superficie.get_size()

    # Botão voltar
    bw, bh = 150, 50
    bx = (w - bw) // 2
    by_voltar = int(h * 0.8)

    while True:
        # Fundo
        superficie.fill(BG)

        # Título
        titulo = "COMO JOGAR"
        tw_approx = len(titulo) * 6 * 2
        draw_text(superficie, titulo, (w - tw_approx)//2, 50, TEXT, scale=2)

        # Texto de instruções
        instrucoes = [
            "OBJETIVO:",
            "- Coletar peixes e navegar",
            "- Evitar pedras",
            "",
            "CONTROLES:",
            "- W A S D: mover jangadeiro",
            "- ESC: sair do jogo",
        ]

        start_y = 150
        for i, linha in enumerate(instrucoes):
            draw_text(superficie, linha, 50, start_y + i * 30, TEXT, scale=2)

        # Botão voltar
        draw_button(superficie, bx, by_voltar, bw, bh, "VOLTAR", BTN_FILL, BTN_BORDER, BTN_TEXT)

        pygame.display.flip()

        # Eventos
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mx, my = e.pos
                if ponto_em_retangulo(mx, my, bx, by_voltar, bw, bh):
                    return  # volta para menu
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return