## packages standard :
import time
import json
import random
from enum import Enum

## packages add-ons :
import damv1env as env
import damv1time7 as time7
import damv1time7.mylogger as Q
import damv1manipulation as mpl

## Reference use "pyairtable" ***
## https://pyairtable.readthedocs.io/en/latest/getting-started.html
from pyairtable import Api, Base, Table
from pyairtable.formulas import match, FIND, FIELD, EQUAL, STR_VALUE, OR, AND, escape_quotes

from .myairtable_projectk8salert import utils, \
        const_type, const_sincelast, const_process, const_status, const_execmethod

class sandbox():
    AIRTABLE_API_KEY = env.sandbox_airtable.api_key.value
    AIRTABLE_BASE_ID = env.sandbox_airtable.base_id.value
    AIRTABLE_TABLE_NAME = env.sandbox_airtable.table_name.value
    ## * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
    ## USED PYAIRTABLE
    ## * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Example : [ get data by formula match with condition OR ]
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # out = f.pyairtable_loadAll_by_OR_condition({'status': 'Done','Enable': True})
    # print(out)
    def pyairtable_loadAll_by_OR_condition(self, _pattern):
        # Notes : If match_any=True, expressions are grouped with OR()
        lst_output =[]
        Q.logger(time7.currentTime7(),'    - Loading airtable by OR contion on formula:')
        try:
            if len(_pattern)!=0:
                table = Table(self.AIRTABLE_API_KEY, self.AIRTABLE_BASE_ID, self.AIRTABLE_TABLE_NAME)
                query = match(_pattern,match_any=True)
                r = table.all(formula=query)
                if r: 
                    lst_output = r
                    Q.logger(time7.currentTime7(),'      Successful load data')
        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "pyairtable_loadAll_by_OR_condition"')    
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
        return lst_output

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Example : [ get data by raw formula ]
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # raw_example = None
    # # skenario 1
    # raw_example = "FIND('Done', {Status})"
    # # skenario 2
    # raw_example =  "AND(NOT(OR({status}='Done', {Status}='To do')),{ns}='sit')"
    # # skenario 3
    # raw_status_todo = EQUAL(STR_VALUE('To do'),FIELD('status'))
    # raw_status_done = EQUAL(STR_VALUE('Done'),FIELD('status'))
    # raw_example = OR(raw_status_todo,raw_status_done)
    # # skenario 4
    # raw_example = EQUAL(STR_VALUE('To do'),FIELD('status'))
    # # skenario 5
    # raw_example = FIND(STR_VALUE('inventory'),FIELD('target contains'))
    # out = f.pyairtable__loadAll_by_rawformula(raw_example)
    # print(out)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def pyairtable__loadAll_by_rawformula(self, _raw):
        # Reference https://pyairtable.readthedocs.io/en/latest/api.html
        Q.logger(time7.currentTime7(),'    - Loading airtable by raw formula:')
        lst_output = []
        try:
            if _raw.strip()!= '':
                table = Table(self.AIRTABLE_API_KEY, self.AIRTABLE_BASE_ID, self.AIRTABLE_TABLE_NAME)
                r = table.all(formula=_raw)
                if r: 
                    lst_output = r 
                    Q.logger(time7.currentTime7(),'      Successful load data')
        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "pyairtable__loadAll_by_rawformula"')    
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
        return lst_output

