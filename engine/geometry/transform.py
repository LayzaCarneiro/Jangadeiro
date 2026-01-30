import math

# =====================================================
# MATRIZES 2D HOMOGÊNEAS
# =====================================================
def identidade():
    return [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]

def translacao(tx, ty):
    return [
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ]

def escala(sx, sy):
    return [
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ]

def rotacao(theta):
    c = math.cos(theta)
    s = math.sin(theta)
    return [
        [ c, -s, 0],
        [ s,  c, 0],
        [ 0,  0, 1]
    ]

def multiplica_matrizes(a, b):
    r = [[0]*3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                r[i][j] += a[i][k] * b[k][j]
    return r

# =====================================================
# COMPOSIÇÃO DE TRANSFORMAÇÕES
# =====================================================
def cria_transformacao():
    return identidade()

def aplica_transformacao(m, pontos):
    novos = []
    for x, y in pontos:
        v = [x, y, 1]
        x_novo = m[0][0]*v[0] + m[0][1]*v[1] + m[0][2]
        y_novo = m[1][0]*v[0] + m[1][1]*v[1] + m[1][2]
        novos.append((round(x_novo), round(y_novo)))
    return novos


# =====================================================
# ROTAÇÃO EM TORNO DE UM PONTO (PIVÔ)
# =====================================================
def rotacionar_pontos_em_torno_de(pontos, cx, cy, theta):
    """
    Rotaciona uma lista de pontos (x, y) em theta radianos
    em torno do ponto (cx, cy). 
    Retorna nova lista de pontos (inteiros).
    """
    t_neg = translacao(-cx, -cy)
    r = rotacao(theta)
    t_pos = translacao(cx, cy)
    m = multiplica_matrizes(t_pos, multiplica_matrizes(r, t_neg))
    return aplica_transformacao(m, pontos)

# =====================================================
# Polígono em coordenadas absolutas
# =====================================================
poligono_original = [
    (200, 150),
    (300, 170),
    (320, 240),
    (250, 290),
    (190, 230)
]

# centro (pivô)
cx = sum(p[0] for p in poligono_original) / len(poligono_original)
cy = sum(p[1] for p in poligono_original) / len(poligono_original)

angulo = 0
tempo = 0