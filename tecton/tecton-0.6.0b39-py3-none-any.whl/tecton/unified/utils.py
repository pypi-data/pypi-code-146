from functools import wraps

from tecton import conf
from tecton._internals import errors
from tecton.unified import common
from tecton.unified import validations_api


def requires_validation(func):
    """Check if the object has been validated, if not validate the object."""

    @wraps(func)
    def wrapper(fco_object: common.BaseTectonObject, *args, **kwargs):
        if fco_object._is_valid:
            return func(fco_object, *args, **kwargs)

        # Object has not already been validated.
        if conf.get_or_none("TECTON_VALIDATION_MODE") == validations_api.ValidationMode.AUTOMATIC:
            print("Automatic validation mode is enabled. Starting validation...")
            fco_object.validate()
            if not fco_object._is_valid:
                raise errors.AUTOMATIC_VALIDATION_FAILED(func.__name__, type(fco_object).__name__)
        else:
            raise errors.TECTON_OBJECT_REQUIRES_VALIDATION(func.__name__, type(fco_object).__name__)

        return func(fco_object, *args, **kwargs)

    return wrapper


def requires_remote_object(func):
    """Assert this function is being called on a remote Tecton object, aka an object applied and fetched from the backend, and raise error otherwise."""

    @wraps(func)
    def wrapper(fco_object: common.BaseTectonObject, *args, **kwargs):
        if fco_object._spec is None or fco_object._spec.is_local_object:
            raise errors.INVALID_USAGE_FOR_LOCAL_TECTON_OBJECT(func.__name__)
        return func(fco_object, *args, **kwargs)

    return wrapper
