
import math
import assets.colors as color
from engine.framebuffer import set_pixel
from engine.math.auxiliary import interpolar_cor
from engine.fill.scanline import scanline_fill_gradiente
from engine.raster.line import bresenham, desenhar_poligono

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

