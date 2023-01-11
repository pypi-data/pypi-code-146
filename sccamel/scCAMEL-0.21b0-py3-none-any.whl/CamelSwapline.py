# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn import manifold
from collections import defaultdict
#from mpl_toolkits.mplot3d import Axes3D
import math
import sklearn
import scipy
import openpyxl
import os
import sys
#imports
import pandas as pd
import pickle as pickle
from scipy.spatial.distance import cdist, pdist, squareform
#import backspinpy
#from backspinpy import fit_CV
#from backspinpy.Cef_tools import *
#from __future__ import division
import pandas as pd
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
#from sklearn.cross_validation import StratifiedShuffleSplit
from collections import defaultdict
from sklearn import preprocessing
import matplotlib.patches as mpatches
from sklearn.decomposition import PCA
import umap
import scipy
from scipy import sparse
from sklearn.metrics import pairwise_distances
# with pickle
import logging
from scipy.sparse import issparse, coo_matrix
import pickle
import random

import seaborn as sns

import datetime
import seaborn as sns
import pandas as pd
import pickle as pickle
from scipy.spatial.distance import cdist, pdist, squareform
#import backspinpy
import pandas as pd
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.model_selection import StratifiedShuffleSplit
from collections import defaultdict
from sklearn import preprocessing
import matplotlib.patches as mpatches
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
from scipy.spatial import distance
from scipy.cluster import hierarchy
import seaborn as sns
import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.utils.data as Data
import torchvision
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import torch.utils.data as data_utils
from matplotlib import cm
import numpy as np
import pandas as pd
import pickle as pickle
from scipy.spatial.distance import cdist, pdist, squareform
#import backspinpy
import pandas as pd
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.model_selection import StratifiedShuffleSplit
from collections import defaultdict
from sklearn import preprocessing
import matplotlib.patches as mpatches
import torch.nn.functional as F
import math
from scipy.stats import ranksums
#import gpytorch

from scipy import sparse
import urllib.request
import os.path
from scipy.io import loadmat
from math import floor
#from matplotlib.legend_handler import Handler

def package_version():
    alllist=[]
    for m in globals().values():
        if getattr(m, '__version__', None):
            alllist.append(f'{m.__name__}=={m.__version__}')
    return alllist

def shannon_entropy(S, mode="discrete"):
    """
    https://stackoverflow.com/questions/42683287/python-numpy-shannon-entropy-array
    """
    S = np.asarray(S)
    pS = S / S.sum()
    # Remove zeros
    if mode == "continuous":
        return -np.sum(pS*np.log2(S))
    if mode == "discrete":
        pS = pS[np.nonzero(pS)[0]]
        return -np.sum(pS*np.log2(pS))


def PurityEstimationLearningScore(datax, clusterlist,  elbow=True, figureplot=True):
    cluslist = list(set(datax.obs[clusterlist]))
    entropyValue1=[]
    for item in cluslist:
        scpd1 = datax[datax.obs[clusterlist] == item]
        X_pcavalue=np.array(scpd1.obsm['Celltype_Score'])
        v0 = shannon_entropy(
            (X_pcavalue[:, 0] - X_pcavalue[:, 0].min()) / (X_pcavalue[:, 0].max() - X_pcavalue[:, 0].min()))
        v0=v0/scpd1.shape[0]
        num=X_pcavalue.shape[1]
        for i in range(1, num):
            vtemp = shannon_entropy(
                (X_pcavalue[:, i] - X_pcavalue[:, i].min()) / (X_pcavalue[:, i].max() - X_pcavalue[:, i].min()))
            vtemp=vtemp/scpd1.shape[0]
            v0 = v0 * vtemp
        entropyValue1.append(v0 ** (-1 / num))
    entropyValue2=[]
    for item in cluslist:
        scpd1 = datax[datax.obs[clusterlist] == item]
        X_pcavalueAll=np.array(scpd1.obsm['Celltype_Score'])
        orishape=X_pcavalueAll.shape
        arr=X_pcavalueAll.flatten()
        np.random.shuffle(arr)
        X_pcavalue=arr.reshape(orishape)
        #datax.obsm["PCAall"]=X_pcavalueAllnew
        v0 = shannon_entropy(
            (X_pcavalue[:, 0] - X_pcavalue[:, 0].min()) / (X_pcavalue[:, 0].max() - X_pcavalue[:, 0].min()))
        v0=v0/scpd1.shape[0]
        num=X_pcavalue.shape[1]
        for i in range(1, num):
            vtemp = shannon_entropy(
                (X_pcavalue[:, i] - X_pcavalue[:, i].min()) / (X_pcavalue[:, i].max() - X_pcavalue[:, i].min()))
            vtemp=vtemp/scpd1.shape[0]
            v0 = v0 * vtemp
        entropyValue2.append(v0 ** (-1 / num))
    entropyValue=np.array(entropyValue2)/np.array(entropyValue1)-1
    dfsort = pd.DataFrame([cluslist, entropyValue]).T
    dfsort.columns = ["Name", "Values"]
    dfsort = dfsort.sort_values(["Values"], ascending=False)
    dfsort["Purity"] = [1] * dfsort.shape[0]
    if elbow==True:
        from kneed import KneeLocator
        kn = KneeLocator(range(0, dfsort.shape[0]), dfsort["Values"], curve='convex', direction='decreasing')
        dfsort["Purity"][:(kn.knee + 1)] = 0
    if figureplot:
        fig = plt.figure()
        fig, ax = plt.subplots(figsize=(7, 7))
        plt.scatter(dfsort["Name"], dfsort["Values"], s=100)
        plt.xticks(rotation=70, fontsize=15)
        plt.yticks(rotation=0, fontsize=15)
        if elbow==True:
            plt.axvline(dfsort["Name"].values[kn.knee], c='r', alpha=0.8, linestyle='dashed')
        plt.ylabel('LearningScore_Normalized Purity', position=(0, 0.5), color=(0.2, 0.2, 0.2),
                   alpha=0.8, fontsize=20)
        plt.xlabel("Cell Types", fontsize=20)
        ax.spines.right.set_visible(False)
        ax.spines.top.set_visible(False)
        plt.grid(False)
    return dfsort

def PurityEstimationPCA(datax, clusterlist, PCnum=10, elbow=True, figureplot=True):
    num = PCnum
    cluslist = list(set(datax.obs[clusterlist]))
    X = datax.X
    pca_ = PCA(n_components=min(datax.shape[0], num), svd_solver='auto', random_state=0)
    PCAmodel = pca_.fit(X)
        # X_cca,Y_cca=cca_.fit_transform(X,Y)
    X_pcavalueAll = abs(PCAmodel.transform(X))
    datax.obsm["PCAall"]=X_pcavalueAll
    entropyValue1 = []
    for item in cluslist:
        scpd1 = datax[datax.obs[clusterlist] == item]
        X_pcavalue=scpd1.obsm["PCAall"]
        v0 = shannon_entropy(
            (X_pcavalue[:, 0] - X_pcavalue[:, 0].min()) / (X_pcavalue[:, 0].max() - X_pcavalue[:, 0].min()))
        v0=v0/scpd1.shape[0]
        for i in range(1, num):
            vtemp = shannon_entropy(
                (X_pcavalue[:, i] - X_pcavalue[:, i].min()) / (X_pcavalue[:, i].max() - X_pcavalue[:, i].min()))
            vtemp=vtemp/scpd1.shape[0]
            v0 = v0 * vtemp
        entropyValue1.append(v0 ** (-1 / num))
    orishape=X_pcavalueAll.shape
    arr=X_pcavalueAll.flatten()
    np.random.shuffle(arr)
    X_pcavalueAllnew=arr.reshape(orishape)
    datax.obsm["PCAall"]=X_pcavalueAllnew
    entropyValue2=[]
    for item in cluslist:
        scpd1 = datax[datax.obs[clusterlist] == item]
        X_pcavalue=scpd1.obsm["PCAall"]
        v0 = shannon_entropy(
            (X_pcavalue[:, 0] - X_pcavalue[:, 0].min()) / (X_pcavalue[:, 0].max() - X_pcavalue[:, 0].min()))
        v0=v0/scpd1.shape[0]
        for i in range(1, num):
            vtemp = shannon_entropy(
                (X_pcavalue[:, i] - X_pcavalue[:, i].min()) / (X_pcavalue[:, i].max() - X_pcavalue[:, i].min()))
            vtemp=vtemp/scpd1.shape[0]
            v0 = v0 * vtemp
        entropyValue2.append(v0 ** (-1 / num))
    entropyValue=np.array(entropyValue2)/np.array(entropyValue1)-1
    dfsort = pd.DataFrame([cluslist, entropyValue]).T
    dfsort.columns = ["Name", "Values"]
    dfsort = dfsort.sort_values(["Values"], ascending=False)
    dfsort["Purity"] = [1] * dfsort.shape[0]
    if elbow==True:
        from kneed import KneeLocator
        kn = KneeLocator(range(0, dfsort.shape[0]), dfsort["Values"], curve='convex', direction='decreasing')
        dfsort["Purity"][:(kn.knee + 1)] = 0
    if figureplot:
        fig = plt.figure()
        fig, ax = plt.subplots(figsize=(7, 7))
        plt.scatter(dfsort["Name"], dfsort["Values"], s=100)
        plt.xticks(rotation=70, fontsize=15)
        plt.yticks(rotation=0, fontsize=15)
        if elbow==True:
            plt.axvline(dfsort["Name"].values[kn.knee], c='r', alpha=0.8, linestyle='dashed')
        plt.ylabel('%sPCs_Normalized Purity'%PCnum, position=(0, 0.5), color=(0.2, 0.2, 0.2),
                   alpha=0.8, fontsize=20)
        plt.xlabel("Cell Types", fontsize=20)
        ax.spines.right.set_visible(False)
        ax.spines.top.set_visible(False)
        plt.grid(False)
    return dfsort

def PurityEstimation(datax, clusterlist, PCnum=10, figureplot=True):
    entropyValue = []
    num = PCnum
    cluslist = list(set(datax.obs[clusterlist]))
    for item in cluslist:
        scpd1 = datax[datax.obs[clusterlist] == item]
        X = scpd1.X
        pca_ = PCA(n_components=min(scpd1.shape[0], num), svd_solver='auto', random_state=0)
        PCAmodel = pca_.fit(X)
        # X_cca,Y_cca=cca_.fit_transform(X,Y)
        X_pcavalue = abs(PCAmodel.transform(X))
        v0 = shannon_entropy(
            (X_pcavalue[:, 0] - X_pcavalue[:, 0].min()) / (X_pcavalue[:, 0].max() - X_pcavalue[:, 0].min()))
        for i in range(1, num):
            vtemp = shannon_entropy(
                (X_pcavalue[:, i] - X_pcavalue[:, i].min()) / (X_pcavalue[:, i].max() - X_pcavalue[:, i].min()))
            v0 = v0 * vtemp
        # v1=shannon_entropy((X_pcavalue[:,0]-X_pcavalue[:,0].min())/(X_pcavalue[:,0].max()-X_pcavalue[:,0].min()), mode="discrete", verbose=False)
        # v2=shannon_entropy((X_pcavalue[:,1]-X_pcavalue[:,1].min())/(X_pcavalue[:,1].max()-X_pcavalue[:,1].min()), mode="discrete", verbose=False)
        # v1=shannon_entropy((X_pcavalue.std(1)-X_pcavalue.std(1).min())/(X_pcavalue.std(1).max()-X_pcavalue.std(1).min()), mode="discrete", verbose=False)
        entropyValue.append(v0 ** (-(1 / num)))
    dfsort = pd.DataFrame([cluslist, entropyValue]).T
    dfsort.columns = ["Name", "Values"]
    dfsort = dfsort.sort_values(["Values"], ascending=False)
    from kneed import KneeLocator
    kn = KneeLocator(range(0, dfsort.shape[0]), dfsort["Values"], curve='convex', direction='decreasing')
    dfsort["Purity"] = [1] * dfsort.shape[0]
    dfsort["Purity"][:(kn.knee + 1)] = 0
    if figureplot:
        fig = plt.figure()
        fig, ax = plt.subplots(figsize=(7, 7))
        plt.scatter(dfsort["Name"], dfsort["Values"], s=100)
        plt.xticks(rotation=70, fontsize=15)
        plt.yticks(rotation=0, fontsize=15)
        plt.axvline(dfsort["Name"].values[kn.knee], c='r', alpha=0.8, linestyle='dashed')
        plt.ylabel('Normalized Entropy', position=(0, 0.5), color=(0.2, 0.2, 0.2),
                   alpha=0.8, fontsize=20)
        plt.xlabel("Cell Types", fontsize=20)
        ax.spines.right.set_visible(False)
        ax.spines.top.set_visible(False)
        plt.grid(False)
    return dfsort


