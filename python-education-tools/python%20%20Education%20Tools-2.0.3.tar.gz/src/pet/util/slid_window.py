def slid_window(s, size=2,strid=1):
    ns=[s[i:i+size] for i in s[:-size+1:strid]]
    return ns

print(slid_window(tuple(range(10)), 4,3))