def command(name, aliases=None, usage=None, description=None, roles=None, ignore_filter=False,has_arts=False):
    def decorator(func):
        setattr(func, '__command__', name)
        setattr(func, '__ignore_filter__', ignore_filter)
        setattr(func,'has_arts',has_arts)
        if description:
            setattr(func, 'description', description)
        if aliases:
            setattr(func, 'aliases', aliases)
        if usage:
            setattr(func, 'usage', usage)
        if roles is []:
            setattr(func, 'roles', [])
        elif roles is not None:
            setattr(func,'roles',roles)


        return func

    return decorator


def listener(ignore_filter=False):
    def decorator(func):
        setattr(func, '__listener__', func.__name__)
        setattr(func, '__ignore_filter__', ignore_filter)
        return func

    return decorator


class Cog:
    def __init__(self, bot):
        self.bot = bot
