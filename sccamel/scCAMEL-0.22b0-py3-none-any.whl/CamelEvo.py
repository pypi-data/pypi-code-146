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
import pandas as pd
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.model_selection import StratifiedShuffleSplit
from collections import defaultdict
from sklearn import preprocessing
import matplotlib.patches as mpatches
import torch.nn.functional as F
import math
#import gpytorch
import logging
import datetime
from scipy import sparse
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.cross_decomposition import CCA
import pandas as pd
import os.path
from arboreto.utils import load_tf_names
from arboreto.algo import grnboost2
from distributed import LocalCluster, Client
from kneed import KneeLocator
import scanpy as sc
import matplotlib.patches as patches
from matplotlib import pyplot as plt
from matplotlib.path import Path

from matplotlib.collections import PatchCollection

import urllib.request
import os.path
from scipy.io import loadmat
from math import floor
import anndata
# Make plots inline

import scipy.cluster.hierarchy as sch
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
import matplotlib
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.spatial import distance
from scipy.cluster import hierarchy
import matplotlib.patches as patches
from matplotlib import pyplot as plt
from matplotlib.path import Path

from matplotlib.collections import PatchCollection


# import seaborn as sns
# sns.set_theme()

colormap_list = ["nipy_spectral", "terrain", "gist_rainbow", "CMRmap", "coolwarm", "gnuplot", "gist_stern", "brg",
                 "rainbow"]

