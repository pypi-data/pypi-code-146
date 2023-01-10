import pandas as pd
import re



##############################
##### Verilerin okunması #####
##############################
def dataRead(path_):
    veri_df = pd.read_csv(path_,header=None)
    return veri_df

#####################################
##### Ağırlıkların hesaplanması #####
#####################################
def weighting(dm):
    df = dm.copy()
    judge = re.findall('r[0-9]',str(df.columns))
    number_of_judge = len(judge)
    sj = 'sj'
    kj = 'kj'
    qj = 'qj'
    wj = 'wj'
    for j in range(1,number_of_judge+1):
        for i in range(0,len(df)):
            if i == 0:
                df.loc[i,qj+str(j)] = 1
            else:
                df.loc[i,qj+str(j)] = df.loc[i-1,qj+str(j)] / df.loc[i,kj+str(j)]
    for i in range(1,number_of_judge+1):
        df[wj+str(i)] = df[qj+str(i)] / sum(df[qj+str(i)])
        df.sort_values(by=[wj+str(i)],ascending=False)
    return df