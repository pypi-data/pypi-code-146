import os
from datetime import datetime
from time import time


def now(fmt='%Y-%m-%d %H:%M:%S'):
    """
    Return the current timestamp formatted with a specific format.

    @return: now datetime string
    """

    return datetime.now().strftime(fmt)


def get_slug(name):
    """
    Get the name e returns the slug.

    @param name: object name string
    @return: slug string
    """

    return name.lower().replace(' ', '_')


def get_parameters(storage_manager, parameters):
    """
    Get the input dictionary and take a particular action for each type of input.
    @param storage_manager: manager of the storage, used to handle the load and save of the files
    @param parameters: input dictionary that contains the list of input to be returned in a proper way
    @return: returns the list of input opportunely processed
    """

    # Initialize the list of parameters
    params_list = []

    # For each parameter provided by the user, the component puts in the params list or load it from the
    # storage
    for param in parameters:

        # Type of the input
        type = param['type']

        # Value of the input
        value = param['value']

        # Additional parameters expressed by the user
        additional_params = param['params'] if 'params' in param else {}

        try:
            # File case
            if type == 'file':

                # If the path is expressed as a list, it is converted into a string
                if isinstance(value, list):
                    value = os.path.join(*value)

                params_list.append(storage_manager.get_file(filename=value, params=additional_params))

            # Folder case
            elif type == 'folder':

                params_list.append(storage_manager.get_folder_files(folder_name=value, params=additional_params))

            # Query case
            elif type == 'query':

                params_list.append(storage_manager.fetch_query(query=value, params=additional_params))

            # All other cases: for example a string or and integer value
            else:
                params_list.append(value)

        # Exception in the case of file not found error
        except FileNotFoundError as e:
            raise Exception(
                f"Failed to load parameter with type '{type}' - '{value}'. Exception message: File not found in the "
                f"specified path.", exc_info=e)

        # Generic exception: in the future more specific cases could be handled
        except Exception as e:
            raise Exception(f"Failed to load parameter with type '{type}' - '{value}'. Exception message: {e}", exc_info=e)

    # Return the list of parameters
    return params_list


def get_time():
    # Get current timestamp
    n = time()

    return n


def elapsed(t1):
    # Compute the difference
    delta = int(get_time() - t1)

    # Seconds
    if delta < 60:
        return f"{delta} sec"

    # Minutes, seconds
    elif delta < 3600:
        minutes = int(delta / 60)
        seconds = delta - (minutes * 60)
        return f"{minutes} min {delta} sec"

    # Hours, minutes, seconds
    elif delta < (3600 * 24):
        hours = int(delta / 3600)
        minutes = int((delta - (hours * 3600)) / 60)
        seconds = delta - (minutes * 60) - (hours * 3600)
        return f"{hours} hours {minutes} min {delta} sec"

    # Days, Hours, minutes, seconds
    elif delta >= (3600 * 24):
        days = int(delta / (3600*24))
        hours = int((delta - (days * 24 * 3600)) / 3600)
        minutes = int((delta - (hours * 3600) - (days * 24 * 3600)) / 60)
        seconds = delta - (minutes * 60) - (hours * 3600) - (days * 24 * 3600)
        return f"{days} days {hours} hours {minutes} min {delta} sec"

    else:
        return f"{delta} sec"
