# -*- coding: utf-8 -*-
"""
Tela inicial do jogo "Jangada das Estrelas".
Todo o desenho usa apenas set_pixel (via bresenham, círculo, elipse, scanline).
"""

import pygame
import assets.colors as color
from engine.raster.circle import draw_circle
from app.scenes.auxiliary_functions import draw_text, draw_button, ponto_em_retangulo
from app.scenes.instructions import run_instructions
from assets.music_manager import music_manager

def draw_title_scene(surf, w, h):
    """
    Sol, horizonte e ondas usando retas, circunferência e elipse.
    
    Args:
        surf: pygame.Surface onde desenhar.
        w: largura da tela.
        h: altura da tela.
    """
    
    # Sol (circunferência)
    draw_circle(surf, int(w * 0.85), int(h * 0.15), 50, color.SUN)
    # Horizonte (reta)
    y_h = int(h * 0.65)


# ======================================
# FUNÇÃO PRINCIPAL
# ======================================
def run_menu(superficie):
    """
    Toda a renderização usa apenas set_pixel (através dos algoritmos do engine).

    Executa a tela inicial do jogo com botões:
    - INICIAR
    - COMO JOGAR
    - SAIR

    Args:
        superficie: pygame.Surface principal do jogo.

    Retorna:
        String indicando a ação escolhida: 'iniciar' ou 'sair'.
    """
    w = superficie.get_width()
    h = superficie.get_height()

    # Botões
    bw, bh = 180, 50
    bx = (w - bw) // 2
    by_iniciar = int(h * 0.45)
    by_instrucoes = by_iniciar + 70
    by_sair = by_instrucoes + 70

    # Garante que a música do menu está tocando
    music_manager.play("menu")

    while True:
        # Fundo (usa fill para performance; os elementos são desenhados com set_pixel)
        superficie.fill(color.SKY)

        # Cena: sol, horizonte, ondas
        draw_title_scene(superficie, w, h)

        # Título
        titulo = "JANGADA DAS ESTRELAS"
        tw_approx = len(titulo) * 6 * 2
        draw_text(superficie, titulo, (w - tw_approx) // 2, int(h * 0.22), color.TITLE, scale=2)

        # Botões
        draw_button(superficie, bx, by_iniciar, bw, bh, "INICIAR", color.BTN_FILL, color.BTN_BORDER, color.BTN_TEXT)
        draw_button(superficie, bx, by_instrucoes, bw, bh, "COMO JOGAR", color.BTN_FILL, color.BTN_BORDER, color.BTN_TEXT)
        draw_button(superficie, bx, by_sair, bw, bh, "SAIR", color.BTN_FILL, color.BTN_BORDER, color.BTN_TEXT)

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "sair"
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mx, my = e.pos
                if ponto_em_retangulo(mx, my, bx, by_iniciar, bw, bh):
                    return "iniciar"
                if ponto_em_retangulo(mx, my, bx, by_instrucoes, bw, bh):
                    run_instructions(superficie)
                if ponto_em_retangulo(mx, my, bx, by_sair, bw, bh):
                    return "sair"
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return "sair"
