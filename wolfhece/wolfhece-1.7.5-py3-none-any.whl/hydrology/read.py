import numpy as np
import os


def read_bin(path, fileName, nbBytes=[]): 

    if nbBytes==[]:
        nbBytes = [1,1,2,1,1,1,8]

    f = open(path+fileName, "rb")
    num = f.read(4)
    nbL = int.from_bytes(num, byteorder='little', signed=True)
    num = f.read(4)
    nbC = int.from_bytes(num, byteorder='little', signed=True)
    print("nb lines = ", nbL)
    print("nb col = ", nbC)


    Data = []
    for i in range(nbL):
        Data.append([])
        for j in range(nbC+1):
            if(nbBytes[j]!=8):
                numB = f.read(nbBytes[j])
                myNum = int.from_bytes(numB, byteorder='little', signed=True)
                Data[i].append(myNum)
            elif(nbBytes[j]==8):
                numB = f.read(8)
                temp = np.frombuffer(numB,dtype=np.float64)
                Data[i].append(temp[0])

    f.close()
    return Data



def is_relative_path(path:str):

    isRelativePath = False

    if len(path)>0:
        if path[0] == ".":
            isRelativePath = True
    else:
        isRelativePath = None
    
    return isRelativePath


    
def relative_2_absolute(fileName:str, prefix:str="", applyCWD:bool=True):

    info = 0

    if prefix == "" :
        if applyCWD :
            prefix = os.path.dirname(__file__)
        else:
            print("ERROR : the path is relative but no prefix is given")
            info = -1
            return info
    
    if is_relative_path(fileName):
        finalName = os.path.join(prefix, fileName)
    else:
        print("This path is not initially a relative path!")
        info  = 1
        finalName = fileName
    
    return info, finalName


def check_path(fileName:str, prefix:str="", applyCWD:bool=True):

    info, finalName = relative_2_absolute(fileName, prefix, applyCWD)
    if info<0:
        info = -2
        return info
    
    isPresent = os.path.exists(finalName)

    if(not(isPresent)):
        print("ERROR : this file or directory does not exist")
        print("File name : ", finalName)
        info = -1
        return info, fileName
    
    return info, finalName
    