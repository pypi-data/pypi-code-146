import pandas as pd
import numpy as np


def dataRead(path_):
    veri_df = pd.read_csv(path_,error_bad_lines=False, header=None)
    return veri_df

###################################################
#### İkili karşılaştırma matrisinin bulunması #####
###################################################
def pwMatrix(df):
    A=[]
    for i in df.iloc[:,0]:
        try:
            A.append(int(i))
        except:
            if len(i.split('/')) >1:
                A.append(int(i.split('/')[0]) / int(i.split('/')[1]))
            else:
                A.append(int(i))
    n = (1 +(1-4*1*(-1*2*(len(df))))**0.5) / 2
    #nxn boyutunda sıfır matrisi oluşturma
    matris = pd.DataFrame(0, index=np.arange(n), columns=np.arange(n))
    indice = 0
    for i in range(0,int(n)):
        for j in range(0,int(n)):
            if i == j:
                matris.iloc[i,j] = 1
            elif i>j:
                matris.iloc[i,j]=1 / matris.iloc[j,i]
            else:
                matris.iloc[i,j]= float(A[indice])
                indice+=1
    return matris

#####################################
##### Önceliklerin Hesaplanması #####
#####################################
def priority(dm):
    matris_normal_sum = dm / dm.sum(axis=0)
    dm['prior']=matris_normal_sum.mean(axis=1)
    return dm

############################################
##### Tutarlılık Oranının hesaplanması #####
############################################
def consistencyRatio(dm):
    def normalize(x):
        fac = abs(x).max()
        x_n = x / x.max()
        return fac, x_n
    x = [1]*int(n)
    x = np.array(x)
    a = dm.iloc[:,0:-1].to_numpy()

    for i in range(100):
        x = np.dot(a, x)
        lambda_1, x = normalize(x)
    n = len(dm.index)
    rci = {3:0.58,4:0.90,5:1.12,6:1.24,7:1.32,8:1.41,9:1.45,10:1.49,11:1.51,12:1.48,13:1.56,14:1.57,15:1.59}
    ri = rci[int(n)]
    ci = (lambda_1 - int(n)) / (n-1)
    cr = ci / ri
    return cr