def UMAPtrain(datax,NN=25,mdist=0.6, rd=173, n_comp=2):
    #XXdf, df with row cellID, with columns probability features, and the last column is clustername
    XX=datax.obsm["Celltype_Score"].astype(np.float32)
    umaptrain = umap.UMAP(n_neighbors=NN, min_dist=mdist,
                          # metric='correlation',
                          random_state=rd,
                          n_components=n_comp).fit(XX)
    datax.obsm['X_umap']= umaptrain.embedding_
    datax.obsm['X_draw_graph_fr'] = umaptrain.embedding_
    datax.obsm['X_CAMELumap'] = umaptrain.embedding_
    #dfg = pd.DataFrame(X_r)
    #dfg.index = XXdf.index
    #dfg2 = dfg.join(XXdf.iloc[:,-1:], how="inner")
    return datax, umaptrain


def EnrichScore_Ranksum(adata, foldchange=1, meanthreshold=0.05, pvalue=0.1):
    cluslist = list(set(adata.obs["Cluster"]))
    dfgrp = pd.DataFrame(adata.X.T, index=adata.var.index, columns=adata.obs.index).T
    dfgrp["Cluster"] = adata.obs["Cluster"]
    # dfgrp.shape
    markers = defaultdict(set)
    mkdict = {}
    sys.stdout.write("[%s]" % "Processing")
    sys.stdout.flush()
    sys.stdout.write("\b" * (50 + 1))  # return to start of line, after '['
    perc = len(cluslist)
    for ct in cluslist:
        temp = {}
        for num in range(min(2, int(len(cluslist) / 4) + 1), len(cluslist)):
            temp[num] = []
        dftemp1 = dfgrp.loc[dfgrp["Cluster"] == ct]
        # y=0

        itemindex = cluslist.index(ct)
        # setup toolbar

        sys.stdout.write("-%s%%-" % int(itemindex * 100 / perc))
        sys.stdout.flush()
        for mk in dfgrp.columns[:-1]:
            x = 0
            # y = 0
            dfgrpmk = dfgrp[[mk, "Cluster"]]
            for ct2 in list(set(cluslist) - set([ct])):
                dftemp2 = dfgrpmk.loc[dfgrpmk["Cluster"] == ct2]
                # pval = scipy.stats.ttest_ind(dftemp1[mk], dftemp2[mk], equal_var=False).pvalue

                score, pval = ranksums(dftemp1[mk], dftemp2[mk])
                fc = (dftemp1[mk].mean() + 0.0001) / (dftemp2[mk].mean() + 0.0001)
                # if (score10.loc[mk,ct] >= float(score10.loc[mk,ct2])) & (EScore.loc[mk,ct] >= float(EScore.loc[mk,ct2]))&(ratiovalue.loc[mk,ct]>0.9)& (score10.loc[mk,ct] > 1) & (EScore.loc[mk,ct] > 1) :
                if (fc > foldchange) & (dftemp1[mk].mean() > meanthreshold) & (pval < pvalue):
                    x = x + 1
                # if (score10.loc[mk, ct] * fc < float(score10.loc[mk, ct2])) & (
                #      EScore.loc[mk, ct] * fc < float(EScore.loc[mk, ct2])):
                # if (score10.loc[mk,ct] < float(score10.loc[mk,ct2])) & (EScore.loc[mk,ct] < float(EScore.loc[mk,ct2])) &(ratiovalue.loc[mk,ct]<0.1)& (EScore.loc[mk,ct] < 0.1):
                # y = y + 1
            if x in list(range(min(2, int(len(cluslist) / 4) + 1), len(cluslist))):
                temp[x].append(mk)
            # if y in list(range(min(3, int(len(df_fold.columns) / 4) + 1), len(df_fold.columns))):
            #  temp[y].append(mk)
            # markers[ct2] -= set([mk])
        # for num in range(2,len(df_fold.columns)-1):
        mkdict[ct] = temp
    genelist = []
    grouplist = []
    numberlist = []
    for num in range(min(2, int(len(cluslist) / 4) + 2), len(cluslist)):
        for ct in cluslist:
            genelist.extend(mkdict[ct][num])
            grouplist.extend([ct] * len(mkdict[ct][num]))
            numberlist.extend([num] * len(mkdict[ct][num]))
    print("Camel...Running: Marker is coming out...")
    dfmk = pd.DataFrame([genelist, grouplist, numberlist])
    dfmk.columns = dfmk.iloc[0, :]
    dfmk = dfmk.T
    dfmk.columns = ["Gene", "Group", "Num"]
    return dfmk

def ConsistantAssign(datax,dfsig,outputfilepath=None,outputPlot=True ):
    dfprob=pd.DataFrame(datax.obsm['Celltype_Score'], index=datax.obs.index,columns=datax.uns['Celltype_Score_RefCellType'])
    dfprob1=dfprob-dfsig.quantile(0.95)
    dfprob1[dfprob1<0]=0
    dfprob1neg=dfprob1.loc[dfprob1.sum(1)==0]
    dfprob1posi=dfprob1.loc[dfprob1.sum(1)>0]
    cluslist=[]
    colname=dfprob1posi.columns
    for i in range(dfprob1posi.shape[0]):
        temp=dfprob1posi.iloc[i,:]
        cluslist.append(colname[temp.tolist().index(max(temp))])
    dfprob1posi["PredictCluster"]=cluslist
    dfprob1neg["PredictCluster"]=["NoPrediction"]*dfprob1neg.shape[0]
    dfprob1=dfprob1posi.append(dfprob1neg)
    dfprob1=dfprob1.loc[datax.obs.index]
    datax.obs["PredictCluster"]=dfprob1["PredictCluster"]
    sumlist=[]
    for item in datax.obs.index:
        if datax.obs.loc[item,"Cluster"]==datax.obs.loc[item,"PredictCluster"]:
            sumlist.append(1)
        else:
            sumlist.append(0)
    datax.obs["ClusterConsistanceScore"]=sumlist
    if outputfilepath!=None:
        dfoutput=datax.obs.loc[datax.obs["ClusterConsistanceScore"]==0][["Cluster","PredictCluster"]].sort_values(["Cluster"])
        dfoutput.to_csv(outputfilepath,sep="\t")
    if outputPlot==True:
        Percent0=datax.obs.groupby(["Cluster"])["ClusterConsistanceScore"].sum()/datax.obs.groupby(["Cluster"])["ClusterConsistanceScore"].count()
        Percent75=1-Percent0
        PercentDf=[Percent0,Percent75]
        PercentSum=pd.DataFrame(PercentDf,index=["Consistent","Inconsistent"])*100

        plt.figure(figsize=(25,10))

        cmap = plt.cm.bwr
        percfig=PercentSum.T.plot.bar(stacked=True, legend=False, figsize=(20, 10),yticks = range(0,101,10),color=cmap(np.linspace(0, 1, 2)),alpha=0.95)
        plt.xticks(rotation=90,
                   #horizontalalignment='center',
                   verticalalignment='top', position=(0,-0.05), fontsize=20)
        plt.yticks(rotation=0, verticalalignment='top', position=(0,0), fontsize=20)
        percfig.set_ylim(ymin=0, ymax=100)
        #percfig.grid(False)
        plt.ylabel('Percentage of consistently assigned cells (%)', fontsize=25, position=(0,0.5), color=(0.2,0.2,0.2), alpha=0.95)
        plt.xlabel("",position=(0,-0.5), fontsize=15)
        percfig.spines.right.set_visible(False)
        percfig.spines.top.set_visible(False)
        recs2 = []
        for i in range(len(PercentSum.index.tolist())):
            recs2.append(mpatches.Rectangle((0,0),1,1, alpha=0.95,edgecolor="Grey", fc=cmap(np.linspace(0, 1, 2))[i]))

        percfig.legend(recs2,PercentSum.index.tolist(),loc=2,bbox_to_anchor=(1.01, 1.1), prop={'size':25})
    return datax


def patch_violinplot():
    from matplotlib.collections import PolyCollection
    ax = plt.gca()
    for art in ax.get_children():
        if isinstance(art, PolyCollection):
            art.set_edgecolor((0.6, 0.6, 0.6))


from matplotlib import pyplot
from matplotlib import gridspec



def CellTypeSimilarityViolinPlot(datax, dataref,fontsizevalue=15):
    #### need set if, to check the Cluster, celltype_score, etc......
    genename = np.sort(list(set(datax.obs["Cluster"])))
    name = np.sort(list(set(dataref.obs["Cluster"])))
    dfprob = pd.DataFrame(datax.obsm['Celltype_Score'])
    dfprob.columns = datax.uns['Celltype_Score_RefCellType']
    dfprob.index = datax.obs.index
    dfmk = dfprob.astype(float).join(datax.obs["Cluster"], how="inner").T
    refcolor_dict=pd.Series(dataref.uns["refcolor_dict"])
    color_dictw = refcolor_dict
    color_dictw = color_dictw.map(lambda x: list(map(lambda y: y / 255., x)))
    fig = pyplot.figure(figsize=(int(len(name)/2), len(genename)))
    gs0 = gridspec.GridSpec(len(genename), 1)
    for g in range(len(genename)):
        axleft = plt.subplot(gs0[g, :])
        gs00 = gridspec.GridSpecFromSubplotSpec(1, len(name), subplot_spec=gs0[g])
        x = np.arange(0.5, len(name) + 0.5, 1)
        y = [100] * len(name)
        # plt.plot(x,100, color=array(color_dictw[dftemp.index[1]]))
        plt.bar(x, y, width=0.95, alpha=0.4, color="white")
        # if genename [g] in ['NC_Progenitor&Fibro','Core']:
        #    plt.bar(x, y,  width=0.95,alpha=0.4, color="#A4A4A4")
        # refmarker=dftestnewtf.loc[dftestnewtf["Group"]==genename [g]].index
        # for i in range(len(name)):
        #    if name[i] in refmarker:
        #       plt.bar(x[i], y[i],  width=0.95,alpha=0.4, color="#A4A4A4")
        plt.grid(False)
        plt.axis([0, len(name), 0, 100])
        if len(genename[g]) > 127:
            axleft.set_ylabel("%s\n%s\n%s" % (genename[g][:15], genename[g][15:-11], genename[g][-11:]), fontsize=int(fontsizevalue),
                              rotation=0, labelpad=90)
        else:
            axleft.set_ylabel("%s\n%s" % (genename[g][:15], genename[g][15:]), fontsize=int(fontsizevalue), rotation=0, labelpad=90)
            axleft.yaxis.set_label_coords(-0.3, 0)
        plt.xticks(x, name, rotation=90, horizontalalignment='center', verticalalignment='top',
                   position=(0, 0), fontsize=fontsizevalue)
        # plt.yticks([])
        axleft.spines['right'].set_visible(False)
        axleft.spines['top'].set_visible(False)
        sns.set_style("whitegrid")
        # ymin, ymax = plt.get_ylim()
        # axright = axleft.twinx()
        # axright.set_ylabel("Spikeline:Relative_expression \n (count/max_count)",fontsize=10)
        plt.yticks(fontsize=int(fontsizevalue/3)+1)
        plt.grid(False)
        axleft.set_ylim(0, 100)
        # axright.spines['right'].set_visible(False)
        # axright.spines['top'].set_visible(False)
        if g != len(genename) - 1:
            axleft.set_xticklabels([])
        # plt.title(genename[g], fontsize=10)

        for i in range(len(name)):
            dftemp = dfmk.T.loc[dfmk.loc["Cluster"] == genename[g]]
            dftest = dftemp.T.loc[~dftemp.columns.isin(["Cluster"])].T.astype(float)
            # dftemp=dftest.join(dftemp["Cluster"],how="inner")
            axl = fig.add_subplot(gs00[0, i])
            # dftempsort=dftemp[genename[g]]
            # maxvalue=log10(dfmk.loc[name[i]].max()+1)
            axl.set_ylim([0, 100])
            axl.set_xlim([0, 0.9])
            # for m in range(len(dftemp[genename[g]].index)):
            #    plt.plot([m/len(dftemp[genename[g]].index)-0.5,m/len(dftemp[genename[g]].index)-0.5],
            #            [0, dftempsort[m]],c="k",lw=1)
            axl.axis("off")

            anum = axl.twinx()
            anum.set_ylim([-0.01, 100])
            # dfnew=log2(dftest+1).astype(float).divide(maxvalue)
            # dfnew=dftest.divide(maxvalue)
            dfnew = dftest
            dfnew = dfnew.join(dftemp["Cluster"], how="inner")
            ax = sns.violinplot(y=name[i], scale="width", bw=0.4, cut=2,
                                gridsize=500, saturation=1, width=0.9, edgecolor=None,
                                color=np.array(color_dictw[name[i]]),
                                inner='box', data=dfnew, ax=anum)
            plt.setp(ax.collections, alpha=.5)
            # test=fig.add_subplot(1,1,1)

            # test=plt.figure(figsize=(5,10))

            # (dftemp["SOX2"].sort_values()/ratio).plot.bar(color=array(color_dictw[name[i]]),width=1,ax=ax2)

            # (dftemp["SOX2"].sort_values()/ratio).plot.bar(color=array(color_dictw[name[i]]),width=1)
            # %axis("off")
            # sns.stripplot(y=dftemp.index.name, x=dftemp.columns.name, jitter=.2,
            #              color=array(color_dictw[dftemp.index[1]]),  edgecolor='gray', linewidth=0.7,
            #             alpha=.6, size=6, data=dftemp, ax=anum)
            anum.axis('off')
    return dfprob


