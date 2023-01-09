#################################### Paquetes ##############################################
import pandas as pd
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import seaborn as sns
from tabulate import tabulate
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import linear_model
from sklearn.model_selection import cross_val_score, cross_val_predict
import joblib
from sklearn.linear_model import ElasticNet
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import sys
import xgboost as xgb

############################### Funciones ##################################################
def InsertColumns(D): #(D es la tabla) 
    D=D.astype({'nro_dormitorios': 'uint8','nro_banos':'uint8','nro_estacionamientos':'uint8','sup_util':'float64',
                'sup_total':'float64','valor_uf':'float64'})
    
    D.insert(D.shape[1],'ufm2(sup_util)',D.loc[:,'valor_uf']/D.loc[:,'sup_util'], True) 
    D.insert(D.shape[1],'ufm2(sup_total)',D.loc[:,'valor_uf']/D.loc[:,'sup_total'], True)
    D.insert(D.shape[1],'sup_total/sup_util',D.loc[:,'sup_total']/D.loc[:,'sup_util'], True) 
    return D
# Concatenación de tablas de ventas y tasaciones
def tabla_auxiliar(df1,variables): #df1 es la tabla de ofertas, variables son las columnas que se guardarán
    df1_aux=df1[variables]
    return df1_aux

# Selección de comuna
def Selec_Comuna(D1,cve): #(D1 es la tabla, cve: es el codigo de la comuna)
    comunas=[19,21,22,52]
    while cve not in comunas:
        print('Ingrese alguna de las siguientes comunas: La Reina (19), Las Condes (21), Lo Barnechea (22) o Vitacura (52):')
        cve=int(input())
    if cve==52:
        tol=5000
    else:
        tol=1000
    D_comuna=D1.loc[(D1.loc[:,'cve_comuna']==cve) & (D1.loc[:,'valor_uf']>=tol)]
    return D_comuna
def datosduplicados(tabla,T): #(tabla es la tabla, T es True entonces se muestra la cantidad de datos eliminados)
    n_inicial = tabla.shape[0];
    tabla2 = tabla.drop_duplicates(subset=['nro_dormitorios','nro_banos','nro_estacionamientos','longitud','latitud',
                                          'sup_util','sup_total'])
    
    if T==True:
        print(f'Hay {n_inicial-tabla2.shape[0]} datos duplicados')
        print(f'Al eliminarlos quedan {tabla2.shape[0]} datos')
    return tabla2
#Identificación de atípicos dada una columna
def outliers_col(df,columna,n,a,T,n_i,limit):  #(df:tabla, columna, n: cantidad de datos inicial,
                                               # a: zscore o IQR, T es True entonces se muestran los resultados
                                               # n_i: cantidad de datos inicial, limit: limite del zscore)
    tabla= pd.DataFrame.from_dict({
    'Variable': [],'Cantidad de Atípicos': [],
    'Type': []});
    col = ['Variable','Cantidad de Atípicos','Type'];
    k=0;
    if (a=='zscore'):
        n_outliers = len(df[np.abs(stats.zscore(df[columna])) > limit])
        k=k+n_outliers;
        tablaux = pd.DataFrame([[df[columna].name,n_outliers,df[columna].dtype]],
                                    columns=col);
        tabla=pd.concat([tabla, tablaux],ignore_index=True);
        
    if (a=='IQR'):
        Q1,Q3 = np.percentile(df[columna], [25,75])
        iqr = Q3 - Q1
        ul = Q3+1.5*iqr
        ll = Q1-1.5*iqr
        n_outliers = len(df[(df[columna] > ul) | (df[columna] < ll)])
        k=k+n_outliers;
        tablaux = pd.DataFrame([[df[columna].name,n_outliers,df[columna].dtype]],
                                    columns=col);
        tabla=pd.concat([tabla, tablaux],ignore_index=True);
    if T==True:
        print(tabulate(tabla, headers=col, tablefmt="fancy_grid"))  
        print('\nSe eliminarán:',k,'datos, y quedarán al menos:',n-k)
        print('en porcentaje con respecto a la cantidad inicial:',(n-k)*100/n_i,'%.\n')     
    return k,tabla
#Eliminación de atípicos dada una columna
def outliers_col_eliminacion(df,columna,a,limit):  #(df:tabla, columna, a: zscore o IQR, limit: limite del zscore)
    if a=='zscore':
        l=df[np.abs(stats.zscore(df[columna])) > limit].index;
        for x in l.values:
            df.loc[x,columna] = np.nan;
                
    if a=='IQR':
        Q1,Q3 = np.percentile(df[columna], [25,75])
        iqr = Q3 - Q1
        ul = Q3+1.5*iqr
        ll = Q1-1.5*iqr
        l=df[(df[columna] > ul) | (df[columna] < ll)].index;
        for x in l.values:
            df.loc[x,columna] = np.nan;
    
    df=df.dropna(axis = 0);
    return df

# Gráficas
def grafico_histograma_sns(df,columna,option1,option2):   #(df:tabla, columna, option1: kde True or False
                                                          #,option2: discrete True or False)
    plt.figure(figsize = (9,4))
    #sns.set_style("whitegrid")
    sns.histplot(data=df[columna],color="#008080",
                 kde=option1,discrete=option2,bins=100);
    plt.xlabel(None)
    plt.title(columna);
    plt.ylabel('Cantidad')
    plt.grid(True, color='lightgrey',linestyle='--')
    plt.show() 
def grafico_hyb_sns(df,columna,option1,option2,binss,col):   #(df:tabla, columna, option1: kde True or False
                                                             #,option2: discrete True or False, binss: numero de bins,
                                                             # col: color)
    #plt.rcParams['figure.figsize'] = (6,4)
    f, (ax_box, ax_hist) = plt.subplots(2,sharex=True,gridspec_kw={"height_ratios": (.25, .95)})
    red_cir = dict(markerfacecolor='maroon',marker='o',markersize=6)
    #sns.set_style("whitegrid")
    plt.grid(True, color='lightgrey',linestyle='--')
    sns.boxplot(x=df[columna],ax=ax_box,color=col,
                flierprops=red_cir).set_title(columna)
    
    sns.stripplot(x=df[columna],ax=ax_box,color="lightsalmon",jitter=0.15, size=2.5)
    sns.histplot(data=df[columna],color=col,ax=ax_hist,
                 kde=option1,discrete=option2,bins=binss)   
    ax_box.set(xlabel='')
    ax_box.grid(True, color='lightgrey',linestyle='--')
    ax_hist.set(xlabel='')
    ax_hist.set(ylabel='Cantidad')
    ax_hist.grid(True, color='lightgrey',linestyle='--')
    plt.show()
