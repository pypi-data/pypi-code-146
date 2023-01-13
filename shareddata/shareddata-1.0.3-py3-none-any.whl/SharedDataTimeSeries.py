# THIRD PARTY LIBS
import os,sys
import pandas as pd
import numpy as np
import json
import time
from numba import jit
from pandas.tseries.offsets import BDay
from pathlib import Path
from multiprocessing import shared_memory
from concurrent.futures import ThreadPoolExecutor
import io, gzip, hashlib, shutil
from threading import Thread

from subprocess import run, PIPE
from datetime import datetime, timedelta

from SharedData.Logger import Logger
from SharedData.SharedDataAWSS3 import Legacy_S3SyncDownloadTimeSeries,\
    Legacy_S3Upload,S3Upload,S3Download,UpdateModTime
from SharedData.SharedDataRealTime import SharedDataRealTime

class SharedDataTimeSeries:

    def __init__(self, sharedDataPeriod, tag, value=None):    
        self.sharedDataPeriod = sharedDataPeriod
        self.tag = tag
        
        self.sharedDataFeeder = sharedDataPeriod.sharedDataFeeder
        self.sharedData = sharedDataPeriod.sharedDataFeeder.sharedData        

        self.period = sharedDataPeriod.period
        self.periodSeconds = sharedDataPeriod.periodSeconds               
        self.feeder = self.sharedDataFeeder.feeder

        self.create_map = 'na'
        self.init_time = time.time()
        self.download_time = pd.NaT
        self.last_update = pd.NaT
        self.first_update = pd.NaT
        
        # Time series dataframe
        self.data = pd.DataFrame()
        self.index = pd.Index([])
        self.columns = pd.Index([])

                        
        if value is None: #Read dataset tag
            feeder = self.sharedDataFeeder.feeder            
            dataset = sharedDataPeriod.dataset
            sharedData = sharedDataPeriod.sharedData
        
            if not tag in dataset.index:                
                if (not self.sharedDataFeeder.default_collections is None):
                    self.startDate = sharedDataPeriod.default_startDate
                    self.collections = self.sharedDataFeeder.default_collections
                    self.collections = self.collections.replace('\n','').split(',')
                else:
                    raise ValueError('tag '+tag+' not found in dataset!')
            else:
                self.startDate = dataset['startDate'][tag]
                self.collections = dataset['collections'][tag].split(',')

            _symbols = pd.Index([])
            for collection in self.collections:
                _symbols = _symbols.union(sharedData.getSymbols(collection))
                if len(_symbols)==0:
                    raise Exception('collection '+collection+' has no symbols!')
            _timeidx = sharedDataPeriod.getTimeIndex(self.startDate)
            self.index = _timeidx
            self.columns = _symbols
                
            self.symbolidx = {}
            for i in range(len(self.columns)):
                self.symbolidx[self.columns.values[i]] = i
            self.ctimeidx = sharedDataPeriod.getContinousTimeIndex(self.startDate)

            #allocate memory
            self.isCreate = self.Malloc()
            if self.isCreate:                                        
                self.Read()
        
        else: # map existing dataframe
            self.startDate = value.index[0]
            self.index = value.index
            self.columns = value.columns
                       
            self.symbolidx = {}
            for i in range(len(self.columns)):
                self.symbolidx[self.columns.values[i]] = i

            self.ctimeidx = self.sharedDataPeriod.getContinousTimeIndex(self.startDate)
            #allocate memory
            isCreate = self.Malloc(value=value)

        self.init_time = time.time() - self.init_time

    def getDataPath(self, iswrite=False):
        shm_name = self.sharedData.user + '\\' + self.sharedData.database + '\\' \
            + self.sharedDataFeeder.feeder + '\\' + self.period + '\\' + self.tag
        shm_name = shm_name.replace('\\','/')
        
        if not iswrite:
            if 'LEGACY_READ' in os.environ:
                path = Path(os.environ['LEGACY_DATABASE_FOLDER'])
            else:
                path = Path(os.environ['DATABASE_FOLDER'])
        else:
            if 'LEGACY_WRITE' in os.environ:
                path = Path(os.environ['LEGACY_DATABASE_FOLDER'])
            else:
                path = Path(os.environ['DATABASE_FOLDER'])

        path = path / shm_name
        #path = Path(str(path).replace('\\','/'))        
        if not os.path.isdir(path):
            os.makedirs(path)
        
        return path, shm_name

    def get_loc_symbol(self, symbol):
        if symbol in self.symbolidx.keys():
            return self.symbolidx[symbol]
        else:
            return np.nan

    def get_loc_timestamp(self, ts):
        istartdate = self.startDate.timestamp() #seconds
        if not np.isscalar(ts):
            tidx = self.get_loc_timestamp_Jit(ts, istartdate, \
                self.periodSeconds, self.ctimeidx)            
            return tidx
        else:
            tids = np.int64(ts) #seconds
            tids = np.int64(tids - istartdate)
            tids = np.int64(tids/self.periodSeconds)
            if tids<self.ctimeidx.shape[0]:
                tidx = self.ctimeidx[tids]
                return tidx
            else:
                return np.nan
    
    @staticmethod
    @jit(nopython=True, nogil=True, cache=True)
    def get_loc_timestamp_Jit(ts, istartdate, periodSeconds, ctimeidx):
        tidx = np.empty(ts.shape, dtype=np.float64)
        len_ctimeidx = len(ctimeidx)
        for i in range(len(tidx)):
            tid = np.int64(ts[i])
            tid = np.int64(tid-istartdate)
            tid = np.int64(tid/periodSeconds)
            if tid < len_ctimeidx:
                tidx[i] = ctimeidx[tid]
            else:
                tidx[i] = np.nan
        return tidx

    def getValue(self,ts,symbol):
        sidx = self.get_loc_symbol(symbol)
        tidx = self.get_loc_timestamp(ts)
        if (not np.isnan(sidx)) & (not np.isnan(tidx)):
            return self.data.values[np.int64(tidx),int(sidx)]
        else:
            return np.nan

    def setValue(self,ts,symbol,value):
        sidx = self.get_loc_symbol(symbol)
        tidx = self.get_loc_timestamp(ts)
        if (not np.isnan(sidx)) & (not np.isnan(tidx)):
            self.data.values[np.int64(tidx),int(sidx)] = value

    def setValues(self,ts,symbol,values):
        sidx = self.get_loc_symbol(symbol)
        tidx = self.get_loc_timestamp(ts)
        self.setValuesSymbolJit(self.data.values, tidx, sidx, values)
    
    @staticmethod
    @jit(nopython=True, nogil=True, cache=True)
    def setValuesSymbolJit(values,tidx,sidx,arr):
        if not np.isnan(sidx):
            s = np.int64(sidx)
            i = 0
            for t in tidx:
                if not np.isnan(t):
                    values[np.int64(t),s] = arr[i]
                i=i+1

    @staticmethod
    @jit(nopython=True, nogil=True, cache=True)
    def setValuesJit(values,tidx,sidx,arr):
        i = 0
        for t in tidx:
            if not np.isnan(t):
                j = 0
                for s in sidx:
                    if not np.isnan(s):
                        values[np.int64(t),np.int64(s)] = arr[i,j]
                    j=j+1
            i=i+1

    # C R U D

    # MALLOC LEGACY
    def MallocLegacy(self, value=None):
        tini=time.time()
        
        #Create write ndarray
        path, shm_name = self.getDataPath()
        fpath = path / ('shm_info.json')
        if os.environ['LOG_LEVEL']=='DEBUG':
            Logger.log.debug('Malloc %s ...%.2f%% ' % (shm_name,0.0))

        file_exists = False
        try: # try create memory file
            rows = len(self.index)
            cols = len(self.columns)
            nbytes = int(rows*cols*8)

            self.shm = shared_memory.SharedMemory(\
                name = shm_name,create=True, size=nbytes)

            self.shmarr = np.ndarray((rows,cols),\
                dtype=np.float64, buffer=self.shm.buf)
            
            if not value is None:
                self.shmarr[:] = value.values.copy()
            else:
                self.shmarr[:] = np.nan
            
            self.data = pd.DataFrame(self.shmarr,\
                        index=self.index,\
                        columns=self.columns,\
                        copy=False)
            
            if not value is None:
                value = self.data

            with open(str(fpath), 'w+') as outfile:
                shm_info = {
                    'shm_name':shm_name,
                    'index': self.data.index.values.tolist(),
                    'columns': self.data.columns.values.tolist()                                 
                    }
                json.dump(shm_info, outfile, indent=3)
            
            if os.environ['LOG_LEVEL']=='DEBUG':
                Logger.log.debug('Malloc create %s ...%.2f%% %.2f sec! ' % \
                    (shm_name,100,time.time()-tini))            
            self.create_map = 'create'
            return True
        except:
            pass
        
        if fpath.is_file():
            with open(str(fpath), 'r') as infile:                
                shm_info = json.load(infile)                
                self.index = pd.Index(shm_info['index']).astype('datetime64[ns]')
                self.columns = pd.Index(shm_info['columns'])
                shm_name = shm_info['shm_name']
                rows = len(self.index)
                cols = len(self.columns)

                # map memory file
                self.shm = shared_memory.SharedMemory(\
                    name=shm_name, create=False)
                self.shmarr = np.ndarray((rows,cols),\
                    dtype=np.float64, buffer=self.shm.buf)
                self.data = pd.DataFrame(self.shmarr,\
                            index=self.index,\
                            columns=self.columns,\
                            copy=False)
                
                if not value is None:
                    iidx = value.index.intersection(self.data.index)
                    icol = value.columns.intersection(self.data.columns)
                    self.data.loc[iidx, icol] = value.loc[iidx, icol]

                if os.environ['LOG_LEVEL']=='DEBUG':
                    Logger.log.debug('Malloc map %s/%s/%s ...%.2f%% %.2f sec! ' % \
                        (self.feeder,self.period,self.tag,100,time.time()-tini)) 
                self.create_map = 'map'
        return False
      
    def Malloc(self, value=None):
        tini=time.time()
        
        #Create write ndarray
        path, shm_name = self.getDataPath(iswrite=True)        
        if os.environ['LOG_LEVEL']=='DEBUG':
            Logger.log.debug('Malloc %s ...%.2f%% ' % (shm_name,0.0))

        try: # try create memory file
            r = len(self.index)
            c = len(self.columns)
                        
            idx_b = self.index.astype(np.int64).values.tobytes()
            colscsv_b = str.encode(','.join(self.columns.values),\
                encoding='UTF-8',errors='ignore')
            nb_idx = len(idx_b)
            nb_cols = len(colscsv_b)
            nb_data = int(r*c*8)
            header_b = np.array([r,c,nb_idx,nb_cols,nb_data]).astype(np.int64).tobytes()
            nb_header = len(header_b)
            
            nb_buf = nb_header+nb_idx+nb_cols+nb_data
            nb_offset = nb_header+nb_idx+nb_cols

            self.shm = shared_memory.SharedMemory(\
                name = shm_name,create=True, size=nb_buf)

            i=0
            self.shm.buf[i:nb_header] = header_b
            i = i + nb_header
            self.shm.buf[i:i+nb_idx] = idx_b
            i = i + nb_idx
            self.shm.buf[i:i+nb_cols] = colscsv_b

            self.shmarr = np.ndarray((r,c),\
                dtype=np.float64, buffer=self.shm.buf, offset=nb_offset)
            
            if not value is None:
                self.shmarr[:] = value.values.copy()
            else:
                self.shmarr[:] = np.nan
            
            self.data = pd.DataFrame(self.shmarr,\
                        index=self.index,\
                        columns=self.columns,\
                        copy=False)
            
            if not value is None:
                value = self.data

            if os.environ['LOG_LEVEL']=='DEBUG':
                Logger.log.debug('Malloc create %s ...%.2f%% %.2f sec! ' % \
                    (shm_name,100,time.time()-tini))            
            self.create_map = 'create'
            return True
        except Exception as e:
            pass
                        
        # map memory file
        self.shm = shared_memory.SharedMemory(\
            name=shm_name, create=False)
        
        i=0
        nb_header=40
        header = np.frombuffer(self.shm.buf[i:nb_header],dtype=np.int64)
        i = i + nb_header
        nb_idx = header[2]
        idx_b = bytes(self.shm.buf[i:i+nb_idx])
        self.index = pd.to_datetime(np.frombuffer(idx_b,dtype=np.int64))
        i = i + nb_idx
        nb_cols = header[3]
        cols_b = bytes(self.shm.buf[i:i+nb_cols])
        self.columns = cols_b.decode(encoding='UTF-8',errors='ignore').split(',')

        r = header[0]
        c = header[1]        
        nb_data = header[4]
        nb_offset = nb_header+nb_idx+nb_cols                
        
        self.shmarr = np.ndarray((r,c), dtype=np.float64,\
             buffer=self.shm.buf, offset=nb_offset)

        self.data = pd.DataFrame(self.shmarr,\
                    index=self.index,\
                    columns=self.columns,\
                    copy=False)
        
        if not value is None:
            iidx = value.index.intersection(self.data.index)
            icol = value.columns.intersection(self.data.columns)
            self.data.loc[iidx, icol] = value.loc[iidx, icol]

        if os.environ['LOG_LEVEL']=='DEBUG':
            Logger.log.debug('Malloc map %s/%s/%s ...%.2f%% %.2f sec! ' % \
                (self.feeder,self.period,self.tag,100,time.time()-tini)) 
        self.create_map = 'map'
        return False
    
    # READ
    def Read(self):           
        if 'LEGACY_READ' in os.environ:
            return self.legacy_read_multithread()
        else:
            return self.read_partitions()

    # READ CURRENT
    def read_partitions(self):
        tini = time.time()
        path, shm_name = self.getDataPath()
        headpath = path / (self.tag+'_head.bin')
        tailpath = path / (self.tag+'_tail.bin')   
        head_io = None
        tail_io = None
        if self.sharedData.s3read:
            force_download= (not self.sharedData.save_local)
            
            [head_io_gzip, head_local_mtime, head_remote_mtime] = \
                S3Download(str(headpath),str(headpath)+'.gzip',force_download)
            if not head_io_gzip is None:
                head_io = io.BytesIO()
                head_io_gzip.seek(0)
                with gzip.GzipFile(fileobj=head_io_gzip, mode='rb') as gz:
                    shutil.copyfileobj(gz,head_io)
                if self.sharedData.save_local:                    
                    SharedDataTimeSeries.write_file(head_io,headpath,mtime=head_remote_mtime)
                    UpdateModTime(headpath,head_remote_mtime)
                    
            
            [tail_io_gzip, tail_local_mtime, tail_remote_mtime] = \
                S3Download(str(tailpath),str(tailpath)+'.gzip',force_download)
            if not tail_io_gzip is None:
                tail_io = io.BytesIO()
                tail_io_gzip.seek(0)
                with gzip.GzipFile(fileobj=tail_io_gzip, mode='rb') as gz:
                    shutil.copyfileobj(gz,tail_io)
                if self.sharedData.save_local:                    
                    SharedDataTimeSeries.write_file(tail_io,tailpath,mtime=tail_remote_mtime)
                    UpdateModTime(tailpath,tail_remote_mtime)
        
        if (head_io is None) & (self.sharedData.save_local):
            # read local
            if os.path.isfile(str(headpath)):
                head_io = open(str(headpath),'rb')
            
        if (tail_io is None) & (self.sharedData.save_local):
            if os.path.isfile(str(tailpath)):
                tail_io = open(str(tailpath),'rb')
        
        if not head_io is None:
            head_io.seek(0)
            self.read_data(head_io,headpath)
            head_io.close()

        if not tail_io is None:
            tail_io.seek(0)
            self.read_data(tail_io,tailpath)
            tail_io.close()

    def read_data(self,data_io,path):
        _header = np.frombuffer(data_io.read(40),dtype=np.int64)
        _idx_b = data_io.read(int(_header[2]))
        _idx = pd.to_datetime(np.frombuffer(_idx_b,dtype=np.int64))
        _colscsv_b = data_io.read(int(_header[3]))
        _colscsv = _colscsv_b.decode(encoding='UTF-8',errors='ignore')
        _cols = _colscsv.split(',')
        _data = np.frombuffer(data_io.read(int(_header[4])),dtype=np.float64).reshape((_header[0],_header[1]))        
        #calculate hash
        _m = hashlib.md5(_idx_b)
        _m.update(_colscsv_b)
        _m.update(_data)
        _md5hash_b = _m.digest()
        __md5hash_b = data_io.read(16)
        if not _md5hash_b==__md5hash_b:
            raise Exception('Timeseries file corrupted!\n%s' % (path))
        sidx = np.array([self.get_loc_symbol(s) for s in _cols])
        ts = _idx.values.astype(np.int64)/10**9 #seconds
        tidx = self.get_loc_timestamp(ts)
        self.setValuesJit(self.data.values,tidx,sidx,_data)
        data_io.close()

    # READ LEGACY
    def legacy_read_multithread(self):
        path, shm_name = self.getDataPath() 
        if self.sharedData.s3read:            
            self.download_time = time.time()
            Legacy_S3SyncDownloadTimeSeries(str(path), shm_name)
            self.download_time = time.time()-self.download_time
       
        years = [int(x.stem) for x in path.glob('*.npy') if x.is_file()]
        fpaths = [x for x in path.glob('*.npy') if x.is_file()]
        if len(fpaths)>0:
            mtime = [datetime.fromtimestamp(os.stat(f).st_mtime) for f in fpaths]
            if len(mtime)>0:
                self.last_update = max(mtime)
                self.first_update = min(mtime)
            else:
                self.last_update = pd.NaT
                self.first_update = pd.NaT
                
            files = pd.DataFrame([years,fpaths]).T
            files.columns = ['year','fpath']
            files = files.sort_values(by='year')
            nfiles = len(files.index)
            if nfiles>0:
                tini=time.time()
                if os.environ['LOG_LEVEL']=='DEBUG':
                    Logger.log.debug('Reading %s ...%.2f%% ' % (shm_name,0.0))   
                n=0
                file_paths = files['fpath']
                if file_paths.shape[0]>0:
                    # create a thread pool
                    with ThreadPoolExecutor(file_paths.shape[0]) as exe:
                        futures = [exe.submit(self.legacy_read_thread, fpath) \
                            for fpath in file_paths]
                        # collect data
                        data = [future.result() for future in futures]                
                if os.environ['LOG_LEVEL']=='DEBUG':
                    Logger.log.debug('Reading %s ...%.2f%% %.2f sec! ' % \
                        (shm_name,100*(n/nfiles),time.time()-tini))        
        
    def legacy_read_thread(self,fpath):
        arr = np.load(str(fpath),mmap_mode='r')
        r ,c = arr.shape
        if (r>0):                   
            idxfpath = str(fpath).replace('.npy','.csv')
            with open(idxfpath,'r') as f:
                dfidx = f.read()
            dfidx = dfidx.split(',')
            sidx = [self.get_loc_symbol(s) for s in dfidx[1:]]
            sidx = np.array(sidx)                    
            ts = (arr[:,0]).astype(np.int64) #seconds
            tidx = self.get_loc_timestamp(ts)

            self.setValuesJit(self.data.values,tidx,sidx,arr[:,1:])
            return True
        return False
                    
    # WRITE
    def Write(self, busdays=None, startDate=None):

        firstdate = self.data.first_valid_index()
        if (startDate is None) & (busdays is None):
            firstdate = self.startDate
        elif not busdays is None:
            firstdate =  self.data.last_valid_index() - BDay(busdays)
        elif not startDate is None:
            firstdate = startDate
        
        if 'LEGACY_WRITE' in os.environ:
            self.legacy_write_multithread(firstdate)
        else:
            self.write_partitions(firstdate)
            
    # WRITE CURRENT
    def write_partitions(self,firstdate):
        tini = time.time()
        path, shm_name = self.getDataPath(iswrite=True)
        
        partdate = pd.Timestamp(datetime(datetime.now().year,1,1))
        threads = []

        mtime = datetime.now().timestamp()
        if firstdate<partdate:
            # write head
            threads = [*threads , \
                Thread(target=SharedDataTimeSeries.write_timeseries_df,\
                    args=(self,self.data.loc[:partdate], str(path / (self.tag+'_head.bin')), mtime) )]            
        # write tail
        threads = [*threads , \
                Thread(target=SharedDataTimeSeries.write_timeseries_df,\
                    args=(self,self.data.loc[partdate:], str(path / (self.tag+'_tail.bin')), mtime) )]

        for i in range(len(threads)):
            threads[i].start()

        for i in range(len(threads)):
            threads[i].join()
        
    def write_timeseries_df(self,df,tag_path,mtime):
        ts_io = SharedDataTimeSeries.create_timeseries_io(df)        
        threads=[]
        if self.sharedData.s3write:
            ts_io.seek(0)
            gzip_io = io.BytesIO()
            with gzip.GzipFile(fileobj=gzip_io, mode='wb', compresslevel=1) as gz:
                shutil.copyfileobj(ts_io, gz)

            threads = [*threads , \
                Thread(target=S3Upload,args=(gzip_io, tag_path+'.gzip', mtime) )]

        if self.sharedData.save_local:
            threads = [*threads , \
                Thread(target=SharedDataTimeSeries.write_file, args=(ts_io, tag_path, mtime) )]
                            
        for i in range(len(threads)):
            threads[i].start()

        for i in range(len(threads)):
            threads[i].join()

    def create_timeseries_io(df):
        df = df.dropna(how='all',axis=0).dropna(how='all',axis=1)
        r, c = df.shape
        idx = (df.index.astype(np.int64))
        idx_b = idx.values.tobytes()
        cols = df.columns.values
        colscsv = ','.join(cols)
        colscsv_b = str.encode(colscsv,encoding='UTF-8',errors='ignore')
        nbidx = len(idx_b)
        nbcols = len(colscsv_b)
        data = np.ascontiguousarray(df.values.astype(np.float64))
        header = np.array([r,c,nbidx,nbcols,r*c*8]).astype(np.int64)
        #calculate hash
        m = hashlib.md5(idx_b)
        m.update(colscsv_b)
        m.update(data)
        md5hash_b = m.digest()
        # allocate memory
        io_obj = io.BytesIO()        
        io_obj.write(header)
        io_obj.write(idx_b)
        io_obj.write(colscsv_b)
        io_obj.write(data)
        io_obj.write(md5hash_b)        
        return io_obj

    def write_file(io_obj,path,mtime):
        with open(path, 'wb') as f:
            f.write(io_obj.getbuffer())
            f.flush()
        os.utime(path, (mtime, mtime))

    # WRITE LEGACY
    def legacy_write_multithread(self, firstdate):
        tini = time.time()
        if os.environ['LOG_LEVEL']=='DEBUG':
            startdatestr = firstdate.strftime('%Y-%m-%d')
            Logger.log.debug('Writing %s from %s ...%.2f%% ' % \
                (shm_name,startdatestr,0.0))
        path, shm_name = self.getDataPath(iswrite=True)
        if not os.path.isdir(path):
            os.makedirs(path)                
        years = self.data.loc[firstdate:,:].index.year.unique()
        if years.shape[0]>0:
            # create a thread pool
            with ThreadPoolExecutor(years.shape[0]) as exe:
                futures = [exe.submit(self.legacy_write_thread, year, path) \
                    for year in years]
                # collect data
                data = [future.result() for future in futures]

            if os.environ['LOG_LEVEL']=='DEBUG':
                Logger.log.debug('Writing %s from %s ...%.2f%% %.2f sec!' % \
                    (shm_name,startdatestr,100,time.time()-tini))        
        
    def legacy_write_thread(self,y, path):
        idx = self.data.index[self.data.index.year==y]
        dfyear = self.data.loc[idx,:].copy()
        dfyear = dfyear.dropna(how='all').dropna(axis=1,how='all')
        if dfyear.shape[0]>0:
            dfyear.index = (dfyear.index.astype(np.int64)/10**9).astype(np.int64)
            dfyear = dfyear.reset_index()

            fpath_npy = path / (str(y)+'.npy')
            with open(fpath_npy, 'wb') as f:
                np.save(f,dfyear.values.astype(np.float64))
                f.flush()
            
            cols = ','.join(dfyear.columns)            
            fpath_csv = path / (str(y)+'.csv')    
            with open(fpath_csv, 'w') as f:
                f.write(cols)
                f.flush()

            if self.sharedData.s3write:                
                Legacy_S3Upload(fpath_npy)
                Legacy_S3Upload(fpath_csv)
            
    # MESSAGES
    def Broadcast(self,idx,col):
        SharedDataRealTime.Broadcast(
            self.sharedData,
            self.feeder,
            self.period,
            self.tag,
            idx,col)