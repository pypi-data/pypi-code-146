import os
import pandas as pd
import numpy as np
import anndata as ann

from main import *
from diff_utils import *
import plottings as pl
# adata = dataset.melanoma()
# weight_matrix(adata, l=1.2, cutoff=0.2, single_cell=False) # weight_matrix by rbf kernel
# extract_lr(adata, 'human', min_cell=3)
# spatialdm_global(adata,1000, select_num=None, method='both', nproc=1)     # global Moran selection
# sig_pairs(adata, method='permutation', fdr=True, threshold=0.1)
# spatialdm_local(adata, n_perm=1000, method='both', select_num=None, nproc=1)     # local spot selection
# sig_spots(adata, method='permutation', fdr=False, threshold=0.1)     # significant local spots

from datasets import dataset

adata = dataset.melanoma()
weight_matrix(adata, l=1.2, cutoff=0.2, single_cell=False)  # weight_matrix by rbf kernel
extract_lr(adata, 'human', min_cell=3)
spatialdm_global(adata,1000, specified_ind=None, method='both', nproc=1)     # global Moran selection
sig_pairs(adata, method='permutation', fdr=True, threshold=0.1)
spatialdm_local(adata, n_perm=1000, method='both', specified_ind=None, nproc=1)     # local spot selection
sig_spots(adata, method='permutation', fdr=False, threshold=0.1)     # significant local spots
write_spatialdm_h5ad(adata, filename='test.h5ad')
bdata = read_spatialdm_h5ad(filename='test.h5ad')
bdata