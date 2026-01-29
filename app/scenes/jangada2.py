# -*- coding: utf-8 -*-
"""
Jangada renderizada com set_pixel e gradiente de duas cores marrons.
Controle WASD e coleta de peixes.
"""

import pygame
import sys
import random
import math
import assets.colors as color
from engine.framebuffer import set_pixel
from engine.raster.line import bresenham, desenhar_poligono
from engine.fill.scanline import scanline_fill, scanline_fill_gradiente
from engine.math.auxiliary import interpolar_cor
from engine.clipping.cohen_sutherland import cohen_sutherland_clip
from engine.raster.line import bresenham

def draw_raft(superficie, x, y):
    """
    Desenha uma jangada estilizada com gradiente marrom.
    Forma: trapézio alongado (vista de cima) com proa.
    """
    # Dimensões da jangada
    largura_base = 50
    largura_proa = 30
    comprimento = 70
    altura_proa = 15
    
    # Corpo principal (retângulo alongado)
    corpo_pontos = [
        (x, y + altura_proa),
        (x + largura_base, y + altura_proa),
        (x + largura_base, y + altura_proa + comprimento),
        (x, y + altura_proa + comprimento)
    ]
    
    # Preenche corpo com gradiente vertical (marrom escuro → claro)
    scanline_fill_gradiente(
        superficie, 
        corpo_pontos, 
        color.WOOD_DARK, 
        color.WOOD_LIGHT, 
        direcao='vertical'
    )
    
    # Contorno do corpo
    desenhar_poligono(superficie, corpo_pontos, color.DETAIL_COLOR)
    
    # Proa (triângulo na frente)
    proa_pontos = [
        (x + (largura_base - largura_proa) // 2, y),
        (x + (largura_base + largura_proa) // 2, y),
        (x + largura_base // 2, y + altura_proa)
    ]
    
    # Preenche proa com gradiente (mais escuro na ponta)
    scanline_fill_gradiente(
        superficie,
        proa_pontos,
        color.WOOD_DARK,
        color.WOOD_LIGHT,
        direcao='vertical'
    )
    
    # Contorno da proa
    desenhar_poligono(superficie, proa_pontos, color.DETAIL_COLOR)
    
    # Detalhes: linhas horizontais (tábuas)
    for i in range(3):
        y_tabua = y + altura_proa + 15 + i * 18
        bresenham(
            superficie,
            x + 5,
            y_tabua,
            x + largura_base - 5,
            y_tabua,
            color.DETAIL_COLOR
        )
    
    # Detalhe central (mastro ou estrutura)
    centro_x = x + largura_base // 2
    centro_y = y + altura_proa + comprimento // 2
    bresenham(
        superficie,
        centro_x - 3,
        centro_y - 5,
        centro_x + 3,
        centro_y - 5,
        color.DETAIL_COLOR
    )
    bresenham(
        superficie,
        centro_x,
        centro_y - 5,
        centro_x,
        centro_y + 5,
        color.DETAIL_COLOR
    )


def draw_fish_icon(superficie, x, y, tamanho=8):
    """
    Desenha um pequeno ícone de peixe para o contador.
    """
    # Corpo pequeno (elipse)
    a = tamanho // 2
    b = tamanho // 3
    for dy in range(-b, b + 1):
        for dx in range(-a, a + 1):
            if a > 0 and b > 0:
                if (dx * dx) / (a * a) + (dy * dy) / (b * b) <= 1:
                    t = (dy + b) / (2 * b) if b > 0 else 0.5
                    if t < 0.5:
                        t_grad = t * 2
                    else:
                        t_grad = (1 - t) * 2
                    cor = interpolar_cor(color.FISH_BLUE, color.FISH_WHITE, t_grad)
                    set_pixel(superficie, x + dx, y + dy, cor)
    
    # Cauda
    cauda_pontos = [
        (x - a - 1, y),
        (x - a - 3, y - 2),
        (x - a - 3, y + 2)
    ]
    scanline_fill(superficie, cauda_pontos, color.FISH_BLUE)
    desenhar_poligono(superficie, cauda_pontos, color.FISH_OUTLINE)


def draw_heart_icon(superficie, x, y, tamanho=6):
    for dy in range(tamanho * 2):
        for dx in range(tamanho * 2):
            nx = (dx - tamanho) / tamanho
            ny = (dy - tamanho) / tamanho
            val = (nx*nx + ny*ny - 1)**3 - nx*nx*ny*ny*ny
            if val <= 0:
                cor = color.HEART_RED if ny < 0 else color.HEART_DARK
                set_pixel(superficie, x + dx, y + dy, cor)


def draw_simple_text(superficie, texto, x, y, cor):
    """
    Desenha texto simples usando apenas set_pixel.
    Versão minimalista para números e letras básicas.
    """
    # Fonte 3x5 simplificada para números e algumas letras
    chars = {
        '0': ['XXX', 'X X', 'X X', 'X X', 'XXX'],
        '1': [' X ', 'XX ', ' X ', ' X ', 'XXX'],
        '2': ['XXX', '  X', 'XXX', 'X  ', 'XXX'],
        '3': ['XXX', '  X', 'XXX', '  X', 'XXX'],
        '4': ['X X', 'X X', 'XXX', '  X', '  X'],
        '5': ['XXX', 'X  ', 'XXX', '  X', 'XXX'],
        '6': ['XXX', 'X  ', 'XXX', 'X X', 'XXX'],
        '7': ['XXX', '  X', '  X', '  X', '  X'],
        '8': ['XXX', 'X X', 'XXX', 'X X', 'XXX'],
        '9': ['XXX', 'X X', 'XXX', '  X', 'XXX'],
        'P': ['XXX', 'X X', 'XXX', 'X  ', 'X  '],
        ':': ['   ', ' X ', '   ', ' X ', '   '],
    }
    
    dx = 0
    for c in texto:
        if c in chars:
            pattern = chars[c]
            for row, line in enumerate(pattern):
                for col, pixel in enumerate(line):
                    if pixel == 'X':
                        set_pixel(superficie, x + dx + col, y + row, cor)
        dx += 4  # Espaço entre caracteres


def draw_fish(superficie, x, y):
    """
    Desenha um peixe detalhado com gradiente azul e branco.
    Forma: corpo oval + cauda + barbatanas.
    """
    # Corpo principal (oval alongado)
    corpo_largura = 20
    corpo_altura = 12
    corpo_x = x
    corpo_y = y
    
    # Desenha corpo com gradiente (azul → branco → azul)
    for dy in range(-corpo_altura // 2, corpo_altura // 2 + 1):
        for dx in range(-corpo_largura // 2, corpo_largura // 2 + 1):
            # Fórmula de elipse: (dx/a)² + (dy/b)² <= 1
            a = corpo_largura // 2
            b = corpo_altura // 2
            if a > 0 and b > 0:
                if (dx * dx) / (a * a) + (dy * dy) / (b * b) <= 1:
                    # Gradiente vertical: azul no topo, branco no meio, azul embaixo
                    t = (dy + b) / (2 * b) if b > 0 else 0.5
                    # Cria gradiente simétrico (azul → branco → azul)
                    if t < 0.5:
                        t_grad = t * 2  # 0 → 1 (topo → meio)
                    else:
                        t_grad = (1 - t) * 2  # 1 → 0 (meio → base)
                    
                    cor = interpolar_cor(color.FISH_BLUE, color.FISH_WHITE, t_grad)
                    set_pixel(superficie, corpo_x + dx, corpo_y + dy, cor)
    
    # Contorno do corpo
    for dy in range(-corpo_altura // 2, corpo_altura // 2 + 1):
        for dx in range(-corpo_largura // 2, corpo_largura // 2 + 1):
            a = corpo_largura // 2
            b = corpo_altura // 2
            if a > 0 and b > 0:
                dist = (dx * dx) / (a * a) + (dy * dy) / (b * b)
                # Contorno: pixels na borda da elipse
                if 0.85 <= dist <= 1.0:
                    set_pixel(superficie, corpo_x + dx, corpo_y + dy,color.FISH_OUTLINE)
    
    # Cauda (barbatana traseira)
    cauda_pontos = [
        (corpo_x - corpo_largura // 2 - 2, corpo_y),
        (corpo_x - corpo_largura // 2 - 8, corpo_y - 6),
        (corpo_x - corpo_largura // 2 - 8, corpo_y + 6)
    ]
    scanline_fill_gradiente(superficie, cauda_pontos, color.FISH_BLUE, color.FISH_WHITE, direcao='vertical')
    desenhar_poligono(superficie, cauda_pontos, color.FISH_OUTLINE)
    
    # Barbatana superior
    barbatana_sup_pontos = [
        (corpo_x + 2, corpo_y - corpo_altura // 2),
        (corpo_x + 8, corpo_y - corpo_altura // 2 - 4),
        (corpo_x + 12, corpo_y - corpo_altura // 2)
    ]
    scanline_fill_gradiente(superficie, barbatana_sup_pontos, color.FISH_BLUE, color.FISH_WHITE, direcao='vertical')
    desenhar_poligono(superficie, barbatana_sup_pontos, color.FISH_OUTLINE)
    
    # Barbatana inferior
    barbatana_inf_pontos = [
        (corpo_x + 2, corpo_y + corpo_altura // 2),
        (corpo_x + 8, corpo_y + corpo_altura // 2 + 4),
        (corpo_x + 12, corpo_y + corpo_altura // 2)
    ]
    scanline_fill_gradiente(superficie, barbatana_inf_pontos, color.FISH_BLUE, color.FISH_WHITE, direcao='vertical')
    desenhar_poligono(superficie, barbatana_inf_pontos, color.FISH_OUTLINE)
    
    # Olho
    olho_x = corpo_x + 4
    olho_y = corpo_y - 2
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            if dx * dx + dy * dy <= 4:
                if dx * dx + dy * dy <= 1:
                    set_pixel(superficie, olho_x + dx, olho_y + dy, (255, 255, 255))  # Branco
                else:
                    set_pixel(superficie, olho_x + dx, olho_y + dy, (0, 0, 0))  # Preto


def draw_waves_around_fish(superficie, x, y, offset_y):
    """
    Desenha pequenas ondas ao redor do peixe, simulando movimento na água.
    offset_y: offset vertical do peixe (para sincronizar com animação)
    """
    # Raio das ondas
    raio_onda = 25
    
    # Desenha círculos concêntricos (ondas)
    for r in range(raio_onda - 8, raio_onda + 1, 2):
        # Usa seno para criar ondas irregulares
        num_pontos = 32
        pontos_onda = []
        for i in range(num_pontos):
            angulo = (i / num_pontos) * 2 * math.pi
            # Adiciona variação baseada no offset_y para animação
            variacao = math.sin(angulo * 3 + offset_y * 0.1) * 2
            px = int(x + (r + variacao) * math.cos(angulo))
            py = int(y + (r + variacao) * math.sin(angulo))
            pontos_onda.append((px, py))
        
        # Desenha a onda como linhas conectadas
        for i in range(len(pontos_onda)):
            x0, y0 = pontos_onda[i]
            x1, y1 = pontos_onda[(i + 1) % len(pontos_onda)]
            # Só desenha se estiver dentro da tela
            if 0 <= x0 < superficie.get_width() and 0 <= y0 < superficie.get_height():
                bresenham(superficie, x0, y0, x1, y1, color.WAVE_COLOR)


def check_collision(raft_x, raft_y, fish_x, fish_y):
    """
    Verifica colisão entre jangada e peixe.
    Jangada: aproximadamente 50x85 pixels (incluindo proa)
    Peixe: aproximadamente 28x12 pixels (corpo + cauda + barbatanas)
    """
    # Área aproximada da jangada
    raft_w = 50
    raft_h = 85  # altura_proa (15) + comprimento (70)
    raft_left = raft_x
    raft_top = raft_y
    raft_right = raft_x + raft_w
    raft_bottom = raft_top + raft_h
    
    # Área aproximada do peixe (corpo 20x12 + cauda ~8 pixels)
    fish_w = 28
    fish_h = 12
    fish_left = fish_x - fish_w // 2
    fish_right = fish_x + fish_w // 2
    fish_top = fish_y - fish_h // 2
    fish_bottom = fish_y + fish_h // 2
    
    # Verifica sobreposição de retângulos (AABB)
    return not (raft_right < fish_left or 
                raft_left > fish_right or 
                raft_bottom < fish_top or 
                raft_top > fish_bottom)


def draw_obstacle(superficie, x, y, tamanho=14):
    """
    Obstáculo simples (rocha) vista de cima
    """
    for dy in range(-tamanho, tamanho + 1):
        for dx in range(-tamanho, tamanho + 1):
            if dx*dx + dy*dy <= tamanho*tamanho:
                cor = (80, 80, 90)
                if dx*dx + dy*dy > (tamanho-2)*(tamanho-2):
                    cor = (50, 50, 60)  # contorno
                set_pixel(superficie, x + dx, y + dy, cor)


def check_collision_obstacle(raft_x, raft_y, obs_x, obs_y):
    raft_w = 50
    raft_h = 85

    obs_r = 14

    raft_left = raft_x
    raft_right = raft_x + raft_w
    raft_top = raft_y
    raft_bottom = raft_y + raft_h

    obs_left = obs_x - obs_r
    obs_right = obs_x + obs_r
    obs_top = obs_y - obs_r
    obs_bottom = obs_y + obs_r

    return not (
        raft_right < obs_left or
        raft_left > obs_right or
        raft_bottom < obs_top or
        raft_top > obs_bottom
    )

def draw_minimap(
    superficie,
    raft_x, raft_y,
    fish_x, fish_y,
    obstaculos,
    camera_x, camera_y,
    WORLD_WIDTH, WORLD_HEIGHT,
    WIDTH, HEIGHT
):
    # Tamanho do minimapa
    MAP_W = 180
    MAP_H = 180
    MAP_X = WIDTH - MAP_W - 15
    MAP_Y = 15

    # Fundo
    for y in range(MAP_H):
        for x in range(MAP_W):
            set_pixel(superficie, MAP_X + x, MAP_Y + y, (20, 40, 60))

    # Escala mundo → minimapa
    sx = MAP_W / WORLD_WIDTH
    sy = MAP_H / WORLD_HEIGHT

    # ===== VIEWPORT (retângulo da câmera) =====
    vx = int(camera_x * sx)
    vy = int(camera_y * sy)
    vw = int(WIDTH * sx)
    vh = int(HEIGHT * sy)

    # Contorno do viewport
    for i in range(vw):
        set_pixel(superficie, MAP_X + vx + i, MAP_Y + vy, (255, 255, 255))
        set_pixel(superficie, MAP_X + vx + i, MAP_Y + vy + vh, (255, 255, 255))

    for i in range(vh):
        set_pixel(superficie, MAP_X + vx, MAP_Y + vy + i, (255, 255, 255))
        set_pixel(superficie, MAP_X + vx + vw, MAP_Y + vy + i, (255, 255, 255))

    # ===== PEIXE =====
    px = int(fish_x * sx)
    py = int(fish_y * sy)
    set_pixel(superficie, MAP_X + px, MAP_Y + py, color.FISH_BLUE)

    # ===== OBSTÁCULOS =====
    for obs in obstaculos:
        ox = int(obs[0] * sx)
        oy = int(obs[1] * sy)
        set_pixel(superficie, MAP_X + ox, MAP_Y + oy, (120, 120, 120))

    # ===== JANGADA (PLAYER) =====
    rx = int(raft_x * sx)
    ry = int(raft_y * sy)

    for dy in range(-2, 3):
        for dx in range(-2, 3):
            set_pixel(
                superficie,
                MAP_X + rx + dx,
                MAP_Y + ry + dy,
                (255, 255, 255)
            )

def main():
    pygame.init()
    
    # ===== VIEWPORT (TELA) =====
    WIDTH, HEIGHT = 1000, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jangada das Estrelas - Gameplay")
    
    clock = pygame.time.Clock()

    # ===== JANELA (MUNDO) =====
    WORLD_WIDTH = 3000
    WORLD_HEIGHT = 3000

    # ===== POSIÇÕES NO MUNDO =====
    raft_x = WORLD_WIDTH // 2
    raft_y = WORLD_HEIGHT // 2
    speed = 4

    # Peixe no mundo
    fish_x = random.randint(100, WORLD_WIDTH - 100)
    fish_y_base = random.randint(100, WORLD_HEIGHT - 100)
    fish_y = fish_y_base

    # Animação do peixe
    fish_animation_offset = 0.0
    fish_animation_speed = 0.15
    fish_animation_range = 8

    # Obstáculos no mundo
    NUM_OBSTACULOS = 5
    obstaculos = []
    while len(obstaculos) < NUM_OBSTACULOS:
        ox = random.randint(100, WORLD_WIDTH - 100)
        oy = random.randint(100, WORLD_HEIGHT - 100)

        if abs(ox - fish_x) < 80 and abs(oy - fish_y_base) < 80:
            continue

        obstaculos.append([ox, oy])

    pontos = 0
    vidas = 3

    running = True
    while running:
        screen.fill(color.SEA_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # ===== INPUT (MOVE NO MUNDO) =====
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            raft_y -= speed
        if keys[pygame.K_s]:
            raft_y += speed
        if keys[pygame.K_a]:
            raft_x -= speed
        if keys[pygame.K_d]:
            raft_x += speed

        # Limites do MUNDO
        raft_x = max(0, min(WORLD_WIDTH - 50, raft_x))
        raft_y = max(0, min(WORLD_HEIGHT - 85, raft_y))

        # ===== CÂMERA (VIEWPORT) =====
        camera_x = raft_x - WIDTH // 2
        camera_y = raft_y - HEIGHT // 2

        camera_x = max(0, min(WORLD_WIDTH - WIDTH, camera_x))
        camera_y = max(0, min(WORLD_HEIGHT - HEIGHT, camera_y))

        # ===== ANIMAÇÃO DO PEIXE =====
        fish_animation_offset += fish_animation_speed
        fish_y = fish_y_base + math.sin(fish_animation_offset) * fish_animation_range

        # ===== COLISÕES (EM COORDENADAS DO MUNDO) =====
        if check_collision(raft_x, raft_y, fish_x, fish_y_base):
            pontos += 1
            fish_x = random.randint(100, WORLD_WIDTH - 100)
            fish_y_base = random.randint(100, WORLD_HEIGHT - 100)
            fish_animation_offset = 0.0

        for obs in obstaculos[:]:
            if check_collision_obstacle(raft_x, raft_y, obs[0], obs[1]):
                vidas -= 1
                obstaculos.remove(obs)
                break

        if vidas <= 0:
            running = False
            resultado = "GAME OVER"
        elif pontos >= 5:
            running = False
            resultado = "VITORIA"

        # ===== DESENHO (MUNDO → VIEWPORT) =====
        draw_waves_around_fish(
            screen,
            fish_x - camera_x,
            fish_y_base - camera_y,
            fish_animation_offset
        )

        draw_fish(
            screen,
            fish_x - camera_x,
            int(fish_y - camera_y)
        )

        for obs in obstaculos:
            draw_obstacle(
                screen,
                obs[0] - camera_x,
                obs[1] - camera_y
            )

        draw_raft(
            screen,
            raft_x - camera_x,
            raft_y - camera_y
        )

        draw_minimap(
            screen,
            raft_x, raft_y,
            fish_x, fish_y_base,
            obstaculos,
            camera_x, camera_y,
            WORLD_WIDTH, WORLD_HEIGHT,
            WIDTH, HEIGHT
        )


        # ===== HUD (NÃO USA CÂMERA) =====
        draw_heart_icon(screen, 10, 28, tamanho=5)
        draw_simple_text(screen, str(vidas), 28, 30, (255, 255, 255))

        draw_fish_icon(screen, 10, 10, tamanho=10)
        draw_simple_text(screen, str(pontos), 25, 10, (255, 255, 255))

        pygame.display.flip()
        clock.tick(60)

    # ===== TELA FINAL =====
    screen.fill(color.SEA_COLOR)
    if resultado == "GAME OVER":
        draw_simple_text(screen, "0", WIDTH//2 - 6, HEIGHT//2, color.GAME_OVER_RED)
        draw_simple_text(screen, "P", WIDTH//2 - 6, HEIGHT//2 + 10, color.GAME_OVER_RED)
    else:
        draw_simple_text(screen, "5", WIDTH//2 - 6, HEIGHT//2, color.WIN_GREEN)
        draw_simple_text(screen, "P", WIDTH//2 - 6, HEIGHT//2 + 10, color.WIN_GREEN)

    pygame.display.flip()
    pygame.time.delay(2500)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
