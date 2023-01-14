from random import randint

def play_coin_game():
    user_val = int(input("Bet: 0 -> Kok | 1 -> Pil user imput: "))
    pc_val = randint(0,1)

    if user_val == pc_val:
        print('You Win!!')
    else:
        print('You Lose!!')