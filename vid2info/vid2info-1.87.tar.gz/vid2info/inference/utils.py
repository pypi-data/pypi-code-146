"""
Pipeline utils. This file include functions that will help to format the data

Author: Eric Canas.
Github: https://github.com/Eric-Canas
Email: eric@ericcanas.com
Date: 15-07-2022
"""
import math

import numpy as np
import torch
from warnings import warn

# IDS
from vid2info.inference.config import XMIN, YMIN, YMAX, XMAX, CONFIDENCE, CLASS_ID, CLASS_NAME, BBOX_XYXY, UINT8_TO_FLOAT, \
    INFERENCE_DEVICE

DEFAULT_DEVICE = torch.device(INFERENCE_DEVICE)

def bbox_to_dict(bbox: list | tuple | np.ndarray,
                 class_names: list | tuple | np.ndarray | None = None,
                 **kwargs) -> dict:
    """
    Convert a bounding box in the format [x1, y1, x2, y2, conf[, class]] to a dictionary.

    Args:
        bbox: Iterable. A bounding box in the format [x1, y1, x2, y2, conf [, class]].
        class_names: Iterable. A list of class names.
        **kwargs: Additional arguments to be passed to the dictionary.

    Returns:
        A dictionary with the bounding box information. The dictionary has the following keys:
            - xmin: Integer. The x coordinate of the top left corner.
            - ymin: Integer. The y coordinate of the top left corner.
            - xmax: Integer. The x coordinate of the bottom right corner.
            - ymax: Integer. The y coordinate of the bottom right corner.
            - bbox_xyxy: Tuple. The bounding box in the format (x1, y1, x2, y2).
            - confidence: Float. The confidence of the bounding box.
            - class_id: Integer. The class id.
            - class_name: String. The class name.
        And additional arguments passed to the dictionary as kwargs.
    """
    assert 5 <= len(bbox) <= 6, f'Expected bounding box to have 5 or 6 elements: ' \
                                f'[x1, y1, x2, y2, conf [, class]]. Got {len(bbox)}.'
    if class_names is not None and len(bbox) == 5:
        warn("The bounding box doesn't contain a class (only 5 elements). class_names is ignored.")
    if isinstance(bbox, np.ndarray):
        bbox = bbox.tolist()
    x_min, y_min, x_max, y_max, confidence = bbox[:5]
    out = {XMIN: x_min, YMIN: y_min, XMAX: x_max, YMAX: y_max, BBOX_XYXY: (x_min, y_min, x_max, y_max),
           CONFIDENCE: confidence, **kwargs}
    if len(bbox) == 6:
        class_id = int(bbox[5])
        out[CLASS_ID] = class_id
        if class_names is not None:
            out[CLASS_NAME] = class_names[class_id]
    return out

def image_to_float_tensor(image: np.ndarray | torch.Tensor, is_bgr: bool = False,
                          device: torch.device = DEFAULT_DEVICE) -> torch.Tensor:
    """
    Return the given image as a tensor in format torch.float32 in the correct RGB format.
    :param image: np.ndarray or torch.tensor as uint8 (0, 255) or float32 (0., 1.). The image to convert,
                  in format (H, W, C). Channels must be 3, RGB or BGR.
    :param is_bgr: Boolean. If True, the image is in BGR format, otherwise it is in RGB format.
    :param device: String. The device to use for the tensor.
    :return: torch.Tensor in format torch.float32. The image in format (H, W, C) within the range (0., 1.).
    """
    if device.type.startswith('cuda'):
        assert torch.cuda.is_available(), 'CUDA is not available.'
    else:
        assert device.type == 'cpu', f'Only cuda and cpu devices are supported. Got{device}.'

    assert image.ndim in (3, 4), f'Expected image to have 3 or 4 dimensions. Got {image.ndim}.'
    assert image.shape[-1] == 3, f'Expected image to have 3 channels (format ([B,] H, W, 3). Got {image.shape}.'

    if image.dtype == np.uint8:
        image = torch.tensor(data=image, dtype=torch.float32, device=device) * UINT8_TO_FLOAT
    elif image.dtype == np.float32:
        image = torch.tensor(data=image, dtype=torch.float32, device=device)
    elif image.dtype == torch.uint8:
        image = image.to(device=device) * UINT8_TO_FLOAT
    elif image.dtype == torch.float32:
        image = image.to(device=device)
    else:
        raise TypeError(f'Expected image to be in format np.uint8, np.float32, torch.uint8 or torch.float32. '
                        f'Got {image.dtype}.')
    if is_bgr:
        image = image[..., [2, 1, 0]].contiguous()

    assert torch.max(image).item() <= 1. and torch.min(image).item() >= 0., \
        f'Image is expected to be in range (0., 1.). Got ({torch.min(image).item()}, {torch.max(image).item()}).'

    return image

