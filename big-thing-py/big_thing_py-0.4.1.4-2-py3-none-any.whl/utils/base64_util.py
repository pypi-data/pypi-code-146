import base64


def string_to_base64(string: str):
    return base64.b64encode(string.encode('utf-8')).decode('utf-8')


def base64_to_string(base64_string: str):
    return base64.b64decode(base64_string).decode('utf-8')


if __name__ == '__main__':
    print(string_to_base64('100'))
