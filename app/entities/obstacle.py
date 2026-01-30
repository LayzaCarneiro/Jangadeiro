
from engine.framebuffer import set_pixel

def draw_obstacle(superficie, x, y, tamanho=14):
    """
    Obstáculo simples (rocha) vista de cima
    """
    for dy in range(-tamanho, tamanho + 1):
        for dx in range(-tamanho, tamanho + 1):
            if dx*dx + dy*dy <= tamanho*tamanho:
                cor = (80, 80, 90)
                if dx*dx + dy*dy > (tamanho-2)*(tamanho-2):
                    cor = (50, 50, 60)  # contorno
                set_pixel(superficie, x + dx, y + dy, cor)
