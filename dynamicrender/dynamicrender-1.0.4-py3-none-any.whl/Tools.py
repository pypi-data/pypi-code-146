import asyncio
import httpx
import numpy as np
from PIL import Image, ImageDraw
from io import BytesIO
from typing import Optional, Union


async def merge_pictures(pic_list: list) -> Image.Image:
    img_list = [i for i in pic_list if i is not None]
    temp = np.array(Image.new("RGBA", (1080, 0), (255, 255, 255)))
    for i in img_list:
        temp = np.concatenate((temp, np.array(i)))
    return Image.fromarray(temp)


async def circle_picture(img: Image.Image, scal_size: Optional[int] = None) -> Image.Image:
    """
     Make the picture round
    :param img:
    :param scal_size:
    :return:
    """

    img_origin_size = img.size
    img = img.resize((img_origin_size[0] * 3, img_origin_size[1] * 3))
    img_size = img.size

    mask = Image.new("L", (img_size[0], img_size[1]), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, img_size[0], img_size[1]), fill=255)
    img.putalpha(mask)
    draw = ImageDraw.Draw(img)
    draw.ellipse((0, 0, img_size[0], img_size[1]),
                 outline=(251, 114, 153), width=10)
    img = img.resize(img_origin_size)
    if scal_size:
        img = img.resize((scal_size, scal_size))
    return img


async def get_pictures(url: Union[str, list], img_size: Union[int, tuple, None] = None) -> Union[
    None, Image.Image, list]:
    """
    get images from net
    :param img_size: If the image needs to be scaled, this parameter is the size of the scaled image
    :param url:
    :return:
    """

    async with httpx.AsyncClient() as client:
        if isinstance(url, str):
            if img_size:
                img = await send_request(client, url, img_size)
            else:
                img = await send_request(client, url)
            return img
        if isinstance(url, list):
            if img_size:
                task = [send_request(client, i, img_size) for i in url]
            else:
                task = [send_request(client, i) for i in url]
            result = await asyncio.gather(*task)
            return result
        else:
            return None


async def send_request(client: httpx.AsyncClient, url: str, img_size: Union[int, tuple, None] = None) -> Optional[
    Image.Image]:
    """
    发送网络请求
    :param img_size: If the image needs to be scaled, this parameter is the size of the scaled image
    :param client: client
    :param url: image url
    :return:
    """
    try:
        response = await client.get(url)
        img = Image.open(BytesIO(response.content))
        img = img.convert("RGBA")
        if img_size:
            if isinstance(img_size, int):
                img = img.resize((img_size, img_size))
            else:
                img = img.resize(img_size)
        return img
    except Exception:
        return None
