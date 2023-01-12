# Copyright (C) 2020 Majormode.  All rights reserved.
#
# This software is the confidential and proprietary information of
# Majormode or one of its subsidiaries.  You shall not disclose this
# confidential information and shall use it only in accordance with the
# terms of the license agreement or other applicable agreement you
# entered into with Majormode.
#
# MAJORMODE MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY
# OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE, OR NON-INFRINGEMENT.  MAJORMODE SHALL NOT BE LIABLE FOR ANY
# LOSSES OR DAMAGES SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING
# OR DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.

import csv
import logging
import math
import os
import re
from typing import Dict, Any

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import qrcode
import unidecode

from .model import IdCardInfo


CSV_FIELD_NAME_ACCOUNT_ID = 'ID'
CSV_FIELD_NAME_CART_TYPE = 'Card Type'
CSV_FIELD_NAME_CLASS_NAME = 'Class Name'
CSV_FIELD_NAME_FIRST_NAME = 'First Name'
CSV_FIELD_NAME_FULL_NAME = 'Full Name'
CSV_FIELD_NAME_GRADE_LEVEL = 'Grade Level'
CSV_FIELD_NAME_GRADE_NAME = 'Grade Name'
CSV_FIELD_NAME_LAST_NAME = 'Last Name'
CSV_FIELD_NAME_REGISTRATION_FILE_ID = '#'

CSV_FIELD_NAMES = {
    CSV_FIELD_NAME_ACCOUNT_ID: True,
    CSV_FIELD_NAME_CART_TYPE: False,
    CSV_FIELD_NAME_CLASS_NAME: False,
    CSV_FIELD_NAME_FIRST_NAME: False,
    CSV_FIELD_NAME_FULL_NAME: False,
    CSV_FIELD_NAME_GRADE_LEVEL: False,
    CSV_FIELD_NAME_GRADE_NAME: False,
    CSV_FIELD_NAME_LAST_NAME: True,
    CSV_FIELD_NAME_REGISTRATION_FILE_ID: False,
}

DEFAULT_CSV_DELIMITER_CHARACTER = ','
DEFAULT_CSV_ESCAPE_CHARACTER = None
DEFAULT_CSV_QUOTE_CHARACTER = '"'

DEFAULT_FONT_NAME = 'Calibri Bold'
DEFAULT_FONT_SIZE = 56
DEFAULT_FONT_MAXIMAL_SIZE = 70
DEFAULT_FONT_MINIMAL_SIZE = 48

# Default relative path of the folder where the font files are stored in.
DEFAULT_FONT_RELATIVE_PATH = 'fonts'

DEFAULT_ID_CARD_WIDTH = 540
DEFAULT_ID_CARD_HEIGHT = 860
DEFAULT_ID_CARD_RATIO = DEFAULT_ID_CARD_WIDTH / DEFAULT_ID_CARD_HEIGHT
DEFAULT_ID_CARD_MAXIMUM_STANDARD_DEVIANCE = 0.01

DEFAULT_LINE_SPACING = 12

REGEX_PATTERN_ID_CARD_FIELD_NAME = r'{([a-z\s#]+)}'
REGEX_PATTERN_ID_CARD_FILE_NAME_FORMAT = '{}(_{})*'.format(
    REGEX_PATTERN_ID_CARD_FIELD_NAME,
    REGEX_PATTERN_ID_CARD_FIELD_NAME)

REGEX_ID_CARD_FIELD_NAME = re.compile(REGEX_PATTERN_ID_CARD_FIELD_NAME)
REGEX_ID_CARD_FILE_NAME_FORMAT = re.compile(REGEX_PATTERN_ID_CARD_FILE_NAME_FORMAT)


