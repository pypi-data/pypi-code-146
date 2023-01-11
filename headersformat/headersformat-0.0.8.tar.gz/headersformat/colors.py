import sys
import os
import platform

colors = True  # Output should be colored
machine = sys.platform  # Detecting the os of current system
checkplatform = platform.platform() # Get current version of OS

if machine.lower().startswith(('os', 'win', 'darwin', 'ios')):
    colors = False  # Colors shouldn't be displayed on mac & windows
if checkplatform.startswith("Windows-10") and int(platform.version().split(".")[2]) >= 10586:
    colors = True
    os.system('')   # Enables the ANSI
if not colors:
    end = red = white = green = yellow = run = bad = good = info = que = ''
else:
    white = '\033[97m'
    green = '\033[92m'
    red = '\033[91m'
    yellow = '\033[93m'
    end = '\033[0m'
    back = '\033[7;91m' #背景红
    info = '\033[93m[!]\033[0m' #[!]
    que = '\033[94m[?]\033[0m'#[?]
    bad = '\033[91m[-]\033[0m'#[-]
    good = '\033[92m[+]\033[0m'#[+]
    run = '\033[97m[~]\033[0m'#[~]
if __name__ == '__main__':
    s = """
        __                   __                  ____                           __
       / /_  ___  ____ _____/ /__  __________   / __/___  _________ ___  ____ _/ /_
      / __ \/ _ \/ __ `/ __  / _ \/ ___/ ___/  / /_/ __ \/ ___/ __ `__ \/ __ `/ __/
     / / / /  __/ /_/ / /_/ /  __/ /  (__  )  / __/ /_/ / /  / / / / / / /_/ / /_
    /_/ /_/\___/\__,_/\__,_/\___/_/  /____/  /_/  \____/_/  /_/ /_/ /_/\__,_/\__/
    """
    print(f'''{red}{s}''')
    print(f'''{white}我是白，{green}我是绿,{red}我是红，{yellow}我是黄，{back}我是黑，{info}info，{que}que{bad}bad{good}good{run}run''')
    print('''%s\tXSStrike %sv3.1.5%s''' % (red, white, end))

