import pygame
import sys
import math

pygame.init()
largura, altura = 400, 300
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Pink Floyd Capa")

def setPixel(superficie, x, y, cor):
    if 0 <= x < superficie.get_width() and 0 <= y < superficie.get_height():
        superficie.set_at((x, y), cor)

def desenha_linha(superficie, x1, y1, x2, y2, cor):
    # bresenham
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    erro = dx - dy

    while True:
        setPixel(superficie, x1, y1, cor)

        if x1 == x2 and y1 == y2:
            break

        e2 = 2 * erro
        if e2 > -dy:
            erro -= dy
            x1 += sx
        if e2 < dx:
            erro += dx
            y1 += sy


def desenha_triangulo(superficie, p1, p2, p3, cor):
    desenha_linha(superficie, p1[0], p1[1], p2[0], p2[1], cor)
    desenha_linha(superficie, p2[0], p2[1], p3[0], p3[1], cor)
    desenha_linha(superficie, p3[0], p3[1], p1[0], p1[1], cor)

def desenhar_seno(superficie, cor):
    amplitude = altura // 4
    centro_y = altura // 2
    frequencia = 2*math.pi / largura

    for x in range(largura):
       # y = centro_y - int(math.sin(x*frequencia)*amplitude)

        fase = pygame.time.get_ticks() * 0.005
        y = centro_y - int(math.sin(x * frequencia + fase) * amplitude)

        setPixel(superficie, x, y, cor)

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    tela.fill((0, 0, 0))

    setPixel(tela, 200, 150, (255, 0, 0))
    setPixel(tela, 210, 150, (0, 255, 0))
    setPixel(tela, 220, 150, (0, 0, 255))
    setPixel(tela, 230, 150, (255, 255, 0))

    p1 = (200, 50)
    p2 = (100, 200)
    p3 = (300, 200)

    desenha_triangulo(tela, p1, p2, p3, (255, 255, 255))
    desenhar_seno(tela, (0, 255, 255))

    pygame.display.flip()

def dda(superficie, x0, x1, y0, y1, cor):
    dx = x1 - x0
    dy = y1- y0

    passos = max(abs(dx), abs(dy))

pygame.quit()
sys.exit()
