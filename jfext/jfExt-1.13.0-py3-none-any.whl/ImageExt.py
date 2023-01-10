# -*- coding: utf-8 -*-
"""
jfExt.ImageExt.py
~~~~~~~~~~~~~~~~~

:copyright: (c) 2018-2022 by the Ji Fu, see AUTHORS for more details.
:license: MIT, see LICENSE for more details.
"""

from icecream import ic # noqa


def image_to_square(in_file, out_file, size=1024, background_color=(255, 255, 255)):
    """
    >>> 图片转换成正方形
    :param {String} in_file: 图片读取地址
    :param {String} out_file: 图片输出地址
    :param {Int} size: 图片长度/宽度
    :param {(Int, Int, Int)} background_color: 背景颜色
    """
    from PIL import Image
    image = Image.open(in_file)
    image = image.convert('RGB')
    w, h = image.size
    # 创建背景图，颜色值为127
    background = Image.new('RGB', size=(max(w, h), max(w, h)), color=(255, 255, 255))
    # 一侧需要填充的长度
    length = int(abs(w - h) // 2)
    # 粘贴的位置
    box = (length, 0) if w < h else (0, length)
    background.paste(image, box)
    # 缩放
    image_data = background.resize((1024, 1024))
    # background.show()
    image_data.save(out_file)
