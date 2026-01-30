
import app.constants as constant
import assets.colors as color
from engine.geometry.cohen_sutherland import draw_line
from engine.raster.line import bresenham, desenhar_poligono
from engine.geometry.transform import rotacionar_pontos_em_torno_de
from engine.fill.scanline import scanline_fill_gradiente

def draw_raft(superficie, x, y, viewport, angle=0):
    """
    Desenha uma jangada estilizada com gradiente marrom.
    angle: rotação em radianos em torno do centro da jangada (0 = sem rotação).
    """
    largura_base = constant.RAFT_LARGURA
    largura_proa = 30
    comprimento = constant.COMPRIMENTO
    altura_proa = constant.ALTURA_PROA

    cx = x + largura_base // 2
    cy = y + altura_proa + comprimento // 2

    # Corpo principal (retângulo alongado)
    corpo_pontos = [
        (x, y + altura_proa),
        (x + largura_base, y + altura_proa),
        (x + largura_base, y + altura_proa + comprimento),
        (x, y + altura_proa + comprimento),
    ]

    # Proa (triângulo na frente)
    proa_pontos = [
        (x + (largura_base - largura_proa) // 2, y),
        (x + (largura_base + largura_proa) // 2, y),
        (x + largura_base // 2, y + altura_proa),
    ]

    # Pontos das linhas de detalhe (tábuas e mastro)
    linhas_detalhe = []
    for i in range(3):
        y_tabua = y + altura_proa + 15 + i * 18
        linhas_detalhe.append(((x + 5, y_tabua), (x + largura_base - 5, y_tabua)))
    linhas_detalhe.append(((cx - 3, cy - 5), (cx + 3, cy - 5)))
    linhas_detalhe.append(((cx, cy - 5), (cx, cy + 5)))

    if angle != 0:
        corpo_pontos = rotacionar_pontos_em_torno_de(corpo_pontos, cx, cy, angle)
        proa_pontos = rotacionar_pontos_em_torno_de(proa_pontos, cx, cy, angle)
        linhas_rot = []
        for (p0, p1) in linhas_detalhe:
            pts = rotacionar_pontos_em_torno_de([p0, p1], cx, cy, angle)
            linhas_rot.append((tuple(pts[0]), tuple(pts[1])))
        linhas_detalhe = linhas_rot

    # Preenche corpo com gradiente
    scanline_fill_gradiente(
        superficie,
        corpo_pontos,
        color.WOOD_DARK,
        color.WOOD_LIGHT,
        direcao="vertical",
    )
    desenhar_poligono(superficie, corpo_pontos, color.DETAIL_COLOR)

    # Preenche proa com gradiente
    scanline_fill_gradiente(
        superficie,
        proa_pontos,
        color.WOOD_DARK,
        color.WOOD_LIGHT,
        direcao="vertical",
    )
    
    # Contorno da proa
    desenhar_poligono(superficie, proa_pontos, color.DETAIL_COLOR)
    
    # Detalhes: linhas horizontais (tábuas)
    for i in range(3):
        y_tabua = y + altura_proa + 15 + i * 18
        draw_line(
            superficie,
            x + 5, y_tabua,
            x + largura_base - 5, y_tabua,
            color.DETAIL_COLOR,
            viewport=viewport
        )
    
    # Detalhe central (mastro ou estrutura)
    centro_x = x + largura_base // 2
    centro_y = y + altura_proa + comprimento // 2
    draw_line(
        superficie,
        centro_x - 3, centro_y - 5,
        centro_x + 3, centro_y - 5,
        color.DETAIL_COLOR,
        viewport=viewport
    )
    draw_line(
        superficie,
        centro_x, centro_y - 5,
        centro_x, centro_y + 5,
        color.DETAIL_COLOR,
        viewport=viewport
    )
    desenhar_poligono(superficie, proa_pontos, color.DETAIL_COLOR)

    # Detalhes: tábuas e mastro
    for (x0, y0), (x1, y1) in linhas_detalhe:
        bresenham(superficie, x0, y0, x1, y1, color.DETAIL_COLOR)