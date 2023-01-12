# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 07:41:11 2022

@author: Antonio
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

import random
import re
import string
from pathlib import Path

from autologbook import autoconfig
from autologbook.autotools import ElementTypeGuesser, get_patterns_from_config

image_file_matching = autoconfig.IMAGEFILE_MATCHING_PATTERNS
image_file_exclude = autoconfig.IMAGEFILE_EXCLUDE_PATTERNS
attachment_include_pattern = autoconfig.ATTACHMENT_MATCHING_PATTERNS
attachment_exclude_pattern = autoconfig.ATTACHMENT_EXCLUDE_PATTERNS
yaml_file_include_pattern = autoconfig.YAMLFILE_MATCHING_PATTERNS
yaml_file_exclude_pattern = autoconfig.YAMLFILE_EXCLUDE_PATTERNS
navigation_include_pattern = autoconfig.NAVIGATION_MATCHING_PATTERNS
navigation_exclude_pattern = autoconfig.NAVIGATION_EXCLUDE_PATTERNS
video_include_pattern = autoconfig.VIDEO_MATCHING_PATTERNS
video_exclude_pattern = autoconfig.VIDEO_EXCLUDE_PATTERNS
optical_include_pattern = autoconfig.OPTICAL_IMAGE_MATCHING_PATTERNS
optical_exclude_pattern = autoconfig.OPTICAL_IMAGE_EXCLUDE_PATTERNS


def alternate_case(input_str):
    """
    Return a string with alternating case

    Parameters
    ----------
    input_str : str
        input string to be alternated.

    Returns
    -------
    output_str : str
        A string with alternating case.

    """
    output_str = ''
    for i in range(len(input_str)):
        if i % 2 == 0:
            output_str = output_str + input_str[i].lower()
        else:
            output_str = output_str + input_str[i].upper()

    return output_str


def file_name_generator(size, chars=string.ascii_letters + string.digits):
    """
    Generate a string with a random content

    Parameters
    ----------
    size : int
        The length of the string to be generated.
    chars : str, optional
        The universe set from where the random content of the output string has to come from.
        The default is string.ascii_letters + string.digits.

    Returns
    -------
    file_name
        A string with random content.

    """
    return ''.join(random.choice(chars) for _ in range(size))


def execute_is_ok_test(guesser, paths):
    """
    Make the guesser to execute the is_ok test on all paths.

    Parameters
    ----------
    guesser : autotools.ElementTypeGuesser
        The ElementTypeGuesser that must execute the is_ok test.
    paths : list
        A list with all the paths that have to be tested.

    Returns
    -------
    None.

    """
    expected_result = True
    overall_result = True

    for path in paths:
        if guesser.is_ok(path):
            result = True
        else:
            result = False
        if result != expected_result:
            print(f'Error matching {path}')
        overall_result = overall_result and result

    assert overall_result == expected_result


def execute_is_ok_test_fail(guesser, paths):
    """
    Make the guesser to execute the is_ok test on all paths expecting to fail
    all the time.

    Parameters
    ----------
    guesser : autotools.ElementTypeGuesser
        The ElementTypeGuesser that must execute the is_ok test.
    paths : list
        A list with all the paths that have to be tested.

    Returns
    -------
    None.

    """
    expected_result = False
    overall_result = False

    for path in paths:
        if guesser.is_ok(path):
            result = True
            print(f"This {path} is ok, but it shouldn't!")
        else:
            result = False
        overall_result = overall_result or result

    assert overall_result == expected_result


def execute_matching_test(guesser, paths):
    """
    Make the guesser to execute the is_matching test on all paths.

    Parameters
    ----------
    guesser : autotools.ElementTypeGuesser
        The ElementTypeGuesser that must execute the is_matching test.
    paths : list
        A list with all the paths that have to be tested.

    Returns
    -------
    None.

    """
    expected_result = True
    overall_result = True

    for path in paths:
        if guesser._is_matching(path):
            result = True
        else:
            result = False
        if result != expected_result:
            print(f'Error matching {path}')
        overall_result = overall_result and result

    assert overall_result == expected_result


def execute_excluded_test(guesser, paths):
    """
    Make the guesser to execute the is_excluded test on all paths.

    Parameters
    ----------
    guesser : autotools.ElementTypeGuesser
        The ElementTypeGuesser that must execute the is_excluded test.
    paths : list
        A list with all the paths that have to be tested.

    Returns
    -------
    None.

    """
    expected_result = True
    overall_result = True

    for path in paths:
        if guesser._is_excluded(path):
            result = True
        else:
            result = False
        if result != expected_result:
            print(f'Error matching {path}')
        overall_result = overall_result and result
    assert overall_result is True


