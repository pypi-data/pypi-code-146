import pandas as pd
import numpy as np

def stats(df):
    
    df_stats=pd.DataFrame()

    df_stats=df.describe(percentiles=[.1,.2,.25,.3,.4,.5,.6,.7,.75,.8,.9,.95,.99]).T

    dfMissing=((df.isna().sum()/len(df))*100).to_frame('%ofMissingValues')

    df_temp = df.apply(pd.to_numeric, errors='coerce')
    num_columns = df_temp.select_dtypes(exclude=['object']).columns
    cat_columns = df_temp.select_dtypes(['object']).columns

    dfNonZero=df_temp[num_columns].apply(lambda x: 100 * ((x > 0) & (x.notnull())).mean()).to_frame("%ofNonZeroValues")
    dfNonZero.loc[cat_columns,'%ofNonZeroValues']=np.nan

    dfUnique=df.apply(lambda x: x.nunique(dropna=False), axis=0).to_frame("#ofUniqueValues")


    FinalDF=pd.concat([df_stats,dfMissing,dfNonZero,dfUnique],ignore_index=False,axis=1)

    return FinalDF


def iv_woe(data, target, bins,optimize,thresold):
    
    newDF,woeDF,IVDEF,woeDEF = pd.DataFrame(), pd.DataFrame(),pd.DataFrame(),pd.DataFrame()
    cols = data.columns
    for column in cols[~cols.isin([target])]:
        d1=pd.DataFrame()
        if optimize==True:
            for bin in range(20,0,-1):
                ivO,woeO=iv_woe(data[[column,target]],target,bins=bin,optimize=False,thresold=0)
                w=woeO.loc[woeO['Cutoff'] != 'nan']
                if (all(i >= thresold for i in w['% of N'])):     
                    #print(column,"-",bin)
                    IVDEF=pd.concat([IVDEF,ivO], axis=0)
                    woeDEF=pd.concat([woeDEF,woeO],axis=0)
                    break
                if bin==1:
                    print("couldn't create bins for {0} with specified thresold".format(column))
                    IVDEF=pd.concat([IVDEF,ivO], axis=0)
                    woeDEF=pd.concat([woeDEF,woeO],axis=0)
                    break

                    

        if (data[column].dtype.kind in 'bifc') and (len(np.unique(data[column]))>10):
            binned_x = pd.qcut(data[column], bins,  duplicates='drop')
            d0 = pd.DataFrame({'x': binned_x, 'y': data[target]})
        else:
            d0 = pd.DataFrame({'x': data[column], 'y': data[target]})
        d0 = d0.astype({"x": str})
        d = d0.groupby("x", as_index=False, dropna=False).agg({"y": ["count", "sum"]})
        d.columns = ['Cutoff', 'N', 'Events']
        d['% of N']=d['N']/len(data)
        d['% of Events'] = np.maximum(d['Events'], 0.5) / d['Events'].sum()
        d['Non-Events'] = d['N'] - d['Events']
        d['% of Non-Events'] = np.maximum(d['Non-Events'], 0.5) / d['Non-Events'].sum()
        
        d['WoE'] = np.log(d['% of Non-Events']/d['% of Events'])
        d['IV'] = d['WoE'] * (d['% of Non-Events']-d['% of Events'])
        d['Bin_index']=d['Cutoff'].str.extract('\((.*),', expand=False).astype(float)
        d['% of Events_Bin']=d['Events']/d['N']
        d['% of Non-Events_Bin']=d['Non-Events']/d['N']
        
        d.insert(loc=0, column='Variable', value=column)
        
        temp =pd.DataFrame({"Variable" : [column], "IV" : [round(d['IV'].sum(),4)]}, columns = ["Variable", "IV"])
        newDF=pd.concat([newDF,temp], axis=0)
        woeDF=pd.concat([woeDF,d], axis=0)

        woeDF=woeDF.sort_values(by="Bin_index")
        
        woeDF = woeDF.reset_index(drop=True)
        result = woeDF.groupby('Variable').agg({'% of N': ['min', 'max']})
    
    if optimize==True:
        IVDEF=IVDEF.sort_values(by="IV",ascending=False).reset_index(drop=True)
        return IVDEF,woeDEF
    else:
        return newDF, woeDF