def grafico_boxplot_jitted(df,columna,jit):              #(df:tabla, columna, jit: si o no)
    plt.rcParams['figure.figsize'] = (9,12)
    red_cir = dict(markerfacecolor='maroon',marker='o',markersize=6)
    #sns.set_style("whitegrid")
    plt.grid(True, color='lightgrey',linestyle='--')
    if(jit=='no'):
        sns.boxplot(y=df[columna],color="#008080",
                     flierprops=red_cir).set_title(columna);  
    else:
        ax=sns.boxplot(x=df[columna],data=df,color="#008080",
                flierprops=red_cir).set_title(columna); 
        ax=sns.stripplot(x=df[columna], data=df, color="lightsalmon", jitter=0.15, size=2.5)

    plt.xlabel(None)   
    plt.grid(True, color='lightgrey',linestyle='--')
    plt.show()

# Eliminar datos iguales a 0
def Del_DBcero(df):  #df:tabla de ofertas
    if not sys.warnoptions:
        import warnings
        warnings.simplefilter("ignore")
    I1=df[(df['nro_dormitorios']<1)].index
    for x in I1.values:
            df.loc[x,'nro_dormitorios'] = np.nan;
            
    I2=df[(df['nro_banos']<1)].index
    for x in I2.values:
            df.loc[x,'nro_banos'] = np.nan;
            
    df=df.dropna(axis = 0);
    return df
def atypicals_be_gone(df,pars,T,metodo,limit,colors):
    ## Gráficos antes de la eliminación
    # Histogramas 1
    print('Histogramas (con atípicos)')
    for j in range(0,len(pars)):
        grafico_hyb_sns(df,pars[j],True,False,100,colors[j])
        plt.show()
    ## Eliminación de atípicos  
    n_i=df.shape[0]
    for j in range(0,len(pars)):
        w=1
        if T==True:
            print(f'Eliminación de atípicos considerando: {pars[j]}')
        while (w!=0):
            [w,resum]=outliers_col(df,pars[j],df.shape[0],metodo,T,n_i,limit);
            df=outliers_col_eliminacion(df,pars[j],metodo,limit);
    ## Gráficos después de la eliminación
    # Histogramas 2
    print('Histogramas (sin atípicos)')
    for j in range(0,len(pars)):
        grafico_hyb_sns(df,pars[j],True,False,100,colors[j])
        plt.show()
   
    return df

# Matriz de correlación
def matriz_correlacion(df):
    matriz = df.corr(method='kendall')
    plt.rcParams['figure.figsize'] = (7,7);
    plt.matshow(matriz, cmap='BrBG', vmin=-1, vmax=1)
    plt.xticks(range(df.shape[1]), df.columns, rotation=90)
    plt.yticks(range(df.shape[1]), df.columns)

    for i in range(len(matriz.columns)):
          for j in range(len(matriz.columns)):
                 plt.text(i, j, round(matriz.iloc[i, j], 2),
                 ha="center", va="center")

    plt.colorbar()
    plt.grid(False)
    plt.show()
# Cálcular el tamaño de la muestra
def tam_muestra(ofertas_comuna1,confianza):
    alpha=1-confianza # Confianza del 90%=0.9
    N=ofertas_comuna1.shape[0]
    er=10/ofertas_comuna1['valor_uf'].mean()
    Z=stats.norm.ppf(1-alpha/2)
    COV=ofertas_comuna1['valor_uf'].std()/ofertas_comuna1['valor_uf'].mean()
    nmuestra=(N*(COV**2)*(Z**2))/((er**2)*(N-1)+(COV**2)*(Z**2))
    n_muestra=int(nmuestra)
    return n_muestra

def Muestra(df1,df2,cve,ant):
    nn=tam_muestra(df1,0.9) 
    n1=int(nn/10) 
    N=df1.shape[0] 
    n2=int(N/10) 
    df3=df1.sort_values(by=ant, ascending= True)
    Muestras=[]
    for i in range(0,2):
        a1=df3.iloc[0:n2,:]
        b1=df3.iloc[n2:2*n2,:]
        c1=df3.iloc[2*n2:3*n2,:]
        d1=df3.iloc[3*n2:4*n2,:]
        e1=df3.iloc[4*n2:5*n2,:]
        f1=df3.iloc[5*n2:6*n2,:]
        g1=df3.iloc[6*n2:7*n2,:]
        h1=df3.iloc[7*n2:8*n2,:]
        i1=df3.iloc[8*n2:9*n2,:]
        j1=df3.iloc[9*n2:N+1,:]
        if n1==n2:
            A1=a1.sample(n=n1)
            B1=b1.sample(n=n1)
            C1=c1.sample(n=n1)
            D1=d1.sample(n=n1)
            E1=e1.sample(n=n1)
            F1=f1.sample(n=n1)
            G1=g1.sample(n=n1)
            H1=h1.sample(n=n1)
            I1=i1.sample(n=n1)
            J1=j1.sample(n=nn-9*n1)
        else:
            k,n3=0,n1 
            while 10*n1+k<=nn:
                if 10*n1+k==nn:
                    A1=a1.sample(n=n1)
                    B1=b1.sample(n=n1)
                    C1=c1.sample(n=n1)
                    D1=d1.sample(n=n1)
                    E1=e1.sample(n=n1)
                    F1=f1.sample(n=n1)
                    G1=g1.sample(n=n1)
                    H1=h1.sample(n=n1)
                    I1=i1.sample(n=n1)
                    J1=j1.sample(n=n1)
                    break   
                k=k+1 
                n3=n3+1
                A1=a1.sample(n=n3)
                if 10*n1+k==nn:
                    B1=b1.sample(n=n1)
                    C1=c1.sample(n=n1)
                    D1=d1.sample(n=n1)
                    E1=e1.sample(n=n1)
                    F1=f1.sample(n=n1)
                    G1=g1.sample(n=n1)
                    H1=h1.sample(n=n1)
                    I1=i1.sample(n=n1)
                    J1=j1.sample(n=n1)
                    break
                k=k+1
                B1=b1.sample(n=n3) 
                if 10*n1+k==nn:
                    C1=c1.sample(n=n1)
                    D1=d1.sample(n=n1)
                    E1=e1.sample(n=n1)
                    F1=f1.sample(n=n1)
                    G1=g1.sample(n=n1)
                    H1=h1.sample(n=n1)
                    I1=i1.sample(n=n1)
                    J1=j1.sample(n=n1)
                    break
                k=k+1
                C1=c1.sample(n=n3)
                if 10*n1+k==nn:    
                    D1=d1.sample(n=n1)
                    E1=e1.sample(n=n1)
                    F1=f1.sample(n=n1)
                    G1=g1.sample(n=n1)
                    H1=h1.sample(n=n1)
                    I1=i1.sample(n=n1)
                    J1=j1.sample(n=n1)
                    break  
                k=k+1
                D1=d1.sample(n=n3) 
                if 10*n1+k==nn:
                    E1=e1.sample(n=n1)
                    F1=f1.sample(n=n1)
                    G1=g1.sample(n=n1)
                    H1=h1.sample(n=n1)
                    I1=i1.sample(n=n1)
                    J1=j1.sample(n=n1)
                    break 
                k=k+1
                E1=e1.sample(n=n3)
                if 10*n1+k==nn:
                    F1=f1.sample(n=n1)
                    G1=g1.sample(n=n1)
                    H1=h1.sample(n=n1)
                    I1=i1.sample(n=n1)
                    J1=j1.sample(n=n1)
                    break 
                k=k+1
                F1=f1.sample(n=n3)
                if 10*n1+k==nn:
                    G1=g1.sample(n=n1)
                    H1=h1.sample(n=n1)
                    I1=i1.sample(n=n1)
                    J1=j1.sample(n=n1)
                    break
                k=k+1
                G1=g1.sample(n=n3)
                if 10*n1+k==nn:
                    H1=h1.sample(n=n1)
                    I1=i1.sample(n=n1)
                    J1=j1.sample(n=n1)
                    break 
                k=k+1
                H1=h1.sample(n=n3)
                if 10*n1+k==nn:
                    I1=i1.sample(n=n1)
                    J1=j1.sample(n=n1)
                    break 
                k=k+1
                I1=i1.sample(n=n3)
                if 10*n1+k==nn:
                    J1=j1.sample(n=n1)
                    break 
                k=k+1
                J1=j1.sample(n=n3)
        MuestraML=pd.concat([A1,B1,C1,D1,E1,F1,G1,H1,I1,J1],sort=False)
        MuestraML=datosduplicados(MuestraML,False)
        Muestras.append(MuestraML)
    MuestraML=Muestras[0]
    MuestraAVM=pd.merge(df2,Muestras[1], how="right", 
                        on=["cve_comuna",'nro_dormitorios','nro_banos','nro_estacionamientos',"longitud","latitud","sup_util","sup_total","valor_uf"])

    MuestraAVM=datosduplicados(MuestraAVM,False)
    nombre1='Muestra_Oferta_ML'+str(cve)+'.xlsx'
    nombre2='Muestra_Oferta_AVM'+str(cve)+'.xlsx'
    MuestraML.to_excel(nombre1)
    MuestraAVM.to_excel(nombre2)
    return MuestraML,MuestraAVM,nn

