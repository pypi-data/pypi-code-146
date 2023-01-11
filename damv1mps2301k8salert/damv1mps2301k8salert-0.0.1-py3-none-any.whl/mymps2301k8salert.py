import json

# ------- reborn packages --------------
# import damv1env as env
import damv1time7 as time7
import damv1time7.mylogger as Q
# import damv1kubectl as dkube
# import damv1manipulation as mpl
# import damv1templateprojectk8salert as tmpltk8salert
# import damv1evernoteprojectk8salert as evrnotek8salert
# import damv1telegramprojectk8salert as telegk8salert
import damv1airtableprojectk8salert as airtblk8salert
# --------------------------------------

# fCls = dkube.sanbox()
# tCls = tmpltk8salert.displayed
# eCls = evrnotek8salert.sanbox()
# eCls_u = evrnotek8salert.utils()
# mCls = telegk8salert.sanbox()
aCls = airtblk8salert.sandbox()
uCls = airtblk8salert.utils()

def execution(_funct_k8salert):
    MaxThread = 3
    MaxSecondsTimeLogsWaiting = 7200 # seconds, for next thread delimiter processing [from start_data to last_of_log_N] | saran : ambil waktu maksimum dari setiap workflow
    MinSecondsSilentLogger = 2.8 # seconds
    # skenario 1
    Q.logger(time7.currentTime7(),'')
    Q.logger(time7.currentTime7(),'(1) - Airtable Load All by Enable ( ローディング )')
    data = aCls.pyairtable_loadAll_by_enable_ColParams(True)
    lst_data = uCls.convert_airtableDict_to_dictionary(data)
    uCls.view_dictionary(lst_data)
    ## skenario 2
    if len(lst_data)!=0:
        ## skenario 3
        aCls.pyairtable_detectCrashProcess_then_recovery(lst_data, _argMaxThread = MaxThread, \
                    _argMaxSecondsTimeLogsWaiting = MaxSecondsTimeLogsWaiting, \
                    _argDiffMinSecondsSilentLogger_forUpdate = MinSecondsSilentLogger)
        ## skenario 4
        Q.logger(time7.currentTime7(),'')
        Q.logger(time7.currentTime7(),'[ Ready ]')
        Q.logger(time7.currentTime7(),'(2) - Processing')
        for idx, r in  enumerate(lst_data):
            r_id = uCls.escape_dict(r,'id')
            r_name = uCls.escape_dict(r,'name')
            r_title = uCls.escape_dict(r,'title')
            r_type = uCls.escape_dict(r,'type')
            r_ns = uCls.escape_dict(r,'ns')
            r_targets = uCls.escape_dict(r,'target contains')
            r_patterns = uCls.escape_dict(r,'patterns')
            r_Enable = uCls.escape_dict(r,'Enable')
            r_excmethod = uCls.escape_dict(r,'exec method')
            number = idx + 1
            lst_patterns = json.loads(r_patterns)
            lst_targets = json.loads(r_targets)
            ## skenario 5
            if airtblk8salert.const_type.log.value in r_type:
                ## skenario 6
                IntCipNow = aCls.pyairtable_getIntCip_now(r_id, _argMaxThread = MaxThread)
                if int(IntCipNow)>=int(MaxThread):
                    Q.logger(time7.currentTime7(),f'      Terminated process of number-{str(number)} : cip available must be less than', str(MaxThread),"!")
                else:
                    ## skenario 7
                    first_thread = aCls.pyairtable_getFields_FirstThreadNumberAvailable(r_id)
                    if len(first_thread)!=0:
                        ## skenario 8
                        aCls.pyairtable_update_StartEnd_process(r_id, r_name, r_Enable, airtblk8salert.const_process.start.value, _argMaxThread = MaxThread)
                        ## skenario 9
                        thread = first_thread['first value'] # GET NUMBER OF THREAD AVAILABLE
                        ## skenario 10 | first event update lastoflog
                        aCls.pyairtable_threadUpdate_lastoflog(r_id,int(thread),time7.currentTime7(), _argMaxThread = MaxThread)
                        ## skenario 11
                        ## * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
                        count_detected_object, \
                        url_shareable_evernotes = _funct_k8salert\
                        (    number, r_title, r_ns, airtblk8salert.const_sincelast.h24.value, lst_patterns, lst_targets, \
                            _argThreadNumber = int(thread), _argIdAirtable = str(r_id), \
                            _argDiffMinSecondsSilentLogger_forUpdate = MinSecondsSilentLogger
                        ) 
                        ## * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
                        Q.logger('{0}'.format(str(time7.currentTime7())),'')
                        ## skenario 12
                        aCls.pyairtable_append_detected_and_report_process(r_id, r_name, r_Enable, count_detected_object,url_shareable_evernotes)
                        ## skenario 13
                        aCls.pyairtable_update_StartEnd_process(r_id, r_name, r_Enable, airtblk8salert.const_process.end.value, _argMaxThread = MaxThread)
                        ## skenario 14
                        aCls.pyairtable_update_clearOneSelection_lastoflog(r_id,int(thread),_argMaxThread = MaxThread)
                        if number< len(lst_data): 
                            Q.logger(time7.currentTime7(),'      Next process')
                        elif number >= len(lst_data):
                            Q.logger(time7.currentTime7(),'      End process')
    else:
        Q.logger(time7.currentTime7(),'[ Not Ready ]')
    Q.logger(time7.currentTime7(),'All Done, tank you ( ありがとう )')
    Q.logger(time7.currentTime7(),'Copyright ( はんけん ) : ( DAM ) Dhony Abu Muhammad @Jan2023 ')