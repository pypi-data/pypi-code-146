from aicsimageio import AICSImage
import cv2 as cv

from .conversions import conversions


def align(
    raw_image_path_one: str,
    raw_image_path_two: str,
    scene: str = "",
    eval_method: str = "cv.TM_CCOEFF_NORMED",
    objective: str = "20X",
) -> tuple:

    """Process Two .czi images to determine predicted micron shift from `raw_image_path_one` to `raw_image_path_two`

    Parameters
    ----------
    raw_image_path_one : str
        Path to the original image. (timepoint 0).
    raw_image_path_two : str
        Path to the new image. (timepoint 1).

    Keyword Arguments
    -----------------
    scene: str
        An optional parameter to look at a particular scene of a .czi.
    env_method: str
        The opencv2 evaluation method you would like to use. Default is set to cv.TM_CCOEFF_NORMED.
    objective: str
        The magnification of the image in order to determine the pixel to micron ratio. Default is
        set to 20X.

    Returns
    -------
    adjusted_shift: tuple(int,int)
        Returns the predicted shift in microns (x,y).
    """

    # Read in Images as AICSImage
    img1 = AICSImage(raw_image_path_one)
    img2 = AICSImage(raw_image_path_two)
    micron_conversion_const = conversions.MICRON_CONVERSION[objective]
    # AICS Image defaults to the first scene
    if scene != "":
        img1.set_scene(scene)
        img2.set_scene(scene)

    # Building images from AICSImage, C and Z can be varied if image is not accurate
    temp_image_1 = img1.get_image_data("XY", C=0, Z=0, S=0, T=0)
    temp_image_2 = img2.get_image_data("XY", C=0, Z=0, S=0, T=0)

    # Image Formatting
    temp_image_1 = cv.normalize(temp_image_1, None, 0, 255, cv.NORM_MINMAX).astype(
        "uint8"
    )
    temp_image_2 = cv.normalize(temp_image_2, None, 0, 255, cv.NORM_MINMAX).astype(
        "uint8"
    )

    # Creating a padded template (Padding 250 Pixels)
    template = temp_image_2[250:-250, 250:-250]
    # w, h = template.shape[::-1] # Likely used later to adjust (250)

    # Evaluate matches
    method = eval(eval_method)
    res = cv.matchTemplate(temp_image_1, template, method)
    _, _, min_loc, max_loc = cv.minMaxLoc(res)

    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc

    # Determining shift
    shift = [top_left[0] - 250, top_left[1] - 250]

    # adjust for rotation by AicsImage
    adjusted_shift = (
        int(micron_conversion_const * -shift[1]),
        int(micron_conversion_const * shift[0]),
    )

    return adjusted_shift
