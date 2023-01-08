"""
This Program is for getting os info and making commands,

if you make a terminal, you can use this for getting the ip,
and other useful things, so the output can look like this: user@ip
"""
#imports:
import time, os, socket
from styles import Style



#extras:
#current user
def currentUserInfo():
    """
    This will return the current user of this computer
    this is used in some of the osInfo functions

    [0] is for username
    [1] is for ip
    """
    #yes this is so easy
    current_User = os.getlogin()
    current_ip = socket.gethostbyname(socket.gethostname())
    return current_User, current_ip



#this will make a linux looking user line: <user>@<ip>
def simpleLinuxUser(user=str("")):
    """
    This this make a simple user and ip output,

    user:      the users name

    if "user" is left empty, this will use the windows logged in user
    otherwise "user" is what you gona see before ip: <user>@<ip>
    ip can't get changed, it will always what the pc have

    this also will give a <user> a bold font style,
    and <@ip> a cyan font style from styles.Style
    also ending on the same line, and with default color
    """
    if user == "":
        user = currentUserInfo()[0]
    
    ip = currentUserInfo()[1]
    print(Style.Colors["BOLD"] + user + Style.Colors["CYAN"] + f"@{ip}:", Style.Colors["ENDC"] + " ", sep="", end="")


#this will make a linux looking user line: <user>@<ip>\n
def simpleLinuxUserNL(user=str(""), newLine=int(1)):
    """
    This is just like "simpleLinuxUser" but NL is for newLine

    user:     user name, or what user is logged in
    newLine:  How many times this will make a new line after user details

    this might give an error if you just do: simpleLinuxUserNL(5)
    you need to do: simpleLinuxUserNL(newLine=5)

    this will make a output looking like this:  <user>@<ip> :and end with
    newLineCommand * newLine number

    in this you can only change user and new line
    """
    if user == "":
        user = currentUserInfo()[0]
    
    ip = currentUserInfo()[1]
    nl = ""
    for x in range(newLine):
        nl = nl + "\n"

    print(Style.Colors["BOLD"] + user + Style.Colors["CYAN"] + f"@{ip}:", Style.Colors["ENDC"] + " ", end=nl)