from .setting import setting


def api_keyword_to_url(api_keyword):
    url = setting.HOST_URL + "api/" + api_keyword
    return url
