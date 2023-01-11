from TheSilent.clear import *

red = "\033[1;31m"

#attempts to view source code of file
def source_code_viewer(file, keyword = ""):
    clear()

    count = 0
    
    with open(file, "rb") as f:
        for i in f:
            hex_code = str(i).replace("b'", "")
            hex_code = str(hex_code).replace("'", "")
            hex_code = str(hex_code).replace("b\"", "")
            hex_code = str(hex_code).replace("\"", "")
            hex_code = str(hex_code).replace("\\x", "")

            result = str(i, "ascii", errors = "replace")

            if keyword in result or keyword in hex_code:
                print(red + result)
                print(red + hex_code)

                count += 1

                if count == 128:
                    count = 0
                    pause = input()

    print(red + "\ndone")
