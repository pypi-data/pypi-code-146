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
Convert image format

@author: Antonio Bulgheroni
@email: antonio.bulgheroni@ec.europa.eu

"""
import argparse
import sys
from argparse import ArgumentParser
from pathlib import Path

import PIL
from PIL import Image

from autologbook import autoconfig
from labtools.util import convert_image_format, get_image_list_from_directory_list, get_image_list_from_file_list

program_name = 'image-converter'
program_version = 'v0.0.1'
autologbook_version = autoconfig.VERSION

ext_format_dict = Image.registered_extensions()
supported_formats = [
    f for ex, f in Image.registered_extensions().items() if f in Image.OPEN]
format_exts_dict = dict()
for form in sorted(supported_formats):
    exts = [key for key, value in ext_format_dict.items() if value == form]
    format_exts_dict[form] = exts


class FormatNotSupported(Exception):
    pass


def argument_parser() -> ArgumentParser:
    """Return the argument parser object."""
    parser = ArgumentParser(description='''
                                     Tool for converting image formats.
                                     ''')

    parser.add_argument('-f', '--output-format', dest='output_format', action='store', default='png', nargs='?',
                        type=str, help='The output format for the conversion. The default is png. ' ''
                        'Use -l to get a list of supported formats.')

    parser.add_argument('-i', '--input-images', metavar='image_files', type=Path, nargs='*', dest='image_files',
                        help='One or more image files to be converted. Wildcards patterns are also accepted.')

    parser.add_argument('-d', '--input-directory', metavar='image_folders', type=Path, nargs='*', dest='image_folders',
                        help='One or more image folder. All image files will be converted to the output format.')

    parser.add_argument('-r', '--recursive', dest='recursive', action='store_true', default=False,
                        help='Scan each directory recursively. It is used only with the -d / --input-directory option.')

    parser.add_argument('-l', '--list-supported-format', dest='supported_formats', action='store_true', default=False,
                        help='Print the list of supported formats and exit.')

    version_msg = f'{program_name} version is {program_version}.' + '\n' \
                  + f'autologbook package version is {autologbook_version}'
    parser.add_argument('-v', '--version', action='version', version=version_msg,
                        help='Print the software version and exit.')

    return parser


def get_output_format(args: argparse.Namespace) -> str:
    """
    Get the output format.

    This function interprets the argparse namespace and checks if what the user provided is a valid image format.
    It looks among the supported formats and also among the extensions.

    Parameters
    ----------
    args: argparse.Namespace
        The parsed argument namespace

    Returns
    -------
    A string containing the output format.

    """
    # check the if the output format is supported.
    # let's assume the user used the format tag as a start
    # all supperted formats are UPPER case
    if args.output_format.upper() in supported_formats:
        # be sure that the format is stored in upper case
        args.output_format = args.output_format.upper()
    else:
        # maybe the user used the file extensions.
        # all extensions are lower case
        if args.output_format.startswith('.'):
            if args.output_format.lower() in ext_format_dict:
                args.output_format = ext_format_dict[args.output_format].upper(
                )
            else:
                raise FormatNotSupported(f'{args.output_format} is not supported. '
                                         'Use -l to get a list of all supported extensions.')
        else:
            if '.' + args.output_format.lower() in ext_format_dict:
                args.output_format = ext_format_dict['.'
                                                     + args.output_format].upper()
            else:
                raise FormatNotSupported(f'{args.output_format} is not supported. '
                                         'Use -l to get a list of all supported extensions.')
    return args.output_format


def main():
    cli_args = sys.argv[1:]
    parser = argument_parser()
    parser.prog = program_name
    args = parser.parse_args(cli_args)

    if args.supported_formats:
        print(
            f'This is the list of supported formats (total: {len(supported_formats)}) with their file extensions:')
        for form, exts in format_exts_dict.items():
            print(f'{form:<6} -> {", ".join(exts)}')
        return

    if args.image_files is None and args.image_folders is None:
        print('Please select at least one file (-i) or one folder (-d)')
        return

    try:
        output_format = get_output_format(args)

        input_images = list()
        input_images.extend(get_image_list_from_file_list(args.image_files))
        input_images.extend(get_image_list_from_directory_list(
            args.image_folders, args.recursive))

        print(f'Starting the conversion of {len(input_images)} images')
        for image in input_images:
            try:
                output_file_name = image.parent / \
                    Path(image.stem + format_exts_dict[output_format][0])
                convert_image_format(
                    input_img=image, format=output_format, output_img=output_file_name)
            except FileNotFoundError as e:
                print(f'ERROR: Could not find image {image}')
                print(e)
            except PIL.UnidentifiedImageError as e:
                print(f'ERROR: {image} cannot be opened')
                print(e)
            except OSError as e:
                print('ERROR: the output file could not be written.')
                print(e)
            except (ValueError, TypeError) as e:
                print(f'ERROR: converting {image}')
                print(e)
                raise e

    except FormatNotSupported as e:
        print('Output image format not supported')
        print(e)


if __name__ == '__main__':
    main()
