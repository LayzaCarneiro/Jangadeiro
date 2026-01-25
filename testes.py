# # teste do set pixel
# fb.set_pixel(tela, 100, 100, (255, 0, 0))

# # teste do get pixel
# cor = fb.getPixel(tela, 100, 100)

# # usa a cor lida para desenhar outro pixel
# fb.set_pixel(tela, 300, 100, cor)


## teste do clear
# for x in range(50, 350):
#     fb.set_pixel(tela, x, 150, (255, 255, 255))
#     fb.clear(superficie=tela)


## testar dda
# rt.dda(tela, 50, 150, 350, 150, (255, 0, 0))
# rt.dda(tela, 200, 50, 200, 250, (0, 255, 0))
# rt.dda(tela, 50, 50, 250, 250, (0, 0, 255))
# rt.dda(tela, 50, 250, 250, 50, (255, 255, 0))
# rt.dda(tela, 100, 100, 100, 100, (255, 0, 255))
# rt.dda(tela, -50, 150, 450, 150, (0, 255, 255))


## testar bresenham
# rt.bresenham(tela, 50, 150, 350, 150, (255, 0, 0))     # horizontal
# rt.bresenham(tela, 200, 50, 200, 250, (0, 255, 0))     # vertical
# rt.bresenham(tela, 50, 50, 250, 250, (0, 0, 255))      # diagonal +
# rt.bresenham(tela, 50, 250, 250, 50, (255, 255, 0))    # diagonal -
# rt.bresenham(tela, 150, 50, 200, 250, (255, 0, 255))   # steep
# rt.bresenham(tela, 350, 200, 50, 100, (0, 255, 255))   # invertido
# rt.bresenham(tela, 100, 100, 100, 100, (255, 255, 255))# ponto

## testar flood fil
# # Borda branca
# rt.bresenham(tela, 100, 80, 300, 80, (255, 255, 255))
# rt.bresenham(tela, 300, 80, 300, 220, (255, 255, 255))
# rt.bresenham(tela, 300, 220, 100, 220, (255, 255, 255))
# rt.bresenham(tela, 100, 220, 100, 80, (255, 255, 255))

# engine.fill.flood_fill.flood_fill_iterativo(
#     tela,
#     150, 150,           # ponto interno
#     (0, 0, 255),        # cor de preenchimento
#     (255, 255, 255)     # cor da borda
# )


## testar scanline
# # Borda branca
# triangulo = [
#     (200, 60),
#     (300, 200),
#     (100, 200)
# ]

# # Desenha borda
# for i in range(len(triangulo)):
#     x0, y0 = triangulo[i]
#     x1, y1 = triangulo[(i + 1) % len(triangulo)]
#     rt.bresenham(tela, x0, y0, x1, y1, (255, 255, 255))

# # Preenche
# engine.fill.scanline.scanline_fill(tela, triangulo, (0, 0, 255))


## testar desenhar poligonos
# triangulo = [(250, 80), (350, 250), (150, 250)]
# quadrado = [(50, 50), (150, 50), (150, 150), (50, 150)]
# pentagono = [(350, 60), (420, 120), (390, 200), (310, 200), (280, 120)]
# desenhar_poligono(tela, triangulo, (255, 0, 0))
# desenhar_poligono(tela, quadrado, (0, 255, 0))
# desenhar_poligono(tela, pentagono, (0, 0, 255))


## testar circulo
    # draw_circle(tela, 300, 200, 100, (0, 0, 0))
    # flood_fill_iterativo(tela, 300, 200, (255, 0, 0), (0, 0, 0))


## testar elipse
    # draw_elipse(tela, 300, 200, 150, 80, (0, 0, 0))
    # flood_fill_iterativo(tela, 300, 200, (0, 150, 255), (0, 0, 0))


## testes transformaçoes
#     poligono = [
#     (200, 150),
#     (300, 170),
#     (320, 240),
#     (250, 290),
#     (190, 230)
# ]

#     cx = sum(p[0] for p in poligono) / len(poligono)
#     cy = sum(p[1] for p in poligono) / len(poligono)

#     desenhar_poligono(tela, poligono, (150, 150, 150))

#     M = identidade()
#     p = aplica_transformacao(M, poligono)

#     desenhar_poligono(tela, p, (0, 0, 0))


#     M = identidade()
#     M = multiplica_matrizes(translacao(100, 50), M)

#     p = aplica_transformacao(M, poligono)
#     desenhar_poligono(tela, p, (255, 0, 0))

#     M = identidade()
#     M = multiplica_matrizes(escala(2, 2), M)

#     p = aplica_transformacao(M, poligono)
#     desenhar_poligono(tela, p, (0, 0, 255))

#     M = identidade()
#     M = multiplica_matrizes(translacao(cx, cy), M)
#     M = multiplica_matrizes(escala(1.5, 1.5), M)
#     M = multiplica_matrizes(translacao(-cx, -cy), M)

#     p = aplica_transformacao(M, poligono)
#     desenhar_poligono(tela, p, (0, 150, 255))

#     M = identidade()
#     M = multiplica_matrizes(rotacao(math.radians(45)), M)

#     p = aplica_transformacao(M, poligono)
#     desenhar_poligono(tela, p, (255, 0, 255))

#     M = identidade()
#     M = multiplica_matrizes(translacao(cx, cy), M)
#     M = multiplica_matrizes(rotacao(math.radians(45)), M)
#     M = multiplica_matrizes(translacao(-cx, -cy), M)

#     p = aplica_transformacao(M, poligono)
#     desenhar_poligono(tela, p, (255, 100, 0))