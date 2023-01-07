""" Flask Restful Instance Wrapper
"""


def restful_api_route(self, *args, **kwargs):
    """ Function to allow a flask restul instance to add routes using a
        decorator
    """

    def wrapper(cls):
        self.add_resource(cls, *args, **kwargs)
        return cls

    return wrapper
