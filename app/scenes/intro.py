# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════
# CENA DE INTRODUÇÃO
# ═══════════════════════════════════════════════════════════════
# Cena inicial que apresenta o jogo com animação.
#
# Demonstra os seguintes requisitos:
# - (b) Primitivas: polígonos (jangada, personagem)
# - (c) Preenchimento: scanline_fill (mar, areia), flood_fill (personagem)
# - (e) Animação: jangada balançando, personagem andando
# - (h) Textura: céu e areia com textura
#
# Elementos da cena:
# - Céu com textura
# - Mar com gradiente
# - Areia texturizada
# - Jangada balançando suavemente (animação)
# - Personagem caminhando em direção à jangada (animação)
# - Transição suave para o menu
# ═══════════════════════════════════════════════════════════════

import pygame
import math
import assets.colors as color
from engine.raster.circle import draw_circle
from engine.fill.flood_fill import flood_fill_iterativo
from engine.fill.scanline import scanline_fill, scanline_fill_gradiente
from engine.geometry.cohen_sutherland import draw_line_clipped
from app.scenes.menu import run_menu
from app.entities.raft import draw_jangada
from assets.music_manager import music_manager
 

# ─── Funções Auxiliares ───
def draw_background(tela, largura, altura, textura_ceu=None, textura_areia=None):
    """
    Desenha o cenário de fundo da introdução.
    
    REQUISITOS:
    - (c) Preenchimento: scanline_fill para mar e areia
    - (h) Textura: céu e areia texturizados
    
    Args:
        tela: pygame.Surface
        largura: largura da tela
        altura: altura da tela
        textura_ceu: pygame.Surface com textura do céu (opcional)
        textura_areia: pygame.Surface com textura da areia (opcional)
    """
    # Céu com textura
    if textura_ceu:
        ceu = [
            (0, 0),
            (largura, 0),
            (largura, altura // 2),
            (0, altura // 2)
        ]
        scanline_texture_all(tela, ceu, textura_ceu, largura, altura // 2)
    else:
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
    if textura_areia:
        scanline_texture_all(
            tela,
            areia,
            textura_areia,
            largura,
            altura - (altura // 2 + 120),
            altura // 2 + 120
        )
    else:
        scanline_fill(tela, areia, color.SUN_ORANGE)


def scanline_texture_all(tela, pontos, textura, width, height, y_offset=0):
    """Preenche polígono com textura usando scanline."""
    tex_w, tex_h = textura.get_width(), textura.get_height()
    n = len(pontos)
    ys = [p[1] for p in pontos]
    y_min = int(min(ys))
    y_max = int(max(ys))

    for y in range(y_min, y_max):
        inter = []
        for i in range(n):
            x0, y0 = pontos[i]
            x1, y1 = pontos[(i + 1) % n]
            if y0 == y1:
                continue
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            if y < y0 or y >= y1:
                continue
            t = (y - y0) / (y1 - y0)
            x = x0 + t * (x1 - x0)
            inter.append(x)
        inter.sort()
        for i in range(0, len(inter), 2):
            if i + 1 >= len(inter):
                continue
            x_start = int(inter[i])
            x_end = int(inter[i + 1])
            for x in range(x_start, x_end + 1):
                tx = int((x / width) * (tex_w - 1)) if width > 0 else 0
                ty = int(((y - y_offset) / height) * (tex_h - 1)) if height > 0 else 0
                tx = max(0, min(tx, tex_w - 1))
                ty = max(0, min(ty, tex_h - 1))
                if 0 <= x < width and 0 <= (y - y_offset) < height:
                    tela.set_at((x, y), textura.get_at((tx, ty))[:3])


def draw_character_clipped(tela, cx, cy, dx, dy):
    """
    Desenha um jangadeiro estilizado usando polígonos preenchidos via scanline.
    Corpo, braços e pernas usam scanline_fill ou scanline_fill_gradiente.
    Cabeça ainda é um círculo preenchido. Adiciona chapéu.
    """
    x = cx + dx
    y = cy + dy

    # Cabeça
    draw_circle(tela, x, y, 12, color.DETAIL_COLOR)
    flood_fill_iterativo(tela, x, y, color.SKIN, color.DETAIL_COLOR)

    # Chapéu cônico
    chapeu = [
        (x - 12, y - 6),   # base esquerda
        (x + 12, y - 6),   # base direita
        (x, y - 22)        # topo
    ]
    scanline_fill_gradiente(tela, chapeu, color.WOOD_LIGHT, color.WOOD_DARK, direcao='vertical')

    # Corpo (trapezoide) com gradiente da roupa
    corpo = [
        (x - 10, y + 12),
        (x + 10, y + 12),
        (x + 8, y + 40),
        (x - 8, y + 40)
    ]
    scanline_fill_gradiente(tela, corpo, color.SEA_GREEN_DARK, color.SEA_GREEN_LIGHT, direcao='vertical')

    # Braços (polígonos inclinados)
    braco_esq = [(x - 10, y + 15), (x - 12, y + 18), (x - 20, y + 28), (x - 18, y + 25)]
    braco_dir = [(x + 10, y + 15), (x + 12, y + 18), (x + 20, y + 28), (x + 18, y + 25)]
    scanline_fill(tela, braco_esq, color.SKIN)
    scanline_fill(tela, braco_dir, color.SKIN)

    # Pernas (trapezoides)
    perna_esq = [(x - 8, y + 40), (x - 2, y + 40), (x - 4, y + 60), (x - 10, y + 60)]
    perna_dir = [(x + 2, y + 40), (x + 8, y + 40), (x + 10, y + 60), (x + 4, y + 60)]
    scanline_fill(tela, perna_esq, color.SKIN)
    scanline_fill(tela, perna_dir, color.SKIN)


def draw_raft_translated(tela, largura, altura, dx, scale=3):
    """
    Desenha a jangada usando draw_jangada, com deslocamento horizontal.
    A jangada será grande e posicionada na borda inferior do mar.

    Args:
        tela: pygame.Surface onde desenhar.
        largura, altura: dimensões da tela.
        dx: deslocamento horizontal da jangada (para balanço).
        scale: escala da jangada (quanto maior, mais gigante).
    """
    # base_y posiciona a jangada na borda inferior do mar
    base_x = largura // 2 + dx 
    base_y = altura // 2 + 70

    draw_jangada(tela, base_x, base_y, scale)


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
    textura_ceu = pygame.image.load("assets/textures/ceu.png").convert()
    textura_areia = pygame.image.load("assets/textures/areia.png").convert()

    # Carrega textura do céu
    textura_ceu = None
    try:
        textura_ceu = pygame.image.load("assets/textures/ceu.png").convert()
    except:
        pass  # se não encontrar, usa cor sólida

    # posição inicial do jangadeiro (fora da tela à esquerda)
    dx = -330  # começa bem fora
    dy = 120

    # centro da “janela do mundo”
    cx = largura // 2 - 200
    cy = altura // 2 + 60
    # Inicia música da introdução/menu
    music_manager.play("menu")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "sair"

        tela.fill(color.SKY_DUSK_BLUE)

        draw_background(tela, largura, altura, textura_ceu, textura_areia)

        # jangadeiro andando em direção ao mar
        if dx < 0:
            dx += 30

        # jangada balançando levemente
        amplitude = 6      # quanto a jangada se move (pixels)
        frequencia = 1   # quão rápido vai e volta
        raft_dx = int(amplitude * math.sin(frame * frequencia))
        draw_raft_translated(tela, largura, altura, raft_dx, scale=3)

        # movimento do jangadeiro (areia -> jangada)
        vel_x = 3
        vel_y = -2

        if dx < 0:
            dx += vel_x
            dx = min(dx, 0)

        if dy > 0:
            dy += vel_y
            dy = max(dy, 0)

        draw_character_clipped(tela, cx, cy, dx, dy)

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