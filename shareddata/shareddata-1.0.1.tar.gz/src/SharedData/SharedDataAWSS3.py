import os,sys
import logging
import subprocess
import boto3
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime,timedelta
import time
import pytz
import io

from SharedData.Logger import Logger
from SharedData.MultiProc import io_bound_process

def S3GetSession(isupload=False):
    if not isupload: # DOWNLOAD
        if not 'LEGACY_READ' in os.environ:
            _session = boto3.Session(profile_name=os.environ['S3_AWS_PROFILE'])
            if 'S3_ENDPOINT_URL' in os.environ:                
                _s3 = _session.resource('s3',endpoint_url=os.environ['S3_ENDPOINT_URL'])
            else:
                _s3 = _session.resource('s3')
            _bucket = _s3.Bucket(os.environ['S3_BUCKET'].replace('s3://',''))
        else:
            _session = boto3.Session(profile_name=os.environ['LEGACY_S3_AWS_PROFILE'])
            if 'LEGACY_S3_ENDPOINT_URL' in os.environ:
                _s3 = _session.resource('s3',endpoint_url=os.environ['LEGACY_S3_ENDPOINT_URL'])
            else:
                _s3 = _session.resource('s3')
            _bucket = _s3.Bucket(os.environ['LEGACY_S3_BUCKET'].replace('s3://',''))
        
    else: # UPLOAD
        if not 'LEGACY_WRITE' in os.environ:
            _session = boto3.Session(profile_name=os.environ['S3_AWS_PROFILE'])
            if 'S3_ENDPOINT_URL' in os.environ:
                _s3 = _session.resource('s3',endpoint_url=os.environ['S3_ENDPOINT_URL'])
            else:
                _s3 = _session.resource('s3')
            _bucket = _s3.Bucket(os.environ['S3_BUCKET'].replace('s3://',''))
        else:
            _session = boto3.Session(profile_name=os.environ['LEGACY_S3_AWS_PROFILE'])
            if 'LEGACY_S3_ENDPOINT_URL' in os.environ:
                _s3 = _session.resource('s3',endpoint_url=os.environ['LEGACY_S3_ENDPOINT_URL'])
            else:
                _s3 = _session.resource('s3')
            _bucket = _s3.Bucket(os.environ['LEGACY_S3_BUCKET'].replace('s3://',''))

    return _s3,_bucket

# LEGACY METHODS
def LegacyS3SyncDownloadDataFrame(path,shm_name):
   
    npypath = (os.environ['LEGACY_DATABASE_FOLDER']+'\\'+str(shm_name)).replace('/','\\')+'.npy'
    success = LegacyS3Download(npypath)
    jsonpath = npypath.replace('.npy','.json')
    success = (success) & (LegacyS3Download(jsonpath))

    if success:
        if os.environ['LOG_LEVEL']=='DEBUG':
            Logger.log.debug('AWS S3 Sync DataFrame %s,%s DONE!' % (Logger.user,shm_name))
    else:
        Logger.log.error('AWS S3 Sync DataFrame %s,%s ERROR!' % (Logger.user,shm_name))
    return success

def Legacy_S3SyncDownloadTimeSeries(path,shm_name):
    tini = time.time()
    s3,bucket = S3GetSession()
    success=True
    dbfolder = os.environ['LEGACY_DATABASE_FOLDER']
    
    files = np.array([dbfolder+'\\'+obj_s.key.replace('/','\\')\
        for obj_s in bucket.objects.filter(Prefix=shm_name+'/')])
    idx = ['shm_info.json' not in f for f in files]
    files = files[idx]
    if len(files)>0:
        result = io_bound_process(LegacyS3DownloadThread,files,[s3])

    if success:
        if os.environ['LOG_LEVEL']=='DEBUG':
            Logger.log.debug('AWS S3 Sync timeseries %s,%s DONE!' % (Logger.user,shm_name))
    else:
        Logger.log.error('AWS S3 Sync timeseries %s,%s ERROR!' % (Logger.user,shm_name))
    return success

