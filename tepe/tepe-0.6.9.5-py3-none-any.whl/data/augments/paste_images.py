import random

import cv2
import numpy as np


def rotation(image, angle, center=None, scale=1) -> np.ndarray:
    """

    Args:
        image (np.ndarray):
        angle: 0-360,逆时针旋转
        center: rotation center
        scale: image scale factor

    Returns:

    """
    h, w = image.shape[:2]
    if center is None:
        center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, scale)
    dst = cv2.warpAffine(image, M, (w, h), borderValue=0)
    return dst


def add_alpha_channel(im) -> np.ndarray:
    """ 为原图添加透明通道"""
    b, g, r = cv2.split(im)
    a = np.ones(b.shape, dtype=b.dtype) * 255  # 创建Alpha通道
    img_new = cv2.merge((b, g, r, a))  # 融合通道
    return img_new


def paste_images(src_img, png_imgs, fac=0.4) -> np.ndarray:
    """
    将透明的png图像贴到三通道jpg上
    Args:
        src_img (str | np.ndarray): jpg image path or array
        png_imgs (list[str]): png image paths
        fac (float): png scale factor

    Returns:

    """
    src = src_img
    if isinstance(src_img, str):
        src = cv2.imread(src_img, cv2.IMREAD_UNCHANGED)
    if src.shape[2] != 4:
        src = add_alpha_channel(src)
    src_h, src_w = src.shape[:2]

    for png_img in png_imgs:
        im = cv2.imread(png_img, cv2.IMREAD_UNCHANGED)
        h, w = im.shape[:2]

        ## random rotation
        im = rotation(im.copy(), random.randint(-5, 5))
        im = cv2.resize(im, (int(w * fac), int(h * fac)))
        new_h, new_w = im.shape[:2]

        ## random select paste position
        x0 = random.randint(0, src_w - new_w)
        y0 = random.randint(0, src_h - new_h)
        x1 = x0 + new_w
        y1 = y0 + new_h

        ## paste
        alpha_png = im[:, :, 3] / 255.0
        alpha_jpg = 1 - alpha_png
        for c in range(3):
            src[y0:y1, x0:x1, c] = alpha_jpg * src[y0:y1, x0:x1, c] + alpha_png * im[:, :, c]

    return src


if __name__ == '__main__':
    dst = paste_images(
        src_img="../images/paste_img/example.jpg",
        png_imgs=["../images/paste_img/cat.png", "../images/paste_img/cat2.png"]
    )

    cv2.namedWindow('dst', cv2.WINDOW_FREERATIO)
    cv2.imshow('dst', dst)
    cv2.waitKey()