def __build_card_image_default_file_name(id_card):
    file_name = '-'.join(unidecode.unidecode(id_card.full_name.lower()).split())

    if id_card.class_name:
        class_name = '-'.join(unidecode.unidecode(id_card.class_name.lower()).split())
        file_name = f'{class_name}_{file_name}'
    elif id_card.grade_name:
        file_name = f'{id_card.grade_name.lower()}_{file_name}'

    if id_card.grade_level is not None:
        file_name = f'{id_card.grade_level}_{file_name}'

    if id_card.registration_id:
        file_name = f'{file_name}_{id_card.registration_id}'

    return file_name


def __build_card_image_formatted_file_name(id_card, file_name_format):
    field_names = __validate_id_card_file_name_format(file_name_format)

    field_name_attribute_mapping = {
        CSV_FIELD_NAME_ACCOUNT_ID.lower(): id_card.account_id,
        CSV_FIELD_NAME_CART_TYPE.lower(): id_card.card_type,
        CSV_FIELD_NAME_CLASS_NAME.lower(): id_card.class_name,
        CSV_FIELD_NAME_FIRST_NAME.lower(): id_card.first_name,
        CSV_FIELD_NAME_FULL_NAME.lower(): id_card.full_name,
        CSV_FIELD_NAME_GRADE_LEVEL.lower(): id_card.grade_level,
        CSV_FIELD_NAME_GRADE_NAME.lower(): id_card.grade_name,
        CSV_FIELD_NAME_LAST_NAME.lower(): id_card.last_name,
        CSV_FIELD_NAME_REGISTRATION_FILE_ID.lower(): id_card.registration_id,
    }

    file_name = '_'.join([
        str(field_name_attribute_mapping[field_name])
        for field_name in field_names
    ])

    return file_name


def __validate_id_card_file_name_format(file_name_format):
    """
    Validate the format of a ID card file name.

    A ID card file name format MUST be composed of field names to build
    this file name with.  These field names MUST be defined in parentheses,
    each field names separated with a character underscore.

    For example:

        {id}_{first name}_{grade level}


    @param file_name_format: A string corresponding to the format of an ID
        card file.


    @return: A list of strings corresponding to the names of the fields to
        build the ID card file name with.


    @raise ValueError: If the file name format is not valid.
    """
    if not REGEX_ID_CARD_FILE_NAME_FORMAT.match(file_name_format):
        raise ValueError("Invalid ID card file name format")

    valid_field_names = [
        field_name.lower()
        for field_name in CSV_FIELD_NAMES.keys()
    ]

    field_names = REGEX_ID_CARD_FIELD_NAME.findall(file_name_format)
    for field_name in field_names:
        if field_name not in valid_field_names:
            raise ValueError(f'Invalid field "{field_name}" in ID card file name format')

    return field_names


def build_card_image_file_name(id_card: IdCardInfo, file_name_format=None):
    """
    Build the name of the ID card's image file.


    @param id_card: An object `IdCardInfo`.

    @param file_name_format: Specify the format of ID card file name.


    @return: The file name of the ID card.
    """
    return __build_card_image_default_file_name(id_card) if not file_name_format \
        else __build_card_image_formatted_file_name(id_card, file_name_format)


def calculate_card_image_size(size: str or (int, int)) -> (int, int):
    """
    Return the image size of an ID card.


    @param size: The desired size of the ID card image.  The specified
        width and height MUST correspond to the ratio of a CR80 standard
        credit card size ID-1 in portrait mode (54mm x 85.6mm).

        This argument is either a tuple of two integers `(width, height)`
        or a string representation of two integers separated with the
        character `x`.  For examples: `(540, 860)` or  `'540x860'`.

        One of the two dimensions, either the width or the height, can be
        omitted.  For examples: `(540, None)` or  `'540x'`; `(None, 860)`
        or `'x860'`.

        The function automatically calculates the value of the missing
        dimension.


    @return: A tuple `(width, height)` of ID card images.


    @raise ValueError: if the argument `size_str` doesn't correspond to 2
        numbers separated with the character `x`.
    """
    if isinstance(size, str):
        size = size.split('x')
        if len(size) != 2:
            raise ValueError('Invalid image size specification')

    card_image_width, card_image_height = size

    if card_image_width and card_image_height:
        card_image_width = int(card_image_width)
        card_image_height = int(card_image_height)
        if calculate_relative_difference(
                card_image_width / card_image_height,
                DEFAULT_ID_CARD_RATIO) > DEFAULT_ID_CARD_MAXIMUM_STANDARD_DEVIANCE:
            raise ValueError('invalid ID card image size ratio')
    else:
        if card_image_width is None and card_image_height is None:
            raise ValueError('invalid ID card image size specification')

        if card_image_width:
            card_image_width = int(card_image_width)
            card_image_height = math.ceil(card_image_width / DEFAULT_ID_CARD_RATIO)
        else:
            card_image_height = int(card_image_height)
            card_image_width = math.ceil(card_image_height * DEFAULT_ID_CARD_RATIO)

    return card_image_width, card_image_height


