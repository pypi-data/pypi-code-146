from base64 import b64decode as b64d
from base64 import b64encode as b64e
import time
from subprocess import check_output as ch
import random
import math
import threading as th
def decrypt(key,cipher):
    j = 0
    plaint_s = ""
    for i in range(len(cipher)):
            plaint_s+= chr(cipher[i]^int(key[j]))
    return plaint_s
def encrypt(key,plaint):
    j = 0
    cipher_s = []
    cipher_e = b''
    for i in range(len(plaint)):
        cipher_s+= chr(plaint[i]^int(key[j]))
    for i in cipher_s:
        cipher_e+=i.encode()
    return cipher_e
""" 
===Mr.enc===
Rsa_ library developed by Codelogy
GitHub: github.com/MrFploit
Telegram: @codelogy
twitter: twitter.com/MrFploit
"""
p = 0
q = 0
def lod_pack_pr(pack :str):
    """
    Converts the private key package to a usable state
    """
    pack = pack.replace("_______________BEGIN RSA PRIVATE KEY_______________","")
    pack = pack.replace("_______________END RSA PRIVATE KEY_______________","")
    pack = pack.split("\n")
    pack = "".join(pack)
    return pack
def lod_pack_pu(pack:str):
    """
    Converts the public key package to a usable state
    """
    pack = pack.replace("_______________BEGIN RSA PUBLIC KEY_______________","")
    pack = pack.replace("_______________END RSA PUBLIC KEY_______________","")
    pack = pack.split("\n")
    pack = "".join(pack)
    return pack
def extended_gcd(a: int, b: int) -> int:
    """
    gcd = an algorithm for finding the greatest common divisor between two non-negative numbers
    """
    x = 0
    y = 1
    lx = 1
    ly = 0
    oa = a
    ob = b
    while b != 0:
        q = a // b
        (a, b) = (b, a % b)
        (x, lx) = ((lx - (q * x)), x)
        (y, ly) = ((ly - (q * y)), y)
    if lx < 0:
        lx += ob
    if ly < 0:
        ly += oa
    return a, lx, ly
def D(e :int , phi :int) -> int:
    """
    By receiving e and ϕ(n), it generates the public key
    To create a public key, proceed as follows
    d * e ( mod ϕ ( n )) = 1
    """
    (divider, inv, _) = extended_gcd(e, phi)
    if divider != 1:
        raise print("error")
    return inv
def E(a,b,s):
    """
    Generates a random number that is between 1 and ϕ(n)
    and is prime in relation to n and ϕ(n)
    """
    while True:
        n = random.randint(s,a)
        if math.gcd(n,b) == 1:
            if math.gcd(n,a) == 1:
                break
            else:
                continue
    return n
def nBitRandom(n:int) -> int:
    """
    The first large number
    """
    a = ch(f'prime.exe {n}',shell=True).decode()
    return int(a)
def getLowLevelPrime(n,i):
    """
    Making the first two big random numbers
    """
    global p ,q
    if i == 1:
        p = nBitRandom(n)
    else:
        q =nBitRandom(n)
    return True
def key_Generator(len_key:int) -> dict:
    """
    RSA random key construction
    For Windows
    """
    t1 = th.Thread(target=getLowLevelPrime, args=(len_key,1,)) 
    t2 = th.Thread(target=getLowLevelPrime, args=(len_key,0,))
    t1.start() 
    t2.start() 
    t1.join() 
    t2.join() 
    n = p * q
    i_Euler = (p-1) * (q-1)
    e = E(i_Euler,n,p)
    d = D(e,i_Euler)
    key_loded={"e":e,"d":d,"n":n};del e,d,n
    return key_loded
def decrypt_int(cipher:int,d,n):
    db = pow(cipher, d, n)
    return db
def encrypt_int(plaint:int,e,n):
    db = pow(plaint, e, n)
    return db
def key_Generator_advanced(p:int,q:int) -> dict:
    """
    Creating the key by receiving p and q, which should be the first two large random numbers
    """
    n = p * q
    i_Euler = (p-1) * (q-1)
    e = E(i_Euler,n,p)
    d = D(e,i_Euler)
    key_loded={"e":e,"d":d,"n":n}
    cipher = encrypt_int(5569,e,n)
    if decrypt_int(cipher,d,n) != 5569:
        return "error p or q is not prime"
    else:
        del e,d,n
        return key_loded
def Xor(n,No,res):
    res = str(res)
    No = pow(n,No)
    No = str(No)
    db_x = encrypt(No,res)
    return db_x
