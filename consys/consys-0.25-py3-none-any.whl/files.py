"""
Files functionality
"""

import os
import re
import base64
import string
import random
import binascii

import requests
from PIL import Image, ExifTags, UnidentifiedImageError

from .errors import ErrorUpload


class FileUploader:
    """ File uploader """

    def __init__(self, path='/', prefix='/', side_optimized=None):
        self.path = path
        self.prefix = prefix
        self.side_optimized = side_optimized

    def get_name(self, url, num):
        """ Check existence the file by name """

        for i in os.listdir(f'{self.path}{url}/'):
            if re.search(rf"^{str(num)}.", i):
                return i

        return None

    @staticmethod
    def max_name(url):
        """ Next file ID """

        files = os.listdir(url)
        count = 0

        for i in files:
            j = re.findall(r'\d+', i)
            if len(j) and int(j[0]) > count:
                count = int(j[0])

        return count+1

    # pylint: disable=too-many-locals,too-many-branches,too-many-statements
    def image(self, data, encoding='base64', file_format='png'):
        """ Upload image """

        if data is None:
            return data

        if encoding != 'bytes':
            try:
                match = re.search(r'^\w+\.\w+$', data)
            except TypeError as e:
                raise ErrorUpload('image') from e

            if match:
                return data

        url = self.path
        url_opt = url + 'opt/'

        if encoding == 'base64':
            try:
                file_format = re.search(r'data:image/.+;base64,', data) \
                                .group()[11:-8]
                b64 = data.split(',')[1]
                data = base64.b64decode(b64)
            except (AttributeError, binascii.Error) as e:
                raise ErrorUpload('image') from e

        file_id = self.max_name(url)
        offset = '0' * max(0, 10-len(str(file_id)))
        payload = ''.join(
            random.choice(string.ascii_lowercase)
            for _ in range(6)
        )
        file_id = f'{offset}{file_id}{payload}'
        file_format = file_format.lower()
        file_name = f'{file_id}.{file_format}'
        url += file_name
        url_opt += file_name

        # TODO: check image data before save
        with open(url, 'wb') as file:
            try:
                file.write(data)
            except TypeError as e:
                raise ErrorUpload('image') from e

        # EXIF data
        # pylint: disable=protected-access

        try:
            try:
                img = Image.open(url)
            except UnidentifiedImageError as e:
                raise ErrorUpload('image') from e

            orientation = None

            # pylint: disable=consider-using-dict-items
            # pylint: disable=consider-iterating-dictionary
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break

            exif = dict(img._getexif().items())

            if exif[orientation] == 3:
                img = img.transpose(Image.ROTATE_180)
            elif exif[orientation] == 6:
                img = img.transpose(Image.ROTATE_270)
            elif exif[orientation] == 8:
                img = img.transpose(Image.ROTATE_90)

            img.save(url)
            img.close()

        except (AttributeError, KeyError, IndexError):
            pass

        # Optimized version
        if self.side_optimized:
            img = Image.open(url)

            if img.size[0] > img.size[1]:
                hpercent = (self.side_optimized / float(img.size[1]))
                wsize = int(float(img.size[0]) * float(hpercent))
                img = img.resize((wsize, self.side_optimized), Image.ANTIALIAS)
            else:
                wpercent = (self.side_optimized / float(img.size[0]))
                hsize = int(float(img.size[1]) * float(wpercent))
                img = img.resize((self.side_optimized, hsize), Image.ANTIALIAS)

            img.save(url_opt)

        return file_name

    def reimg(self, text):
        """ Load all images images from the text to the server """

        if text is None:
            return text

        # Base64
        while True:
            fragment = re.search(
                r'<img [^>]*src=[^>]+data:image/\w+;base64,[^\'">]+=[^>]+>',
                text
            )

            if fragment is None:
                break

            first, _ = fragment.span()
            meta_fragment = re.search(
                r'data:image/\w+;base64,[^\'">]+=', fragment.group()
            )

            meta_first, meta_last = meta_fragment.span()
            data = self.image(meta_fragment.group())
            text = text[:first+meta_first] \
                + self.prefix + data \
                + text[first+meta_last:]

        # External links
        while True:
            fragment = re.search(
                r'<img [^>]*src=[^\'">]*[\'"][^\'">]*http[^\'">]+[^>]*>', text
            )

            if fragment is None:
                break

            first, _ = fragment.span()
            meta_fragment = re.search(
                r'http[^\'">]+', fragment.group()
            )

            meta_first, meta_last = meta_fragment.span()
            link = meta_fragment.group()
            data = requests.get(link, timeout=10).content

            if '.' in link:
                file_format = link.split('.')[-1]

                if (
                    'latex' in file_format
                    or '/' in file_format
                    or len(file_format) > 5
                ):
                    file_format = 'png'

            else:
                file_format = None

            data = self.image(data, encoding='bytes', file_format=file_format)
            text = (
                text[:first+meta_first]
                + self.prefix + data
                + text[first+meta_last:]
            )

        return text
