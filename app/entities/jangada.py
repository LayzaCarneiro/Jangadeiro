from assets.colors import WOOD_LIGHT, WOOD_DARK, BLACK, SKIN, CLOTH, OAR_WOOD, OAR_DARK
# =========================
# Jangada (Raft)
# =========================

def draw_raft(screen, cx, cy, width, height,
              bresenham_reta, flood_fill):
    """
    Jangada vista de cima (polígono)
    """

    hw = width // 2
    hh = height // 2

    raft = [
        (cx - hw, cy - hh),
        (cx + hw, cy - hh),
        (cx + hw, cy + hh),
        (cx - hw, cy + hh)
    ]

    # Contorno
    for i in range(4):
        x0, y0 = raft[i]
        x1, y1 = raft[(i + 1) % 4]
        bresenham_reta(screen, x0, y0, x1, y1, WOOD_LIGHT)

    # Preenchimento
    flood_fill(screen, cx, cy, WOOD_DARK, WOOD_LIGHT)

    # Tábuas (linhas)
    step = height // 4
    for y in range(cy - hh + step, cy + hh, step):
        bresenham_reta(
            screen,
            cx - hw, y,
            cx + hw, y,
            WOOD_LIGHT
        )


# =========================
# Jangadeiro (Top-down)
# =========================

def draw_fisherman(screen, cx, cy,
                   draw_circle, bresenham_reta, flood_fill):
    """
    Corpo simples visto de cima
    """

    # Cabeça
    draw_circle(screen, cx, cy - 14, 8, BLACK)
    flood_fill(screen, cx, cy - 14, SKIN, BLACK)

    # Corpo (retângulo)
    body = [
        (cx - 8, cy - 4),
        (cx + 8, cy - 4),
        (cx + 8, cy + 14),
        (cx - 8, cy + 14)
    ]

    for i in range(4):
        x0, y0 = body[i]
        x1, y1 = body[(i + 1) % 4]
        bresenham_reta(screen, x0, y0, x1, y1, BLACK)

    flood_fill(screen, cx, cy + 4, CLOTH, BLACK)


# =========================
# Oar (Remo)
# =========================

def draw_oar(screen, cx, cy, length,
             bresenham_reta, draw_ellipse, flood_fill):
    """
    Remo visto de cima
    """

    # Cabo
    x0 = cx - length // 2
    x1 = cx + length // 2

    bresenham_reta(
        screen,
        x0, cy,
        x1, cy,
        OAR_WOOD
    )

    # Pá (elipse)
    paddle_x = x1 + 8

    draw_ellipse(
        screen,
        paddle_x, cy,
        10, 6,
        OAR_DARK
    )

    flood_fill(
        screen,
        paddle_x, cy,
        OAR_WOOD,
        OAR_DARK
    )


# =========================
# Full Raft (Top-down)
# =========================

def draw_full_raft(screen, cx, cy,
                   bresenham_reta,
                   draw_circle,
                   draw_ellipse,
                   flood_fill):
    """
    Jangada + jangadeiro + remo
    """

    # Jangada
    draw_raft(
        screen,
        cx, cy,
        width=120,
        height=60,
        bresenham_reta=bresenham_reta,
        flood_fill=flood_fill
    )

    # Jangadeiro
    draw_fisherman(
        screen,
        cx, cy,
        draw_circle,
        bresenham_reta,
        flood_fill
    )

    # Remo (lado direito)
    draw_oar(
        screen,
        cx + 80,
        cy,
        length=100,
        bresenham_reta=bresenham_reta,
        draw_ellipse=draw_ellipse,
        flood_fill=flood_fill
    )