def calculate_full_name_optimal_font_size(
        full_name,
        text_area_width,
        font_file_path_name,
        first_name=None,
        last_name=None,
        maximal_font_size=DEFAULT_FONT_MINIMAL_SIZE,
        minimal_font_size=DEFAULT_FONT_MAXIMAL_SIZE):
    """
    Calculate the optimal font size to display the full name in the
    specified text area.

    If the text area is too small to write the full name with the minimal
    size of the font, the function calculates the largest size of the font
    that can be used to display the first name and the last name in two
    separated lines.


    @param full_name: A full name of the person.

    @param text_area_width: The width in pixels of the area to display the
        full name.

    @param font_file_path_name: The absolute path and name of the font
        file to use to display the full name.

    @param first_name: The first name of the person.

    @param last_name: The last name of the person.

    @param maximal_font_size: The maximal size of the font to use to
        display the full name.

    @param minimal_font_size: THe minimal size of the font to use to
        display the full name.


    @return: A tuple `(font_size, text_width, text_height, multiline_required)`
        where:

        - `font_size`: The largest font size to display the text in the
          specified area.

        - `text_width`: The width in pixels of the text displayed with this
          font size.

        - `text_height`: The height in pixels of the text displayed with this
          font size.

        - `multiline_required`: `False` if the full name can be displayed on 1
          single line; `True` if the full name MUST be displayed as the first
          name and the last name on 2 separated lines.
    """
    if not full_name:
        raise ValueError("MUST specify a valid value for argument 'full_name'")

    if text_area_width is None or text_area_width <= 0:
        raise ValueError("MUST specify a valid value for argument 'text_area_width'")

    if minimal_font_size is None or minimal_font_size <= 0:
        raise ValueError("MUST specify a valid value for argument 'minimal_font_size'")

    if maximal_font_size is None or maximal_font_size <= 0:
        raise ValueError("MUST specify a valid value for argument 'maximal_font_size'")

    if minimal_font_size > maximal_font_size:
        raise ValueError("Argument 'minimal_font_size' MUST be lowest than 'maximal_font_size'")

    multiline_required = False
    best_font_size, best_text_width, best_text_height = calculate_text_optimal_font_size(
        full_name,
        text_area_width,
        font_file_path_name)

    if best_text_width > text_area_width:
        if not first_name or not last_name \
           or len(first_name) >= len(full_name) \
           or len(last_name) >= len(full_name):
            raise ValueError("the size of the font is too small compared to the requirement")

        best_first_name_font_size, best_first_name_text_width, best_first_name_text_height = \
            calculate_text_optimal_font_size(first_name, text_area_width, font_file_path_name)

        best_last_name_font_size, best_last_name_text_width, best_last_name_text_height = \
            calculate_text_optimal_font_size(last_name, text_area_width, font_file_path_name)

        multiline_required = True
        if best_first_name_font_size < best_last_name_font_size:
            best_font_size, best_text_width, best_text_height = \
                best_first_name_font_size, best_first_name_text_width, best_first_name_text_height
        else:
            best_font_size, best_text_width, best_text_height = \
                best_last_name_font_size, best_last_name_text_width, best_last_name_text_height

    return best_font_size, best_text_width, best_text_height, multiline_required


