import functools
import logging

logger = logging.getLogger(__name__)


def powerml_filter(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Load Data to be filtered
        data_to_filter = kwargs['data']
        passing_data = []
        # pass data into filter function
        for datapoint in data_to_filter:
            result = func(
                model_input=datapoint["model_input"], model_output=datapoint["model_output"])
            if result:
                passing_data.append(datapoint)
        return passing_data
    wrapper.is_filter_function = True
    return wrapper
