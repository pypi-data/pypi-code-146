# MIT License
#
# Copyright (c) 2023 Johannes Fischer
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Varios functions based on: https://github.com/hansalemaos/PILasOPENCV/
# MIT License
#
# Copyright (c) 2019 Andreas Bunkahle
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from math import ceil
import freetype
from a_cv_imwrite_imread_plus import open_image_in_cv
import cv2
import numpy as np


def reverse_color(color):
    if len(color) == 3:
        return list(reversed(color))
    elif len(color) == 4:
        return list(reversed(color[:3])) + [color[-1]]
    return color


def center_text_at_certain_size_at_a_specific_point(
    img,
    text,
    maxwidth,
    maxheight,
    wheretoput=(200, 200),
    color=(255, 255, 0),
    add_thickness_each=10,
):
    imgOriginalScene = img.copy()

    farbe = reverse_color(color)
    intFontFace = cv2.FONT_HERSHEY_SIMPLEX
    fltFontScale = 0.01
    intFontThickness = int(ceil(fltFontScale * 1.5))
    textSize = (0, 0)
    addthick = 1
    addsize = 0.1
    upcounter = 0
    while True:
        upcounter = upcounter + 1
        if upcounter % add_thickness_each == 0:
            intFontThickness += addthick

        textSize2, baseline2 = cv2.getTextSize(
            text, intFontFace, fltFontScale, int(intFontThickness)
        )

        if textSize2[0] > maxwidth:
            break
        if textSize2[1] > maxheight:
            break
        fltFontScale = fltFontScale + addsize
        textSize, baseline = textSize2, baseline2
    if textSize == (0, 0):
        textSize = textSize2
    ptCenterOfTextAreaX = int(textSize[0] / 2) + wheretoput[0]
    ptCenterOfTextAreaY = int(textSize[1] / 2) + wheretoput[1]
    textSizeWidth, textSizeHeight = textSize  # unpack text size width and height

    ptLowerLeftTextOriginX = int(
        ptCenterOfTextAreaX - (textSizeWidth / 2)
    )  # calculate the lower left origin of the text area
    ptLowerLeftTextOriginY = int(
        ptCenterOfTextAreaY + (textSizeHeight / 2)
    )  # based on the text area center, width, and height
    texta = cv2.putText(
        imgOriginalScene,
        text,
        (ptLowerLeftTextOriginX, ptLowerLeftTextOriginY),
        intFontFace,
        fltFontScale,
        farbe,
        intFontThickness,
    )
    return (
        texta,
        ptLowerLeftTextOriginX,
        ptLowerLeftTextOriginY,
        intFontFace,
        fltFontScale,
        intFontThickness,
        textSize,
    )


