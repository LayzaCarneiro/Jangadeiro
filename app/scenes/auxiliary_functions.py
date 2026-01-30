from engine.framebuffer import set_pixel
from engine.fill.scanline import scanline_fill
from engine.raster.line import desenhar_poligono

# Fonte 5x7 (apenas set_pixel) – caracteres usados: A C D E G I J L N R S T V (espaço)
# Cada letra: 7 linhas de 5 caracteres; 'X' = pixel ligado
_FONT = {
    " ": ["     ", "     ", "     ", "     ", "     ", "     ", "     "],
    "A": ["  X  ", " X X ", "X   X", "XXXXX", "X   X", "X   X", "X   X"],
    "B": ["XXXX ", "X   X", "X   X", "XXXX ", "X   X", "X   X", "XXXX "],
    "C": [" XXX ", "X   X", "X    ", "X    ", "X    ", "X   X", " XXX "],
    "D": ["XXX  ", "X  X ", "X   X", "X   X", "X   X", "X  X ", "XXX  "],
    "E": ["XXXXX", "X    ", "X    ", "XXX  ", "X    ", "X    ", "XXXXX"],
    "F": ["XXXXX", "X    ", "X    ", "XXXX ", "X    ", "X    ", "X    "],
    "G": [" XXX ", "X   X", "X    ", "X XXX", "X   X", "X   X", " XXX "],
    "H": ["X   X", "X   X", "X   X", "XXXXX", "X   X", "X   X", "X   X"],
    "I": [" XXX ", "  X  ", "  X  ", "  X  ", "  X  ", "  X  ", " XXX "],
    "J": ["    X", "    X", "    X", "    X", "    X", "X   X", " XXX "],
    "K": ["X   X", "X  X ", "X X  ", "XX   ", "X X  ", "X  X ", "X   X"],
    "L": ["X    ", "X    ", "X    ", "X    ", "X    ", "X    ", "XXXXX"],
    "M": ["X   X", "XX XX", "X X X", "X   X", "X   X", "X   X", "X   X"],
    "N": ["X   X", "XX  X", "X X X", "X  XX", "X   X", "X   X", "X   X"],
    "O": [" XXX ", "X   X", "X   X", "X   X", "X   X", "X   X", " XXX "],
    "P": ["XXXX ", "X   X", "X   X", "XXXX ", "X    ", "X    ", "X    "],
    "Q": [" XXX ", "X   X", "X   X", "X   X", "X X X", "X  X ", " XX X"],
    "R": ["XXXX ", "X   X", "X   X", "XXXX ", "X X  ", "X  X ", "X   X"],
    "S": [" XXX ", "X   X", "X    ", " XXX ", "    X", "X   X", " XXX "],
    "T": ["XXXXX", "  X  ", "  X  ", "  X  ", "  X  ", "  X  ", "  X  "],
    "U": ["X   X", "X   X", "X   X", "X   X", "X   X", "X   X", " XXX "],
    "V": ["X   X", "X   X", "X   X", "X   X", " X X ", " X X ", "  X  "],
    "W": ["X   X", "X   X", "X   X", "X X X", "X X X", "XX XX", "X   X"],
    "X": ["X   X", "X   X", " X X ", "  X  ", " X X ", "X   X", "X   X"],
    "Y": ["X   X", "X   X", " X X ", "  X  ", "  X  ", "  X  ", "  X  "],
    "Z": ["XXXXX", "    X", "   X ", "  X  ", " X   ", "X    ", "XXXXX"],

    # números básicos
    "0": [" XXX ", "X   X", "X  XX", "X X X", "XX  X", "X   X", " XXX "],
    "1": ["  X  ", " XX  ", "  X  ", "  X  ", "  X  ", "  X  ", " XXX "],
    "2": [" XXX ", "X   X", "    X", "   X ", "  X  ", " X   ", "XXXXX"],
    "3": [" XXX ", "X   X", "    X", "  XX ", "    X", "X   X", " XXX "],
    "4": ["   X ", "  XX ", " X X ", "X  X ", "XXXXX", "   X ", "   X "],
    "5": ["XXXXX", "X    ", "XXXX ", "    X", "    X", "X   X", " XXX "],
    "6": [" XXX ", "X   X", "X    ", "XXXX ", "X   X", "X   X", " XXX "],
    "7": ["XXXXX", "    X", "   X ", "  X  ", " X   ", " X   ", " X   "],
    "8": [" XXX ", "X   X", "X   X", " XXX ", "X   X", "X   X", " XXX "],
    "9": [" XXX ", "X   X", "X   X", " XXXX", "    X", "X   X", " XXX "],

    # sinais básicos
    ":": ["     ", "  X  ", "     ", "     ", "  X  ", "     ", "     "],
    "-": ["     ", "     ", "     ", "XXXXX", "     ", "     ", "     "],
    ".": ["     ", "     ", "     ", "     ", "     ", "  X  ", "     "],
}


def _draw_char(surf, c, x, y, cor, scale=2):
    c = c.upper()
    rows = _FONT.get(c, _FONT[" "])
    for row, s in enumerate(rows):
        for col, ch in enumerate(s):
            if ch == "X":
                for dy in range(scale):
                    for dx in range(scale):
                        set_pixel(surf, x + col * scale + dx, y + row * scale + dy, cor)


def draw_text(surf, texto, x, y, cor, scale=2):
    """Desenha texto com a fonte 5x7 via set_pixel."""
    dx = 0
    for c in texto:
        if c.upper() in _FONT:
            _draw_char(surf, c, x + dx, y, cor, scale)
        dx += 6 * scale  # largura aproximada por letra + espaço


def draw_button(surf, x, y, larg, alt, texto, cor_fundo, cor_borda, cor_texto):
    """Botão: polígono preenchido com scanline + borda com bresenham + texto."""
    pts = [(x, y), (x + larg, y), (x + larg, y + alt), (x, y + alt)]
    scanline_fill(surf, pts, cor_fundo)
    desenhar_poligono(surf, pts, cor_borda)
    # texto centralizado (aproximado)
    tw = len(texto) * 6 * 2  # 6*scale por letra, scale=2
    tx = x + (larg - tw) // 2
    ty = y + (alt - 7 * 2) // 2  # 7*scale de altura
    draw_text(surf, texto, max(x, tx), ty, cor_texto, scale=2)


def ponto_em_retangulo(px, py, rx, ry, rw, rh):
    return rx <= px <= rx + rw and ry <= py <= ry + rh