def test_successful_creation():
    """
    Test the capability to create a ElementTypeGuesser with all possible
    combination of input parameters.

    Returns
    -------
    None.

    """
    pattern = 'abcd'
    exclude = '1234'
    cpattern = re.compile(pattern)
    cexclude = re.compile(exclude)

    patterns = [file_name_generator(5) for _ in range(5)]
    excludes = [file_name_generator(5) for _ in range(5)]

    p = [pattern, cpattern, patterns]
    e = [exclude, cexclude, excludes, None]

    for i in p:
        for j in e:
            ElementTypeGuesser(i, j)


def test_failed_creation():
    """
    Test the detection of wrong type parameters in the creation of a new
    ElementTypeGuesser

    Returns
    -------
    None.

    """
    pattern = 'abcd'
    exclude = '1234'
    cpattern = re.compile(pattern)
    cexclude = re.compile(exclude)

    patterns = [file_name_generator(5) for _ in range(5)]
    excludes = [file_name_generator(5) for _ in range(5)]

    wrong_arg = Path().cwd()

    raise_count = 0

    p = [pattern, cpattern, patterns]
    e = [exclude, cexclude, excludes, None]

    for i in p:
        try:
            # noinspection PyTypeChecker
            ElementTypeGuesser(i, wrong_arg)
        except TypeError:
            raise_count += 1

    for i in e:
        try:
            # noinspection PyTypeChecker
            ElementTypeGuesser(wrong_arg, i)
        except TypeError:
            raise_count += 1

    assert raise_count == len(p) + len(e)


def test_valid_microscope_picture():
    """
    Test ElementTypeGuesser matching and excluding regular expressions.

    Returns
    -------
    None.

    """
    etg = ElementTypeGuesser(image_file_matching, image_file_exclude)

    exts = ['.tif', '_crop.tif', 'crop.tif']

    paths_to_test = []

    for ext in exts:
        paths_to_test.append(
            'filename-' + file_name_generator(8) + ext.lower())
        paths_to_test.append(
            'filename-' + file_name_generator(8) + alternate_case(ext))
        paths_to_test.append(
            'filename-' + file_name_generator(8) + ext.upper())

    execute_is_ok_test(etg, paths_to_test)


def test_excluded_microscope_picture():
    """
    Test ElementTypeGuesser excluding regular expressions.

    Returns
    -------
    None.

    """
    etg = ElementTypeGuesser(image_file_matching, image_file_exclude)

    intra = ['crop', 'cropped', 'croped']
    ext = ['_crop.tif', '_croped.tif', '_cropped.tif']
    paths_to_test = []

    for i in intra:
        for e in ext:
            paths_to_test.append('path-' + file_name_generator(5)
                                 + i.lower() + 'filename-' + file_name_generator(8) + e.lower())
            paths_to_test.append('path-' + file_name_generator(5)
                                 + i.lower() + 'filename-' + file_name_generator(8) + e.upper())
            paths_to_test.append('path-' + file_name_generator(5) + i.lower()
                                 + 'filename-' + file_name_generator(8) + alternate_case(e))

            paths_to_test.append('path-' + file_name_generator(5)
                                 + i.upper() + 'filename-' + file_name_generator(8) + e.lower())
            paths_to_test.append('path-' + file_name_generator(5)
                                 + i.upper() + 'filename-' + file_name_generator(8) + e.upper())
            paths_to_test.append('path-' + file_name_generator(5) + i.upper()
                                 + 'filename-' + file_name_generator(8) + alternate_case(e))

            paths_to_test.append('path-' + file_name_generator(5) + alternate_case(
                i) + 'filename-' + file_name_generator(8) + e.lower())
            paths_to_test.append('path-' + file_name_generator(5) + alternate_case(
                i) + 'filename-' + file_name_generator(8) + e.upper())
            paths_to_test.append('path-' + file_name_generator(5) + alternate_case(
                i) + 'filename-' + file_name_generator(8) + alternate_case(e))

    intra = ['\\exclude\\', '\\recycle\\']
    ext = ['.tif']
    for i in intra:
        for e in ext:
            paths_to_test.append('path-' + file_name_generator(5)
                                 + i.lower() + 'filename-' + file_name_generator(8) + e.lower())
            paths_to_test.append('path-' + file_name_generator(5)
                                 + i.lower() + 'filename-' + file_name_generator(8) + e.upper())
            paths_to_test.append('path-' + file_name_generator(5) + i.lower()
                                 + 'filename-' + file_name_generator(8) + alternate_case(e))

            paths_to_test.append('path-' + file_name_generator(5)
                                 + i.upper() + 'filename-' + file_name_generator(8) + e.lower())
            paths_to_test.append('path-' + file_name_generator(5)
                                 + i.upper() + 'filename-' + file_name_generator(8) + e.upper())
            paths_to_test.append('path-' + file_name_generator(5) + i.upper()
                                 + 'filename-' + file_name_generator(8) + alternate_case(e))

            paths_to_test.append('path-' + file_name_generator(5) + alternate_case(
                i) + 'filename-' + file_name_generator(8) + e.lower())
            paths_to_test.append('path-' + file_name_generator(5) + alternate_case(
                i) + 'filename-' + file_name_generator(8) + e.upper())
            paths_to_test.append('path-' + file_name_generator(5) + alternate_case(
                i) + 'filename-' + file_name_generator(8) + alternate_case(e))

    execute_excluded_test(etg, paths_to_test)