def CAMEL_RTplot(Z2, fontsize=20, figsize=[10, 10], pallete="gist_rainbow", addlabels=True, figsavename="test.pdf",
                 sample_classes=None, colorlabels=None,
                 colorlabels_legend=None):
    """
    Rebuilt, originally from RadialTree https://github.com/koonimaru/radialtree
    Drawing a radial dendrogram from a scipy dendrogram output.
    Parameters
    ----------
    Z2 : dictionary
        A dictionary returned by scipy.cluster.hierarchy.dendrogram
    addlabels: bool
        A bool to choose if labels are shown.
    fontsize : float
        A float to specify the font size
    figsize : [x, y] array-like
        1D array-like of floats to specify the figure size
    pallete : string
        Matlab colormap name.
    sample_classes : dict
        A dictionary that contains lists of sample subtypes or classes. These classes appear
        as color labels of each leaf. Colormaps are automatically assigned. Not compatible
        with options "colorlabels" and "colorlabels_legend".
        e.g., {"color1":["Class1","Class2","Class1","Class3", ....]}
    colorlabels : dict
        A dictionary to set color labels to leaves. The key is the name of the color label.
        The value is the list of RGB color codes, each corresponds to the color of a leaf.
        e.g., {"color1":[[1,0,0,1], ....]}
    colorlabels_legend : dict
        A nested dictionary to generate the legends of color labels. The key is the name of
        the color label. The value is a dictionary that has two keys "colors" and "labels".
        The value of "colors" is the list of RGB color codes, each corresponds to the class of a leaf.
        e.g., {"color1":{"colors":[[1,0,0,1], ....], "labels":["label1","label2",...]}}

    Returns
    -------
    Raises
    ------
    Notes
    -----
    References
    ----------
    See Also
    --------
    Examples
    --------
    """
    if figsize == None and colorlabels != None:
        figsize = [10, 5]
    elif figsize == None and sample_classes != None:
        figsize = [10, 5]
    elif figsize == None:
        figsize = [5, 5]
    # linewidth=0.5
    linewidth = 2
    R = 1
    # width=R*0.1
    width = R * 0.5
    space = R * 0.5
    if colorlabels != None:
        offset = width * len(colorlabels) / R + space * (len(colorlabels) - 1) / R + 0.05
        print(offset)
    elif sample_classes != None:
        offset = width * len(sample_classes) / R + space * (len(sample_classes) - 1) / R + 0.05
        print(offset)
    else:
        offset = 0
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial']
    plt.rcParams['svg.fonttype'] = 'none'
    xmax = np.amax(Z2['icoord'])
    ymax = np.amax(Z2['dcoord'])

    ucolors = sorted(set(Z2["color_list"]))
    # cmap = cm.gist_rainbow(np.linspace(0, 1, len(ucolors)))
    cmp = cm.get_cmap(pallete, len(ucolors))
    # print(cmp)
    if type(cmp) == matplotlib.colors.LinearSegmentedColormap:
        cmap = cmp(np.linspace(0, 1, len(ucolors)))
    else:
        cmap = cmp.colors
    fig, ax = plt.subplots(figsize=figsize)
    i = 0
    label_coords = []
    for x, y, c in sorted(zip(Z2['icoord'], Z2['dcoord'], Z2["color_list"])):
        # x, y = Z2['icoord'][0], Z2['dcoord'][0]
        _color = cmap[ucolors.index(c)]
        if c == "C0":  # np.abs(_xr1)<0.000000001 and np.abs(_yr1) <0.000000001:
            _color = "black"

        # transforming original x coordinates into relative circumference positions and y into radius
        # the rightmost leaf is going to [1, 0]
        r = R * (1 - np.array(y) / ymax)
        _x = np.cos(2 * np.pi * np.array(
            [x[0], x[2]]) / xmax)  # transforming original x coordinates into x circumference positions
        _xr0 = _x[0] * r[0]
        _xr1 = _x[0] * r[1]
        _xr2 = _x[1] * r[2]
        _xr3 = _x[1] * r[3]
        _y = np.sin(2 * np.pi * np.array(
            [x[0], x[2]]) / xmax)  # transforming original x coordinates into y circumference positions
        _yr0 = _y[0] * r[0]
        _yr1 = _y[0] * r[1]
        _yr2 = _y[1] * r[2]
        _yr3 = _y[1] * r[3]
        # plt.scatter([_xr0, _xr1, _xr2, _xr3],[_yr0, _yr1, _yr2,_yr3], c="b")

        # if y[0]>0 and y[3]>0:
        # _color="black"
        # plotting radial lines
        plt.plot([_xr0, _xr1], [_yr0, _yr1], c=_color, linewidth=linewidth)
        plt.plot([_xr2, _xr3], [_yr2, _yr3], c=_color, linewidth=linewidth)

        # plotting circular links between nodes
        if _yr1 > 0 and _yr2 > 0:
            link = np.sqrt(r[1] ** 2 - np.linspace(_xr1, _xr2, 100) ** 2)
            plt.plot(np.linspace(_xr1, _xr2, 100), link, c=_color, linewidth=linewidth)
        elif _yr1 < 0 and _yr2 < 0:
            link = -np.sqrt(r[1] ** 2 - np.linspace(_xr1, _xr2, 100) ** 2)

            plt.plot(np.linspace(_xr1, _xr2, 100), link, c=_color, linewidth=linewidth)
        elif _yr1 > 0 and _yr2 < 0:
            _r = r[1]
            if _xr1 < 0 or _xr2 < 0:
                _r = -_r
            link = np.sqrt(r[1] ** 2 - np.linspace(_xr1, _r, 100) ** 2)
            plt.plot(np.linspace(_xr1, _r, 100), link, c=_color, linewidth=linewidth)
            link = -np.sqrt(r[1] ** 2 - np.linspace(_r, _xr2, 100) ** 2)
            plt.plot(np.linspace(_r, _xr2, 100), link, c=_color, linewidth=linewidth)

        # Calculating the x, y coordinates and rotation angles of labels

        if y[0] == 0:
            label_coords.append([(1.05 + offset) * _xr0, (1.05 + offset) * _yr0, 360 * x[0] / xmax])
            # plt.text(1.05*_xr0, 1.05*_yr0, Z2['ivl'][i],{'va': 'center'},rotation_mode='anchor', rotation=360*x[0]/xmax)
            i += 1
        if y[3] == 0:
            label_coords.append([(1.05 + offset) * _xr3, (1.05 + offset) * _yr3, 360 * x[2] / xmax])
            # plt.text(1.05*_xr3, 1.05*_yr3, Z2['ivl'][i],{'va': 'center'},rotation_mode='anchor', rotation=360*x[2]/xmax)
            i += 1

    if addlabels == True:
        assert len(Z2['ivl']) == len(label_coords), "Internal error, label numbers " + str(
            len(Z2['ivl'])) + " and " + str(len(label_coords)) + " must be equal!"

        # Adding labels
        for (_x, _y, _rot), label in zip(label_coords, Z2['ivl']):
            if label.split("_")[0] == "Macq":
                colortemp = "red"
            elif label[0] == "h":
                colortemp = "blue"
            else:
                colortemp = "grey"
            if (_rot >= 270) or (_rot < 90):
                plt.text(_x, _y, label, {'va': 'center'}, rotation_mode='anchor', rotation=_rot, c=colortemp,
                         horizontalalignment="left", verticalalignment="center",
                         fontsize=fontsize)
            else:
                plt.text(_x, _y, label, {'va': 'center'}, rotation_mode='anchor', rotation=180 + _rot, c=colortemp,
                         horizontalalignment="right", verticalalignment="center",
                         fontsize=fontsize)

    if colorlabels != None:
        assert len(Z2['ivl']) == len(label_coords), "Internal error, label numbers " + str(
            len(Z2['ivl'])) + " and " + str(len(label_coords)) + " must be equal!"

        j = 0
        outerrad = R * 1.05 + width * len(colorlabels) + space * (len(colorlabels) - 1)
        print(outerrad)
        # sort_index=np.argsort(Z2['icoord'])
        # print(sort_index)
        intervals = []
        for i in range(len(label_coords)):
            _xl, _yl, _rotl = label_coords[i - 1]
            _x, _y, _rot = label_coords[i]
            if i == len(label_coords) - 1:
                _xr, _yr, _rotr = label_coords[0]
            else:
                _xr, _yr, _rotr = label_coords[i + 1]
            d = ((_xr - _xl) ** 2 + (_yr - _yl) ** 2) ** 0.5
            intervals.append(d)
        colorpos = intervals  # np.ones([len(label_coords)])
        labelnames = []
        for labelname, colorlist in colorlabels.items():
            colorlist = np.array(colorlist)[Z2['leaves']]
            outerrad = outerrad - width * j - space * j
            innerrad = outerrad - width
            patches, texts = plt.pie(colorpos, colors=colorlist,
                                     radius=outerrad,
                                     counterclock=True,
                                     startangle=label_coords[0][2] * 0.5)
            circle = plt.Circle((0, 0), innerrad, fc='whitesmoke')
            plt.gca().add_patch(circle)
            labelnames.append(labelname)
            j += 1

        if colorlabels_legend != None:
            for i, labelname in enumerate(labelnames):
                print(colorlabels_legend[labelname]["colors"])
                colorlines = []
                for c in colorlabels_legend[labelname]["colors"]:
                    colorlines.append(Line2D([0], [0], color=c, lw=8))
                leg = plt.legend(colorlines,
                                 colorlabels_legend[labelname]["labels"],
                                 bbox_to_anchor=(1.5 + 0.3 * i, 1.0),
                                 title=labelname)
                plt.gca().add_artist(leg)
    elif sample_classes != None:
        assert len(Z2['ivl']) == len(label_coords), "Internal error, label numbers " + str(
            len(Z2['ivl'])) + " and " + str(len(label_coords)) + " must be equal!"

        j = 0
        outerrad = R * 1.05 + width * len(sample_classes) + space * (len(sample_classes) - 1)
        print(outerrad)
        # sort_index=np.argsort(Z2['icoord'])
        # print(sort_index)
        intervals = []
        for i in range(len(label_coords)):
            _xl, _yl, _rotl = label_coords[i - 1]
            _x, _y, _rot = label_coords[i]
            if i == len(label_coords) - 1:
                _xr, _yr, _rotr = label_coords[0]
            else:
                _xr, _yr, _rotr = label_coords[i + 1]
            d = ((_xr - _xl) ** 2 + (_yr - _yl) ** 2) ** 0.5
            intervals.append(d)
        colorpos = intervals  # np.ones([len(label_coords)])
        labelnames = []
        colorlabels_legend = {}
        for labelname, colorlist in sample_classes.items():
            ucolors = sorted(list(np.unique(colorlist)))
            type_num = len(ucolors)
            _cmp = cm.get_cmap(colormap_list[j], type_num)
            _colorlist = [_cmp(ucolors.index(c) / (type_num - 1)) for c in colorlist]
            _colorlist = np.array(_colorlist)[Z2['leaves']]
            outerrad = outerrad - width * j - space * j
            innerrad = outerrad - width
            patches, texts = plt.pie(colorpos, colors=_colorlist,
                                     radius=outerrad,
                                     counterclock=True,
                                     startangle=label_coords[0][2] * 0.5)
            circle = plt.Circle((0, 0), innerrad, fc='whitesmoke')
            plt.gca().add_patch(circle)
            labelnames.append(labelname)
            colorlabels_legend[labelname] = {}
            colorlabels_legend[labelname]["colors"] = _cmp(np.linspace(0, 1, type_num))
            colorlabels_legend[labelname]["labels"] = ucolors
            j += 1

        if colorlabels_legend != None:
            for i, labelname in enumerate(labelnames):
                print(colorlabels_legend[labelname]["colors"])
                colorlines = []
                for c in colorlabels_legend[labelname]["colors"]:
                    colorlines.append(Line2D([0], [0], color=c, lw=8))
                leg = plt.legend(colorlines,
                                 colorlabels_legend[labelname]["labels"],
                                 bbox_to_anchor=(1.5 + 0.3 * i, 1.0),
                                 title=labelname)
                plt.gca().add_artist(leg)
            # break
    ax.spines.right.set_visible(False)
    ax.spines.top.set_visible(False)
    ax.spines.left.set_visible(False)
    ax.spines.bottom.set_visible(False)
    plt.xticks([])
    plt.yticks([])
    if colorlabels != None:
        maxr = R * 1.05 + width * len(colorlabels) + space * (len(colorlabels) - 1)
    elif sample_classes != None:
        maxr = R * 1.05 + width * len(sample_classes) + space * (len(sample_classes) - 1)
    else:
        maxr = R * 1.05
    plt.xlim(-maxr, maxr)
    plt.ylim(-maxr, maxr)

    # else:
    if figsavename != None:
        plt.savefig(figsavename, bbox_inches='tight')
    else:
        plt.show()
    # fig, ax

