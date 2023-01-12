from .Encrypt import Encrypt


print('''Thankyou for using our service.\n1.) We request you to not use any symbols as they are out of our range.
2.) If you get 'Error Encrypting' then replace all symbols if used or replace white spaces with underscores ('_').\n\n''')


Encrypt((input("\nEnter your message:\n").strip()), (input('\nEnter your password:\n').strip()),
        (input('\nEnter image address:\n ').strip()))

#Encrypt('My name is Justin', '3020128', 'car.jpg')