def center_of_text_at_certain_size_at_a_specific_point_with_boxes(
    img,
    text,
    maxwidth,
    maxheight,
    wheretoput=(200, 200),
    color=(255, 255, 0),
    add_thickness_each=10,
    rectangle_border_size=5,
    rectangle_border_colors=((244, 255, 0), (244, 0, 255)),
):
    imgOriginalScene = img.copy()

    farbe = reverse_color(color)
    intFontFace = cv2.FONT_HERSHEY_SIMPLEX
    fltFontScale = 0.01
    intFontThickness = int(ceil(fltFontScale * 1.5))
    textSize = (0, 0)
    textSize2 = (0, 0)
    addthick = 1
    addsize = 0.1
    upcounter = 0
    while True:
        upcounter = upcounter + 1
        if upcounter % add_thickness_each == 0:
            intFontThickness += addthick

        textSize2, baseline2 = cv2.getTextSize(
            text, intFontFace, fltFontScale, int(intFontThickness)
        )

        if textSize2[0] > maxwidth:
            break
        if textSize2[1] > maxheight:
            break
        fltFontScale = fltFontScale + addsize
        textSize, baseline = textSize2, baseline2
    if textSize == (0, 0):
        textSize = textSize2
    ptCenterOfTextAreaX = int(textSize[0] / 2) + wheretoput[0]
    ptCenterOfTextAreaY = int(textSize[1] / 2) + wheretoput[1]
    textSizeWidth, textSizeHeight = textSize  # unpack text size width and height

    ptLowerLeftTextOriginX = int(
        ptCenterOfTextAreaX - (textSizeWidth / 2)
    )  # calculate the lower left origin of the text area
    ptLowerLeftTextOriginY = int(
        ptCenterOfTextAreaY + (textSizeHeight / 2)
    )  # based on the text area center, width, and height
    border_width = 20
    border_heigth = 20

    addition = rectangle_border_size
    newcolors = []
    for colo in rectangle_border_colors:
        newcolors.append((addition, reverse_color(colo)))
        addition = addition + rectangle_border_size
    newcolors = list(reversed(newcolors))

    for col_ in newcolors:
        rectangle_border_size = col_[0]
        imgOriginalScene = cv2.rectangle(
            imgOriginalScene,
            (
                wheretoput[0] - (border_width // 2) - rectangle_border_size,
                wheretoput[1] - (border_heigth // 2) - rectangle_border_size,
            ),
            (
                wheretoput[0]
                + textSize[0]
                + border_width
                + intFontThickness
                + rectangle_border_size,
                wheretoput[1]
                + textSize[1]
                + border_heigth // 2
                + intFontThickness
                + rectangle_border_size,
            ),
            col_[1],
            -1,
        )

    imgOriginalScene = cv2.rectangle(
        imgOriginalScene,
        (wheretoput[0] - (border_width // 2), wheretoput[1] - (border_heigth // 2)),
        (
            wheretoput[0] + textSize[0] + border_width + intFontThickness,
            wheretoput[1] + textSize[1] + border_heigth // 2 + intFontThickness,
        ),
        (0, 0, 255),
        -1,
    )

    texta = cv2.putText(
        imgOriginalScene,
        text,
        (ptLowerLeftTextOriginX, ptLowerLeftTextOriginY),
        intFontFace,
        fltFontScale,
        farbe,
        intFontThickness,
    )
    return (
        texta,
        ptLowerLeftTextOriginX,
        ptLowerLeftTextOriginY,
        intFontFace,
        fltFontScale,
        intFontThickness,
        textSize,
    )


def upperleft_of_text_at_certain_size_at_a_specific_point(
    img,
    text,
    maxwidth,
    maxheight,
    wheretoput=(200, 200),
    color=(255, 255, 0),
    add_thickness_each=10,
):
    imgOriginalScene = img.copy()

    farbe = reverse_color(color)
    intFontFace = cv2.FONT_HERSHEY_SIMPLEX
    fltFontScale = 0.01
    intFontThickness = int(ceil(fltFontScale * 1.5))
    textSize = (0, 0)
    textSize2 = (0, 0)

    addthick = 1
    addsize = 0.1
    upcounter = 0
    while True:
        upcounter = upcounter + 1
        if upcounter % add_thickness_each == 0:
            intFontThickness += addthick

        textSize2, baseline2 = cv2.getTextSize(
            text, intFontFace, fltFontScale, int(intFontThickness)
        )
        if textSize2[0] > maxwidth:
            break
        if textSize2[1] > maxheight:
            break
        fltFontScale = fltFontScale + addsize
        textSize, baseline = textSize2, baseline2
    if textSize == (0, 0):
        textSize = textSize2
    ptLowerLeftTextOriginX = wheretoput[0]
    ptLowerLeftTextOriginY = wheretoput[1]
    texta = cv2.putText(
        imgOriginalScene,
        text,
        (ptLowerLeftTextOriginX, ptLowerLeftTextOriginY),
        intFontFace,
        fltFontScale,
        farbe,
        intFontThickness,
    )
    return (
        texta,
        ptLowerLeftTextOriginX,
        ptLowerLeftTextOriginY,
        intFontFace,
        fltFontScale,
        intFontThickness,
        textSize,
    )


def getsize(text, ttf_font, scale=1.0, thickness=1):
    if isinstance(ttf_font, freetype.Face):
        slot = ttf_font.glyph
        width, height, baseline = 0, 0, 0
        previous = 0
        for i, c in enumerate(text):
            ttf_font.load_char(c)
            bitmap = slot.bitmap
            height = max(height, bitmap.rows + max(0, -(slot.bitmap_top - bitmap.rows)))
            baseline = max(baseline, max(0, -(slot.bitmap_top - bitmap.rows)))
            kerning = ttf_font.get_kerning(previous, c)
            width += (slot.advance.x >> 6) + (kerning.x >> 6)
            previous = c
    else:
        size = cv2.getTextSize(text, ttf_font, scale, thickness)
        width = size[0][0]
        height = size[0][1]
        baseline = size[1]
    return width, height, baseline


def getmask(text_to_write, ttf_font):
    text = f"|{text_to_write}|"
    slot = ttf_font.glyph
    width, height, baseline = getsize(text, ttf_font)
    width, _, _ = getsize(text_to_write, ttf_font)
    Z = np.zeros((height, width), dtype=np.ubyte)
    x, y = 0, 0
    previous = 0
    maxlentext = len(text) - 1
    for ini, c in enumerate(text):
        ttf_font.load_char(c)
        bitmap = slot.bitmap
        top = slot.bitmap_top
        left = slot.bitmap_left
        w, h = bitmap.width, bitmap.rows
        y = height - baseline - top
        if y <= 0:
            y = 0
        kerning = ttf_font.get_kerning(previous, c)
        x += kerning.x >> 6
        character = np.array(bitmap.buffer, dtype="uint8").reshape(h, w)
        if ini != 0 and ini != maxlentext:
            try:
                Z[y : y + h, x : x + w] += character
            except ValueError:
                while x + w > Z.shape[1]:
                    x = x - 1
                if x > 0:
                    Z[: character.shape[0], x : x + w] += character
            x += slot.advance.x >> 6
            previous = c
    return Z


def _paste(mother, child, x, y):
    "Pastes the numpy image child into the numpy image mother at position (x, y)"
    size = mother.shape
    csize = child.shape
    if y + csize[0] < 0 or x + csize[1] < 0 or y > size[0] or x > size[1]:
        return mother
    sel = [int(y), int(x), csize[0], csize[1]]
    csel = [0, 0, csize[0], csize[1]]
    if y < 0:
        sel[0] = 0
        sel[2] = csel[2] + y
        csel[0] = -y
    elif y + sel[2] >= size[0]:
        sel[2] = int(size[0])
        csel[2] = size[0] - y
    else:
        sel[2] = sel[0] + sel[2]
    if x < 0:
        sel[1] = 0
        sel[3] = csel[3] + x
        csel[1] = -x
    elif x + sel[3] >= size[1]:
        sel[3] = int(size[1])
        csel[3] = size[1] - x
    else:
        sel[3] = sel[1] + sel[3]
    childpart = child[csel[0] : csel[2], csel[1] : csel[3]]
    mother[sel[0] : sel[2], sel[1] : sel[3]] = childpart
    return mother


def split(im, image=None):
    _instance = im.copy()
    "splits the image into its color bands"
    if image is None:
        if len(_instance.shape) == 3:
            if _instance.shape[2] == 1:
                return _instance.copy()
            elif _instance.shape[2] == 2:
                l, a = cv2.split(_instance)
                return l, a
            elif _instance.shape[2] == 3:
                b, g, r = cv2.split(_instance)
                return b, g, r
            else:
                b, g, r, a = cv2.split(_instance)
                return b, g, r, a
        else:
            return _instance
    else:
        if len(_instance.shape) == 3:
            if image.shape[2] == 1:
                return image.copy()
            elif image.shape[2] == 2:
                l, a = cv2.split(image)
                return l, a
            elif image.shape[2] == 3:
                b, g, r = cv2.split(image)
                return b, g, r
            else:
                b, g, r, a = cv2.split(image)
                return b, g, r, a
        else:
            return _instance


def composite(background, foreground, mask, np_image=False, neg_mask=False):
    "pastes the foreground image into the background image using the mask"
    # Convert uint8 to float
    foreground = foreground.astype(float)
    old_type = background.dtype
    background = background.astype(float)
    # Normalize the alpha mask to keep intensity between 0 and 1
    if neg_mask:
        alphamask = mask.astype(float) / 255
    else:
        alphamask = (~mask).astype(float) / 255

    fslen = len(foreground.shape)
    if len(alphamask.shape) != fslen:
        img = np.zeros(foreground.shape, dtype=foreground.dtype)
        if fslen > 2:
            if foreground.shape[2] >= 2:
                img[:, :, 0] = alphamask
                img[:, :, 1] = alphamask
            if foreground.shape[2] >= 3:
                img[:, :, 2] = alphamask
            if foreground.shape[2] == 4:
                img[:, :, 3] = alphamask
            alphamask = img.copy()
    # Multiply the foreground with the alpha mask
    try:
        foreground = cv2.multiply(alphamask, foreground)
    except:
        if alphamask.shape[2] == 1 and foreground.shape[2] == 3:
            triplemask = cv2.merge((alphamask, alphamask, alphamask))
            foreground = cv2.multiply(triplemask, foreground)
        else:
            raise ValueError(
                "OpenCV Error: Sizes of input arguments do not match (The operation is neither 'array op array' (where arrays have the same size and the same number of channels), nor 'array op scalar', nor 'scalar op array') in cv::arithm_op, file ..\..\..\..\opencv\modules\core\src\arithm.cpp"
            )
    # Multiply the background with ( 1 - alpha )
    bslen = len(background.shape)
    if len(alphamask.shape) != bslen:
        img = np.zeros(background.shape, dtype=background.dtype)
        if bslen > 2:
            if background.shape[2] >= 2:
                img[:, :, 0] = alphamask
                img[:, :, 1] = alphamask
            if background.shape[2] >= 3:
                img[:, :, 2] = alphamask
            if background.shape[2] == 4:
                img[:, :, 3] = alphamask
            alphamask = img.copy()
    try:
        background = cv2.multiply(1.0 - alphamask, background)
    except:
        if alphamask.shape[2] == 1 and foreground.shape[2] == 3:
            background = cv2.multiply(1.0 - triplemask, background)
        else:
            raise ValueError(
                "OpenCV Error: Sizes of input arguments do not match (The operation is neither 'array op array' (where arrays have the same size and the same number of channels), nor 'array op scalar', nor 'scalar op array') in cv::arithm_op, file ..\..\..\..\opencv\modules\core\src\arithm.cpp"
            )
    outImage = cv2.add(foreground, background)
    outImage = outImage / 255
    outImage = outImage * 255
    outImage = outImage.astype(old_type)
    return outImage


def paste(imgbase, img_color, box=None, mask=None, transparency=-1):
    "pastes either an image or a color to a region of interest defined in box with a mask"
    _instance = imgbase.copy()
    if box is None:
        raise ValueError("cannot determine region size; use 4-item box")
    img_dim = (box[3] + 1, box[2] + 1)
    channels, depth = (
        2 if len(img_color.shape) == 2 else img_color.shape[-1],
        img_color.dtype,
    )
    colorbox = np.zeros((img_dim[0], img_dim[1], channels), dtype=depth)
    if channels > 2:
        colorbox[:] = img_color[0][0]
    else:
        colorbox[:] = img_color[0]
    _img_color = colorbox.copy()
    if mask is None:
        _instance = _paste(_instance, _img_color, box[0], box[1])
    else:
        # enlarge the image _img_color without resizing to the new_canvas
        new_canvas = np.zeros(_instance.shape, dtype=_instance.dtype)
        new_canvas = _paste(new_canvas, _img_color, box[0], box[1])

        if len(_instance.shape) == 3:
            if _instance.shape[2] == 4:  # RGBA
                *b, _mask = split(mask)

            elif _instance.shape[2] == 1:
                _mask = _instance.copy()
        else:
            _mask = _instance.copy()

        if mask.shape[:2] != new_canvas.shape[:2]:
            _new_mask = np.zeros(_instance.shape[:2], dtype=_instance.dtype)
            _new_mask = ~(_paste(_new_mask, mask, box[0], box[1]))
        else:
            _new_mask = ~mask
        if transparency > 0:
            calcmaxadd = _new_mask.copy()
            calcmaxadd[np.where(calcmaxadd >= np.max(img_color[0][0]))] = 0
            maxcolor = np.max(img_color[0][0])
            maxadd = 254 - maxcolor
            if transparency < maxadd:
                maxadd = transparency
            _new_mask[np.where(_new_mask <= maxcolor)] = (
                maxadd + _new_mask[np.where(_new_mask <= maxcolor)]
            )
        _instance = composite(_instance, new_canvas, _new_mask, np_image=True)
    return _instance


def get_image_mask(image, color):
    ink = reverse_color(color)
    img = np.zeros(image.shape, dtype=image.dtype)
    if len(img.shape) > 2:
        if img.shape[2] >= 2:
            img[:, :, 0] = ink[0]
            img[:, :, 1] = ink[1]
        if img.shape[2] >= 3:
            img[:, :, 2] = ink[2]
        if img.shape[2] == 4:
            img[:, :, 3] = 0
    else:
        img[:] = ink
    return img


def get_font_regular_size(fontpath=r"C:\Windows\Fonts\ANTQUAB.TTF", size=32):
    ttf_font = freetype.Face(fontpath)
    ttf_font.set_char_size(size * size)
    return ttf_font


def get_right_font_fix(text, fontpath=r"C:\Windows\Fonts\ANTQUAB.TTF", fixedsize=32):
    size = fixedsize
    # line = f"|{text}|"
    if isinstance(fontpath, str):
        ttf_font = freetype.Face(fontpath)
    else:
        ttf_font = fontpath

    ttf_font.set_char_size(size * size)
    width, height, baseline = getsize(text, ttf_font)
    _, height, _ = getsize("|", ttf_font)
    return ttf_font, size, width, height, getmask(text, ttf_font)


def get_right_font(
    text, fontpath=r"C:\Windows\Fonts\ANTQUAB.TTF", maxwidth=300, maxheight=100
):
    line = f"|{text}|"
    if isinstance(fontpath, str):
        ttf_font = freetype.Face(fontpath)
    else:
        ttf_font = fontpath
    size = 1
    width, height = 0, 0
    goodsize = size

    while True:
        ttf_font.set_char_size(size * size)
        width2, height2, baseline2 = getsize(line, ttf_font)
        width_substract, height_substract, baseline_substract = getsize("||", ttf_font)

        width2, height2, baseline2 = (
            width2 - width_substract,
            height2 - height_substract,
            baseline2 - baseline_substract,
        )
        if width2 <= maxwidth:
            width = width2
            goodsize = size
        if height2 <= maxheight:
            height = height2
            goodsize = size
        if height2 > maxheight:
            break
        if width2 > maxwidth:
            break
        size = size + 1
    if width == 0 and height == 0:
        width, height = width2, height2
    ttf_font.set_char_size(goodsize * goodsize)
    width, height, baseline = getsize(text, ttf_font)
    _, height, _ = getsize("|", ttf_font)
    return ttf_font, goodsize, width, height, getmask(text, ttf_font)


def gray_to_rgb(im):
    return cv2.cvtColor(im.copy(), cv2.COLOR_GRAY2BGR)


def convert_cv_image_to_3_channels(img):
    image = img.copy()
    if image.shape[-1] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

    elif image.shape[-1] == 2:
        image = gray_to_rgb(image)
    return image


def convert_cv_image_to_4_channels(img):
    image = img.copy()
    if image.shape[-1] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)

    elif len(image) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGBA)
    return image


def put_ttf_font_at_exact_location_with_exact_size(
    image,
    text,
    coords,
    color=(255, 255, 210),
    font=r"C:\Windows\Fonts\ANTQUAB.TTF",
    maxwidth=300,
    maxheight=100,
    fonttransparency=50,
):
    if fonttransparency > 0:
        color = [x if x < 255 else 254 for x in color]
    xy = coords
    ink = color
    ttf_font, goodsize, width, height, fontmask = get_right_font(
        text, fontpath=font, maxwidth=maxwidth, maxheight=maxheight
    )
    image = open_image_in_cv(image)
    img2 = convert_cv_image_to_4_channels(image)
    fontmask = convert_cv_image_to_4_channels(fontmask)
    img = get_image_mask(image=img2, color=ink)
    box = [int(xy[0]), int(xy[1]), int(xy[0] + width), int(xy[1] + height)]
    bala = paste(
        imgbase=img2,
        img_color=img,
        box=box,
        mask=fontmask,
        transparency=fonttransparency,
    )
    return {
        "result": bala,
        "font": ttf_font,
        "fontsize": goodsize,
        "width": width,
        "height": height,
        "fontmask": fontmask,
        "font_coords": box,
    }


def transparent_rectangle(image, box, color=(255, 255, 255), transparency=0.5):
    image = open_image_in_cv(image)
    img = convert_cv_image_to_4_channels(image)
    shapes = np.zeros_like(img, np.uint8)
    cv2.rectangle(shapes, box[:2], box[2:], color[:3], cv2.FILLED)
    out = img.copy()
    alpha = transparency
    mask = shapes.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, shapes, 1 - alpha, 0)[mask]
    return out


def transparent_circle(
    image,
    center=(300, 300),
    radius=75,
    color=(255, 255, 255),
    transparency=0.5,
    blurborder=10,
    circleborder=20,
):
    image = open_image_in_cv(image)
    img = convert_cv_image_to_4_channels(image)
    shapes = np.zeros_like(img, np.uint8)
    cv2.circle(shapes, center, radius + blurborder + circleborder, color, cv2.FILLED)
    shapes = cv2.blur(shapes, (blurborder, blurborder))
    out = img.copy()
    alpha = transparency
    mask = shapes.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, shapes, 1 - alpha, 0)[mask]
    return out


