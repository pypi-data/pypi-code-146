'''
Define decorators to be used with any element classes
'''
import logging
import functools

def owner_required(fn):
    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs):
        if self.context == 'owner':
            return fn(self, *args, **kwargs)
        else:
            logging.warning('This function is only permitted in the owner context')
            raise ValueError('This function is only permitted in the owner context')
    return wrapper