def Legacy_S3SyncDownloadMetadata(pathpkl,name):    
    
    success = LegacyS3Download(str(pathpkl))
    
    if success:
        if os.environ['LOG_LEVEL']=='DEBUG':
            Logger.log.debug('AWS S3 Sync download metadata %s,%s DONE!' % (Logger.user,name))
    else:
        Logger.log.error('AWS S3 Sync download metadata %s,%s ERROR!' % (Logger.user,name))        
    return success

def LegacyS3Download(local_path,s3=None):
    bucket_name = os.environ['LEGACY_S3_BUCKET'].replace('s3://','')
    s3_path = str(local_path).replace(os.environ['LEGACY_DATABASE_FOLDER'],'').replace('\\','/')[1:]
    if s3 is None:
        s3,bucket = S3GetSession()
    # load obj
    obj = s3.Object(bucket_name, s3_path)
    isnewer = False
    ischg = False
    try:
        # remote mtime size
        remote_mtime = obj.last_modified.timestamp()
        if 'mtime' in obj.metadata:
            remote_mtime = float(obj.metadata['mtime'])
        #remote_size = obj.content_length
    except:
        # remote file dont exist 
        return True
    
    if os.path.isfile(str(local_path)):
        # local mtime size
        local_mtime = datetime.utcfromtimestamp(os.path.getmtime(local_path)).timestamp()
        #local_size = os.path.getsize(local_path)
        #compare
        isnewer = remote_mtime>local_mtime
        #ischg = remote_size!=local_size
    else:
        # local file dont exist 
        isnewer = True
        #ischg = True

    if isnewer:
        try:
            path = Path(local_path)
            if not path.parent.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
            obj.download_file(local_path)
            # update modification time
            remote_mtime_dt = datetime.fromtimestamp(remote_mtime)
            offset =  remote_mtime_dt - datetime.utcfromtimestamp(remote_mtime)        
            remote_mtime_local_tz = remote_mtime_dt+offset
            remote_mtime_local_tz_ts = remote_mtime_local_tz.timestamp()
            os.utime(local_path, (remote_mtime_local_tz_ts, remote_mtime_local_tz_ts))
            if os.environ['LOG_LEVEL']=='DEBUG':
                Logger.log.debug('downloading %s,%s DONE!' % (Logger.user,local_path))
        except Exception as e:
            Logger.log.error('downloading %s,%s ERROR!\n%s' % (Logger.user,local_path,str(e)))
            raise Exception('downloading %s,%s ERROR!\n%s' % (Logger.user,local_path,str(e)))
    return True
    
def LegacyS3DownloadThread(iteration, args):
    return [LegacyS3Download(iteration,s3=args[0])]

def Legacy_S3Upload(localfilepath):
    remotefilepath = str(localfilepath).replace(\
            os.environ['DATABASE_FOLDER'],os.environ['S3_BUCKET'])
    remotefilepath = remotefilepath.replace('\\','/')        
    localfilepath = str(localfilepath).replace('\\','/')
      
    trials = 3
    success=False
    while trials>0:        
        try:                
            s3,bucket = S3GetSession(isupload=True)
            mtime = os.path.getmtime(localfilepath)
            mtime_utc = datetime.utcfromtimestamp(mtime).timestamp()
            mtime_str = str(mtime_utc)
            bucket.upload_file(localfilepath,remotefilepath.replace(os.environ['S3_BUCKET'],'')[1:],\
                ExtraArgs={'Metadata': {'mtime': mtime_str}})
            if os.environ['LOG_LEVEL']=='DEBUG':
                Logger.log.debug(Logger.user+' Uploading to S3 '+str(localfilepath)+' DONE!')
            success = True
            break
        except Exception as e:
            Logger.log.warning(Logger.user+' Uploading to S3 '+localfilepath+' FAILED! retrying(%i,3)...\n%s ' % (trials,str(e)))
            trials = trials - 1

    if not success:
        Logger.log.error(Logger.user+' Uploading to S3 '+localfilepath+' ERROR! \n%s ' % str(e))

