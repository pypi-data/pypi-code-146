#!/usr/bin/env python

from __future__ import print_function
import os
import copy

class log_general(object):
    def __init__(self,
        outdir='.',
        prefix='',
        subfix='',
        
        n_log_conf=100,
        n_log_magn=100,
        n_log_ener=100,

        log_initial_conf = True,
        log_final_conf = True,
        log_topo_chg = False,
        log_force = False,
        log_ham = True,
        log_conf = True,
        single_ovf = True,
        
        log_conf_file = 'spin_confs.ovf',
        log_ener_file = 'ener.dat',
        log_dist_file = 'dist.dat',
        log_ham_file  = 'Hamiltonian.dat',
        log_Q_file    = 'topo_chg.dat',
        log_file      = None,
        archive_file = 'M.dat',

        tri_simplices = None,
        remove_existing_outdir = False,
        verbosity = 2,
        ):

        self._log_initial_conf = log_initial_conf
        self._log_final_conf   = log_final_conf
        self._log_topo_chg     = log_topo_chg
        self._log_force        = log_force
        self._log_ham          = log_ham
        self._log_conf         = log_conf
        self._single_ovf       = single_ovf

        if outdir=='.' or outdir=='./': outdir = os.getcwd()
        if prefix != '': prefix = '{}_'.format(prefix)
        if subfix != '': subfix = '_{}'.format(subfix)
        self._outdir=outdir
 
        self._prefix = prefix
        self._n_log_configuration = n_log_conf
        self._n_log_magnetization = n_log_magn
        self._n_log_energy        = n_log_ener
        self._tri_simplices = tri_simplices
        init_conf_file  = 'initial_{}'.format(log_conf_file)
        final_conf_file = 'final_{}'.format(log_conf_file)
        self._log_conf_file   = log_conf_file
        self._init_conf_file  = init_conf_file
        self._final_conf_file = final_conf_file
        self._log_ener_file = log_ener_file
        self._log_dist_file = log_dist_file
        self._log_ham_file  = log_ham_file
        self._log_Q_file    = log_Q_file
        self._archive_file = archive_file
        if log_file is not None: self._log_file = '{}/{}{}'.format(outdir,prefix,log_file)
        else: self._log_file = log_file
        self.set_logging_files(self._outdir)
        self.set_outdir(outdir)
        self._remove_existing_outdir = remove_existing_outdir
        self._verbosity = verbosity
        
    #def __deepcopy__(self,memo):
    #    print('__deepcopy__({})'.format(memo))
    #    return log_general(copy.deepcopy(memo))


    def set_verbosity(self,verbosity):
        err = 'log_general: You try to set verbosity = {}, it should be an non-negative integer!'.format(verbosity)
        assert type(verbosity)==int and verbosity>=0, err
        self._verbosity = verbosity


    def add_attr(self,key,value):
        self.__dict__.setdefault(key,value)


    def set_logging_files(self,outdir):
        self._log_conf_file   = '{}/{}{}'.format(outdir,self._prefix,self._log_conf_file)
        self._init_conf_file  = '{}/{}{}'.format(outdir,self._prefix,self._init_conf_file)
        self._final_conf_file = '{}/{}{}'.format(outdir,self._prefix,self._final_conf_file)
        self._log_ener_file = '{}/{}{}'.format(outdir,self._prefix,self._log_ener_file)
        self._log_dist_file = '{}/{}{}'.format(outdir,self._prefix,self._log_dist_file)
        self._log_ham_file  = '{}/{}{}'.format(outdir,self._prefix,self._log_ham_file)
        self._log_Q_file    = '{}/{}{}'.format(outdir,self._prefix,self._log_Q_file)
        self._archive_file = '{}/{}{}'.format(outdir,self._prefix,self._archive_file)


    def verbose_logging_info(self,fw=None):
        print ('\n{0}\nLogging setup: Start\n{0}\n'.format('-'*60),file=fw)
        print ('Log data to the directory\n{}'.format(self._outdir),file=fw)
        if self._log_initial_conf: 
            print ('initial  configuration   dumped to {}'.format(self._init_conf_file.split('/')[-1]),file=fw)
        if self._log_final_conf: 
            print ('final    configuration   dumped to {}'.format(self._final_conf_file.split('/')[-1]),file=fw)
        print ('snapshot configurations  dumped to {}'.format(self._log_conf_file.split('/')[-1]),file=fw)
        print ('energy and magnetization dumped to {}'.format(self._archive_file.split('/')[-1]),file=fw)
        print ('dump snapshot configurations  every {} iterations'.format(self._n_log_configuration),file=fw)
        print ('dump magnetization every {} iterations'.format(self._n_log_magnetization),file=fw)
        print ('dump energy every {} iterations'.format(self._n_log_energy),file=fw)
        print ('\n*** Topological Charge ***',file=fw)
        print ('log_topo_chg = {}'.format(self._log_topo_chg),file=fw)
        if self._tri_simplices is not None: print ('The topological charge will be\ncalculated and logged',file=fw)
        else:  print ('Simplices not provided\nTopological charge won\'t be calculated',file=fw)
        print ('\n{0}\nLogging setup:   End\n{0}\n'.format('-'*60),file=fw)


    def set_outdir(self,outdir):
        self._log_conf_file   = self._log_conf_file.replace(self._outdir,outdir)
        self._init_conf_file  = self._init_conf_file.replace(self._outdir,outdir)
        self._final_conf_file = self._final_conf_file.replace(self._outdir,outdir)
        self._log_ener_file   = self._log_ener_file.replace(self._outdir,outdir) 
        self._log_dist_file   = self._log_dist_file.replace(self._outdir,outdir)
        self._log_ham_file    = self._log_ham_file.replace(self._outdir,outdir)
        self._log_Q_file      = self._log_Q_file.replace(self._outdir,outdir)
        self._archive_file    = self._archive_file.replace(self._outdir,outdir)
        if self._log_file is not None: self._log_file = self._log_file.replace(self._outdir,outdir)
        self._outdir = outdir


    def prepare_logging_dir(self):
        if self._outdir not in ['.','./',os.getcwd()] and self._remove_existing_outdir:
            if os.path.isdir(self._outdir): os.system('rm -r {} 2>/dev/null'.format(self._outdir))
            if not os.path.isdir(self._outdir): os.mkdir(self._outdir)


if __name__=='__main__':
    log_handle = log_general()
    fmt = '{:>25s}  =  {:<20s}'
    for key in log_handle.__dict__.keys():
        value = log_handle.__dict__[key]
        if value is not None: print (fmt.format(key,str(value)))
    log_handle.verbose_logging_info()
