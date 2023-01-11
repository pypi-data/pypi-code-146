#!/usr/bin/python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class Ascii:
    """ ascii characters. """
    vertical_line = '│'
    horizontal_line = '─'
    horizontal_vertical = '┼'
    upper_right_corner = '┐'
    lower_left_corner = '└'
    lower_right_corner = '┘'
    upper_left_corner = '┌'
    horizontal_and_up = '┴'
    horizontal_and_down = '┬'
    vertical_and_right = '├'
    vertical_and_left = '┤'
