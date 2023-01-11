"""OpenCV image reader"""
import cv2
import numpy as np

def image_read(path: str) -> np.ndarray:
    """OpenCV image reader"""
    cv_res = cv2.imread(path)
    assert cv_res is not None, f"OpenCV returned None for '{path}'"
    bgr_image = cv_res[..., 0 : 3]
    b, g, r = cv2.split(bgr_image)
    image = cv2.merge([r, g, b]).astype(np.uint8)
    return image
