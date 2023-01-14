from TheSilent.clear import *

import itertools

cyan = "\033[1;36m"

#brute force hash
def brute_force_hash(my_hash, minimum = 1, maximum = 36, timer = 60, mask = ""):
    dictionary = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ "
    crack_boolean = False
    timer *= 60
    hash_count = 0
    my_hash = my_hash.lower()

    clear()

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

    if mask == "":
        for i in range (minimum, maximum):
            if crack_boolean == True:
                break
            
            print(cyan + "attempting length: " + str(i))
            
            for ii in itertools.product(dictionary, repeat = i):
                compute = "".join(ii)
                hash_count += 1
                
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

        print(cyan + "hashes computed: " + str(hash_count))

    if mask != "":
        for i in range (minimum, maximum):
            start = time.time()

            if crack_boolean == True:
                break
            
            print(cyan + "attempting length: " + str(i))
            
            for ii in itertools.product(dictionary, repeat = i):
                var = "".join(ii)
                compute = mask + var
                hash_count += 1
                
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

        print(cyan + "hashes computed: " + str(hash_count))