def Muestra_Total(A):
    if A=="ML":
        LR = pd.read_excel('Muestra_Oferta_ML19.xlsx');
        LC = pd.read_excel('Muestra_Oferta_ML21.xlsx');
        LB = pd.read_excel('Muestra_Oferta_ML22.xlsx');
        V = pd.read_excel('Muestra_Oferta_ML52.xlsx');
        Muestra = pd.concat([LR,LC,LB,V], ignore_index=True, sort=False)
        Muestra.to_excel('Muestra_Total_Oferta_ML.xlsx')
    elif A=="AVM":
        LR = pd.read_excel('Muestra_Oferta_AVM19.xlsx');
        LC = pd.read_excel('Muestra_Oferta_AVM21.xlsx');
        LB = pd.read_excel('Muestra_Oferta_AVM22.xlsx');
        V = pd.read_excel('Muestra_Oferta_AVM52.xlsx');
        Muestra = pd.concat([LR,LC,LB,V], ignore_index=True, sort=False)
        Muestra.to_excel('Muestra_Total_Oferta_AVM.xlsx')
    return Muestra
# Gráfica de boxplots #columna: 'nro dormitorios','nro banos','nro estacionamientos'
def grafico_boxplot_rcParams(df2,columna):
    plt.rcParams['figure.figsize'] = (9,6);
    sns.boxplot(data=df2.sort_values(by=[columna],
              ascending=True, inplace=False), 
              x=columna, y="valor_uf",
              showfliers=False,palette="Set2");
    sns.stripplot(data=df2.sort_values(by=[columna], 
              ascending=True, inplace=False), 
              x=columna, y="valor_uf",
              linewidth=1.0,palette="Set2");
    plt.xlabel(columna[4:])
    plt.ylabel('Valor UF')
    plt.title('Distribución valor UF por número de '+columna[4:])
    plt.grid(True, color='lightgrey',linestyle='--')
    plt.show()

def GraEstModels(a,b,c,d,e,f,g,h):
    xvec=list(a)
    xvec2=list(c)
    xvec3=list(e)
    xvec4=list(g)
    for k in range(0,len(xvec2)):
        xvec.append(xvec2[k])
    for k in range(0,len(xvec3)):
        xvec.append(xvec3[k])
    for k in range(0,len(xvec4)):
        xvec.append(xvec4[k])   
    xmin,xmax=min(xvec)-250,max(xvec)+250
    yvec=list(b)
    yvec2=list(d)
    yvec3=list(f)
    yvec4=list(h)
    for k in range(0,len(yvec2)):
        yvec.append(yvec2[k])
    for k in range(0,len(yvec3)):
        yvec.append(yvec4[k])
    for k in range(0,len(yvec4)):
        yvec.append(yvec4[k])
    ymin,ymax=min(yvec)-250,max(yvec)+250
    red=[xmin,xmax]
    
    fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(14,10))
    axs[0,0].scatter(a,b,color="#008080");
    axs[0,0].plot(red,red,color="red")
    axs[0,0].set_xlabel('Valor Observado',size=12)
    axs[0,0].set_ylabel('Valor Estimado',size=12)
    axs[0,0].grid(True)
    axs[0,0].set_xlim(xmin,xmax)
    axs[0,0].set_ylim(ymin,ymax)
    axs[0,0].set_title('Regresión Lineal', size= 16)

    axs[0,1].scatter(c,d,color="#008080");
    axs[0,1].plot(red,red,color="red")
    axs[0,1].set_xlabel('Valor Observado',size=12)
    axs[0,1].set_ylabel('Valor Estimado',size=12)
    axs[0,1].grid(True)
    axs[0,1].set_xlim(xmin,xmax)
    axs[0,1].set_ylim(ymin,ymax)
    axs[0,1].set_title('ElasticNet', size= 16)
    
    axs[1,0].scatter(e,f,color="#008080");
    axs[1,0].plot(red,red,color="red")
    axs[1,0].set_xlabel('Valor Observado',size=12)
    axs[1,0].set_ylabel('Valor Estimado',size=12)
    axs[1,0].grid(True)
    axs[1,0].set_xlim(xmin,xmax)
    axs[1,0].set_ylim(ymin,ymax)
    axs[1,0].set_title('Random Forest', size= 16)
    
    axs[1,1].scatter(g,h,color="#008080");
    axs[1,1].plot(red,red,color="red")
    axs[1,1].set_xlabel('Valor Observado',size=12)
    axs[1,1].set_ylabel('Valor Estimado',size=12)
    axs[1,1].grid(True)
    axs[1,1].set_xlim(xmin,xmax)
    axs[1,1].set_ylim(ymin,ymax)
    axs[1,1].set_title('Extreme Gradient Boosting', size= 16)

    plt.show()