def save_load_model(filename, modelname=None, type="save"):
    if type=="save":
        pickle.dump(modelname, open(filename, 'wb'))
    elif type=="load":
        loaded_model = pickle.load((open(filename, 'rb')))
        return loaded_model

def rgb2hex(r,g,b):
    return "#{:02x}{:02x}{:02x}".format(r,g,b)

def addcolor(datax,clustername="Cluster", colorcode="color", predef=pd.Series()):
    if not colorcode in datax.obs.columns:
        if predef.empty:
            color_dict = {}
            wanted_order=list(set(datax.obs[clustername]))
            for item in wanted_order:
                color_dict[item] = np.array(random.sample(range(0, 255), 3)).tolist()
            colorlist=[]
            for item in datax.obs[clustername]:
                colorlist.append((np.array(color_dict[item])/255).tolist())
            clist = []
            for item in colorlist:
                clist.append(rgb2hex(int(item[0] * 255), int(item[1] * 255), int(item[2] * 255)))
            datax.obs[colorcode]=clist
            datax.uns["refcolor_dict"] =color_dict
        else:
            color_dict=predef
            colorlist = []
            for item in datax.obs[clustername]:
                colorlist.append((np.array(color_dict[item]) / 255).tolist())
            clist = []
            for item in colorlist:
                clist.append(rgb2hex(int(item[0] * 255), int(item[1] * 255), int(item[2] * 255)))
            datax.obs[colorcode] = clist
            datax.uns["refcolor_dict"] = color_dict
    return datax

def MergeCluster(adatax, reflist=[], NewName=None):
    newlist=[]
    adatax.obs[ 'Origin_Assigned_Celltype']=adatax.obs[ 'Assigned_Celltype']
    for item in adatax.obs[ 'Assigned_Celltype']:
        if item in reflist:
            newlist.append(NewName)
        else:
            newlist.append(item)
    adatax.obs[ 'Assigned_Celltype']=newlist
    return adatax

def UMAP_plot(datax,clustername="Cluster", colorcode="color",legendOnPlot=False,Ncol=2,
              legendshow=True,figuresize=(10,10),alphavalue=0.8, lwvalue=0.1, markervalue=".",
             dotsize=200,lengendfont=20, legendloc=2,bbox_to_anchorvalues=(1.15, 1.2)):
    #groups=list(set(df["Cluster"]))
    #annot=dfref["Cluster"].values
    #fname="uMAP_GBM"
    #title=''
    #prefix='uMAP'
    #colorlist=[]
    #for item in df["Cluster"].values:
    if not colorcode in datax.obs.columns:
        color_dict = {}
        wanted_order=list(set(datax.obs[clustername]))
        for item in wanted_order:
            color_dict[item] = (np.array(random.sample(range(0, 499), 3))/500).tolist()
        colorlist=[]
        for item in datax.obs[clustername]:
            colorlist.append(color_dict[item])
        datax.obs[colorcode]=colorlist
    fig=plt.figure(figsize=figuresize, facecolor='w')
    ax = fig.add_subplot(111)
    ax.scatter(datax.obsm["X_umap"][:,0],datax.obsm["X_umap"][:,1],c=datax.obs[colorcode],
               alpha=alphavalue, lw=lwvalue,
                marker=markervalue, s=dotsize)
    plt.grid(False)
    plt.axis("off")
    if legendshow==True:
        recs = []
        dfc = datax.obs[[clustername, colorcode]]
        dfc.index = dfc[clustername]
        dfc = dfc[~dfc.index.duplicated(keep='first')]
        xwanted_order = sorted(list(set(datax.obs[clustername])))
        for item in xwanted_order:
            recs.append(mpatches.Rectangle((0,0),1,1,fc=dfc.loc[item,colorcode]))
        ax.legend(recs,xwanted_order, ncol=Ncol,loc=legendloc,bbox_to_anchor=bbox_to_anchorvalues, prop={'size': lengendfont})
        #xwanted_order=list(set(dfref["Cluster"]))
        #for item in xwanted_order:
         #   recs.append(mpatches.Rectangle((0,0),1,1,fc=color_dict2[item]))
        #plt.legend(recs,xwanted_order, loc=2,bbox_to_anchor=(1.15, 1.2), prop={'size': 25})
    if legendOnPlot==True:
        dfposi=pd.DataFrame(datax.obsm["X_umap"], index=datax.obs.index, columns=["UMAP_X", "UMAP_Y"]).astype(float)
        dfposi[clustername]=datax.obs[clustername]
        textpositionLv = dfposi.groupby([clustername]).mean()
        for i in range(textpositionLv.shape[0]):
            plt.text(textpositionLv.iloc[i, 0], textpositionLv.iloc[i, 1], textpositionLv.index[i], fontsize=lengendfont)
    return datax, ax


def UMAPplotRefPred(DataRef, DataPdt, refClusterName,pdtClusterName, refColorCode, pdtColorCode,figuresize=(10, 10),
                    RefAlphaValue=0.8, RefLwValue=0.1, RefMarkerValue="x", RefDotSize=200,
                    PdtAlphaValue=0.8, PdtLwValue=0.1, PdtMarkerValue=".", PdtDotSize=200,
                    lengendfont=20, RefLegendloc=2, PdtLegendloc=3, Refbbox_to_anchorvalues=(1.15, 1.2),
                    Pdtbbox_to_anchorvalues=(1.15, 0.05)):
    # groups=list(set(df["Cluster"]))
    # annot=dfref["Cluster"].values
    # fname="uMAP_GBM"
    # title=''
    # prefix='uMAP'
    # colorlist=[]
    # for item in df["Cluster"].values:
    import matplotlib
    if not refColorCode in DataRef.obs.columns:
        color_dict = {}
        wanted_order = list(set(DataRef.obs[refClusterName]))
        for item in wanted_order:
            color_dict[item] = (np.array(random.sample(range(0, 999), 3))/1000).tolist()
        colorlist = []
        for item in DataRef.obs[refClusterName]:
            colorlist.append(color_dict[item])
        DataRef.obs[refColorCode] = colorlist
    if not pdtColorCode in DataPdt.obs.columns:
        color_dict = {}
        wanted_order = list(set(DataPdt.obs[pdtClusterName]))
        for item in wanted_order:
            color_dict[item] = (np.array(random.sample(range(0, 999), 3))/1000).tolist()
        colorlist = []
        for item in DataPdt.obs[pdtClusterName]:
            colorlist.append(color_dict[item])
        DataPdt.obs[pdtColorCode] = colorlist

    fig = plt.figure(figsize=figuresize, facecolor='w')
    ax = fig.add_subplot(111)
    ax.scatter(DataRef.obsm["X_umap"][:, 0], DataRef.obsm["X_umap"][:, 1], c=DataRef.obs[refColorCode],
               alpha=RefAlphaValue,
               lw=RefLwValue,
               marker=RefMarkerValue, s=RefDotSize)
    ax.scatter(DataPdt.obsm["X_umap"][:, 0], DataPdt.obsm["X_umap"][:, 1], c=DataPdt.obs[pdtColorCode],
               alpha=PdtAlphaValue,
               lw=PdtLwValue,
               marker=PdtMarkerValue, s=PdtDotSize)
    plt.grid(False)
    plt.axis("off")

    recs = []
    dfc = DataRef.obs[[refClusterName, refColorCode]]
    dfc.index = dfc[refClusterName]
    dfc = dfc[~dfc.index.duplicated(keep='first')]
    xwanted_order = list(set(DataRef.obs[refClusterName]))
    for item in xwanted_order:
        recs.append(mpatches.Rectangle((0, 0), 1, 1, fc=dfc.loc[item, refColorCode]))
    legend1 = ax.legend(recs, xwanted_order, loc=RefLegendloc, bbox_to_anchor=Refbbox_to_anchorvalues,
                        prop={'size': lengendfont})

    recs2 = []
    dfcPdt = DataPdt.obs[[pdtClusterName, pdtColorCode]]
    dfcPdt.index = dfcPdt[pdtClusterName]
    dfcPdt = dfcPdt[~dfcPdt.index.duplicated(keep='first')]
    mwanted_order = list(set(DataPdt.obs[pdtClusterName]))
    for item in mwanted_order:
        recs2.append(matplotlib.patches.Circle((2, 2), radius=1, fc=dfcPdt.loc[item, pdtColorCode]))
    ax.legend(recs2, mwanted_order, loc=PdtLegendloc, bbox_to_anchor=Pdtbbox_to_anchorvalues,
              prop={'size': lengendfont})
    plt.gca().add_artist(legend1)
# xwanted_order=list(set(dfref["Cluster"]))
# for item in xwanted_order:
#   recs.append(mpatches.Rectangle((0,0),1,1,fc=color_dict2[item]))
# plt.legend(recs,xwanted_order, loc=2,bbox_to_anchor=(1.15, 1.2), prop={'size': 25})
    return DataRef, DataPdt, ax

def indices_distancesDensematrix(D, n_neighbors):
    sample_range = np.arange(D.shape[0])[:, None]
    indices = np.argpartition(D, n_neighbors-1, axis=1)[:, :n_neighbors]
    indices = indices[sample_range, np.argsort(D[sample_range, indices])]
    distances = D[sample_range, indices]
    return indices, distances
def sparse_matrixindicesDistances(indices, distances, nobs, n_neighbors):
    n_nonzeros = nobs * n_neighbors
    indptr = np.arange(0, n_nonzeros + 1, n_neighbors)
    D = scipy.sparse.csr_matrix((distances.copy().ravel(),  # must do copy here
                                indices.copy().ravel(),
                                indptr),
                                shape=(nobs, nobs))
    D.eliminate_zeros()
    return D

def connectivities_to_igraph(adjacency, directed=None):
    """Get igraph graph from adjacency matrix."""
    try:
        import igraph as ig
    except ImportError:
        raise ImportError(
            'Please install igraph!'
        )
    sources, targets = adjacency.nonzero()
    weights = adjacency[sources, targets]
    if isinstance(weights, np.matrix):
        weights = weights.A1
    gph = ig.Graph(directed=directed)
    gph.add_vertices(adjacency.shape[0])  # this adds adjacency.shap[0] vertices
    gph.add_edges(list(zip(sources, targets)))
    try:
        gph.es['weight'] = weights
    except:
        pass
    if gph.vcount() != adjacency.shape[0]:
        logging.warn('The constructed graph has only {} nodes. '
                  'Your adjacency matrix contained redundant nodes.'
                  .format(gph.vcount()))
    return gph

