# # teste do set pixel
# fb.setPixel(tela, 100, 100, (255, 0, 0))

# # teste do get pixel
# cor = fb.getPixel(tela, 100, 100)

# # usa a cor lida para desenhar outro pixel
# fb.setPixel(tela, 300, 100, cor)


## teste do clear
# for x in range(50, 350):
#     fb.setPixel(tela, x, 150, (255, 255, 255))
#     fb.clear(superficie=tela)


## dda
# rt.dda(tela, 50, 150, 350, 150, (255, 0, 0))
# rt.dda(tela, 200, 50, 200, 250, (0, 255, 0))
# rt.dda(tela, 50, 50, 250, 250, (0, 0, 255))
# rt.dda(tela, 50, 250, 250, 50, (255, 255, 0))
# rt.dda(tela, 100, 100, 100, 100, (255, 0, 255))
# rt.dda(tela, -50, 150, 450, 150, (0, 255, 255))


## bresenham
# rt.bresenham(tela, 50, 150, 350, 150, (255, 0, 0))     # horizontal
# rt.bresenham(tela, 200, 50, 200, 250, (0, 255, 0))     # vertical
# rt.bresenham(tela, 50, 50, 250, 250, (0, 0, 255))      # diagonal +
# rt.bresenham(tela, 50, 250, 250, 50, (255, 255, 0))    # diagonal -
# rt.bresenham(tela, 150, 50, 200, 250, (255, 0, 255))   # steep
# rt.bresenham(tela, 350, 200, 50, 100, (0, 255, 255))   # invertido
# rt.bresenham(tela, 100, 100, 100, 100, (255, 255, 255))# ponto

## flood fil
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


## scanline
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