def get_l_r_pad(value: int) -> tuple[int, int]:
    """
    Convert an integer to a tuple of two integers to be used for padding purposes.
    Formula is: (floor(value/2), ceil(value/2)).
    This function is used to set a padding standard so avoiding errors when setting pads.

    :param value: Integer. The total number of pixels to add.
    :return: Tuple of two integers. The left and right padding (floor(value/2), ceil(value/2)).
    """
    return (int(math.floor(value/2)), int(math.ceil(value/2)))

def crop_bbox_from_image(image: np.ndarray,
                         bbox_xyxy: np.ndarray | list[float | int, float | int, float | int, float | int] |
                                    tuple[float|int, float|int, float|int, float|int],
                         is_normalized: bool = False, copy = True) -> np.ndarray:
    """
    Crop a bounding box from an image.
    :param image: np.ndarray. The image to crop.
    :param bbox_xyxy: np.ndarray or iterable of four floats or ints, in the formate (x1, y1, x2, y2). The bounding box
                 to crop.
    :param is_normalized: Boolean. If True, the bounding box is in normalized coordinates, otherwise it is in pixels.

    :return: np.ndarray. The cropped image.
    """
    assert type(is_normalized) == bool, f'Expected is_normalized to be a boolean. Got {is_normalized}.'
    assert image.ndim in (2, 3), f'Expected image to have 3 or 2 dimensions (H, W [,C]). Got {image.shape}.'
    assert len(bbox_xyxy) == 4, f'Expected bounding box to have 4 elements. Got {len(bbox_xyxy)}.'

    h, w = image.shape[:2]
    # Denormalize the bounding box
    if is_normalized:
        assert min(bbox_xyxy) >= -0.5 and max(bbox_xyxy) <= 1.5, f'Expected bounding box to be in normalized coordinates. ' \
                                                     f'Got {bbox_xyxy}.'
        bbox_xyxy = tuple(int(np.clip(a=round(coord * size), a_min=0., a_max=size))
                                    for coord, size in zip(bbox_xyxy, (w, h, w, h)))
    x1, y1, x2, y2 = bbox_xyxy
    # Crop it
    cropped_frame = image[y1:y2, x1:x2]
    # Copy it if needed (to avoid changing the original image and reduce memory usage)
    if copy:
        cropped_frame = cropped_frame.copy()
    return cropped_frame

def raw_yolo_bboxes_to_xyxy_co_cl(preds : torch.Tensor):
    """
    Convert the raw predictions of the YOLO model (x_center, y_center, h, w, conf, class1_conf, ...)
     to the format (x, y, w, h, conf, class).
    :param preds: torch.Tensor. The raw predictions of the YOLO model. In format (B, N, 5 + C).
    :return: torch.Tensor. The predictions in the format (B, N, 6) - bboxes:(x, y, w, h, conf, class).
    """
    assert preds.ndim in (2, 3), f'Expected predictions to have 2 or 3 dimensions ([B,] N, 5 + C). Got {preds.ndim}.'
    assert preds.shape[-1] > 5, f'Expected predictions to have 5 + C elements. Got {preds.shape}.'

    # Get the bounding boxes
    preds[..., :2] -= preds[..., 2:4] * 0.5
    preds[..., 2:4] += preds[..., :2]
    # Multiply general confidence by class confidence
    preds[..., 5:] *= preds[..., 4:5]
    # Get the index and conf of max class
    conf, class_idx = torch.max(preds[..., 5:], dim=-1)
    preds[..., 4] = conf
    preds[..., 5] = class_idx.to(dtype=preds.dtype)
    return preds[..., :6]