def put_ttf_font_in_box_at_exact_location_with_exact_size(
    image,
    text,
    coords,
    color=(255, 255, 210),
    font=r"C:\Windows\Fonts\ANTQUAB.TTF",
    maxwidth=300,
    maxheight=100,
    fonttransparency=50,
    boxtransparency=0.2,
    boxcolor=(255, 0, 0),
):
    if fonttransparency > 0:
        color = [x if x < 255 else 254 for x in color]
    xy = coords
    ink = color
    ttf_font, goodsize, width, height, fontmask = get_right_font(
        text, fontpath=font, maxwidth=maxwidth, maxheight=maxheight
    )
    image = open_image_in_cv(image)
    img2 = convert_cv_image_to_4_channels(image)
    fontmask = convert_cv_image_to_4_channels(fontmask)
    boxcolor = reverse_color(boxcolor)
    img = get_image_mask(image=img2, color=ink)
    box = [int(xy[0]), int(xy[1]), int(xy[0] + width), int(xy[1] + height)]
    img2 = transparent_rectangle(img2, box, boxcolor, transparency=boxtransparency)
    bala = paste(
        imgbase=img2,
        img_color=img,
        box=box,
        mask=fontmask,
        transparency=fonttransparency,
    )
    return {
        "result": bala,
        "font": ttf_font,
        "fontsize": goodsize,
        "width": width,
        "height": height,
        "fontmask": fontmask,
        "font_coords": box,
    }


