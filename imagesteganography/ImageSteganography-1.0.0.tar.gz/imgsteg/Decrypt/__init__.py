from .Decrypt import Decrypt
import time



print(f'''If you encounter any 'Error decrypting' or is your "Shared Key" is less than {22**2} or greater than {99**2} you might get a wrong message.
In such case ask the sender to replace white spaces with underscores or ask them not to use any symbols''')


Decrypt(input('\nEnter image address:\n'), input('Enter your password:\n'), input('Enter your security key:\n'))
time.sleep(5)

#Decrypt('Decrypt\\finally_done.png', '3020128', '1024')#