def porcentajeerror(a,b): # a: y_test, b: y_pred
    r1=100*(b-a)/a;
    rr1=r1.tolist();
    tabla= pd.DataFrame.from_dict({'Intervalo':[],'%_Est_Acumulado': [],'Cantidad_Est_Relativa': []});
    col = ['Intervalo','%_Est_Acumulado','Cantidad_Est_Relativa'];
    cant=0
    k=[5,10,15,20,25,50]
    for lim in range(0,len(k)):
        if k[lim]==5:
            inter=f"|Error|<={k[lim]} %"
        else: 
            inter=f"{k[lim-1]}% <|Error|<={k[lim]}%"
        porcentaje1=100*sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr1))/len(rr1)
        cantidad1=sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr1))-cant
        cant=cant+cantidad1

        tablaux = pd.DataFrame([[inter,porcentaje1,cantidad1]], columns=col);
        tabla=pd.concat([tabla, tablaux],ignore_index=True);
    return tabla
def Entrenamiento(df2, t_s):
    Xrlinter = np.array(df2[['nro_dormitorios','nro_banos','nro_estacionamientos','longitud','latitud','sup_util','sup_total']])
    yrlinter = np.array(df2.valor_uf)
    Xrlinter_train, Xrlinter_test, yrlinter_train, yrlinter_test = train_test_split(Xrlinter, yrlinter, test_size=t_s)
    return Xrlinter_train, Xrlinter_test, yrlinter_train, yrlinter_test

def Escalas(cve, Xrlinter_train, Xrlinter_test):
    scl = StandardScaler().fit(Xrlinter_train)
    Xrlinter_train = scl.transform(Xrlinter_train)  
    Xrlinter_test = scl.transform(Xrlinter_test)  
    return Xrlinter_train, Xrlinter_test,scl
# Regresion lineal para una indexacion
def Regresion(Xtrain,Xtest,ytrain,ytest,k):
    multi_regr= linear_model.LinearRegression()
    multi_regr.fit(Xtrain, ytrain)
    y_pred13 =cross_val_predict(multi_regr, Xtest, ytest, cv=k)
    return multi_regr,y_pred13

def RegresionEleccion(df2,cve,k): # df2: Muestra para ML
    L1,L1_test,L1_pred,L1_er,L1_reg=[],[],[],[],[]
    SCL1=[]
    for i in range(0,30):
        # Entrenamientos
        Xtodos_train, Xtodos_test, ytodos_train, ytodos_test=Entrenamiento(df2,0.2)
        # Escalas
        Xtodos_train, Xtodos_test,scl1 =Escalas(cve, Xtodos_train, Xtodos_test)
        # Regresiones            
        regr1,y_pred13=Regresion(Xtodos_train, Xtodos_test,ytodos_train,ytodos_test,k)

        E=porcentajeerror(ytodos_test,y_pred13)
        a=sum(E["Cantidad_Est_Relativa"][0:3])
        L1.append(a) # Lista con las cantidades de errores menores que +-15%
        L1_test.append(ytodos_test)
        L1_pred.append(y_pred13)
        L1_er.append(max(abs(ytodos_test-y_pred13)))
        L1_reg.append(regr1)
        SCL1.append(scl1)

    L1_T=L1_test[0]
    L1_P=L1_pred[0]
    L1_R=L1_reg[0]
    L1_E=L1_er[0]
    L1_F=L1[0]
    SCL1_F=SCL1[0]
    for k in range(0,len(L1)):
        if L1[k]>=L1_F and L1_er[k]<L1_E:
            L1_T=L1_test[k]
            L1_P=L1_pred[k]
            L1_R=L1_reg[k]
            L1_E=L1_er[k]
            L1_F=L1[k]
            SCL1_F=SCL1[k]
    ytodos_test,y_pred13,regr1=L1_T,L1_P,L1_R
    # Se guarda el escalamiento para cada forma con la que se trabajan los datos de entrada
    scaler1_file = "escalaRL_Oferta_"+str(cve)+".save"
    joblib.dump(SCL1_F, scaler1_file)
    print("Regresión lineal se ha ejecutado con éxito. Se procederá a guardar los resultados.")
    joblib.dump(regr1,"Rlineal_Oferta_"+str(cve)+".joblib")
    return SCL1_F,ytodos_test,y_pred13,regr1
# ElasticNet para uno
def ELasticNet(Xlrinter_train, Xlrinter_test,yrlinter_train,yrlinter_test,CV):
    ENet_models = {}
    training_scores = []
    test_scores = []
    L1_ratio=[0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1]
    for l1_ratio in L1_ratio:
        if not sys.warnoptions:
            import warnings
            warnings.simplefilter("ignore")
        ENet = ElasticNet(alpha=1,l1_ratio=l1_ratio,max_iter=8000).fit(Xlrinter_train, yrlinter_train)
        training_scores.append(ENet.score(Xlrinter_train, yrlinter_train))
        test_scores.append(ENet.score(Xlrinter_test, yrlinter_test))
        ENet_models[l1_ratio] = ENet
    a_aux,a=0,0
    for k in range(0,len(L1_ratio)):
        if test_scores[k]>test_scores[a_aux]:
            a_aux=k
            a=L1_ratio[k]
        if not sys.warnoptions:
            import warnings
            warnings.simplefilter("ignore")
    ENet=ENet_models[a]
    ENet.fit(Xlrinter_train, yrlinter_train)
    y_pred23 = cross_val_predict(ENet, Xlrinter_test, np.ravel(yrlinter_test), cv=CV)
    if not sys.warnoptions:
        import warnings
        warnings.simplefilter("ignore")
    return ENet,y_pred23

def ELasticNetEleccion(df2,cve):
    L1,L1_test,L1_pred,L1_er,L1_ENet=[],[],[],[],[]
    SCL2=[]
    for i in range(0,20):
        # Entrenamientos
        Xtodos_train, Xtodos_test, ytodos_train, ytodos_test=Entrenamiento(df2,0.2)
        # Escalas
        Xtodos_train, Xtodos_test,scl2 =Escalas(cve, Xtodos_train, Xtodos_test)
        # ElasticNets
        ENet1,y_pred23=ELasticNet(Xtodos_train,Xtodos_test,ytodos_train,ytodos_test,10)
        E=porcentajeerror(ytodos_test,y_pred23)
        a=sum(E["Cantidad_Est_Relativa"][0:3])
        L1.append(a) # Lista con las cantidades de errores menores que +-15%
        L1_test.append(ytodos_test)
        L1_pred.append(y_pred23)
        L1_er.append(max(abs(ytodos_test-y_pred23)))
        L1_ENet.append(ENet1)
        SCL2.append(scl2)

    L1_T=L1_test[0]
    L1_P=L1_pred[0]
    L1_R=L1_ENet[0]
    L1_E=L1_er[0]
    L1_F=L1[0]
    SCL2_F=SCL2[0]
    for k in range(0,len(L1)):
        if L1[k]>=L1_F and L1_er[k]<L1_E:
            L1_T=L1_test[k]
            L1_P=L1_pred[k]
            L1_R=L1_ENet[k]
            L1_E=L1_er[k]
            L1_F=L1[k]
            SCL2_F=SCL2[k]
    ytodos_test,y_pred23,ENet1,scl2=L1_T,L1_P,L1_R,SCL2_F
    scaler1_file = "escalaEN_Oferta_"+str(cve)+".save"
    joblib.dump(scl2, scaler1_file) 
    print("Elastic Net se ha ejecutado con éxito. Se procederá a guardar los resultados.")
    joblib.dump(ENet1,"ElasticNet_Oferta_"+str(cve)+".joblib")
    return scl2,ytodos_test,y_pred23,ENet1