def UMAPindices_distancesTosparseMatrix(knn_indices, knn_dists, n_obs, n_neighbors):
    rows = np.zeros((n_obs * n_neighbors), dtype=np.int64)
    cols = np.zeros((n_obs * n_neighbors), dtype=np.int64)
    vals = np.zeros((n_obs * n_neighbors), dtype=np.float64)

    for i in range(knn_indices.shape[0]):
        for j in range(n_neighbors):
            if knn_indices[i, j] == -1:
                continue  # We didn't get the full knn for i
            if knn_indices[i, j] == i:
                val = 0.0
            else:
                val = knn_dists[i, j]

            rows[i * n_neighbors + j] = i
            cols[i * n_neighbors + j] = knn_indices[i, j]
            vals[i * n_neighbors + j] = val

    result = coo_matrix((vals, (rows, cols)),
                                      shape=(n_obs, n_obs))
    result.eliminate_zeros()
    return result.tocsr()

def _compute_connectivities_umapXX(
    knn_indices,
    knn_dists,
    n_obs,
    n_neighbors,
    set_op_mix_ratio=1.0,
    local_connectivity=1.0,
):
    """
    credits go to Scanpy, with modifications
    Given a set of data X, a neighborhood size, and a measure of distance
    compute the fuzzy simplicial set (here represented as a fuzzy graph in
    the form of a sparse matrix) associated to the data. This is done by
    locally approximating geodesic distance at each point, creating a fuzzy
    simplicial set for each such point, and then combining all the local
    fuzzy simplicial sets into a global one via a fuzzy union.
    """
#    with warnings.catch_warnings():
        # umap 0.5.0
#        warnings.filterwarnings("ignore", message=r"Tensorflow not installed")
    from umap.umap_ import fuzzy_simplicial_set

    X = coo_matrix(([], ([], [])), shape=(n_obs, 1))
    connectivities = fuzzy_simplicial_set(
        X,
        n_neighbors,
        None,
        None,
        knn_indices=knn_indices,
        knn_dists=knn_dists,
        set_op_mix_ratio=set_op_mix_ratio,
        local_connectivity=local_connectivity,
    )

    if isinstance(connectivities, tuple):
        # In umap-learn 0.4, this returns (result, sigmas, rhos)
        connectivities = connectivities[0]

    distances = UMAPindices_distancesTosparseMatrix(
        knn_indices, knn_dists, n_obs, n_neighbors
    )

    return distances, connectivities.tocsr()

def SWAPLINE_dist(datax, n_neighbors=50, metric = 'euclidean'):
    #n_pcs = 30, n_neighbors = len(dfnn.index),  metric = 'euclidean'
    ####
    # must be np.float32
    ####
    XX = datax.obsm["Celltype_Score"].astype(np.float32)

    #pca_ = PCA(n_components=n_pcs, svd_solver='arpack', random_state=0)
    #X_pca = pca_.fit_transform(X)
    PariDistances = pairwise_distances(XX, metric=metric)
    knn_indices, knn_distances = indices_distancesDensematrix(PariDistances, n_neighbors)
    logging.info('Camel...Running: distance calculating.....')
    #_distances = sparse_matrixindicesDistances(knn_indices, knn_distances, XX.shape[0], n_neighbors)
    #dftestdist = pd.DataFrame(knn_distances)
    #dftest = 0
    #dftestindex = pd.DataFrame(knn_indices)
    # dfnn=df.T
    # dfnn.shape
    #dftestindex.index = dfnn.index
    _distances, _connectivities = _compute_connectivities_umapXX(
        knn_indices, knn_distances, XX.shape[0], n_neighbors)
    datax.obsp["connectivities"]=_connectivities
    datax.obsp["distances"] = _distances
    #logging.info('Camel...Running: connectivity calculating.....')
    #neighbors_distances = _distances
    #neighbors_connectivities = _connectivities
    #adjacency = _connectivities
    #neighbors_connectivities = _connectivities
    logging.info('Camel...Running: finish.....')
    return datax

def clusterfinder(datax,Th_value =1, method="Louvain"):
    buildgraph = connectivities_to_igraph(adjacency=datax.obsp["connectivities"], directed=True)
    if method=="Louvain":

        from natsort import natsorted
        try:
            import louvain
            #import leidenalg
        except ImportError:
            raise ImportError(
                'Please install the louvain!.'
            )
        #partition_kwargs = dict(partition_kwargs)

        logging.info('Camel...Running: Louvain clustering')

        parttern = louvain.find_partition(
            buildgraph,
            partition_type=louvain.RBConfigurationVertexPartition,
            resolution_parameter=Th_value,
            #**partition_kwargs
        )
        # output clusters
        clustergroups = np.array(parttern.membership)
        cellcluster = pd.Categorical(
            values=clustergroups.astype('U'),
            categories=natsorted(np.unique(clustergroups).astype('U')),
        )

    elif method=="Leiden":
        from natsort import natsorted
        try:
            #import louvain
            import leidenalg
        except ImportError:
            raise ImportError(
                'Please install leidenalg!'
            )
        #partition_kwargs = dict(partition_kwargs)

        print('Camel...Running: Leiden clustering')
        #partition_type options:
        #leidenalg.RBConfigurationVertexPartition
        #leidenalg.CPMVertexPartition
        #leidenalg.SignificanceVertexPartition
        #leidenalg.RBERVertexPartition
        #leidenalg.MutableVertexPartition
        #leidenalg.ModularityVertexPartition
        # clustering proper
        parttern = leidenalg.find_partition(
            buildgraph,
            partition_type = leidenalg.RBConfigurationVertexPartition,
            resolution_parameter=Th_value,
            )
        # output clusters
        clustergroups = np.array(parttern.membership)
        cellcluster = pd.Categorical(
            values=clustergroups.astype('U'),
            categories=natsorted(np.unique(clustergroups).astype('U')),
        )
    datax.obs["Assigned_Celltype"]=cellcluster
    return datax

def transfer_learning(UMAPmodel, datapdt, datax,clustername, colorcode, n_neighbors=50):
    try:
        from sklearn.neighbors import KNeighborsClassifier
    except ImportError:
        raise ImportError(
            'Please install sklearn!'
        )
    X_rTest = UMAPmodel.transform(datapdt.obsm["Celltype_Score"])
    datapdt.obsm['X_umap'] = X_rTest
    # dfg = pd.DataFrame(X_r)
    #dfgTest.index = dfpcaTest.index
    #dfgTest.columns=["UMAP_X","UMAP_Y"]
    #dfpdtTest = dfgTest.join(dfclusTest["Cluster"], how="inner")
    neigh = KNeighborsClassifier(n_neighbors=n_neighbors, metric="euclidean")
    neigh.fit(datax.obsm["Celltype_Score"].astype(np.float32), datax.obs[clustername])
    datapdt.obs[clustername] = neigh.predict(datapdt.obsm["Celltype_Score"].astype(np.float32))
    if colorcode in datax.obs.columns:
        dfc = datax.obs[[clustername, colorcode]]
        dfc.index = dfc[clustername]
        dfc = dfc[~dfc.index.duplicated(keep='first')]
        colorlist=[]
        for item in  datapdt.obs[clustername]:
            colorlist.append(dfc.loc[item,colorcode])
        datapdt.obs[colorcode]=colorlist
    return datapdt

def prediction(datax, mcolor_dict,net,learninggroup="train", radarplot=True, fontsizeValue=35,
              datarefplot=None,
               ncolnm=1, bbValue=(1.1, 1.05)):
    #mwanted_order = mwanted_order, mclasses_names = mclasses_names, mprotogruop = dfpfcclus.loc["Cluster"].values,
    #mdf_train_set = mdf_train_set, figsizeV = 18, mtrain_index = mtrain_index, net = net, mreorder_ix = mreorder_ix,
    #mcolor_dict = refcolor_dict, learninggroup = "test"

    mcolor_dict=pd.Series(mcolor_dict)
    if  learninggroup=="train":
        mdf_train_set = pd.DataFrame(datax.obsm["train_set_values"].T, index=datax.uns["train_set_gene"],
                                     columns=datax.obs.index)
        mtrain_index = datax.obs["mtrain_index"].values
        mwanted_order = datax.uns["mwanted_order"]
        mclasses_names = datax.uns["mclasses_names"]
        mprotogruop = datax.obs["Cluster"].values
        dfpfcclus = datax.obs["Cluster"]
        mreorder_ix = [list(mclasses_names).index(i) for i in mwanted_order]
        mbool00 = np.in1d( mclasses_names[mtrain_index],  mwanted_order )
        if (np.sum(mcolor_dict ==None)!=0) or (np.sum(mcolor_dict.index.isin(mwanted_order))!=len(mwanted_order)):
            mcolor_dict={}
            for item in mwanted_order:
                mcolor_dict[item] = (np.array(random.sample(range(0, 999), 3)) / 1000).tolist()
        else:
            mcolor_dict = mcolor_dict.map(lambda x: list(map(lambda y: y/255., x)))
        #color_dict
        #mcolor_dict = mcolor_dict.map(lambda x: list(map(lambda y: y/255., x)))
        #rcParams['savefig.dpi'] = 500
        #mnewcolors = array(list(mcolor_dict[mprotogruop].values))
        normalizer = 0.9*mdf_train_set.values.max(1)[:,np.newaxis]
        ####
        # must be np.float32
        ####
        refdataLR=net.predict_proba((mdf_train_set.values/ normalizer).astype(np.float32).T)

        todaytime=f"{datetime.datetime.now():%Y%m%d%I%M%p}"

        dataRef= refdataLR[:,mreorder_ix]
        mreordername=[]
        for i in mreorder_ix:
            mreordername.append(list(mclasses_names)[i])
        dfprobCL=pd.DataFrame(dataRef*100, index=mdf_train_set.columns,columns=mreordername)
        #dfnewcl=pd.DataFrame(array([xtest,ytest]).T, index=mdf_train_set.columns)
        datax.obsm["Celltype_Score"]=dfprobCL.values
        datax.uns["Celltype_Score_RefCellType"]=dfprobCL.columns.tolist()
        datax.uns["Celltype_OrderNumber"]=mreorder_ix
        if radarplot ==True:
            axm, dfclRef = RadarVisualization(refdataLR=refdataLR, mreorder_ix=mreorder_ix,
                                              #fontsizeValue=fontsizeValue,
                                              Ncolm=ncolnm, bbValue=bbValue,
                                                        mtrain_index=mtrain_index,
                                                        mclasses_names=mclasses_names,
                                              mcolor_dict=mcolor_dict,
                                              dataclpn=None, learninggroup=learninggroup,
                                                        mdf_train_set=mdf_train_set,
                                                        mwanted_order=mwanted_order,
                                                        mprotogruop=mprotogruop,
                                              fontsizeValue=int(100/int(len(mwanted_order)**0.5))
                                              )
            datax.obsm["CelltypeScoreCoordinates"]=dfclRef.values
        return datax

    elif learninggroup=="test":
        mdf_train_set = pd.DataFrame(datax.obsm["test_set_values"].T, index=datax.uns["train_set_gene"],
                                     columns=datax.obs.index)
        mtrain_index = datax.obs["mtrain_index"].values
        mwanted_order = datax.uns["mwanted_order"]
        mclasses_names = datax.uns["mclasses_names"]
        mprotogruop = datax.obs["Cluster"].values
        dfpfcclus = datax.obs["Cluster"]
        mreorder_ix = [list(mwanted_order).index(i) for i in mwanted_order]
        if (np.sum(mcolor_dict ==None)!=0) or (np.sum(mcolor_dict.index.isin(mwanted_order))!=len(mwanted_order)):
            mcolor_dict={}
            for item in mwanted_order:
                mcolor_dict[item]=random.sample(range(0, 255), 3)
        mcolor_dict = mcolor_dict.map(lambda x: list(map(lambda y: y/255., x)))
        #mnewcolors = array(list(mcolor_dict[mprotogruop].values))
        normalizerTest=0.9*mdf_train_set.values.max(1)[:,np.newaxis]
        normalizedValue=(mdf_train_set.sub(mdf_train_set.min(1),0).div(normalizerTest,0).fillna(0).values).T

        ####
        # must be np.float32
        ####
        dataRef=net.predict_proba((normalizedValue).astype(np.float32))[:,datarefplot.uns["Celltype_OrderNumber"]]
        mreordername=[]
        for i in mreorder_ix:
            mreordername.append(list(mclasses_names)[i])
        #ollist=[datarefplot.uns['Celltype_Score_RefCellType'][i] for i in datarefplot.uns['Celltype_OrderNumber']]
        #dfprobCL=pd.DataFrame(dataRef*100,   index=mdf_train_set.columns,columns= collist)
        dfprobCL = pd.DataFrame(dataRef * 100, index=mdf_train_set.columns,
                                columns=datarefplot.uns['Celltype_Score_RefCellType'])
        #dfnewcl=pd.DataFrame(array([xtest,ytest]).T, index=mdf_train_set.columns)
        datax.obsm["Celltype_Score"]=dfprobCL.values
        datax.uns["Celltype_Score_RefCellType"]=dfprobCL.columns.tolist()
        datax.uns["Celltype_OrderNumber"]=mreorder_ix
        if radarplot ==True:
            axm, dfclRef = RadarVisualization(refdataLR=dataRef,
                                              mreorder_ix=datarefplot.uns["Celltype_OrderNumber"],
                                            mtrain_index=datarefplot.obs["mtrain_index"].values,
                                              learninggroup="test",
                                              Ncolm=ncolnm, bbValue=bbValue,
                                              mdf_train_set=mdf_train_set,
                                              mprotogruop=datax.obs["Cluster"].values,
                                                    dataclpn=dataRef,
                                                    mwanted_order=mwanted_order,
                                              mclasses_names=datarefplot.uns["mclasses_names"],
                                                    mcolor_dict=mcolor_dict,
                                              fontsizeValue=int(100/int(len(mwanted_order)**0.5)))
            datax.obsm["CelltypeScoreCoordinates"]=dfclRef.values
        return datax



        return mreordername, dfprobCL,  mcolor_dict, dataRef





