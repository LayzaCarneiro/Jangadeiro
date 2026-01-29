
def interpolar_cor(cor1, cor2, t):
    """
    Interpola linearmente entre duas cores RGB.
    t: 0.0 = cor1, 1.0 = cor2
    """
    r1, g1, b1 = cor1
    r2, g2, b2 = cor2
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    return (r, g, b)