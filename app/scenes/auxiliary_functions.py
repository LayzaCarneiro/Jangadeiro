# ═══════════════════════════════════════════════════════════════
# UTILITÁRIOS DE UI E TEXTO
# ═══════════════════════════════════════════════════════════════
# Conjunto de funções auxiliares para UI e texto no jogo.
#
# Demonstra os seguintes requisitos:
# - (a) set_pixel: fonte e desenhos pixel a pixel
# - (b) Primitivas: polígonos e linhas em botões
# - (c) Preenchimento: scanline_fill para botões
# - (i) Interação: suporte a botões (detecção de clique)
#
# Conteúdo:
# - Fonte 5x7 baseada em pixels
# - Funções de texto e botões
# - Funções auxiliares (clique, pixel escalado, randint)
# ═══════════════════════════════════════════════════════════════

from engine.framebuffer import set_pixel
from engine.fill.scanline import scanline_fill
from engine.raster.line import desenhar_poligono

# ─── Fonte 5x7 Pixel ───
# Cada letra: 7 linhas de 5 pixels ('X' = pixel ligado, ' ' = desligado)
# Caracteres suportados: letras A-Z, números 0-9, sinais básicos (:-.)
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
    ",": ["     ", "     ", "     ", "     ", "     ", "  X  ", " X   "],
    "!": ["  X  ", "  X  ", "  X  ", "  X  ", "     ", "  X  ", "     "],
}


def _draw_char(surf, c, x, y, cor, scale=2):
    """
    Desenha um único caractere usando a fonte 5x7.

    Args:
        surf: pygame.Surface onde desenhar.
        c (str): Caractere a desenhar.
        x, y (int): Posição superior esquerda.
        cor (tuple): Cor RGB do pixel.
        scale (int): Fator de escala.
    """
    c = c.upper()
    rows = _FONT.get(c, _FONT[" "])
    for row, s in enumerate(rows):
        for col, ch in enumerate(s):
            if ch == "X":
                for dy in range(scale):
                    for dx in range(scale):
                        set_pixel(surf, x + col * scale + dx, y + row * scale + dy, cor)



def draw_simple_text(superficie, texto, x, y, cor, scale=1):
    """
    Desenha texto simples usando apenas set_pixel.
    scale: 1 = normal; 2 = cada pixel vira bloco 2×2.
    """
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
        '/': ['  X', '  X', ' X ', 'X  ', 'X  '],  
    }
    
    dx = 0
    for c in texto:
        if c in chars:
            pattern = chars[c]
            for row, line in enumerate(pattern):
                for col, pixel in enumerate(line):
                    if pixel == 'X':
                        _set_pixel_scaled(superficie, x, y, dx + col, row, cor, scale)
        dx += 4 * scale  # Espaço entre caracteres


def draw_text(surf, texto, x, y, cor, scale=2):
    """
    Desenha texto com a fonte 5x7 via set_pixel.
    
    REQUISITO: (a) Acesso direto por pixel
    """
    dx = 0
    for c in texto:
        if c.upper() in _FONT:
            _draw_char(surf, c, x + dx, y, cor, scale)
        dx += 6 * scale  # largura aproximada por letra + espaço


def draw_button(surf, x, y, larg, alt, texto, cor_fundo, cor_borda, cor_texto):
    """
    Botão: polígono preenchido com scanline + borda com bresenham + texto.

    Args:
    surf: pygame.Surface onde desenhar.
    x, y (int): Posição do canto superior esquerdo.
    larg, alt (int): Largura e altura do botão.
    texto (str): Texto do botão.
    cor_fundo (tuple): Cor de preenchimento do botão.
    cor_borda (tuple): Cor da borda do botão.
    cor_texto (tuple): Cor do texto.
    """
    pts = [(x, y), (x + larg, y), (x + larg, y + alt), (x, y + alt)]
    scanline_fill(surf, pts, cor_fundo)
    desenhar_poligono(surf, pts, cor_borda)
    # texto centralizado (aproximado)
    tw = len(texto) * 6 * 2  # 6*scale por letra, scale=2
    tx = x + (larg - tw) // 2
    ty = y + (alt - 7 * 2) // 2  # 7*scale de altura
    draw_text(surf, texto, max(x, tx), ty, cor_texto, scale=2)


def ponto_em_retangulo(px, py, rx, ry, rw, rh):
    """
    Verifica se um ponto está dentro de um retângulo.

    Args:
        px, py (int): Coordenadas do ponto.
        rx, ry (int): Canto superior esquerdo do retângulo.
        rw, rh (int): Largura e altura do retângulo.

    Returns:
        bool: True se o ponto estiver dentro, False caso contrário.
    """
    return rx <= px <= rx + rw and ry <= py <= ry + rh


def _set_pixel_scaled(superficie, base_x, base_y, local_x, local_y, cor, scale):
    """
    Desenha um "pixel lógico" como bloco scale×scale usando só set_pixel.
    base_x, base_y = canto superior esquerdo do elemento; local_x, local_y = offset.
    """
    if scale <= 1:
        set_pixel(superficie, base_x + local_x, base_y + local_y, cor)
        return
    for sy in range(scale):
        for sx in range(scale):
            set_pixel(
                superficie,
                base_x + local_x * scale + sx,
                base_y + local_y * scale + sy,
                cor,
            )


# Semente inicial interna
_seed = 123456789  # qualquer número inicial

def randint(a, b):
    """Gera inteiro pseudoaleatório entre a e b sem usar time ou módulos."""
    global _seed
    # LCG simples: Linear Congruential Generator
    a_lcg = 1664525
    c_lcg = 1013904223
    m_lcg = 2**32

    # Atualiza a semente
    _seed = (a_lcg * _seed + c_lcg) % m_lcg

    # Converte para o intervalo desejado
    return a + int((_seed / m_lcg) * (b - a + 1))