def put_ttf_font_in_circle_at_exact_location_with_exact_size(
    image,
    text,
    coords,
    color=(255, 255, 210),
    font=r"C:\Windows\Fonts\ANTQUAB.TTF",
    maxwidth=300,
    maxheight=100,
    fonttransparency=50,
    circletransparency=0.2,
    circlecolor=(255, 0, 0),
    blurborder=10,
    circleborder=20,
):
    if fonttransparency > 0:
        color = [x if x < 255 else 254 for x in color]
    xy = coords
    ink = color
    ttf_font, goodsize, width, height, fontmask = get_right_font(
        text,
        fontpath=font,
        maxwidth=maxwidth - blurborder - circleborder,
        maxheight=maxheight,
    )
    image = open_image_in_cv(image)
    img2 = convert_cv_image_to_4_channels(image)
    fontmask = convert_cv_image_to_4_channels(fontmask)
    circlecolor = reverse_color(circlecolor)
    img = get_image_mask(image=img2, color=ink)
    box = [int(xy[0]), int(xy[1]), int(xy[0] + width), int(xy[1] + height)]
    img2 = transparent_circle(
        img2,
        center=(int(xy[0] + width / 2), int(xy[1] + height / 2)),
        radius=width // 2,
        color=circlecolor,
        transparency=circletransparency,
        blurborder=blurborder,
        circleborder=circleborder,
    )
    bala = paste(
        imgbase=img2,
        img_color=img,
        box=box,
        mask=fontmask,
        transparency=fonttransparency,
    )
    return {
        "result": bala,
        "font": ttf_font,
        "fontsize": goodsize,
        "width": width,
        "height": height,
        "fontmask": fontmask,
        "font_coords": box,
    }


