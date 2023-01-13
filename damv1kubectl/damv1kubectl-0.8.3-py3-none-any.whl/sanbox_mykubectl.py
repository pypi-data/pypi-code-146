import damv1env as env
import damv1time7 as time7
import damv1time7.mylogger as Q
import damv1myparamikossh as prmko
import damv1manipulation as mpl

import re
from enum import Enum

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Depricated
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# class strcommandpods(Enum):
#     command_for_name_sort_by_ascending = f'''kubectl get pods -n {{ns}} --no-headers'''
#     command_for_name_sort_by_descending = f'''kubectl get pods -n {{ns}} --no-headers | sort --key 1 --reverse'''
#     command_for_status_sort_by_ascending = f'''kubectl get pods -n {{ns}} --no-headers | sort --key 3'''
#     command_for_restart_sort_by_descending = f'''kubectl get pods -n {{ns}} --no-headers | sort --key 4 --numeric --reverse'''
#     command_for_age_created_sort_by_ascending = f'''kubectl get pods -n {{ns}} --no-headers --sort-by=.metadata.creationTimestamp'''
#     command_for_age_start_sort_by_ascending = f'''kubectl get pods -n {{ns}} --no-headers --sort-by=.status.startTime'''
class sanbox():
    dtFormated = '%Y-%m-%dT%H:%M:%SZ'
    # changes this for sandbox / production (  コンフィギュレーション )
    SRV_HOST = env.sandbox_srv.host.value
    SRV_USERNAME = env.sandbox_srv.username.value
    SRV_PORT = env.sandbox_srv.port.value
    SRV_PRIVATEKEY = env.sandbox_srv.privatekey.value

    def execsshcmd(self, _strcmd):
        oput = None # イニシャライズ
        try:
            if _strcmd.strip():
                oput = prmko.sshcommand(self.SRV_HOST, self.SRV_USERNAME, self.SRV_PORT, self.SRV_PRIVATEKEY, _strcmd, False)
        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "execsshcmd"')  
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
        return oput  

    def execsshcmd_detail_v2(self, _strcmd):
        oput = None # イニシャライズ
        bStatus_complete = False
        exception_message_handler = ''
        try:
            if _strcmd.strip():
                oput = prmko.sshcommand(self.SRV_HOST, self.SRV_USERNAME, self.SRV_PORT, self.SRV_PRIVATEKEY, _strcmd, False)
                bStatus_complete = True
        except Exception as e:
            exception_message_handler = str(e)
            Q.logger(time7.currentTime7(),'Fail of function "execsshcmd_detail_v2"')  
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
        return bStatus_complete, exception_message_handler, oput  


    def strCurrentTime_formatedPods_fromServer(self):
        outstr = self.execsshcmd('date +"{0}"'.format(self.dtFormated))
        lenofstr = len(outstr)
        value_line = str(outstr[0][0:lenofstr-2])
        return value_line

    def ageContainer_byCurrentTimeFromServer(self, _startedAt):
        age = time7.difference_datetime_by_dHMS_from_between(str(_startedAt), self.strCurrentTime_formatedPods_fromServer(), self.dtFormated)
        return age

    def filter_dict_iPodC_the_get_unique_dicts(self, _origin_dict, _lst_target):
        list_of_unique_dicts = []
        if len(_origin_dict)!=0:
            basket = []
            if len(_lst_target)!=0:
                for line_json_pods_inf in _origin_dict:
                    if len(_lst_target) !=0:
                        for target in _lst_target:
                            re_target = re.compile(r"({})".format(target), flags=re.IGNORECASE)
                            if re.search(re_target, str(line_json_pods_inf)):
                                basket.append(line_json_pods_inf)
            else: basket = _origin_dict
            list_of_unique_dicts = {x['pod']:x for x in basket}.values()
        return list(list_of_unique_dicts)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Depricated
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # def getLst_info_allPods_by_ns(self, _ns, OptSortCmd = strcommandpods.command_for_name_sort_by_ascending._value_):
    #     lst_po = [] # イニシャライズ
    #     try:
    #         query = OptSortCmd.format(ns = _ns) # クエリ
    #         cmd_gtpo = "{0} | awk {{'{1}'}} | column -t".format(query,'print $1"|"$3"|"$4"|"$5$6')
    #         lst_ipo = self.execsshcmd(cmd_gtpo)
    #         if len(lst_ipo)!=0:
    #             fdRow={}
    #             for row in lst_ipo:
    #                 sp_ipo = row.split('|')
    #                 fdRow = {   'name':sp_ipo[0],
    #                             'status':sp_ipo[1],
    #                             'restart':sp_ipo[2],
    #                             'age':sp_ipo[3] }
    #                 lst_po.append(fdRow)
    #     except Exception as e:
    #         Q.logger(time7.currentTime7(),'Fail of function "getLst_info_allPods_by_ns"')  
    #         Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
    #     return lst_po

## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## Januari 6, 2023
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def generate_json_from_lstInfoPods(self, _lst_ipoC):
        data = []
        try:
            if len(_lst_ipoC)!=0:
                for iPo in _lst_ipoC:
                    line = str(iPo).strip().removesuffix('\n')
                    lst_line = line.split('||')
                    data_line = {}
                    for idx, inf in enumerate(lst_line):
                        if inf.strip()!='':
                            if idx == 0: # info for pod
                                lst_infpod = inf.strip('][').split(', ')
                                if "'list'" in str(type(lst_infpod)):
                                    data_line['pod'] = str(lst_infpod[0])
                                    data_line['namespace'] = str(lst_infpod[1])
                            if idx == 1: # info for containers
                                dict_container = []
                                lst_line_container = inf.split('|')
                                for line_container in lst_line_container:
                                    if line_container.strip()!='':
                                        data_line_container = {}
                                        lst_infcontainer =  line_container.strip('][').split(', ')
                                        data_line_container['name']= lst_infcontainer[0]
                                        data_line_container['restart'] = str(lst_infcontainer[1])
                                        data_line_container['started'] = lst_infcontainer[2]
                                        data_line_container['stateStartedAt'] = lst_infcontainer[3]
                                        data_line_container['stateReason'] = lst_infcontainer[4]
                                        data_line_container['exitCode'] = lst_infcontainer[5]
                                        data_line_container['lastStateReason'] = lst_infcontainer[6]
                                        data_line_container['lastStateStartedAt'] = lst_infcontainer[7]
                                        data_line_container['lastStateFinishedAt'] = lst_infcontainer[8]
                                        dict_container.append(data_line_container)
                                data_line['containers'] = dict_container
                    if len(data_line)>0:
                        data.append(data_line)
        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "generate_json_from_lstInfoPods"')  
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
        return data

    def getLst_info_singlePods_by_podname_ns_v2(self, _podname, _ns, _bShowCommandGtPoC=False):
        lst_ipoC = []
        try:
            str_jsonpath =  '{"["}{.metadata.name}{", "}{.metadata.namespace}{"]||"}'\
                            '{range .status.containerStatuses[*]}{"["}'\
                            '{.name}{", "}{.restartCount}{", "}{.started}{", "}{.state.running.startedAt}{", "}{.state.waiting.reason}{", "}{.lastState.terminated.exitCode}{", "}{.lastState.terminated.reason}{", "}{.lastState.terminated.startedAt}{", "}{.lastState.terminated.finishedAt}{"]|"}'\
                            '{end}'

            cmd_gtPoC = "kubectl get pods {podname} -n {ns} -o jsonpath='{c_jsonpath}' --sort-by=.metadata.name".format(podname =  _podname, ns = _ns, c_jsonpath = str_jsonpath)
            if _bShowCommandGtPoC==True: print(cmd_gtPoC)
            raw_datas = self.execsshcmd(cmd_gtPoC)
            if raw_datas==None:
                raise Exception('Please check your connection and try again [Fail of function "execsshcmd"]')
            else: lst_ipoC = raw_datas
        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "getLst_info_singlePods_by_podname_ns_v2"')  
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
        return self.generate_json_from_lstInfoPods(lst_ipoC)

    def getLst_info_allPods_by_ns_v2(self, _ns, _bShowCommandGtPoC=False):
        lst_ipoC = []
        try:
            str_jsonpath =  '{range .items[*]}{"\\n["}{.metadata.name}{", "}{.metadata.namespace}{"]||"}'\
                            '{range .status.containerStatuses[*]}{"["}'\
                            '{.name}{", "}{.restartCount}{", "}{.started}{", "}{.state.running.startedAt}{", "}{.state.waiting.reason}{", "}{.lastState.terminated.exitCode}{", "}{.lastState.terminated.reason}{", "}{.lastState.terminated.startedAt}{", "}{.lastState.terminated.finishedAt}{"]|"}'\
                            '{end}{end}'

            # cmd_gtPoC = "kubectl get pods -n {ns} -o jsonpath='{c_jsonpath}' --sort-by=.metadata.name | sort -r".format(ns = _ns, c_jsonpath = str_jsonpath)
            cmd_gtPoC = "kubectl get pods -n {ns} -o jsonpath='{c_jsonpath}' --sort-by=.metadata.name".format(ns = _ns, c_jsonpath = str_jsonpath)
            if _bShowCommandGtPoC==True: print(cmd_gtPoC)
            raw_datas = self.execsshcmd(cmd_gtPoC)
            if raw_datas==None:
                raise Exception('Please check your connection and try again [Fail of function "execsshcmd"]')
            else: lst_ipoC = raw_datas
        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "getLst_info_allPods_by_ns_v2"')  
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
        return self.generate_json_from_lstInfoPods(lst_ipoC)

    def trans_infParentContainer(self, _idx, _pod):
        try:
            Pod_idx = _idx    
            Pod_name = _pod['pod']
            Pod_namespace = _pod['namespace']
            Dict_cont = _pod['containers']   
        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "trans_infParentContainer"')  
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
        return Pod_idx, Pod_name, Pod_namespace, Dict_cont 

    def getStatus_singlePods(self, _podname, _ns):
        oput = ''
        try:
            cmd = f'''kubectl get pods {{podname}} -n {{ns}} --no-headers'''
            query = cmd.format( podname = _podname, ns = _ns) # クエリ
            formated = "{0} | awk {{'{1}'}} | column -t".format(query,'print $3')
            lst_oput = self.execsshcmd(formated)
            if len(lst_oput)!=0:
                oput = str(lst_oput[0]).removesuffix('\n')
        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "getStatus_singlePods"')  
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
        return oput  

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Depricated
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # def trans_infAllContainer(self, _cont):
    #     Cont_name = ''; Cont_restart = ''; Cont_started = ''; Cont_stateStartedAt = ''
    #     Cont_exitCode = ''; Cont_stateReason = ''
    #     Cont_lastStateReason = '';  Cont_lastStateStartedAt = ''; Cont_lastStateFinishedAt = ''
    #     Cont_STATUS = ''; Cont_REASON = ''; Cont_AGE = ''
    #     try:
    #         Cont_name = _cont['name']
    #         Cont_restart = _cont['restart']
    #         Cont_started = _cont['started']
    #         Cont_stateStartedAt = _cont['stateStartedAt']
    #         Cont_exitCode = _cont['exitCode']
    #         Cont_stateReason = _cont['stateReason']
    #         Cont_lastStateReason = _cont['lastStateReason']
    #         Cont_lastStateStartedAt = _cont['lastStateStartedAt']
    #         Cont_lastStateFinishedAt = _cont['lastStateFinishedAt']

    #         if bool(Cont_started) == True and str(Cont_stateStartedAt).strip()!='': Cont_STATUS = 'Running'
    #         else: Cont_STATUS = Cont_stateReason

    #         if str(Cont_exitCode).strip()!='' and str(Cont_stateReason).strip()!='':
    #             Cont_REASON = '{0} - exit code: {1}'.format(str(Cont_stateReason), str(Cont_exitCode))
    #         else: Cont_REASON = ''

    #         if int(Cont_restart)==0 and bool(Cont_started)==True:
    #             if str(Cont_stateStartedAt).strip()!='':
    #                 Cont_AGE = '{0}'.format(self.ageContainer_byCurrentTimeFromServer(Cont_stateStartedAt))
    #         else: 
    #             if str(Cont_stateStartedAt).strip()!='':
    #                 Cont_AGE = '({0})'.format(self.ageContainer_byCurrentTimeFromServer(Cont_stateStartedAt))
    #             else: Cont_AGE = '({0})'.format(self.ageContainer_byCurrentTimeFromServer(Cont_lastStateFinishedAt))
    #     except Exception as e:
    #         Q.logger(time7.currentTime7(),'Fail of function "trans_infAllContainer"')  
    #         Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
    #     return  Cont_name, Cont_restart, Cont_started, Cont_stateStartedAt, Cont_exitCode, Cont_stateReason, \
    #             Cont_lastStateReason, Cont_lastStateStartedAt, Cont_lastStateFinishedAt, \
    #             Cont_STATUS, Cont_REASON, Cont_AGE

    def trans_infAllContainer_v2(self, _cont):
        Cont_name = ''; Cont_restart = ''; Cont_started = ''; Cont_stateStartedAt = ''
        Cont_exitCode = ''; Cont_stateReason = ''
        Cont_lastStateReason = '';  Cont_lastStateStartedAt = ''; Cont_lastStateFinishedAt = ''
        Cont_STATUS = ''; Cont_REASON = ''; Cont_AGE = ''
        bStatus_complete = False
        exception_message_handler = ''        
        try:
            Cont_name = _cont['name']
            Cont_restart = _cont['restart']
            Cont_started = _cont['started']
            Cont_stateStartedAt = _cont['stateStartedAt']
            Cont_exitCode = _cont['exitCode']
            Cont_stateReason = _cont['stateReason']
            Cont_lastStateReason = _cont['lastStateReason']
            Cont_lastStateStartedAt = _cont['lastStateStartedAt']
            Cont_lastStateFinishedAt = _cont['lastStateFinishedAt']

            if bool(Cont_started) == True and str(Cont_stateStartedAt).strip()!='': Cont_STATUS = 'Running'
            else: Cont_STATUS = Cont_stateReason

            if str(Cont_exitCode).strip()!='' and str(Cont_stateReason).strip()!='':
                Cont_REASON = '{0} - exit code: {1}'.format(str(Cont_stateReason), str(Cont_exitCode))
            else: Cont_REASON = ''

            if int(Cont_restart)==0 and bool(Cont_started)==True:
                if str(Cont_stateStartedAt).strip()!='':
                    Cont_AGE = '{0}'.format(self.ageContainer_byCurrentTimeFromServer(Cont_stateStartedAt))
            else: 
                if str(Cont_stateStartedAt).strip()!='':
                    Cont_AGE = '({0})'.format(self.ageContainer_byCurrentTimeFromServer(Cont_stateStartedAt))
                else: Cont_AGE = '({0})'.format(self.ageContainer_byCurrentTimeFromServer(Cont_lastStateFinishedAt))
            bStatus_complete = True
        except Exception as e:
            exception_message_handler = str(e)
            Q.logger(time7.currentTime7(),'Fail of function "trans_infAllContainer"')  
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
        return  bStatus_complete, exception_message_handler, \
                Cont_name, Cont_restart, Cont_started, Cont_stateStartedAt, Cont_exitCode, Cont_stateReason, \
                Cont_lastStateReason, Cont_lastStateStartedAt, Cont_lastStateFinishedAt, \
                Cont_STATUS, Cont_REASON, Cont_AGE

    def printlf_infHeadPodContainers(self, _dict, _writeOnFile, _fullfilename, _showPrintlf):
        f = None
        try:
            if _showPrintlf == True:
                print(time7.currentTime7(),' '*12,"check length lst_pod :", str(len(_dict)))
                print(time7.currentTime7())

            f = None
            if _writeOnFile == True:
                f = open(_fullfilename, 'w')     
                f.write(time7.currentTime7() + ' '*12 + 'check len lst_pod :' + str(len(_dict)));f.write('\n')   
                f.write(time7.currentTime7());f.write('\n')   
        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "printlf_infHeadPodContainers"')  
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
        return f


    def printlf_infParentContainer(self, f, _writeOnFile, _showPrintlf, *args):
        try:
            if _writeOnFile == True:
                f.write(time7.currentTime7() +' '*12 + 'pod idx :' + str(args[0]));f.write('\n')
                f.write(time7.currentTime7() +' '*12 + 'pod name :' + str(args[1]));f.write('\n')
                f.write(time7.currentTime7() +' '*12 + 'pod namespace :' + str(args[2]));f.write('\n')
                f.write(time7.currentTime7() +' '*12 + 'pod containers count :' + str(len(args[3])));f.write('\n')

            if _showPrintlf == True:
                print(time7.currentTime7(),' '*12,'pod idx :', args[0])
                print(time7.currentTime7(),' '*12,'pod name :', args[1])
                print(time7.currentTime7(),' '*12,'pod namespace :', args[2])
                print(time7.currentTime7(),' '*12,'pod containers count :', len(args[3]))
        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "printlf_infParentContainer"')  
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))

    def printlf_infAllContainer(self, f, _writeOnFile, _showPrintlf, *args):
        try:
            if _writeOnFile == True:
                f.write(time7.currentTime7() +' '*13 + '-');f.write('\n')
                f.write(time7.currentTime7() +' '*12 + 'container name :' + args[0]);f.write('\n')
                f.write(time7.currentTime7() +' '*12 + 'container restart :' + args[1]);f.write('\n')
                f.write(time7.currentTime7() +' '*12 + 'container started :' + args[2]);f.write('\n')
                f.write(time7.currentTime7() +' '*12 + 'container stateStartedAt :' + args[3]);f.write('\n')
                f.write(time7.currentTime7() +' '*12 + 'container exitCode :' + args[4]);f.write('\n')
                f.write(time7.currentTime7() +' '*12 + 'container stateReason :' + args[5]);f.write('\n')
                f.write(time7.currentTime7() +' '*12 + 'container lastStateReason :' + args[6]);f.write('\n')
                f.write(time7.currentTime7() +' '*12 + 'container lastStateStartedAt :' + args[7]);f.write('\n')
                f.write(time7.currentTime7() +' '*12 + 'container lastStateFinishedAt :' + args[8]);f.write('\n')
                f.write(time7.currentTime7() +' '*12 + 'container STATUS :' + args[9]);f.write('\n')
                f.write(time7.currentTime7() +' '*12 + 'container REASON :' + args[10]);f.write('\n')
                f.write(time7.currentTime7() +' '*12 + 'container AGE :' + args[11]);f.write('\n')

            if _showPrintlf == True:
                print(time7.currentTime7(),' '*13 + '-')
                print(time7.currentTime7(),' '*12,'container name :', args[0])
                print(time7.currentTime7(),' '*12,'container restart :', args[1])
                print(time7.currentTime7(),' '*12,'container started :', args[2])
                print(time7.currentTime7(),' '*12,'container stateStartedAt :', args[3])
                print(time7.currentTime7(),' '*12,'container exitCode :', args[4])
                print(time7.currentTime7(),' '*12,'container stateReason :', args[5])
                print(time7.currentTime7(),' '*12,'container lastStateReason :', args[6])
                print(time7.currentTime7(),' '*12,'container lastStateStartedAt :', args[7])
                print(time7.currentTime7(),' '*12,'container lastStateFinishedAt :', args[8])
                print(time7.currentTime7(),' '*12,'container STATUS :', args[9])
                print(time7.currentTime7(),' '*12,'container REASON :', args[10])
                print(time7.currentTime7(),' '*12,'container AGE :', args[11])
        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "printlf_infAllContainer"')  
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))

    def printlf_infFooterPodContainers(self, f, _writeOnFile, _showPrintlf):
        try:
            if _writeOnFile == True:
                f.write(time7.currentTime7() + ' '*12 + '- '*42);f.write('\n')
            if _showPrintlf == True:
                print(time7.currentTime7(), ' '*12  + '- '*42)
        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "printlf_infFooterPodContainers"')  
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def execCmd_by_regex_strquery(self, _strcmd, target_str=[],**kwargs):
        oput = [] # イニシャライズ
        get_bStatus_complete_sshcmd = False
        get_exception_message_handler = ''
        try:
            idAirtable = ''; DiffMinSecondsSilentLogger_forUpdate = 0; threadNumber = 0; funct_pyairtable_update, \
            bparam = mpl.kwargs().getValueAllowed(kwargs, '_argFunctAirtable_update', mpl.variable_type.method.value, None) 
            if bparam==True:
                threadNumber, \
                bparam = mpl.kwargs().getValueAllowed(kwargs,'_argThreadNumber',mpl.variable_type.int.value, 0)
                if bparam==True:
                    idAirtable, \
                    bparam = mpl.kwargs().getValueAllowed(kwargs,'_argIdAirtable',mpl.variable_type.str.value, None)
                    if bparam==True: 
                        DiffMinSecondsSilentLogger_forUpdate, \
                        bparam = mpl.kwargs().getValueAllowed(kwargs,'_argDiffMinSecondsSilentLogger_forUpdate',mpl.variable_type.float.value,0)

            if _strcmd.strip():
                if len(target_str) !=0:
                    for target in target_str:
                        print('\r{0}              Scanning target regex '.format(time7.currentTime7()), end='')

                        if str(threadNumber).strip()!= '' and str(idAirtable).strip() != '' and float(DiffMinSecondsSilentLogger_forUpdate) != 0:
                            Q.logger(time7.currentTime7(),'', _argMarkSilentLogger=True, \
                                                              _argFunctAirtable_update = funct_pyairtable_update, \
                                                              _argThreadNumber=threadNumber, _argIdAirtable=idAirtable, \
                                                              _argDiffMinSecondsSilentLogger_forUpdate = DiffMinSecondsSilentLogger_forUpdate)
                        # SCANNING TARGET LAYER 2    
                        re_target = re.compile(r"({})".format(target), flags=re.IGNORECASE)
                        if re.search(re_target, _strcmd):
                            get_bStatus_complete_sshcmd, get_exception_message_handler, oput = self.execsshcmd_detail_v2(_strcmd) #  specific objects スペシャルオブジェクト
                else:
                    print('\r{0}              Scanning target regex '.format(time7.currentTime7()), end='')

                    if str(threadNumber).strip()!= '' and str(idAirtable).strip() != '' and float(DiffMinSecondsSilentLogger_forUpdate) != 0:
                        Q.logger(time7.currentTime7(),'', _argMarkSilentLogger=True, \
                                                          _argFunctAirtable_update = funct_pyairtable_update, \
                                                          _argThreadNumber=threadNumber, _argIdAirtable=idAirtable, \
                                                          _argDiffMinSecondsSilentLogger_forUpdate = DiffMinSecondsSilentLogger_forUpdate)

                    get_bStatus_complete_sshcmd, get_exception_message_handler, oput = self.execsshcmd_detail_v2(_strcmd) # all objects すべてオブジェクト
        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "execCmd_by_regex_strquery"')  
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
        return get_bStatus_complete_sshcmd, get_exception_message_handler, oput 
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Depricated
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # def getLst_log_pod_by_pattern_andTarget(self, _sincelast, _pod, _namespace, _pattern, _lst_target, **kwargs):
    #     lst_oput = [] # イニシャライズ
    #     # threadNumber = 0
    #     # idAirtable = None
    #     # DiffMinSecondsSilentLogger_forUpdate = 0
    #     # showCommandkubectl=False
    #     try:
    #         idAirtable = None; DiffMinSecondsSilentLogger_forUpdate = 0; threadNumber, \
    #         bparam = mpl.kwargs().getValueAllowed(kwargs,'_argThreadNumber',mpl.variable_type.int.value, 0)
    #         if bparam==True:
    #             idAirtable, \
    #             bparam = mpl.kwargs().getValueAllowed(kwargs,'_argIdAirtable',mpl.variable_type.str.value, None)
    #             if bparam==True: 
    #                 DiffMinSecondsSilentLogger_forUpdate, \
    #                 bparam = mpl.kwargs().getValueAllowed(kwargs,'_argDiffMinSecondsSilentLogger_forUpdate',mpl.variable_type.int.value,0)
    #         # if '_argThreadNumber' in kwargs:
    #         #     if "'int'" in str(type(threadNumber)):
    #         #         threadNumber = kwargs.get("_argThreadNumber") 
    #         #         if '_argIdAirtable' in kwargs:
    #         #             idAirtable = kwargs.get("_argIdAirtable") 
    #         #             if '_argDiffMinSecondsSilentLogger_forUpdate' in kwargs:
    #         #                 DiffMinSecondsSilentLogger_forUpdate = int(kwargs.get("_argDiffMinSecondsSilentLogger_forUpdate"))


    #         showCommandkubectl, \
    #         bparam = mpl.kwargs().getValueAllowed(kwargs,'_argShowCommandkubectl',mpl.variable_type.bool.value, False)
    #         # if '_argShowCommandkubectl' in kwargs:
    #         #     showCommandkubectl = kwargs.get("_argShowCommandkubectl")

    #         # Notes :
    #         # Regular Expression or sed for remove 'ANSI escape sequence' = sed -r "s/\x1b\[[^@-~]*[@-~]//g"     
    #         query = r'kubectl logs --since={0} --timestamps=true {1} -n {2} | sed -r "s/\x1b\[[0-9;]*m//g" | grep "{3}" | sort -k2 -r | head -n 1'.format(\
    #                 _sincelast,_pod,_namespace,_pattern)
    #         if showCommandkubectl == True: Q.logger(time7.currentTime7(),query) # for show command kubectl
    #         lst_oput = self.execCmd_by_regex_strquery(query, _lst_target, _argDiffMinSecondsSilentLogger_forUpdate = DiffMinSecondsSilentLogger_forUpdate, \
    #                                 _argThreadNumber=threadNumber, _argIdAirtable=idAirtable)
    #     except Exception as e:
    #         Q.logger(time7.currentTime7(),'Fail of function "getLst_log_pod_by_pattern_andTarget"')  
    #         Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
    #     return lst_oput 


## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## Januari 6, 2023
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def getLst_log_pod_by_pattern_andTarget_v2(self, _sincelast, _pod, _container, _namespace, _pattern, _lst_target, **kwargs):
        lst_oput = [] # イニシャライズ
        get_bStatus_complete_sshcmd = False
        get_exception_message_handler = ''
        try:
            idAirtable = ''; DiffMinSecondsSilentLogger_forUpdate = 0; threadNumber = 0; funct_pyairtable_update, \
            bparam = mpl.kwargs().getValueAllowed(kwargs, '_argFunctAirtable_update', mpl.variable_type.method.value, None) 
            if bparam==True:
                threadNumber , \
                bparam = mpl.kwargs().getValueAllowed(kwargs,'_argThreadNumber',mpl.variable_type.int.value, 0)
                if bparam==True:
                    idAirtable, \
                    bparam = mpl.kwargs().getValueAllowed(kwargs,'_argIdAirtable',mpl.variable_type.str.value, None)
                    if bparam==True: 
                        DiffMinSecondsSilentLogger_forUpdate, \
                        bparam = mpl.kwargs().getValueAllowed(kwargs,'_argDiffMinSecondsSilentLogger_forUpdate',mpl.variable_type.float.value,0)

            showCommandkubectl, \
            bparam = mpl.kwargs().getValueAllowed(kwargs,'_argShowCommandkubectl',mpl.variable_type.bool.value, False)

            # Notes :
            # Regular Expression or sed for remove 'ANSI escape sequence' = sed -r "s/\x1b\[[^@-~]*[@-~]//g"     
            query = r'kubectl logs --since={0} --timestamps=true {1} -c {2} -n {3} | sed -r "s/\x1b\[[0-9;]*m//g" | grep "{4}" | sort -k2 -r | head -n 1'.format(\
                    _sincelast, _pod, _container, _namespace, _pattern)

            # if showCommandkubectl == True: Q.logger(time7.currentTime7(),query) # for show command kubectl
            if showCommandkubectl == True: Q.logger(time7.currentTime7(),'\n' + query) # for show command kubectl

            if str(threadNumber).strip()!= '' and str(idAirtable).strip() != '' and float(DiffMinSecondsSilentLogger_forUpdate) != 0:
                get_bStatus_complete_sshcmd, get_exception_message_handler, lst_oput = self.execCmd_by_regex_strquery(  query, _lst_target, \
                                                                                        _argFunctAirtable_update = funct_pyairtable_update, \
                                                                                        _argThreadNumber=threadNumber, _argIdAirtable=idAirtable, \
                                                                                        _argDiffMinSecondsSilentLogger_forUpdate = DiffMinSecondsSilentLogger_forUpdate )
            else: get_bStatus_complete_sshcmd, get_exception_message_handler, lst_oput = self.execCmd_by_regex_strquery(  query, _lst_target )

        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "getLst_log_pod_by_pattern_andTarget_v2"')  
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
        return get_bStatus_complete_sshcmd, get_exception_message_handler, lst_oput 
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -








# # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ## uncomments this bellow for testing only ( テスティング ) !
# # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# f = sanbox()
# def excute(_ns):
#     lst_po = []
#     Q.logger(time7.currentTime7(),'Begin ( はじまり )')
#     Q.logger(time7.currentTime7(),'(1) - Loading Process ( ローディング )')
#     lst_po = f.getLst_info_allPods_by_ns('sit')
#     print(lst_po)

# excute('sit')