import pygame
import sys
import engine.raster.line as rt
import engine.fill.scanline

pygame.init()
largura, altura = 400, 300
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Main")

rodando = True

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    tela.fill((0, 0, 0))

    # testes

    # Borda branca
    triangulo = [
        (200, 60),
        (300, 200),
        (100, 200)
    ]

    # Desenha borda
    for i in range(len(triangulo)):
        x0, y0 = triangulo[i]
        x1, y1 = triangulo[(i + 1) % len(triangulo)]
        rt.bresenham(tela, x0, y0, x1, y1, (255, 255, 255))

    # Preenche
    engine.fill.scanline.scanline_fill(tela, triangulo, (0, 0, 255))



    pygame.display.flip()

pygame.quit()
sys.exit()