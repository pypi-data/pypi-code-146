"""Faker Utils"""
import inspect
import secrets
import logging
from faker import Faker

fake = Faker('en_US')


def get_callable_method_names() -> list[str]:
    """Returns all the available methods from faker object"""

    # exceptional methods are non-callable methods or required some params
    exceptional_list = ['cache_pattern', 'factories', 'generator_attrs',
                        'seed', 'locales', 'providers', 'random',
                        'unique', 'weights']
    # filtering methods
    methods = [obj for obj in dir(fake)
               if not obj.startswith('__') and not obj.startswith('_')]
    filtered_list = [x for x in methods if x not in exceptional_list]
    callable_methods_names = []

    # checking if there are any positional params required
    for method in filtered_list:
        try:
            method_to_call = getattr(fake, method)
            sig = inspect.signature(method_to_call)
            if not sig.parameters:
                callable_methods_names.append(method)
        except AttributeError as attribute_error:
            logging.error('Error getting method %s: %s', method, attribute_error)
        # except Exception as error:
        #     logging.error('Error getting method %s: %s', method, error)
    return callable_methods_names


def random_faker_method():
    """Random function from faker"""
    methods = get_callable_method_names()
    method = secrets.choice(methods)
    return method


def callable_methods(methods):
    """returns list of callable faker methods from method names"""
    call_methods = []
    for method in methods:
        method_to_call = getattr(fake, method)
        call_methods.append(method_to_call())
    return call_methods
