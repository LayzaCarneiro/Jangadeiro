# -*- coding: utf-8 -*-
"""
Tela de consolação quando o jogador perde todas as vidas.
Mesmo tom de azul do menu, mensagem em vermelho, botões amarelos como no menu.
"""

import pygame
from app.scenes.auxiliary_functions import draw_text, draw_button, ponto_em_retangulo

# Mesmo padrão do menu
SKY = (135, 206, 235)
MESSAGE_COLOR = (200, 50, 50)   # Vermelho
BTN_FILL = (255, 204, 92)
BTN_BORDER = (180, 140, 50)
BTN_TEXT = (60, 50, 40)


def run_game_over(superficie):
    """
    Exibe a tela "VOCÊ PERDEU". Retorna 'jogar_novamente' ou 'sair'.
    """
    w = superficie.get_width()
    h = superficie.get_height()

    bw, bh = 220, 50
    bx = (w - bw) // 2
    by_jogar = int(h * 0.52)
    by_sair = by_jogar + 70

    while True:
        superficie.fill(SKY)

        # Mensagem em vermelho (mesma fonte e renderização do menu)
        titulo = "VOCE PERDEU"
        tw_approx = len(titulo) * 6 * 2
        draw_text(superficie, titulo, (w - tw_approx) // 2, int(h * 0.28), MESSAGE_COLOR, scale=2)

        # Botões amarelos como no menu
        draw_button(superficie, bx, by_jogar, bw, bh, "JOGAR NOVAMENTE", BTN_FILL, BTN_BORDER, BTN_TEXT)
        draw_button(superficie, bx, by_sair, bw, bh, "SAIR", BTN_FILL, BTN_BORDER, BTN_TEXT)

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "sair"
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mx, my = e.pos
                if ponto_em_retangulo(mx, my, bx, by_jogar, bw, bh):
                    return "jogar_novamente"
                if ponto_em_retangulo(mx, my, bx, by_sair, bw, bh):
                    return "sair"
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return "sair"
