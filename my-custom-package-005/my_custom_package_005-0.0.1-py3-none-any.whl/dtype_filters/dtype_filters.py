# this method take a list or tuple, and then return multiple lists having same type of values
# e.g: if we give him a list having multiple type of values 
#it will make the separate collection of same type of values and then return these

def apply_filter(lis):
    
    sList = []
    iList = []
    fList = []
    bList = []
    
    s = i = f = b = 0  #flags use to identify which type of values exist in the list/tuple
    
    sList.clear()
    iList.clear()
    fList.clear()
    bList.clear()

    for item in lis:
        t = type(item)
    
        #checking type of every element of the list and
        #making separate lists of same type of items
        if t == type("string"): 
            sList.append(item)
        elif t == type(1):
            iList.append(item)
        elif t == type(1.0):
            fList.append(item)
        elif t == type(True):
            bList.append(item)
    
    #now checking the length of each list using flag variables
    if len(sList) > 0:
        s = 1
    if len(iList) > 0:
        i = 1
    if len(fList) > 0:
        f = 1
    if len(bList) > 0:
        b = 1
        
    #now checking which lists are not empty
    #and then returning these lists
    if s == 1 and i == 1 and f == 1 and b == 1:
        return sList, iList, fList, bList
    elif s == 1 and i == 1 and f == 1:
        return sList, iList, fList
    elif s == 1 and i == 1 and b == 1:
        return sList, iList, bList
    elif s == 1 and f == 1 and b == 1:
        return sList, fList, bList
    elif i == 1 and f == 1 and b == 1:
        return iList, fList, bList
    elif s == 1 and i == 1:
        return sList, iList
    elif s == 1 and f == 1:
        return sList, fList
    elif s == 1 and b == 1:
        return sList, bList
    elif f == 1 and i == 1:
        return fList, iList
    elif f == 1 and b == 1:
        return fList, bList
    elif i == 1 and b == 1:
        return iList, bList
    elif i == 1:
        return iList
    elif b == 1:
        return bList
    elif s == 1:
        return sList
    elif f == 1:
        return fList
