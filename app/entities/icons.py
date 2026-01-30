
import assets.colors as color
from engine.math.auxiliary import interpolar_cor
from engine.fill.scanline import scanline_fill
from engine.raster.line import desenhar_poligono
from app.scenes.auxiliary_functions import _set_pixel_scaled

def draw_fish_icon(superficie, x, y, tamanho=8, scale=1):
    """
    Desenha um pequeno ícone de peixe para o contador.
    scale: 1 = normal; 2 = cada pixel vira bloco 2x2 (só set_pixel).
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
                    _set_pixel_scaled(superficie, x, y, dx, dy, cor, scale)
    
    # Cauda
    cauda_pontos = [
        (x - a - 1, y),
        (x - a - 3, y - 2),
        (x - a - 3, y + 2)
    ]
    if scale == 1:
        scanline_fill(superficie, cauda_pontos, color.FISH_BLUE)
        desenhar_poligono(superficie, cauda_pontos, color.FISH_OUTLINE)
    else:
        cauda_esc = [(x + (px - x) * scale, y + (py - y) * scale) for px, py in cauda_pontos]
        scanline_fill(superficie, cauda_esc, color.FISH_BLUE)
        desenhar_poligono(superficie, cauda_esc, color.FISH_OUTLINE)


def draw_heart_icon(superficie, x, y, tamanho=6, scale=1):
    """Ícone de coração; scale=2 desenha cada pixel como bloco 2×2 (só set_pixel)."""
    for dy in range(tamanho * 2):
        for dx in range(tamanho * 2):
            nx = (dx - tamanho) / tamanho
            ny = (dy - tamanho) / tamanho
            val = (nx*nx + ny*ny - 1)**3 - nx*nx*ny*ny*ny
            if val <= 0:
                cor = color.HEART_RED if ny < 0 else color.HEART_DARK
                _set_pixel_scaled(superficie, x, y, dx, dy, cor, scale)
