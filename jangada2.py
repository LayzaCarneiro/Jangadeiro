# -*- coding: utf-8 -*-
"""
Jangada renderizada com set_pixel e gradiente de duas cores marrons.
Controle WASD e coleta de peixes.
"""

import pygame
import sys
import random
import math
from engine.framebuffer import set_pixel
from engine.raster.line import bresenham, desenhar_poligono
from engine.fill.scanline import scanline_fill

# Cores
SEA_COLOR = (0, 120, 170)
WOOD_DARK = (92, 64, 51)      # Marrom escuro
WOOD_LIGHT = (181, 136, 99)   # Marrom claro
FISH_BLUE = (50, 150, 255)    # Azul do peixe
FISH_WHITE = (200, 230, 255)  # Branco do peixe
FISH_OUTLINE = (30, 100, 200) # Contorno do peixe
WAVE_COLOR = (100, 180, 220)  # Cor das ondas
DETAIL_COLOR = (60, 40, 30)   # Contorno escuro


def interpolar_cor(cor1, cor2, t):
    """
    Interpola linearmente entre duas cores RGB.
    t: 0.0 = cor1, 1.0 = cor2
    """
    r1, g1, b1 = cor1
    r2, g2, b2 = cor2
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    return (r, g, b)


def scanline_fill_gradiente(superficie, pontos, cor_inicio, cor_fim, direcao='vertical'):
    """
    Preenche polígono com gradiente linear.
    direcao: 'vertical' (de cima para baixo) ou 'horizontal' (esquerda para direita)
    """
    ys = [p[1] for p in pontos]
    xs = [p[0] for p in pontos]
    y_min = min(ys)
    y_max = max(ys)
    x_min = min(xs)
    x_max = max(xs)
    
    n = len(pontos)
    
    for y in range(y_min, y_max):
        intersecoes_x = []
        
        for i in range(n):
            x0, y0 = pontos[i]
            x1, y1 = pontos[(i + 1) % n]
            
            if y0 == y1:
                continue
            
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            
            if y < y0 or y >= y1:
                continue
            
            x = x0 + (y - y0) * (x1 - x0) / (y1 - y0)
            intersecoes_x.append(x)
        
        intersecoes_x.sort()
        
        for i in range(0, len(intersecoes_x), 2):
            if i + 1 < len(intersecoes_x):
                x_inicio = int(round(intersecoes_x[i]))
                x_fim = int(round(intersecoes_x[i + 1]))
                
                for x in range(x_inicio, x_fim + 1):
                    if direcao == 'vertical':
                        # Gradiente vertical: t baseado em y
                        if y_max != y_min:
                            t = (y - y_min) / (y_max - y_min)
                        else:
                            t = 0.5
                    else:
                        # Gradiente horizontal: t baseado em x
                        if x_max != x_min:
                            t = (x - x_min) / (x_max - x_min)
                        else:
                            t = 0.5
                    
                    cor = interpolar_cor(cor_inicio, cor_fim, t)
                    set_pixel(superficie, x, y, cor)


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
        WOOD_DARK, 
        WOOD_LIGHT, 
        direcao='vertical'
    )
    
    # Contorno do corpo
    desenhar_poligono(superficie, corpo_pontos, DETAIL_COLOR)
    
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
        WOOD_DARK,
        WOOD_LIGHT,
        direcao='vertical'
    )
    
    # Contorno da proa
    desenhar_poligono(superficie, proa_pontos, DETAIL_COLOR)
    
    # Detalhes: linhas horizontais (tábuas)
    for i in range(3):
        y_tabua = y + altura_proa + 15 + i * 18
        bresenham(
            superficie,
            x + 5,
            y_tabua,
            x + largura_base - 5,
            y_tabua,
            DETAIL_COLOR
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
        DETAIL_COLOR
    )
    bresenham(
        superficie,
        centro_x,
        centro_y - 5,
        centro_x,
        centro_y + 5,
        DETAIL_COLOR
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
                    cor = interpolar_cor(FISH_BLUE, FISH_WHITE, t_grad)
                    set_pixel(superficie, x + dx, y + dy, cor)
    
    # Cauda
    cauda_pontos = [
        (x - a - 1, y),
        (x - a - 3, y - 2),
        (x - a - 3, y + 2)
    ]
    scanline_fill(superficie, cauda_pontos, FISH_BLUE)
    desenhar_poligono(superficie, cauda_pontos, FISH_OUTLINE)


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
                    
                    cor = interpolar_cor(FISH_BLUE, FISH_WHITE, t_grad)
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
                    set_pixel(superficie, corpo_x + dx, corpo_y + dy, FISH_OUTLINE)
    
    # Cauda (barbatana traseira)
    cauda_pontos = [
        (corpo_x - corpo_largura // 2 - 2, corpo_y),
        (corpo_x - corpo_largura // 2 - 8, corpo_y - 6),
        (corpo_x - corpo_largura // 2 - 8, corpo_y + 6)
    ]
    scanline_fill_gradiente(superficie, cauda_pontos, FISH_BLUE, FISH_WHITE, direcao='vertical')
    desenhar_poligono(superficie, cauda_pontos, FISH_OUTLINE)
    
    # Barbatana superior
    barbatana_sup_pontos = [
        (corpo_x + 2, corpo_y - corpo_altura // 2),
        (corpo_x + 8, corpo_y - corpo_altura // 2 - 4),
        (corpo_x + 12, corpo_y - corpo_altura // 2)
    ]
    scanline_fill_gradiente(superficie, barbatana_sup_pontos, FISH_BLUE, FISH_WHITE, direcao='vertical')
    desenhar_poligono(superficie, barbatana_sup_pontos, FISH_OUTLINE)
    
    # Barbatana inferior
    barbatana_inf_pontos = [
        (corpo_x + 2, corpo_y + corpo_altura // 2),
        (corpo_x + 8, corpo_y + corpo_altura // 2 + 4),
        (corpo_x + 12, corpo_y + corpo_altura // 2)
    ]
    scanline_fill_gradiente(superficie, barbatana_inf_pontos, FISH_BLUE, FISH_WHITE, direcao='vertical')
    desenhar_poligono(superficie, barbatana_inf_pontos, FISH_OUTLINE)
    
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
                bresenham(superficie, x0, y0, x1, y1, WAVE_COLOR)


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


def main():
    pygame.init()
    
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jangada das Estrelas - Gameplay")
    
    clock = pygame.time.Clock()
    
    # Posições iniciais
    raft_x = WIDTH // 2 - 25
    raft_y = HEIGHT // 2 - 42
    speed = 4
    
    # Peixe inicial
    fish_x = random.randint(50, WIDTH - 50)
    fish_y_base = random.randint(200, HEIGHT - 200)  # Posição base (centro da animação)
    fish_y = fish_y_base
    
    # Animação do peixe
    fish_animation_offset = 0.0
    fish_animation_speed = 0.15
    fish_animation_range = 8  # Amplitude da animação (pixels)
    
    # Pontuação
    pontos = 0
    
    running = True
    frame_count = 0
    while running:
        frame_count += 1
        
        # Limpa tela (usa fill para performance, mas todo o resto é set_pixel)
        screen.fill(SEA_COLOR)
        
        # Processa eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Input (WASD)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            raft_y -= speed
        if keys[pygame.K_s]:
            raft_y += speed
        if keys[pygame.K_a]:
            raft_x -= speed
        if keys[pygame.K_d]:
            raft_x += speed
        
        # Limites da tela
        raft_x = max(0, min(WIDTH - 50, raft_x))
        raft_y = max(0, min(HEIGHT - 85, raft_y))
        
        # Animação do peixe (sobe e desce)
        fish_animation_offset += fish_animation_speed
        fish_y = fish_y_base + math.sin(fish_animation_offset) * fish_animation_range
        
        # Colisão jangada × peixe (usa posição base para consistência)
        if check_collision(raft_x, raft_y, fish_x, fish_y_base):
            pontos += 1
            # Reposiciona peixe
            fish_x = random.randint(50, WIDTH - 50)
            fish_y_base = random.randint(200, HEIGHT - 200)
            fish_y = fish_y_base
            fish_animation_offset = 0.0
        
        # Renderização (tudo via set_pixel)
        # Desenha ondas primeiro (atrás do peixe)
        draw_waves_around_fish(screen, fish_x, fish_y_base, fish_animation_offset)
        
        # Desenha peixe
        draw_fish(screen, fish_x, int(fish_y))
        
        # Desenha jangada
        draw_raft(screen, raft_x, raft_y)
        
        # Pontuação com ícone de peixe
        # Ícone de peixe
        draw_fish_icon(screen, 10, 10, tamanho=10)
        # Número de pontos
        draw_simple_text(screen, str(pontos), 25, 10, (255, 255, 255))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
