def intInput(inp: str) -> int:
    """Loops Until Input Is An Integer

    :param inp: The input to ask the user
    :type inp: str
    :return: The users input as an integer
    :rtype: int
    """
    inp = input(inp)

    while not inp.isdigit():
        inp = input("Please enter a number: ")
    else:
        return int(inp)


def floatInput(inp: str) -> float:
    """Loops Until Input Is A Float or Intiger

    :param inp: The input to ask the user
    :type inp: str
    :return: The users input as a float
    :rtype: float
    """
    inp = input(inp)

    while not inp.replace(".", "").isdigit():
        inp = input("Please enter a number: ")
    else:
        return float(inp)


def puncList(inp: list[str]) -> str:
    """Returns a string of a list with commas and an 'or' before the last item

    :param inp: The list to change
    :type inp: list[str]
    :return: A string of the punctuated list, split over multiple lines.
    :rtype: str
    """
    if len(inp) > 1:
        return f"{', '.join(inp[:-1])} or\n{inp[-1]}"
    else:
        return inp[0]


def loopInput(inp: str, options: list[str]) -> str:
    """Loops until input is in list
    Prints a list of acceptable inputs if one is not entered.

    :param inp: Input to ask the user
    :type inp: str
    :param options: List of acceptable inputs
    :type options: list[str]
    :return: The users input
    :rtype: str
    """
    while True:
        choice = input(inp).lower()
        if choice in options:
            return choice
        else:
            print(
                f"Choice must be: {', '.join(options[:-1])} or {options[-1]}")


def rangeInput(inp: str, minimum: int, maximum: int) -> int:
    """Input that must be between a min and max

    :param inp: Input to ask the user
    :type inp: str
    :param minimum: Minimum value the user must enter
    :type minimum: int
    :param maximum: Maximum value the user must enter
    :type maximum: int
    :return: The number the user entered
    :rtype: int
    """
    number = intInput(inp)
    while number < minimum or number > maximum:
        number = intInput(
            f"Please enter a number between {minimum} and {maximum}: ")
    else:
        return int(number)


def sortObj(objects: list[object], attribute: str, reverse: bool = False):
    """Sorts a list of objects by an attribute

    :param objects: List of objects to sort
    :type objects: list[object]
    :param attribute: Attribute to sort by
    :type attribute: str
    :param reverse: Reverse the sort, defaults to False
    :type reverse: bool, optional

    Modifies provided list
    """
    objects.sort(key=lambda x: getattr(x, attribute), reverse=reverse)


def sortDict(dictionary: dict, reverse: bool = False):
    """Sorts a dictionary by value

    :param dictionary: Dictionary to sort
    :type dictionary: dict
    :param reverse: Reverse the sort, defaults to False
    :type reverse: bool, optional
    :return: Sorted dictionary
    :rtype: dict
    """
    return dict(sorted(dictionary.items(), key=lambda x: x[1], reverse=reverse))


def sortList(list: list, index: int = 0, reverse: bool = False):
    """Sorts a list

    :param list: List to sort
    :type list: list
    :param index: Index of the list item to use for sorting, defaults to 0
    :type index: int, optional
    :param reverse: Reverse the sort, defaults to False
    :type reverse: bool, optional

    Modifies provided list
    """
    list.sort(key=lambda x: x[index], reverse=reverse)


def autoInput(inp: str, choices: list[str], cutoff: int = 3, default: str = "Invalid Input") -> str:
    """Automatically inputs the closest choice to the input

    :param inp: The input to ask the user
    :type inp: str
    :param choices: The list of choices the user can choose from
    :type choices: list[str]
    :param cutoff: The cutoff for the distance between input and choice, defaults to 3
    :type cutoff: int, optional
    :param default: The input to return if the cutoff is met, defaults to "Invalid Input"
    :type default: str, optional
    :return: Users input or the default
    :rtype: str
    """
    # Levenshtein Distance
    inp = input(inp)
    lowest = [default, 0]
    for i in choices:
        if len(i) > lowest[1]:
            lowest[1] = len(i)

    for choice in choices:
        distances = [[0 for _ in range(len(choice) + 1)] for _ in range(len(inp) + 1)]
        for t1 in range(len(inp) + 1):
            distances[t1][0] = t1
        for t2 in range(len(choice) + 1):
            distances[0][t2] = t2

        for t1 in range(1, len(inp) + 1):
            for t2 in range(1, len(choice) + 1):
                if inp[t1-1] == choice[t2-1]:
                    distances[t1][t2] = distances[t1 - 1][t2 - 1]
                else:
                    a = distances[t1][t2 - 1]
                    b = distances[t1 - 1][t2]
                    c = distances[t1 - 1][t2 - 1]

                    if a <= b and a <= c:
                        distances[t1][t2] = a + 1
                    elif b <= a and b <= c:
                        distances[t1][t2] = b + 1
                    else:
                        distances[t1][t2] = c + 1

        distance = distances[len(inp)][len(choice)]

        if distance < lowest[1] and distance <= cutoff:
            lowest[0] = choice
            lowest[1] = distance

    return lowest[0]