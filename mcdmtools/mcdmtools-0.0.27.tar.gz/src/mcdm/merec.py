import pandas as pd
import numpy as np
import math

def dataRead(path_, index_):
    """Eğer index True ise ilk sütun index olarak alınır\
        dosya yolu ise virgül ile ayrılmış olan bir csv dosyasını işaret etmelidir."""
    if index_ == True:
        veri_df = pd.read_csv(path_,index_col=0)
    elif index_ == False:
        veri_df = pd.read_csv(path_)
    return veri_df

############################################################################
######### Alternatiflerin genel performanslarının değerlendirilmesi ########
############################################################################
def Si(dm, profitcost):
    dm2 = dm.copy()
    df_Si = abs(np.log(dm2))
    df_Si = 1 + (1 /len(profitcost.columns)) * df_Si.sum(axis = 1)
    df_Si = np.log(df_Si)
    return df_Si

##############################################################################################
######### Herbir alternatifin kriter i hariç tutularak performanslarının hesaplanması ########
##############################################################################################
def Sij(dm, dm_norm):
    df_Sij = pd.DataFrame(columns = list(dm.columns))
    for i in range(0,len(dm.index)):
        liste_Si = []
        for j in range(0,len(dm.columns)):
            #liste_satir.append(df.iloc[i,j])
            liste_satir = []
            for k in range(0,len(dm.columns)):
                if k == j:
                    pass
                else:
                    liste_satir.append(dm_norm.iloc[i,k])
            #print("S'"+str(i+1)+str(j+1),np.log(1+(1/len(df.columns))*sum(abs(np.log(liste_satir)))))
            liste_Si.append(np.log(1+(1/len(dm.columns))*sum(abs(np.log(liste_satir)))))
        df_Sij.loc[i] = liste_Si
    return df_Sij

######################################################
######### Toplam mutlak sapmanın hesaplanması ########
######################################################
def removalEffect(dm, dfSi, dfSij):
    removal_effect_Ei = []
    for i in range(0,len(dm.columns)):
        removal_effect_Ei.append(abs(dfSij.iloc[:,i]-list(dfSi)).sum())
    return removal_effect_Ei

##################################################
######### Nihai ağırlıkların hesaplanması ########
##################################################
def calculatingWeight(liste, dm):
    df_weight = pd.DataFrame(columns = list(dm.columns))
    df_weight.loc[0] = list(liste/sum(liste))
    return df_weight