## Random Forest para un par de datos
def RForest(Xtrain,Xtest,ytrain,ytest,k):
    rforest = RandomForestRegressor(max_features=7,random_state=42)  
    params={'n_estimators':[300,400,500,600,800],
           'max_depth':[30,50,70,90]}  
    Search=GridSearchCV(estimator=rforest,
                       param_grid=params,
                       n_jobs=-1)
    rforest1=Search.fit(Xtrain,ytrain)
    rforest1.best_estimator_
    y_pred43 = cross_val_predict(rforest1, Xtest, np.ravel(ytest), cv=k)
    return rforest1,y_pred43

def RForestEleccion(df2,cve,k):
    # Entrenamiento
    Xtodos_train, Xtodos_test, ytodos_train, ytodos_test=Entrenamiento(df2,0.2)
    # Escala
    Xtodos_train, Xtodos_test,scl3 =Escalas(cve, Xtodos_train, Xtodos_test)
    # Random Forest
    rforest1,y_pred43=RForest(Xtodos_train,Xtodos_test,ytodos_train,ytodos_test,k)

    scaler1_file = "escalaRF_Oferta_"+str(cve)+".save"
    joblib.dump(scl3, scaler1_file)
    print("El método de Random Forest se ha ejecutado con éxito. Se procederá a guardar los resultados.")
    joblib.dump(rforest1,"RForest_Oferta_"+str(cve)+".joblib")
    return scl3,ytodos_test,y_pred43,rforest1

# XGB para un par de datos
def XGB(Xtrain,Xtest,ytrain,ytest,k):
    xg=xgb.XGBRegressor(objective="reg:squarederror",alpha=1)
    colsample= [0.4,0.6,0.8]
    lr=[0.05,0.1]
    max_d=[25,45,60,80]
    n_est=[400,550,700]
    params={"colsample_bytree":colsample,"learning_rate":lr,"max_depth":max_d,"n_estimators":n_est}
    search=GridSearchCV(estimator=xg,param_grid=params,n_jobs=-1)
    search_model=search.fit(Xtrain,ytrain)
    search_model.best_params_                    
    y_pred63 = cross_val_predict(search_model, Xtest, np.ravel(ytest), cv=k)
    return search_model,y_pred63

def XGB_Eleccion(df2,cve,k):
    # Entrenamientos
    Xtodos_train, Xtodos_test, ytodos_train, ytodos_test=Entrenamiento(df2,0.2)
    # Escalas
    Xtodos_train, Xtodos_test,scl4 =Escalas(cve, Xtodos_train, Xtodos_test)
    # XGBs
    xgb1,y_pred43=XGB(Xtodos_train,Xtodos_test,ytodos_train,ytodos_test,k)

    scaler1_file = "escalaXGB_Oferta_"+str(cve)+".save"
    joblib.dump(scl4, scaler1_file)
    print("El método de Extreme Gradient Boosting se ha ejecutado con éxito. Se procederá a guardar los resultados.")
    joblib.dump(xgb1,"XGB_Oferta_"+str(cve)+".joblib")
    return scl4,ytodos_test,y_pred43,xgb1

# Error para los 4 modelos
def porcentajeerror2(a,b,c,d,e,f,g,h):
    r1=100*(b-a)/a;
    rr1=r1.tolist();
    r2=100*(d-c)/c;
    rr2=r2.tolist();
    r3=100*(f-e)/e;
    rr3=r3.tolist();
    r4=100*(h-g)/g;
    rr4=r4.tolist();
    
    tabla= pd.DataFrame.from_dict({'Intervalo':[],
                                '%_Est_Regresión': [],'Cantidad_Est_Regresión': [],
                                '%_Est_ElasticNet': [],'Cantidad_Est_ElasticNet': [],
                                '%_Est_RandomForest': [],'Cantidad_Est_RandomForest': [],
                                 '%_Est_XGboosting': [],'Cantidad_Est_XGboosting':[]});
    col = ['Intervalo','%_Est_Regresión','Cantidad_Est_Regresión','%_Est_ElasticNet','Cantidad_Est_ElasticNet',
        '%_Est_RandomForest','Cantidad_Est_RandomForest', '%_Est_XGboosting','Cantidad_Est_XGboosting'];
    cant=[0,0,0,0]
    k=[5,10,15,20,25,50]
    for lim in range(0,len(k)):
        if k[lim]==5:
            inter=f"|Error|<={k[lim]} %"
        else: 
            inter=f"{k[lim-1]}% <|Error|<={k[lim]}%"
        porcentaje1=100*sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr1))/len(rr1)
        cantidad1=sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr1))-cant[0]
        porcentaje2=100*sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr2))/len(rr2)
        cantidad2=sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr2))-cant[1]
        porcentaje3=100*sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr3))/len(rr3)
        cantidad3=sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr3))-cant[2]
        porcentaje4=100*sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr4))/len(rr4)
        cantidad4=sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr4))-cant[3]
        cant=[cant[0]+cantidad1,cant[1]+cantidad2,cant[2]+cantidad3,cant[3]+cantidad4]
      
        tablaux = pd.DataFrame([[inter,porcentaje1,cantidad1,porcentaje2,cantidad2,porcentaje3,cantidad3,porcentaje4,cantidad4]],
                              columns=col);
        tabla=pd.concat([tabla, tablaux],ignore_index=True);
    return tabla
