import requests

from .network import get_host


_HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': '*',
    'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'Connection': 'keep-alive',
    'sec-ch-dpr': '1',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="103", "Google Chrome";v="103"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"103.0.5060.114"',
    'sec-ch-ua-full-version-list': '".Not/A)Brand";v="99.0.0.0", "Google Chrome";v="103.0.5060.114", "Chromium";v="103.0.5060.114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform-version': '"14.0.0"',
    'sec-ch-ua-wow64': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}


# Response and requests

def get_request_headers(
    url: str,
    add_origin: bool = True,
    referer: str = None,
    **kwargs
):
    """Get requests headers."""

    host = get_host(url)

    headers = {
        **_HEADERS,
        **kwargs
    }

    if add_origin:
        headers['origin'] = host

    if referer:
        headers['referer'] = referer

    return headers


def get_response(
    url: str,
    method: str = 'POST',
    method_data: dict = {},
    cookies: dict = {},
    files: dict = {},
    headers: bool = True,
    extra_headers: dict = {},
    header_add_host: bool = True,
    header_referer: str = None,
    proxies: dict = {},
    max_redirect: int = 5,
    timeout: int = 3,
    verify: bool = True
):
    """Get the request."""

    max_redirect += 1
    redirect_urls = set()

    while max_redirect:
        try:
            kwargs = {
                'url': url,
                'method': method,
                'cookies': cookies,
                'files': files,
                'proxies': proxies,
                'timeout': timeout,
                'allow_redirects': False,
                'verify': verify
            }

            if method.lower() == 'get':
                kwargs['params'] = method_data
            elif method.lower() == 'post':
                kwargs['data'] = method_data

            if headers:
                headers = get_request_headers(
                    url,
                    header_add_host,
                    header_referer
                )

                kwargs['headers'] = {
                    **headers,
                    **extra_headers
                }

            response = requests.request(**kwargs)

            if 300 <= response.status_code <= 310:
                redirect_to = response.headers['location']

                if redirect_to in redirect_urls:
                    break

                url = redirect_to
                redirect_urls.add(url)
                max_redirect -= 1
            else:
                break
        except:
            return None

    return response