def PCAesti(adatax,ReadyModel=None):
    X =adatax.obsm["PCAraw0"]
    if ReadyModel==None:
        pca_ = PCA(n_components=adatax.obsm["PCAraw0"].shape[1]-1, svd_solver='arpack', random_state=0)
        PCAmodel= pca_.fit(X)
        #X_cca,Y_cca=cca_.fit_transform(X,Y)
        X_pcavalue=PCAmodel.transform(X)
        adatax.obsm['Celltype_ScoreAll']=X_pcavalue
        plt.figure(figsize=(5,5))
        plt.scatter(list(range(0,adatax.obsm["PCAraw0"].shape[1]-1)),PCAmodel.explained_variance_ratio_)
        plt.xlabel("Comp_Num",fontsize=15)
        plt.ylabel('PCAratio',fontsize=15)
        adatax.obsm['Celltype_ScoreAll']=X_pcavalue
        adatax.obsm['X_pca']=X_pcavalue
        adatax.uns['pca']=PCAmodel.explained_variance_ratio_
        return adatax, PCAmodel
    else:
        X_pcavalue=ReadyModel.transform(X)
        adatax.obsm['Celltype_ScoreAll']=X_pcavalue
        adatax.obsm['X_pca']=X_pcavalue
        adatax.uns['pca']=ReadyModel.explained_variance_ratio_
        return adatax



from scipy import sparse
import scipy

from scipy import sparse
import scipy


