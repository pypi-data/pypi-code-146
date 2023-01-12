class BaseSwitcherException(Exception):
    def __init__(self, **kwargs):
        self.name = self.__class__.__name__
        self.message = kwargs.get('message', self.name)
        self.status = kwargs.get('status', 0)
        self.http_status_code = kwargs.get('http_status_code', 500)
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'


class BadRequestException(BaseSwitcherException):
    def __init__(self, **kwargs):
        self.retry = kwargs.get('retry', False)
        super().__init__(**kwargs)

    def must_retry(self):
        return self.retry


class BadProviderException(BaseSwitcherException):
    def __init__(self, **kwargs):
        self.switch_provider = kwargs.get('switch_provider', False)
        super().__init__(**kwargs)

    def must_switch_provider(self):
        return self.switch_provider


class ExitException(BaseSwitcherException):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ValidationResponseException(BaseSwitcherException):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.validation = kwargs.get('key', {})
        self.message = f"{self.name}: key `{str(self.validation)}`"


class ResponseNotFoundException(BaseSwitcherException):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.validation = kwargs.get('key', {})
        self.message = f"{self.name}: key `{str(self.validation)}`"
