# -*- coding: utf-8 -*-
"""
História introdutória do jogo "Jangadeiro: Dragão do Mar"
- Mostra a história dos jangadeiros do Ceará
- Antes do menu do jogo
"""
import sys
import pygame
import math
import assets.colors as color
from app.scenes.auxiliary_functions import randint, draw_text
from engine.fill.flood_fill import flood_fill_iterativo
from engine.framebuffer import set_pixel
from app.entities.raft import draw_jangada
from app.entities.fish import draw_fish
from assets.music_manager import music_manager

# =====================================================
# Funções auxiliares
# =====================================================
def draw_waves(surf, y_start, y_end, amplitude=10, wavelength=50, color=(25, 104, 163)):
    """Desenha ondas simples no mar."""
    w = surf.get_width()
    for x in range(w):
        y = int(amplitude * math.sin(2 * math.pi * x / wavelength))
        for yy in range(y_start + y, y_end):
            set_pixel(surf, x, yy, color)

def draw_sand_gradient(surf, y_start, y_end, top_color=color.SAND, bottom_color=(210, 180, 140)):
    """Gradiente simples para areia da praia."""
    h = y_end - y_start
    for y in range(h):
        r = int(top_color[0] + (bottom_color[0]-top_color[0]) * y / h)
        g = int(top_color[1] + (bottom_color[1]-top_color[1]) * y / h)
        b = int(top_color[2] + (bottom_color[2]-top_color[2]) * y / h)
        for x in range(surf.get_width()):
            set_pixel(surf, x, y_start + y, (r, g, b))


# =====================================================
# História
# =====================================================
slides = [
    {
        "texto": [
            "Nas areias brancas do Ceara, o sol dita o ritmo da vida.",
            "Entre as ondas e o vento, surge a figura de um homem",
            "que se tornaria lenda: Francisco Jose do Nascimento.",
            "",
            "Conhecido como 'Dragao do Mar', ele liderou jangadeiros",
            "em uma luta por liberdade, provando que o mar",
            "nao aceita correntes, nem escravidao."
        ],
        "draw_extra": lambda surf, w, h: (
            draw_sand_gradient(surf, int(h*0.8), h),
            draw_waves(surf, int(h*0.6), int(h*0.8)),
            draw_jangada(surf, int(w*0.3), int(h*0.7), scale=0.7),
            draw_jangada(surf, int(w*0.6), int(h*0.72), scale=0.5),
            draw_jangada(surf, int(w*0.75), int(h*0.68), scale=0.6)
        )
    },
    {
        "texto": [
            "A rotina era bruta. Antes do sol nascer, o buzios soava.",
            "Sem bussola, os jangadeiros liam o ceu e as correntes.",
            "A noite, o Cruzeiro do Sul era o guia para o porto seguro.",
            "",
            "Navegavam ate o 'fundo', onde a agua muda de cor.",
            "La, o peixe e farto, mas o perigo e constante.",
            "Cada onda vencida era uma vitoria para a comunidade."
        ],
    "draw_extra": lambda surf, w, h: [
        draw_fish(surf, int(w*0.3), int(h*0.55), cor=color.FISH_GOLD),
        draw_fish(surf, int(w*0.4), int(h*0.6), cor=color.FISH_BLUE),
        draw_fish(surf, int(w*0.5), int(h*0.5), cor=color.FISH_TURQUOISE),
        draw_fish(surf, int(w*0.6), int(h*0.65), cor=color.FISH_GOLD),
        draw_fish(surf, int(w*0.7), int(h*0.52), cor=color.FISH_BLUE),
        draw_fish(surf, int(w*0.75), int(h*0.58), cor=color.FISH_TURQUOISE),
        draw_fish(surf, int(w*0.8), int(h*0.6), cor=color.FISH_TURQUOISE),
    ]
    },
    {
        "texto": [
            "Agora, voce navegara ao lado do Dragao do Mar!",
            "",
            "Sua missao e ajuda-lo a pescar os peixes mais valiosos",
            "enquanto desvia das pedras e perigos que surgem no caminho.",
            "",
            "Mantenha os olhos nas estrelas para nao perder o rumo.",
            "",
            "Assuma o leme da 'Libertadora'! Use W-A-S-D para navegar",
            "e proteja sua tripulacao dos arrecifes traicoeiros!"
        ],
        "draw_extra": lambda surf, w, h: (
            # Céu: lua crescente no canto superior direito
            [set_pixel(surf, int(w*0.9)+dx, int(h*0.15)+dy, (255, 255, 200)) 
            for dx in range(-20, 21) for dy in range(-20, 21) 
            if dx*dx + dy*dy <= 20*20 and (dx-5)**2 + dy**2 > 15*15],

            # Estrelas
            [
                [set_pixel(surf, x, y, (255, 255, 255)) or
                set_pixel(surf, x+1, y, (255,255,255)) or
                set_pixel(surf, x-1, y, (255,255,255)) or
                set_pixel(surf, x, y+1, (255,255,255)) or
                set_pixel(surf, x, y-1, (255,255,255))
                for x, y in [(randint(0, w-1), randint(0, int(h*0.5)))]
                ][0]
                for _ in range(150)
            ],
            # Mar: gradiente + ondas
            [
                # Gradiente vertical do mar até a base da tela
                [set_pixel(surf, x, y, (
                    int(25 + (50 - 25) * ((y - int(h*0.6)) / (h - int(h*0.6)))),
                    int(104 + (150 - 104) * ((y - int(h*0.6)) / (h - int(h*0.6)))),
                    int(163 + (200 - 163) * ((y - int(h*0.6)) / (h - int(h*0.6))))
                )) for x in range(w) for y in range(int(h*0.6), h)],
            ],
            [
                draw_jangada(surf, int(w*0.2), int(h*0.75), scale=2.5),
                draw_jangada(surf, int(w*0.5), int(h*0.78), scale=3),
                draw_jangada(surf, int(w*0.7), int(h*0.74), scale=2),
                draw_jangada(surf, int(w*0.85), int(h*0.76), scale=2.2)
            ]
        )
    }
]

# =====================================================
# Função principal
# =====================================================
def run_story(superficie):
    w, h = superficie.get_width(), superficie.get_height()
    slide_index = 0
    clock = pygame.time.Clock()

    music_manager.play("menu")

    while slide_index < len(slides):
        superficie.fill(color.SKY)  # fundo inicial do céu

        # Flood fill do mar
        flood_fill_iterativo(superficie, x=w//2, y=3*h//4, 
                            cor_preenchimento=color.SEA, 
                            cor_borda=color.SKY) 

        slide = slides[slide_index]
        y_text = int(h*0.1)
        for line in slide["texto"]:
            draw_text(superficie, line, 50, y_text, color.TEXT_COLOR, scale=2)
            y_text += 30  # um pouco mais de espaço entre linhas

        # Extras do slide
        slide["draw_extra"](superficie, w, h)

        # Indicação visual de avançar
        draw_text(superficie, "Clique ou pressione ENTER para continuar", 50, h-50, color.TEXT_COLOR, scale=1)

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