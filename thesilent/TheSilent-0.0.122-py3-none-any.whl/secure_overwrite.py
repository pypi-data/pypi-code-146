from TheSilent.clear import *

import binascii

cyan = "\033[1;36m"

#securely destroys data
def secure_overwrite(file):
    clear()

    result = ""
    last_result = ""
    
    progress = 0

    print(cyan + "preparing")
    
    try:
        with open(file, "rb") as f:
            storage = f.seek(0, 2)

    except PermissionError:
        print(cyan + "ERROR! Permission denied!")
        exit()

    gb = math.floor(storage / 1000000000)

    for i in range(0, 20000000):
        result += "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"

    for i in range(0, storage % 2000000000):
        last_result += "00"

    result = binascii.unhexlify(result)
    last_result = binascii.unhexlify(last_result)
    jk_last_result = binascii.unhexlify("00")

    for i in range(1, 8):
        tracker = 0
        
        try:
            for ii in range(0, gb):
                clear()
                print(cyan + "pass: " + str(i))
                print(cyan + "gb: " + str(ii))

                with open(file, "wb+") as f:
                    f.seek(tracker) 
                    f.write(result)
                    tracker += 1000000000
            
        except OSError:
            continue

        try:
            clear()
            print(cyan + "pass: " + str(i))
            print(cyan + "gb: " + str(gb))

            with open(file, "wb+") as f:
                f.seek(tracker) 
                f.write(last_result)
                tracker += len(last_result)

        except OSError:
            continue

        try:
            with open(file, "wb+") as f:
                f.seek(tracker) 
                f.write(jk_last_result)
                tracker += 2

        except OSError:
            continue

    clear()
    print(cyan + file)
    print(cyan + "done")