def test_matching_but_excluded_microscope_picture():
    """
    Test ElementTypeGuesser capability to match a path but exclude this due to
    the exclude rule.

    Returns
    -------
    None.

    """
    etg = ElementTypeGuesser(image_file_matching, image_file_exclude)

    intra = ['crop', 'cropped', 'croped']
    ext = ['_crop.tif', '_croped.tif', '_cropped.tif']
    paths_to_test = []

    for i in intra:
        for e in ext:
            paths_to_test.append('path-' + file_name_generator(5)
                                 + i.lower() + 'filename-' + file_name_generator(8) + e.lower())
            paths_to_test.append('path-' + file_name_generator(5)
                                 + i.lower() + 'filename-' + file_name_generator(8) + e.upper())
            paths_to_test.append('path-' + file_name_generator(5) + i.lower()
                                 + 'filename-' + file_name_generator(8) + alternate_case(e))

            paths_to_test.append('path-' + file_name_generator(5)
                                 + i.upper() + 'filename-' + file_name_generator(8) + e.lower())
            paths_to_test.append('path-' + file_name_generator(5)
                                 + i.upper() + 'filename-' + file_name_generator(8) + e.upper())
            paths_to_test.append('path-' + file_name_generator(5) + i.upper()
                                 + 'filename-' + file_name_generator(8) + alternate_case(e))

            paths_to_test.append('path-' + file_name_generator(5) + alternate_case(
                i) + 'filename-' + file_name_generator(8) + e.lower())
            paths_to_test.append('path-' + file_name_generator(5) + alternate_case(
                i) + 'filename-' + file_name_generator(8) + e.upper())
            paths_to_test.append('path-' + file_name_generator(5) + alternate_case(
                i) + 'filename-' + file_name_generator(8) + alternate_case(e))

    folder = ['excluded', 'recycle']
    for f in folder:
        for e in ext:
            paths_to_test.append(file_name_generator(5) + '\\' + f + '\\' + file_name_generator(8) + e)

    execute_matching_test(etg, paths_to_test)
    execute_excluded_test(etg, paths_to_test)