def calculate_relative_difference(i, j):
    """
    Calculate the relative difference between two numbers.

    The function takes the absolute difference divided by the absolute
    value of their arithmetic mean.


    @param i: A number.

    @param j: Another number.


    @return: A float representing the relative difference (a ratio) between
        the two numbers passed to this function.
    """
    return 0 if i + j == 0 else abs(i - j) / abs(i + j) * 2


def calculate_text_optimal_font_size(
        text,
        text_area_width,
        font_file_path_name,
        font_maximal_size=DEFAULT_FONT_MAXIMAL_SIZE,
        font_minimal_size=DEFAULT_FONT_MINIMAL_SIZE,
        font_size=DEFAULT_FONT_SIZE):
    """
    Return the optimal font size to display the specified text in the
    given text area.


    @param text: A string to be displayed in one line only.

    @param text_area_width: The width of the area to display the text.

    @param font_file_path_name: The absolute path and name of the font
        file.

    @param font_minimal_size: Minimal acceptable size of the font to
        display the text.

    @param font_maximal_size: Maximal acceptable size of the font to
        display the text.

    @param font_size: The default font size to use.  This size will be
        adjusted to display the text in the largest possible font size.


    @return: A tuple `(font_size, text_width, text_height)` where:

        * `font_size`: The largest font size to display the text in the
          specified area.

        * `text_width`: The width in pixels of the text displayed with this
          font size.

        * `text_height`: The height in pixels of the text displayed with this
          font size.
    """
    if not text:
        raise ValueError("MUST specify a valid value for argument 'text'")

    if font_size is None or font_size <= 0:
        raise ValueError("MUST specify a valid value for argument 'font_size'")

    if text_area_width <= 0:
        raise ValueError("MUST specify a valid value for argument 'text_area_width'")

    font = ImageFont.truetype(font_file_path_name, font_size)
    text_width, text_height = font.getsize(text)

    if text_width > text_area_width:
        best_font_size, best_text_width, best_text_height = font_size, text_width, text_height

        while font_size > font_minimal_size:
            font_size -= 1
            font = ImageFont.truetype(font_file_path_name, font_size)
            text_width, text_height = font.getsize(text)
            if text_width <= text_area_width:
                break
            best_font_size, best_text_width, best_text_height = font_size, text_width, text_height

    else:
        best_font_size, best_text_width, best_text_height = font_size, text_width, text_height

        while font_size < font_maximal_size:
            font_size += 1
            font = ImageFont.truetype(font_file_path_name, font_size)
            text_width, text_height = font.getsize(text)
            if text_width >= text_area_width:
                break
            best_font_size, best_text_width, best_text_height = font_size, text_width, text_height

    return best_font_size, best_text_width, best_text_height


