#!/usr/bin/env python

import argparse
from .formats import FORMATS

ENCODINGS = ['utf_8', 'iso8859_1', 'mac_roman']
formats_listed = list(FORMATS.keys())

def main():

    # Parser
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    description = f"""{parser.prog} shifts the timecodes of a subtitle file
    by a given amount to synchronize it to a video stream.""".replace('\n',' ')
    parser.description = description
    parser.add_argument('input',
                        type=str, 
                        help='path to the input file')
    parser.add_argument('shift',
                        type=float,
                        help='shift (in seconds)')
    parser.add_argument('-o', '--output',
                        type=str,
                        help='path to the output file. If not provided, it overwrites the input file')
    parser.add_argument('-f', '--format',
                        type=str,
                        default='srt',
                        help=f'input subtitle file format, should be one of {formats_listed}')
    parser.add_argument('-r', '--framerate',
                        type=float,
                        default=24.0,
                        help='video framerate (only affects certain formats)')
    args = parser.parse_args()

    # Custom variables linked to parser
    input_file = args.input
    shift = args.shift
    output_file = args.output
    format = args.format
    framerate = args.framerate

    # Sanity check on the format
    if format not in formats_listed:
        raise ValueError(f'{format} is not a valid or supported file format.')
    sub_parser = FORMATS[format]

    # Read input file with the correct encoding
    input_encoding = None
    text = None
    for e in ENCODINGS:
        try:
            with open(input_file, 'r', encoding=e) as sub_file:
                text = sub_file.readlines()
                input_encoding = e
                break
        except UnicodeDecodeError:
            pass
        except:
            print('An error occured while reading the input file.')

    # Name of the output file
    if output_file is None:
        output_file = input_file

    # Write shifted file
    with open(output_file, 'w', encoding=input_encoding) as sub_file:
        sub_parser(sub_file, text, shift, framerate=framerate)

if __name__ == '__main__':
    main()