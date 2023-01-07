def nbCMin(MP):
    nb=0
    for i in MP:
      if 'a'<=i<='z': #vérifier les caractères Min
        nb+=1 #incrémenter le nb de caractères Maj
    return nb
def nbCMaj(MP):
    nb=0
    for i in MP:
      if 'A'<=i<='Z': #vérifier les caractères Maj
        nb+=1 #incrémenter le nb de caractères #Maj
    return nb
def NbcAlpha(MP):
    return len(MP)-nbCMaj(MP)-nbCMin(MP)

def longMaj(MP):
    d=0
    s=0
    i=0 
    while i< len (MP): #parcourir le mot de passe
        if'A'<MP[i]<'Z': #vérifier les caractères Maj
            s+=1 #incrémenter la taille de la séquence
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
  while i < len (MP): #parcourir le mot de passe
    if'a'<MP[i]<'z': #vérifier les caractères Min
       s+=1
    else:
      if s>d:
         d=s
         s=0
    i+=1
  return d



def score(MP):
#Calcul bonus
  bonus=len(MP)*4 + (len(MP)-nbCMaj(MP))*2 +(len(MP)-nbCMin(MP))*3+ NbcAlpha(MP)*5
#Calcul pénalité
penalites=longMin(MP)*2+longMaj(MP)*2
val=bonus-penalites
if val<20:  
  print('très faible')
elif val<40:
  print('faible')
elif val<80:
  print('fort')
else:
  print('très fort')
if __name__ == '__main__':
  MP='P@cSI_promo2017'
score(MP)