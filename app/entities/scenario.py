import math

# =========================
# Colors (RGB)
# =========================

SEA_GREEN = (40, 120, 100)
ROCK_GRAY = (90, 90, 90)
ROCK_DARK = (60, 60, 60)

FISH_ORANGE = (255, 150, 60)
FISH_BLUE = (80, 160, 220)

BOAT_WOOD = (160, 120, 70)
BOAT_DARK = (120, 90, 50)
WHITE = (255, 255, 255)


# =========================
# World Data
# =========================

WORLD_WIDTH = 2000
WORLD_HEIGHT = 2000

ROCKS = [
    (400, 300, 25),
    (800, 600, 30),
    (1200, 500, 20),
    (1500, 900, 35),
    (600, 1200, 28),
]

FISHES = [
    (500, 400, 10, FISH_ORANGE),
    (700, 450, 8, FISH_BLUE),
    (1000, 800, 12, FISH_ORANGE),
    (1300, 700, 9, FISH_BLUE),
    (1600, 1000, 11, FISH_ORANGE),
]


# =========================
# Sea
# =========================

def draw_sea(screen, setPixel):
    width = screen.get_width()
    height = screen.get_height()

    for y in range(height):
        for x in range(width):
            setPixel(screen, x, y, SEA_GREEN)


# =========================
# Rocks
# =========================

def draw_rock(screen, cx, cy, radius,
              offset_x, offset_y,
              draw_circle, flood_fill):

    sx = cx - offset_x
    sy = cy - offset_y

    draw_circle(screen, int(sx), int(sy), radius, ROCK_GRAY)
    flood_fill(screen, int(sx), int(sy), ROCK_DARK, ROCK_GRAY)


def draw_rocks(screen, offset_x, offset_y,
               draw_circle, flood_fill):

    for r in ROCKS:
        draw_rock(
            screen,
            r[0], r[1], r[2],
            offset_x, offset_y,
            draw_circle, flood_fill
        )


# =========================
# Fish (static)
# =========================

def draw_fish(screen, cx, cy, size, color,
              offset_x, offset_y,
              bresenham_reta, draw_circle):

    sx = cx - offset_x
    sy = cy - offset_y

    draw_circle(screen, int(sx), int(sy), size, color)

    tail = [
        (sx - size, sy),
        (sx - size - size // 2, sy - size // 2),
        (sx - size - size // 2, sy + size // 2)
    ]

    for i in range(3):
        x0, y0 = tail[i]
        x1, y1 = tail[(i + 1) % 3]
        bresenham_reta(
            screen,
            int(x0), int(y0),
            int(x1), int(y1),
            color
        )

    draw_circle(
        screen,
        int(sx + size // 3),
        int(sy - size // 4),
        2,
        WHITE
    )


def draw_fishes(screen, offset_x, offset_y,
                bresenham_reta, draw_circle):

    for f in FISHES:
        draw_fish(
            screen,
            f[0], f[1], f[2], f[3],
            offset_x, offset_y,
            bresenham_reta, draw_circle
        )


# =========================
# Boat (TOP-DOWN)
# =========================

def draw_boat(screen, cx, cy, size,
              bresenham_reta, flood_fill):
    """
    Barco visto de cima (polígono simples)
    """

    half = size // 2

    hull = [
        (cx - half, cy + half),
        (cx + half, cy + half),
        (cx + half // 2, cy - half),
        (cx - half // 2, cy - half)
    ]

    # Casco
    for i in range(len(hull)):
        x0, y0 = hull[i]
        x1, y1 = hull[(i + 1) % len(hull)]
        bresenham_reta(screen, x0, y0, x1, y1, BOAT_WOOD)

    flood_fill(screen, cx, cy, BOAT_DARK, BOAT_WOOD)

    # Linha central (detalhe)
    bresenham_reta(
        screen,
        cx, cy + half,
        cx, cy - half,
        BOAT_WOOD
    )


# =========================
# Scenario Builder
# =========================

def draw_scenario(screen,
                  boat_x,
                  boat_y,
                  setPixel,
                  draw_circle,
                  flood_fill,
                  bresenham_reta):
    """
    Desenha cenário + barco
    """

    width = screen.get_width()
    height = screen.get_height()

    # Offset do mundo (barco como referência)
    offset_x = boat_x - width // 2
    offset_y = boat_y - height + 120  # barco embaixo

    # 1. Mar
    draw_sea(screen, setPixel)

    # 2. Mundo
    draw_rocks(screen, offset_x, offset_y, draw_circle, flood_fill)
    draw_fishes(screen, offset_x, offset_y, bresenham_reta, draw_circle)

    # 3. Barco (sempre visível)
    draw_boat(
        screen,
        width // 2,
        height - 120,
        60,
        bresenham_reta,
        flood_fill
    )
