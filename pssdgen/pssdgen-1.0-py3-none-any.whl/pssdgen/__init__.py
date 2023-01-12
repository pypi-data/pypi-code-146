import random


def none_():
    final_password = None
    print(final_password)
    exit()


def password_generation(
        adding_a_digit,
        adding_letters,
        adding_special_characters,
        user_password_length):
    try:
        if adding_a_digit == 1 or adding_a_digit == 2 and adding_letters == 1 or adding_letters == 2 or adding_special_characters == 1 or adding_special_characters == 2:
            if user_password_length > 30:
                user_password_length = 30
            if user_password_length < 6:
                user_password_length = 6

            final_password = ""
            resultat_all = ""

            if adding_a_digit == 1:
                resultat_all += "1234567890"

            elif adding_a_digit == 2:
                pass

            else:
                none_()

            if adding_letters == 1:
                resultat_all += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

            elif adding_letters == 2:
                pass

            else:
                none_()

            if adding_special_characters == 1:
                resultat_all += "!@#$%^&*()_'\\|?.,"

            elif adding_special_characters == 2:
                pass

            else:
                none_()
            additional_choice = ""

            N = 30  # ПРОГОНИМИМ НАШ resultat_all перед основным выбором
            while N != 0:
                additional_choice += random.choice(resultat_all)
                N -= 1

            while user_password_length != 0:  # ЦИКЛ ОКОНЧАТЕЛЬНОГО ВЫБОРА
                final_password += random.choice(additional_choice)

                user_password_length -= 1
            print(final_password)

    except BaseException:
        none_()
