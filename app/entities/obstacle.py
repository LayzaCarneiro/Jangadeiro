
from engine.framebuffer import set_pixel
import random

def draw_obstacle(superficie, x, y, tamanho=14, tipo=None):
    """
    Desenha um obstáculo com múltiplos tipos.
    
    Args:
        superficie: pygame.Surface
        x, y: posição
        tamanho: tamanho do obstáculo
        tipo: tipo de obstáculo (0 = rocha, 1 = alga, 2 = coral)
    """
    # Se tipo não for especificado, usa rocha (padrão)
    if tipo is None:
        tipo = 0
    
    if tipo == 0:
        # Rocha (cinza)
        draw_rock(superficie, x, y, tamanho)
    elif tipo == 1:
        # Alga (verde)
        draw_seaweed(superficie, x, y, tamanho)
    else:
        # Coral (laranja)
        draw_coral(superficie, x, y, tamanho)


def draw_rock(superficie, x, y, tamanho=14):
    """Rocha cinza com textura e sombreado"""
    for dy in range(-tamanho, tamanho + 1):
        for dx in range(-tamanho, tamanho + 1):
            dist = dx*dx + dy*dy
            if dist <= tamanho*tamanho:
                # Gradiente radial para volume
                intensidade = 1.0 - (dist / (tamanho*tamanho))
                # Cinza claro no centro, cinza escuro nas bordas
                base_cor = int(100 + intensidade * 30)
                cor = (base_cor, base_cor, base_cor + 10)
                set_pixel(superficie, x + dx, y + dy, cor)
            elif dist <= (tamanho+2)*(tamanho+2):
                # Contorno mais escuro
                set_pixel(superficie, x + dx, y + dy, (40, 40, 50))


def draw_seaweed(superficie, x, y, tamanho=14):
    """Alga ondulante com padrão de folhas"""
    import math
    for dy in range(-tamanho, tamanho + 1):
        for dx in range(-tamanho, tamanho + 1):
            # Forma ondulante (elipse horizontal com variação)
            largura = tamanho + int(3 * math.sin(dy * 0.3))
            altura = int(tamanho * 0.8)
            
            if abs(dy) <= altura and abs(dx) <= largura//2:
                # Verde variado com padrão
                verde_base = 150 - abs(dx) * 5
                cor = (40, verde_base, 80)
                
                # Padrão de listras verticais
                if dx % 3 == 0:
                    cor = (60, verde_base + 30, 100)
                
                set_pixel(superficie, x + dx, y + dy, cor)
            elif abs(dx) <= largura//2 and abs(dy) <= altura + 2:
                # Contorno verde mais escuro
                set_pixel(superficie, x + dx, y + dy, (20, 80, 50))


def draw_coral(superficie, x, y, tamanho=14):
    """Coral em forma de árvore/ramificações"""
    import math
    for dy in range(-tamanho, tamanho + 1):
        for dx in range(-tamanho, tamanho + 1):
            # Tronco principal (centro)
            if abs(dx) <= 2 and dy >= -tamanho:
                cor = (200, 100, 40)
                set_pixel(superficie, x + dx, y + dy, cor)
            
            # Ramificações diagonais (padrão coral)
            elif abs(dy) < tamanho:
                # Lado esquerdo
                if dx <= -3 and dx >= -(tamanho//2) and dy >= (dx // 2) - 2:
                    dist_ramo = abs(dx) + abs(dy)
                    if dist_ramo < tamanho:
                        intensidade = 1.0 - (dist_ramo / tamanho)
                        cor_val = int(200 - intensidade * 50)
                        cor = (cor_val, int(100 + intensidade * 30), int(40 + intensidade * 20))
                        set_pixel(superficie, x + dx, y + dy, cor)
                
                # Lado direito
                elif dx >= 3 and dx <= (tamanho//2) and dy >= (-dx // 2) - 2:
                    dist_ramo = abs(dx) + abs(dy)
                    if dist_ramo < tamanho:
                        intensidade = 1.0 - (dist_ramo / tamanho)
                        cor_val = int(200 - intensidade * 50)
                        cor = (cor_val, int(100 + intensidade * 30), int(40 + intensidade * 20))
                        set_pixel(superficie, x + dx, y + dy, cor)
