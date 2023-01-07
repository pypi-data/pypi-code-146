import damv1manipulation as mpl
import damv1airtableprojectk8salert as airtblk8salert
from .mytime7 import currentTime7 as cT7, difference_datetimezone7_by_seconds_from_between as diff_btwnsecT7

from enum import Enum

class const_thread(Enum):
    number_1 = 1
    number_2 = 2
    number_3 = 3

aCls = airtblk8salert.sandbox()

dThreadMark = {}
silentLogger = {}

def diffRange_logger(_time=cT7(), **kwargs):
    diffMark = 0
    if '_argThreadNumber' in kwargs:
        threadNumber = kwargs.get("_argThreadNumber")
        key = str(threadNumber).strip()
        if not key in dThreadMark:
            dThreadMark[key] = str(_time).strip()
        else:
            origin_mark = str(dThreadMark[key]).strip()
            # print('  - origin :',origin_mark)
            update_mark = str(_time).strip()
            # print('  - update :',update_mark)
            diffMark = diff_btwnsecT7(origin_mark,update_mark)
            dThreadMark[key] = str(_time).strip()
            # print('    [ Diff :',str(diffMark),'s ]')
    return diffMark

# # Depricated 01 Jan 2023
# def logger(_time=cT7(), *args, **kwargs):   
    
#     print(_time,' '.join(args))

#     try:
#         threadNumber = const_thread.number_1.value
#         if '_argThreadNumber' in kwargs:
#             threadNumber = kwargs.get("_argThreadNumber") 
#             if "'int'" in str(type(threadNumber)):
#                 idAirtable = None
#                 if '_argIdAirtable' in kwargs:
#                     idAirtable = kwargs.get("_argIdAirtable") 
#                     if str(idAirtable).strip()!='':
#                         aCls.pyairtable_updateDateTime_CurrentNumberLastOfLog(threadNumber,idAirtable)
#                         # pass
#     except ValueError:
#         pass


def logger(_time=cT7(), *args, **kwargs):   
    
    messages = ' '.join(args)
    bAirtableReact = False
    bShow = True
    try:

        idAirtable = ''; threadNumber, \
        bparam = mpl.kwargs().getValueAllowed(kwargs,'_argThreadNumber',mpl.variable_type.int.value, const_thread.number_1.value)        
        if bparam == True:
            idAirtable, \
            bparam = mpl.kwargs().getValueAllowed(kwargs,'_argIdAirtable',mpl.variable_type.str.value, '')
            if bparam == True:
                if (not '_argMarkSilentLogger' in kwargs) and (not '_argDiffMinSecondsSilentLogger_forUpdate' in kwargs):
                    bAirtableReact = True
                else:
                    MarkSilentLogger, \
                    bparam = mpl.kwargs().getValueAllowed(kwargs,'_argMarkSilentLogger',mpl.variable_type.bool.value, False)     
                    if bparam == True:
                        if MarkSilentLogger == True:
                            bShow = False
                            silentLogger[str(threadNumber)] = messages
                            DiffMinSecondsSilentLogger_forUpdate, \
                            bparam = mpl.kwargs().getValueAllowed(kwargs,'_argDiffMinSecondsSilentLogger_forUpdate',mpl.variable_type.float, 2.0)
                            if f"'{str('float')}'" in str(type(kwargs.get(str('_argDiffMinSecondsSilentLogger_forUpdate')))):
                                print("CHECKING . . . YES FLOAT TYPE")
                            if bparam == True:
                                diffRlogger = float(diffRange_logger(cT7(),_argThreadNumber = threadNumber))
                                if diffRlogger >= float(DiffMinSecondsSilentLogger_forUpdate):
                                    print("CHECKING . . .OK")
                                    bAirtableReact = True

        # idAirtable='';threadNumber = const_thread.number_1.value
        # if '_argThreadNumber' in kwargs:
        #     threadNumber = kwargs.get("_argThreadNumber") 
        #     if "'int'" in str(type(threadNumber)):
        #         idAirtable = None
        #         if '_argIdAirtable' in kwargs:
        #             idAirtable = kwargs.get("_argIdAirtable") 
        #             if not '_argMarkSilentLogger' in kwargs and not '_argDiffMinSecondsSilentLogger_forUpdate':
        #                 if str(idAirtable).strip()!='':
        #                     bAirtableReact = True
        #             else:
        #                 MarkSilentLogger = kwargs.get("_argMarkSilentLogger")
        #                 DiffMinSecondsSilentLogger_forUpdate = kwargs.get("_argDiffMinSecondsSilentLogger_forUpdate")
        #                 if "'bool'" in str(type(MarkSilentLogger)):
        #                     bShow = False
        #                     silentLogger[str(threadNumber)] = messages
        #                     if MarkSilentLogger==True:
        #                         diffRlogger = diffRange_logger(cT7(),_argThreadNumber = threadNumber)
        #                         if diffRlogger >= float(DiffMinSecondsSilentLogger_forUpdate):
        #                             bAirtableReact = True

        if bShow == True: print(_time,messages)

        # print('    [ Ready for update airtable, if condition arguments for config airtable is set. ]')
        if bAirtableReact == True: aCls.pyairtable_updateDateTime_CurrentNumberLastOfLog(threadNumber,idAirtable)
    except ValueError:
        pass


# ##Only for testing
# import time
# import random

# # for i in range(1,5):
# #     diffRange_logger(cT7(),_argThreadNumber=1)
# #     time.sleep(2)

# for i in range(1,55):
#     THREADNUMBER = 1
#     random_decimal = random.randint(155, 580)/100

#     msgSilentLogger = ''
#     if str(THREADNUMBER)in silentLogger:
#         msgSilentLogger = silentLogger[str(THREADNUMBER)]
#     print("---> check message from silentLogger :",msgSilentLogger )

#     loggerV2(cT7(),'Hello World!', _argMarkSilentLogger=True, _argDiffMinSecondsSilentLogger_forUpdate = 5, _argThreadNumber=THREADNUMBER, _argIdAirtable='recdObiUDW8KsxW2w')
#     # Q.loggerV2(time7.currentTime7(),'Hello World!', _argMarkSilentLogger=True, _argDiffMinSecondsSilentLogger_forUpdate = 5, _argThreadNumber=THREADNUMBER, _argIdAirtable='recdObiUDW8KsxW2w')

#     time.sleep(random_decimal)
#     # time.sleep(4)
#     print('')