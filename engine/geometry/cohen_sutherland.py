from engine.raster.line import bresenham

INSIDE = 0
LEFT   = 1
RIGHT  = 2
BOTTOM = 4
TOP    = 8

def codigo_regiao(x, y, xmin, ymin, xmax, ymax):
    code = INSIDE
    if x < xmin: code |= LEFT
    elif x > xmax: code |= RIGHT
    if y < ymin: code |= TOP      # y cresce para baixo
    elif y > ymax: code |= BOTTOM
    return code

def cohen_sutherland(x0, y0, x1, y1, xmin, ymin, xmax, ymax):
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
    xmin, ymin, xmax, ymax = viewport
    visivel, cx0, cy0, cx1, cy1 = cohen_sutherland(x0, y0, x1, y1, xmin, ymin, xmax, ymax)
    if not visivel:
        return
    bresenham(tela, cx0, cy0, cx1, cy1, cor)