def FindGenePatterns(adata, celltypelabel="Cluster", corrThre=0.3, ThreNumber=2,
                      TopWeightedFilter=False, DatasetName=None, filelist=None, plotfig=False):
    if type(adata.X) == sparse.csr.csr_matrix:
        adata.X = adata.X.toarray()
    adata1 = adata[:, adata.X.T.sum(1) > 0]
    df_dev = pd.DataFrame(adata1.X.T, index=adata1.var.index, columns=adata1.obs.index)
    dfpfcclus = pd.DataFrame(adata1.obs[celltypelabel].values, index=adata1.obs.index, columns=[celltypelabel]).T
    logging.info('Camel_Evo...Running: select the signature genes from each cell types....')
    sc.tl.rank_genes_groups(adata1, celltypelabel, method='wilcoxon')
    result = adata1.uns['rank_genes_groups']
    groups = result['names'].dtype.names
    dfgene = pd.DataFrame(
        {group + '_' + key[:1]: result[key][group]
         for group in groups for key in ['names', 'logfoldchanges', 'pvals', 'pvals_adj']})
    df100 = dfgene.iloc[:100, :]
    genelist = []
    for i in range(0, df100.shape[1], 3):
        genelist.extend(df100.iloc[:, i].values)
    dfmk = genelist
    adata1.X = (adata1.X / adata1.X.T.sum(1)) * 100000
    adata1 = adata1[:, list(set(dfmk))]
    logging.info('Camel_Evo...Running: calculating associated genes...')
    GenePCA = np.dot(adata1.X.T, adata1.obsm['Celltype_ScoreAll'])
    s, p = scipy.stats.spearmanr(GenePCA, axis=1)
    dfcorr = pd.DataFrame(s)
    dfcorr.index = adata1.var.index.tolist()
    dfcorr.columns = adata1.var.index.tolist()
    dfcorr = dfcorr.fillna(0)
    dfcorr20 = dfcorr[(corrThre < dfcorr.abs()).astype(int).sum() > int(ThreNumber)]
    logging.info('Camel_Evo...Running: deciding the associated gene patterns...')
    Dvalue = hierarchy.linkage(dfcorr20.values, method="complete",
                               metric="correlation")
    # fig = plt.figure(figsize=(10, 10))
    if plotfig == True:
        sns.set(rc={'axes.facecolor': 'white', 'axes.edgecolor': 'gray', 'figure.facecolor': 'white'})
        ax = hierarchy.dendrogram(Dvalue,
                                  color_threshold=1,
                                  leaf_font_size=0, leaf_rotation=90,
                                  labels=dfcorr20.index.tolist())
    test = scipy.cluster.hierarchy.cut_tree(Dvalue, n_clusters=50, height=None)
    test2 = scipy.cluster.hierarchy.cut_tree(Dvalue, n_clusters=5, height=None)
    logging.info('Camel_Evo...Running: deciding the associated gene patterns...Ready!')
    logging.info('Camel_Evo...Running: filtering and outputting...')
    dfcorr20["GeneCluster"] = test.flatten()
    dfcorr20["GeneClusterNew"] = test2.flatten()
    dfcount = dfcorr20.iloc[:, -10:].groupby(["GeneCluster"]).count()
    keeplist = dfcount[dfcount > 5].dropna().index.tolist()
    dfcorr30 = dfcorr20.loc[dfcorr20["GeneCluster"].isin(keeplist)]
    if TopWeightedFilter == True:
        xcount = 0
        for jname in set(DatasetName):

            print(jname)
            for item in filelist:
                if (item.split("_")[0] == jname) & (item.split("_")[1] == jname):
                    print(item)
                    sctest = anndata.read(item)
                    namelist = []
                    for m in sctest.uns['Celltype_Score_RefCellType']:
                        namelist.append("%s_%s" % (jname, m))
                    dfval = pd.DataFrame(sctest.uns['ConstrualValue_DeepLift_ClusterRef'].T,
                                         index=sctest.uns['train_set_gene'], columns=namelist)
                    clist = []
                    dfvaltemp = (dfval.T / dfval.max(1)).T
                    for item in dfvaltemp.columns:
                        tempindex = dfvaltemp[item].loc[dfvaltemp[item] >= 1].index
                        clist.extend(tempindex)

                    dfval = dfvaltemp.loc[set(clist)].join(
                        dfcorr20.loc[dfcorr20["GeneCluster"].isin(keeplist)]["GeneCluster"], how="inner")
                    # dfval=dfvaltemp.loc[set(clist)].join(dfcorr20["GeneCluster"],how="inner")
                    # dfval=dfval.loc[set(clist)].join(dfcorr20.loc[dfcorr20["GeneCluster"].isin(keeplist)]["GeneCluster"],how="inner")
                    dftemp = dfval.groupby("GeneCluster").mean()
                    # dftemp=(dftemp.T/dftemp.max(1)).T
                    if xcount == 0:
                        dffinal = dftemp
                    else:
                        dffinal = dffinal.join(dftemp, how="outer")
            xcount = xcount + 1
        dfall = dffinal
        df = dfall - 100 / dfall.shape[0]
        df = df.T
        df = (df / df.max()) * 100
        dfpacorr = df.corr()
        dfpacorr = dfpacorr[((corrThre / 2 < dfpacorr.abs()).astype(int).sum() > int(ThreNumber)) & (
                (corrThre < dfpacorr.abs()).astype(int).sum() > int(ThreNumber / 2))]
        dfcorr30 = dfcorr30.loc[dfcorr30["GeneCluster"].isin(dfpacorr.index.tolist())]

    # df=df[dfpacorr.index]

    # df_dev20=df_dev.loc[dfcorr20]
    adataGP = adata[:, dfcorr30.index.tolist()]
    adataGP.var = dfcorr30[["GeneCluster", "GeneClusterNew"]]
    adataGP.var["FilteredGeneList"] = dfcorr30["GeneCluster"].isin(keeplist)
    return adataGP


import os.path


def GRN_TFscore(df_dev, GRNgenes):
    var_names = df_dev.index
    gene_list = GRNgenes

    obs_avg = df_dev.mean(1)
    obs_avg = obs_avg[np.isfinite(obs_avg)]
    n_items = int(np.round(len(obs_avg) / 50))
    obs_cut = obs_avg.rank(method='min') // n_items
    # now pick `ctrl_size` genes from every cut
    ctrl_size = 100
    control_genes = set()
    for cut in np.unique(obs_cut.loc[gene_list]):
        r_genes = np.array(obs_cut[obs_cut == cut].index)
        np.random.shuffle(r_genes)
        control_genes.update(set(r_genes[:ctrl_size]))  # uses full r_genes if ctrl_size > len(r_genes)
    control_genes = list(control_genes - set(gene_list))
    gene_list = list(gene_list)
    X_list = df_dev.loc[gene_list].T.values
    X_control = df_dev.loc[control_genes].mean().values
    TFscore = np.nanmean(X_list, axis=1) - X_control
    return TFscore