def test_invalid_microscope_picture():
    """
    Test the ElementTypeGuesser to identify invalid microscope pictures-

    Returns
    -------
    None.

    """
    etg = ElementTypeGuesser(image_file_matching, image_file_exclude)

    paths_to_test = []

    # add wrong extensions
    n_exts = 5
    # note the missing . in front of tif
    bad_exts = [random.choice(['.bmp', '.jpg', '.png', 'tif'])
                for _ in range(n_exts)]
    crop_intra = ['crop', 'cropped', 'croped']
    crop_ext = ['_crop.tif', '_croped.tif', '_cropped.tif']

    for e in bad_exts:
        # add not matching filenames
        paths_to_test.append('filename-' + file_name_generator(8) + e.lower())
        paths_to_test.append('filename-' + file_name_generator(8) + e.upper())
        paths_to_test.append(
            'filename-' + file_name_generator(8) + alternate_case(e))

    for i in crop_intra:
        for e in crop_ext:
            # add matching filenames but excluded
            paths_to_test.append('path-' + file_name_generator(5)
                                 + i.lower() + 'filename-' + file_name_generator(8) + e.lower())
            paths_to_test.append('path-' + file_name_generator(5)
                                 + i.lower() + 'filename-' + file_name_generator(8) + e.upper())
            paths_to_test.append('path-' + file_name_generator(5) + i.lower()
                                 + 'filename-' + file_name_generator(8) + alternate_case(e))

            paths_to_test.append('path-' + file_name_generator(5)
                                 + i.upper() + 'filename-' + file_name_generator(8) + e.lower())
            paths_to_test.append('path-' + file_name_generator(5)
                                 + i.upper() + 'filename-' + file_name_generator(8) + e.upper())
            paths_to_test.append('path-' + file_name_generator(5) + i.upper()
                                 + 'filename-' + file_name_generator(8) + alternate_case(e))

            paths_to_test.append('path-' + file_name_generator(5) + alternate_case(
                i) + 'filename-' + file_name_generator(8) + e.lower())
            paths_to_test.append('path-' + file_name_generator(5) + alternate_case(
                i) + 'filename-' + file_name_generator(8) + e.upper())
            paths_to_test.append('path-' + file_name_generator(5) + alternate_case(
                i) + 'filename-' + file_name_generator(8) + alternate_case(e))

    execute_is_ok_test_fail(etg, paths_to_test)


def test_valid_navigation_picture():
    """
    Test the matching regular expression for Navigation Images.

    Returns
    -------
    None.

    """
    etg = ElementTypeGuesser(navigation_include_pattern,
                             navigation_exclude_pattern)

    valid_intra = ['navcam', 'Nav-Cam', 'Nav_Cam', 'navigationcam',
                   'navcamera', 'navigation-camera', 'navigation-camera']

    path_to_test = []

    for i in valid_intra:
        path_to_test.append(file_name_generator(8) + i.lower() + '.jpg')
        path_to_test.append(file_name_generator(8) + i.upper() + '.jpg')
        path_to_test.append(file_name_generator(8)
                            + alternate_case(i) + '.jpg')

    execute_is_ok_test(etg, path_to_test)


def test_valid_attachment():
    """
    Test the matching regular expression for Attachments file.

    Returns
    -------
    None.

    """
    etg = ElementTypeGuesser(attachment_include_pattern,
                             attachment_exclude_pattern)

    valid_ext = ['doc', 'docx', 'pdf', 'xls', 'xlsx', 'xlsm']

    path_to_test = []

    for ext in valid_ext:
        path_to_test.append(file_name_generator(8) + '.' + ext.lower())
        path_to_test.append(file_name_generator(8) + '.' + ext.upper())

    execute_is_ok_test(etg, path_to_test)


def test_valid_yaml():
    """
    Test the matching regular expression for yaml customization files.

    Returns
    -------
    None.

    """
    etg = ElementTypeGuesser(yaml_file_include_pattern,
                             yaml_file_exclude_pattern)

    valid_ext = ['yml', 'yaml']

    path_to_test = []

    for ext in valid_ext:
        path_to_test.append(file_name_generator(8) + '.' + ext.lower())
        path_to_test.append(file_name_generator(8) + '.' + ext.upper())
        path_to_test.append(file_name_generator(8) + '.' + alternate_case(ext))

    execute_is_ok_test(etg, path_to_test)


def test_pattern_grabbing():
    matching, excluded = get_patterns_from_config()
    c_matching = [re.compile(r) for r in matching]
    c_excluded = [re.compile(r) for r in excluded]

    exts = ['.tif', '_crop.tif', 'crop.tif', '.rst']

    paths_to_test = []

    for ext in exts:
        paths_to_test.append(
            'filename-' + file_name_generator(8) + ext.lower())
        paths_to_test.append(
            'filename-' + file_name_generator(8) + alternate_case(ext))
        paths_to_test.append(
            'filename-' + file_name_generator(8) + ext.upper())
        paths_to_test.append(
            'crop/filename-' + file_name_generator(8) + ext.upper())

    skipped = 0
    accepted = 0
    not_accepted = 0

    for p in paths_to_test:
        if any(r.match(p) for r in c_excluded):
            skipped += 1
        else:
            if any(r.match(p) for r in c_matching):
                accepted += 1
            else:
                not_accepted += 1

    assert skipped == 1
    assert accepted == 11
    assert not_accepted == 4


