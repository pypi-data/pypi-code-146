#!/usr/bin/env python3
from typing import List, Union, Callable, Set, Dict, Tuple, Optional
from dofast.base.command import CliCommand
import os

def rounded_corners(image_name: str, rad: int = -1):
    """Add rounded_corners to images"""
    import uuid
    from PIL import Image, ImageDraw
    im = Image.open(image_name)
    w, h = im.size
    if rad < 0:
        hmean = 2 * w * h / (w + h)
        rad = int(hmean * 0.025)
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, "white")
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    export_name = f'{uuid.uuid4()}.png'
    print(f'Export to {export_name}')
    im.save(export_name)
    return im

def rc(path:str, radis:int=-1):
    rounded_corners(path, radis)
    