import string
import secrets
 
 
def password_generation(
        adding_digits,
        adding_letters,
        adding_special_characters,
        user_password_length) -> str:
 
    if not any((adding_digits, adding_letters, adding_special_characters)):
        raise Exception("Error!")
 
    generation_string = ""
 
    if adding_digits:
        generation_string += string.digits
 
    if adding_letters:
        generation_string += string.ascii_letters
 
    if adding_special_characters:
        generation_string += string.punctuation
 
    password = ''.join(secrets.choice(generation_string)
                       for i in range(user_password_length))
    return password