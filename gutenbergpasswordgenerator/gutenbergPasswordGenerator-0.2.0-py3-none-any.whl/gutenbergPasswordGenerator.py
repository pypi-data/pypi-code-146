import gutenbergpy.textget
import string
import random


def get_book(BOOK_ID: int) -> bytes:
    """
    gets full text of corresponding value

    Parameters
    ----------
    BOOK_ID
        integer that will correspond to a specific book in the
        Gutenberg Project

    Returns
    -------
    a bytes object that contains the full text of the novel

    Examples
    --------

    get_book()
    default value is 890, will return Edward Gibbon's Decline and Fall of the
    Roman Empire

    get_book(2701)
    returns Moby Dick; Or, The Whale by Herman Melville

    """
    book = gutenbergpy.textget.get_text_by_id(BOOK_ID)
    return book


def clean_book(book: bytes) -> list:
    """
    takes bytes object from get_book function, converts it a list used to
    create password candidates

    Parameters
    ----------
    book
        bytes object created via the get_book function, contains the full
        text of the specified work from the Gutenberg Project

    Returns
    -------
    A setified list object that contains every unique word in the work

    Examples
    --------

    clean_book('Hello World')
    ['Hello','World']

    clean_book('Buffalo buffalo Buffalo buffalo \
        buffalo buffalo Buffalo buffalo')
    ['Buffalo']

    """
    final_book = []
    clean_book = gutenbergpy.textget.strip_headers(book)
    clean_book = clean_book.decode()
    split = clean_book.split()
    final_book = [x.title() for x in split if len(x) >= 4]
    final_book = set(final_book)
    final_book = list(final_book)
    return final_book


def create_candidates(final_book: list, PASSWORD_LENGTH: int) -> list:
    """
    accepts the setified list object from the clean_book function,
    generates 5 candidates that contain 2 numbers and 1 special character

    Parameters
    ----------
    final_book
        setified list object created by the clean_book function

    PASSWORD_LENGTH
        int that specifies the minimum length for password candiates

    Returns
    -------
    a list object of length 5 containing strings of viable password candiates:
        at least PASSWORD_LENGTH in length
        containing both capital and lowercase letters
        containing at least 2 numerical characters
        containing at least 1 special character

    Examples
    --------
    create_candidates()
        ['FinishedEntertained57*', 'WillinglySeekMaster28#', \
            'IncreasedFastingTreasures10&', 'AnnouncingPetulantly53)', \
            'AerialSworeExposition99)']

    """
    NUMBER_OF_PASSWORDS = 5
    password_candidates = []
    numbers = [*range(1, 100)]
    characters = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "?", "/"]
    while len(password_candidates) < NUMBER_OF_PASSWORDS:
        password = ""
        while len(password) < PASSWORD_LENGTH - 3:
            choice = random.choice(final_book)
            valid_word = True
            for character in choice:
                if character in string.ascii_letters:
                    continue
                else:
                    valid_word = False
            if valid_word:
                password += choice
        # selects a random choice from the numbers variable,
        # if it's a single digit, add a leading 0
        digit_choice = random.choice(numbers)
        if digit_choice < 10:
            digit_choice = f"0{digit_choice}"
        password += str(digit_choice)
        # adding a random special character to round out the password
        password += random.choice(characters)
        password_candidates.append(password)
    return password_candidates


def generate_passwords(BOOK_ID=890, PASSWORD_LENGTH=20) -> list:
    """
    wrapper function, incorporates all previous functions to get reasonable output

    Parameters
    ----------
    BOOK_ID
        int that corresponds to a specific Gutenberg project title
            -defaults to Edward Gibbon's Decline and Fall of the Roman Empire

    PASSWORD_LENGTH
        int that specifies the length of the password candidates
            -defaults to 20, selected via trial and error

    Returns
    -------
    a list of 5 password candidate strings:
        at least PASSWORD_LENGTH in length
        containing both capital and lowercase letters
        containing at least 2 numerical characters
        containing at least 1 special character

    Examples
    --------
    create_candidates()
        ['FinishedEntertained57*', 'WillinglySeekMaster28#', \
            'IncreasedFastingTreasures10&', 'AnnouncingPetulantly53)', \
            'AerialSworeExposition99)']
    """
    book = get_book(BOOK_ID)
    final_book = clean_book(book)
    return create_candidates(final_book, PASSWORD_LENGTH)
