# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 14:28:16 2020

@author: Ani chattaraj
"""

import numpy as np
import os, sys
from time import time
from glob import glob
import re 
import bionetgen 
from .HelperFunctions import * 


class BNG_multiTrials:
    '''
    Provide a bngl file with 'writeXML()' action command, 
    and this class will execute 'numRuns' trials upto 't_end' seconds with different seeds

    '''
    def __init__(self, bng_file, numRuns=10, t_end=0.01, steps=10):
        
        self.infile = bng_file 
        self.numRuns = numRuns
        self.t_end = t_end 
        self.steps = steps 
    
    def __repr__(self):
        info = f"\n***** // ***** \nClass : {self.__class__.__name__}\nFile Path : {self.infile}\n\nt_end : {self.t_end} seconds \t output_steps : {self.steps}\nNumber of runs: {self.numRuns}\n"
        names, numSite, counts, ComplexIC = self.getMolecules()
        info = info + f'\nMolecules: {names}\nNumber of binding sites: {numSite}\nSpecies Counts: {counts}\n'
        if ComplexIC:
            info = info + '\033[1m' + '\n*** WARNING ***\nNumber of species is different than number of molecular types!\nIn case you have multi-molecular species as your initial condition, please provide total counts of each molecular types for subsequent analysis!\n' + '\033[0m'
        return info
    
    def getOutPath(self):
        path = self.infile.replace('.bngl', '') 
        if not os.path.isdir(path):
            os.makedirs(path)
        return path 
    
    def simulate(self, file):
        path = self.getOutPath()
        bionetgen.run(file, out=path, suppress=True)
    
    def createTempFiles(self):
        # replace the action command with simulate_nf and create N number of such files
        path = self.getOutPath()
        bng_files = [path + f'/Run_{r}.bngl' for r in range(1, self.numRuns+1)]
        seeds = [1807253 + r*5397 for r in range(self.numRuns)]
        
        np.savetxt(path + '/seedList.txt', seeds)
            
        with open(self.infile, 'r') as tmf:
            lines = tmf.readlines()
            brak_open, brak_close = '{', '}'
            end_model_idx = 0
            
            for j, line in enumerate(lines):
                if re.search('end model', line, re.IGNORECASE):
                    end_model_idx = j+1 
            lines = lines[:end_model_idx]
            lines.append('\n\n\n')
            
            for i, bfile in enumerate(bng_files):
                with open(bfile, 'w') as tf:
                    lines[-1] = f'simulate_nf({brak_open}t_end=>{self.t_end},n_steps=>{self.steps}, seed=>{seeds[i]}, complex=>0{brak_close})\n'
                    tf.writelines(lines)
        return bng_files 
    
    def getMolecules(self):
        # checkString = lambda strings, line: np.any([re.search(string, line, re.IGNORECASE) for string in strings])
        #molList = ['molecules','molecule types','molecular types']
        #begin_molBlock = ['begin ' + mol for mol in molList]
        #end_molBlock = ['end ' + mol for mol in molList]
        
        names, vals, counts = [], [], [] # Molecular names, valency (number of binding sites) and counts
        IsComplexIC = False # Is there any multi-molecular species at the initial condition ?
        model = bionetgen.bngmodel(self.infile)
        params = model.parameters
        molecules = model.molecule_types 
        species = model.species
        
        names = [str(e.name) for e in molecules.items.values()]
        molStr = [str(e.molecule) for e in molecules.items.values()]
        sites = [re.findall('\(([^\)]+)\)',line) for line in molStr] # grab stuff inside ()
        vals = [len(elem[0].split(',')) for elem in sites]
        
        spNames = [species.items[s].name for s in species.items]
        if len(names) != len(spNames):
            IsComplexIC = True 
        
        counts = [species.items[s].count for s in species.items]
        
        # Whether species counts are provided directly 
        # or in the form of parameters
        GivenDirectCount = all(e.isdigit() for e in counts)
        
        if not GivenDirectCount:
            pDict = {params.items[p].name : params.items[p].value  for p in params.items}
            counts = [float(pDict[p]) for p in counts]
        else:
            counts = [float(c) for c in counts]
            
        return names, vals, counts, IsComplexIC

    @staticmethod
    def removeFiles(files):
        [os.remove(file) for file in files]
    
    def checkExistingResults(self, delSim):
        if not delSim:
            gfiles = glob(self.getOutPath() + '/*.gdat')
            if len(gfiles) > self.numRuns:
                print('\033[1m' + 'Simulations exist! Number of exisiting trials are larger than the current one. Removing existing results ...' + '\033[0m')
                print()
                ssfiles = glob(self.getOutPath() + '/*.species')
                self.removeFiles(gfiles)
                self.removeFiles(ssfiles)
            else:
                pass
        else:
            gfiles = glob(self.getOutPath() + '/*.gdat')
            ssfiles = glob(self.getOutPath() + '/*.species')
            self.removeFiles(gfiles)
            self.removeFiles(ssfiles)
            print('Removed existing simulations!')
            

    @displayExecutionTime
    def runTrials(self, delSim=False):
        bng_files = self.createTempFiles()
        N_file = len(bng_files)
        self.checkExistingResults(delSim)
        
        for i, bf in enumerate(bng_files):
            self.simulate(bf)
            ProgressBar('NFsim progress', (i+1)/N_file)
        
        xml_files = glob(self.getOutPath() + '/*.xml')
        
        self.removeFiles(xml_files)
        self.removeFiles(bng_files)
        
        
      
         

    
    