### %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
### %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
### SCHEMA TABLE PROJECTS    
# 'name'                          # single line text
# 'title'                         # single line text
# 'type'                          # single select | Log-pod, Restart-pod
# 'ns'                            # single line text | description: namespace
# 'target contains'               # long text | values: [dictionary]
# 'patterns'                      # long text | values: [dictionary]
# 'Enable'                        # checkbox
# 'status'                        # single select | To do, In Progress, Done
# 'cip'                           # number (integer:2) | description: Counter in Progress
# 'start date'                    # single line text
# 'end date'                      # single line text
# 'detected'                      # single line text | values: [dictionary]
# 'report'                        # single line text | values: [dictionary]
# 'exec method'                   # single select | One-to-one, One-to-many
# 'last of log 1'                 # single line text | description the current time live last of log
# 'last of log 2'                 # single line text | description the current time live last of log
# 'last of log 3'                 # single line text | description the current time live last of log
### %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
### %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    ## * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
    ## USED PYAIRTABLE
    ## * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
    
    def pyairtable_delete_all_rows(self):
        Q.logger(time7.currentTime7(),'    - Deleting all rows data ( すべて消す ):')
        boolexecute = False
        try:
            table = Table(self.AIRTABLE_API_KEY, self.AIRTABLE_BASE_ID, self.AIRTABLE_TABLE_NAME)
            data = table.all()
            if data:
                for row in data:
                    Q.logger(time7.currentTime7(),'        Deleted id (', row['id'],')')
                    table.delete(row['id'])
                Q.logger(time7.currentTime7(),'      Successful delete all data')
            else:
                Q.logger(time7.currentTime7(),'      Data is empty, abort delete')
            boolexecute = True
        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "pyairtable_delete_all_rows"')    
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))    
        return boolexecute

    def pyairtable_create_batchrow(self):
        Q.logger(time7.currentTime7(),'    - Creating batch of row data:')
        boolexecute = False
        try:
            table = Table(self.AIRTABLE_API_KEY, self.AIRTABLE_BASE_ID, self.AIRTABLE_TABLE_NAME)
            table.batch_create(\
                    [
                        # {'name':'WF-1', 'title': escape_quotes('[ALERT] Logs service SIT'), 'type':'Log-pod', 'ns':'sit', 'target contains':escape_quotes('["dashboardsvc", "distributorshippromotionquery", "inventory", "pricecmd", "shopeeintegrationcmd", "userquery", "warehousequery"]'),'patterns':escape_quotes('["ERROR 7 ---","Error while validating pooled Jedis object","JedisConnectionException: java.net.SocketTimeoutException: Read timed out"]'), 'Enable': True, 'status':'To do','detected':'[]','report':escape_quotes('[]')},
                        # {'name':'WF-2', 'title': escape_quotes('[ALERT] Logs service UAT'), 'type':'Log-pod','ns':'uat', 'target contains':escape_quotes('["dashboardsvc", "distributorshippromotionquery", "inventory", "pricecmd", "shopeeintegrationcmd", "userquery", "warehousequery"]'),'patterns':escape_quotes('["ERROR 7 ---","Error while validating pooled Jedis object","JedisConnectionException: java.net.SocketTimeoutException: Read timed out"]'), 'Enable': True, 'status':'To do','detected':'[]','report':escape_quotes('[]')},
                        {'name':'WF-1', 'title': escape_quotes('[ALERT] Logs service SIT'), 'type':'Log-pod', 'ns':'sit', 'target contains':escape_quotes('["wmsjavelin", "webcommerceinventory"]'),'patterns':escape_quotes('["error: ERROR sql insert with","Execution of Rabbit message listener failed"]'), 'Enable': True, 'status':'To do','detected':'[]','report':escape_quotes('[]')},
                        {'name':'WF-2', 'title': escape_quotes('[ALERT] Logs service UAT'), 'type':'Log-pod','ns':'uat', 'target contains':escape_quotes('["wmsjavelin", "webcommerceinventory"]'),'patterns':escape_quotes('["error: ERROR sql insert with","Execution of Rabbit message listener failed"]'), 'Enable': True, 'status':'To do','detected':'[]','report':escape_quotes('[]')},
                        {'name':'WF-3', 'title': escape_quotes('[ALERT] Restarts tracked'), 'type':'Restart-pod','ns':'sit', 'target contains':'[]','patterns':'["Restart"]', 'status':'To do','detected':'[]','report':'[]'},
                        {'name':'WF-4', 'title': escape_quotes('[ALERT] Restarts tracked'), 'type':'Restart-pod','ns':'uat', 'target contains':'[]','patterns':'["Restart"]', 'status':'To do','detected':'[]','report':'[]'},
                    ]
                )
            Q.logger(time7.currentTime7(),'      Successful create batch of row data')
        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "pyairtable_create_batchrow"')    
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))    
        return boolexecute

    def pyairtable_loadAll_by_enable_ColParams(self, _enable=True):
        data = []
        Q.logger(time7.currentTime7(),'    - Loading airtable:')
        try:
            table = Table(self.AIRTABLE_API_KEY, self.AIRTABLE_BASE_ID, self.AIRTABLE_TABLE_NAME)
            query = match({"enable": _enable})
            airtable = table.all(formula=query,fields=['name', 'title', 'type', 'ns', 'target contains', 'patterns', 'Enable', 'status', 'cip', 'start date', 'exec method', 'last of log 1', 'last of log 2', 'last of log 3'])
            if airtable: 
                data = airtable
                Q.logger(time7.currentTime7(),'      Successful load data')
        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "pyairtable_loadAll_by_enable_ColParams"')
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
        return data

    def pyairtable_getFirstLstDict_by_name_and_enable(self, _table, _name, _Enable, _fields):
        lst_data = []
        try:
            query = match({'name': _name, "Enable": bool(_Enable)})
            airtable = _table.first(formula=query,fields=_fields)
            dict_airtable = []; dict_airtable.append(airtable)
            lst_data = utils().convert_airtableDict_to_dictionary(dict_airtable)
        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "pyairtable_getFirstLstDict_by_name_and_enable"')
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
        return lst_data

    def pyairtable_update_StartEnd_process(self, _id, _name, _Enable, _stepProcess, **kwargs):
        try:
            Q.logger(time7.currentTime7(),'    - Update process ( status, cip, start/end date ) :')
            table = Table(self.AIRTABLE_API_KEY, self.AIRTABLE_BASE_ID, self.AIRTABLE_TABLE_NAME)
            lst_data = self.pyairtable_getFirstLstDict_by_name_and_enable(table, _name,_Enable,['name','type','cip'])
            if len(lst_data)!=0:
                id = str(utils().escape_dict(lst_data[0],'id')).strip()
                cipInt = int(utils().escape_dict(lst_data[0],'cip','0'))
                field_date = None

                maxThreadNumber = 3 # Default ( デフォルト )
                if '_argMaxThread' in kwargs:
                    maxThreadNumber = kwargs.get("_argMaxThread") 
                    Q.logger(time7.currentTime7(),"      set _argMaxThread : ", str(maxThreadNumber))

                if id == str(_id).strip():
                    match _stepProcess:
                        case const_process.start.value: 
                            Q.logger(time7.currentTime7(),'      [ airtable - assign start process ]')
                            if cipInt<int(maxThreadNumber) : cipInt = cipInt + 1
                            field_date = 'start date'
                        case const_process.end.value: 
                            Q.logger(time7.currentTime7(),'      [ airtable - assign end process ]')
                            if cipInt>0: cipInt = cipInt - 1
                            field_date = 'end date'
                    if cipInt == 0:
                        table.update(id,{'status':const_status.Done.value, field_date:time7.currentTime7(), 'cip':cipInt})
                    else:
                        table.update(id,{'status':const_status.InProgress.value, field_date:time7.currentTime7(), 'cip': cipInt})
                    Q.logger(time7.currentTime7(),'        successful assign ')
        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "pyairtable_update_StartEnd_process"')
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))

    def pyairtable_append_detected_and_report_process(self, _id, _name, _Enable, _sumDetected, _urlShareable):
        try:
            table = Table(self.AIRTABLE_API_KEY, self.AIRTABLE_BASE_ID, self.AIRTABLE_TABLE_NAME)
            lst_data = self.pyairtable_getFirstLstDict_by_name_and_enable(table, _name,_Enable,['name','detected','report'])
            if len(lst_data)!=0:

                Q.logger(time7.currentTime7(),'      [ airtable - assign object detected and shared report ] ')
                id = str(utils().escape_dict(lst_data[0],'id')).strip()
                lst_detected = []; lst_detected = json.loads(utils().escape_dict(lst_data[0],'detected','[]'))
                if len(lst_detected)>=3:lst_detected.clear()
                lst_detected.append(_sumDetected)

                lst_report = []; lst_report = json.loads(utils().escape_dict(lst_data[0],'report','[]'))
                if len(lst_report)>=3:lst_report.clear()
                lst_report.append(_urlShareable)

                if id == str(_id).strip():
                    table.update(id,{'detected':escape_quotes(json.dumps(lst_detected)), 'report':escape_quotes(json.dumps(lst_report))})
                    Q.logger(time7.currentTime7(),'        successful assign ')
        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "pyairtable_append_detected_and_report_process"')
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))

    def pyairtable_threadUpdate_lastoflog(self, _id, _numThread, _valueForUpdate = time7.currentTime7(), **kwargs):
        try:
            Q.logger(time7.currentTime7(),'    - Update last of log fields airtable:')
            table = Table(self.AIRTABLE_API_KEY, self.AIRTABLE_BASE_ID, self.AIRTABLE_TABLE_NAME)
            allowArgs = False
            maxThreadNumber = 3 # Default ( デフォルト )
            if '_argMaxThread' in kwargs:
                maxThreadNumber = kwargs.get("_argMaxThread") 
                Q.logger(time7.currentTime7(),"      set _argMaxThread : ", str(maxThreadNumber))

            if str(_id).strip()!= '' and "'int'" in str(type(_numThread)) :
                if int(_numThread)>0 and int(_numThread)<= maxThreadNumber:
                    allowArgs = True

            if allowArgs == True:
                paramUpdate = {}; paramUpdate['last of log {0}'.format(_numThread)] = _valueForUpdate
                table.update(_id,paramUpdate)
                Q.logger(time7.currentTime7(),'      Success for update')
            else:
                Q.logger(time7.currentTime7(),'      Perboden Arguments')
        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "pyairtable_threadUpdate_lastoflog"')
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',e)
    
    def pyairtable_update_clearAll_lastoflog(self, _id, **kwargs):
        try:
            Q.logger(time7.currentTime7(),'    - Update clear all last of log fields airtable:')
            table = Table(self.AIRTABLE_API_KEY, self.AIRTABLE_BASE_ID, self.AIRTABLE_TABLE_NAME)
            allowArgs = False
            maxThreadNumber = 3 # Default ( デフォルト )
            if '_argMaxThread' in kwargs:
                maxThreadNumber = kwargs.get("_argMaxThread") 
                Q.logger(time7.currentTime7(),"      set _argMaxThread : ", str(maxThreadNumber))

            if str(_id).strip()!= '':
                allowArgs = True
            
            if allowArgs == True:
                for i in range(1,maxThreadNumber+1):
                    paramUpdate = {}; paramUpdate['last of log {0}'.format(i)] = ''
                    table.update(_id,paramUpdate)
                Q.logger(time7.currentTime7(),'      Success for clear all update')
        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "pyairtable_update_clearAll_lastoflog"')
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))

    def pyairtable_update_clearOneSelection_lastoflog(self, _id, _numThread, **kwargs):
        try:
            Q.logger(time7.currentTime7(),'    - Update clear one selection from last of log fields airtable:')
            table = Table(self.AIRTABLE_API_KEY, self.AIRTABLE_BASE_ID, self.AIRTABLE_TABLE_NAME)
            allowArgs = False
            maxThreadNumber = 3 # Default ( デフォルト )
            if '_argMaxThread' in kwargs:
                maxThreadNumber = kwargs.get("_argMaxThread") 
                Q.logger(time7.currentTime7(),"      set _argMaxThread : ", str(maxThreadNumber))

            if str(_id).strip()!= '' and "'int'" in str(type(_numThread)) :
                if int(_numThread)>0 and int(_numThread)<= maxThreadNumber:
                    allowArgs = True

            if allowArgs == True:
                paramUpdate = {}; paramUpdate['last of log {0}'.format(str(_numThread))] = ''
                table.update(_id,paramUpdate)
                Q.logger(time7.currentTime7(),'      Success for clear one update')

        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "pyairtable_update_clearOneSelection_lastoflog"')
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))

    def pyairtable_getIntCip_now(self, _id, **kwargs):
        IntCipNow = 0
        try:
            Q.logger(time7.currentTime7(),'    - Get Integer Cip (Count in process) now:')
            allowArgs = False
            maxThreadNumber = 3
            if str(_id).strip()!= '':
                allowArgs = True

            if '_argMaxThread' in kwargs:
                maxThreadNumber = kwargs.get("_argMaxThread") 
                Q.logger(time7.currentTime7(),"      set _argMaxThread : ", str(maxThreadNumber))

            if allowArgs == True:
                api = Api(self.AIRTABLE_API_KEY)
                record = []; record.append(api.get(self.AIRTABLE_BASE_ID, self.AIRTABLE_TABLE_NAME, _id))
                data = utils().convert_airtableDict_to_dictionary(record)
                # utils().view_dictionary(data)

                if 'cip' in data[0].keys():
                    IntCipNow = int(data[0]['cip'])
                    Q.logger(time7.currentTime7(),'      get cip update : ({0})'.format(str(IntCipNow)))
                else:
                    Q.logger(time7.currentTime7(),'      Not found cip key')

        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "pyairtable_getIntCip_now"')
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
        return IntCipNow


    def pyairtable_getFields_FirstThreadNumberAvailable(self, _id, **kwargs):
        info_first_available = {}
        try:
            Q.logger(time7.currentTime7(),'    - Get info first threads available:')
            allowArgs = False
            maxThreadNumber = 3
            if str(_id).strip()!= '':
                allowArgs = True

            if '_argMaxThread' in kwargs:
                maxThreadNumber = kwargs.get("_argMaxThread") 
                Q.logger(time7.currentTime7(),"      set _argMaxThread : ", str(maxThreadNumber))

            if allowArgs == True:
                api = Api(self.AIRTABLE_API_KEY)
                record = []; record.append(api.get(self.AIRTABLE_BASE_ID, self.AIRTABLE_TABLE_NAME, _id))
                data = utils().convert_airtableDict_to_dictionary(record)
                # utils().view_dictionary(data)
                lst_keyAvailable = {}
                for i in range(1, maxThreadNumber + 1):
                    key = 'last of log {0}'.format(str(i))
                    if not key in data[0].keys():
                        lst_keyAvailable[key] = str(i)

                if len(lst_keyAvailable)>0:
                    # get first key available
                    first_key = next(iter(lst_keyAvailable))
                    first_value = lst_keyAvailable[first_key]
                    info_first_available['first key']= first_key
                    info_first_available['first value']= first_value
                    Q.logger(time7.currentTime7(),'      available of first key and value {', f'"{first_key}" : {first_value}','}')
                else:
                    Q.logger(time7.currentTime7(),'      [ not available thread ]')
        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "pyairtable_getFields_FirstThreadNumberAvailable"')
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
        return info_first_available
    
    def pyairtable_detectCrashProcess_then_recovery(self, _lst_data, **kwargs):
        try:
            Q.logger(time7.currentTime7(),'    - Checking for crash process:')
            maxThreadNumber = 3
            maxSecondsTimeLogsWaiting = 60
            DiffMinSecondsSilentLogger_forUpdate = 3.5
            if '_argMaxThread' in kwargs:
                maxThreadNumber = kwargs.get("_argMaxThread") 
                Q.logger(time7.currentTime7(),"      set _argMaxThread :", str(maxThreadNumber))

            if '_argMaxSecondsTimeLogsWaiting' in kwargs:
                maxSecondsTimeLogsWaiting = kwargs.get("_argMaxSecondsTimeLogsWaiting") 
                Q.logger(time7.currentTime7(),"      set _argMaxSecondsTimeLogsWaiting :", str(maxSecondsTimeLogsWaiting),'s')

            if '_argDiffMinSecondsSilentLogger_forUpdate' in kwargs:
                DiffMinSecondsSilentLogger_forUpdate = kwargs.get("_argDiffMinSecondsSilentLogger_forUpdate") 
                Q.logger(time7.currentTime7(),"      set _argDiffMinSecondsSilentLogger_forUpdate :", str(DiffMinSecondsSilentLogger_forUpdate),'s')


            if len(_lst_data)!=0:
                u = utils()
                Q.logger(time7.currentTime7(),'      ','.'*40)
                for idx, r in  enumerate(_lst_data):
                    r_id = u.escape_dict(r,'id')
                    r_status = u.escape_dict(r,'status')
                    r_cip = u.escape_dict(r,'cip',0)
                    r_start_date = u.escape_dict(r,'start date')
                    r_lastOfLog1 = u.escape_dict(r,'last of log 1')
                    r_lastOfLog2 = u.escape_dict(r,'last of log 2')
                    r_lastOfLog3 = u.escape_dict(r,'last of log 3')
                    Q.logger(time7.currentTime7(),'       -> check esc id :', str(r_id))
                    Q.logger(time7.currentTime7(),'       -> check esc status :', str(r_status))
                    Q.logger(time7.currentTime7(),'       -> check esc cip :', str(r_cip))
                    Q.logger(time7.currentTime7(),'       -> check esc last of log 1 :', str(r_lastOfLog1) )
                    Q.logger(time7.currentTime7(),'       -> check esc last of log 2 :', str(r_lastOfLog2) )
                    Q.logger(time7.currentTime7(),'       -> check esc last of log 3 :', str(r_lastOfLog3) )
                    if str(r_status).strip()==const_status.InProgress.value and \
                        int(r_cip)!=0 and \
                        str(r_lastOfLog1).strip() == '' and \
                        str(r_lastOfLog2).strip() == '' and \
                        str(r_lastOfLog3).strip() == '':
                        Q.logger(time7.currentTime7(),'       Parameter 1 :')
                        Q.logger(time7.currentTime7(),'       [ Detected Crash Process ]')
                        table = Table(self.AIRTABLE_API_KEY, self.AIRTABLE_BASE_ID, self.AIRTABLE_TABLE_NAME)
                        table.update(r_id,{'status':escape_quotes(const_status.ToDo.value), 'cip':0})
                        Q.logger(time7.currentTime7(),'        => Success for recovery')
                    lst_tLast_log = []
                    if str(r_lastOfLog1).strip() != '': lst_tLast_log.append(str(r_lastOfLog1).strip())
                    if str(r_lastOfLog2).strip() != '': lst_tLast_log.append(str(r_lastOfLog2).strip())
                    if str(r_lastOfLog3).strip() != '': lst_tLast_log.append(str(r_lastOfLog3).strip())
                    if len(lst_tLast_log)!=0 and int(r_cip)!=0 and str(r_status).strip()==const_status.InProgress.value:
                        Q.logger(time7.currentTime7(),'     Parameter 2 :')
                        max_lastoflog=str(time7.maxdatetime_lstdict(lst_tLast_log)).replace(' ', 'T').replace('07:00','0700')
                        Q.logger(time7.currentTime7(),'       -> check start date :', str(r_start_date))
                        Q.logger(time7.currentTime7(),'       -> check max last of logs :', str(max_lastoflog))
                        diffseconds = time7.difference_datetimezone7_by_seconds_from_between(r_start_date,max_lastoflog)
                        Q.logger(time7.currentTime7(),'          [result check difference_datetimezone7_by_seconds_from_between : {}s ]'.format(str(diffseconds)))
                        if diffseconds >= int(maxSecondsTimeLogsWaiting):
                            Q.logger(time7.currentTime7(),'          [ Detected Crash Process ]')
                            table = Table(self.AIRTABLE_API_KEY, self.AIRTABLE_BASE_ID, self.AIRTABLE_TABLE_NAME)
                            table.update(r_id,{'status':escape_quotes(const_status.ToDo.value), 'cip':0})
                            self.pyairtable_update_clearAll_lastoflog(r_id, _argMaxThread = maxThreadNumber)
                            Q.logger(time7.currentTime7(),'        => Success for recovery')
                    Q.logger(time7.currentTime7(),'      ','.'*40)

        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "pyairtable_detectCrashProcess_then_recovery"')
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))

    def pyairtable_updateDateTime_CurrentNumberLastOfLog(self, _numberOfThread, _id, **kwargs):
        if "'int'" in str(type(_numberOfThread)) and str(_id)!='':
            table = Table(self.AIRTABLE_API_KEY, self.AIRTABLE_BASE_ID, self.AIRTABLE_TABLE_NAME)
            table.update(_id,{f'last of log {str(_numberOfThread)}':escape_quotes(time7.currentTime7())})

### - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  
#  PYAIRTABLE for function add / update new row manage process   
    def pyairtable_InsertUpdateData_SingleRow(self, _patterns_notEmpty, **kwargs):
        Q.logger(time7.currentTime7(),'    - Add/Update data single row in airtable :')
        allowParam = False; lst_singleRow = {}
        try:
            singleRow_name, allowParam = utils().scannKwargs_param_String_Integer_Boolean_Type('_argName', kwargs, mpl.variable_type.str.value, '',True)
            singleRow_title, allowParam = utils().scannKwargs_param_String_Integer_Boolean_Type('_argTitle', kwargs, mpl.variable_type.str.value, '', True)
            singleRow_type, allowParam = utils().scannKwargs_paramStringSingleSelectType('_argType', kwargs, const_type,True)
            singleRow_ns, allowParam = utils().scannKwargs_param_String_Integer_Boolean_Type('_argNs', kwargs, mpl.variable_type.str.value, '', True)
            singleRow_targets, allowParam = utils().scannKwargs_paramListType('_argTargets', kwargs,False,True)
            singleRow_patterns, allowParam = utils().scannKwargs_paramListType('_argPatterns', kwargs, _patterns_notEmpty, True)
            singleRow_Enable, allowParam = utils().scannKwargs_param_String_Integer_Boolean_Type('_argEnable', kwargs, mpl.variable_type.bool.value, False, True)
            singleRow_status, allowParam = utils().scannKwargs_paramStringSingleSelectType('_argStatus', kwargs, const_status, True)
            singleRow_cip , allowParam = utils().scannKwargs_param_String_Integer_Boolean_Type('_argCip', kwargs, mpl.variable_type.int.value, '', True)
            singleRow_execMethod, allowParam = utils().scannKwargs_paramStringSingleSelectType('_argExecMethod', kwargs, const_execmethod,True)
            ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            if allowParam == True:
                if str(singleRow_name).strip(): lst_singleRow['name'] = escape_quotes(singleRow_name.strip())
                if str(singleRow_title).strip(): lst_singleRow['title'] = escape_quotes(singleRow_title.strip())
                if str(singleRow_type).strip(): lst_singleRow['type'] = escape_quotes(singleRow_type.strip())
                if str(singleRow_ns).strip(): lst_singleRow['ns'] = escape_quotes(singleRow_ns.strip())
                if str(singleRow_targets).strip(): lst_singleRow['target contains'] = singleRow_targets
                if str(singleRow_patterns).strip(): lst_singleRow['patterns'] = singleRow_patterns
                if str(singleRow_Enable).strip(): lst_singleRow['Enable'] = singleRow_Enable
                if str(singleRow_status).strip(): lst_singleRow['status'] = escape_quotes(singleRow_status.strip())
                if str(singleRow_cip).strip():lst_singleRow['cip'] = singleRow_cip
                if str(singleRow_execMethod).strip(): lst_singleRow['exec method'] = escape_quotes(singleRow_execMethod.strip())
            ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                # Connection table
                table = Table(self.AIRTABLE_API_KEY, self.AIRTABLE_BASE_ID, self.AIRTABLE_TABLE_NAME)
                # Find value in field name
                formula = match({"name": str(singleRow_name).strip()})
                r = table.first(formula=formula) 
                # Condition insert or update of data
                if r == None : 
                    Q.logger(time7.currentTime7(), ' '*8, 'Data is not exists')
                    table.create(lst_singleRow)
                    Q.logger(time7.currentTime7(), ' '*8, 'New data is created')
                else:
                    Q.logger(time7.currentTime7(), ' '*8, 'Data is exists')
                    table.update(r['id'],lst_singleRow)
                    Q.logger(time7.currentTime7(), ' '*8, f'New data is updated [ id: {r["id"]} ]')
            ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "pyairtable_InsertUpdateData_SingleRow"')    
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
        return lst_singleRow
