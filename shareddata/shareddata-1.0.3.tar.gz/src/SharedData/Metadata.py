import os
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd
import numpy as np
import time
import subprocess
from datetime import datetime, timedelta
import gzip,io,shutil

from SharedData.Logger import Logger
from SharedData.SharedDataAWSS3 import Legacy_S3SyncDownloadMetadata,\
    Legacy_S3Upload,S3Upload,S3ListFolder,S3Download,UpdateModTime

class Metadata():
    
    def __init__(self, name, mode='rw', user='master',\
        sync_frequency_days=None, debug=None):
        
        if Logger.log is None:
            Logger('Metadata')
        
        self.user = user
        
        self.s3read = False
        self.s3write = False
        if mode == 'r':
            self.s3read = True
            self.s3write = False
        elif mode == 'w':
            self.s3read = False
            self.s3write = True
        elif mode == 'rw':
            self.s3read = True
            self.s3write = True        

        self.save_local = True
        if os.environ['SAVE_LOCAL']!='True':
            self.save_local = False

        self.name = name
        self.xls = {}
        self.static = pd.DataFrame([])                

        if 'LEGACY_READ' in os.environ:
            self.legacy_load()
        else:
            self.load()

    def load(self):
        self.fpath = Path(os.environ['DATABASE_FOLDER']) / self.user
        self.pathxls = self.fpath /  ('Metadata/'+self.name+'.xlsx')
        self.path = self.fpath /  ('Metadata/'+self.name+'.pkl')
        
        if not self.path.parent.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
        
        readpkl=True
        readxlsx=False
        if self.save_local:
            # prefer read pkl
            # but read excel if newer        
            readpkl = self.path.is_file()
            readxlsx = self.pathxls.is_file()
            if (readpkl) & (readxlsx):
                readxlsx = os.path.getmtime(self.pathxls)>os.path.getmtime(self.path)
                readpkl = not readxlsx
                        
        if (not readxlsx) | (not self.save_local):
            pkl_io = None            
            if (self.s3read): 
                force_download = (not self.save_local)
                [pkl_io, local_mtime, remote_mtime] = \
                    S3Download(str(self.path),str(self.path)+'.gzip',force_download)
                if (not pkl_io is None):
                    pkl_io.seek(0)                    
                    self.static = pd.read_pickle(pkl_io,compression='gzip')
                    self.static = self.static.sort_index()
                    if (self.save_local):
                        self.static.to_pickle(self.path)
                        UpdateModTime(self.path,remote_mtime)
                        
            if (pkl_io is None) & (self.path.is_file()):            
                self.static = pd.read_pickle(self.path)
                self.static = self.static.sort_index()

        elif readxlsx:
            tini = time.time()
            
            self.xls = pd.read_excel(self.pathxls,sheet_name=None)
            if 'static' in self.xls:
                self.static = self.xls['static']

            if not self.static.empty:
                self.static = self.static.set_index(self.static.columns[0])

            if os.environ['LOG_LEVEL']=='DEBUG':
                Logger.log.debug('Loading metadata xlsx %s %.2f done!' % (self.name,time.time()-tini))
        
        if os.environ['LOG_LEVEL']=='DEBUG':
            Logger.log.debug('Initializing Metadata %s,%s DONE!' % (self.name,self.mode))

    def legacy_load(self):
        self.fpath = Path(os.environ['LEGACY_DATABASE_FOLDER']) / self.user
        self.pathxls = self.fpath /  ('Metadata/'+self.name+'.xlsx')
        self.pathpkl = self.fpath /  ('Metadata/'+self.name+'.pkl')

        if (self.s3read):            
            Legacy_S3SyncDownloadMetadata(self.pathpkl,self.name)
                    
        # prefer read pkl
        # but read excel if newer
        readpkl = self.pathpkl.is_file()
        readxlsx = self.pathxls.is_file()
        if (readpkl) & (readxlsx):
            readxlsx = os.path.getmtime(self.pathxls)>os.path.getmtime(self.pathpkl)
            readpkl = not readxlsx
        
        if readpkl:
            tini = time.time()

            self.static = pd.read_pickle(self.pathpkl)
            self.static = self.static.sort_index()

            if os.environ['LOG_LEVEL']=='DEBUG':
                Logger.log.debug('Loading metadata pkl %s %.2f done!' % (self.name,time.time()-tini))

        elif readxlsx:
            tini = time.time()
            
            self.xls = pd.read_excel(self.pathxls,sheet_name=None)
            if 'static' in self.xls:
                self.static = self.xls['static']

            if not self.static.empty:
                self.static = self.static.set_index(self.static.columns[0])

            if os.environ['LOG_LEVEL']=='DEBUG':
                Logger.log.debug('Loading metadata xlsx %s %.2f done!' % (self.name,time.time()-tini))
        
        if os.environ['LOG_LEVEL']=='DEBUG':
            Logger.log.debug('Initializing Metadata %s,%s DONE!' % (self.name,self.mode))

    def save(self,save_excel=False):
        if 'LEGACY_WRITE' in os.environ:
            self.legacy_save(save_excel)
        else:
            self.save_metadata(save_excel)

    def save_metadata(self,save_excel=False):
        fpath = Path(os.environ['DATABASE_FOLDER']) / self.user
        self.pathxls = fpath /  ('Metadata/'+self.name+'.xlsx')
        self.path = fpath /  ('Metadata/'+self.name+'.pkl')

        tini = time.time()
        mtime = datetime.now().timestamp()
        if not os.path.isdir(self.path.parents[0]):
            os.makedirs(self.path.parents[0])
        # save excel first so that last modified
        # timestamp is older
        if save_excel:
            with open(self.pathxls, 'wb') as f:
                writer = pd.ExcelWriter(f, engine='xlsxwriter')            
                self.static.to_excel(writer,sheet_name='static')
                writer.close()
                f.flush()
            os.utime(self.pathxls, (mtime, mtime))
        
        
        pkl_io = None
        if self.save_local:            
            pkl_io = io.BytesIO()
            pkl_io.close = lambda: None
            self.static.to_pickle(pkl_io)
            pkl_io.seek(0)
            with open(self.path, 'wb') as f:
                f.write(pkl_io.getbuffer())
                f.flush()
                f.close()
            os.utime(self.path, (mtime, mtime))

        if self.s3write:
            if pkl_io is None:
                pkl_io = io.BytesIO()
                pkl_io.close = lambda: None
                self.static.to_pickle(pkl_io)
            pkl_io.seek(0)
            gzip_io = io.BytesIO()
            with gzip.GzipFile(fileobj=gzip_io, mode='wb', compresslevel=1) as gz:
                shutil.copyfileobj(pkl_io, gz)                        
            S3Upload(gzip_io, str(self.path)+'.gzip', mtime)

        if not pkl_io is None:
            io.BytesIO.close(gzip_io)

        if os.environ['LOG_LEVEL']=='DEBUG':
            Logger.log.debug('Saving metadata ' + self.name + ' %.2f done!' % (time.time()-tini))

    def legacy_save(self,save_excel=False):
        tini = time.time()
        if os.environ['LOG_LEVEL']=='DEBUG':
            Logger.log.debug('Saving metadata ' + self.name + ' ...')  
        if not os.path.isdir(self.pathpkl.parents[0]):
            os.makedirs(self.pathpkl.parents[0])                   

        # save excel first so that last modified
        # timestamp is older        
        if save_excel:
            with open(self.pathxls, 'wb') as f:
                writer = pd.ExcelWriter(f, engine='xlsxwriter')            
                self.static.to_excel(writer,sheet_name='static')
                writer.save()                
                f.flush()

        with open(self.pathpkl, 'wb') as f:
            self.static.to_pickle(f)
            f.flush()

        if self.s3write:
            Legacy_S3Upload(self.pathpkl)

        if os.environ['LOG_LEVEL']=='DEBUG':
            Logger.log.debug('Saving metadata ' + self.name + ' %.2f done!' % (time.time()-tini))
    
    def mergeUpdate(self,newdf):
        newidx = ~newdf.index.isin(self.static.index)
        if newidx.any():
            self.static = self.static.reindex(index=self.static.index.union(newdf.index))

        newcolsidx = ~newdf.columns.isin(self.static.columns)
        if newcolsidx.any():
            newcols = newdf.columns[newcolsidx]            
            self.static = pd.concat([self.static,newdf[newcols]],axis=1)
            
        self.static.update(newdf)

    @staticmethod
    def list(keyword, user='master'):
        mdprefix = user+'/Metadata/'
        keys = S3ListFolder(mdprefix+keyword)
        keys = keys[['.pkl' in k for k in keys]]
        keys = [k.replace(mdprefix,'').split('.')[0] for k in keys]
        return keys

    def __setitem__(self, tag, value):
        self.static[tag] = value
                
    def __getitem__(self, tag):
        return self.static[tag]