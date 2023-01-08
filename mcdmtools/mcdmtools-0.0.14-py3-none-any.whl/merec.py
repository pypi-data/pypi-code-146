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

    