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

from pyairtable import Api, Base, Table
from pyairtable.formulas import match, FIND, FIELD, EQUAL, STR_VALUE, OR, AND, escape_quotes

from .myairtable_projectk8salert import utils, \
        const_type, const_sincelast, const_process, const_status, const_execmethod

class production():
    AIRTABLE_API_KEY = env.production_airtable.api_key.value
    AIRTABLE_BASE_ID = env.production_airtable.base_id.value
    AIRTABLE_TABLE_NAME = env.production_airtable.table_name.value
    ## * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
    ## USED PYAIRTABLE of PRODUCTION
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
#  PRODUCTION
#  PYAIRTABLE for function add / update new row manage process   
    def pyairtable_InsertUpdateData_SingleRow(self, _patterns_notEmpty, **kwargs):
        Q.logger(time7.currentTime7(),'    - Add/Update data single row in airtable :')
        allowParam = False; lst_singleRow = {}
        try:
            singleRow_name, allowParam = utils().scannKwargs_param_String_Integer_Boolean_Type('_argName', kwargs, mpl.variable_type.str.value, '',True)
            singleRow_title, allowParam = utils().scannKwargs_param_String_Integer_Boolean_Type('_argTitle', kwargs, mpl.variable_type.str.value, '', True)
            singleRow_type, allowParam = utils().scannKwargs_paramStringSingleSelectType('_argType', kwargs,  const_type,True)
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