def open_pack_pu(addr):
    """
    Read pack from file
    """
    pack_pu=""
    with open(addr,"r")as f:
        pack_pu = f.readlines()
    pack_pu = lod_pack_pu("".join(pack_pu))
    pack_pu = b64d(pack_pu.encode()).decode()
    pack_pu = pack_pu.split("!&")
    (d,n)=pack_pu[0],pack_pu[1];del pack_pu
    key_loded={"d":d,"n":n};del d,n
    return key_loded
    
def open_pack_pr(addr):
    """
    Read pack from file
    """
    pack_pr=""
    with open(addr,"r")as f:
        pack_pr = f.readlines()
    pack_pr = lod_pack_pr("".join(pack_pr))
    pack_pr = b64d(pack_pr.encode()).decode()
    pack_pr = pack_pr.split("!&")   
    (e,n)=pack_pr[0],pack_pr[1];del pack_pr
    key_loded={"e":e,"n":n};del e,n
    return key_loded
def save_pack(key:dict,addr1,addr2) -> bool:
        """
        Save and pack the key in the file
        addr1=PRIVATE KEY file
        addr2=PUBLIC KEY file
        """
        e = key.get("e")
        d = key.get("d")
        n = key.get("n")
        pack_ = str(e)+"!&"+str(n)
        pack_ = b64e(pack_.encode()).decode()
        lol =""
        (s,t)=0,70
        while True:
            if pack_[s:t] == '':
                break
            lol+=pack_[s:t]+"\n"
            s+=70
            t+=70
        pack_ = f'_______________BEGIN RSA PRIVATE KEY_______________\n{lol}_______________END RSA PRIVATE KEY_______________'
        with open (addr1,"w") as f:
            f.write(pack_)
        pack_ = str(d)+"!&"+str(n)
        pack_ = b64e(pack_.encode()).decode()
        lol =""
        (s,t)=0,70
        while True:
            if pack_[s:t] == '':
                break
            lol+=pack_[s:t]+"\n"
            s+=70
            t+=70
        pack_ = f'_______________BEGIN RSA PUBLIC KEY_______________\n{lol}_______________END RSA PUBLIC KEY_______________'
        with open (addr2,"w") as f:
            f.write(pack_)
        return True
class New_rsa_decryptor:
    def __init__(self,key:dict):
        self.d = key.get("d")
        self.n = key.get("n")
    def decrypt(self,cipher:bytes):
        cipher = int.from_bytes(cipher, "big")
        db = pow(cipher, int(self.d), int(self.n))
        db = db.to_bytes((db.bit_length() + 7) // 8, 'big')
        return db
    def decrypt_blind(self,cipher:bytes,No:int):
        """
        Decryption with blinding to prevent mid-channel analysis
        """
        No = pow(self.n,No)
        cipher = int.from_bytes(cipher, "big")
        db = decrypt_int(cipher, int(self.d), int(self.n))
        db = db.to_bytes((db.bit_length() + 7) // 8, 'big')
        db = decrypt(str(No),db)
        return db
class New_rsa_encryptor:
    def __init__(self,key:dict):
        self.e = key.get("e")
        self.n = key.get("n")
    def encrypt(self,plaint:bytes):
        plaint = int.from_bytes(plaint, "big")
        db = pow(plaint, int(self.e), int(self.n))
        db = db.to_bytes((db.bit_length() + 7) // 8, 'big')
        return db
    def encrypt_blind(self,plaint:bytes,No:int):
        """
        Encryption with blinding to prevent mid-channel analysis
        """
        No = pow(self.n,No)
        plaint = encrypt(str(No),plaint)
        plaint = int.from_bytes(plaint, "big")
        db = encrypt_int(plaint, int(self.e), int(self.n))
        db = db.to_bytes((db.bit_length() + 7) // 8, 'big')
        return db
if __name__ == "__main__":
    print("plaint : RSA_ENCRYPT test\nkey len = 2080")
    a = time.time()
    try:
        b = key_Generator(2080)
    except:
        import prime
        q = prime(2080)
        p = prime(2080)
        b = key_Generator_advanced(p,q)
    rsa = New_rsa_encryptor(b)
    q = b64e(rsa.encrypt(b"RSA_ENCRYPT test")).decode()
    print("encrypted: ",q)
    rsa = New_rsa_decryptor(b)
    q = rsa.decrypt(b64d(q.encode())).decode()
    b = time.time() - a
    print(f'decrypted: {q}\ntime: {b}')