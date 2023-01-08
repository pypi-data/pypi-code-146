from dataclasses import dataclass


@dataclass(init=False)
class Result:
    body: any

    def __init__(self, **kwargs):
        self.body = kwargs

    def __getattr__(self, name):
        return self.body.get(name)
    
    def with_attributes(self, **kwargs):
        return self.__class__(**{**self.body, **kwargs})


class Success(Result):
    def is_success(self):
        return True

    def is_failure(self):
        return False

    def map(self, f):
        return f(self)

    def do(self, f):
        f(self)
        return self

    def prefix_error(self, prefix):
        return self

    def or_fail_with(self, **kwargs):
        return self


class Failure(Result):
    def is_success(self):
        return False

    def is_failure(self):
        return True

    def map(self, f):
        return self

    def prefix_error(self, prefix):
        return Failure(message=prefix + self.message)

    def do(self, f):
        return self

    def or_fail_with(self, **kwargs):
        return Failure(**dict(reason=self), **kwargs)


class PartialSuccess(Result):
    def is_success(self):
        return False

    def is_failure(self):
        return True

    def map(self, f):
        return PartialSuccess(**{**self.body, **f(self).body})

    def do(self, f):
        f(self)
        return self

    def or_fail_with(self, **kwargs):
        return self
