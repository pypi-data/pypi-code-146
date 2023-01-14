from datetime import datetime
import pandas as pd
import numpy as np
import pytz
from tzlocal import get_localzone 
local_tz = pytz.timezone(str(get_localzone()))

from SharedData.Logger import Logger
logger = Logger(__file__,user='guest')
from SharedData.Metadata import Metadata
from SharedData.SharedDataAWSKinesis import KinesisLogStreamConsumer

schedule_name = 'SCHEDULES/TRADEBOT06'
today = datetime.now().date()
year = today.timetuple()[0]
month = today.timetuple()[1]
day = today.timetuple()[2]        

_sched = Metadata(schedule_name).static.reset_index(drop=True)
sched = pd.DataFrame()
for i,s in _sched.iterrows():
    runtimes = s['Run Times'].split(',')
    for t in runtimes:
        hour = int(t.split(':')[0])
        minute = int(t.split(':')[1])
        dttm = local_tz.localize(datetime(year,month,day,hour,minute))
        s['Run Times'] = dttm
        sched = sched.reindex(columns=s.index.union(sched.columns))
        sched = pd.concat([sched, pd.DataFrame(s).T])

sched = sched.sort_values(by=['Run Times','Name']).reset_index(drop=True)
sched['Status'] = np.nan
sched['Last Message'] = np.nan

uruntimes = sched['Run Times'].unique()
runtime = uruntimes[0]
sched_sort = pd.DataFrame(columns=sched.columns)
for runtime in uruntimes:
    # mark pending routines
    while True:
        idx = runtime.astimezone(tz=local_tz)>=sched['Run Times']
        idx = (idx) & ((sched['Status'].isnull()) | (sched['Status']=='WAITING DEPENDENCIES'))

        dfpending = sched[idx]
        expiredidx = dfpending.duplicated(['Computer','Script'],keep='last')
        if expiredidx.any():
            expiredids = expiredidx.index[expiredidx]
            sched.loc[expiredids,'Status'] = 'EXPIRED'
        dfpending = dfpending[~expiredidx]
        i=0
        for i in dfpending.index:
            r = dfpending.loc[i]
            if not str(r['Dependencies'])=='nan':
                run=True
                sched.loc[i,'Status'] = 'WAITING DEPENDENCIES'
                dependencies = r['Dependencies'].replace('\n','').split(',')                
                for dep in dependencies:
                    computer = dep.split(':')[0]
                    script = dep.split(':')[1]
                    idx = sched['Computer']==computer
                    idx = (idx) & (sched['Script']==script)
                    idx = (idx) & (sched['Run Times']<=runtime.astimezone(tz=local_tz))
                    ids = sched.index[idx]
                    if len(ids)==0:
                        Logger.log.error('Dependency not scheduled for '+r['Computer']+':'+r['Script'])
                        raise Exception('Dependency not scheduled for '+r['Computer']+':'+r['Script'])                        
                    else:
                        if not str(sched.loc[ids[-1],'Status']) == 'COMPLETED':
                            run=False
                if run:
                    sched.loc[i,'Status'] = 'PENDING'
            else:
                sched.loc[i,'Status'] = 'PENDING'

        idx = sched['Status']=='PENDING'
        if idx.any():
            sched_sort = pd.concat([sched_sort, sched[idx]])
            sched_sort['Status'] = np.nan
            sched.loc[idx,'Status'] = 'COMPLETED'
        else:
            break

sched_sort.head(50)

    

