#Concatenate elements of a nested lists in vertical format...
def VerticalConcate(list1): #->[["abc", "rfd"],["tew"]] 
    """This method will take a nested list and concatenate vertical elements of it"""
    resList=[]
    count=0
    while count!=len(list1): 
        concate = ''
        for l in list1:
            try:
                concate = concate+l[count]#0->concate=abctew  #1->rfd
            except IndexError:
                pass
        resList.append(concate)#-> ["abctew", "rfd"]
        count = count+1
        resList = [mem for mem in resList if mem]
    return resList
          
    
#This Function will return the indexex of only the strings in your given list
def IndexOfStrings(list2):
    for s in list2:
        if(type(s) is str): #if the element of list is string print the index 
            print(list2.index(s))