from engine.framebuffer import set_pixel
import assets.colors as color
from random import randint, seed

seed(42)  # Para que estrelas fiquem consistentes

def draw_minimap(
    superficie,
    raft_x, raft_y,
    fish_x, fish_y,
    obstaculos,
    camera_x, camera_y,
    WORLD_WIDTH, WORLD_HEIGHT,
    WIDTH, HEIGHT
):
    MAP_W, MAP_H = 180, 180
    MAP_X, MAP_Y = WIDTH - MAP_W - 15, 15

    # ===== FUNDO ESCURO + ESTRELAS =====
    for y in range(MAP_H):
        for x in range(MAP_W):
            set_pixel(superficie, MAP_X + x, MAP_Y + y, (15, 25, 40))

    # Pequenas estrelas aleatórias
    for _ in range(80):
        sx = randint(0, MAP_W-1)
        sy = randint(0, MAP_H-1)
        brilho = randint(180, 255)
        set_pixel(superficie, MAP_X + sx, MAP_Y + sy, (brilho, brilho, 255))

    # Escala mundo → minimapa
    scale_x = MAP_W / WORLD_WIDTH
    scale_y = MAP_H / WORLD_HEIGHT

    # ===== VIEWPORT =====
    vx = int(camera_x * scale_x)
    vy = int(camera_y * scale_y)
    vw = int(WIDTH * scale_x)
    vh = int(HEIGHT * scale_y)

    # Contorno da câmera
    for i in range(vw):
        set_pixel(superficie, MAP_X + vx + i, MAP_Y + vy, (255, 255, 255))
        set_pixel(superficie, MAP_X + vx + i, MAP_Y + vy + vh, (255, 255, 255))
    for i in range(vh):
        set_pixel(superficie, MAP_X + vx, MAP_Y + vy + i, (255, 255, 255))
        set_pixel(superficie, MAP_X + vx + vw, MAP_Y + vy + i, (255, 255, 255))

    # ===== PEIXE =====
    px = int(fish_x * scale_x)
    py = int(fish_y * scale_y)
    # Peixe com "ponto + brilho"
    set_pixel(superficie, MAP_X + px, MAP_Y + py, color.FISH_BLUE)
    for dx in [-1, 1]:
        for dy in [-1, 1]:
            set_pixel(superficie, MAP_X + px + dx, MAP_Y + py + dy, (180, 220, 255))

    # ===== OBSTÁCULOS =====
    for obs in obstaculos:
        ox = int(obs[0] * scale_x)
        oy = int(obs[1] * scale_y)
        # Obstáculo mais suave
        set_pixel(superficie, MAP_X + ox, MAP_Y + oy, (120, 120, 120))
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                set_pixel(superficie, MAP_X + ox + dx, MAP_Y + oy + dy, (80, 80, 80))

    # ===== JANGADA =====
    rx = int(raft_x * scale_x)
    ry = int(raft_y * scale_y)
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            set_pixel(superficie, MAP_X + rx + dx, MAP_Y + ry + dy, (255, 255, 255))
    # Pequeno triângulo para indicar direção (opcional)
    set_pixel(superficie, MAP_X + rx, MAP_Y + ry - 3, (255, 255, 255))