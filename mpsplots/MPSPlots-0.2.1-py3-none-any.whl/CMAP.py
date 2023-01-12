#!/usr/bin/env python
# -*- coding: utf-8 -*-


from matplotlib.colors import LinearSegmentedColormap

BKR = \
LinearSegmentedColormap.from_list('BKR', (
    # Edit this gradient at https://eltos.github.io/gradient/#0:7A90FF-33.9:0025B3-50:000000-75.8:C7030D-100:FF6E75
    (0.000, (0.478, 0.565, 1.000)),
    (0.339, (0.000, 0.145, 0.702)),
    (0.500, (0.000, 0.000, 0.000)),
    (0.758, (0.780, 0.012, 0.051)),
    (1.000, (1.000, 0.431, 0.459))))


BWR = \
LinearSegmentedColormap.from_list('RKB', (
    # Edit this gradient at https://eltos.github.io/gradient/#0025B3-7A90FF-FFFFFF-FF6E75-C7030D
    (0.000, (0.000, 0.145, 0.702)),
    (0.250, (0.478, 0.565, 1.000)),
    (0.500, (1.000, 1.000, 1.000)),
    (0.750, (1.000, 0.431, 0.459)),
    (1.000, (0.780, 0.012, 0.051))))