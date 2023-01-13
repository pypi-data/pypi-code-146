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

class const_type(Enum):
    log = 'Log-pod'
    restart = 'Restart-pod'

class const_sincelast(Enum):
    h1 = '1h'
    h12 = '12h'
    h24 = '24h'
    
class const_process(Enum):
    end = 0
    start = 1

class const_status(Enum):
    ToDo = 'To do'
    InProgress = 'In progress'
    Done = 'Done'

class const_execmethod(Enum):
    OneToOne = 'One-to-one'
    OneToMany = 'One-to-many'


class utils():
    def simulation(self,_number,_nameof_msg_rpt, _namespace, _sincelast, _lst_patterns, _lst_target=[], **kwargs):
        allowParam = False;threadNumber = None;idAirtable = None
        if '_argThreadNumber' in kwargs:
                    threadNumber = kwargs.get("_argThreadNumber") 
                    if "'int'" in str(type(threadNumber)):
                        idAirtable = None
                        if '_argIdAirtable' in kwargs:
                            idAirtable = kwargs.get("_argIdAirtable") 
                            allowParam = True
        if allowParam==True:
            Q.logger(time7.currentTime7(),'',_argThreadNumber = threadNumber, _argIdAirtable = idAirtable)
            Q.logger(time7.currentTime7(),'      [ Begin simulation - {0} ] シミュレーション'.format(_number),_argThreadNumber = threadNumber, _argIdAirtable = idAirtable)
            Q.logger(time7.currentTime7(),'        Arguments (パラメタ値):',_argThreadNumber = threadNumber, _argIdAirtable = idAirtable)
            Q.logger(time7.currentTime7(),'         - name of message :', _nameof_msg_rpt,_argThreadNumber = threadNumber, _argIdAirtable = idAirtable)
            Q.logger(time7.currentTime7(),'         - namespace :', _namespace,_argThreadNumber = threadNumber, _argIdAirtable = idAirtable)
            Q.logger(time7.currentTime7(),'         - sincelast :', _sincelast,_argThreadNumber = threadNumber, _argIdAirtable = idAirtable)
            Q.logger(time7.currentTime7(),'         - patterns :', str(_lst_patterns),_argThreadNumber = threadNumber, _argIdAirtable = idAirtable)
            Q.logger(time7.currentTime7(),'         - targets :', str(_lst_target),_argThreadNumber = threadNumber, _argIdAirtable = idAirtable)
            Q.logger(time7.currentTime7(),'      ', '.'*83,_argThreadNumber = threadNumber, _argIdAirtable = idAirtable)



            if len(_lst_target)!=0:
                for x in _lst_target:
                    Q.logger(time7.currentTime7(),'       In Progress step (',str(x),')',_argThreadNumber = threadNumber, _argIdAirtable = idAirtable)
                    time.sleep(1)
            Q.logger(time7.currentTime7(),'      ', '.'*83,_argThreadNumber = threadNumber, _argIdAirtable = idAirtable)
            Q.logger(time7.currentTime7(),'',_argThreadNumber = threadNumber, _argIdAirtable = idAirtable)
            Q.logger(time7.currentTime7(),'',_argThreadNumber = threadNumber, _argIdAirtable = idAirtable)


    def convert_airtableDict_to_dictionary(self,airtable):
        lst_data = []
        try:
            if airtable:
                for page in airtable:
                    dict_row = {}
                    dict_row['id'] = page['id']
                    for key in page.keys():
                        if 'dict' in str(type(page[key])):
                            for record in page[key]:
                                dict_row[record] = page[key][record]
                    lst_data.append(dict_row)
        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "convert_airtableDict_to_dictionary"')    
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
        return lst_data

    def view_dictionary(self,lst_dict):
        try:
            if lst_dict:
                Q.logger(time7.currentTime7(),'')
                Q.logger(time7.currentTime7(),'      [view dictionary]')
                Q.logger(time7.currentTime7(),'     ','-'*50)
                for row in lst_dict:
                    for record in row:
                        Q.logger(time7.currentTime7(),' '*6,record,':',str(row[record]))
                    Q.logger(time7.currentTime7(),'     ','-'*50)
                    time.sleep(1)
                Q.logger(time7.currentTime7(),'')
        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "view_dictionary"')    
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))

    # into utils Class
    def escape_dict(self,_page, _key, _esc=''):
        oput = None
        try: oput = str(_page[_key]).strip()
        except: oput = _esc
        return oput

