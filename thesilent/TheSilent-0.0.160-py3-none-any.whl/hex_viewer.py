from TheSilent.clear import *

import codecs

cyan = "\033[1;36m"

def hex_viewer(file):
    clear()

    count = 0

    my_string = ""
    
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(2), b""):
            try:
                hex_code = codecs.decode(chunk, "hex")
                clean = str(hex_code).replace("b", "")
                clean = clean.replace("'", "")
                clean = clean.replace("\\", "")
                clean = clean.replace("x", "")

                my_string += clean

                count += 1

                if count == 64:
                    print(cyan + my_string)
                    
                    count = 0
                    my_string = ""
                    
            except:
                pass

    print(cyan + "\ndone")
