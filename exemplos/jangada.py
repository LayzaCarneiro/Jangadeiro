import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jangada - Visão de Cima")

clock = pygame.time.Clock()

SEA_COLOR = (0, 120, 170)
BOAT_COLOR = (139, 69, 19)
DETAIL = (100, 50, 20)
FISH_COLOR = (255, 200, 0)

# -----------------------------
# SET PIXEL
# -----------------------------
def set_pixel(x, y, color):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        screen.set_at((x, y), color)

# -----------------------------
# BRESENHAM - LINHA
# -----------------------------
def draw_line(x0, y0, x1, y1, color):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        set_pixel(x0, y0, color)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

# -----------------------------
# RETÂNGULO PREENCHIDO
# -----------------------------
def fill_rect(x, y, w, h, color):
    for i in range(x, x + w):
        for j in range(y, y + h):
            set_pixel(i, j, color)

# -----------------------------
# BARCO (TOP-DOWN)
# -----------------------------
def draw_boat(x, y):
    # Corpo
    fill_rect(x, y, 30, 50, BOAT_COLOR)

    # Bordas
    draw_line(x, y, x + 30, y, DETAIL)
    draw_line(x, y + 50, x + 30, y + 50, DETAIL)
    draw_line(x, y, x, y + 50, DETAIL)
    draw_line(x + 30, y, x + 30, y + 50, DETAIL)

    # Proa
    draw_line(x, y, x + 15, y - 15, DETAIL)
    draw_line(x + 30, y, x + 15, y - 15, DETAIL)

    # Centro
    fill_rect(x + 10, y + 20, 10, 15, (160, 82, 45))

# -----------------------------
# PEIXE
# -----------------------------
def draw_fish(x, y):
    set_pixel(x, y, FISH_COLOR)
    set_pixel(x - 1, y, FISH_COLOR)
    set_pixel(x + 1, y, FISH_COLOR)
    set_pixel(x, y - 1, FISH_COLOR)
    set_pixel(x, y + 1, FISH_COLOR)

# -----------------------------
# COLISÃO SIMPLES (AABB)
# -----------------------------
def check_collision(bx, by, bw, bh, fx, fy):
    return (bx < fx < bx + bw) and (by < fy < by + bh)

# -----------------------------
# POSIÇÕES INICIAIS
# -----------------------------
boat_x = 400
boat_y = 300
speed = 4

fish_x = random.randint(50, WIDTH - 50)
fish_y = random.randint(50, HEIGHT - 50)

# -----------------------------
# LOOP PRINCIPAL
# -----------------------------
running = True
while running:
    screen.fill(SEA_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # INPUT
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        boat_y -= speed
    if keys[pygame.K_s]:
        boat_y += speed
    if keys[pygame.K_a]:
        boat_x -= speed
    if keys[pygame.K_d]:
        boat_x += speed

    # LIMITES DA TELA
    boat_x = max(0, min(WIDTH - 30, boat_x))
    boat_y = max(0, min(HEIGHT - 50, boat_y))

    # COLISÃO BARCO × PEIXE
    if check_collision(boat_x, boat_y, 30, 50, fish_x, fish_y):
        fish_x = random.randint(50, WIDTH - 50)
        fish_y = random.randint(50, HEIGHT - 50)

    # DESENHO
    draw_fish(fish_x, fish_y)
    draw_boat(boat_x, boat_y)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
