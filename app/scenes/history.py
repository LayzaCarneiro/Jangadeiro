# -*- coding: utf-8 -*-
"""
História introdutória do jogo "Jangadeiro: Dragão do Mar"
- Mostra a história dos jangadeiros do Ceará
- Antes do menu do jogo
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import pygame
import math
from engine.framebuffer import set_pixel
from engine.raster.line import bresenham, desenhar_poligono
from engine.fill.scanline import scanline_fill
from app.scenes.auxiliary_functions import draw_text, draw_button

# Cores
SKY = (135, 206, 235)
SEA = (25, 104, 163)
SUN = (255, 223, 0)
SAND = (194, 178, 128)
TEXT_COLOR = (255, 255, 255)
JANGADA_COLOR = (139, 69, 19)
PEIXE_COLOR = (255, 100, 100)

# =====================================================
# Funções auxiliares
# =====================================================
def draw_gradient(surf, top_color, bottom_color):
    """Cria gradiente vertical."""
    h = surf.get_height()
    for y in range(h):
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * y / h)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * y / h)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * y / h)
        for x in range(surf.get_width()):
            set_pixel(surf, x, y, (r, g, b))

def draw_sun(surf, x, y, r, color):
    """Desenha sol simples usando bresenham."""
    for angle in range(0, 360, 5):
        rad = math.radians(angle)
        px = int(x + r * math.cos(rad))
        py = int(y + r * math.sin(rad))
        set_pixel(surf, px, py, color)

def draw_jangada(surf, x, y, scale=1):
    """Desenha uma jangada simples como polígono."""
    points = [
        (x, y),
        (x + 50*scale, y),
        (x + 40*scale, y + 10*scale),
        (x + 10*scale, y + 10*scale)
    ]
    scanline_fill(surf, points, JANGADA_COLOR)
    desenhar_poligono(surf, points, (0, 0, 0))
    # mastro
    desenhar_poligono(surf, [(x+25*scale, y), (x+25*scale, y-30*scale)], (0,0,0))
    # vela
    sail = [(x+25*scale, y-30*scale), (x+45*scale, y-10*scale), (x+25*scale, y)]
    scanline_fill(surf, sail, (255, 255, 255))
    desenhar_poligono(surf, sail, (0,0,0))

def draw_peixe(surf, x, y, scale=1):
    """Desenha peixe simples."""
    points = [
        (x, y),
        (x + 10*scale, y + 5*scale),
        (x, y + 10*scale),
        (x - 10*scale, y + 5*scale)
    ]
    scanline_fill(surf, points, PEIXE_COLOR)
    desenhar_poligono(surf, points, (0,0,0))

# =====================================================
# Slides da história
# =====================================================
slides = [
    {
        "texto": [
            "Nas areias brancas do Ceara, o sol dita o ritmo da vida.",
            "Entre as ondas e o vento, surge a figura de um homem",
            "que se tornaria lenda: Francisco Jose do Nascimento."
        ],
        "draw_extra": lambda surf, w, h: draw_sun(surf, int(w*0.85), int(h*0.15), 50, SUN)
    },
    {
        "texto": [
            "Conhecido como 'Dragao do Mar', ele liderou jangadeiros",
            "em uma luta por liberdade, provando que o mar",
            "nao aceita correntes, nem escravidao."
        ],
        "draw_extra": lambda surf, w, h: draw_jangada(surf, int(w/2 - 25), int(h*0.6))
    },
    {
        "texto": [
            "A rotina era bruta. Antes do sol nascer, o buzios soava.",
            "Sem bussola, os jangadeiros liam o ceu e as correntes.",
            "À noite, o Cruzeiro do Sul era o guia para o porto seguro."
        ],
        "draw_extra": lambda surf, w, h: draw_stars(surf, w, h) # Sugestão: Desenhar o Cruzeiro do Sul
    },
    {
        "texto": [
            "Navegavam ate o 'fundo', onde a agua muda de cor.",
            "La, o peixe e farto, mas o perigo e constante.",
            "Cada onda vencida era uma vitoria para a comunidade."
        ],
        "draw_extra": lambda surf, w, h: draw_deep_sea(surf) # Sugestão: Ondas mais escuras/fortes
    },
    {
        "texto": [
            "Agora, voce navegara ao lado do Dragao do Mar!",
            "Sua missao e ajuda-lo a pescar os peixes mais valiosos",
            "enquanto desvia das pedras e perigos que surgem no caminho."
        ],
        "draw_extra": lambda surf, w, h: draw_peixe(surf, int(w/2), int(h*0.5))
    },
    {
        "texto": [
            "Mantenha os olhos nas estrelas para nao perder o rumo.",
            "Assuma o leme da 'Libertadora', use W, A, S, D para navegar",
            "e proteja sua tripulacao dos arrecifes traiçoeiros!"
        ],
        "draw_extra": lambda surf, w, h: None
    }
]

# =====================================================
# Função principal
# =====================================================
def run_story(superficie):
    w, h = superficie.get_width(), superficie.get_height()
    slide_index = 0
    clock = pygame.time.Clock()

    while slide_index < len(slides):
        superficie.fill((0,0,0))
        draw_gradient(superficie, SKY, SEA)

        slide = slides[slide_index]
        y_text = int(h*0.1)
        for line in slide["texto"]:
            draw_text(superficie, line, 50, y_text, TEXT_COLOR, scale=2)
            y_text += 30  # um pouco mais de espaço entre linhas

        # Extras do slide
        slide["draw_extra"](superficie, w, h)

        # Indicação visual de avançar
        draw_text(superficie, "Clique ou pressione ENTER para continuar", 50, h-50, TEXT_COLOR, scale=1)

        pygame.display.flip()
        clock.tick(60)

        # Espera ação do jogador
        waiting = True
        while waiting:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif e.type == pygame.KEYDOWN:
                    if e.key in (pygame.K_RETURN, pygame.K_SPACE):
                        slide_index += 1
                        waiting = False
                    elif e.key == pygame.K_ESCAPE:
                        return
                elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    # Avança slide ao clicar com botão esquerdo
                    slide_index += 1
                    waiting = False


# =====================================================
# Teste rápido
# =====================================================
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("História Jangadeiros - Teste")
    run_story(screen)
    pygame.quit()