def FindTFassociatedGP(adata, tf_filepath=None,
                       N_CPU=2, N_memory=16e9, N_threads=1,
                       filepath=None,
                       TFtoGeneFile=None,
                       TFassociatedGeneFile="TF-Top100Targets.csv",
                       plotfig=True):
    df_dev = pd.DataFrame(adata.X.T, index=adata.var.index, columns=adata.obs.index)
    TFtoGeneFilePath = filepath + TFtoGeneFile
    if os.path.isfile(TFtoGeneFilePath):
        print('CamelEvo...Running: TFtoGene File is ready, reading.....')
        network = pd.read_table(TFtoGeneFilePath, index_col=0, header=0, sep=",")
    else:
        logging.info('CamelEvo...Running: TF associated genes, will take hours.....')
        print('CamelEvo...Running: TF associated genes, will take hours.....')
        local_cluster = LocalCluster(n_workers=N_CPU,
                                     threads_per_worker=N_threads,
                                     memory_limit=N_memory)
        custom_client = Client(local_cluster)
        # load the data
        ex_matrix = pd.DataFrame(adata.X, index=adata.obs.index, columns=adata.var.index)
        tf_names = load_tf_names(tf_filepath)
        # run GRN inference multiple times
        network = grnboost2(expression_data=ex_matrix,
                            tf_names=tf_names,
                            client_or_address=custom_client,  # specify the custom client
                            seed=666)

        network.to_csv(TFtoGeneFilePath, sep=",")
    svalue = max(int(network.shape[0] / 50), 1)
    kn = KneeLocator(range(network.shape[0]), network["importance"], curve='convex', direction='decreasing', S=svalue)
    #  dfsort["Purity"] = [1] * dfsort.shape[0]
    # dfsort["Purity"][:(kn.knee + 1)] = 0
    dfgrn = network.iloc[:kn.knee, :]
    if plotfig == True:
        plt.scatter(range(network.shape[0]), network["importance"], c="silver")
        plt.axvline(kn.knee, c='r', alpha=0.8, linestyle='dashed')
    dfgrn["TF_Cluster"] = [None] * dfgrn.shape[0]
    dfgrn.index = dfgrn["TF"]
    for item in set(dfgrn["TF"]):
        if item in adata.var.index:
            dfgrn.loc[item, "TF_Cluster"] = adata.var.loc[item, "GeneClusterNew"]
    dfgrn["target_Cluster"] = [None] * dfgrn.shape[0]
    dfgrn.index = dfgrn["target"]
    for item in set(dfgrn["target"]):
        if item in adata.var.index:
            dfgrn.loc[item, "target_Cluster"] = adata.var.loc[item, "GeneClusterNew"]
    dfgrnfilt = dfgrn.loc[dfgrn["TF_Cluster"] == dfgrn["target_Cluster"]]
    dfgrnfilt = dfgrnfilt.sort_values(["importance"], ascending=False)
    df_devcorr = df_dev.loc[adata.var.index]
    TFscorelist = []
    GRN_TFlist1 = []
    GRN_TFlist2 = []
    GRNtargetlist = []
    logging.info('CamelEvo...Running: calculating score of TF-associated gene patterns, %s TFs in total.....' % len(
        set(dfgrn["TF"])))
    print('CamelEvo...Running: calculating score of TF-associated gene patterns, %s TFs in total.....' % len(
        set(dfgrn["TF"])))
    for item in set(dfgrn["TF"]):
        templist = dfgrnfilt.loc[dfgrnfilt["TF"] == item, "target"][:100].values.tolist()
        GRNtargetlist.append(templist)
        GRN_TFlist1.append(item)
        if len(templist) <= 5:
            logging.info("Skip for calculation: Due to <5 Targets_%s" % item)
            print("Skip for calculation: Due to <5 Targets_%s" % item)
            continue
        else:
            GRNgenes = templist[:20] + [item]
            GRN_TFlist2.append(item)
            TFscore = [0] * df_dev.shape[1]
            for i in range(5):
                TFscore = TFscore + GRN_TFscore(df_dev=df_devcorr.astype(float), GRNgenes=GRNgenes)
            TFscorelist.append(TFscore / 5)
            logging.info(item)
            print(item)
    dfTFtarget = pd.DataFrame(GRNtargetlist)
    dfTFtarget.index = GRN_TFlist1
    dfregscore = pd.DataFrame(TFscorelist)
    dfregscore.index = GRN_TFlist2
    dfregscore.columns = df_dev.columns
    dfregscore[dfregscore < 0] = 0
    idlist = []
    for item in dfregscore.index:
        idlist.append("%s_+GRN" % item)
    dfregscore.index = idlist
    # dfregscore.to_csv("AllSensoryNeuron_coreTF_GRN.csv",sep="\t")
    TFgenePatternsFilePath = filepath + TFassociatedGeneFile
    dfTFtarget.T.to_csv(TFgenePatternsFilePath, sep="\t")

    adataTF = sc.AnnData(dfregscore.T)
    adataTF = adataTF[adata.obs.index, :]
    adataTF.obs = adata.obs
    return adataTF


def SpeciesTFgenePatterns(adata, fontsizeWeight=0.65, clusterlist=None,
                           filepath="/Yizhou_KI_OneCloud/OneDrive - Karolinska Institutet/Datasets_Template/scCamel_result_files/",
                          savefig="SpeciesTFgenePatterns.png"):
    dfregscore=pd.DataFrame(adata.X)
    dfregscore.index=adata.obs.index
    dfregscore.columns=adata.var.index
    dfregscore=dfregscore.join(adata.obs["Cluster"],how="inner")
    dfscore=dfregscore.groupby(["Cluster"]).mean()
    if clusterlist==None:
        plt.figure(figsize=(int(dfscore.shape[1]/4.5),int(dfscore.shape[0]/4.5)))
        sns.set_style("white")
        sns.set(font_scale= fontsizeWeight)
        sns.clustermap(dfscore,
                       metric="correlation",
                       method="complete",
                       cmap="seismic",
                       row_cluster=True,
                       col_cluster=True,
                       z_score=0,figsize=(int(dfscore.shape[1]/4.5),int(dfscore.shape[0]/4.5)),
                      )
        #fig.set_size_inches(30, 15)
        if savefig!=None:
            savefile=filepath+savefig
            plt.savefig(savefile)
    else:
        dfscore=dfscore.reindex(clusterlist).dropna()
        plt.figure(figsize=(int(dfscore.shape[1]/4.5),int(dfscore.shape[0]/4.5)))
        sns.set_style("white")
        sns.set(font_scale= fontsizeWeight)
        sns.clustermap(dfscore,
                       metric="correlation",
                       method="complete",
                       cmap="seismic",
                       row_cluster=False,
                       col_cluster=True,
                       z_score=0,figsize=(int(dfscore.shape[1]/4.5),int(dfscore.shape[0]/4.5)),
                      )
        #fig.set_size_inches(30, 15)
        if savefig!=None:
            savefile=filepath+savefig
            plt.savefig(savefile)


