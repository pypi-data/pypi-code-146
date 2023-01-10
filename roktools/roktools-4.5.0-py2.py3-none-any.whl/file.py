

def grep_lines(filename:str, pattern_string: str):
    """
    Generator function used to grep lines from a file. Can be used in methods
    such as numpy.genfromtxt, ...

    >>> generator = grep_lines(filename, "pattern")
    >>> data = numpy.loadtxt(generator)
    """

    with open(filename, 'r') as fh:
        for line in fh:
            if pattern_string in line:
                yield line