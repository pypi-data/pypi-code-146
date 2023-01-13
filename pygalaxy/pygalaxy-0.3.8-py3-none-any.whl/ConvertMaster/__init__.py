#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def hex_to_rgb(hex_str: str):
    hex_str = hex_str.lstrip('#')
    lv = len(hex_str)
    return tuple(int(hex_str[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


if __name__ == '__main__':
    print(hex_to_rgb('#ffffff'))
