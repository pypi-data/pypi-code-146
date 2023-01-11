"""Title module"""
import numpy as np
from PIL import Image, ImageDraw, ImageOps

from .text import get_default_font, image_add_text, StrOrColor
from ...logger import logger

def image_add_title(image: np.ndarray, text: str, font: str = None, font_color: str = "white",
                    background_color: StrOrColor = "black", top_padding: int = None, size_px: int = None) -> np.ndarray:
    """Calls image_add_text to add title on an updated image with padding on top for space and text centered"""
    assert len(image.shape) == 3, f"Wrong image shape: {image.shape}"
    height, _ = image.shape[0 : 2]
    pil_image = Image.fromarray(image.astype(np.uint8))
    draw = ImageDraw.Draw(pil_image)

    if top_padding is None:
        top_padding = int(height * 0.15)
        logger.debug2(f"Top padding not provided. Giving 15% of the image = {top_padding}")

    if size_px is None:
        size_px = top_padding

    if font is None:
        font = get_default_font(size_px=size_px)

    # Expand the image with (left=0, top=top_padding, right=0, bottom=0)
    border = (0, top_padding, 0, 0)
    expanded_image = ImageOps.expand(pil_image, border=border, fill=background_color)
    expanded_image = np.array(expanded_image)
    text_width, text_height = draw.textsize(text, font)
    position = -text_height // 4.8, (expanded_image.shape[1] - text_width) // 2
    return image_add_text(expanded_image, text, position, font, font_color)
