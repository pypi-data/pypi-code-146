class BasePlatformManager:
    DESCRIPTION_TEMPLATE = "basic.txt"

    def __init__(self, *args, **kwargs):
        super(BasePlatformManager, self).__init__(*args, **kwargs)

    @classmethod
    def get_platform_manager_class(cls, key):
        for platform in cls.__subclasses__():
            if platform.KEY.lower() == key.lower():
                return platform
        return cls