def MergeObjectValue(DatasetName, filelist,filepath):
    for jname in set(DatasetName):
        xcount=0
        for item in filelist:
            if item.split("_")[0]==jname:
                if xcount==0:
                    tempname="sc%s"%(jname)
                    vars()[tempname] = anndata.read(filepath+item)
                    sctemp=vars()[tempname]
                    #dfdevOri=pd.DataFrame(sctemp.obsm["ConstrualValue_DeepLift"].T*10000,
                    #                             index=sctemp.uns["train_set_gene"], columns=sctemp.obs.index)
                    #dfdevOri=dfdevOri.loc[set(sctemp1.var.index)&set(dfdevOri.index)]
                    #xm=log2(sctemp.obsm['NormalizedMatrix'].T*10000+1)
                    #xm= softmax(xm, axis=1)
                    dfdevOri=pd.DataFrame(sctemp.obsm['NormalizedMatrix'].T,index=sctemp.uns["train_set_gene"], columns=sctemp.obs.index)
                    dfdevOri["GeneCount"]=1
                    dfdevOri=dfdevOri.reindex(sctemp.var.index).fillna(0)
                    scorearray=sctemp.obsm['Celltype_Score']
                else:
                    vars()["sc_%s"%xcount] = anndata.read(filepath+item)
                    sctemp=vars()["sc_%s"%xcount]
                    if type(sctemp.X)==sparse.csr.csr_matrix:
                        sctemp.X=sctemp.X.todense()
                    #xm=log2(sctemp.obsm["ConstrualValue_DeepLift"].T*10000+1)
                    #xm= softmax(xm, axis=1)
                    dfdev=pd.DataFrame(sctemp.obsm['NormalizedMatrix'].T,index=sctemp.uns["train_set_gene"], columns=sctemp.obs.index)
                    dfdev["GeneCount"]=1
                    dfdev=dfdev.reindex(sctemp.var.index).fillna(0)
                    dfdevOri=dfdevOri+dfdev
                    dftest=dfdevOri.T/dfdevOri["GeneCount"]
                    dftest=dftest.T.dropna().T
                    scorearray=np.concatenate((scorearray, vars()["sc_%s"%xcount].obsm['Celltype_Score']),axis=1)
                xcount=xcount+1
        vars()[tempname]= anndata.AnnData(dfdevOri.iloc[:,:-1].T)
        vars()[tempname].obs=sctemp.obs
        vars()[tempname].obsm=sctemp.obsm
        vars()[tempname].uns=sctemp.uns
        vars()[tempname].obsm['PCAraw0']=scorearray
        vars()[tempname].obs["Dataset"]=[jname]*vars()[tempname].shape[0]
    vectorlist=[]
    for jname in set(DatasetName):
        tempname="sc%s"%(jname)
        vectorlist.append(vars()[tempname] )
        #print(tempname)
    adatax=anndata.concat(vectorlist)
    return adatax

def mat_plot(mat):
    # Take a matrix data instead of a dendrogram data, calculate dendrogram and draw a circular dendrogram
    pass


def pandas_plot(df):
    pass


def ConservedCellTypePlot(dataref, dataz, datas, threshold, FigName=None):
    dfc = dataref.obs.groupby(["Cluster", "Assigned_Celltype"]).count()
    dfmean = dfc / dataref.obs.groupby(["Cluster"]).count()
    dfnew = dfmean
    dfz = dfnew.loc[set(dataz.obs["Cluster"])]
    dfz["OriCluster"] = dfz.index.get_level_values(0)
    dfz["AssignedCluster"] = dfz.index.get_level_values(1)
    dfz1 = pd.pivot_table(dfz, values='color', index=['AssignedCluster'], columns='OriCluster').reindex(
        set(dataref.obs["Assigned_Celltype"])).fillna(0)
    dfs = dfnew.loc[set(datas.obs["Cluster"])]
    dfs["OriCluster"] = dfs.index.get_level_values(0)
    dfs["AssignedCluster"] = dfs.index.get_level_values(1)
    dfs1 = pd.pivot_table(dfs, values='color', index=['AssignedCluster'], columns='OriCluster').reindex(
        set(dataref.obs["Assigned_Celltype"])).fillna(0)
    dfn = pd.DataFrame(dfz1.T.values.dot(dfs1.values))
    dfn.index = dfz1.columns
    dfn.columns = dfs1.columns
    dfn = dfn.reset_index()
    data = pd.melt(dfn,
                   id_vars='OriCluster',
                   value_vars=list(dfn.columns[1:]),  # list of days of the week
                   var_name='TargetCluster',
                   value_name='Weight')

    data = data.loc[data['Weight'] > threshold]
    # data
    startlist_lack = set(dfn["OriCluster"].tolist()) - set(data["OriCluster"].tolist())
    # dfn.columns[1:]
    endlist_lack = set(dfn.columns[1:].tolist()) - set(data["TargetCluster"].tolist())
    for item in startlist_lack:
        print(item)
        data.loc[data.index[-1] + 1] = [item, "ZZZemptyR", 0.5]

    # data
    for item in endlist_lack:
        # print(item)
        data.loc[data.index[-1] + 1] = ["ZZZemptyL", item, 0.5]
    # arr= data2.iloc[:, 1:].stack().unique()
    # arr = arr[arr != 'ZZZemptyL']
    # all_labels= arr[arr != 'ZZZemptyR']
    # arr
    # colorsnew = dict(zip(all_labels,newcolors))
    colorsnew = dict(zip(dataref.obs["Cluster"].values, dataref.obs["color"].values))

    colorsnew['ZZZemptyL'] = "#ffffff"
    colorsnew['ZZZemptyR'] = "#ffffff"

    data = data[['Weight', 'OriCluster', 'TargetCluster']]
    datanew = data[data["Weight"] > threshold]

    plt.figure(figsize=(12, 10))
    CAMELsanky(datanew,
               # cmap=newcmp,
               colors=colorsnew,
               # flows_color=(.5, .2, 1),
               titles_color=None, labels_color="k")
    if FigName != None:
        plt.savefig(FigName, bbox_inches='tight')


