class Singleton(type):

    """
        A metaclass whose child classes have a single instance for the same init arguments
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        key = '@'.join([v for _, v in kwargs.items()])
        if  key not in cls._instances:
            cls._instances[key] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[key]