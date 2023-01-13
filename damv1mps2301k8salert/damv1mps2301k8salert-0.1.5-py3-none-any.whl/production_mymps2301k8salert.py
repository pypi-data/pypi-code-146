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
