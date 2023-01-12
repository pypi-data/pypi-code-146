# -*- coding: utf-8 -*-
"""
Implementation of the optical images factory
"""

# Copyright (c) 2022. Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction, including without
# limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
# Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

#
#
from __future__ import annotations

import piexif
from pathlib import Path
from typing import Any
from PIL import Image, ExifTags
import logging
from autologbook.html_helpers import HTMLHelperMixin
from autologbook import autoconfig, autoerror
from autologbook.autotools import OpticalImageType, pretty_print_dict, ResolutionUnit
from autologbook.containers import ResettableDict

log = logging.getLogger('__main__')

orientation_value = {
    1: '0 degrees',
    2: '0 degrees, mirrored',
    3: '180 degrees',
    4: '180 degrees, mirrored',
    5: '90 degrees',
    6: '90 degrees, mirrored',
    7: '270 degrees',
    8: '270 degrees, mirrored'
}


class GenericOpticalImage(HTMLHelperMixin):
    def __init__(self, path: str | Path):
        super().__init__()
        self.params = dict()
        self._raw_metadata = None
        self.params['path'] = Path(path)
        self.params['filename'] = self.params['path'].name
        self.params['url'] = self.convert_path_to_uri(path)
        self.params['key'] = str(path)
        self.params['thumb_rowspan'] = 1
        self.params['thumb_max_width'] = autoconfig.IMAGE_SAMPLE_THUMB_MAX_WIDTH
        self._type = OpticalImageType.GENERIC_OPTICAL_IMAGE
        self.retrieve_metadata()
        self.template = 'optical_image_base_template.yammy'

    @property
    def key(self) -> str:
        return self.params['key']

    @property
    def path(self) -> Path:
        return self.params['path']

    @path.setter
    def path(self, path: str | Path):
        self.params['path'] = Path(path)

    def get_parameter(self, param_key: str, default_value: Any = None) -> Any:
        if param_key in self.params:
            return self.params[param_key]
        else:
            return default_value

    def print_metadata(self):
        pretty_print_dict(self.params)

    def retrieve_metadata(self):
        with Image.open(self.path) as img:
            img.load()
            self._retrieve_basic_info(img)
            self._retrieve_raw_metadata(img)
            self._process_raw_metadata()

        img.close()

    def update(self):
        self.retrieve_metadata()

    def _retrieve_basic_info(self, img: Image):
        self.params['format'] = img.format
        self.params['x_pixel'], self.params['y_pixel'] = img.size

    def _retrieve_raw_metadata(self, img: Image):
        self._raw_metadata = dict(img.getexif())

    def _process_raw_metadata(self):
        for key, value in self._raw_metadata.items():
            self.params[ExifTags.TAGS.get(key, key)] = value
        self.params['Resolution'] = f"{self.params.get('XResolution', '0')} x {self.params.get('YResolution', '0')} " \
                                    f"{ResolutionUnit.inverse_resolution_unit(ResolutionUnit(self.params.get('ResolutionUnit', 1)))} "
        self.params['MP'] = float(self.params.get('x_pixel', 0)) * float(self.params.get('y_pixel', 0)) / 1000000
        self.params['Orientation_str'] = orientation_value.get(self.params.get('Orientation', 1), '0 degrees')


class DigitalCameraOpticalImage(GenericOpticalImage):

    def __init__(self, path: str | Path):
        super().__init__(path)
        self._type = OpticalImageType.DIGITAL_CAMERA_OPTICAL_IMAGE
        self.retrieve_metadata()
        self.params['thumb_rowspan'] = 2
        self.template = 'digital_camera_optical_image_template.yammy'


class KeyenceMicroscopeImage(GenericOpticalImage):

    def __init__(self, path: str | Path):
        super().__init__(path)
        self._type = OpticalImageType.KEYENCE_OPTICAL_IMAGE
        self.retrieve_metadata()
        self.params['thumb_rowspan'] = 2
        self.template = 'keyence_optical_image_template.yammy'