### %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
### %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


class testing():
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    ## uncomments this bellow for testing only ( テスティング ) !
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def excute(self):
        f = sandbox()
        u = utils()
        # used PYAIRTABLE
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # # skenario 1
        # Q.logger(time7.currentTime7(),'')
        # f.pyairtable_delete_all_rows()
        # Q.logger(time7.currentTime7(),'')
        # f.pyairtable_create_batchrow()
        # skenario 2
        Q.logger(time7.currentTime7(),'')
        Q.logger(time7.currentTime7(),'(1) - Airtable Load All by Enable ( ローディング )')
        data=f.pyairtable_loadAll_by_enable_ColParams(True)
        lst_data = u.convert_airtableDict_to_dictionary(data)
        ## skenario 3
        u.view_dictionary(lst_data)
        # print(json.dumps(lst_data))
        MaxThread = 3
        MaxSecondsTimeLogsWaiting = 60 # seconds
        if len(lst_data)!=0:
            ## skenario 4
            f.pyairtable_detectCrashProcess_then_recovery(lst_data, _argMaxThread = MaxThread, _argMaxSecondsTimeLogsWaiting = MaxSecondsTimeLogsWaiting)
            ## skenario 5
            Q.logger(time7.currentTime7(),'[ Ready ]')
            Q.logger(time7.currentTime7(),'(2) - Processing')
            for idx, r in  enumerate(lst_data):
                r_id = u.escape_dict(r,'id')
                r_name = u.escape_dict(r,'name')
                r_title = u.escape_dict(r,'title')
                r_type = u.escape_dict(r,'type')
                r_ns = u.escape_dict(r,'ns')
                r_targets = u.escape_dict(r,'target contains')
                r_patterns = u.escape_dict(r,'patterns')
                r_Enable = u.escape_dict(r,'Enable')
                r_excmethod = u.escape_dict(r,'exec method')
                number = idx + 1
                lst_patterns = json.loads(r_patterns)
                lst_targets = json.loads(r_targets)
                if const_type.log.value in r_type:
                    ## skenario 6
                    IntCipNow = f.pyairtable_getIntCip_now(r_id, _argMaxThread = MaxThread)
                    if int(IntCipNow)<int(MaxThread):
                        first_thread = f.pyairtable_getFields_FirstThreadNumberAvailable(r_id)
                        if len(first_thread)!=0:
                            Q.logger(time7.currentTime7(),'')
                            f.pyairtable_update_StartEnd_process(r_id, r_name, r_Enable, const_process.start.value, _argMaxThread = MaxThread)
                            ## skenario 7
                            thread = first_thread['first value'] # GET NUMBER OF THREAD AVAILABLE
                            f.pyairtable_threadUpdate_lastoflog(r_id,int(thread),time7.currentTime7(), _argMaxThread = MaxThread)
                            ## skenario 8
                            u.simulation(number, r_title, r_ns, const_sincelast.h24.value, lst_patterns, lst_targets, _argThreadNumber = int(thread), _argIdAirtable = str(r_id))
                            ## skenario 9
                            sumDetected = str(random.randint(1, 50))
                            urlShareable = "https://sandbox.evernote.com/shard/s1/sh/dd93c15c-33dc-4c56-9836-f36a0cb95631/8ea7d65a0f5835dfcf7c62f3ce5dee60"
                            f.pyairtable_append_detected_and_report_process(r_id, r_name, r_Enable, sumDetected,urlShareable)
                            ## skenario 10
                            f.pyairtable_update_StartEnd_process(r_id, r_name, r_Enable, const_process.end.value, _argMaxThread = MaxThread)
                            ## skenario 11
                            f.pyairtable_update_clearOneSelection_lastoflog(r_id,int(thread),_argMaxThread = MaxThread)
                            Q.logger(time7.currentTime7(),'')
            Q.logger(time7.currentTime7(),'All Done ( 仕上がり )')
        else:
            Q.logger(time7.currentTime7(),'[ Not Ready ]')



        # ## test 1
        # data = f.pyairtable_loadAll_by_OR_condition({'status': 'Done','Enable': True})
        # lst_data = u.convert_airtableDict_to_dictionary(data)
        # u.view_dictionary(lst_data)

        # ## test 2
        # raw_example = FIND(STR_VALUE('inventory'),FIELD('target contains'))
        # data = f.pyairtable__loadAll_by_rawformula(raw_example)
        # lst_data = u.convert_airtableDict_to_dictionary(data)
        # u.view_dictionary(lst_data)

        # # skenario available thread
        # f.pyairtable_update_clearAll_lastoflog('recDguppltP1M0uKb')
        # first_thread = f.pyairtable_getFields_FirstThreadNumberAvailable('recDguppltP1M0uKb')
        # if len(first_thread)!=0:
        #     thread = first_thread['first value']
        #     f.pyairtable_threadUpdate_lastoflog('recDguppltP1M0uKb',int(thread),time7.currentTime7(), _argMaxThread = 3)

# test = testing()
# test.excute()