def RadarPlot(data, scaling=False,start_angle=90, rotate_labels=True, labels=('one','two','three'),fontsizeV=20,
                  sides=3, label_offset=0.10, fig_args = {'figsize':(18,18),'facecolor':'white','edgecolor':'white'}):
    '''
    This will create a basic polygonal plot

    # Scale data for plot (i.e. a + b + c = 1)
    scaling=True,
    # Direction of first vertex.
    start_angle=90,
    # Orient labels perpendicular to vertices.
    rotate_labels=True,
    # Labels for vertices.
    labels=('one','two','three')
    # Offset for label from vertex (percent of distance from origin).
    label_offset=0.10,
    # Any matplotlib keyword args for plots.
    edge_args={'color':'black','linewidth':2},
    # Any matplotlib keyword args for figures.
    fig_args = {'figsize':(8,8),'facecolor':'white','edgecolor':'white'},
    '''
    pi=np.pi
    basis = np.array([[np.cos(2*i*pi/sides + start_angle*pi/180),
                    np.sin(2*i*pi/sides + start_angle*pi/180)] for i in range(sides)])
    RadialBasis=np.array([[np.cos(2*i*pi/sides + (start_angle+180/sides)*pi/180),
                    np.sin(2*i*pi/sides + (start_angle+180/sides)*pi/180)] for i in range(sides)])

    # If data is Nxsides, newdata is Nx2.
    if scaling:
        # Scales data
        newdata = np.dot((data.T / data.sum(-1)).T,basis)
    else:
        # Assumes data already sums to 1.
        newdata = np.dot(data,basis)

    fig = plt.figure(**fig_args)
    ax = fig.add_subplot(111)

    for i,l in enumerate(labels):
        if i >= sides:
            break
        basis2= np.array([[np.cos(2*i*pi/sides + (start_angle+180/sides/2)*pi/180),
                    np.sin(2*i*pi/sides + (start_angle+180/sides/2)*pi/180)] for i in range(sides)])
        x = basis2[i,0]
        y = basis2[i,1]
        if rotate_labels:
            angle = 180*np.arctan(y/x)/pi + 75
            if angle > 90 and angle <= 270:
                angle = np.mod(angle + 180,360)
        else:
            angle = 0
        if l=="Microglia":
            basis3= np.array([[np.cos(2*i*pi/sides + (start_angle+180/sides)*pi/180),
                    np.sin(2*i*pi/sides + (start_angle+180/sides)*pi/180)] for i in range(sides)])
            x = basis3[i,0]
            y = basis3[i,1]
            ax.text(
                x*(1.1 + label_offset),
                y*(1.1 + label_offset),
                l,
                horizontalalignment='center',
                verticalalignment='center',
                rotation=angle-16,
                fontsize=fontsizeV
            )
        elif l=="Cajal-Retzius":
            basis3= np.array([[np.cos(2*i*pi/sides + (start_angle+220/sides)*pi/180),
                    np.sin(2*i*pi/sides + (start_angle+220/sides)*pi/180)] for i in range(sides)])
            x = basis3[i,0]
            y = basis3[i,1]
            ax.text(
                x*(1.15 + label_offset),
                y*(1.15 + label_offset),
                l,
                horizontalalignment='center',
                verticalalignment='center',
                rotation=angle-16,
                fontsize=fontsizeV
            )
        elif len(l)>8:
            basis3= np.array([[np.cos(2*i*pi/sides + (start_angle+180/sides)*pi/180),
                    np.sin(2*i*pi/sides + (start_angle+180/sides)*pi/180)] for i in range(sides)])
            x = basis3[i,0]
            y = basis3[i,1]
            ax.text(
                x*(1.113 + label_offset),
                y*(1.113 + label_offset),
                l,
                horizontalalignment='center',
                verticalalignment='center',
                rotation=angle-16,
                fontsize=fontsizeV
            )
        elif len(l)>=5:
            basis4= np.array([[np.cos(2*i*pi/sides + (start_angle+180/sides/1.5)*pi/180),
                    np.sin(2*i*pi/sides + (start_angle+180/sides/1.5)*pi/180)] for i in range(sides)])
            x = basis4[i,0]
            y = basis4[i,1]
            ax.text(
                x*(1.03 + label_offset),
                y*(1.03 + label_offset),
                l,
                horizontalalignment='center',
                verticalalignment='center',
                rotation=angle-15,
                fontsize=fontsizeV
            )
        else:
            ax.text(
                x*(1.01 + label_offset),
                y*(1.01 + label_offset),
                l,
                horizontalalignment='center',
                verticalalignment='center',
                rotation=angle-15,
                fontsize=fontsizeV
            )
    # Clear normal matplotlib axes graphics

    ax.set_xticks(())
    ax.set_yticks(())
    ax.set_frame_on(False)

    # Plot borders
    ax.plot([basis[_,0] for _ in list(range(sides))+ [0,]], [basis[_,1] for _ in list(range(sides))+ [0,]],c='black',lw=2)
    ax.plot([basis[_,0]*0.75 for _ in list(range(sides))+ [0,]],[basis[_,1]*0.75 for _ in list(range(sides))+ [0,]],c='#B3B6B7',lw=1)
    ax.plot([basis[_,0]*0.5 for _ in list(range(sides))+ [0,]],[basis[_,1]*0.5 for _ in list(range(sides))+ [0,]],c='#B3B6B7',lw=1)
    ax.plot([basis[_,0]*0.25 for _ in list(range(sides))+ [0,]],[basis[_,1]*0.25 for _ in list(range(sides))+ [0,]],c='#B3B6B7',lw=1)
    for _ in list(range(sides)):
        ax.plot([0,RadialBasis[_,0]*0.98],[0,RadialBasis[_,1]*0.98], color='#B3B6B7', linewidth=1, linestyle='dashed')
    return newdata,ax


def RadarVisualization(refdataLR, dataclpn, mreorder_ix, fontsizeValue,bbValue,
                       mtrain_index, mwanted_order,Ncolm,
                       mprotogruop,mdf_train_set,
                       mclasses_names, mcolor_dict, learninggroup="train"):
    #refdataLR = refdataLR, dataclpn = dataclpn, mreorder_ix = mreorder_idx,
    #mtrain_index = mtrain_index, mwanted_order = wanted_orderclpn,
    #mprotogruop = dfpfcclus.loc["Cluster"].values,mdf_train_set=mdf_train_set,
    #mclasses_names = mclasses_names, mcolor_dict = color_dictclpn, learninggroup = "train"
    if learninggroup == "train":
        mnewdata, axm = RadarPlot(refdataLR[:, mreorder_ix], sides=len(mreorder_ix),
                                  fontsizeV=fontsizeValue,labels=mclasses_names[mreorder_ix])
        mbool00 = np.in1d(mclasses_names[mtrain_index], mwanted_order)
        xtest = mnewdata[mbool00, 0] * 0.99
        ytest = mnewdata[mbool00, 1] * 0.99
        alllist=[]
        for item in mprotogruop:
            alllist.append(mcolor_dict[item])
        mnewcolors = np.array(alllist)

        axm.scatter(xtest, ytest, alpha=0.8, c=mnewcolors[mbool00, :], s=200, lw=0.2)
        dfnewcl = pd.DataFrame(np.array([xtest, ytest]).T, index=mdf_train_set.columns)
        recs = []
        for item in mwanted_order:
            recs.append(mpatches.Rectangle((0, 0), 1, 1, fc=mcolor_dict[item]))
        axm.legend(recs, mwanted_order, loc=2, bbox_to_anchor=(1.05, 1.05), prop={'size': fontsizeValue})
        return axm, dfnewcl

    elif learninggroup == "test":
        #mnewdata, axm = RadarPlot(refdataLR[:, mreorder_ix], sides=len(mreorder_ix), labels=mclasses_names[mreorder_ix])
        mnewdata, axm = RadarPlot(refdataLR, sides=len(mreorder_ix), labels=mclasses_names[mreorder_ix])

        # mbool00 = in1d( mclasses_names[mtrain_index],  mwanted_order )
        sides = len(mreorder_ix)
        start_angle = 90
        pi=np.pi
        basisclpn = np.array([[np.cos(2 * i * pi / sides + start_angle * pi / 180),
                            np.sin(2 * i * pi / sides + start_angle * pi / 180)] for i in range(sides)])
        newdataclpn = np.dot(dataclpn, basisclpn)
        xtest = mnewdata[:, 0] * 0.99
        ytest = mnewdata[:, 1] * 0.99
        dfnewcl = pd.DataFrame(np.array([xtest, ytest]).T, index=mdf_train_set.columns)
        # mcolor_dict = mcolor_dict.map(lambda x: list(map(lambda y: y/255., x)))

        mnewcolors = np.array(list(mcolor_dict[mprotogruop].values))

        axm.scatter(xtest, ytest, alpha=0.8, c=mnewcolors, s=200, lw=0.2)

        recs = []
        for item in mwanted_order:
            recs.append(mpatches.Rectangle((0, 0), 1, 1, fc=mcolor_dict[item]))
        axm.legend(recs, mwanted_order, loc=2, bbox_to_anchor=bbValue,ncol=Ncolm, prop={'size': fontsizeValue})
        return axm, dfnewcl



def permutationTest(datax,net,num, plotshow=True):
    dfprobRef = pd.DataFrame(datax.obsm["Celltype_Score"], index=datax.obs.index,
                             columns=datax.uns["Celltype_Score_RefCellType"])
    #dfpfcclus = datax.obs[["mtrain_index", "Cluster"]].T
    #mwanted_order = datax.uns["mwanted_order"]
    mreorder_ix=datax.uns["Celltype_OrderNumber"]
    mdf_train_set = pd.DataFrame(datax.obsm["train_set_values"].T, index=datax.uns["train_set_gene"],
                                 columns=datax.obs.index)

    test = mdf_train_set.values.reshape((len(mdf_train_set.columns) * len(mdf_train_set.index)))
    test = np.random.permutation(test)
    test = test.reshape((len(mdf_train_set.index), len(mdf_train_set.columns)))
    dftest = pd.DataFrame(test).astype(float)
    xp = dftest.values
    xp -= xp.min()
    xp /= xp.ptp()
    ####
    # must be np.float32
    ####
    test0 = net.predict_proba((xp).T.astype(np.float32))[:, mreorder_ix]
    for i in range(0, num):
        test = mdf_train_set.values.reshape((len(mdf_train_set.columns) * len(mdf_train_set.index)))
        test = np.random.permutation(test)
        test = test.reshape((len(mdf_train_set.index), len(mdf_train_set.columns)))
        dftest = pd.DataFrame(test).astype(float)
        xp = dftest.values
        xp -= xp.min()
        xp /= xp.ptp()
        ####
        # must be np.float32
        ####
        dataRef2 = net.predict_proba((xp).T.astype(np.float32))[:, mreorder_ix]

        test0 = np.append(test0, dataRef2, axis=0)
        # test0=test0+dataRef2

    thresholdlist = []
    temp = []
    for threshold in np.arange(0.0, 1.0, 0.01):
        thresholdlist.append("Prob_%s%%" % int(threshold * 100))
        temp.append((np.sum(test0 > threshold, axis=0) / test0.shape[0]))

    ratiodf = pd.DataFrame(temp)
    ratiodf.index = thresholdlist
    ratiodf.columns = dfprobRef.columns
    dftest0 = pd.DataFrame(test0 * 100, columns=dfprobRef.columns)
    if plotshow== True:
        import seaborn as sns
        fig = plt.figure()
        fig, ax = plt.subplots(figsize=(15, 7))
        ax = sns.violinplot(scale="width", bw=0.4, cut=2, gridsize=100, saturation=0.9, scale_hue=False,
                            width=0.95, palette=["grey"], linewidth=0.5, split=True, data=dftest0, alpha=0.75)
        ax = sns.scatterplot(data=dftest0.quantile(0.9), c=["r"], marker="X", s=200)
        plt.axhline(50, c='b', alpha=0.8, linestyle='dashed')
        ax.set_ylim(ymin=-0.01, ymax=100)
        plt.xticks(rotation=90, fontsize=22)
        plt.yticks(
            fontsize=25)
        plt.title("Cell-Type Fractions", fontsize=25)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
    return dftest0, ratiodf




