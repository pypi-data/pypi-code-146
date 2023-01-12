# -*- coding: utf-8 -*-

#  Copyright (c) 2022.  Antonio Bulgheroni.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
#  documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
#  permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
#  Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
#  WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
#  OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
#   documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
#   rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
#   permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#
#
#
#
#
#
#
"""
Set of Utilities for the labtools module.

@author: Antonio Bulgheroni
@email: antonio.bulgheroni@ec.europa.eu

"""
from pathlib import Path

from PIL import Image


def get_image_list_from_file_list(input_selection: list[Path | str]) -> list[Path]:
    supported_extensions = {
        ex for ex, f in Image.registered_extensions().items() if f in Image.OPEN}

    image_list = list()

    if input_selection is None:
        return image_list

    for file in get_file_list(input_selection):
        if not isinstance(file, Path):
            file = Path(file)
        if file.suffix in supported_extensions:
            image_list.append(file)

    return image_list


def get_image_list_from_directory_list(input_selection: list[Path], recursive: bool) -> list[Path]:

    supported_extensions = {
        ex for ex, f in Image.registered_extensions().items() if f in Image.OPEN}
    image_list = list()

    if input_selection is None:
        return image_list

    if recursive:
        pattern = '**/*'
    else:
        pattern = '*'
    for dir in input_selection:
        if dir.is_dir():
            for file in dir.glob(pattern):
                if file.suffix in supported_extensions:
                    image_list.append(file)
    return image_list


def get_file_list(input_selection: list) -> list:
    """
    Return a list of files starting from a CLI arguments

    Parameters
    ----------
    input_selection:
        list from the CLI parsed argument.

    Returns
    -------
    list of Path

    """
    image_list = []
    for image_path in input_selection:

        if not isinstance(image_path, Path):
            image_path = Path(image_path)

        # each entry can be:
        # Case 1. a directory. Just skip it
        # Case 2. not a file nor a dir, then it is very likely a pattern

        if image_path.is_dir():
            print(f'Problems with {image_path}')
            print(
                'Only file names or patterns can be processed. Directories are not accepted.')
        elif image_path.is_file():
            image_list.append(image_path)
        elif not image_path.is_dir() and not image_path.is_file():
            # it is very likely a pattern
            pattern = image_path.name
            folder = image_path.parent
            image_list.extend(list(folder.glob(pattern)))
    return image_list


def convert_image_format(input_img: Path | str, format: str, output_img: Path | str | None = None):
    """
    Convert the format of an image.

    This function is taking an input image in a format and converting it into a specified format.
    The path of the converted image is returned.

    Parameters
    ----------
    input_img: Path | str
        The path of the input image to be converted.

    format: str
        The output format.

    output_img: Path | str | None
        The path of the converted image. If None, the filename of the input image will be modified using the default
        suffix of the desired output format.

    """
    if isinstance(input_img, str):
        input_img = Path(input_img)

    if output_img is None:
        output_img = input_img.parent / Path(input_img.stem + '.' + format)

    with Image.open(input_img) as orig_img:
        if format == 'JPEG' and orig_img.mode == 'P':
            orig_img = orig_img.convert('RGB')
            print('QQQQ')
        if orig_img.format != format:
            print(
                f'Converting {input_img} from {orig_img.format} to {format}.')
            orig_img.save(output_img)
        else:
            print(
                f'Image {input_img} is already in the target format {format}.')