def put_ttf_font_multiline_in_box_at_exact_location_with_exact_size(
    image,
    textwithnewline,
    coords,
    color=(255, 255, 210),
    font=r"C:\Windows\Fonts\ANTQUAB.TTF",
    maxwidth=300,
    maxheight=100,
    fonttransparency=50,
    boxtransparency=0.2,
    boxcolor=(255, 0, 0),
    boxborder=20,
):
    xy = coords
    ink = color
    allsizeresults = []
    textsplitted = textwithnewline.strip().splitlines()
    for text in textsplitted:
        ttf_font, goodsize, width, height, fontmask = get_right_font(
            text,
            fontpath=font,
            maxwidth=maxwidth - (boxborder * 2),
            maxheight=(maxheight - (boxborder * 2)) // len(textsplitted),
        )
        allsizeresults.append((ttf_font, goodsize, width, height, fontmask))
    allsort = sorted(allsizeresults, key=lambda x: x[1])
    ttf_font, goodsize, width, height, fontmask = allsort[0]
    image = open_image_in_cv(image)
    img2 = convert_cv_image_to_4_channels(image)
    ttf_font = get_font_regular_size(fontpath=font, size=goodsize)
    boxcolor = reverse_color(boxcolor)
    box = xy
    for ini, text in enumerate(textsplitted):
        fontmask = getmask(text, ttf_font)
        fontmask = convert_cv_image_to_4_channels(fontmask)
        img = get_image_mask(image=img2, color=ink)
        box = [
            int(xy[0]),
            int(xy[1] + height * ini),
            int(xy[0] + width),
            int(xy[1] + height * (ini + 1)),
        ]
        if ini == 0:
            boxba = (
                box[0] - boxborder,
                box[1],
                box[2] + boxborder,
                box[3] - 1,
            )  # +boxborder
            img2 = transparent_rectangle(
                img2, boxba, boxcolor, transparency=boxtransparency
            )
        elif ini == len(textsplitted) - 1:
            boxba = box[0] - boxborder, box[1], box[2] + boxborder, box[3] + boxborder
            img2 = transparent_rectangle(
                img2, boxba, boxcolor, transparency=boxtransparency
            )
        else:
            boxba = box[0] - boxborder, box[1], box[2] + boxborder, box[3] - 1
            img2 = transparent_rectangle(
                img2, boxba, boxcolor, transparency=boxtransparency
            )
        img2 = paste(
            imgbase=img2,
            img_color=img,
            box=box,
            mask=fontmask,
            transparency=fonttransparency,
        )
    return {
        "result": img2,
        "font": ttf_font,
        "fontsize": goodsize,
        "width": width,
        "height": height,
        "fontmask": fontmask,
        "font_coords": box,
    }


