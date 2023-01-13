import random, time_uuid
from datetime import datetime,timedelta, timezone

def currentTime7():
    now = datetime.now()
    d = datetime.fromisoformat(now.isoformat())
    tz = timezone(timedelta(hours=7))
    return d.astimezone(tz).strftime('%Y-%m-%dT%H:%M:%S.%f%z')

def generate_uuids_byTime7():
    now = datetime.now()
    d = datetime.fromisoformat(now.isoformat())
    tz = timezone(timedelta(hours=7))

    rand_time = lambda: float(random.randrange(0,100)) + d.astimezone(tz).timestamp()#time_uuid.utctime()
    uuids_tz7 = time_uuid.TimeUUID.with_timestamp(rand_time()) 
    return uuids_tz7

def convert_timestamp_to_datetimezone7(_timestamp):
    dt = datetime.fromtimestamp(_timestamp / 1e3)
    dtiso = datetime.fromisoformat(dt.isoformat())
    tz = timezone(timedelta(hours=7))
    return dtiso.astimezone(tz).strftime('%Y-%m-%dT%H:%M:%S.%f%z')

def difference_datetimezone7_by_day_from_now(_dtz_target):
    tz = timezone(timedelta(hours=7))
    dtz_now = datetime.fromisoformat(datetime.now().isoformat()).astimezone(tz)
    dtz_target = datetime.strptime(str(_dtz_target).strip(),'%Y-%m-%dT%H:%M:%S.%f%z')
    return (dtz_now-dtz_target).days
    
def difference_datetimezone7_by_seconds_from_between(_dtz_first, _dtz_last):
    _dtz_1 = datetime.strptime(str(_dtz_first).strip(),'%Y-%m-%dT%H:%M:%S.%f%z')
    _dtz_2 = datetime.strptime(str(_dtz_last).strip(),'%Y-%m-%dT%H:%M:%S.%f%z')
    diff = (_dtz_2-_dtz_1).seconds
    return diff

def maxdatetime_lstdict(_lst_dict=[]):
    mxtime = None
    try:
        if len(_lst_dict)!=0:
            _lst_t = []
            for t in _lst_dict:
                _lst_t.append(datetime.strptime(t,'%Y-%m-%dT%H:%M:%S.%f%z'))
            mxtime = max(_lst_t)
    except:
        mxtime = None
    return mxtime
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## For General date time
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def difference_datetime_by_seconds_from_between(_dt_first, _dt_last, _dtFormated):
    _dt_1 = datetime.strptime(str(_dt_first).strip(), _dtFormated)
    _dt_2 = datetime.strptime(str(_dt_last).strip(), _dtFormated)
    diff = (_dt_2-_dt_1).total_seconds() 
    return diff

def difference_datetime_by_dHMS_from_between(_dt_first, _dt_last, _dtFormated):
    time = float(difference_datetime_by_seconds_from_between(_dt_first, _dt_last, _dtFormated))
    day =  time // (24 * 3600)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time
    result = "%dd %dh%dm%ds" % (day, hour, minutes, seconds)
    return result

def datetime_withAdjustedHour_fromServer(_str_dt, _hour, _dtFormated='%Y-%m-%dT%H:%M:%SZ'):
    dt = datetime.strptime(str(_str_dt).strip(),_dtFormated)
    dt_adjusted =  (dt + timedelta(hours=int(_hour))).strftime(_dtFormated)
    return dt_adjusted