from engine.raster.line import bresenham

# ============================
# Códigos de região para Cohen-Sutherland
# ============================
INSIDE = 0   # Dentro da área de recorte
LEFT   = 1   # Fora à esquerda
RIGHT  = 2   # Fora à direita
BOTTOM = 4   # Fora abaixo
TOP    = 8   # Fora acima

def codigo_regiao(x, y, xmin, ymin, xmax, ymax):
    """
    Calcula o código de região de um ponto para o algoritmo
    de recorte de linha Cohen-Sutherland.

    Args:
        x, y: coordenadas do ponto
        xmin, ymin, xmax, ymax: limites do retângulo de recorte

    Returns:
        int: código de região (bitmask)
    """
    code = INSIDE
    if x < xmin: code |= LEFT
    elif x > xmax: code |= RIGHT
    if y < ymin: code |= TOP      # y cresce para baixo
    elif y > ymax: code |= BOTTOM
    return code

def cohen_sutherland(x0, y0, x1, y1, xmin, ymin, xmax, ymax):
    """
    Aplica o algoritmo de recorte Cohen-Sutherland a uma linha.
    
    Args:
        x0, y0, x1, y1: coordenadas da linha
        xmin, ymin, xmax, ymax: retângulo de recorte

    Returns:
        tuple:
            - bool: True se a linha (ou parte dela) é visível
            - x0, y0, x1, y1: coordenadas da linha recortada (ou None se fora)
    """
    c0 = codigo_regiao(x0, y0, xmin, ymin, xmax, ymax)
    c1 = codigo_regiao(x1, y1, xmin, ymin, xmax, ymax)

    while True:
        if not (c0 | c1):
            return True, x0, y0, x1, y1  # totalmente visível

        if c0 & c1:
            return False, None, None, None, None  # totalmente fora

        c_out = c0 if c0 else c1

        if c_out & TOP:
            x = x0 + (x1 - x0) * (ymin - y0) / (y1 - y0)
            y = ymin
        elif c_out & BOTTOM:
            x = x0 + (x1 - x0) * (ymax - y0) / (y1 - y0)
            y = ymax
        elif c_out & RIGHT:
            y = y0 + (y1 - y0) * (xmax - x0) / (x1 - x0)
            x = xmax
        elif c_out & LEFT:
            y = y0 + (y1 - y0) * (xmin - x0) / (x1 - x0)
            x = xmin

        if c_out == c0:
            x0, y0 = x, y
            c0 = codigo_regiao(x0, y0, xmin, ymin, xmax, ymax)
        else:
            x1, y1 = x, y
            c1 = codigo_regiao(x1, y1, xmin, ymin, xmax, ymax)


def draw_line(superficie, x0, y0, x1, y1, color, viewport=None):
    """
    Desenha uma linha usando Bresenham.
    Se 'viewport' for fornecido, aplica clipping Cohen-Sutherland.
    Se não, desenha direto.

    Args:
        superficie: pygame.Surface onde desenhar
        x0, y0, x1, y1: coordenadas da linha
        color: cor da linha
        viewport: tupla (xmin, ymin, largura, altura). Se fornecido,
                  aplica recorte Cohen-Sutherland.
    """
    if viewport:
        xmin, ymin, w, h = viewport
        xmax = xmin + w
        ymax = ymin + h

        visible, cx0, cy0, cx1, cy1 = cohen_sutherland(
            x0, y0, x1, y1,
            xmin, ymin,
            xmax, ymax
        )

        if not visible:
            return  # totalmente fora da tela

        x0, y0, x1, y1 = cx0, cy0, cx1, cy1

    bresenham(x0, y0, x1, y1, color)


def draw_line_clipped(tela, x0, y0, x1, y1, cor, viewport):
    """
    Wrapper para desenhar uma linha com clipping Cohen-Sutherland.
    
    Args:
        tela: pygame.Surface onde desenhar
        x0, y0, x1, y1: coordenadas da linha
        cor: cor da linha
        viewport: tupla (xmin, ymin, xmax, ymax) definindo o retângulo de recorte
    """
    xmin, ymin, xmax, ymax = viewport
    visivel, cx0, cy0, cx1, cy1 = cohen_sutherland(x0, y0, x1, y1, xmin, ymin, xmax, ymax)
    if not visivel:
        return
    bresenham(tela, cx0, cy0, cx1, cy1, cor)