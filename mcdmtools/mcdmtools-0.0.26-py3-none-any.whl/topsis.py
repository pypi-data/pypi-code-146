import pandas as pd
import numpy as np

def dataRead(path_, index_):
    """Eğer index True ise ilk sütun index olarak alınır\
        dosya yolu ise virgül ile ayrılmış olan bir csv dosyasını işaret etmelidir."""
    if index_ == True:
        veri_df = pd.read_csv(path_,index_col=0)
    elif index_ == False:
        veri_df = pd.read_csv(path_)
    return veri_df

####################################################################
######### İdeal ve negatif ideal Çözüm Vektörünün Bulunması ########
####################################################################
def AplusAminusVector(weighted_, profitcost, dm):
    Aplus = [max(weighted_.iloc[:,i])  if profitcost.iloc[0,i]== 'max' else min(weighted_.iloc[:,i]) for i in range(0,len(dm.columns))]
    Aminus = [min(weighted_.iloc[:,i])  if profitcost.iloc[0,i]== 'max' else max(weighted_.iloc[:,i]) for i in range(0,len(dm.columns))]
    return Aplus, Aminus

#################################################
######### Ayrım ölçümlerinin bulunması ##########
#################################################
def SplusSminusVector(weighted_, Aplus, Aminus):
    Splus = [sum(list(map(lambda x,y : (x-y)**2, weighted_.iloc[i],Aplus)))**0.5 for i in range(0, len(weighted_))]
    Sminus = [sum(list(map(lambda x,y : (x-y)**2, weighted_.iloc[i],Aminus)))**0.5 for i in range(0, len(weighted_))]
    return Splus, Sminus

##############################################################################
######### İdeal çözüme olan göreli yakınlık değerlerinin hesaplanması ########
##############################################################################
def Si(Splus, Sminus, dm):
    dm_result = dm.copy()
    rank_order_vector = {list(dm_result.index)[i]: Sminus[i] / (Splus[i] + Sminus[i]) for i in range(0, len(dm_result.index))}
    dm_result['Si'] = list(rank_order_vector.values())
    return dm_result