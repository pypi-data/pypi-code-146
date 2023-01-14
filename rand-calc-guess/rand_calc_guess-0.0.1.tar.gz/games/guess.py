import random

def guess_num():
    name = input("Your name : ")
    print("Hi! ", name, " please guess a number between 0 to 10 in 3 attempts")

    number = random.randint(0, 10)
    attempts = 3

    while attempts:
        num = int(input())
        if num == number:
            print("Hurray! You have guessed the right number")
            break
        if num >= 5:
            print("Your guess is too high")
        if num < 5:
            print("Your guess is too low")
        attempts -= 1

    if num != number:
        print("\nOh no! You couldn't guess the right answer")
        print("The answer was ", number)

