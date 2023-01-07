def nbCMin(MP):
     nb=0 
     for i in MP: 
        if 'a'<=i<='z': 
            nb+=1 
        return nb

def nbCMaj(MP): 
    nb=0 
    for i in MP: 
        if 'A'<=i<='Z':
            nb+=1
        return nb

def NbcAlpha(MP): 
    return len(MP)-nbCMaj(MP)-nbCMin(MP)

def longMaj(MP): 
    d=0 
    s=0 
    i=0 
    while i< len(MP):
        if'A'<MP[i]<'Z': 
           s+=1 
    else: 
        if s>d: 
            d=s
            s=0 
        i+=1
    return d

def longMin(MP):
    d=0 
    s=0 
    i=0 
    while i < len(MP):
        if'A'< MP[i]<'z':
          s+=1 
    else: 
        if s>d: 
            d=s 
            s=0 
        i+=1 
    return d

def score(MP):
     bonus=len(MP)*4 + (len(MP)-nbCMaj(MP))*2 +(len(MP)-nbCMin(MP))*3+ NbcAlpha(MP)*5
     penalites=longMin(MP)*2+longMaj(MP)*2 
     val=bonus-penalites 
     if val<20: 
        print('très faible') 
     elif val<40: print('faible') 
     elif val<80: print('fort') 
     else: print('très fort')
     if __name__ == '__main__': 
         MP='P@cSI_promo2017' 
         score(MP)