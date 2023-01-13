import json

# ------- reborn packages --------------
# import damv1env as env
import damv1time7 as time7
import damv1time7.mylogger as Q
import damv1airtableprojectk8salert as airtblk8salert
# --------------------------------------
aCls = airtblk8salert.production()
uCls = airtblk8salert.utils()

class production():
    def execution(self, _funct_k8salert):
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
