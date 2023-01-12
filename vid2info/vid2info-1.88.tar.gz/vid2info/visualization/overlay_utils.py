"""
Utils that helps to overlay the scene state annotations on a given image.

Author: Eric Canas.
Github: https://github.com/Eric-Canas
Email: eric@ericcanas.com
Date: 17-07-2022
"""

import numpy as np
import cv2
from time import time
from collections import deque

from vid2info.state.scene_state import SceneState
from vid2info.state.element_state import ElementState

from vid2info.visualization.config import DEFAULT_OVERLAY_CORNER, OVERLAY_CORNER_PAD, GENERAL_OVERLAY_FONT_SIZE, \
    DISPLAYABLE_GENERAL_INFORMATION, CURRENT_TIME, DISPLAYABLE_INFORMATION_TEXTS, TIME_FORMAT, DEFAULT_TEXT_COLOR, \
    GENERAL_INFORMATION_DISPLAY_ORDER, NO_ELEMENT_TEXT, CURRENT_FPS, DEFAULT_INTERLINE_SPACE, OLDER_ELEMENT_AGE, \
    ELEMENT_AGE_TIME_FORMAT, YOUNGER_ELEMENT_AGE, DETECTIONS_PER_ELEMENT, BBOXES_COLOR_MAP, DEFAULT_BBOX_THICKNESS, \
    BBOX_INFO_FONT_SIZE, MAX_BBOX_COLORS, BBOX_AGE_FONT_SIZE, DEFAULT_BBOX_INFO_THICKNESS, DEFAULT_SEGMENTATION_ALPHA, \
    MIN_BBOX_ALPHA, TRACK_ID, COLOR_BY_OPTIONS, CLASS
from vid2info.visualization.general_utils import apply_pad_on_shortest_axis
from vid2info.utils.general import time_as_str

from matplotlib.colors import LinearSegmentedColormap

FPS_BUFFER = deque(maxlen=24)


def overlay_annotations(image: np.ndarray, scene_state: SceneState, is_bgr: bool =True,
                        color_by: str = TRACK_ID) -> np.ndarray:
    """
    Overlay the scene state annotations on the given image.

    :param image: np.ndarray. Image to overlay the annotations on. In the format (H, W, 3). If is_bgr is True,
            it is assumed to be in BGR forma, otherwise it is assumed to be in RGB.
    :param scene_state: SceneState. The scene state to display, it will contain the tracking information of the
            elements in the scene.
    :param is_bgr: bool. If True, the image is assumed to be in BGR format, otherwise it is assumed to be in RGB.
    :param color_by: str. The color to use for the bounding boxes. Can be one of the following:
        - 'track_id': Color the bounding boxes by the track id.
        - 'class': Color the bounding boxes by the element age.

    :return np.ndarray. The image with the annotations overlaid.
    """
    assert color_by in COLOR_BY_OPTIONS, f"color_by must be one of: {COLOR_BY_OPTIONS}. Got: {color_by}"
    # Overlay the element annotations
    image = overlay_element_bboxes(image=image, scene_state=scene_state, is_bgr=is_bgr, color_by=color_by)

    # Overlay the general annotations
    image = overlay_general_annotations(image=image, scene_state=scene_state, is_bgr=is_bgr)

    return image


