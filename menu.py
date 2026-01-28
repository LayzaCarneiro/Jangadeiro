# -*- coding: utf-8 -*-
"""
Tela inicial do jogo "Jangada das Estrelas".
Todo o desenho usa apenas set_pixel (via bresenham, círculo, elipse, scanline).
"""

import pygame
from engine.framebuffer import set_pixel
from engine.raster.line import bresenham, desenhar_poligono
from engine.raster.circle import draw_circle
from engine.fill.scanline import scanline_fill

# Cores (tema praia/dia)
SKY = (135, 206, 235)
SEA = (0, 120, 170)
SUN = (255, 204, 92)
WAVE = (90, 180, 200)
TITLE = (40, 50, 100)
BTN_FILL = (255, 204, 92)
BTN_BORDER = (180, 140, 50)
BTN_TEXT = (60, 50, 40)


# Fonte 5x7 (apenas set_pixel) – caracteres usados: A C D E G I J L N R S T V (espaço)
# Cada letra: 7 linhas de 5 caracteres; 'X' = pixel ligado
_FONT = {
    " ": ["     ", "     ", "     ", "     ", "     ", "     ", "     "],
    "A": ["  X  ", " X X ", "X   X", "XXXXX", "X   X", "X   X", "X   X"],
    "C": [" XXX ", "X   X", "X    ", "X    ", "X    ", "X   X", " XXX "],
    "D": ["XXX  ", "X  X ", "X   X", "X   X", "X   X", "X  X ", "XXX  "],
    "E": ["XXXXX", "X    ", "X    ", "XXX  ", "X    ", "X    ", "XXXXX"],
    "G": [" XXX ", "X   X", "X    ", "X XXX", "X   X", "X   X", " XXX "],
    "I": [" XXX ", "  X  ", "  X  ", "  X  ", "  X  ", "  X  ", " XXX "],
    "J": ["    X", "    X", "    X", "    X", "    X", "X   X", " XXX "],
    "L": ["X    ", "X    ", "X    ", "X    ", "X    ", "X    ", "XXXXX"],
    "N": ["X   X", "XX  X", "X X X", "X  XX", "X   X", "X   X", "X   X"],
    "R": ["XXXX ", "X   X", "X   X", "XXXX ", "X X  ", "X  X ", "X   X"],
    "S": [" XXX ", "X   X", "X    ", " XXX ", "    X", "X   X", " XXX "],
    "T": ["XXXXX", "  X  ", "  X  ", "  X  ", "  X  ", "  X  ", "  X  "],
    "V": ["X   X", "X   X", "X   X", "X   X", " X X ", " X X ", "  X  "],
    "O": [" XXX ", "X   X", "X   X", "X   X", "X   X", "X   X", " XXX "],
    "M": ["X   X", "XX XX", "X X X", "X   X", "X   X", "X   X", "X   X"],
    "B": ["XXXX ", "X   X", "X   X", "XXXX ", "X   X", "X   X", "XXXX "],
}


def _draw_char(surf, c, x, y, cor, scale=2):
    c = c.upper()
    rows = _FONT.get(c, _FONT[" "])
    for row, s in enumerate(rows):
        for col, ch in enumerate(s):
            if ch == "X":
                for dy in range(scale):
                    for dx in range(scale):
                        set_pixel(surf, x + col * scale + dx, y + row * scale + dy, cor)


def draw_text(surf, texto, x, y, cor, scale=2):
    """Desenha texto com a fonte 5x7 via set_pixel."""
    dx = 0
    for c in texto:
        if c.upper() in _FONT:
            _draw_char(surf, c, x + dx, y, cor, scale)
        dx += 6 * scale  # largura aproximada por letra + espaço


def draw_title_scene(surf, w, h):
    """Sol, horizonte e ondas usando retas, circunferência e elipse."""
    # Sol (circunferência)
    draw_circle(surf, int(w * 0.85), int(h * 0.15), 50, SUN)
    # Horizonte (reta)
    y_h = int(h * 0.65)
    bresenham(surf, 0, y_h, w, y_h, SEA)
    # Ondas (retas)
    for i in range(5):
        y = y_h + 15 + i * 12
        x0, x1 = 0, w
        bresenham(surf, x0, y, x1, y, WAVE)


def draw_button(surf, x, y, larg, alt, texto, cor_fundo, cor_borda, cor_texto):
    """Botão: polígono preenchido com scanline + borda com bresenham + texto."""
    pts = [(x, y), (x + larg, y), (x + larg, y + alt), (x, y + alt)]
    scanline_fill(surf, pts, cor_fundo)
    desenhar_poligono(surf, pts, cor_borda)
    # texto centralizado (aproximado)
    tw = len(texto) * 6 * 2  # 6*scale por letra, scale=2
    tx = x + (larg - tw) // 2
    ty = y + (alt - 7 * 2) // 2  # 7*scale de altura
    draw_text(surf, texto, max(x, tx), ty, cor_texto, scale=2)


def ponto_em_retangulo(px, py, rx, ry, rw, rh):
    return rx <= px <= rx + rw and ry <= py <= ry + rh


def run_menu(superficie):
    """
    Roda a tela inicial. Retorna 'iniciar' ou 'sair'.
    Toda a renderização usa apenas set_pixel (através dos algoritmos do engine).
    """
    w = superficie.get_width()
    h = superficie.get_height()

    # Botões
    bw, bh = 180, 50
    bx = (w - bw) // 2
    by_iniciar = int(h * 0.55)
    by_sair = int(h * 0.55) + 70

    while True:
        # Fundo (usa fill para performance; os elementos são desenhados com set_pixel)
        superficie.fill(SKY)

        # Cena: sol, horizonte, ondas
        draw_title_scene(superficie, w, h)

        # Título
        titulo = "JANGADA DAS ESTRELAS"
        tw_approx = len(titulo) * 6 * 2
        draw_text(superficie, titulo, (w - tw_approx) // 2, int(h * 0.22), TITLE, scale=2)

        # Botões
        draw_button(superficie, bx, by_iniciar, bw, bh, "INICIAR", BTN_FILL, BTN_BORDER, BTN_TEXT)
        draw_button(superficie, bx, by_sair, bw, bh, "SAIR", BTN_FILL, BTN_BORDER, BTN_TEXT)

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "sair"
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mx, my = e.pos
                if ponto_em_retangulo(mx, my, bx, by_iniciar, bw, bh):
                    return "iniciar"
                if ponto_em_retangulo(mx, my, bx, by_sair, bw, bh):
                    return "sair"
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return "sair"
