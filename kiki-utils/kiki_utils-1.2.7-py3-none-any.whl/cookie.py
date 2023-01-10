from http.cookies import SimpleCookie


def read_raw_cookie(cookie_str: str):
    cookies = SimpleCookie()
    cookies.load(cookie_str)
    return {k: v.value for k, v in cookies.items()}