def overlay_general_annotations(image: np.ndarray, scene_state: SceneState, is_bgr: bool = True,
                                overlay_at_xy: tuple[float, float] | list[float, float] = DEFAULT_OVERLAY_CORNER,
                                overlay_pad: float = OVERLAY_CORNER_PAD,
                                overlays_to_show: list[str, ...] | tuple[str, ...] | set[str, ...] | None = None,
                                font_size: float | int = GENERAL_OVERLAY_FONT_SIZE,) -> np.ndarray:
    """
    Overlay the general annotations on the given image.

    Args:
        image: np.ndarray. Image to overlay the annotations on. In the format (H, W, 3). If is_bgr is True,
            it is assumed to be in BGR forma, otherwise it is assumed to be in RGB.
        scene_state: SceneState. The scene state to display, it will contain the tracking information of the
            elements in the scene.
        is_bgr: bool. If True, the image is assumed to be in BGR format, otherwise it is assumed to be in RGB.
        overlay_at_xy: tuple of two floats. The position where to overlay. In the range (0., 1.). (0., 0.) will
            mean the top-left corner, while (1., 0.) will mean the top-right corner.
        overlay_pad: float. Pad to apply to overlay_at_xy. If greater than 0., it will at least keep this pad from the
            nearest edge of the image.
        overlays_to_show: iterable of strings or None. If it is not None, only the information specified in that
            list will be displayed. Possible values to display are: 'detections_per_element', 'current_time',
            'current_fps', 'older_element_age' and 'younger_element_age'.
        font_size: float or int. Font size of the overlay.

    Returns:
        np.ndarray. The image with the general annotations overlaid.
    """

    if overlays_to_show is None:
        overlays_to_show = DISPLAYABLE_GENERAL_INFORMATION
    else:
        assert type(overlays_to_show) in (list, tuple, set), f"overlays_to_show must be a list, tuple or set, " \
                                                                f"not {type(overlays_to_show)}"
        for overlay in overlays_to_show:
            assert overlay in DISPLAYABLE_GENERAL_INFORMATION, f"{overlay} is not a valid overlay to show. Valid values are: " \
                                                                f"{DISPLAYABLE_GENERAL_INFORMATION}"
        overlays_to_show = sorted(overlays_to_show, key=lambda x: GENERAL_INFORMATION_DISPLAY_ORDER[x])
    assert issubclass(type(scene_state), SceneState), f"scene_state must be of type SceneState (or inherit from it)," \
                                                      f"but it is {type(scene_state)}"
    assert all(0. <= x <= 1. for x in overlay_at_xy), f"overlay_at_xy must be in the range (0., 1.). Got {overlay_at_xy}"
    assert 0. <= overlay_pad <= 0.5, f"overlay_pad must be in the range (0., 0.5). Got {overlay_pad}"

    if overlay_pad > 0.:
        overlay_at_xy = apply_pad_on_shortest_axis(original_hw=image.shape[:2], corner_xy=overlay_at_xy,
                                                   pad=overlay_pad)

    row = 0
    for overlay_key in overlays_to_show:
        text = GENERATE_TEXT_FUNCTIONS[overlay_key](scene_state=scene_state)
        put_text(image=image, row=row, text= text, at_xy= overlay_at_xy, font_size= font_size, is_bgr=is_bgr)
        row += len(text)

    return image

