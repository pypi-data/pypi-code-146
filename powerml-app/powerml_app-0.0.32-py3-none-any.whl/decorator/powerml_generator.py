import functools


def powerml_generator(func):
    @functools.wraps(func)
    def wrapper():
        result: list = func()
        # Type checking
        if type(result) != list:
            raise Exception(
                f"Return Value of {func.__name__} is improperly formatted. It should be a list")
        for return_value in result:
            if type(return_value) == str:
                continue
            if 'model_input' in return_value or 'model_output' in return_value:
                continue
            raise Exception(
                f"Return Value of {func.__name__} is improperly formatted. It should be a list of strings or dictionaries with keys 'model_input' and 'model_output'")
        return result
    wrapper.is_generator_function = True
    return wrapper
