import pygame
import sys
import math
from engine.framebuffer import set_pixel
from engine.fill.flood_fill import flood_fill_iterativo
from engine.raster.line import bresenham
from engine.raster.line import desenhar_poligono
from engine.raster.circle import draw_circle
from engine.raster.elipse import draw_elipse
from engine.geometry.transform import identidade, aplica_transformacao, multiplica_matrizes, translacao, escala, rotacao

pygame.init()
largura, altura = 1000, 1000
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Main")

rodando = True

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    tela.fill((255, 255, 255))

    pygame.display.flip()

pygame.quit()
sys.exit()