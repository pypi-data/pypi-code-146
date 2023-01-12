#!/usr/bin/env python

import numpy as np
import pandas as pd
import os
import sys, getopt
import os.path
import argparse

dir = os.path.dirname(os.path.abspath(__file__))
version_py = os.path.join(dir, "_version.py")
exec(open(version_py).read())

def annotation(readcounts,depth,typeid,outfile):
    chrfile = pd.read_csv(readcounts,sep="\t",header=0)
    seqfile = pd.read_csv(depth,sep="\t",header=0)
    rows_count = chrfile.shape[0]

    newdf = pd.DataFrame(np.repeat(seqfile.values, rows_count, axis=0))
    newdf.columns = seqfile.columns

    chrfile['size'] = chrfile['end'].astype(int) - chrfile['start'].astype(int) + 1
    id1 = ['chr','start','end']
    ID = id1.copy()
    ID.extend(seqfile.columns.tolist())

    ### TPM= https://www.reneshbedre.com/blog/expression_units.html
    if(typeid == "TPM"):
        TPM = chrfile[seqfile.columns].div(chrfile['size'].values,axis=0)
        TPM = TPM * 1e3
        factor1 = TPM[seqfile.columns].sum()/1e6
        factor1 = pd.DataFrame(factor1).T
        factor2 = pd.DataFrame(np.repeat(factor1.values, rows_count, axis=0))
        factor2.columns = factor1.columns
        TPM = TPM[seqfile.columns]/factor2[seqfile.columns]
        TPM[id1] = chrfile[id1]
        TPM = TPM[ID]
        TPM.to_csv(outfile+'_TPM.csv',sep="\t",header=False,index=False)
    ### CPM=(mapped reads)*1e6/(total mapped reads)
    elif(typeid == "CPM"):
        CPM = chrfile[seqfile.columns]/newdf[seqfile.columns]
        CPM = CPM * 1e6
        CPM[id1] = chrfile[id1]
        CPM = CPM[ID]
        CPM.to_csv(outfile+'_CPM.csv',sep="\t",header=False,index=False)
    ### FPKM=(mapped reads)*1e9/((total mapped reads)*(gene length))
    elif(typeid == "FPKM"):
        FPKM = chrfile[seqfile.columns].div(chrfile['size'].values,axis=0)
        FPKM = FPKM[seqfile.columns]/newdf[seqfile.columns]
        FPKM = FPKM * 1e6 * 1e3
        FPKM[id1] = chrfile[id1]
        FPKM = FPKM[ID]
        FPKM.to_csv(outfile+'_FPKM.csv',sep="\t",header=False,index=False)
    else:
        print("typeid is error")
    gtf_file.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', dest='input',
                        required=True,
                        help='input file')
    parser.add_argument('-d', '--depth', dest='depth',
                        required=True,
                        help='depth file')
    parser.add_argument('-t', '--typeid', dest='typeid',
                        required=True,
                        help='TPM,CPM,FPKM')
    parser.add_argument('-o', '--out', dest='out',
                        default='out.csv',
                        help='out file. [default: out.csv]')
    parser.add_argument("-V", "--version", action="version",version="ExpreLevEpi {}".format(__version__)\
                      ,help="Print version and exit")
    args = parser.parse_args()
    print('###Parameters:')
    print(args)
    print('###Parameters')
    annotation(args.input,args.depth,args.typeid,args.out,args.version)

if __name__ == '__main__':
    main()
