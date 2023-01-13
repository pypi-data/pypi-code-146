"""package code"""

def factorial(number):
    """Factorial Function

    Args:
        x (number): number to find factorial

    Returns:
        number: factorial of given number
    """
    if number == 1:
        return 1
    return number * factorial(number-1)
