"""Get/set EXIF dates from photos"""
import struct

import piexif


def get_photo_exif(fpath: str):
    """Get EXIF date for a photo, return nothing if there is an error"""
    try:
        return piexif.load(fpath).get("Exif", {}).get(36867)
    except struct.error:
        pass
    return None


def set_photo_exif(fpath: str, date_str: str):
    """Set EXIF date on a photo"""
    exif_dict = piexif.load(fpath)
    exif_dict.get("1st")[306] = date_str
    exif_dict.get("Exif")[36867] = date_str
    exif_dict.get("Exif")[36868] = date_str
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, fpath)