def test_valid_video_file():
    """
    Test the matching regular expression for video files.

    Returns
    -------
    None.

    """
    etg = ElementTypeGuesser(video_include_pattern,
                             video_exclude_pattern)

    valid_ext = ['avi', 'mp4']

    path_to_test = []

    for ext in valid_ext:
        path_to_test.append(file_name_generator(8) + '.' + ext.lower())
        path_to_test.append(file_name_generator(8) + '.' + ext.upper())
        path_to_test.append(file_name_generator(8) + '.' + alternate_case(ext))

    execute_is_ok_test(etg, path_to_test)


def test_invalid_video_file():
    """
    Test the matching regular expression for video files.

    Returns
    -------
    None.

    """
    etg = ElementTypeGuesser(video_include_pattern,
                             video_exclude_pattern)

    invalid_ext = ['flv', 'mp3']

    path_to_test = []

    for ext in invalid_ext:
        path_to_test.append(file_name_generator(8) + '.' + ext.lower())
        path_to_test.append(file_name_generator(8) + '.' + ext.upper())
        path_to_test.append(file_name_generator(8) + '.' + alternate_case(ext))

    execute_is_ok_test_fail(etg, path_to_test)


def test_valid_optical_picture():
    etg = ElementTypeGuesser(optical_include_pattern, optical_exclude_pattern)
    valid_ext = ['.png', '.jpg', '.jfif', '.jpeg', '.jpe', '.jif']

    paths_to_text = []
    for ext in valid_ext:
        paths_to_text.append('f-' + file_name_generator(8) + ext.lower())
        paths_to_text.append('f-' + file_name_generator(8) + ext.upper())
        paths_to_text.append('f-' + file_name_generator(8) + alternate_case(ext))

    execute_is_ok_test(etg, paths_to_text)


def test_matching_but_excluded_optical_picture():
    etg = ElementTypeGuesser(optical_include_pattern, optical_exclude_pattern)
    valid_ext = ['.png', '.jpg', '.jfif', '.jpeg', '.jpe', '.jif']
    invalid_intra = ['excluded', 'exclude', 'recycle', 'recycled']

    paths_to_test = []
    for i in invalid_intra:
        for e in valid_ext:
            paths_to_test.append('path\\' + i.lower() + '\\' + file_name_generator(8) + e.lower())
            paths_to_test.append('path\\' + i.lower() + '\\' + file_name_generator(8) + e.upper())
            paths_to_test.append('path\\' + i.lower() + '\\' + file_name_generator(8) + alternate_case(e))
            paths_to_test.append('path\\' + i.upper() + '\\' + file_name_generator(8) + e.lower())
            paths_to_test.append('path\\' + i.upper() + '\\' + file_name_generator(8) + e.upper())
            paths_to_test.append('path\\' + i.upper() + '\\' + file_name_generator(8) + alternate_case(e))
            paths_to_test.append('path\\' + alternate_case(i) + '\\' + file_name_generator(8) + e.lower())
            paths_to_test.append('path\\' + alternate_case(i) + '\\' + file_name_generator(8) + e.upper())
            paths_to_test.append('path\\' + alternate_case(i) + '\\' + file_name_generator(8) + alternate_case(e))

    execute_matching_test(etg, paths_to_test)
    execute_excluded_test(etg, paths_to_test)


