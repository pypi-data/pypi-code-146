from datetime import datetime


def strtime(dt=None):
    """ Returns time stamp formatted as follows::

        %Y%m%d_%H%M%S

        So all backups and files that require this in the name will have the same format,
        if changes will be in one place, here.
    :parameter dt: a datetime object to be converted to the default format
    :return: Formatted timestamp
    """
    format = "%Y%m%d_%H%M%S"
    if dt is None:
        return datetime.now().strftime(format)
    return dt.strftime(format)