def ProbSinglePlot (datax, mcolor_dict, fs=25):
    import seaborn as sns
    #dfprobRef = dfprobRef, dfpfcclus = dfpfcclus, mwanted_order = mwanted_order, mcolor_dict = refcolor_dict
    # mdf_train_set = pd.DataFrame(datax.obsm["train_set_values"].T, index=datax.uns["train_set_gene"],
    #                             columns=datax.obs.index)
    #mtrain_index = datax.obs["mtrain_index"].values
    #mwanted_order = datax.uns["mwanted_order"]
    #mclasses_names = datax.uns["mclasses_names"]
    #mprotogruop = datax.obs["Cluster"].values
    #dfpfcclus = datax.obs["Cluster"]

    dfprobRef=pd.DataFrame(datax.obsm["Celltype_Score"], index=datax.obs.index, columns=datax.uns["Celltype_Score_RefCellType"])
    dfpfcclus = datax.obs[["mtrain_index","Cluster"]].T
    mwanted_order=datax.uns["mwanted_order"]
    mcolor_dict = mcolor_dict.map(lambda x: list(map(lambda y: y / 255., x)))
    fig = plt.figure(figsize=(50,20))
    x=np.arange(0.5, len(dfprobRef.columns)+0.5, 1)
    y=[80]*len(dfprobRef.columns)
    #plt.plot(x,100, color=array(color_dictw[dftemp.index[1]]))
    plt.bar(x, y,  width=0.95,alpha=0.65, color="w")
    plt.grid(False)
    plt.axis([0,len(dfprobRef.columns),0,101])
    plt.xticks(x, dfprobRef.columns,rotation=90,horizontalalignment='center', verticalalignment='top',
           position=(0,0),  fontsize=fs)
    plt.yticks(fontsize=fs)

    #plt.spines['top'].set_visible(False)
    #plt.axhline( 70, c='b', alpha=0.8,  linestyle='dashed')
    #dfprobRef.plot.scatter(x=dfprobRef.columns.values,y=range(0, 100))
    plt.ylabel('Probability of Cell-Type Similarity (%)',  position=(0,0.5), color=(0.2,0.2,0.2),
               alpha=0.8, fontsize=50)
    plt.xlabel("Cell Types", fontsize=50)
    sns.set_style("whitegrid")
    #plt.setp(ax.collections, alpha=.5)

    for i in range(len(dfprobRef.columns)):
        cells=dfpfcclus.T.loc[dfpfcclus.loc["Cluster"].isin([dfprobRef.columns[i]])].index
        dfprobReftemp=dfprobRef.loc[cells,dfprobRef.columns[i]]
        anum=fig.add_subplot(1,len(dfprobRef.columns),i+1)
        anum.axis([0,1,0,100])
        sns.violinplot(x=dfprobReftemp.index.name,
                       #y=dfprobReftemp.columns,
                       scale="area",bw=0.4,
                       cut=1.2,
                        gridsize=100,saturation=0.5, width=0.98,
                       color=mcolor_dict[mwanted_order[i]],
                       #palette=mcolor_dict[mwanted_order[i]] ,
                       inner= None, data=dfprobReftemp, ax=anum)
        plt.setp(anum.collections, alpha=.65)
        anum.scatter(list(np.random.random_sample(len(dfprobReftemp.index))-0.5),dfprobReftemp.values,
                    c=[mcolor_dict[mwanted_order[i]]]*len(dfprobReftemp.index), alpha=0.95,
                    s =200, edgecolors="grey", lw=2)
        anum.axis('off')

    plt.grid(False)

    # Turns off grid on the secondary (right) Axis.
    #ax.right_ax(False)

    plt.xticks(rotation=90,horizontalalignment='center', verticalalignment='top',
           position=(0,0), fontsize=fs)
    #plt.spines['top'].set_visible(False)
    #plt.axhline( 70, c='b', alpha=0.8,  linestyle='dashed')
    #dfprobRef.plot.scatter(x=dfprobRef.columns.values,y=range(0, 100))
    plt.ylabel('Probability of Cell-Type Similarity (%)', fontsize='large', position=(0,0.5), color=(0.2,0.2,0.2), alpha=0.8)
    plt.xlabel("Cell Types", fontsize=fs)
    #plt.title("Cell-Type Similarity")
    #plt.savefig("ViolinPlot %s.png"%"SOXtest4", bbox_inches="tight")

    recs = []
    for item in mwanted_order:
        recs.append(mpatches.Rectangle((0,0),1,1,fc=mcolor_dict[item]))
    plt.legend(recs,mwanted_order, loc=2,bbox_to_anchor=(1.1, 1.05), prop={'size': fs})
    #plt.savefig("GBMDGTFgenes_mDG_vs_PEgbm_wheel%sPlot.png"%cvalue,bbox_inches='tight')

        #plt.scatter(list(np.random.random_sample(len(dfprobRef.index))/3-0.16+i),dfprobRef.iloc[:,i].values.tolist(),
         #           c=array(list(mcolor_dict[mprotogruop].values)), alpha=0.9, edgecolors="grey", lw=0.3)
    return fig




def patch_violinplot():
    from matplotlib.collections import PolyCollection
    ax = plt.gca()
    for art in ax.get_children():
        if isinstance(art, PolyCollection):
            art.set_edgecolor((0.6, 0.6, 0.6))

def ProbMultiPlot( datax, mcolor_dict,fs=15):
     #dfprobRef, dfpfcclus, mwanted_order, mcolor_dict
#dfprobRef=dfprobRef, dfpfcclus=dfpfcclus, mwanted_order=mwanted_order,
                  # mcolor_dict=refcolor_dict
     mcolor_dict=pd.Series(mcolor_dict)
     mcolor_dict = mcolor_dict.map(lambda x: list(map(lambda y: y / 255., x)))
     dfprobRef = pd.DataFrame(datax.obsm["Celltype_Score"], index=datax.obs.index,
                              columns=datax.uns["Celltype_Score_RefCellType"])
     dfpfcclus = datax.obs[["mtrain_index", "Cluster"]].T
     mwanted_order = datax.uns["mwanted_order"]
     mprotogruop = datax.obs["Cluster"].values
     rdmvalue = np.random.choice(len(dfprobRef.index), 300, replace=False).tolist()
     dftemp = dfprobRef.iloc[rdmvalue, :]
     # seleColor=mnewcolors[rdmvalue]
     fig = plt.figure(figsize=(25, 10))
     fig, ax = plt.subplots()
     fig.set_size_inches(16, 8)
     sns.set_style("whitegrid")

     ax = sns.violinplot(y=dfprobRef.index.name, x=dfprobRef.columns.name, scale="width", bw=0.4, cut=2, gridsize=100,
                         saturation=0.9, width=0.98, palette=mcolor_dict[mwanted_order], inner=None, data=dfprobRef)
     plt.setp(ax.collections, alpha=.8)
     for i in range(len(dfprobRef.columns)):
         plt.scatter(list(np.random.random_sample(len(dfprobRef.index)) / 3 - 0.16 + i),
                     dfprobRef.iloc[:, i].values.tolist(), c=np.array(list(mcolor_dict[mprotogruop].values)), alpha=0.9,
                     edgecolors="grey", lw=0.3)

     # ax=sns.swarmplot(y=dftemp.index.name, x=dfprobRef.columns.name,size=5, edgecolor='gray', linewidth=0.1,palette=seleColor , data = dftemp)
     patch_violinplot()
     # plt.set_frame_on(False) #Remove both axes
     # Turns off grid on the left Axis.

     ax.set_ylim(ymin=0, ymax=100.5)
     ax.grid(False)

     # Turns off grid on the secondary (right) Axis.
     # ax.right_ax(False)

     plt.xticks(rotation=90, horizontalalignment='center', verticalalignment='top',
                position=(0, 0), fontsize=fs)
     ax.spines['top'].set_visible(False)
     # plt.axhline( 70, c='b', alpha=0.8,  linestyle='dashed')
     # dfprobRef.plot.scatter(x=dfprobRef.columns.values,y=range(0, 100))
     plt.ylabel('Probability of Cell-Type Similarity (%)', fontsize=fs,
                position=(0, 0.5), color=(0.2, 0.2, 0.2),
                alpha=0.8)
     plt.xlabel("Cell Types", fontsize=fs)
     # plt.title("Cell-Type Similarity")
     # plt.savefig("ViolinPlot %s.png"%"SOXtest4", bbox_inches="tight")

     recs = []
     for item in mwanted_order:
         recs.append(mpatches.Rectangle((0, 0), 1, 1, fc=mcolor_dict[item]))
     ax.legend(recs, mwanted_order, loc=2, bbox_to_anchor=(1.05, 1.05), prop={'size': fs})
     # plt.savefig("GBMDGTFgenes_mDG_vs_PEgbm_wheel%sPlot.png"%cvalue,bbox_inches='tight')
     return fig



def scaling_data(datax, LogMinMax=False):
    XX = datax.X
    countsInEachCell = np.ravel(XX.astype(float).sum(1)).copy()
    # XX = XXV.copy()
    if issubclass(XX.dtype.type, (int, np.integer)):
        XX = XX.astype(np.float32)  # np.float32 or float (64)
    countsInEachCell = np.asarray(countsInEachCell)
    after = np.median(countsInEachCell[countsInEachCell > 0], axis=0)
    countsInEachCell += (countsInEachCell == 0)
    countsInEachCell = countsInEachCell / after
    np.divide(XX, countsInEachCell[:, None], out=XX)
    XX = (XX.T / XX.sum(1)).T * 100000
    if LogMinMax == True:
        XX = np.log10(XX + 1)
        XX = ((XX.T - XX.min(1)) / XX.max(1)).T

    XX = np.nan_to_num(XX)
    datax.layers["Scaled_Matrix"] = XX

    return datax


def MarkerGenePlot(datax, genelist, nrow=2,fc=12,colormapopt="cividis"):
    import math
    dfexpr = pd.DataFrame(datax.layers['Scaled_Matrix'].T, index=datax.var.index, columns=datax.obs.index)
    dfexpr = dfexpr.T
    dfexpr["UMAPX"] = datax.obsm["X_umap"][:, 0]
    dfexpr["UMAPY"] = datax.obsm["X_umap"][:, 1]
    fig = plt.figure(figsize=(15, 15), facecolor='w')
    for i in range(1, len(genelist) + 1):
        genename = genelist[i - 1]
        plt.subplot(nrow, int(math.ceil(len(genelist) / nrow + 0.5)), i)
        dfe = dfexpr.sort_values(genename)
        plt.scatter(dfe["UMAPX"], dfe["UMAPY"], lw=0.1, edgecolor="grey", c=dfe[genename], s=int(80 / nrow),
                    cmap="cividis")
        plt.title(genename, fontsize=fc)
        plt.axis("off")
    return fig