class DigitalCameraOpticalImageWithGPS(DigitalCameraOpticalImage):

    def __init__(self, path: str | Path):
        super().__init__(path)
        self._type = OpticalImageType.DIGITAL_CAMERA_OPTICAL_IMAGE_WITH_GPS
        self.params['thumb_rowspan'] = 3
        self.template = 'digital_camera_optical_image_gps_template.yammy'

    def retrieve_metadata(self):
        with Image.open(self.path) as img:
            img.load()
            self._retrieve_basic_info(img)
            self._retrieve_raw_metadata(img)
            self._retrieve_gps_metadata(img)
            self._process_raw_metadata()

        img.close()

    def _retrieve_gps_metadata(self, img):
        exif_dict = piexif.load(img.info.get('exif'))
        gps_info = dict()

        gps_key = 'GPS'
        codec = 'UTF-8'
        for tag in exif_dict[gps_key]:
            try:
                element = exif_dict[gps_key][tag].decode(codec)
            except AttributeError:
                element = exif_dict[gps_key][tag]

            gps_info[piexif.TAGS[gps_key][tag]['name']] = element

        self.params['GPSINFO'] = gps_info
        self.params['GPSLatitude'] = self.decode_gps('latitude', gps_info)
        self.params['GPSLongitude'] = self.decode_gps('longitude', gps_info)
        self.params['GPSAltitude'] = self.decode_gps('altitude', gps_info)

    @staticmethod
    def decode_gps(what: str, gps_info: dict) -> str:
        if what.lower() == 'latitude':
            ref_key = 'GPSLatitudeRef'
            val_key = 'GPSLatitude'
        elif what.lower() == 'longitude':
            ref_key = 'GPSLongitudeRef'
            val_key = 'GPSLongitude'
        elif what.lower() == 'altitude':
            ref_key = 'GPSAltitudeRef'
            val_key = 'GPSAltitude'
        else:
            ref_key = ''
            val_key = ''

        if ref_key not in gps_info and val_key not in gps_info:
            return 'Unknown'

        card = gps_info[ref_key]

        if what.lower() in ['latitude', 'longitude']:
            val = [n / d for n, d in gps_info[val_key]]
            return f'{card} {val[0]}° {val[1]}\' {val[2]}\"'
        else:
            val = gps_info[val_key][0] / gps_info[val_key][1]
            return f'{val} m'


class OpticalImageFactory:

    def __init__(self):
        self._creators = dict()

    def register_optical_image_type(self, image_type: OpticalImageType, image_class: type[GenericOpticalImage]):
        self._creators[image_type] = image_class

    def get_optical_image(self, path: str | Path, image_type: OpticalImageType = None) -> GenericOpticalImage:
        if image_type is None:
            image_type = self.guess_type(path)
        if image_type == OpticalImageType.INVALID_OPTICAL_IMAGE:
            raise autoerror.InvalidOpticalImageError(path)
        return self._creators[image_type](path)

    def get_optical_image_type(self) -> list[OpticalImageType]:
        return list(self._creators.keys())

    def remove_optical_image_type(self, image_type: OpticalImageType):
        if image_type in self._creators:
            del self._creators[image_type]
        else:
            log.warning('Image type %s not registered.' % image_type)

    def guess_format(self, path: str | Path) -> str:
        with Image.open(path) as image:
            f = image.format
        image.close()
        return f

    def guess_type_of_jpeg(self, image: Image) -> OpticalImageType:
        try:
            exif = piexif.load(image.info['exif'])
            if piexif.ExifIFD.MakerNote in exif['Exif'] and exif['Exif'][piexif.ExifIFD.MakerNote][
                                                            :7] == b'KmsFile':
                image_type = OpticalImageType.KEYENCE_OPTICAL_IMAGE
            elif 'GPS' in exif and exif['GPS'] != {} and piexif.ImageIFD.Make in exif['0th']:
                image_type = OpticalImageType.DIGITAL_CAMERA_OPTICAL_IMAGE_WITH_GPS
            elif piexif.ImageIFD.Make in exif['0th']:
                if exif['0th'][piexif.ImageIFD.Make] == b'TESCAN':
                    image_type = OpticalImageType.INVALID_OPTICAL_IMAGE
                else:
                    image_type = OpticalImageType.DIGITAL_CAMERA_OPTICAL_IMAGE
            else:
                image_type = OpticalImageType.GENERIC_OPTICAL_IMAGE
        except KeyError:
            image_type = OpticalImageType.GENERIC_OPTICAL_IMAGE
        finally:
            return image_type

    def guess_type_of_png(self, image: Image) -> OpticalImageType:
        return OpticalImageType.GENERIC_OPTICAL_IMAGE

    def guess_type(self, path: str | Path) -> OpticalImageType:
        with Image.open(path) as image:
            image.load()
            try:
                if image.format == 'JPEG':
                    typ = self.guess_type_of_jpeg(image)
                elif image.format == 'PNG':
                    typ = self.guess_type_of_png(image)
                else:
                    typ = OpticalImageType.GENERIC_OPTICAL_IMAGE

            except KeyError:
                typ = OpticalImageType.GENERIC_OPTICAL_IMAGE
            finally:
                image.close()
                return typ


