"myfact module"

def factorial(num):
    """
    Returns the factorial value of the given number.

    :arg num: Interger value of whose factorial we will calculate.

    :return: The value of the the factorial or -1 in case negative value passed.
    """
    if num >= 0:
        if num == 0:
            return 1
        return num * factorial(num -1)
    else:
        return -1