def ConstrualValue(datax,net,filepath, ConstrualModel="DeepLift", MarkerGeneFinder=True,fcV=3, pValCutOff = 0.1):
    torch.manual_seed(0);
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print("CamelRunning with %s"%device)
    if "test_set_values" in datax.obsm:
        mdf_train_set = pd.DataFrame(datax.obsm["test_set_values"].T, index=datax.uns["train_set_gene"],
                                 columns=datax.obs.index)
    elif "train_set_values" in datax.obsm:
        mdf_train_set = pd.DataFrame(datax.obsm["train_set_values"].T, index=datax.uns["train_set_gene"],
                                     columns=datax.obs.index)
    normalizer = 0.9 * mdf_train_set.values.max(1)[:, np.newaxis]
    train = torch.tensor((mdf_train_set.values / normalizer).T.astype(np.float32))
    Refmodel = net.module_
    DataInput = Variable(train, requires_grad=True).to(device)
    if ConstrualModel=="DeepLift":
        from captum.attr import DeepLift
        algorithm = DeepLift(Refmodel)
        # attr_dl = attribute_image_features(dl, data, baselines=0)
        attrValue = algorithm.attribute(DataInput,target=0)
        datax.obsm["ConstrualValue_DeepLift"] =abs(attrValue .detach().cpu().numpy())
        #abs(attrValue .detach().cpu().numpy()),  attrValue is either neg or posi, set abs()
        #datax.uns["train_set_gene"]
    if MarkerGeneFinder==True:
        df_dev=pd.DataFrame(datax.obsm["ConstrualValue_DeepLift"].T*10000,
                             index=datax.uns["train_set_gene"], columns=datax.obs.index)
        dfpfcclus=datax.obs["Cluster"]
        dftestnew=enrichmentscoreBETA(dfpfcclus=dfpfcclus, df_dev=df_dev, fc=fcV,
                                      pvalcutoff = pValCutOff, shortcut=False)
        dfmarker=dftestnew
        with pd.ExcelWriter(filepath) as writer:
            grouplist = datax.uns['mwanted_order']
            ESmarkerlist = []
            columnlist = []
            for i in range(0, len(grouplist) + 1):
                if i == 0:
                    dfmarker.to_excel(writer, sheet_name='All_Summary', index=True, header=True)
                else:
                    dftemp = dfmarker.loc[dfmarker["Group"] == grouplist[i - 1]].sort_values([grouplist[i - 1]],
                                                                                             ascending=False)
                    dftemp.to_excel(writer, sheet_name=grouplist[i - 1], index=True, header=True)
                    ESmarkerlist.append(dftemp.index[:100].tolist())
                    ESmarkerlist.append((100 * dftemp["Num"] / len(grouplist)).astype(int)[:100].tolist())
                    columnlist.append(grouplist[i - 1])
                    columnlist.append("%s_CrossSigScore%%" % grouplist[i - 1])
            dfmk100 = pd.DataFrame(ESmarkerlist, index=columnlist).T
            dfmk100.to_csv("%s_Top100Marker.csv"%filepath,sep="\t")
            datax.uns["TopMarkerGene"]=dfmk100.values
            datax.uns["TopMarkerGene_Cluster"]=columnlist
        return datax
    else:
        return datax

def ConstrualValue22(datax,net,filepath, ConstrualModel="DeepLift", targetvalue=0,MarkerGeneFinder=True,fcV=3, pValCutOff = 0.1):
    torch.manual_seed(0);
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print("CamelRunning with %s"%device)
    if "test_set_values" in datax.obsm:
        mdf_train_set = pd.DataFrame(datax.obsm["test_set_values"].T, index=datax.uns["train_set_gene"],
                                 columns=datax.obs.index)
    elif "train_set_values" in datax.obsm:
        mdf_train_set = pd.DataFrame(datax.obsm["train_set_values"].T, index=datax.uns["train_set_gene"],
                                     columns=datax.obs.index)
    normalizer = 0.9 * mdf_train_set.values.max(1)[:, np.newaxis]
    train = torch.tensor((mdf_train_set.values / normalizer).T.astype(np.float32))
    Refmodel = net.module_
    DataInput = Variable(train, requires_grad=True).to(device)
    if ConstrualModel=="DeepLift":
        from captum.attr import DeepLift
        algorithm = DeepLift(Refmodel)
        # attr_dl = attribute_image_features(dl, data, baselines=0)
        attrValue, deltav = algorithm.attribute(DataInput,target=targetvalue, return_convergence_delta=True)
        datax.obsm["ConstrualValue_DeepLift"] =abs(attrValue .detach().cpu().numpy())
        datax.obsm["ConstrualDelta_DeepLift"] =abs( deltav .detach().cpu().numpy())
        #abs(attrValue .detach().cpu().numpy()),  attrValue is either neg or posi, set abs()
        #datax.uns["train_set_gene"]
    if MarkerGeneFinder==True:
        df_dev=pd.DataFrame(datax.obsm["ConstrualValue_DeepLift"].T*10000,
                             index=datax.uns["train_set_gene"], columns=datax.obs.index)
        dfpfcclus=datax.obs["Cluster"]
        dftestnew=enrichmentscoreBETA(dfpfcclus=dfpfcclus, df_dev=df_dev, fc=fcV,
                                      pvalcutoff = pValCutOff, shortcut=False)
        dfmarker=dftestnew
        with pd.ExcelWriter(filepath) as writer:
            grouplist = datax.uns['mwanted_order']
            ESmarkerlist = []
            columnlist = []
            for i in range(0, len(grouplist) + 1):
                if i == 0:
                    dfmarker.to_excel(writer, sheet_name='All_Summary', index=True, header=True)
                else:
                    dftemp = dfmarker.loc[dfmarker["Group"] == grouplist[i - 1]].sort_values([grouplist[i - 1]],
                                                                                             ascending=False)
                    dftemp.to_excel(writer, sheet_name=grouplist[i - 1], index=True, header=True)
                    ESmarkerlist.append(dftemp.index[:100].tolist())
                    ESmarkerlist.append((100 * dftemp["Num"] / len(grouplist)).astype(int)[:100].tolist())
                    columnlist.append(grouplist[i - 1])
                    columnlist.append("%s_CrossSigScore%%" % grouplist[i - 1])
            dfmk100 = pd.DataFrame(ESmarkerlist, index=columnlist).T
            dfmk100.to_csv("%s_Top100Marker.csv"%filepath,sep="\t")
            datax.uns["TopMarkerGene"]=dfmk100.values
            datax.uns["TopMarkerGene_Cluster"]=columnlist
        return datax
    else:
        return datax


def ConstrualValueRef(datax,net, ConstrualModelvalue="DeepLift"):
    clist=[]
    for i in datax.uns['Celltype_OrderNumber']:
        datax=ConstrualValue22(datax=datax,net=net, filepath=None,targetvalue=i,
                               ConstrualModel="DeepLift",MarkerGeneFinder=False,
                               fcV=1.5, pValCutOff = 0.1)
        clist.append(datax.obsm['ConstrualValue_DeepLift'].T.sum(1).tolist())
    datax.uns['ConstrualValue_DeepLift_ClusterRef']=np.array(clist)
    #dftestx=pd.DataFrame(clist)
    #dftestx.columns=datax.uns[ 'train_set_gene']
    #dftestx.index=datax.uns[ 'mclasses_names']
    #dfprob=pd.DataFrame(datax.obsm['Celltype_Score'])
    #dfprob.index=datax.obs.index
    #dfprob.columns=datax.uns[ 'mclasses_names']
    dfsum=pd.DataFrame(np.dot(datax.obsm['Celltype_Score'],datax.uns['ConstrualValue_DeepLift_ClusterRef']))
    dfsum.columns=datax.uns[ 'train_set_gene']
    dfsum.index=datax.obs.index
    dfref=(dfsum/dfsum.max()).fillna(0)
    dfrefv=pd.DataFrame(datax.obsm[ 'train_set_values'])
    dfrefv.columns=datax.uns[ 'train_set_gene']
    dfrefv.index=datax.obs.index
    dfrefv=dfrefv/dfrefv.max()
    dfall=(dfrefv*dfref)**0.5
    datax.obsm["NormalizedMatrix"]=dfall.values
    return datax

def ConstrualValuePrediction(datapdt, dataref):
    # dataref.uns['ConstrualValue_DeepLift_ClusterRef']=np.array(clist)
    # dftestx=pd.DataFrame(clist)
    # dftestx.columns=datax.uns[ 'train_set_gene']
    # dftestx.index=datax.uns[ 'mclasses_names']
    # dfprob=pd.DataFrame(datax.obsm['Celltype_Score'])
    # dfprob.index=datax.obs.index
    # dfprob.columns=datax.uns[ 'mclasses_names']
    dfsum = pd.DataFrame(np.dot(datapdt.obsm['Celltype_Score'], dataref.uns['ConstrualValue_DeepLift_ClusterRef']))
    dfsum.columns = dataref.uns['train_set_gene']
    dfsum.index = datapdt.obs.index
    dfref = (dfsum / dfsum.max()).fillna(0)
    dfrefv = pd.DataFrame(datapdt.obsm['test_set_values'])
    dfrefv.columns = dataref.uns['train_set_gene']
    dfrefv.index = datapdt.obs.index
    dfrefv = dfrefv / dfrefv.max()
    dfall = (dfrefv * dfref) ** 0.5
    datapdt.obsm["NormalizedMatrix"] = dfall.values
    return datapdt
    
def MarkerDotPlot(datax,filepath, clustername):
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes
    df=pd.DataFrame(datax.X.T,index=datax.var.index,columns=datax.obs.index)
    dfmk=pd.read_table(filepath,index_col=0,sep="\t")
    dfgrpref=df.loc[dfmk[clustername].dropna().values].T
    dfgrpref["Cluster"]=datax.obs["Cluster"]
    dfgrpref=dfgrpref[dfgrpref.columns[::-1]]
    dfmean=dfgrpref.groupby(["Cluster"]).mean()
    dfmean=dfmean/dfmean.sum()
    grpNzCount = dfgrpref.groupby(['Cluster']).agg(lambda x: x.ne(0).sum())/dfgrpref.groupby(["Cluster"]).count()
    xvalue=[]
    for i in range(len(dfmean.index)):
        xvalue.extend([dfmean.index[i]]*len(dfmean.columns))
    yvalue=[]
    yvalue.extend((dfmean.columns.tolist())*len(dfmean.index))
    sns.set_style(style='white')
    plt.figure(figsize=(7,30), facecolor='w')
    plt.rcParams['xtick.bottom'] = plt.rcParams['xtick.labelbottom'] = False
    plt.rcParams['xtick.top'] = plt.rcParams['xtick.labeltop'] = True

    plt.xticks(fontsize=15, rotation=90)
    plt.yticks(fontsize=15, rotation=0)
    ax=plt.scatter( xvalue,yvalue,s = (grpNzCount *250).values.flatten(),
                c=dfmean.values.flatten(),cmap="plasma",
                alpha=.95,
                lw=0.2)
    plt.title(clustername, fontsize=20)

    plt.colorbar(ax, anchor=(0.5,1),fraction=0.05)
    plt.grid("on",alpha=0.5)
    return ax