# Estadisticas de los errores de los 4 modelos
def Tabla_Estadistica_Error(y11,y12,y21,y22,y31,y32,y41,y42):
    E_regr=[]
    E_ElasticNet=[]
    E_RForest=[]
    E_XGB=[]
    Sobreestimados1=0
    Sobreestimados2=0
    Sobreestimados3=0
    Sobreestimados4=0
    Subestimados1=0
    Subestimados2=0
    Subestimados3=0
    Subestimados4=0
    Estimados1=0
    Estimados2=0
    Estimados3=0
    Estimados4=0
    for i in range(0,len(y11)):
        E_regr.append(y11[i]-y12[i])
        if y11[i]-y12[i]<0:
            Sobreestimados1+=1
        elif y11[i]-y12[i]>0:
            Subestimados1+=1
        Estimados1+=1
    for i in range(0,len(y21)):
        E_ElasticNet.append(y21[i]-y22[i])
        if y21[i]-y22[i]<0:
            Sobreestimados2+=1
        elif y21[i]-y22[i]>0:
            Subestimados2+=1
        Estimados2+=1
    for i in range(0,len(y31)):
        E_RForest.append(y31[i]-y32[i])
        if y31[i]-y32[i]<0:
            Sobreestimados3+=1
        elif y31[i]-y32[i]>0:
            Subestimados3+=1
        Estimados3+=1
    for i in range(0,len(y41)):
        E_XGB.append(y41[i]-y42[i])
        if y41[i]-y42[i]<0:
            Sobreestimados4+=1
        elif y41[i]-y42[i]>0:
            Subestimados4+=1
        Estimados4+=1
    Sobreestimados=[Sobreestimados1,Sobreestimados2,Sobreestimados3,Sobreestimados4]
    Subestimados=[Subestimados1,Subestimados2,Subestimados3,Subestimados4]
    Estimados=[Estimados1,Estimados2,Estimados3,Estimados4]
    tabla= pd.DataFrame.from_dict({'Método':[],
                                'Media': [],'Desviación estándar': [],"Rango":[],
                                'Mediana': [],"Cuartil 1": [],
                                "Cuartil 3": [],"Datos sobreestimados":[], "Datos subestimados":[],"Datos Estimados":[]});
    col = ['Método','Media','Desviación estándar',"Rango",'Mediana','Cuartil 1',"Cuartil 3","Datos sobreestimados",
        "Datos subestimados","Datos Estimados"];
    inter=["Regresión lineal","Elastic Net","Random Forest", "Xtreme Gradient Boosting"]
    media=[np.mean(E_regr),np.mean(E_ElasticNet),np.mean(E_RForest),np.mean(E_XGB)]
    ds=[np.std(E_regr),np.std(E_ElasticNet),np.std(E_RForest),np.std(E_XGB)] 
    med=[np.percentile(E_regr,50),np.percentile(E_ElasticNet,50),np.percentile(E_RForest,50),np.percentile(E_XGB,50)]
    Cuart1=[np.percentile(E_regr,25),np.percentile(E_ElasticNet,25),np.percentile(E_RForest,25),np.percentile(E_XGB,25)]
    Cuart3=[np.percentile(E_regr,75),np.percentile(E_ElasticNet,75),np.percentile(E_RForest,75),np.percentile(E_XGB,75)]
    Rango=[max(E_regr)-min(E_regr),max(E_ElasticNet)-min(E_ElasticNet),max(E_RForest)-min(E_RForest),max(E_XGB)-min(E_XGB)]
    for i in range(0,4):
        tablaux = pd.DataFrame([[inter[i],media[i],ds[i],Rango[i],med[i],Cuart1[i],Cuart3[i],Sobreestimados[i],Subestimados[i],Estimados[i]]],
                                  columns=col);
        tabla=pd.concat([tabla, tablaux],ignore_index=True);
    return tabla

##################### PARTE 3 #########################

def InsertColumnasAVM(reavm):
    reavm.insert(reavm.shape[1],'% de error',
             100*(reavm.loc[:,'Estimación AVM']-reavm.loc[:,'valor_uf'])/reavm.loc[:,'valor_uf'],
             True)
    reavm.insert(reavm.shape[1],'error AVM',reavm['Estimación AVM']-reavm['valor_uf'],True)
    return reavm

def Is_estimated_by_AVM(reavm):
    reavm1=reavm.loc[reavm.loc[:,'Estimación AVM']<=0]
    print(f"La cantidad de datos no estimados por AVM es de: {len(reavm[reavm['Estimación AVM']<=0])}")
    print(f"Cuyo porcentaje equivale a: {(len(reavm[reavm['Estimación AVM']<=0])*100)/reavm.shape[0]: .2f}%")
    reavm2=reavm.loc[reavm.loc[:,'Estimación AVM']>0]
    print(f"La cantidad de datos estimados por AVM es de: {len(reavm[reavm['Estimación AVM']>0])}")
    print(f"Cuyo porcentaje equivale a: {(len(reavm[reavm['Estimación AVM']>0])*100)/reavm.shape[0]: .2f}%")
    return reavm1,reavm2

def Rend_Est_AVM(reavm2):
    plt.rcParams['figure.figsize'] = (9,5);
    sns.scatterplot(data=reavm2,x='valor_uf',y='Estimación AVM',color="#008080")
    plt.plot(reavm2['valor_uf'],reavm2['valor_uf'],color="red")
    plt.plot(reavm2['valor_uf'],reavm2['valor_uf']*(1.05),color="blue")
    plt.plot(reavm2['valor_uf'],reavm2['valor_uf']*(0.95),color="blue")
    plt.plot(reavm2['valor_uf'],reavm2['valor_uf']*(1.2),color="orange")
    plt.plot(reavm2['valor_uf'],reavm2['valor_uf']*(0.8),color="orange")
    plt.legend(["Datos","Recta ajustada a los datos","Error del +5%","Error del -5%","Error del +20%","Error del -20%"],bbox_to_anchor=(1, 1), loc='upper left')
    plt.title("Datos estimados por el AVM",size=16)
    plt.xlabel('Valor Observado');
    plt.ylabel('Valor Estimado AVM');
    plt.grid(True)
    plt.show()
    
# Selección de datos del AVM para escalar

def SCL_model(scl,Xtodos,modelo):
    Xtodos=scl.transform(Xtodos)
    ValEst_mod=modelo.predict(Xtodos)
    return ValEst_mod

def InsertColumnsML(reml2,ValEst_RL,ValEst_EN,ValEst_RF,ValEst_XGB):
    reml2.insert(reml2.shape[1],'ValEst_RL',ValEst_RL,True)
    reml2.insert(reml2.shape[1],'ValEst_EN',ValEst_EN,True)
    reml2.insert(reml2.shape[1],'ValEst_RF',ValEst_RF,True)
    reml2.insert(reml2.shape[1],'ValEst_XGB',ValEst_XGB,True)
    reml2.insert(reml2.shape[1],'% de error RL',100*(reml2['ValEst_RL']-reml2['valor_uf'])/reml2['valor_uf'],True)
    reml2.insert(reml2.shape[1],'error RL',reml2['ValEst_RL']-reml2['valor_uf'],True)

    reml2.insert(reml2.shape[1],'% de error EN',100*(reml2['ValEst_EN']-reml2['valor_uf'])/reml2['valor_uf'],True)
    reml2.insert(reml2.shape[1],'error EN',reml2['ValEst_EN']-reml2['valor_uf'],True)

    reml2.insert(reml2.shape[1],'% de error RF',100*(reml2['ValEst_RF']-reml2['valor_uf'])/reml2['valor_uf'],True)
    reml2.insert(reml2.shape[1],'error RF',reml2['ValEst_RF']-reml2['valor_uf'],True)

    reml2.insert(reml2.shape[1],'% de error XGB',100*(reml2['ValEst_XGB']-reml2['valor_uf'])/reml2['valor_uf'],True)
    reml2.insert(reml2.shape[1],'error XGB',reml2['ValEst_XGB']-reml2['valor_uf'],True)
    return reml2

