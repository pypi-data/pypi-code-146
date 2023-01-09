def main():
    global random
    import random
    introdcution=intro()
    while True:
        inputs=choice()
        result=decision()
        print("Do you wanna play again? (Y/N)")
        ans = input().upper()
        if ans == 'Y':
            print('\n')
            continue
        else:
            print('\nHad fun playing with you')
            print('Dust me up, when you get bored')
            break

def intro():
    print("Winning Rules of the Rock Paper Scissor game as follows: \n"+ "Rock  vs Paper     -> Paper wins \n"+ 
    "Rock  vs Scissor   -> Rock wins \n"+ "Paper vs Scissor   -> Scissor wins \n")
    global Dict
    Dict={1:'Rock',2:'Paper',3:'Scissor'}     

def choice():
    print("Entry choice \n 1 for Rock, \n 2 for Paper and \n 3 for Scissor \n")
    
    global user
    user= int(input("Your choice: "))

    while user > 3 or user < 1:
        user= int(input("enter valid input: "))

    print("Your choice is: " + Dict[user])
    print("\nNow its my turn.......")
    global comp
    comp= random.randint(1, 3)
    
    while comp == user:
        comp = random.randint(1, 3)
    
    print("Comp choice is: " + Dict[comp]+'\n')
    
    print(Dict[user] + " V/s " + Dict[comp])
           

def decision():      
    if((user == 1 and comp == 2) or (user == 2 and comp == 1)):
        result = "Paper"
        print("Paper wins", end="\n")
    elif((user == 1 and comp == 3) or (user == 3 and comp == 1)):
        result = "Rock"
        print("Rock wins", end="\n")
    else:
        result = "Scissor"
        print("Scissor wins", end="\n")

    if result == Dict[user]:
        print("<== You win ==>")
    else:
        print("<== Comp win ==>")
        



