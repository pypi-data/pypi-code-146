def is_prime(n) -> bool:
    """
    Check if a number is prime
    :param n: number to check
    :type n: int
    :return: True if prime, False otherwise
    :rtype: bool
    """

    if n < 2:
        return False

    if n in [2, 3]:
        return True

    if n % 2 == 0 or n % 3 == 0:
        return False

    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6

    return True