def Rend_Est_ML(reml2):
    fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(14, 10))

    axs[0,0].scatter(reml2['valor_uf'],reml2['ValEst_RL'],color="#008080");
    axs[0,0].plot(reml2['valor_uf'],reml2['valor_uf']*(1.05),color="blue")
    axs[0,0].plot(reml2['valor_uf'],reml2['valor_uf']*(0.95),color="blue")
    axs[0,0].plot(reml2['valor_uf'],reml2['valor_uf']*(1.2),color="orange")
    axs[0,0].plot(reml2['valor_uf'],reml2['valor_uf']*(0.8),color="orange")
    axs[0,0].plot(reml2['valor_uf'],reml2['valor_uf'],color="red")
    axs[0,0].set_xlabel('Valor Observado')
    axs[0,0].set_ylabel('Valor Estimado')
    axs[0,0].set_title('Regresión Lineal')
    axs[0,0].grid(True)

    axs[0,1].scatter(reml2['valor_uf'],reml2['ValEst_EN'],color="#008080");
    axs[0,1].plot(reml2['valor_uf'],reml2['valor_uf']*(1.05),color="blue")
    axs[0,1].plot(reml2['valor_uf'],reml2['valor_uf']*(0.95),color="blue")
    axs[0,1].plot(reml2['valor_uf'],reml2['valor_uf']*(1.2),color="orange")
    axs[0,1].plot(reml2['valor_uf'],reml2['valor_uf']*(0.8),color="orange")
    axs[0,1].plot(reml2['valor_uf'],reml2['valor_uf'],color="red")
    axs[0,1].set_xlabel('Valor Observado')
    axs[0,1].set_ylabel('Valor Estimado')
    axs[0,1].set_title('ElasticNet')
    axs[0,1].grid(True)

    axs[1,0].scatter(reml2['valor_uf'],reml2['ValEst_RF'],color="#008080");
    axs[1,0].plot(reml2['valor_uf'],reml2['valor_uf'],color="red")
    axs[1,0].plot(reml2['valor_uf'],reml2['valor_uf']*(1.05),color="blue")
    axs[1,0].plot(reml2['valor_uf'],reml2['valor_uf']*(0.95),color="blue")
    axs[1,0].plot(reml2['valor_uf'],reml2['valor_uf']*(1.2),color="orange")
    axs[1,0].plot(reml2['valor_uf'],reml2['valor_uf']*(0.8),color="orange")
    axs[1,0].set_xlabel('Valor Observado')
    axs[1,0].set_ylabel('Valor Estimado')
    axs[1,0].set_title('Random Forest')
    axs[1,0].grid(True)

    axs[1,1].scatter(reml2['valor_uf'],reml2['ValEst_XGB'],color="#008080");
    axs[1,1].plot(reml2['valor_uf'],reml2['valor_uf'],color="red")
    axs[1,1].plot(reml2['valor_uf'],reml2['valor_uf']*(1.05),color="blue")
    axs[1,1].plot(reml2['valor_uf'],reml2['valor_uf']*(0.95),color="blue")
    axs[1,1].plot(reml2['valor_uf'],reml2['valor_uf']*(1.2),color="orange")
    axs[1,1].plot(reml2['valor_uf'],reml2['valor_uf']*(0.8),color="orange")
    axs[1,1].set_xlabel('Valor Observado')
    axs[1,1].set_ylabel('Valor Estimado')
    axs[1,1].set_title('Extreme Gradient Boosting')
    axs[1,1].grid(True)

    plt.show()
    
def atypicals_be_goneAVM(df,pars,T,metodo,limit): 
    ## Eliminación de atípicos  
    n_i=df.shape[0]
    for j in range(0,len(pars)):
        w=1
        if T==True:
            print(f'Eliminación de atípicos considerando: {pars[j]}')
        while (w!=0):
            [w,resum]=outliers_col(df,pars[j],df.shape[0],metodo,T,n_i,limit);
            df=outliers_col_eliminacion(df,pars[j],metodo,limit);
    return df
    
def Error_AVM_vs_ML(reml2):
    real=reml2['valor_uf']
    estimadoavm=reml2['Estimación AVM']
    estimado1=reml2['ValEst_RL']
    estimado2=reml2['ValEst_EN']
    estimado3=reml2['ValEst_RF']
    estimado4=reml2['ValEst_XGB']
    r=100*(estimadoavm-real)/real 
    rr=r.tolist();
    r1=100*(estimado1-real)/real;
    rr1=r1.tolist();
    r2=100*(estimado2-real)/real;
    rr2=r2.tolist();
    r3=100*(estimado3-real)/real;
    rr3=r3.tolist();
    r4=100*(estimado4-real)/real;
    rr4=r4.tolist();

    tabla= pd.DataFrame.from_dict({'Intervalo':[],
                                   '%_AVM_Acumulado': [],'Cantidad_AVM': [],
                                   '%_RL_Acumulado': [],'Cantidad_RL': [],
                                   '%_EN_Acumulado': [],'Cantidad_EN': [],
                                   '%_RF_Acumulado': [],'Cantidad_RF': [],
                                   '%_XGB_Acumulado': [],'Cantidad_XGB': []});

    col = ['Intervalo','%_AVM_Acumulado','Cantidad_AVM','%_RL_Acumulado','Cantidad_RL', '%_EN_Acumulado','Cantidad_EN',
                                   '%_RF_Acumulado','Cantidad_RF', "%_XGB_Acumulado",'Cantidad_XGB'];
    cant=[0,0,0,0,0]
    k=[5,10,15,20,25,50]
    for lim in range(0,len(k)):
        if k[lim]==5:
            inter=f"|Error|<={k[lim]} %"
        else: 
            inter=f"{k[lim-1]}% <|Error|<={k[lim]}%"
        porcentajeavm=100*sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr))/len(rr)
        cantidadavm=sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr))-cant[0]
        porcentaje1=100*sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr1))/len(rr1)
        cantidad1=sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr1))-cant[1]
        porcentaje2=100*sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr2))/len(rr2)
        cantidad2=sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr2))-cant[2]
        porcentaje3=100*sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr3))/len(rr3)
        cantidad3=sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr3))-cant[3]
        porcentaje4=100*sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr4))/len(rr4)
        cantidad4=sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr4))-cant[4]
        cant=[cant[0]+cantidadavm,cant[1]+cantidad1,cant[2]+cantidad2,cant[3]+cantidad3,cant[4]+cantidad4]


        tablaux = pd.DataFrame([[inter,porcentajeavm,cantidadavm,
                                 porcentaje1,cantidad1,porcentaje2,cantidad2,
                                 porcentaje3,cantidad3,porcentaje4,cantidad4]],
                                columns=col);
        tabla=pd.concat([tabla, tablaux],ignore_index=True);
    return tabla