def generate_id_card_image(
        id_card: IdCardInfo,
        card_image_size,
        header_image,
        font_name,
        font_path=None,
        padding=20):
    """
    Generate the image of a ID card.


    @param id_card: An object `IdCardInfo`.

    @param card_image_size: A tuple `(width, height)` corresponding to the
        dimensions of the card's image to generate.

    @param header_image: An object `PIL.Image` of the header image to
        display at topmost position of the card' image.

    @param font_name: Name of the font to use to write the full name (or
        first and last names) on the card's image.

    @param font_path: Absolute path of the directory where the font files
        are stored in.

    @param padding: Space in pixels to generate around the card's image.


    @return: An object `PIL.Image` of the ID card.
    """
    logging.debug(f"Generating the image of ID card for {id_card.full_name}...")

    # Determine the size of the card image based on the given specification.
    # Create a new object `PIL.Image` with a white background.
    id_card_image = Image.new('RGB', card_image_size, color='white')
    card_image_width, card_image_height = card_image_size

    # Calculate the size of the card's view based on the required padding.
    card_view_width, card_view_height = card_image_width - padding * 2, card_image_height - padding * 2

    # Resize the header image to fit the header view of the ID card, and
    # align and display the resized image to this view.
    header_view_width = card_view_width
    header_view_height = math.ceil((card_image_height - card_view_width - padding * 2) / 2)
    scaled_header_image = scale_header_image(header_image, (header_view_width, header_view_height))

    scaled_header_image_width, scaled_header_image_height = scaled_header_image.size
    x = math.ceil((header_view_width - scaled_header_image_width) / 2)
    y = math.ceil((header_view_height - scaled_header_image_height) / 2)
    id_card_image.paste(scaled_header_image, (padding + x, padding + y))

    # Generate the value of the QR code of the ID card and display the image
    # of this QR code at the center of the card.
    qrcode_generator = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=10,
        border=4,
    )

    qrcode_value = f"{str(id_card.card_type)}.{str(id_card.account_id).replace('-', '')}"
    qrcode_generator.add_data(qrcode_value)
    qrcode_generator.make(fit=True)
    qrcode_image = qrcode_generator \
        .make_image(fill_color="black", back_color="white") \
        .resize((card_view_width, card_view_width))

    x = padding
    y = math.ceil((card_image_height - card_view_width) / 2)
    id_card_image.paste(qrcode_image, (x, y))

    # Calculate the optimal font size to display the full name (or the first
    # name and the last name on two separated lines) of the ID card.
    text_area_width = card_view_width

    if font_path is None:
        font_path = os.path.join(os.path.dirname(__file__), DEFAULT_FONT_RELATIVE_PATH)
    font_file_path_name = os.path.join(font_path, f'{font_name}.ttf')

    font_size, text_width, text_height, multiline_required = \
        calculate_full_name_optimal_font_size(
            id_card.full_name,
            text_area_width,
            font_file_path_name,
            first_name=id_card.first_name,
            last_name=id_card.last_name,
            maximal_font_size=DEFAULT_FONT_MAXIMAL_SIZE,
            minimal_font_size=DEFAULT_FONT_MINIMAL_SIZE)

    font = ImageFont.truetype(font_file_path_name, font_size)
    image_draw = ImageDraw.Draw(id_card_image)

    y = card_image_height - header_view_height - padding

    if multiline_required:
        x = math.ceil((text_area_width - font.getsize(id_card.first_name)[0]) / 2) + padding
        image_draw.text((x, y), id_card.first_name, font=font, fill='black')

        x = math.ceil((text_area_width - font.getsize(id_card.last_name)[0]) / 2) + padding
        image_draw.text((x, y + DEFAULT_LINE_SPACING + text_height), id_card.last_name, font=font, fill='black')

    else:
        x = math.ceil((text_area_width - text_width) / 2) + padding
        image_draw.text((x, y), id_card.full_name, font=font, fill='black')

    return id_card_image

#
# def get_project_root_dir():
#     """
#     Returns the name of the project root directory.
#
#
#     @return: Project root directory name.
#     """
#     import inspect
#     from pathlib import Path
#
#     # stack trace history related to the call of this function
#     frame_stack = inspect.stack()
#
#     # get info about the module that has invoked this function
#     # (index=0 is always this very module, index=1 is fine as long this function is not called by some other
#     # function in this module)
#     frame_info = frame_stack[1]
#
#     # if there are multiple calls in the stacktrace of this very module, we have to skip those and take the first
#     # one which comes from another module
#     if frame_info.filename == __file__:
#         for frame in frame_stack:
#             if frame.filename != __file__:
#                 frame_info = frame
#                 break
#
#     # path of the module that has invoked this function
#     caller_path = frame_info.filename
#
#     # absolute path of the of the module that has invoked this function
#     caller_absolute_path = os.path.abspath(caller_path)
#
#     # get the top most directory path which contains the invoker module
#     paths = [p for p in sys.path if p in caller_absolute_path]
#     paths.sort(key=lambda p: len(p))
#     caller_root_path = paths[0]
#
#     if not os.path.isabs(caller_path):
#         # file name of the invoker module (eg: "mymodule.py")
#         caller_module_name = Path(caller_path).name
#
#         # this piece represents a subpath in the project directory
#         # (eg. if the root folder is "myproject" and this function has ben called from myproject/foo/bar/mymodule.py
#         # this will be "foo/bar")
#         project_related_folders = caller_path.replace(os.sep + caller_module_name, '')
#
#         # fix root path by removing the undesired subpath
#         caller_root_path = caller_root_path.replace(project_related_folders, '')
#
#     dir_name = Path(caller_root_path).name
#
#     return dir_name


