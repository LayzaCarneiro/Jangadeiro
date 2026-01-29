from engine.framebuffer import set_pixel
from engine.math.auxiliary import interpolar_cor

# =========================
# Scanline Fill
# =========================
def scanline_fill(superficie, pontos, cor_preenchimento):
    # Encontra Y mínimo e máximo
    ys = [p[1] for p in pontos]
    y_min = min(ys)
    y_max = max(ys)

    n = len(pontos)

    for y in range(y_min, y_max):
        intersecoes_x = []

        for i in range(n):
            x0, y0 = pontos[i]
            x1, y1 = pontos[(i + 1) % n]

            # Ignora arestas horizontais
            if y0 == y1:
                continue

            # Garante y0 < y1
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0

            # Regra Ymin ≤ y < Ymax
            if y < y0 or y >= y1:
                continue

            # Calcula interseção
            x = x0 + (y - y0) * (x1 - x0) / (y1 - y0)
            intersecoes_x.append(x)

        # Ordena interseções
        intersecoes_x.sort()

        # Preenche entre pares
        for i in range(0, len(intersecoes_x), 2):
            if i + 1 < len(intersecoes_x):
                x_inicio = int(round(intersecoes_x[i]))
                x_fim = int(round(intersecoes_x[i + 1]))

                for x in range(x_inicio, x_fim + 1):
                    set_pixel(superficie, x, y, cor_preenchimento)


def scanline_fill_gradiente(superficie, pontos, cor_inicio, cor_fim, direcao='vertical'):
    """
    Preenche polígono com gradiente linear.
    direcao: 'vertical' (de cima para baixo) ou 'horizontal' (esquerda para direita)
    """
    ys = [p[1] for p in pontos]
    xs = [p[0] for p in pontos]
    y_min = min(ys)
    y_max = max(ys)
    x_min = min(xs)
    x_max = max(xs)
    
    n = len(pontos)
    
    for y in range(y_min, y_max):
        intersecoes_x = []
        
        for i in range(n):
            x0, y0 = pontos[i]
            x1, y1 = pontos[(i + 1) % n]
            
            if y0 == y1:
                continue
            
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            
            if y < y0 or y >= y1:
                continue
            
            x = x0 + (y - y0) * (x1 - x0) / (y1 - y0)
            intersecoes_x.append(x)
        
        intersecoes_x.sort()
        
        for i in range(0, len(intersecoes_x), 2):
            if i + 1 < len(intersecoes_x):
                x_inicio = int(round(intersecoes_x[i]))
                x_fim = int(round(intersecoes_x[i + 1]))
                
                for x in range(x_inicio, x_fim + 1):
                    if direcao == 'vertical':
                        # Gradiente vertical: t baseado em y
                        if y_max != y_min:
                            t = (y - y_min) / (y_max - y_min)
                        else:
                            t = 0.5
                    else:
                        # Gradiente horizontal: t baseado em x
                        if x_max != x_min:
                            t = (x - x_min) / (x_max - x_min)
                        else:
                            t = 0.5
                    
                    cor = interpolar_cor(cor_inicio, cor_fim, t)
                    set_pixel(superficie, x, y, cor)
