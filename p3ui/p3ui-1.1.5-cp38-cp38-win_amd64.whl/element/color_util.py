from p3ui.native import Color


def color_mul(color, scalar: float):
    scalar = scalar - int(scalar)
    if scalar < 0:
        return Color(0, 0, 0, 0)
    return Color(int(color.red * scalar),
                 int(color.green * scalar),
                 int(color.blue * scalar),
                 int(color.alpha * scalar))


def color_add(c1: Color, c2: Color):
    return Color(
        min(c1.red + c2.red, 255),
        min(c1.green + c2.green, 255),
        min(c1.blue + c2.blue, 255),
        min(c1.alpha + c2.alpha, 255))


Color.__mul__ = color_mul
Color.__rmul__ = color_mul
Color.__add__ = color_add
