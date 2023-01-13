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