def Tabla_Estadistica_Error2(df):
    E_AVM=df.loc[:,"error AVM"]
    E_regr=df.loc[:,"error RL"]
    E_ElasticNet=df.loc[:,"error EN"]
    E_RForest=df.loc[:,"error RF"]
    E_XGB=df.loc[:,"error XGB"]
    Sobreestimados1=len(E_AVM[E_AVM>0])
    Sobreestimados2=len(E_regr[E_regr>0])
    Sobreestimados3=len(E_ElasticNet[E_ElasticNet>0])
    Sobreestimados4=len(E_RForest[E_RForest>0])
    Sobreestimados5=len(E_XGB[E_XGB>0])
    Subestimados1=len(E_AVM[E_AVM<0])
    Subestimados2=len(E_regr[E_regr<0])
    Subestimados3=len(E_ElasticNet[E_ElasticNet<0])
    Subestimados4=len(E_RForest[E_RForest<0])
    Subestimados5=len(E_XGB[E_XGB<0])
    Estimados1=Sobreestimados1+Subestimados1+len(E_AVM[E_AVM==0])
    Estimados2=Sobreestimados2+Subestimados2+len(E_regr[E_regr==0])
    Estimados3=Sobreestimados3+Subestimados3+len(E_ElasticNet[E_ElasticNet==0])
    Estimados4=Sobreestimados4+Subestimados4+len(E_RForest[E_RForest==0])
    Estimados5=Sobreestimados5+Subestimados5+len(E_XGB[E_XGB==0])
    
    Sobreestimados=[Sobreestimados1,Sobreestimados2,Sobreestimados3,Sobreestimados4,Sobreestimados5]
    Subestimados=[Subestimados1,Subestimados2,Subestimados3,Subestimados4,Subestimados5]
    Estimados=[Estimados1,Estimados2,Estimados3,Estimados4,Estimados5]
    
    tabla= pd.DataFrame.from_dict({'Método':[],
                                'Media': [],'Desviación estándar': [],"Rango":[],
                                'Mediana': [],"Cuartil 1": [],
                                "Cuartil 3": [],"Datos sobreestimados":[], "Datos subestimados":[],"Datos estimados":[]});
    col = ['Método','Media','Desviación estándar',"Rango",'Mediana','Cuartil 1',"Cuartil 3","Datos sobreestimados",
        "Datos subestimados","Datos estimados"];
    inter=["AVM","Regresión lineal","Elastic Net","Random Forest", "Xtreme Gradient Boosting"]
    media=[E_AVM.mean(),np.mean(E_regr),np.mean(E_ElasticNet),np.mean(E_RForest),np.mean(E_XGB)]
    ds=[E_AVM.std(),np.std(E_regr),np.std(E_ElasticNet),np.std(E_RForest),np.std(E_XGB)] 
    med=[E_AVM.median(),np.percentile(E_regr,50),np.percentile(E_ElasticNet,50),np.percentile(E_RForest,50),np.percentile(E_XGB,50)]
    Cuart1=[np.percentile(E_AVM,25),np.percentile(E_regr,25),np.percentile(E_ElasticNet,25),np.percentile(E_RForest,25),np.percentile(E_XGB,25)]
    Cuart3=[np.percentile(E_AVM,75),np.percentile(E_regr,75),np.percentile(E_ElasticNet,75),np.percentile(E_RForest,75),np.percentile(E_XGB,75)]
    Rango=[max(E_AVM)-min(E_AVM),max(E_regr)-min(E_regr),max(E_ElasticNet)-min(E_ElasticNet),max(E_RForest)-min(E_RForest),max(E_XGB)-min(E_XGB)]
    for i in range(0,5):
        tablaux = pd.DataFrame([[inter[i],media[i],ds[i],Rango[i],med[i],Cuart1[i],Cuart3[i],Sobreestimados[i],Subestimados[i],
                                Estimados[i]]],
                                  columns=col);
        tabla=pd.concat([tabla, tablaux],ignore_index=True);
    return tabla

def ModeloFinal(reml2,scls,models,cve):
    Menor50=[] # Lista para guardar los 2 modelos con menor cantidad de datos sobre el 50% de error
    indice=[]
    RL_er=np.array(list(map(abs, reml2['% de error RL'].tolist())))
    EN_er=np.array(list(map(abs, reml2['% de error EN'].tolist())))
    RF_er=np.array(list(map(abs, reml2['% de error RF'].tolist())))
    XGB_er=np.array(list(map(abs, reml2['% de error XGB'].tolist())))
    L=[RL_er,EN_er,RF_er,XGB_er] #Lista 
    a1=len(RL_er[RL_er>20])
    a2=len(EN_er[EN_er>20])
    a3=len(RF_er[RF_er>20])
    a4=len(XGB_er[XGB_er>20])
    a,A=[a1,a2,a3,a4],[a1,a2,a3,a4]
    A.sort()
    for i in range(0,4):
        if a[i]==A[0] or a[i]==A[1]:
            Menor50.append(L[i])
            indice.append(i)
        if len(Menor50)==2:
            break
    M0,M1=Menor50[0],Menor50[1]
    b0=len(M0[M0<10])
    b1=len(M1[M1<10])
    B=[b0,b1]
    for i in range(0,2):
        if B[i]==max(B):
            Model_F=Menor50[i]
            k=indice[i]
    if k==0:
        print("El método escogido de manera definitiva será el de regresión lineal. Se procede a guardarlo")
        scaler_file = "escala_Final_Oferta_"+str(cve)+".save"
        joblib.dump(scls[0], scaler_file)
        joblib.dump(models[0],"Modelo_Final_Oferta_"+str(cve)+".joblib")
        return models[0],scls[0]
    elif k==1:
        print("El método escogido de manera definitiva será el de Elastic Net. Se procede a guardarlo")
        scaler_file = "escala_Final_Oferta_"+str(cve)+".save"
        joblib.dump(scls[1], scaler_file)
        joblib.dump(models[1],"Modelo_Final_Oferta_"+str(cve)+".joblib")
        return models[1],scls[1]
    elif k==2:
        print("El método escogido de manera definitiva será el de Random Forest. Se procede a guardarlo")
        scaler_file = "escala_Final_Oferta_"+str(cve)+".save"
        joblib.dump(scls[2], scaler_file)
        joblib.dump(models[2],"Modelo_Final_Oferta_"+str(cve)+".joblib")
        return models[2],scls[2]
    elif k==3:
        print("El método escogido de manera definitiva será el Extreme Gradient Boosting. Se procede a guardarlo")
        scaler_file = "escala_Final_Oferta_"+str(cve)+".save"
        joblib.dump(scls[3], scaler_file)
        joblib.dump(models[3],"Modelo_Final_Oferta_"+str(cve)+".joblib")
        return models[3],scls[3]