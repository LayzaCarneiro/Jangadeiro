import pygame
import math
import assets.colors as color
from engine.framebuffer import set_pixel
from engine.raster.line import bresenham, desenhar_poligono
from engine.raster.circle import draw_circle, get_circle_points
from engine.raster.elipse import draw_elipse
from engine.fill.flood_fill import flood_fill_iterativo
from engine.fill.scanline import scanline_fill
from app.scenes.menu import run_menu

def draw_sun(tela, largura):
    cx, cy, r = largura // 2, 180, 60
    draw_circle(tela, cx, cy, r, color.SUN)
    flood_fill_iterativo(tela, cx, cy, color.SUN, color.DETAIL_COLOR)


def draw_cloud(tela, x, y):
    get_circle_points(tela, x, y, 50, 20, color.CLOUD)
    flood_fill_iterativo(tela, x, y, color.CLOUD, color.DETAIL_COLOR)


def draw_waves(tela, largura, altura):
    for y in range(360, altura, 20):
        for x in range(0, largura, 40):
            bresenham(tela, x, y, x + 30, y + 5, color.WAVE)

def draw_background(tela, largura, altura):
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

def draw_character_translated(tela, cx, cy, dx, dy):
    x = cx + dx
    y = cy + dy

    # Cabeça
    draw_circle(tela, x, y, 12, color.DETAIL_COLOR)
    flood_fill_iterativo(tela, x, y, color.SKIN, color.DETAIL_COLOR)

    # Corpo
    bresenham(tela, x, y + 12, x, y + 40, color.DETAIL_COLOR)

    # Braços
    bresenham(tela, x, y + 20, x - 15, y + 30, color.DETAIL_COLOR)
    bresenham(tela, x, y + 20, x + 15, y + 30, color.DETAIL_COLOR)

    # Pernas
    bresenham(tela, x, y + 40, x - 10, y + 60, color.DETAIL_COLOR)
    bresenham(tela, x, y + 40, x + 10, y + 60, color.DETAIL_COLOR)

def draw_raft_translated(tela, largura, altura, dx):
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

def run_intro(tela):
    clock = pygame.time.Clock()
    frame = 0

    transition = False
    transition_frame = 0

    # posição inicial do jangadeiro (na areia)
    dx = -200
    dy = 120

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "sair"

        largura, altura = tela.get_size()
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

        draw_character_translated(
            tela,
            largura // 2 - 200,
            altura // 2 + 60,
            dx,
            dy
        )

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


        pygame.display.flip()
        clock.tick(60)
        frame += 1

        # quando chegar na jangada → menu
        if dx >= 0 and not transition:
            transition = True
            transition_frame = 0

