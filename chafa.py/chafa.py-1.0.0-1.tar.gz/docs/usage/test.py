from chafa import *
from chafa.loader import Loader

config = CanvasConfig()

config.height = 30
config.width  = 30

config.pixel_mode = PixelMode.CHAFA_PIXEL_MODE_SIXELS

loader = Loader("./snake.jpg")

term_db = TermDb()
info    = term_db.detect()

print(info.detect_capabilities())

# config.calc_canvas_geometry(
#     loader.width, loader.height,
#     11/24
# )

# config.cell_height = 24
# config.cell_width  = 11

canvas = Canvas(config)

canvas.draw_all_pixels(
    loader.pixel_type,
    loader.get_pixels(),
    loader.width, loader.height,
    loader.rowstride
)

print(canvas.print(fallback=True).decode())

