# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 10:55:00

@author: Antonio Bulgheroni (antonio.bulgheroni@ec.europa.eu)

Executable script to show or dump images metadata

"""

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
import sys
from argparse import ArgumentParser
from pathlib import Path

from PIL import ExifTags, Image

from autologbook import autoconfig
from labtools.util import get_file_list

program_name = 'metadata-reader'
program_version = 'v0.0.1'
autologbook_version = autoconfig.VERSION


def argument_parser() -> ArgumentParser:
    """
    Return the argument parser object.
    """
    parser = ArgumentParser(description='''
                                     Tool for displaying the metadata of one or more image.
                                     ''')
    parser.add_argument('images', metavar='image_files', type=Path, nargs='*',
                        help='One or more image files to show their metadata. Provide a pattern using * and ? wildcards'
                             ' to select many images at once.')

    parser.add_argument('-o', '--output-file', action='store_true', dest='dump_to_file', default=False,
                        help='Instead of displaying the metadata on the standard out, all the information will be'
                             ' written as text in the output file. The output file name will be the same as the input, '
                             'but with a txt suffix.')
    version_msg = f'{program_name} version is {program_version}.' + '\n' \
                  + f'autologbook package version is {autologbook_version}'
    parser.add_argument('-v', '--version', action='version', version=version_msg,
                        help='Print the software version and exit.')

    return parser


def main():
    """
    The main function of the script.
    """
    cli_args = sys.argv[1:]

    parser = argument_parser()
    parser.prog = program_name

    args = parser.parse_args(cli_args)

    if len(args.images) == 0:
        print('Please specify at least one image')

    image_list = get_file_list(args.images)
    output_file = None

    for image in image_list:
        if args.dump_to_file:
            output_file = open(image.parent / Path(image.stem + '.txt'), 'wt')
        msg = f'| Processing image: {image} |'
        double_line = ''.join(['='] * len(msg))
        single_list = ''.join(['-'] * len(msg))
        print(double_line)
        print(msg)
        print(single_list)

        special_tags = []
        output_content = ''
        try:
            with Image.open(image) as source_img:
                exif = source_img.getexif()
                exif_dict = {}
                for k, v in exif.items():
                    if k in ExifTags.TAGS:
                        exif_dict[ExifTags.TAGS[k]] = v
                    else:
                        special_tags.append(k)

                print('Standard EXIF data:')
                print('')
                for k, v in exif_dict.items():
                    output_content += f'{k}: {v}\n'

                if len(special_tags):
                    for tag in special_tags:
                        output_content += f'\nExtra tag: {tag}\n\n'
                        for line in str(exif[tag]).splitlines(keepends=False):
                            output_content += line + '\n'

                print(output_content)

        except Exception as e:
            print(f'| Error opening file {image} |')
            if args.dump_to_file:
                output_file.close()
            raise e

        print(double_line)
        if args.dump_to_file:
            output_file.write(output_content)
            output_file.close()


if __name__ == '__main__':
    main()