#  PYAIRTABLE for function add / update new row manage process   
    def scannKwargs_param_String_Integer_Boolean_Type(self, _strKwargsName,kwargs, _variable_type_value, _default_getValue, _isMandatory = False):
        kwargs_value = None; allowParam = False
        try:
            kwargs_value, dump = mpl.kwargs().getValueAllowed(kwargs, _strKwargsName, _variable_type_value, _default_getValue)
            if dump == False:
                allowParam = False
                if _isMandatory == True: raise Exception('Sorry this is mandatory, please check your {0} type.'.format(str(_strKwargsName)))
                else: 
                    if not str(_strKwargsName) in kwargs: return '', True
                    else: 
                        if not _variable_type_value in str(type(kwargs)): 
                            raise Exception('Sorry, please check your {0} type.'.format(str(_strKwargsName)))
            else:
                if len(str(kwargs_value).strip()) != 0: allowParam = True
                else:
                    allowParam = False
                    raise Exception('Sorry, please check your {0} value.'.format(str(_strKwargsName)))
        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "scannKwargs_param_String_Integer_Boolean_Type"')
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
        return kwargs_value, allowParam

    def scannKwargs_paramStringSingleSelectType(self, _strKwargsName,kwargs, members, _isMandatory = False):
        kwargs_value = None; allowParam = False
        try:
            kwargs_value, dump = mpl.kwargs().getValueAllowed(kwargs, _strKwargsName, mpl.variable_type.str.value,'')
            if dump == False:
                allowParam = False
                if _isMandatory == True: raise Exception(f"Sorry this is mandatory, please check your {_strKwargsName} type.")
                else:
                    if not str(_strKwargsName) in kwargs: return '', True
                    else: 
                        if not mpl.variable_type.str.value in str(type(kwargs)): 
                            raise Exception('Sorry, please check your {0} type.'.format(str(_strKwargsName)))            
            else:
                if str(kwargs_value).strip()!='':
                    value = [member.value for member in members]
                    if str(kwargs_value).strip() in value: allowParam = True
                    else:
                        allowParam = False
                        raise Exception(f"Sorry, your {_strKwargsName} is not valid. Please check your value. Value available is {str(value)}")
                else:
                    allowParam = False
                    raise Exception(f"Sorry, please check your {_strKwargsName} value.")
        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "scannKwargs_paramStringSingleSelectType"')
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
        return kwargs_value, allowParam    

    def scannKwargs_paramListType(self, _strKwargsName, kwargs, notEmpty = False, _isMandatory = False):
        kwargs_value = None; allowParam = False
        try:
            kwargs_value, dump = mpl.kwargs().getValueAllowed(kwargs, _strKwargsName, mpl.variable_type.list.value,[])
            if dump == False:
                allowParam = False
                if _isMandatory == True: raise Exception('Sorry this is mandatory, please check your {0} type.'.format(str(_strKwargsName)))
                else:
                    if not str(_strKwargsName) in kwargs: return '', True
                    else: 
                        if not mpl.variable_type.list.value in str(type(kwargs)): 
                            raise Exception('Sorry, please check your {0} type.'.format(str(_strKwargsName)))  
            else: 
                if notEmpty == True:
                    if len(kwargs_value)!= 0: allowParam = True
                    else: 
                        allowParam = False
                        raise Exception(f"Sorry, your {_strKwargsName} cannot be empty")
                else: allowParam = True

            kwargs_value = json.dumps(kwargs_value)

        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "scannKwargs_paramListType"')
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
        return kwargs_value, allowParam