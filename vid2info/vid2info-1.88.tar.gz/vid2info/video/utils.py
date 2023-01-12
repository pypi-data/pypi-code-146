def calculate_frame_size_keeping_aspect_ratio(original_h: int, original_w: int,
                                              new_h: int | None, new_w: int | None) -> tuple[int, int]:
    """
    When only one of the frame size dimensions is given, the other one is calculated keeping the
    aspect ratio with the original video.

    :param original_h: int. The original video height.
    :param original_w: int. The original video width.

    :param new_h: int or None. Height of the frame. If None, w must be provided.
    :param new_w: int or None. Width of the frame. If None, h must be provided.

    :return: The height and width of the frame.
    """

    if new_h is None and new_w is not None:
        new_h = int(round(original_h * new_w / original_w))
    elif new_h is not None and new_w is None:
        new_w = int(round(original_w * new_h / original_h))
    else:
        raise ValueError(f'Only one of the frame size dimensions must be provided.'
                         f' Got h={new_h} and w={new_w}.')
    return new_h, new_w
