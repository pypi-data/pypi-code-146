def mean(L):
    sum_=0
    for i in L:
        sum_+=i
    avg=sum_/len(L)
    return avg
def median(L):
      n = len(L)
      m = n // 2
      if n % 2 == 0:
        return (L[m - 1] + L[m]) / 2
      else:
        return L[m]
def mode(L):
    y={}
    for a in L:
        if a not in y:
            y[a]=1
        else:
            y[a]+=1
    return [g for g,m in y.items() if m==max(y.values())]
