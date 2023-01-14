#this will return the each word frequency in the given string
def count_all(st):
    
    """ this function will require a String of words 
    and then return each word count in the string"""
    
    st = st.split(" ") #spliting each word on the basis of space it will return a list of words
    dict1 = dict() #creating an empty dictionary
    
    for item in st: #loop througn all the list
        a = st.count(item) #counting each word
        dict1.update({item :a}) #putting each word in the dictionary
    
    for k,v in dict1.items():
        print("{} : {} times".format(k,v)) #now loop through the dictionary and printing each word count