# CURRENT METHODS
def S3ListFolder(prefix):
    s3,bucket = S3GetSession()
    keys = np.array([obj_s.key for obj_s in bucket.objects.filter(Prefix=prefix)])
    return keys

def S3Download(local_path, remote_path, force_download=False):
    bucket_name = os.environ['S3_BUCKET'].replace('s3://','')
    s3_path = str(remote_path).replace(os.environ['DATABASE_FOLDER'],'').replace('\\','/')[1:]
    s3,bucket = S3GetSession()
    # load obj
    obj = s3.Object(bucket_name, s3_path)    
    remote_mtime = None
    try:
        # remote mtime
        remote_mtime = obj.last_modified.timestamp()
        if 'mtime' in obj.metadata:
            remote_mtime = float(obj.metadata['mtime'])
        remote_exists = True        
    except:
        # remote file dont exist 
        remote_exists = False

    remote_isnewer = False
    local_exists = os.path.isfile(str(local_path))
    local_mtime = None
    if local_exists:        
        # local mtime
        local_mtime = datetime.utcfromtimestamp(os.path.getmtime(local_path)).timestamp()        
        #compare
        remote_isnewer = remote_mtime>local_mtime        

    if ((not local_exists) & remote_exists) | (remote_isnewer) | (force_download):
        io_obj = io.BytesIO()
        try:            
            obj.download_fileobj(io_obj)
            return [io_obj , local_mtime, remote_mtime]
        except Exception as e:
            raise Exception('downloading %s,%s ERROR!\n%s' % (Logger.user,local_path,str(e)))
        
    return [None, local_mtime, remote_mtime]

def UpdateModTime(local_path, remote_mtime):    
    # update modification time
    remote_mtime_dt = datetime.fromtimestamp(remote_mtime)
    offset =  remote_mtime_dt - datetime.utcfromtimestamp(remote_mtime)        
    remote_mtime_local_tz = remote_mtime_dt+offset
    remote_mtime_local_tz_ts = remote_mtime_local_tz.timestamp()                
    os.utime(local_path, (remote_mtime_local_tz_ts, remote_mtime_local_tz_ts))

def S3SaveLocal(local_path, io_obj, remote_mtime):
    path = Path(local_path)
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
    with open(local_path,'wb') as f:
        f.write(io_obj.getbuffer())
        f.flush()
    # update modification time
    remote_mtime_dt = datetime.fromtimestamp(remote_mtime)
    offset =  remote_mtime_dt - datetime.utcfromtimestamp(remote_mtime)        
    remote_mtime_local_tz = remote_mtime_dt+offset
    remote_mtime_local_tz_ts = remote_mtime_local_tz.timestamp()                
    os.utime(local_path, (remote_mtime_local_tz_ts, remote_mtime_local_tz_ts))

def S3Upload(file_io, path, mtime):
    remotefilepath = str(path).replace(\
            os.environ['DATABASE_FOLDER'],os.environ['S3_BUCKET'])
    remotefilepath = remotefilepath.replace('\\','/')        
          
    trials = 3
    success=False
    while trials>0:        
        try:                
            s3,bucket = S3GetSession(isupload=True)            
            mtime_utc = datetime.utcfromtimestamp(mtime).timestamp()
            mtime_str = str(mtime_utc)
            file_io.seek(0)
            bucket.upload_fileobj(file_io,remotefilepath.replace(os.environ['S3_BUCKET'],'')[1:],\
                ExtraArgs={'Metadata': {'mtime': mtime_str}})            
            success = True
            break
        except Exception as e:
            Logger.log.warning(Logger.user+' Uploading to S3 '+path+' FAILED! retrying(%i,3)...\n%s ' % (trials,str(e)))
            trials = trials - 1

    if not success:
        Logger.log.error(Logger.user+' Uploading to S3 '+path+' ERROR!')
        raise Exception(Logger.user+' Uploading to S3 '+path+' ERROR!')