def overlay_element_bboxes(image: np.ndarray, scene_state: SceneState, is_bgr: bool = True,
                           bbox_colors : LinearSegmentedColormap = BBOXES_COLOR_MAP,
                           color_by: str = TRACK_ID) -> np.ndarray:
    """
    Overlay all the element bounding boxes of the scene in the given image.

    :param image: np.ndarray. Image to overlay the annotations on. In the format (H, W, 3). If is_bgr is True,
            it is assumed to be in BGR forma, otherwise it is assumed to be in RGB.
    :param scene_state: SceneState. The scene state to display, it will contain the tracking information of the
            elements in the scene.
    :param is_bgr: bool. If True, the image is assumed to be in BGR format, otherwise it is assumed to be in RGB.
    :param color_by: str. The color to use for the bounding boxes. Can be one of the following:
        - 'track_id': Color the bounding boxes by the track id.
        - 'class': Color the bounding boxes by the element age.

    :return np.ndarray. The image with the element bounding boxes overlaid.
    """
    assert issubclass(type(scene_state), SceneState), f"scene_state must be of type SceneState (or inherit from it)," \
                                                      f"but it is {type(scene_state)}"
    assert type(image) is np.ndarray, f"image must be of type np.ndarray, not {type(image)}"
    assert image.ndim == 3, f"image must be of dimension 3, not {image.ndim}"
    assert image.shape[2] == 3, f"image must have 3 channels, not {image.shape[2]}"
    assert type(bbox_colors) is LinearSegmentedColormap, f"bbox_colors must be of type LinearSegmentedColormap, " \
                                                         f"Got {type(bbox_colors)}"

    for track_id, element_state in scene_state.elements.items():
        # Get the id^th color from the color map
        if color_by == TRACK_ID:
            color = bbox_colors(track_id*(bbox_colors.N//MAX_BBOX_COLORS) % (bbox_colors.N + 1))[:3]
        elif color_by == CLASS:
            color = bbox_colors(element_state.class_id*(bbox_colors.N//MAX_BBOX_COLORS) % (bbox_colors.N + 1))[:3]
        # Convert the color to BGR if needed
        if is_bgr:
            color = color[::-1]
        # Draw the bounding box
        image = draw_element_bbox(image=image, element_state=element_state, track_id = track_id,
                                  color=color, segmentation_color=color)

    return image

def draw_element_bbox(image: np.ndarray, element_state: ElementState, track_id: int,
                      color: tuple[float, float, float, [float]],
                      segmentation_color: tuple[float, float, float] | None = None,
                      segmentation_alpha: float = DEFAULT_SEGMENTATION_ALPHA,
                      info_font_size : float = BBOX_INFO_FONT_SIZE,
                      age_font_size : float = BBOX_AGE_FONT_SIZE,
                      thickness: int = DEFAULT_BBOX_THICKNESS,
                      info_thickness: int = DEFAULT_BBOX_INFO_THICKNESS,
                      min_bbox_alpha: float = MIN_BBOX_ALPHA) -> np.ndarray:
    """
    Draw the bounding box of the given element in the given image. Including the element information

    :param image: np.ndarray. Image to draw the bounding box on. In the format (H, W, 3). Channels must be in the same
            format of the color, it is RGBA if the image is RGB or BGRA if the image is BGR. It
    :param element_state: ElementState. The element state to display, it will contain the information of the detected
            object.
    :param color: tuple of three or four floats. The color of the bounding box. If the fourth element is given
            it will be used as the alpha channel. If it is not given, confidence will be used to determine the
            alpha channel.
    :param segmentation_color: tuple of three or four floats. The color of the segmentation. If the fourth element is
            given it will be used as the alpha channel. If it is not given, confidence will be used to determine the
            alpha channel. All classes within that bbox different that background will be colored with this color.

    :return np.ndarray. The image with the bounding box overlaid.
    """
    assert type(image) is np.ndarray, f"image must be of type np.ndarray, not {type(image)}"
    assert image.ndim == 3, f"image must be of dimension 3, not {image.ndim}"
    assert image.shape[2] == 3, f"image must have 3 channels, not {image.shape[2]}"
    assert issubclass(type(element_state), ElementState), f"scene_state must be of type SceneState (or inherit from it)," \
                                                      f"but it is {type(element_state)}"
    assert type(color) in (tuple, list, np.ndarray), f"Color must be an iterable. Got {type(color)}"
    assert 3 <= len(color) <= 4, f"Color must be of length 3 or 4. Got {len(color)}"
    if len(color) == 3:
        color = tuple(color) + (element_state.confidence,)
    assert 0. <= color[3] <= 1., f"Alpha channel must be in the range (0., 1.). Got {color[3]}"

    color, alpha = color[:3], max(color[3], min_bbox_alpha)
    if max(color) <= 1.:
        color = tuple(int(x*255) for x in color)
    h, w = image.shape[:2]
    # Get detection data
    bbox_xyxy, class_name, conf = element_state.bbox_xyxy, element_state.class_name, element_state.confidence
    detection_age = element_state.age_in_seconds
    detection_age = time_as_str(time_as_seconds=detection_age, time_format=ELEMENT_AGE_TIME_FORMAT)
    x1, y1, x2, y2 = tuple(int(np.clip(a=round(coord*shape), a_min=0., a_max=shape))
                           for coord, shape in zip(bbox_xyxy, (w, h, w, h)))

    text = f"{track_id} - {class_name}: {round(conf * 100, 1)}%"
    (text_w, text_h), _ = cv2.getTextSize(text=text, fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                          fontScale=info_font_size, thickness=info_thickness)
    aget_text = f"{detection_age}"
    (age_text_w, age_text_h), _ = cv2.getTextSize(text=aget_text, fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                                  fontScale=age_font_size, thickness=info_thickness)

    info_box_tl_corner, info_box_br_corner = (x1, y1 - (text_h*2)), (x1 + text_w, y1)
    text_tl_corner = (x1, y1 - int(text_h * 1.25))
    age_text_tl_corner = ((x1+x1+age_text_w)//2, info_box_tl_corner[1] - int(age_text_h*0.8))

    shapes = np.zeros_like(image, dtype=np.uint8)
    # Draw the bounding box
    shapes = cv2.rectangle(img=shapes, pt1=(x1, y1), pt2=(x2, y2), color=color, thickness=thickness)
    # Draw the filled rectangle
    shapes = cv2.rectangle(img=shapes, pt1=info_box_tl_corner, pt2=info_box_br_corner,
                           color=color, thickness=cv2.FILLED)
    segmentation_mask = element_state.element_segmentation_mask
    if segmentation_color is not None and segmentation_mask is not None:
        # Draw the segmentation mask
        shapes = overlay_segmentation_mask(image=shapes, segmentation_mask=segmentation_mask, bbox=(x1, y1, x2, y2),
                                            color=segmentation_color, alpha=segmentation_alpha,
                                            segmentation_mask_background_id=element_state.segmentation_background_class_idx)
    # Put it with the alpha
    image = cv2.addWeighted(src1=shapes, alpha=alpha, src2=image, beta=1., gamma=0.)
    # Draw the text in black inside

    image = cv2.putText(img=image, text=text, org=text_tl_corner, fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=info_font_size, color=DEFAULT_TEXT_COLOR, thickness=info_thickness)

    # Draw the age of the bbox
    image = cv2.putText(img=image, text=aget_text, org=age_text_tl_corner,
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=age_font_size,
                        color=color, thickness=thickness)

    return image

def overlay_segmentation_mask(image: np.ndarray, segmentation_mask: np.ndarray,
                              bbox: tuple[int, int, int, int] | None, color: tuple[float, float, float],
                              alpha: float = DEFAULT_SEGMENTATION_ALPHA,
                              segmentation_mask_background_id: int = 0) -> np.ndarray:
    assert type(image) is np.ndarray, f"image must be of type np.ndarray, not {type(image)}"
    assert image.ndim == 3, f"image must be of dimension 3 (format (H, W, C)), not {image.ndim}"
    assert type(segmentation_mask) is np.ndarray, f"segmentation_mask must be of type np.ndarray, not {type(segmentation_mask)}"
    assert segmentation_mask.ndim == 2, f"segmentation_mask must be of dimension 2 (format (H, W)), not {segmentation_mask.ndim}"

    if max(color) <= 1.:
        color = tuple(int(x*255) for x in color)
    assert min(color) >= 0 and max(color) <= 255, f"Color must be in the range [0, 255]. Got {color}"
    # Separate background from no-background
    colored_segmentation_mask = np.zeros(shape=segmentation_mask.shape + (3,), dtype=np.uint8)
    foreground_mask = segmentation_mask != segmentation_mask_background_id
    colored_segmentation_mask[foreground_mask] = color
    if bbox is None:
        assert segmentation_mask.shape == image.shape[:2], f"segmentation_mask must have the same shape as image if " \
                                                           f"bbox is not given. Got {segmentation_mask.shape} and " \
                                                            f"{image.shape[:2]}"
        # Overlay the segmentation mask
        image = cv2.addWeighted(src1=image, alpha=1., src2=colored_segmentation_mask, beta=alpha, gamma=0.)
    else:
        x1, y1, x2, y2 = bbox
        sub_image = image[y1:y2, x1:x2, :]
        assert segmentation_mask.shape == sub_image.shape[:2], \
            f"segmentation_mask must have the same shape as the bounding box. Got {segmentation_mask.shape} and " \
            f"{sub_image.shape[:2]} (Bounding box: {(x1, y1, x2, y2)})"
        # Overlay the segmentation mask
        image[y1:y2, x1:x2, :] = cv2.addWeighted(src1=sub_image, alpha=1., src2=colored_segmentation_mask,
                                                 beta=alpha, gamma=0.)
    return image

def put_text(image : np.ndarray, text : tuple[str, ...] | list[str, ...]  | str,
             at_xy : tuple[float | float] | list[float | float], row : int = 0,
             font_size : float = GENERAL_OVERLAY_FONT_SIZE, color : tuple[int, int, int] = DEFAULT_TEXT_COLOR,
             thickness : int = 1, line_type : int = cv2.LINE_AA,
             font_face : int = cv2.FONT_HERSHEY_SIMPLEX, is_bgr : bool = True) -> np.ndarray:
    """
    Put text on the given image.

    Args:
        image: np.ndarray. Image to put the text on. In the format (H, W, 3). If is_bgr is True,
            it is assumed to be in BGR forma, otherwise it is assumed to be in RGB.
        text: str. Text to put on the image.
        at_xy: tuple of two floats. The position where to put the text. In the range (0., 1.). (0., 0.) will
            mean the top-left corner, while (1., 0.) will mean the top-right corner.
        font_size: float or int. Font size of the overlay.
        color: tuple of three ints. Color of the text, specified in RGB, in the range (0, 255).
        thickness: int. Thickness of the text.
        line_type: int. Line type of the text.
        font_face: int. Font face of the text.
        is_bgr: bool. If True, the image is assumed to be in BGR format, otherwise it is assumed to be in RGB.

    Returns:
        np.ndarray. The image with the text put.
    """
    assert type(image) is np.ndarray, f"image must be of type np.ndarray, not {type(image)}"
    if type(text) is str: text = (text,)
    assert type(text) in (tuple, list, np.ndarray), f"text must be of type str, not {type(text)}"
    assert len(at_xy) == 2, f"at_xy must be of length 2, not {len(at_xy)}"
    assert 0. <= at_xy[0] <= 1. and 0. <= at_xy[1] <= 1., f"at_xy must be in the range (0., 1.). Got {at_xy}"
    assert len(color) == 3, f"color must be of length 3, not {len(color)}"

    if is_bgr:
        color = color[::-1]

    (text_w, text_h), _ = cv2.getTextSize(text=text[0], fontFace=font_face, fontScale=font_size, thickness=thickness)
    for row_i, line in enumerate(text, start=row):
        cv2.putText(img=image, text=line, org=(int(image.shape[1]*at_xy[0]),
                                  int(image.shape[0]*at_xy[1] + row_i*text_h*DEFAULT_INTERLINE_SPACE)),
                    fontFace=font_face, fontScale=font_size, color=color, thickness=thickness,
                    lineType=line_type)
    return image

#  -----------------------  GENERATE TEXT FUNCTIONS  -----------------------

def _get_current_time_text(scene_state: SceneState) -> tuple[str]:
    current_time = time_as_str(time_as_seconds=scene_state.timestamp, time_format=TIME_FORMAT)
    text = f"{DISPLAYABLE_INFORMATION_TEXTS[CURRENT_TIME]}: {current_time}"
    return (text,)

def _get_current_fps_text(scene_state: SceneState = None) -> tuple[str]:
    current_time = time()
    FPS_BUFFER.append(current_time)
    frame_time_diffs = np.diff(FPS_BUFFER)
    frame_rate = str(round(1 / np.mean(frame_time_diffs), ndigits=1)) if len(frame_time_diffs) > 1 else NO_ELEMENT_TEXT
    text = f"{DISPLAYABLE_INFORMATION_TEXTS[CURRENT_FPS]}: {frame_rate}"
    return (text,)

def _get_element_age_text(scene_state: SceneState, overlay_key : str) -> tuple[str]:
    assert overlay_key in (OLDER_ELEMENT_AGE, YOUNGER_ELEMENT_AGE), f"overlay_key must be either {OLDER_ELEMENT_AGE} or " \
                                                                    f"{YOUNGER_ELEMENT_AGE}. Got {overlay_key}"
    all_elements_age = scene_state.get_elements_age_in_seconds()
    if len(all_elements_age) > 0:
        # Find the key with the larger value
        order_function = max if overlay_key == OLDER_ELEMENT_AGE else min
        element = order_function(all_elements_age, key=all_elements_age.get)
        age = all_elements_age[element]
        age_text = time_as_str(time_as_seconds=age, time_format=ELEMENT_AGE_TIME_FORMAT)
        class_name = scene_state.elements[element].class_name
        text = f"{DISPLAYABLE_INFORMATION_TEXTS[overlay_key]}: {class_name} (id: {element})" \
               f" - {age_text}"
    else:
        text = f"{DISPLAYABLE_INFORMATION_TEXTS[overlay_key]}: {NO_ELEMENT_TEXT}"
    return (text,)

def _get_elements_count_text(scene_state: SceneState) -> tuple[str, ...]:
    texts = [f"{DISPLAYABLE_INFORMATION_TEXTS[DETECTIONS_PER_ELEMENT]}"]
    for class_name, count in scene_state.get_element_counts().items():
        texts.append(f"   {class_name}: {count}")
    return tuple(texts)

GENERATE_TEXT_FUNCTIONS = {
    CURRENT_TIME: _get_current_time_text,
    CURRENT_FPS: _get_current_fps_text,
    OLDER_ELEMENT_AGE: lambda scene_state: _get_element_age_text(scene_state=scene_state, overlay_key=OLDER_ELEMENT_AGE),
    YOUNGER_ELEMENT_AGE: lambda scene_state: _get_element_age_text(scene_state=scene_state, overlay_key=YOUNGER_ELEMENT_AGE),
    DETECTIONS_PER_ELEMENT: _get_elements_count_text
}