# Share of total width left empty (same in each phase):
GAPS = .1

# Location of bounds (if a phase is drawn from 0 to 1).
LEFT = .1
RIGHT = .9


def MergeObject(DatasetName, filelist,filepath):
    for jname in set(DatasetName):
        xcount=0
        for item in filelist:
            if item.split("_")[0]==jname:
                if xcount==0:
                    tempname="sc%s"%(jname)
                    vars()[tempname] = anndata.read(filepath+item)
                    scorearray=vars()[tempname].obsm['Celltype_Score']
                else:
                    vars()["sc_%s"%xcount] = anndata.read(filepath+item)
                    scorearray=np.concatenate((scorearray, vars()["sc_%s"%xcount].obsm['Celltype_Score']),axis=1)
                xcount=xcount+1
        vars()[tempname].obsm['PCAraw0']=scorearray
        vars()[tempname].obs["Dataset"]=[jname]*vars()[tempname].shape[0]
    vectorlist=[]
    for jname in set(DatasetName):
        tempname="sc%s"%(jname)
        vectorlist.append(vars()[tempname] )
        #print(tempname)
    adatax=anndata.concat(vectorlist)
    return adatax



def DrawFlow(start, end, width, left, right, color):
    """
    Draw a single flow, from "left" to "right", with y going from "start" to
    "end", width "width" and color "color".
    """
    space = right - left

    verts = np.zeros(shape=(9, 2), dtype='float')
    verts[:, 1] = start
    verts[2:6, 1] = end
    verts[4:, 1] += width

    verts[:, 0] = left
    verts[1:7, 0] += space / 2
    verts[3:5, 0] += space / 2

    codes = [Path.MOVETO,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.LINETO,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.CLOSEPOLY
             ]

    path = Path(verts, codes)

    patch = patches.PathPatch(path, facecolor=color, lw=0, alpha=.4)
    plt.gca().add_patch(patch)


def _node_text(start, size, node_sizes):
    if node_sizes is True:
        node_sizes = '{label} ({size})'
    # Allow for formatting specs:
    elif '{label' not in node_sizes:
        size = node_sizes.format(size)
        node_sizes = '{label} {size}'
    return node_sizes.format(label=start, size=size)


def EvoTreePlot(adatax, ConnFeature="connectivities", color_thresholdValue=5, methodvalue="average",
                metricvalue='correlation',
                fontsize=20, figsize=[10, 10], pallete="gist_rainbow", addlabels=True, figname="202210Treeplot.svg",
                sample_classes=None, colorlabels=None, colorlabels_legend=None):
    dfdist = pd.DataFrame(adatax.obsp[ConnFeature].toarray())
    dfdist.index = adatax.obs.index
    dfdist.columns = adatax.obs.index
    dfdist["Cluster"] = adatax.obs["Cluster"]
    dfdist2 = dfdist.groupby(["Cluster"]).mean().T
    dfdist2["Cluster"] = adatax.obs["Cluster"]
    dfdist2 = dfdist2.groupby(["Cluster"]).mean()
    dfdist3 = dfdist2 + dfdist2.T
    Dvalue = hierarchy.linkage(np.asarray(dfdist3), method=methodvalue,
                               metric=metricvalue)
    Dvalue[:, 2] = (Dvalue[:, 2] - Dvalue[:, 2].min()) / (Dvalue[:, 2].max() - Dvalue[:, 2].min()) + 0.5
    Dvalue[:, 2] = Dvalue[:, 2] + np.array(list(range(0, Dvalue.shape[0] * 10, 10))) / 100
    fig = plt.figure(figsize=(0, 0))
    sns.set(rc={'axes.facecolor': 'white', 'axes.edgecolor': 'gray', 'figure.facecolor': 'white'})
    ax = hierarchy.dendrogram(Dvalue,
                              color_threshold=color_thresholdValue,
                              leaf_font_size=0, leaf_rotation=90,
                              labels=dfdist3.index.tolist())

    fig = plt.figure(figsize=(10, 10))
    # plot a circular dendrogram
    CAMEL_RTplot(Z2=ax, fontsize=20, figsize=[10, 10], pallete="gist_rainbow", addlabels=True, figsavename=figname,
                 sample_classes=sample_classes, colorlabels=colorlabels,
                 colorlabels_legend=colorlabels_legend)