def put_ttf_font_multiline_at_exact_location_with_exact_size(
    image,
    textwithnewline,
    coords,
    color=(255, 255, 210),
    font=r"C:\Windows\Fonts\ANTQUAB.TTF",
    maxwidth=300,
    maxheight=100,
    fonttransparency=50,
):
    if fonttransparency > 0:
        color = [x if x < 255 else 254 for x in color]
    xy = coords
    textsplitted = textwithnewline.strip().splitlines()
    allsizeresults = []
    for text in textsplitted:
        ttf_font, goodsize, width, height, fontmask = get_right_font(
            text,
            fontpath=font,
            maxwidth=maxwidth,
            maxheight=maxheight // len(textsplitted),
        )
        allsizeresults.append((ttf_font, goodsize, width, height, fontmask))
    allsort = sorted(allsizeresults, key=lambda x: x[1])
    ttf_font, goodsize, width, height, fontmask = allsort[0]
    image = open_image_in_cv(image)
    img2 = convert_cv_image_to_4_channels(image)
    ttf_font = get_font_regular_size(fontpath=font, size=goodsize)
    ink = reverse_color(color)
    box = xy
    for ini, text in enumerate(textsplitted):
        fontmask = getmask(text, ttf_font)
        fontmask = convert_cv_image_to_4_channels(fontmask)
        img = get_image_mask(image=img2, color=ink)
        box = [
            int(xy[0]),
            int(xy[1] + height * ini),
            int(xy[0] + width),
            int(xy[1] + height * (ini + 1)),
        ]
        img2 = paste(
            imgbase=img2,
            img_color=img,
            box=box,
            mask=fontmask,
            transparency=fonttransparency,
        )
    return {
        "result": img2,
        "font": ttf_font,
        "fontsize": goodsize,
        "width": width,
        "height": height,
        "fontmask": fontmask,
        "font_coords": box,
    }


