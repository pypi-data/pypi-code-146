def count_all(st):
    st = st.split(" ")
    dict1 = dict()
    temp = ""
    for item in st:
        a = st.count(item)
        dict1.update({item :a})
        if temp == item:
            print("already existed")
        elif a > 1:
            temp = item
            print("{} : {} times".format(item, a))
        else:
            print("{} : {} time".format(item, a))
