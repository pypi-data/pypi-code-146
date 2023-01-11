from TheSilent.clear import *

import itertools

cyan = "\033[1;36m"

#brute force hash using dictionary method
def dictionary_hash(my_file, my_hash = " ", hash_list = " ", mask = False, minimum = 1, maximum = 10):
    clear()

    my_hash = my_hash.lower()

    dictionary = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ "

    hashes = {"blake2b" : 128, "blake2s" : 64, "md5" : 32, "sha1" : 40, "sha224" : 56, "sha256" : 64, "sha512" : 128, "sha3_256" : 64, "sha3_384" : 96, "sha3_512" : 128}

    blake2b = ""
    blake2s = ""
    md5 = ""
    sha1 = ""
    sha224 = ""
    sha256 = ""
    sha512 = ""
    sha3256 = ""
    sha3384 = ""
    sha3512 = ""

    crack_boolean = False
    my_hash_list = []
    password_list = []
    word_list = []

    print(cyan + "cracking hash")

    if hash_list == " " and my_hash != " ":
        with open(my_file, "r", errors = "ignore") as file:
            for i in file:
                clean = i.replace("\n", "")
                word_list.append(clean)

        if mask == False:
            for i in range (minimum, maximum + 1):
                if crack_boolean == True:
                    break
                
                print(cyan + "attempting length: " + str(i))

                for ii in itertools.product(word_list, repeat = i):
                    compute = "".join(ii)

                    if len(my_hash) == 32:
                        md5 = hashlib.md5(compute.encode("utf8")).hexdigest()

                    if len(my_hash) == 40:
                        sha1 = hashlib.sha1(compute.encode("utf8")).hexdigest()

                    if len(my_hash) == 56:
                        sha224 = hashlib.sha224(compute.encode("utf8")).hexdigest()

                    if len(my_hash) == 64:
                        blake2s = hashlib.blake2s(compute.encode("utf8")).hexdigest()
                        sha256 = hashlib.sha256(compute.encode("utf8")).hexdigest()
                        sha3256 = hashlib.sha3_256(compute.encode("utf8")).hexdigest()

                    if len(my_hash) == 96:
                        sha3384 = hashlib.sha3_384(compute.encode("utf8")).hexdigest()

                    if len(my_hash) == 128:
                        blake2b = hashlib.blake2b(compute.encode("utf8")).hexdigest()
                        sha512 = hashlib.sha512(compute.encode("utf8")).hexdigest()
                        sha3512 = hashlib.sha3_512(compute.encode("utf8")).hexdigest()

                    if str(blake2b) == my_hash:
                        crack_boolean = True
                        print(cyan + "password: " + str(compute))
                        break

                    if str(blake2s) == my_hash:
                        crack_boolean = True
                        print(cyan + "password: " + str(compute))
                        break

                    if str(md5) == my_hash:
                        crack_boolean = True
                        print(cyan + "password: " + str(compute))
                        break

                    if str(sha1) == my_hash:
                        crack_boolean = True
                        print(cyan + "password: " + str(compute))
                        break

                    if str(sha224) == my_hash:
                        crack_boolean = True
                        print(cyan + "password: " + str(compute))
                        break

                    if str(sha256) == my_hash:
                        crack_boolean = True
                        print(cyan + "password: " + str(compute))
                        break

                    if str(sha512) == my_hash:
                        crack_boolean = True
                        print(cyan + "password: " + str(compute))
                        break

                    if str(sha3256) == my_hash:
                        crack_boolean = True
                        print(cyan + "password: " + str(compute))
                        break

                    if str(sha3384) == my_hash:
                        crack_boolean = True
                        print(cyan + "password: " + str(compute))
                        break

                    if str(sha3512) == my_hash:
                        crack_boolean = True
                        print(cyan + "password: " + str(compute))
                        break

        if mask == True:
            for i in range (minimum, maximum + 1):
                if crack_boolean == True:
                    break

                print(cyan + "attempting length: " + str(i))

                for words in word_list:
                    if crack_boolean == True:
                        break

                    print("checking: " + words)

                    for ii in itertools.product(dictionary, repeat = i):
                        var = "".join(ii)
                        compute = words + var

                        if len(my_hash) == 32:
                            md5 = hashlib.md5(compute.encode("utf8")).hexdigest()

                        if len(my_hash) == 40:
                            sha1 = hashlib.sha1(compute.encode("utf8")).hexdigest()

                        if len(my_hash) == 56:
                            sha224 = hashlib.sha224(compute.encode("utf8")).hexdigest()

                        if len(my_hash) == 64:
                            blake2s = hashlib.blake2s(compute.encode("utf8")).hexdigest()
                            sha256 = hashlib.sha256(compute.encode("utf8")).hexdigest()
                            sha3256 = hashlib.sha3_256(compute.encode("utf8")).hexdigest()

                        if len(my_hash) == 96:
                            sha3384 = hashlib.sha3_384(compute.encode("utf8")).hexdigest()

                        if len(my_hash) == 128:
                            blake2b = hashlib.blake2b(compute.encode("utf8")).hexdigest()
                            sha512 = hashlib.sha512(compute.encode("utf8")).hexdigest()
                            sha3512 = hashlib.sha3_512(compute.encode("utf8")).hexdigest()

                        if str(blake2b) == my_hash:
                            crack_boolean = True
                            print(cyan + "password: " + str(compute))
                            break

                        if str(blake2s) == my_hash:
                            crack_boolean = True
                            print(cyan + "password: " + str(compute))
                            break

                        if str(md5) == my_hash:
                            crack_boolean = True
                            print(cyan + "password: " + str(compute))
                            break

                        if str(sha1) == my_hash:
                            crack_boolean = True
                            print(cyan + "password: " + str(compute))
                            break

                        if str(sha224) == my_hash:
                            crack_boolean = True
                            print(cyan + "password: " + str(compute))
                            break

                        if str(sha256) == my_hash:
                            crack_boolean = True
                            print(cyan + "password: " + str(compute))
                            break

                        if str(sha512) == my_hash:
                            crack_boolean = True
                            print(cyan + "password: " + str(compute))
                            break

                        if str(sha3256) == my_hash:
                            crack_boolean = True
                            print(cyan + "password: " + str(compute))
                            break

                        if str(sha3384) == my_hash:
                            crack_boolean = True
                            print(cyan + "password: " + str(compute))
                            break

                        if str(sha3512) == my_hash:
                            crack_boolean = True
                            print(cyan + "password: " + str(compute))
                            break

    if hash_list != " " and my_hash == " ":
        with open(hash_list, "r", errors = "ignore") as file:
            for i in file:
                clean = i.replace("\n", "")
                my_hash_list.append(clean)

        with open(my_file, "r", errors = "ignore") as file:
            for i in file:
                clean = i.replace("\n", "")
                word_list.append(clean)

        for my_hash in my_hash_list:   
            my_hash = my_hash.lower()

            if mask == False:
                for i in range (minimum, maximum + 1):
                    if crack_boolean == True:
                        crack_boolean = False
                        break
                    
                    print(cyan + "attempting length: " + str(i))

                    for ii in itertools.product(word_list, repeat = i):
                        compute = "".join(ii)

                        if len(my_hash) == 32:
                            md5 = hashlib.md5(compute.encode("utf8")).hexdigest()

                        if len(my_hash) == 40:
                            sha1 = hashlib.sha1(compute.encode("utf8")).hexdigest()

                        if len(my_hash) == 56:
                            sha224 = hashlib.sha224(compute.encode("utf8")).hexdigest()

                        if len(my_hash) == 64:
                            blake2s = hashlib.blake2s(compute.encode("utf8")).hexdigest()
                            sha256 = hashlib.sha256(compute.encode("utf8")).hexdigest()
                            sha3256 = hashlib.sha3_256(compute.encode("utf8")).hexdigest()

                        if len(my_hash) == 96:
                            sha3384 = hashlib.sha3_384(compute.encode("utf8")).hexdigest()

                        if len(my_hash) == 128:
                            blake2b = hashlib.blake2b(compute.encode("utf8")).hexdigest()
                            sha512 = hashlib.sha512(compute.encode("utf8")).hexdigest()
                            sha3512 = hashlib.sha3_512(compute.encode("utf8")).hexdigest()

                        if str(blake2b) == my_hash:
                            crack_boolean = True
                            print(cyan + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

                        if str(blake2s) == my_hash:
                            crack_boolean = True
                            print(cyan + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

                        if str(md5) == my_hash:
                            crack_boolean = True
                            print(cyan + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

                        if str(sha1) == my_hash:
                            crack_boolean = True
                            print(cyan + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

                        if str(sha224) == my_hash:
                            crack_boolean = True
                            print(cyan + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

                        if str(sha256) == my_hash:
                            crack_boolean = True
                            print(cyan + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

                        if str(sha512) == my_hash:
                            crack_boolean = True
                            print(cyan + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

                        if str(sha3256) == my_hash:
                            crack_boolean = True
                            print(cyan + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

                        if str(sha3384) == my_hash:
                            crack_boolean = True
                            print(cyan + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

                        if str(sha3512) == my_hash:
                            crack_boolean = True
                            print(cyan + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

        if mask == True:
            for i in range (minimum, maximum + 1):
                if crack_boolean == True:
                    break

                print(cyan + "attempting length: " + str(i))

                for words in word_list:
                    if crack_boolean == True:
                        crack_boolean = False
                        break

                    print("checking: " + words)

                    for ii in itertools.product(dictionary, repeat = i):
                        var = "".join(ii)
                        compute = words + var

                        if len(my_hash) == 32:
                            md5 = hashlib.md5(compute.encode("utf8")).hexdigest()

                        if len(my_hash) == 40:
                            sha1 = hashlib.sha1(compute.encode("utf8")).hexdigest()

                        if len(my_hash) == 56:
                            sha224 = hashlib.sha224(compute.encode("utf8")).hexdigest()

                        if len(my_hash) == 64:
                            blake2s = hashlib.blake2s(compute.encode("utf8")).hexdigest()
                            sha256 = hashlib.sha256(compute.encode("utf8")).hexdigest()
                            sha3256 = hashlib.sha3_256(compute.encode("utf8")).hexdigest()

                        if len(my_hash) == 96:
                            sha3384 = hashlib.sha3_384(compute.encode("utf8")).hexdigest()

                        if len(my_hash) == 128:
                            blake2b = hashlib.blake2b(compute.encode("utf8")).hexdigest()
                            sha512 = hashlib.sha512(compute.encode("utf8")).hexdigest()
                            sha3512 = hashlib.sha3_512(compute.encode("utf8")).hexdigest()

                        if str(blake2b) == my_hash:
                            crack_boolean = True
                            print(cyan + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

                        if str(blake2s) == my_hash:
                            crack_boolean = True
                            print(cyan + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

                        if str(md5) == my_hash:
                            crack_boolean = True
                            print(cyan + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

                        if str(sha1) == my_hash:
                            crack_boolean = True
                            print(cyan + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

                        if str(sha224) == my_hash:
                            crack_boolean = True
                            print(cyan + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

                        if str(sha256) == my_hash:
                            crack_boolean = True
                            print(cyan + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

                        if str(sha512) == my_hash:
                            crack_boolean = True
                            print(cyan + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

                        if str(sha3256) == my_hash:
                            crack_boolean = True
                            print(cyan + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

                        if str(sha3384) == my_hash:
                            crack_boolean = True
                            print(cyan + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

                        if str(sha3512) == my_hash:
                            crack_boolean = True
                            print(cyan + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

    with open("password dump.txt", "a") as f:
        for password in password_list:
            f.write(password + "\n")

    print(cyan + "done")
