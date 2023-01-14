import aiohttp

token = ''


class RoleException(BaseException):
    pass


def convert_params(params):
    for param in list(params):
        if params[param] is None:
            params.pop(param)
        elif not isinstance(params[param], (str, int)):
            params[param] = str(params[param])
        elif isinstance(params[param], bool):
            params[param] = str(params[param])
    return params


async def general_request(url, post=False, **params):
    params = convert_params(params)
    timeout = aiohttp.ClientTimeout(total=100, connect=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        res = await session.post(url, data=params) if post else await session.get(url, params=params)
        return await res.json()


async def tg_request(method, post=False, **kwargs):
    return await general_request('https://api.telegram.org/bot{}/{}'.format(token, method), post=post,
                                 **kwargs)
