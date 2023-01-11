import gutenbergpy.textget
import string
import random


def get_book(BOOK_ID: int) -> bytes:
    """accepts one integer parameter, BOOK_ID, gets the full text of the
    corresponding novel"""
    book = gutenbergpy.textget.get_text_by_id(BOOK_ID)
    return book


def clean_book(book: bytes) -> list:
    """takes full text of the novel, converts it to a word dictionary used to
    create passwords"""
    final_book = []
    clean_book = gutenbergpy.textget.strip_headers(book)
    clean_book = clean_book.decode()
    split = clean_book.split()
    final_book = [x.title() for x in split if len(x) >= 4]
    final_book = set(final_book)
    final_book = list(final_book)
    return final_book


def create_candidates(final_book: list, PASSWORD_LENGTH: int) -> list:
    """takes a cleaned list of words from a classic novel, generates a series
    of password candidates that meet the specifications,
    length is at least PASSWORD_LENGTH, contains 2 numerical digits
    and one special character"""
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
    """default BOOK_ID is keyed to Edward Gibbon's
    Decline and Fall of the Roman Empire, PASSWORD_LENGTH was chosen by trial
    and error"""
    book = get_book(BOOK_ID)
    final_book = clean_book(book)
    return create_candidates(final_book, PASSWORD_LENGTH)