def CellTypeSimilarity(datax, labelnum=False, RowCluster=True, fontsizeWeight=0.65,
                        ColCluster=True, metricvalue='correlation', methodvalue="average"):
    dfprob = pd.DataFrame(datax.obsm['Celltype_Score'], index=datax.obs.index,
                          columns=datax.uns['Celltype_Score_RefCellType'])
    dfprob["Cluster"] = datax.obs["Cluster"]
    dfpb2 = dfprob.groupby(["Cluster"]).mean()
    dfpb2 = (dfpb2 + dfpb2.T) / 2
    correlations_array = np.asarray(np.log2(dfpb2.values + 1))
    if labelnum == False:
        sns.set(font_scale=1)
        row_linkage1 = hierarchy.linkage(
            distance.pdist(correlations_array),
            method=methodvalue,
            metric=metricvalue
        )

        col_linkage1 = hierarchy.linkage(
            distance.pdist(correlations_array.T),
            method=methodvalue,
            metric=metricvalue
        )
        plt.figure(figsize=(int(dfpb2.shape[1]), int(dfpb2.shape[0])))
        sns.set_style("white")
        sns.set(font_scale=fontsizeWeight)

        cg = sns.clustermap(np.log10(dfpb2 + 1) ** 0.75,
                            row_linkage=row_linkage1,
                            col_linkage=col_linkage1,
                            method=methodvalue,
                            metric=metricvalue,
                            # z_score=0,
                            row_cluster=RowCluster, col_cluster=ColCluster,
                            figsize=(int(dfpb2.shape[1]), int(dfpb2.shape[0])),
                            cmap="cividis")
        plt.setp(cg.ax_heatmap.yaxis.get_majorticklabels(), rotation=0, fontsize=15)
        plt.setp(cg.ax_heatmap.xaxis.get_majorticklabels(), rotation=90, fontsize=15)
    elif labelnum == True:
        sns.set(font_scale=1)
        labels = dfpb2.values
        labels = labels.round(decimals=1)
        row_linkage1 = hierarchy.linkage(
            distance.pdist(correlations_array),
            method=methodvalue,
            metric=metricvalue
        )
        plt.figure(figsize=(int(dfpb2.shape[1]), int(dfpb2.shape[0])))
        sns.set_style("white")
        sns.set(font_scale=fontsizeWeight)
        col_linkage1 = hierarchy.linkage(
            distance.pdist(correlations_array.T),
            method=methodvalue,
            metric=metricvalue
        )
        cg = sns.clustermap(np.log10(dfpb2 + 1) ** 0.75,
                            row_linkage=row_linkage1,
                            col_linkage=col_linkage1,
                            annot=labels,
                            method=methodvalue,
                            metric=metricvalue,
                            # z_score=0,
                            row_cluster=RowCluster, col_cluster=ColCluster,
                            figsize=(int(dfpb2.shape[1]), int(dfpb2.shape[0])), cmap="cividis")
        plt.setp(cg.ax_heatmap.yaxis.get_majorticklabels(), rotation=0, fontsize=15)
        plt.setp(cg.ax_heatmap.xaxis.get_majorticklabels(), rotation=90, fontsize=15)

def SelfSimilarity(datax, labelnum=False, RowCluster=True,
                   ColCluster=True, metricvalue='correlation',methodvalue="average"):
    dfprob = pd.DataFrame(datax.obsm['Celltype_Score'], index=datax.obs.index,
                          columns=datax.uns['Celltype_Score_RefCellType'])
    dfprob["Cluster"] = datax.obs["Cluster"]
    dfpb2 = dfprob.groupby(["Cluster"]).mean()
    dfpb2 = (dfpb2 + dfpb2.T) / 2
    if labelnum==False:
        sns.set(font_scale=1)

        cg = sns.clustermap(np.log2(dfpb2 + 1), cmap="CMRmap",
                            method=methodvalue,
                            metric=metricvalue,
                            row_cluster=RowCluster, col_cluster=ColCluster,
                            z_score=1, figsize=(10, 10))
        plt.setp(cg.ax_heatmap.yaxis.get_majorticklabels(), rotation=0, fontsize=15)
        plt.setp(cg.ax_heatmap.xaxis.get_majorticklabels(), rotation=90, fontsize=15)
    elif labelnum==True:
        sns.set(font_scale=1)
        labels = dfpb2.values
        labels = labels.round(decimals=1)
        cg = sns.clustermap(np.log2(dfpb2 + 1), cmap="CMRmap",
                            method=methodvalue,
                            metric=metricvalue,
                            annot=labels,
                            row_cluster=RowCluster, col_cluster=ColCluster,
                            z_score=1, figsize=(10, 10))
        plt.setp(cg.ax_heatmap.yaxis.get_majorticklabels(), rotation=0, fontsize=15)
        plt.setp(cg.ax_heatmap.xaxis.get_majorticklabels(), rotation=90, fontsize=15)


def ConvertSparse(adata):
    if type(adata.X)==sparse.csr.csr_matrix:
        adata.X=adata.X.todense()
    return adata


def writedata(adatax,filename,filepath=""):
    adatax.X= sparse.csr_matrix(adatax.X)
    adatax.write(os.path.join(filepath, filename))

def enrichmentscoreBETA(dfpfcclus, df_dev, fc=3, pvalcutoff=0.1, shortcut=True):
    # dfpfcclus = dfpfcclus, df_dev = df_dev, fc = 1.25, shortcut = True
    dfgrp = df_dev.T.astype(float).join(dfpfcclus.T, how="inner")
    dfmean = dfgrp.groupby(['Cluster']).mean()
    dfmedian = dfgrp.groupby(['Cluster']).median().T
    df_means = df_dev.mean(1)
    if shortcut == False:
        print("Camel...Running: clusteringValue1...")
        TotalNzCount = np.sum(dfgrp.iloc[:, :-1] >  0)
        grpNzCount = dfgrp.groupby(['Cluster']).agg(lambda x: x.ne(0).sum())
        print("Camel...Running: clusteringValue2...")
        RestNzCount = TotalNzCount - grpNzCount
        RatioNzCount = (grpNzCount + 0.1) / (RestNzCount + 0.1)/dfgrp.groupby(["Cluster"]).count()*1000
        dfmean = dfmean.T.loc[RatioNzCount.columns].T
        df_means = df_means.loc[RatioNzCount.columns]
        df_fold = (dfmean + 0.01).div(df_means + 0.01, axis=1) ** 0.5
        # df_fold=dfmean.div(df_means,axis=1)
        print("Camel...Running: Enrichment1...")
        EScore = df_fold[RatioNzCount.columns].fillna(0) * RatioNzCount
        EScore = EScore.T
        df_fold = df_fold.T.fillna(0)
        df_avgpos = df_means
        df_avgpos = df_avgpos.fillna(0.0)
        score00 = df_fold
        score10 = df_fold.multiply(df_avgpos, axis=0)
        ix00 = np.argsort(score00, 0)
        # ix05 = np.argsort( score05 , 0)
        ix10 = np.argsort(score10, 0)
        markers = defaultdict(set)
        N = int(len(df_fold.index) / len(df_fold.columns) * 3)
        N= min(len(df_fold.index), N)
        print("Camel...Running: CrossChecking...")
        for ct in df_fold.columns:
            markers[ct] |= set(df_fold.index[ix00.loc[:, ct][::-1]][:N])
            markers[ct] |= set(df_fold.index[ix10.loc[:, ct][::-1]][:N])

        RatioNzCount = RatioNzCount.T
        # RatioNzCount = RatioNzCount.T
        mkdict = {}
        sys.stdout.write("[%s]" % "Processing")
        sys.stdout.flush()
        sys.stdout.write("\b" * (50 + 1))  # return to start of line, after '['
        perc = len(df_fold.columns)
        for ct in df_fold.columns:
            temp = {}
            for num in range(min(3, int(len(df_fold.columns) / 4) + 1), len(df_fold.columns)):
                temp[num] = []
            dftemp1 = dfgrp.loc[dfgrp["Cluster"] == ct]
            # y=0

            itemindex = df_fold.columns.tolist().index(ct)
            # setup toolbar

            sys.stdout.write("-%s%%-" % int(itemindex * 100 / perc))
            sys.stdout.flush()
            for mk in markers[ct]:
                x = 0
                # y = 0
                dfgrpmk = dfgrp[[mk, "Cluster"]]
                for ct2 in list(set(df_fold.columns) - set([ct])):
                    dftemp2 = dfgrpmk.loc[dfgrpmk["Cluster"] == ct2]
                    pval = scipy.stats.ttest_ind(dftemp1[mk], dftemp2[mk], equal_var=False).pvalue
                    # if (score10.loc[mk,ct] >= float(score10.loc[mk,ct2])) & (EScore.loc[mk,ct] >= float(EScore.loc[mk,ct2]))&(ratiovalue.loc[mk,ct]>0.9)& (score10.loc[mk,ct] > 1) & (EScore.loc[mk,ct] > 1) :
                    if (score10.loc[mk, ct] >= float(score10.loc[mk, ct2]) * fc / 2) & (
                            EScore.loc[mk, ct] >= float(EScore.loc[mk, ct2]) * fc) & (pval < pvalcutoff):
                        x = x + 1
                    # if (score10.loc[mk, ct] * fc < float(score10.loc[mk, ct2])) & (
                    #      EScore.loc[mk, ct] * fc < float(EScore.loc[mk, ct2])):
                    # if (score10.loc[mk,ct] < float(score10.loc[mk,ct2])) & (EScore.loc[mk,ct] < float(EScore.loc[mk,ct2])) &(ratiovalue.loc[mk,ct]<0.1)& (EScore.loc[mk,ct] < 0.1):
                    # y = y + 1
                if x in list(range(min(3, int(len(df_fold.columns) / 4) + 1), len(df_fold.columns))):
                    temp[x].append(mk)
                # if y in list(range(min(3, int(len(df_fold.columns) / 4) + 1), len(df_fold.columns))):
                #  temp[y].append(mk)
                # markers[ct2] -= set([mk])
            # for num in range(2,len(df_fold.columns)-1):
            mkdict[ct] = temp
        genelist = []
        grouplist = []
        numberlist = []
        for num in range(min(3, int(len(df_fold.columns) / 4) + 2), len(df_fold.columns)):
            for ct in df_fold.columns:
                genelist.extend(mkdict[ct][num])
                grouplist.extend([ct] * len(mkdict[ct][num]))
                numberlist.extend([num] * len(mkdict[ct][num]))
        print("Camel...Running: Marker is coming out...")
        dfmk = pd.DataFrame([genelist, grouplist, numberlist])
        dfmk.columns = dfmk.iloc[0, :]
        dfmk = dfmk.T
        dfmk.columns = ["Gene", "Group", "Num"]
        dftest = EScore.loc[dfmk.index]
        dftest = dfmk.iloc[:, 1:].T.append(dftest.T)
        dftest = dftest.T.sort_values(by=['Group', 'Num'], ascending=[True, False])
        collist = []
        for item in score10.columns:
            collist.append("Expr_%s" % item)
        score10.columns = collist
        dftestnew = dftest.join(score10, how="inner")
        # list_genes = list(set(dftestnew.index))
        return dftestnew
    elif shortcut == True:
        # df_fold=(dfmean+0.01).div(df_means+0.01,axis=1)**0.5
        print("Camel...Running: clusteringValue1...")
        df_fold = dfmean.div(df_means, axis=1)
        # dfmean=dfgrp.groupby(['Cluster']).mean()
        # df_means = df_dev.mean(1)
        # df_fold=dfmean.div(df_means,axis=1)
        df_fold = df_fold.T.dropna()
        df_avgpos = df_means
        df_avgpos = df_avgpos.fillna(0)
        score00 = df_fold
        score10 = df_fold.multiply(df_avgpos, axis=0)
        print("Camel...Running: clusteringValue2...")

        ix00 = np.argsort(score00, 0)
        ix10 = np.argsort(score10, 0)
        markers = defaultdict(set)
        N = int(len(df_fold.index) / len(df_fold.columns) * 3)
        N = min(len(df_fold.index), N)
        print(N)
        sys.stdout.write("[%s]" % "Processing")
        sys.stdout.flush()
        sys.stdout.write("\b" * (50 + 1))  # return to start of line, after '['
        perc = len(df_fold.columns)
        for ct in df_fold.columns:
            markers[ct] |= set(df_fold.index[ix00.loc[:, ct][::-1]][:N])
            markers[ct] |= set(df_fold.index[ix10.loc[:, ct][::-1]][:N])
        print(len(markers))
        print("Camel...Running: CrossChecking...")
        genelist = []
        for ct in df_fold.columns:
            for mk in markers[ct]:
                for ct2 in list(set(df_fold.columns) - set([ct])):
                    if (score10.loc[mk, ct] >= float(score10.loc[mk, ct2])* fc) & (
                            score00.loc[mk, ct] >= float(score00.loc[mk, ct2])* fc ) & (dfmedian.loc[mk, ct] > 0):
                        genelist.append(mk)
                    #elif (score10.loc[mk, ct] < float(score10.loc[mk, ct2])) & (
                     #       score00.loc[mk, ct] < float(score00.loc[mk, ct2])) & (dfmedian.loc[mk, ct] <= 0):
                      #  genelist.append(mk)
            itemindex = df_fold.columns.tolist().index(ct)
            # setup toolbar

            sys.stdout.write("-%s%%-" % int(itemindex * 100 / perc))
            sys.stdout.flush()
        print("Camel...Running: output genelist...")
        return genelist

