def infinite_iterator(iterator):
    """Infinite iterator

    :param iterator: iterator
    :type iterator: iterator
    :yield: item from iterator
    :rtype: Any
    """
    while True:
        for item in iterator:
            yield item

            
def property_with_cache(func):
    """Property decorator to cache the result of a property. The result is cached in the attribute of name "_{func.__name__}".

    :param func: function to decorate
    :type func: function
    :return: decorated function
    :rtype: function
    """
    @property
    def decorated_func(self):
        # Get the attribute name
        attr_name = f"_{func.__name__}"
        # Create the attribute if it does not exists
        if not hasattr(self, attr_name) or getattr(self, attr_name) is None:
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)
    return decorated_func
