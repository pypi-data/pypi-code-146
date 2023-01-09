from io import StringIO, BytesIO
import base64
from PIL import Image
from PIL import ImageChops
import math, operator
from functools import reduce
import re
import os
import requests
from bs4 import BeautifulSoup

CURRENT_PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_keypad_img(LOG_PATH=os.path.devnull):
    def hex2bin(hex):
        hex_tab = "0123456789abcdef"
        result = []

        for i in range(0, len(hex), 2):
            ch1 = hex_tab.index(hex[i])
            ch2 = hex_tab.index(hex[i + 1])
            byte1 = (ch1 << 4) | ch2
            result.append(chr(byte1))

        return ''.join(result)

    session = requests.Session()

    res = session.get('https://obank.kbstar.com/quics?page=C025255&cc=b028364:b028702&QSL=F')

    ori_html = res.text

    search = re.search('hex2bin\("[a-z0-9]{1,}"\)', ori_html)

    hex = search.group().replace("\")", "").replace("hex2bin(\"", "")

    html = hex2bin(hex)

    bs = BeautifulSoup(html, 'html.parser')

    img_tag = bs.find('img')

    img_url = 'https://obank.kbstar.com' + img_tag.attrs.get('src')

    keymap = img_tag.attrs.get('usemap').replace('#divKeypad', '')[:-3]

    img_res = session.get(img_url, stream=True)
    real = Image.open(BytesIO(img_res.content))

    ori_bs = BeautifulSoup(ori_html, 'html.parser')

    KEYPAD_USEYN = ori_bs.select_one('input[id*="KEYPAD_USEYN"]').get('value')
    area_list = bs.select('map > area')

    area_hash_list = []
    area_pattern = re.compile("'(\w+)'")

    for area in area_list:
        re_matched = area_pattern.findall(area.attrs.get('onmousedown'))
        if re_matched:
            area_hash_list.append(re_matched[0])

    JSESSIONID = session.cookies['JSESSIONID']
    QSID = session.cookies['QSID']

    # Get list
    num_sequence = _get_keypad_num_list(real)

    PW_DIGITS = {}
    # FIXED
    PW_DIGITS['1'] = area_hash_list[0]
    PW_DIGITS['2'] = area_hash_list[1]
    PW_DIGITS['3'] = area_hash_list[2]
    PW_DIGITS['4'] = area_hash_list[3]
    PW_DIGITS['6'] = area_hash_list[5]

    # Floating..
    for idx, num in enumerate(num_sequence):
        if idx == 0:
            PW_DIGITS[str(num)] = area_hash_list[4]
        elif idx == 1:
            PW_DIGITS[str(num)] = area_hash_list[6]
        elif idx == 2:
            PW_DIGITS[str(num)] = area_hash_list[7]
        elif idx == 3:
            PW_DIGITS[str(num)] = area_hash_list[8]
        elif idx == 4:
            PW_DIGITS[str(num)] = area_hash_list[9]

    return {
        'JSESSIONID': JSESSIONID,
        'QSID': QSID,
        'KEYMAP': keymap,
        'PW_DIGITS': PW_DIGITS,
        'KEYPAD_USEYN': KEYPAD_USEYN
    }


def rmsdiff(im1, im2):
    h = ImageChops.difference(im1, im2).histogram()
    return math.sqrt(reduce(operator.add,
                            map(lambda h, i: h * (i ** 2), h, range(256))
                            ) / (float(im1.size[0]) * im1.size[1]))


def _get_keypad_num_list(img):
    img = img.convert('RGBA')

    # 57x57 box
    box_5th = Image.open(os.path.join(CURRENT_PACKAGE_DIR, 'assets', '5.png'))
    box_7th = Image.open(os.path.join(CURRENT_PACKAGE_DIR, 'assets', '7.png'))
    box_8th = Image.open(os.path.join(CURRENT_PACKAGE_DIR, 'assets', '8.png'))
    box_9th = Image.open(os.path.join(CURRENT_PACKAGE_DIR, 'assets', '9.png'))
    box_0th = Image.open(os.path.join(CURRENT_PACKAGE_DIR, 'assets', '0.png'))

    box_dict = {
        5: box_5th,
        7: box_7th,
        8: box_8th,
        9: box_9th,
        0: box_0th,
    }

    # 57x57 box
    crop_5th = img.crop(box=(74, 99, 131, 156))
    crop_7th = img.crop(box=(16, 157, 73, 214))
    crop_8th = img.crop(box=(74, 157, 131, 214))
    crop_9th = img.crop(box=(132, 157, 189, 214))
    crop_0th = img.crop(box=(74, 215, 131, 272))

    crop_list = [crop_5th, crop_7th, crop_8th, crop_9th, crop_0th]

    keypad_num_list = []

    for idx, crop in enumerate(crop_list):
        for key, box in box_dict.items():
            try:
                diff = rmsdiff(crop, box)
                if diff < 13:
                    keypad_num_list += [key]
            except Exception as e:
                print(e)
    return keypad_num_list


if __name__ == '__main__':
    print(get_keypad_img('phantomjs'))  # PATH to phantomjs
    print(_get_keypad_num_list())
