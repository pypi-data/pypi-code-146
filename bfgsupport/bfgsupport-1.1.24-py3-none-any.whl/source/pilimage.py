"""Various image handling utilities. """

import wx
from PIL import Image


def image_from_list(image_list):
    """Create a single image from a list of images."""
    widths, heights = zip(*(image.size for image in image_list))
    total_width = sum(widths)
    total_height = max(heights)

    pil_image = Image.new('RGBA', (total_width, total_height))
    x_offset = 0
    for image in image_list:
        pil_image.paste(image, (x_offset, 0))
        x_offset += image.size[0]
    return pil_image


def static_bitmap_from_pil_image(caller, pil_image, name=''):
    """Return a static bitmap from an image."""
    wx_image = wx.Image(pil_image.size[0], pil_image.size[1])
    wx_image.SetData(pil_image.convert('RGB').tobytes())
    if pil_image.mode == 'RGBA':
        wx_image.SetAlpha(pil_image.convert('RGBA').tobytes()[3::4])
    bitmap = wx.Bitmap(wx_image)
    static_bitmap = wx.StaticBitmap(caller, wx.ID_ANY, wx.NullBitmap, name=name)
    static_bitmap.SetBitmap(bitmap)
    return static_bitmap


def image_to_pil(image):
    """Convert wx.Image to PIL Image."""
    width, height = image.GetSize()
    data = image.GetData()

    red_image = Image.new('L', (width, height))
    red_image.frombytes(bytes(data[0::3]))
    green_image = Image.new('L', (width, height))
    green_image.frombytes(bytes(data[1::3]))
    blue_image = Image.new('L', (width, height))
    blue_image.frombytes(bytes(data[2::3]))

    if image.HasAlpha():
        alpha_image = Image.new('L', (width, height))
        alpha_image.frombytes(bytes(image.GetAlpha()))
        pil_image = Image.merge('RGBA', (red_image, green_image, blue_image, alpha_image))
    else:
        pil_image = Image.merge('RGB', (red_image, green_image, blue_image))
    return pil_image


def pil_to_image(pil_image):
    """Return a wx.image from a pil image."""
    wx_image = wx.Image(pil_image.size[0], pil_image.size[1])
    wx_image.SetData(pil_image.convert('RGB').tobytes())
    if pil_image.mode == 'RGBA':
        wx_image.SetAlpha(pil_image.convert('RGBA').tobytes()[3::4])
    return wx_image


def resize_image(image, size, scale=1):
    """Return a resized image."""
    width, height = size
    image_size = (int(width * scale), int(height * scale))
    image = image.resize(image_size, Image.ANTIALIAS)
    return image


def open(path):
    """Open the image."""
    return Image.open(path)


def scale_image(image, scale):
    """Return a scaled wx.image."""
    width = image.GetWidth() * scale
    height = image.GetHeight() * scale
    scaled_image = image.Scale(width, height)
    return scaled_image


def crop_horizontal(image, cropped_proportion):
    """Return a cropped image of the card."""
    pil_image = image_to_pil(image)
    width, height = pil_image.size
    crop_width = int(width * cropped_proportion)
    cropped_image = pil_image.crop((0, 0, crop_width, height))
    image = pil_to_image(cropped_image)
    return image
