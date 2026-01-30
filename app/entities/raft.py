# ═══════════════════════════════════════════════════════════════
# JANGADA (PLAYER)
# ═══════════════════════════════════════════════════════════════
# Representa o jogador no jogo.
#
# Demonstra os seguintes requisitos:
# - (b) Primitivas: polígonos com desenhar_poligono
# - (c) Preenchimento: scanline_fill_gradiente
# - (d) Transformações: rotação em torno de pivô ao colidir
# - (e) Animação: rotação 360° em colisão
# ═══════════════════════════════════════════════════════════════

import app.constants as constant
import assets.colors as color
from engine.geometry.cohen_sutherland import draw_line
from engine.raster.line import bresenham, desenhar_poligono
from engine.geometry.transform import rotacionar_pontos_em_torno_de
from engine.fill.scanline import scanline_fill_gradiente, scanline_fill

def draw_raft(superficie, x, y, viewport, angle=0):
    """
    Desenha a jangada do jogador com gradiente e detalhes.
    
    REQUISITOS:
    - (b) Primitivas gráficas: polígonos (corpo + proa)
    - (c) Preenchimento: scanline_fill_gradiente (madeira)
    - (d) Transformações: rotação em torno do centro (colisão)
    
    Estrutura:
    - Corpo retangular (madeira com gradiente vertical)
    - Proa triangular (frente da jangada)
    - Linhas de detalhe (tábuas e mastro)
    
    Args:
        superficie: pygame.Surface
        x, y: posição do canto superior esquerdo
        viewport: tupla (xmin, ymin, w, h) para clipping
        angle: ângulo de rotação em radianos (0 = sem rotação)
    """
    largura_base = constant.RAFT_LARGURA
    comprimento = constant.COMPRIMENTO

    cx = x + largura_base // 2
    cy = y + comprimento // 2

    # Corpo principal (retângulo alongado)
    corpo = [
        (x, y),
        (x + largura_base, y),
        (x + largura_base, y + comprimento),
        (x, y + comprimento)
    ]

    # Rotação opcional
    if angle != 0:
        corpo = rotacionar_pontos_em_torno_de(corpo, cx, cy, angle)

    # Preenchimento do corpo com gradiente simples
    scanline_fill_gradiente(superficie, corpo, color.WOOD_DARK, color.WOOD_LIGHT, direcao="vertical")
    desenhar_poligono(superficie, corpo, color.DETAIL_COLOR)

    # Linhas representando tábuas
    for i in range(1, 3):
        y_tabua = y + i * (comprimento // 3)
        draw_line(superficie, x + 2, y_tabua, x + largura_base - 2, y_tabua, color.DETAIL_COLOR, viewport=viewport)

    # Jangadeiro: chapéu cônico simples no centro do retângulo
    chapeu = [
        (cx - 6, cy - 4),
        (cx + 6, cy - 4),
        (cx, cy - 12)
    ]
    scanline_fill_gradiente(superficie, chapeu, color.WOOD_LIGHT, color.WOOD_DARK, direcao="vertical")
    desenhar_poligono(superficie, chapeu, color.DETAIL_COLOR)

def draw_jangada(surf, x, y, scale=1):
    """Desenha uma jangada simples como polígono."""
    points = [
        (x, y),
        (x + 50*scale, y),
        (x + 40*scale, y + 10*scale),
        (x + 10*scale, y + 10*scale)
    ]
    scanline_fill(surf, points, color.JANGADA_COLOR)
    desenhar_poligono(surf, points, (0, 0, 0))
    # mastro
    desenhar_poligono(surf, [(x+25*scale, y), (x+25*scale, y-30*scale)], (0,0,0))
    # vela
    sail = [(x+25*scale, y-30*scale), (x+45*scale, y-10*scale), (x+25*scale, y)]
    scanline_fill(surf, sail, (255, 255, 255))
    desenhar_poligono(surf, sail, (0,0,0))
