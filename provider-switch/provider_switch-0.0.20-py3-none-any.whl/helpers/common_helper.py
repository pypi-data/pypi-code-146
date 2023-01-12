from urllib.parse import urlparse


class CommonHelper(object):
    @staticmethod
    def get_attr(obj, attr: str, default: str = None):
        if type(obj) is dict:
            if hasattr(obj, attr):
                return getattr(obj, attr)

        if type(obj) is list:
            if attr in obj:
                return obj[attr]

        return default

    @staticmethod
    def is_url(string):
        try:
            result = urlparse(string)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    @staticmethod
    def format_data(data, format):
        if not data:
            return None

        if isinstance(data, str):
            for key, value in format.items():
                if value is not None:
                    data = data.replace(f'{{{key}}}', str(value))
            return data
        elif isinstance(data, dict):
            for key, value in data.items():
                data[key] = CommonHelper.format_data(value, format)

            return data
