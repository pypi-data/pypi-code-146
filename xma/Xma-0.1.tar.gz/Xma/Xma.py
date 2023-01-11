import random as rD
size = '1'
def size_set(size_):
    global size
    size+= ('0'*size_)
def X(nonce,key,Size):
    return pow(nonce,key,Size) * (len(str(Size))+(key%Size)) % Size
def rnd(x,key,Rd):
    global size
    return ((int(x)*int(key))<<Rd)* (len(x)+int(key)) << Rd % int(size)
def NO(no,key,size):
    return pow(no,key,size) * (len(str(size))+(key%size)) % size
class New_Xma:
    def __init__(self,key:bytes,No:bytes,nonce:bytes) -> None:
        global size
        if len(nonce+No+key) < 96 :
            raise NameError("Short key length")
        else:
            self.nonce = int.from_bytes(nonce, "big")
            self.key = int.from_bytes(key, "big") 
            self.no = int.from_bytes(No, "big")
            self.x = str(X(self.nonce,self.key,int(size)))
            self.no = str(NO(self.key,self.no,int(size)))
    def SEF_RKF(self,PL:bytes):
        PL = str(int.from_bytes(PL, "big"))
        rd = rD.randint(10,100)
        x = rnd(self.x,self.key,len(PL)+rd)
        x = int(str(int(x))[:len(PL)+rd])
        PL = str((int(PL)^int(x)))
        no = str(rnd(self.no,self.key,len(PL)))
        no = no[:len(str(PL))]
        Ciphe = []
        j = 0
        for i in PL:
            Ciphe.append(chr(int(i)<<int(no[j])).encode())
            j +=1
        return b''.join(Ciphe)
    def SDF_RKF(self,CP:bytes):
        CP = CP.decode()
        x = rnd(self.x,self.key,len(CP))
        x = str(int(x))[:len(CP)]
        no = str(rnd(self.no,self.key,len(CP)))
        no = no[:len(CP)]
        j = 0
        Ciphe = []
        for i in CP:
            Ciphe.append(str(ord(i)>>int(no[j])))
            j+=1
        CP = ''.join(Ciphe)
        CP = int(CP)^int(x)
        return CP.to_bytes((CP.bit_length() + 7) // 8, 'big')
    def SEF_F(self,PL:bytes):
        PL = str(int.from_bytes(PL, "big"))
        rd = rD.randint(10,100)
        x = int(self.x[:len(PL)+rd])
        PL = str((int(PL)^int(x)))
        no = str(self.no[:len(str(PL))])
        Ciphe = []
        j = 0
        for i in PL:
            Ciphe.append(chr(int(i)<<int(no[j])).encode())
            j +=1
        return b''.join(Ciphe)
    def SDF_F(self,CP:bytes):
        CP = CP.decode()
        x = int(self.x[:len(CP)])
        no = str(self.no[:len(CP)])
        j = 0
        Ciphe = []
        for i in CP:
            Ciphe.append(str(ord(i)>>int(no[j])))
            j+=1
        CP = ''.join(Ciphe)
        CP = int(CP)^int(x)
        return CP.to_bytes((CP.bit_length() + 7) // 8, 'big')
if __name__ == '__main__':
    tst_msg = b'test encrypt'
    print("PL = "+tst_msg.decode())
    size_set(200)
    xm = New_Xma(b'jiooiodalksjlijalijliadjljadljdlijalihcigceiahljae',b'bjiooiodawriywrlksjlijalijliadjljadljdlijalihcigcwuueiwu9uwoahljae',b'\x19\xd0 4\xf2\xc4\x84Y0N|2\t\xbb^\x1bn\r\xbb\x08\x08\x86\x15\xb2T;\xb9D[\xd0\xcf\x16')
    enc = xm.SEF_F(tst_msg)
    print(f'enc = {enc}')
    dec = xm.SDF_F(enc)
    print(f'dec = {dec}')