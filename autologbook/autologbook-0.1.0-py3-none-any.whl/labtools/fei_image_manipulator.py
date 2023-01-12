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
Manipulate FEI images.

@author: Antonio Bulgheroni
@email: antonio.bulgheroni@ec.europa.eu

"""
from __future__ import annotations

import argparse
import datetime
import shutil
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any

from PIL import Image

from autologbook import autoconfig
from autologbook.autoerror import NotFEIMicroscopePicture
from autologbook.autoprotocol import FEIPicture
from autologbook.autotools import FEITagCodes
from labtools.util import get_file_list

program_name = 'fei-image-manipulator'
program_version = 'v0.0.1'
autologbook_version = autoconfig.VERSION


class ImageType:
    """Helper class to store information about image checking."""

    def __init__(self, filename: Path | str, is_fei: bool, fei_subtype: FEITagCodes | None = None,
                 fei_metadata: Any = None):
        self.filename = filename
        self.is_fei = is_fei
        self.fei_subtype = fei_subtype
        self.fei_metadata = fei_metadata


def argument_parser() -> ArgumentParser:
    """
    Return the argument parser object.
    """
    parser = ArgumentParser(description='Tool for the manipulation of FEI microscope TIFF images.',
                            prog=program_name)

    # global parameters and options.
    parser.add_argument('-v', '--version', action='version',
                        version=(f'{program_name} is {program_version}. - '
                                 f'autologbook package is version {autologbook_version}.'),
                        help='Print the version number and exit.')

    subparsers = parser.add_subparsers(title='Commands',
                                       description='This tool comes with a variety of commands to '
                                                   'allow different operations to be performed.',
                                       help='Here below is a list of available commands.',
                                       dest='command_name')

    # command check
    check_parser = subparsers.add_parser(
        'check', help='Check whether an input image is a valid FEI image.')
    check_parser.add_argument('images', metavar='image_files', type=Path, nargs='+',
                              help='One or more image files to check whether they are valid FEI images.'
                                   ' Provide a pattern using * and ? wildcards'
                                   ' to select many images at once.')
    check_parser.add_argument('-o', '--output-file', action='store', default=None, dest='output_file',
                              help=('If an output filename is provided, '
                                    'the output of this command is also saved in a text file'))
    check_parser.add_argument('-s', '--silent', action='store_true', default=False, dest='silent',
                              help=('If selected, the program will run silently. '
                                    'If an output file is not specified, no output will be produced.'))
    check_parser.add_argument('-H', '--human-readable', action='store_true', default=False,
                              help='Set this option to have an output that is human readable.'
                                   + 'The default is a tab separated file that can be easily parsed by MS Excel.')
    check_parser.set_defaults(func=do_check)

    # command metadata
    metadata_parser = subparsers.add_parser(
        'metadata', help='Display FEI specific metadata.')
    metadata_parser.add_argument('images', metavar='image_files', type=Path, nargs='+',
                                 help='One or more image files to extract FEI metadata.'
                                      ' Provide a pattern using * and ? wildcards'
                                      ' to select many images at once.')
    metadata_parser.add_argument('-o', '--output-file', action='store_true', dest='dump_to_file', default=False,
                                 help='Instead of displaying the metadata on the standard out, '
                                      'all the information will be'
                                      ' written as text in the output file. '
                                      'The output file name will be the same as the input, '
                                      'but with a txt suffix.')
    metadata_parser.set_defaults(func=do_metadata)

    calibrate_parser = subparsers.add_parser('calibrate',
                                             help='Calibrate FEI images using information in the FEI tags.')
    calibrate_parser.add_argument('images', metavar='image_files', type=Path, nargs='+',
                                  help='One or more image files to calibrate.'
                                       ' Provide a pattern using * and ? wildcards'
                                       ' to select many images at once.')
    calibrate_parser.add_argument('-r', '--rename', action='store_true', default=False, dest='rename',
                                  help='If set, the calibrated image instead of being overwritten to the original one'
                                       ' will be saved in a separate file with the '
                                       'filename pattern: original_name_calib.tiff')
    calibrate_parser.set_defaults(func=do_calibrate)

    databar_removal_parser = subparsers.add_parser('databar',
                                                   help='Remove the data bar from FEI images.')
    databar_removal_parser.add_argument('images', metavar='image_files', type=Path, nargs='+',
                                        help='One or more image files to remove databar.'
                                        ' Provide a pattern using * and ? wildcards'
                                        ' to select many images at once.')
    databar_removal_parser.add_argument('-o', '--overwrite', action='store_true', default=False, dest='overwrite',
                                        help='If set, the image file without databar will be overwritten on the original one')
    databar_removal_parser.set_defaults(func=do_databar_removal)

    return parser


def get_image_type(file: Path) -> ImageType:
    """
    Return the image type

    Parameters
    ----------
    file: Path
        The filename of the TIFF image.

    Returns
    -------
    ImageType
        The type of the TIFF image
    """

    is_fei = True
    fei_subtype = None
    with Image.open(file) as image:
        metadata = image.getexif()
        for tag in FEITagCodes:
            if tag.value in metadata:
                is_fei = True
                fei_subtype = tag
                fei_metadata = metadata.get(tag)
                break
    return ImageType(file, is_fei, fei_subtype, fei_metadata)


def do_databar_removal(args: argparse.Namespace):
    file_list = get_file_list(args.images)
    for file_in in file_list:
        if args.overwrite:
            file_out = file_in
        else:
            file_out = file_in.parent / \
                Path(file_in.stem + '_no_databar' + file_in.suffix)
        try:
            mp = FEIPicture(file_in, png_generation=False)
            mp._remove_databar(file_in, file_out)
            print(f'Databar removed from {file_out}')
        except NotFEIMicroscopePicture:
            print(f'{file_out} is not a FEI image.')


def do_calibrate(args: argparse.Namespace):
    """
    Perform FEI image calibration.

    This function is documented in the autologbook.autoprotocol.FEIPicture.calibrate

    Parameters
    ----------
    args: argparse.Namespace
        The parsed CLI arguments namespace

    """
    file_list = get_file_list(args.images)

    for file_in in file_list:
        if args.rename:
            file_out = file_in.parent / \
                Path(file_in.stem + '_calib' + file_in.suffix)
            shutil.copy(file_in, file_out)
        else:
            file_out = file_in
        try:
            mp = FEIPicture(file_out, png_generation=False)
            mp.calibrate()
            print(f'Calibrated image {file_out}')
        except NotFEIMicroscopePicture:
            print(f'{file_out} is not a FEI image.')


def do_metadata(args: argparse.Namespace):
    """
    Execute the metadata command.

    Parameters
    ----------
    args: argparse.Namespace
        The CLI arguments.
    """
    file_list = get_file_list(args.images)
    for file in file_list:
        output_string = f'# Output of {program_name} {args.command_name} ({program_version}) ' \
                        f'generated on {datetime.datetime.now():%Y%m%d:%H%M%S}' + \
            '\n\n'
        output_string += f'# Input file: {file}' + '\n\n'
        output_string += metadata_prepare_output(get_image_type(file))
        print(output_string)
        if args.dump_to_file:
            txt_file = file.parent / Path(file.stem + '.txt')
            with open(txt_file, 'wt') as txt:
                txt.write(output_string)


def metadata_prepare_output(output_element: ImageType) -> str:
    """
    Prepare the output of the metadata command.

    Parameters
    ----------
    output_element: ImageType
        The element of which the output should be generated.

    Returns
    -------

    """
    if not output_element.is_fei:
        return f'{output_element.filename} has no FEI metadata' + '\n'

    return output_element.fei_metadata


def do_check(args: argparse.Namespace):
    """
    Perform the check about FEI image type.

    Parameters
    ----------
    args: argparse.Namespace
        The argparse namespace

    """
    file_list = get_file_list(args.images)
    output_image_list = []
    for file in file_list:
        output_image_list.append(get_image_type(file))

    output_string = check_prepare_output(args, output_image_list)

    if not args.silent:
        print(output_string)
    if args.output_file:
        with open(args.output_file, 'wt') as txt:
            txt.write(output_string)


def check_prepare_output(args: argparse.Namespace, output_elements: list[ImageType]) -> str:
    """
    Prepare the output string for the check command.

    Parameters
    ----------
    args: argparse.Namespace
        The namespace resulting from the argument parsing.

    output_elements: list[ImageType]
        The list of element for which an output must be generated.

    Returns
    -------
    output_string: str
        The text to be either printed on the std-out or dumped to file.
        The string is formatted for humans or for pc depending on the option selected on the CLI.

    """

    intro = f'Output of {program_name} {args.command_name} ({program_version}) ' \
            f'generated on {datetime.datetime.now():%Y%m%d:%H%M%S}'
    if args.human_readable:
        output_string = (
            intro + '\n\n' 'Filename \t is_fei \t fei_subtype \n\n')
        for element in output_elements:
            if element.is_fei:
                output_string += '{} is FEI compliant of subtype {} \n'.format(element.filename,
                                                                               element.fei_subtype.name)
            else:
                output_string += '{} is **NOT** FEI compliant\n'.format(
                    element.filename)
    else:
        output_string = (
            '# ' + intro + '\n#\n' '# Filename \t is_fei \t fei_subtype \n#\n')
        for element in output_elements:
            output_string += '{} \t {} \t {} \n'.format(
                element.filename, element.is_fei, element.fei_subtype.name)
    return output_string


def main():
    """The main function"""
    cli_args = sys.argv[1:]
    parser = argument_parser()
    args = parser.parse_args(cli_args)
    args.func(args)


if __name__ == '__main__':
    main()