def putTrueTypeText(img, text, org, fontFace, fontScale, color, *args, **kwargs):
    xy = org
    size = fontScale
    ttf_font, size, width, height, fontmask = get_right_font_fix(
        text, fontpath=fontFace, fixedsize=size
    )
    image = open_image_in_cv(img)
    oldshape = image.shape
    img2 = convert_cv_image_to_4_channels(image)

    fontmask = convert_cv_image_to_4_channels(fontmask)
    img = get_image_mask(image=img2, color=color)
    box = [int(xy[0]), int(xy[1] - height), int(xy[0] + width), int(xy[1])]
    bala = paste(imgbase=img2, img_color=img, box=box, mask=fontmask, transparency=-1)
    if len(oldshape) == 2:
        bala = cv2.cvtColor(bala, cv2.COLOR_BGRA2GRAY)
    elif len(oldshape) == 3:
        if oldshape[-1] == 3:
            bala = cv2.cvtColor(bala, cv2.COLOR_BGRA2BGR)
    return bala


def put_ttf_font_multiline_at_exact_center_location_with_exact_size(
    image,
    textwithnewline,
    coords,
    color=(255, 255, 210),
    font=r"C:\Windows\Fonts\ANTQUAB.TTF",
    maxwidth=300,
    maxheight=100,
    fonttransparency=50,
):
    if fonttransparency > 0:
        color = [x if x < 255 else 254 for x in color]
    xy = coords
    textsplitted = textwithnewline.strip().splitlines()
    allsizeresults = []
    for text in textsplitted:
        ttf_font, goodsize, width, height, fontmask = get_right_font(
            text,
            fontpath=font,
            maxwidth=maxwidth,
            maxheight=maxheight // len(textsplitted),
        )
        allsizeresults.append((ttf_font, goodsize, width, height, fontmask))
    allsort = sorted(allsizeresults, key=lambda x: x[1])
    ttf_font, goodsize, width, height, fontmask = allsort[0]
    image = open_image_in_cv(image)
    img2 = convert_cv_image_to_4_channels(image)
    ttf_font = get_font_regular_size(fontpath=font, size=goodsize)
    ink = reverse_color(color)
    xy = xy[0] - width // 2, xy[1] - (height * len(textsplitted)) // 2
    box = xy
    for ini, text in enumerate(textsplitted):
        fontmask = getmask(text, ttf_font)
        fontmask = convert_cv_image_to_4_channels(fontmask)
        img = get_image_mask(image=img2, color=ink)
        box = [
            int(xy[0]),
            int(xy[1] + height * ini),
            int(xy[0] + width),
            int(xy[1] + height * (ini + 1)),
        ]
        img2 = paste(
            imgbase=img2,
            img_color=img,
            box=box,
            mask=fontmask,
            transparency=fonttransparency,
        )
    return {
        "result": img2,
        "font": ttf_font,
        "fontsize": goodsize,
        "width": width,
        "height": height,
        "fontmask": fontmask,
        "font_coords": box,
    }


