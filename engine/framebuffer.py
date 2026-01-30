
def set_pixel(superficie, x, y, color):    
    """
    Define a cor de um pixel específico na superfície.

    Args:
        superficie: pygame.Surface onde desenhar
        x, y: coordenadas do pixel (inteiros ou float)
        color: tupla (R, G, B) ou (R, G, B, A)
    
    Observações:
        - Verifica limites para não gerar erro.
        - Converte as coordenadas para inteiros.
    """
    if 0 <= x < superficie.get_width() and 0 <= y < superficie.get_height():
        superficie.set_at((int(x), int(y)), color)

def getPixel(superficie, x, y):
    """
    Retorna a cor de um pixel específico na superfície.

    Args:
        superficie: pygame.Surface de onde ler
        x, y: coordenadas do pixel

    Returns:
        Tupla da cor (R, G, B) ou (R, G, B, A) se dentro dos limites,
        None caso esteja fora da superfície.
    """
    if 0 <= x < superficie.get_width() and 0 <= y < superficie.get_height():
        return superficie.get_at((x, y))
    return None

def clear(superficie):
    """
    Limpa toda a superfície preenchendo-a com preto (0, 0, 0).

    Args:
        superficie: pygame.Surface a ser limpa
    """
    for y in range(superficie.get_height()):
        for x in range(superficie.get_width()):
            superficie.set_at((x, y), (0, 0, 0))


def clear_color(superficie, cor):
    """
    Preenche toda a superfície com uma cor específica usando set_at.

    Args:
        superficie: pygame.Surface a ser preenchida
        cor: tupla (R, G, B) ou (R, G, B, A) com a cor desejada
    
    Observações:
        - Funciona de forma similar a `Surface.fill`, mas escreve pixel a pixel.
        - Útil para testes de renderização manual ou efeitos de desenho pixel a pixel.
    """
    for y in range(superficie.get_height()):
        for x in range(superficie.get_width()):
            superficie.set_at((x, y), cor)