def test_excluded_optical_picture():
    etg = ElementTypeGuesser(optical_include_pattern, optical_exclude_pattern)
    invalid_patterns = ['navicam']
    valid_ext = ['.png', '.jpg', '.jfif', '.jpeg', '.jpe', '.jif']

    paths_to_test = []
    for i in invalid_patterns:
        for e in valid_ext:
            paths_to_test.append(file_name_generator(5) + '-' + i.lower() + e.lower())
            paths_to_test.append(file_name_generator(5) + '-' + i.lower() + e.upper())
            paths_to_test.append(file_name_generator(5) + '-' + i.lower() + alternate_case(e))
            paths_to_test.append(file_name_generator(5) + '-' + i.upper() + e.lower())
            paths_to_test.append(file_name_generator(5) + '-' + i.upper() + e.upper())
            paths_to_test.append(file_name_generator(5) + '-' + i.upper() + alternate_case(e))
            paths_to_test.append(file_name_generator(5) + '-' + alternate_case(i) + e.lower())
            paths_to_test.append(file_name_generator(5) + '-' + alternate_case(i) + e.upper())
            paths_to_test.append(file_name_generator(5) + '-' + alternate_case(i) + alternate_case(e))

    invalid_patterns = ['exclude', 'recycle']
    for i in invalid_patterns:
        for e in valid_ext:
            paths_to_test.append(file_name_generator(5) + '\\' + i.lower() + '\\' + file_name_generator(5) + e.lower())
            paths_to_test.append(file_name_generator(5) + '\\' + i.lower() + '\\' + file_name_generator(5) + e.upper())
            paths_to_test.append(file_name_generator(5) + '\\' + i.lower() + '\\' + file_name_generator(5) +
                                 alternate_case(e))
            paths_to_test.append(file_name_generator(5) + '\\' + i.upper() + '\\' + file_name_generator(5) + e.lower())
            paths_to_test.append(file_name_generator(5) + '\\' + i.upper() + '\\' + file_name_generator(5) + e.upper())
            paths_to_test.append(file_name_generator(5) + '\\' + i.upper() + '\\' + file_name_generator(5) +
                                 alternate_case(e))
            paths_to_test.append(file_name_generator(5) + '\\' + alternate_case(i) + '\\' + file_name_generator(5) +
                                 e.lower())
            paths_to_test.append(file_name_generator(5) + '\\' + alternate_case(i) + '\\' + file_name_generator(5) +
                                 e.upper())
            paths_to_test.append(file_name_generator(5) + '\\' + alternate_case(i) + '\\' + file_name_generator(5) +
                                 alternate_case(e))

    paths_to_test.append(file_name_generator(5) + '\\thumb-png\\'.lower() + file_name_generator(5) +
                         '-thumb-png.png'.lower())
    paths_to_test.append(
        file_name_generator(5) + '\\thumb-png\\'.lower() + file_name_generator(5) + '-thumb-png.png'.upper())
    paths_to_test.append(
        file_name_generator(5) + '\\thumb-png\\'.lower() + file_name_generator(5) + alternate_case('-thumb-png.png'))

    paths_to_test.append(file_name_generator(5) + '\\thumb-png\\'.upper() + file_name_generator(5) +
                         '-thumb-png.png'.lower())
    paths_to_test.append(
        file_name_generator(5) + '\\thumb-png\\'.upper() + file_name_generator(5) + '-thumb-png.png'.upper())
    paths_to_test.append(
        file_name_generator(5) + '\\thumb-png\\'.upper() + file_name_generator(5) + alternate_case('-thumb-png.png'))

    paths_to_test.append(
        file_name_generator(5) + alternate_case('\\thumb-png\\') + file_name_generator(5) + '-thumb-png.png'.lower())
    paths_to_test.append(
        file_name_generator(5) + alternate_case('\\thumb-png\\') + file_name_generator(5) + '-thumb-png.png'.upper())
    paths_to_test.append(
        file_name_generator(5) + alternate_case('\\thumb-png\\') + file_name_generator(5) +
        alternate_case('-thumb-png.png'))

    paths_to_test.append(file_name_generator(5) + '\\png\\'.lower() + file_name_generator(5) + '-png.png'.lower())
    paths_to_test.append(file_name_generator(5) + '\\png\\'.lower() + file_name_generator(5) + '-png.png'.upper())
    paths_to_test.append(
        file_name_generator(5) + '\\png\\'.lower() + file_name_generator(5) + alternate_case('-png.png'))

    paths_to_test.append(file_name_generator(5) + '\\png\\'.upper() + file_name_generator(5) + '-png.png'.lower())
    paths_to_test.append(file_name_generator(5) + '\\png\\'.upper() + file_name_generator(5) + '-png.png'.upper())
    paths_to_test.append(
        file_name_generator(5) + '\\png\\'.upper() + file_name_generator(5) + alternate_case('-png.png'))

    paths_to_test.append(
        file_name_generator(5) + alternate_case('\\png\\') + file_name_generator(5) + '-png.png'.lower())
    paths_to_test.append(
        file_name_generator(5) + alternate_case('\\png\\') + file_name_generator(5) + '-png.png'.upper())
    paths_to_test.append(
        file_name_generator(5) + alternate_case('\\png\\') + file_name_generator(5) + alternate_case('-png.png'))

    execute_excluded_test(etg, paths_to_test)
