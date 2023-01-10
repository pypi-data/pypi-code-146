import base64
import configparser
import io

from itsimodels.core.base_models import KEY_FIELD_NAME


def to_conf(model):
    config = configparser.ConfigParser(
        allow_no_value=True,
        interpolation=None
    )
    config.optionxform = str

    key = model.get_key()

    model_data = model.to_dict()

    # Remove the key fields from the data before converting into conf format
    model_data.pop(KEY_FIELD_NAME, None)

    key_field = getattr(model.__class__, KEY_FIELD_NAME)
    if key_field and key_field.alias:
        model_data.pop(key_field.alias, None)

    config_data = {
        key: model_data
    }
    config.read_dict(config_data)

    fobj = io.StringIO()
    config.write(fobj)
    fobj.seek(0)

    return fobj.read()


IMAGE_MIMETYPE_TO_EXT = {
    'image/x-ms-bmp': 'bmp',
    'image/gif': 'gif',
    'image/vnd.microsoft.icon': 'ico',
    'image/ief': 'ief',
    'image/jpeg': 'jpeg',
    'image/x-portable-bitmap': 'pbm',
    'image/x-portable-graymap': 'pgm',
    'image/png': 'png',
    'image/x-portable-anymap': 'pnm',
    'image/x-portable-pixmap': 'ppm',
    'image/x-cmu-raster': 'ras',
    'image/x-rgb': 'rgb',
    'image/svg+xml': 'svg',
    'image/tiff': 'tiff',
    'image/x-xbitmap': 'xbm',
    'image/x-xpixmap': 'xpm',
    'image/x-xwindowdump': 'xwd'
}


def to_image(model):
    data_parts = model.data.split(',')
    if not data_parts:
        return ''

    data_str = data_parts[0] if len(data_parts) == 1 else data_parts[1]
    data = base64.b64decode(data_str)

    return data


def image_file_extension(model):
    return IMAGE_MIMETYPE_TO_EXT[model.type]