def put_ttf_font_multiline_in_box_at_exact_center_location_with_exact_size(
    image,
    textwithnewline,
    coords,
    color=(255, 255, 210),
    font=r"C:\Windows\Fonts\ANTQUAB.TTF",
    maxwidth=300,
    maxheight=100,
    fonttransparency=50,
    boxtransparency=0.2,
    boxcolor=(255, 0, 0),
    boxborder=20,
):
    if fonttransparency > 0:
        color = [x if x < 255 else 254 for x in color]
    xy = coords
    ink = color
    allsizeresults = []
    textsplitted = textwithnewline.strip().splitlines()
    for text in textsplitted:
        ttf_font, goodsize, width, height, fontmask = get_right_font(
            text,
            fontpath=font,
            maxwidth=maxwidth - (boxborder * 2),
            maxheight=(maxheight - (boxborder * 2)) // len(textsplitted),
        )
        allsizeresults.append((ttf_font, goodsize, width, height, fontmask))
    allsort = sorted(allsizeresults, key=lambda x: x[1])
    ttf_font, goodsize, width, height, fontmask = allsort[0]
    image = open_image_in_cv(image)
    img2 = convert_cv_image_to_4_channels(image)
    ttf_font = get_font_regular_size(fontpath=font, size=goodsize)
    boxcolor = reverse_color(boxcolor)
    box = xy
    xy = xy[0] - width // 2, xy[1] - (height * len(textsplitted)) // 2

    for ini, text in enumerate(textsplitted):
        fontmask = getmask(text, ttf_font)
        fontmask = convert_cv_image_to_4_channels(fontmask)
        img = get_image_mask(image=img2, color=ink)
        box = [
            int(xy[0]),
            int(xy[1] + height * ini),
            int(xy[0] + width),
            int(xy[1] + height * (ini + 1)),
        ]
        if ini == 0:
            boxba = (
                box[0] - boxborder,
                box[1],
                box[2] + boxborder,
                box[3] - 1,
            )
            img2 = transparent_rectangle(
                img2, boxba, boxcolor, transparency=boxtransparency
            )
        elif ini == len(textsplitted) - 1:
            boxba = box[0] - boxborder, box[1], box[2] + boxborder, box[3] + boxborder
            img2 = transparent_rectangle(
                img2, boxba, boxcolor, transparency=boxtransparency
            )
        else:
            boxba = box[0] - boxborder, box[1], box[2] + boxborder, box[3] - 1
            img2 = transparent_rectangle(
                img2, boxba, boxcolor, transparency=boxtransparency
            )
        img2 = paste(
            imgbase=img2,
            img_color=img,
            box=box,
            mask=fontmask,
            transparency=fonttransparency,
        )
    return {
        "result": img2,
        "font": ttf_font,
        "fontsize": goodsize,
        "width": width,
        "height": height,
        "fontmask": fontmask,
        "font_coords": box,
    }