def CAMELsanky(data,  # cmap=plt.get_cmap('jet_r'),
               colors=None,
               flows_color=None,
               labels_color='black', titles_color='black', labels_size=20,
               titles_size=20, node_sizes=False, sort_flows_by_nodes=False):
    """
    Draw a sankey diagram.
    Parameters
    ----------
    data : pandas DataFrame, numpy 2-D array, or list of equal length lists
        The data to be represented. Each row describes a flow from the
        beginning to the end. The first column must be numeric and represents
        the (positive) width of the flow. Each other column describes the label
        of the flow at a given stage.
        At least two stages (start, end) are needed to produce a meaningful
        diagram, hence "data" needs to hold three or more columns.
    cmap : colormap, default: 'jet_r'
        Used to assign a color to each block (and to its outgoing flows, unless
        the "flows_color" argument is used).
    flows_color : color, default: None
        Draw all flows of a same color, rather than of the color of each flow's
        starting block.
    labels_color : color or None, default: 'black'
        Color to be used for labels, None to hide them.
    titles_color : color or None, default: 'black'
        Color to be used for titles, None to hide them.
    labels_size : int, default: 20
        Font size for node labels.
    titles_size : int, default: 20
        Font size for titles.
    node_sizes : Boolean or string, default: False
        Whether to show node sizes close to node labels.
        A format string with named placeholders can be passed to control the
        formatting, as in '{label}\n({size}\%)': if only a non-named
        placeholder is present, as in '- {}', the label is prepended separated
        by a space.
        Passing True is equivalent to passing '{label} ({size})' (or '({})').
    sort_flows_by_nodes : Boolean, default: False
        Whether flows from/to a given node should be sorted based on the
        position of the starting and ending nodes - the default is to sort them
        based on their position in the passed data.
    """

    data = pd.DataFrame(data)

    # One column is for the weights, the remaining n+1 limits define n phases:
    phases = data.shape[1] - 2

    # all_labels = data.iloc[:, 1:].stack().unique()

    # colors = dict(zip(all_labels,
    #                  cmap(np.arange(0, len(all_labels))/len(all_labels))))

    # Actual scale from flow/block width to drawn width:
    factor = (1 - GAPS) / data.iloc[:, 0].sum()

    # The first column always contains weights:
    var_weight = data.columns[0]
    for phase in range(phases):
        # ... while the columns containing variables shift at each phase:
        var_left = data.columns[phase + 1]
        var_right = data.columns[phase + 2]

        # Compute total weight for each label:
        l_sizes = data.groupby(var_left)[var_weight].sum()
        r_sizes = data.groupby(var_right)[var_weight].sum()

        # Drop empty cats (https://github.com/pandas-dev/pandas/issues/8559):
        l_sizes, r_sizes = (s.pipe(lambda x: x[x > 0]) for s in (l_sizes, r_sizes))

        # Map weights to drawn sizes:
        l_shares = l_sizes * factor
        r_shares = r_sizes * factor

        # Distribute gap space among gaps:
        l_gaps = GAPS / max((len(l_shares) - 1), 1)
        r_gaps = GAPS / max((len(r_shares) - 1), 1)

        # Compute blocks positions, including gaps:
        l_starts = (l_shares + l_gaps).cumsum().shift().fillna(0)
        r_starts = (r_shares + r_gaps).cumsum().shift().fillna(0)

        for (pos, l, w, starts, shares) in (
                ('right', phase + RIGHT, 1 - RIGHT, r_starts, r_shares),
                ('left', phase, LEFT, l_starts, l_shares)):
            if pos == 'right' and phase < phases - 1:
                # Center text for full width:
                text_x = l + w
            elif pos == 'left' and phase:
                # Do not draw text - it will be drawn by next phase:
                text_x = -1
            else:
                # Center text for half width (first or last extreme):
                text_x = l + 0.5 * w

            for idx, start in enumerate(starts.index):

                # Draw blocks:
                bottom = starts.loc[start]
                p = patches.Rectangle((l, 1 - bottom - shares.loc[start]),
                                      w, shares.loc[start],
                                      fill=False, clip_on=False)
                # if text not in ["ZZZemptyL","ZZZemptyR"]:
                pc = PatchCollection([p], facecolor=colors[start], alpha=.75)
                # else:
                #   pc = PatchCollection([p], facecolor=colors[start], alpha=0)
                plt.gca().add_collection(pc)

                # Draw labels text:
                if text_x != -1 and labels_color is not None:
                    if node_sizes is not False:
                        if phase == 0 and pos == 'left':
                            size = l_sizes.iloc[idx]
                        else:
                            size = r_sizes.iloc[idx]
                        text = _node_text(start, size, node_sizes)
                    else:
                        text = f"{start}"
                    if text not in ["ZZZemptyL", "ZZZemptyR"]:
                        plt.gca().text(text_x,
                                       1 - bottom - 0.5 * shares.loc[start],
                                       text,
                                       horizontalalignment='center',
                                       verticalalignment='center',
                                       fontsize=labels_size, color=labels_color)

            # Draw titles:
            if text_x != -1 and titles_color is not None:
                plt.gca().text(text_x,
                               1,
                               var_left if pos == 'left' else var_right,
                               horizontalalignment='center',
                               verticalalignment='bottom',
                               fontsize=titles_size, color=titles_color)

        # Draw flows:
        flows_list = data[[var_weight,
                           var_left,
                           var_right]]
        if sort_flows_by_nodes:
            # Avoid (probably unjustified - we're working on entire columns)
            # SettingWithCopyWarning:
            flows_list = flows_list.copy()
            for a_var, starts in (var_left, l_starts), (var_right, r_starts):
                dtype = pd.CategoricalDtype(categories=starts.index,
                                            ordered=True)
                flows_list[a_var] = flows_list[a_var].astype(dtype)
            flows_list = flows_list.sort_values([var_left, var_right])

        for idx, (weight, start, end) in flows_list.iterrows():
            if start not in ["ZZZemptyL", "ZZZemptyR"]:
                if end not in ["ZZZemptyL", "ZZZemptyR"]:
                    width = weight * factor
                    l = l_starts.loc[start]
                    r = r_starts.loc[end]
                    DrawFlow(1 - l_starts.loc[start] - width,
                               1 - r_starts.loc[end] - width, width,
                               phase + LEFT, phase + RIGHT,
                               flows_color or colors[start])
                    l_starts.loc[start] += width
                    r_starts.loc[end] += width

    plt.xlim(0, phases)
    plt.axis('off')