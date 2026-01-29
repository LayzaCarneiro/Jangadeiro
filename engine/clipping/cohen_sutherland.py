INSIDE = 0
LEFT   = 1
RIGHT  = 2
BOTTOM = 4
TOP    = 8


def compute_outcode(x, y, xmin, ymin, xmax, ymax):
    code = INSIDE

    if x < xmin:
        code |= LEFT
    elif x > xmax:
        code |= RIGHT

    if y < ymin:
        code |= TOP
    elif y > ymax:
        code |= BOTTOM

    return code


def cohen_sutherland_clip(x0, y0, x1, y1, xmin, ymin, xmax, ymax):
    outcode0 = compute_outcode(x0, y0, xmin, ymin, xmax, ymax)
    outcode1 = compute_outcode(x1, y1, xmin, ymin, xmax, ymax)

    while True:
        if not (outcode0 | outcode1):
            return int(x0), int(y0), int(x1), int(y1)

        if outcode0 & outcode1:
            return None

        outcode_out = outcode0 if outcode0 else outcode1

        if outcode_out & TOP:
            x = x0 + (x1 - x0) * (ymin - y0) / (y1 - y0)
            y = ymin

        elif outcode_out & BOTTOM:
            x = x0 + (x1 - x0) * (ymax - y0) / (y1 - y0)
            y = ymax

        elif outcode_out & RIGHT:
            y = y0 + (y1 - y0) * (xmax - x0) / (x1 - x0)
            x = xmax

        else:  # LEFT
            y = y0 + (y1 - y0) * (xmin - x0) / (x1 - x0)
            x = xmin

        if outcode_out == outcode0:
            x0, y0 = x, y
            outcode0 = compute_outcode(x0, y0, xmin, ymin, xmax, ymax)
        else:
            x1, y1 = x, y
            outcode1 = compute_outcode(x1, y1, xmin, ymin, xmax, ymax)
