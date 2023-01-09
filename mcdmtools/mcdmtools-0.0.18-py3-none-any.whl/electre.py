import pandas as pd
import numpy as np
import itertools

def dataRead(path_, index_):
    """Eğer index True ise ilk sütun index olarak alınır\
        dosya yolu ise virgül ile ayrılmış olan bir csv dosyasını işaret etmelidir."""
    if index_ == True:
        veri_df = pd.read_csv(path_,index_col=0)
    elif index_ == False:
        veri_df = pd.read_csv(path_)
    return veri_df
def weighting(weight_, dm_norm):
    weighting = lambda x, y: x * y
    df_weighted = weighting(dm_norm,list(weight_.iloc[0,:].astype(float)))
    return df_weighted
################################################
####Uyum ve Uyumsuzluk Setlerinin Bulunması#####
################################################
def concordanceDiscorcdance(matris_Y, dm):
    permutation_list = list(itertools.permutations(np.arange(len(dm.index))+1,2))
    uyum_set = dict()
    uyumsuz_set = dict()
    for i in permutation_list:
        c = []
        d = []
        for j in range(0,len(dm.columns)):
            if list(matris_Y.iloc[i[0]-1,:])[j] >= list(matris_Y.iloc[i[1]-1,:])[j]:
                c.append(j+1)
            else:
                d.append(j+1)
        uyum_set[i] = c
        uyumsuz_set[i] = d
    return uyum_set, uyumsuz_set
####################################################
####Uyum (concordance) matrisinin (C) bulunması#####
####################################################
def concordanceMatris(uyumSet, weight_, dm):
    matris_C = pd.DataFrame(float("Nan"), index=np.arange(len(dm.index)), columns=np.arange(len(dm.index)))
    sum_C = 0
    for i in uyumSet:
        Ckl = 0
        for j in uyumSet[i]:
            #print(i,j)
            Ckl = Ckl + float(weight_.iloc[0,j-1])
            #print(Ckl)
        sum_C = sum_C + float(Ckl)
        matris_C.iloc[i[0]-1,i[1]-1] = float(Ckl)
    limit_C = sum_C*(1/(len(dm.index)*(len(dm.index)-1)))
    return matris_C, limit_C
##########################################################
####Uyumsuzluk (discordance) matrisinin (D) bulunması#####
##########################################################
def discordanceMatris(uyumsuzSet, matris_Y, dm):
    matris_D = pd.DataFrame(float("Nan"), index=np.arange(len(dm.index)), columns=np.arange(len(dm.index)))
    sum_D = 0
    for i in uyumsuzSet:
        pay_list = []
        payda_list = []
        for j in uyumsuzSet[i]:
            pay_list.append(abs(matris_Y.iloc[i[0]-1,j-1] - matris_Y.iloc[i[1]-1,j-1]))
        for j in range(0,len(dm.columns)):
            payda_list.append(abs(matris_Y.iloc[i[0]-1,j] - matris_Y.iloc[i[1]-1,j]))
        try:
            sum_D = sum_D + max(pay_list)/max(payda_list)
        except:
            sum_D = 0
        try:
            matris_D.iloc[i[0]-1,i[1]-1] = max(pay_list)/max(payda_list)
        except:
            matris_D.iloc[i[0]-1,i[1]-1] = 0
    limit_D = sum_D*(1/(len(dm.index)*(len(dm.index)-1)))
    return matris_D, limit_D
###################################################################
####Uyum üstünlük (F) (concordance index) matrisinin bulunması#####
###################################################################
def concordanceIndisMatris(matris_C, limit_C):
    matris_F = matris_C.copy()
    matris_F[matris_F>=limit_C]=1
    matris_F[matris_F<limit_C]=0
    return matris_F
#########################################################################
####Uyumsuzluk üstünlük (G) (discordance index) matrisinin bulunması#####
#########################################################################
def discordanceIndisMatris(matris_D, limit_D):
    matris_G = matris_D.copy()
    matris_G[matris_G>=limit_D]=1
    matris_G[matris_G<limit_D]=0
    return matris_G
######################################################
####Toplam baskınlık matrisinin (E) oluşturulması#####
######################################################
def dominanceMatris(matris_F, matris_G, dm):
    matris_E = matris_F.multiply(matris_G)
    matris_E = matris_E.set_axis(list(dm.index.values), axis=0)
    matris_E = matris_E.set_axis(list(dm.index.values), axis=1)
    return matris_E