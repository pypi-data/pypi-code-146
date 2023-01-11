# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 17:33:23 2020

@author: Ani Chattaraj
"""

import numpy as np
from numpy import  array, mean
import pandas as pd 
from glob import glob
import sys, os
import re
from collections import defaultdict, OrderedDict, Counter
import csv 
import json
from .HelperFunctions import *



class NFSim_output_analyzer:
    def __init__(self, path):
        '''
        Parameters
        ----------
        path : File String
            DESCRIPTION: location of the source directory containing gdat files

        Returns
        -------
        None.

        '''
        self.path = path
        
    def __repr__(self):
        simfile = self.path.split('/')[-1]
        gfiles = glob(self.path + "/*.gdat")
        info = f"\n***** // ***** \nClass : {self.__class__.__name__}\nSystem : {simfile}\nTotal Trajectories : {len(gfiles)}\n"
        return info

    #@displayExecutionTime
    def process_gdatfiles(self):
        
        #print( "Path is", self.path)
        '''

        Computes Mean observable counts over multiple trajectories

        '''
        gfiles = glob(self.path + "/*.gdat")
        #print( "Indy: Gfiles are", gfiles)
        if len(gfiles) == 0:
            print('No gdat files found; quitting calculation ...')
            sys.exit()

        '''I use a test gdat file to extract the array dimension
            and name of the observables used in the model'''

        
        test_gf = gfiles[0]
        N_tp, N_obs = np.loadtxt(test_gf).shape # number of timepoints and observables

        with open(test_gf,'r') as tmpf:
            obsList = tmpf.readline().split()[1:]
            obs_names = '\t'.join(obsList)


        '''The temporary matrix would store the data from multiple trajectories
            and perform the average'''

        tmp_matrix = np.empty(shape=(len(gfiles),N_tp, N_obs), dtype=float)
        N_gf = len(gfiles)

        for i, gf in enumerate(gfiles):
            data = np.loadtxt(gf)
            tmp_matrix[i] = data
            ProgressBar('Processing gdat_files', (i+1)/N_gf)
        
        obsDict = {i:elem for i,elem in enumerate(obsList)}
        print('\nObservables: ', obsDict)
        print()
        
        mean_obs = np.mean(tmp_matrix, axis=0)
        std_obs = np.std(tmp_matrix, axis=0)
        outpath = self.getOutpath()
        np.savetxt(outpath + "/Mean_Observable_Counts.txt", mean_obs, header=obs_names, fmt='%.6e')
        np.savetxt(outpath + "/Stdev_Observable_Counts.txt", std_obs, header=obs_names, fmt='%.6e')

    #@displayExecutionTime
    def process_speciesfiles(self, molecules=[], counts=[], valency=[]):

        '''

        molecules = List of molecules used in the model
        -------

        Computes distribution of molecular clusters and their compositions

        '''
        sfiles = glob(self.path + "/*.species")
        #flatten_ = lambda myList: [item for sublist in myList for item in sublist]
        cs_stat, comp_stat = defaultdict(list), defaultdict(list)
        comp_tmp_stat = defaultdict(list)
        bf_stat = defaultdict(list)
        bc_dist_stat = defaultdict(list)
        
        MCL_stat = []
        N_sp = len(sfiles)

        for i, sf in enumerate(sfiles):
            cs, comp, comp_tmp, bf_dict, MCL, bc_stat = self.collect_clusters(sf, molecules, valency)
            #print(bc_stat)

            MCL_stat.extend(MCL)
            
            for size, count in cs.items():
                cs_stat[size].append(count)
            
            for size, composition in comp.items():
                comp_stat[size].append(composition)
            
            for size, cmp_tmp in comp_tmp.items():
                comp_tmp_stat[size].append(cmp_tmp)
            
            for size, bf in bf_dict.items():
                bf_stat[size].extend(bf)
            
            for mol, bc in bc_stat.items():
                bc_dist_stat[mol].extend(bc)
            
            ProgressBar('Processing species_files', (i+1)/N_sp)

        cs_stat = {k: sum(v) for k, v in cs_stat.items()}
        comp_stat = {k: self.flatten_(v) for k, v in comp_stat.items()}
        comp_tmp_stat = {k: self.flatten_(v) for k, v in comp_tmp_stat.items()}

        outpath = self.getOutpath()
        #print(comp_tmp_stat)
        #print(bc_dist_stat)

        self.writeComposition(outpath, comp_stat, molecules, cs_stat, counts, N_sp, comp_tmp_stat)
        self.writeDistribution(outpath, cs_stat)
        self.writeBFdata(outpath, bf_stat)
        self.writeMCLdata(outpath, MCL_stat, bc_dist_stat)

    def getOutpath(self):
        outpath = self.path + "/pyStat"
        if not os.path.isdir(outpath):
            os.makedirs(outpath)
        return outpath

    @staticmethod
    def flatten_(myList):
        # merge sublists to a sigle list
        return [item for sublist in myList for item in sublist]
    
    @staticmethod
    def getMolecularBondCount(cluster, molecules):
        bcDict = {}
        getMolecules = lambda molecule, line: re.findall(molecule + '\(([^\)]+)\)', line)
        get_bc = lambda s: s.count('!') # bc: bond count
        for mol in molecules:
            occurences = getMolecules(mol, cluster)
            if len(occurences) == 0:
                # if cluster does not contain this molecule
                pass
            else:
                bcDict[mol] = [get_bc(elem) for elem in occurences]
        
        return bcDict

    def collect_clusters(self, speciesFile, molecules, valency):
        '''
        Parameters
        ----------
        speciesFile : File String
            DESCRIPTION: Speciesfile containing all the molecular species
        molecules : List of String
            DESCRIPTION: List of molecules used in the model

        Returns
        -------
        A pair of defaultdicts; one with cluster size distribution
        and another with the corresponding compositions of the clusters

        '''
        # counts the pattern 'molecule(*)' in a string called 'line'
        getCount = lambda molecule, line: len(re.findall(molecule + '\(([^\)]+)\)', line)) 
        
        try:
            with open(speciesFile, 'r') as tf:
                currentFrame = tf.readlines()[2:] # to avoid first two warning lines
        except:
            print("File missing: ", speciesFile)
            sys.exit()
        else:
            clus_stat_tmp = defaultdict(list)
            comp_stat = defaultdict(list)
            bf_stat = defaultdict(list)
            bc_stat = defaultdict(list)
            MCL_list = []
            
            for line in currentFrame:
                if not (line == '\n' or re.search('Time', line) or re.search('Sink', line) or re.search('Source', line)):
                    cluster, count = line.split()
                    comp = tuple([getCount(mol, cluster) for mol in molecules]) 
                    
                    #comp = tuple([cluster.count(mol) for mol in molecules])
                    cs = cluster.count('.') + 1 # cluster size
                    if cs > 1:
                        bc_dict = self.getMolecularBondCount(cluster, molecules)
                        for mol, bc in bc_dict.items():
                            bc_stat[mol].extend([bc]*int(count))
                        
                        bound_sites = cluster.count('!')
                        tot_mols = array([getCount(mol, cluster) for mol in molecules]) 
                        tot_sites = sum(tot_mols * array(valency))
                        bf = bound_sites/tot_sites 
                        
                        species = cluster.split('.')
                        
                        get_bc = lambda s: s.count('!') # bc: bond count
                        MCL = [get_bc(sp) for sp in species]  # molecular cross-links
                        
                        bf_stat[cs].extend([bf]*int(count))
                        MCL_list.extend([MCL]*int(count))
                        
                    clus_stat_tmp[cs].append(int(count))
                    comp_stat[cs].append(comp)
                    
        clus_stat = {k: sum(v) for k,v in clus_stat_tmp.items()}
        #bf_stat = {k: mean(v) for k,v in bf_stat.items()}
        
        return clus_stat, comp_stat, clus_stat_tmp, bf_stat, MCL_list, bc_stat 
    
    @staticmethod
    def writeBFdata(outpath, bf_stat):
        bf_stat = OrderedDict(sorted(bf_stat.items(), key = lambda x:x[0])) 
        
        bf_dict = {}
        for k,v in bf_stat.items():
            bf_count = Counter(v)
            N = sum(bf_count.values())
            for bf, count in bf_count.items():
                bf_count[bf] = count/N 
            
            bf_dict[k] = bf_count
        
        with open(outpath + '/BoundFraction.json', 'w') as tf:
            tf.write(json.dumps(bf_dict))
    
    
    def writeMCLdata(self, outpath, MCL_list, bc_stat):
        MCL_file = outpath + '/Bonds_per_single_molecule.csv'
        self.writeCountData(MCL_list, MCL_file)
 
        for mol, bcList in bc_stat.items():
            mFile = outpath + f'/{mol}_bonds_per_molecule.csv'
            self.writeCountData(bcList, mFile)
            
    def writeCountData(self, myList, fName):
        countList = self.flatten_(myList)
        counts_norm = {k: (countList.count(k))/len(countList) for k in set(countList)}
        with open(fName, 'w', newline='') as of:
            obj = csv.writer(of)
            obj.writerow(['BondCounts','frequency'])
            obj.writerows(zip(counts_norm.keys(), counts_norm.values()))
    
    @staticmethod
    def writeDistribution(outpath, cluster_stat):
        '''
        Parameters
        ----------
        outpath : File String
            DESCRIPTION: Location of the output files
        cluster_stat : Defaultdict
            DESCRIPTION: Dictionary with {keys, values} = {cluster size, occurence}

        Returns
        -------
        None.
        '''
        cluster_stat = OrderedDict(sorted(cluster_stat.items(), key = lambda x:x[0]))
        TC = sum(cluster_stat.values()) # total counts
        TM = sum([k*v for k,v in cluster_stat.items()])  # total molecules
        #print('TM = ', TM, ' TC = ',  TC)
        foTM = {cs: count*(cs/TM) for cs,count in cluster_stat.items()} # fraction of total molecules
        occurence = {cs: count/TC for cs, count in cluster_stat.items()}

        with open(outpath + "/Cluster_frequency.csv","w", newline='') as tmpfile:
            wf = csv.writer(tmpfile)
            wf.writerow(['Cluster size','counts'])
            wf.writerows(zip(cluster_stat.keys(),cluster_stat.values()))

        with open(outpath+"/SteadyState_distribution.csv", "w", newline='') as tmpfile:
            wf2 = csv.writer(tmpfile)
            wf2.writerow(['Cluster size','frequency','foTM'])
            wf2.writerows(zip(cluster_stat.keys(), occurence.values(), foTM.values()))

    @staticmethod
    def writeComposition(outpath, compo_dict, molecules, cluster_stat, counts=[], Nrun=1, comp_tmp_stat={}):
        '''
        Parameters
        ----------
        outpath : File String
            DESCRIPTION: Location of the output files
        compo_dict : Defaultdict
            DESCRIPTION: Dictionary with {keys, values} = {cluster size, compositions}
        molecules : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        d = OrderedDict(sorted(compo_dict.items(), key = lambda x:x[0])) 

        compList, compFracList = [], []
        with open(outpath + "/Clusters_composition_stat.txt","w") as tmpfile:
            tmpfile.write(f"Cluster Size \t {molecules} : frequency\n\n")

            for k, v in d.items():
                
                # frequency * composition
                compArr = np.dot(array(comp_tmp_stat[k]) , array([list(elem) for elem in v]))
                
                countArr = array(counts) * Nrun
                
                ratioArr = compArr/countArr
                ratioArr = np.insert(ratioArr, 0, k)
                compList.append(ratioArr)
                
                comp_fracArr = compArr / sum(compArr)
                comp_fracArr = np.insert(comp_fracArr, 0, k)
                compFracList.append(comp_fracArr)
                
                unique_comp = set(v)
                freq = [v.count(uc)/len(v) for uc in unique_comp]
                
                tmpfile.write(f"  {k}\t\t")
                for cmp, occur in zip(unique_comp, freq):
                    cmp = [str(s) for s in cmp]
                    tmpfile.write(",".join(cmp))
                    tmpfile.write(" : {:.2f}%\t".format(occur*100))

                tmpfile.write("\n\n")
        
        df = pd.DataFrame(array(compList))
        df2 = pd.DataFrame(array(compFracList))
        
        headerList = molecules.copy()
        headerList.insert(0, 'Clusters')
        
        #df.to_csv(outpath + '/Molecular_distribution.csv', sep=',', header=headerList)
        df2.to_csv(outpath + '/Cluster_composition.csv', sep=',', header=headerList)
        
