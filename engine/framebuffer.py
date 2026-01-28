
def set_pixel(superficie, x, y, color):
    if 0 <= x < superficie.get_width() and 0 <= y < superficie.get_height():
        superficie.set_at((x, y), color)

def getPixel(superficie, x, y):
    if 0 <= x < superficie.get_width() and 0 <= y < superficie.get_height():
        return superficie.get_at((x, y))
    return None

def clear(superficie):
    for y in range(superficie.get_height()):
        for x in range(superficie.get_width()):
            superficie.set_at((x, y), (0, 0, 0))


def clear_color(superficie, cor):
    """Preenche a superfície com a cor dada usando set_at (set_pixel)."""
    for y in range(superficie.get_height()):
        for x in range(superficie.get_width()):
            superficie.set_at((x, y), cor)