optical_image_factory = OpticalImageFactory()
optical_image_factory.register_optical_image_type(OpticalImageType.GENERIC_OPTICAL_IMAGE, GenericOpticalImage)
optical_image_factory.register_optical_image_type(
    OpticalImageType.DIGITAL_CAMERA_OPTICAL_IMAGE, DigitalCameraOpticalImage)
optical_image_factory.register_optical_image_type(OpticalImageType.KEYENCE_OPTICAL_IMAGE, KeyenceMicroscopeImage)
optical_image_factory.register_optical_image_type(OpticalImageType.DIGITAL_CAMERA_OPTICAL_IMAGE_WITH_GPS,
                                                  DigitalCameraOpticalImageWithGPS)


class OpticalImageDict(ResettableDict):
    """A dictionary of optical images"""

    def __init__(self, initialdata=None):
        super().__init__(initialdata)

    def add(self, optical_image: GenericOpticalImage | str | Path):
        if not isinstance(optical_image, (GenericOpticalImage, str, Path)):
            raise TypeError(
                'Optical Images type must be derived from AbstractOpticalImage, string or path-like')

        if isinstance(optical_image, (str, Path)):
            optical_image = optical_image_factory.get_optical_image(optical_image)

        if optical_image.key in self.data.keys():
            raise autoerror.DuplicatedKey(
                'Attempt to add another optical image with the same key %s' % optical_image.key)
        else:
            self.data[optical_image.params['key']] = optical_image

    def remove(self, optical_image: GenericOpticalImage | str | Path) -> None:
        if not isinstance(optical_image, (GenericOpticalImage, str, Path)):
            raise TypeError('Optical image type must be derived from AbstractOpticalImage, string or path-like')

        if isinstance(optical_image, GenericOpticalImage):
            key = optical_image.key
        else:
            key = str(optical_image)

        if key in self.data:
            del self.data[key]
        else:
            log.warning('Attempt to remove %s from the optical image dictionary, but it was not there' % key)

# optical_image_factory = OpticalImageFactory()
# optical_image_factory.register_optical_image_type(OpticalImageType.GENERIC_OPTICAL_IMAGE, GenericOpticalImage)
# optical_image_factory.register_optical_image_type(
#     OpticalImageType.DIGITAL_CAMERA_OPTICAL_IMAGE, DigitalCameraOpticalImage)
# optical_image_factory.register_optical_image_type(OpticalImageType.KEYENCE_OPTICAL_IMAGE, KeyenceMicroscopeImage)
# optical_image_factory.register_optical_image_type(
#     OpticalImageType.DIGITAL_CAMERA_OPTICAL_IMAGE_WITH_GPS, DigitalCameraOpticalImageWithGPS)
#
# test_image = r'C:\Users\Antonio\Downloads\PXL.jpg'
# new_image = optical_image_factory.get_optical_image(test_image)
# print(new_image._type)
# # new_image.generate_html_code({})
# # print(new_image.print_html(True))
# # new_image.print_metadata()
# #
# # exif = piexif.load(test_image)
# # autologbook.autotools.pretty_print_dict(exif)