def read_id_cards_info_csv_file(
        csv_file_path_name,
        card_type=None,
        delimiter_character=DEFAULT_CSV_DELIMITER_CHARACTER,
        escape_character=DEFAULT_CSV_ESCAPE_CHARACTER,
        quote_character=DEFAULT_CSV_QUOTE_CHARACTER):
    """
    Read a Comma-Separated Value (CSV) file containing the information of
    a list of ID cards.


    @param csv_file_path_name: Absolute path and name of the CSV file.

    @param card_type: An item of the enumeration `IdCardInfo.CARD_TYPE` to
        specify the type of card this CVS file corresponds to.  If not
        this argument is not passed to the function, the CSV file MUST
        contain a header field `CARD_TYPE`.

    @param delimiter_character: Specify the character used to separate
        each field of the CSV file.

    @param escape_character: Specify the character used to surround fields
        that contain the delimiter character.

    @param quote_character: Specify the character used to escape the
        delimiter character, in case quotes aren't used.


    @return: A list of object `IdCardInfo`.


    @raise ValueError: If an argument has an invalid value or if the CSV
        file is missing a required field.
    """
    # if not delimiter_character:
    #     raise ValueError("MUST specify a valid value for argument 'delimiter_character'")
    #
    # if not escape_character:
    #     raise ValueError("MUST specify a valid value for argument 'escape_character'")
    #
    # if not quote_character:
    #     raise ValueError("MUST specify a valid value for argument 'quote_character'")

    with open(csv_file_path_name, 'rt') as fd:
        reader = csv.DictReader(
            fd,
            delimiter=delimiter_character,
            escapechar=escape_character,
            quotechar=quote_character)

        for field_name, is_required in CSV_FIELD_NAMES.items():
            try:
                reader.fieldnames.index(field_name)
            except ValueError:
                if is_required:
                    raise ValueError(f'the CSV file is missing the field "{field_name}"')

        id_cards = [
            IdCardInfo(
                row.get(CSV_FIELD_NAME_CART_TYPE) or card_type,
                row[CSV_FIELD_NAME_ACCOUNT_ID],
                row[CSV_FIELD_NAME_FULL_NAME],
                class_name=row.get(CSV_FIELD_NAME_CLASS_NAME),
                first_name=row.get(CSV_FIELD_NAME_FIRST_NAME),
                grade_level=row.get(CSV_FIELD_NAME_GRADE_LEVEL),
                grade_name=row.get(CSV_FIELD_NAME_GRADE_NAME),
                last_name=row.get(CSV_FIELD_NAME_LAST_NAME),
                registration_id=row.get(CSV_FIELD_NAME_REGISTRATION_FILE_ID)
            )
            for row in reader
        ]

        return id_cards


def scale_header_image(header_image, view_size, copy_required=False):
    """
    Scale the header image to best fit the view's content.

    @param header_image: An object `PIL.Image`.

    @param view_size: A tuple `(width, height)` of the view to display the
        header image in.

    @param copy_required: Indicate whether the function can resize the
        header image in place, modifying the object `header_image` passed
        to the function, or whether to create a copy of this object and
        resize this new object.


    @return: An object `PIL.Image` corresponding to the resized version of
        the header image.
    """
    scaled_header_image = header_image.copy() if copy_required else header_image
    scaled_header_image.thumbnail(view_size)
    return scaled_header_image


