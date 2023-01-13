import html
import json
import sys

# ------- reborn packages --------------
import damv1env as env
import damv1time7 as time7
import damv1time7.mylogger as Q
import damv1kubectl as dkube
import damv1manipulation as mpl
import damv1templateprojectk8salert as tmpltk8salert
import damv1evernoteprojectk8salert as evrnotek8salert
import damv1telegramprojectk8salert as telegk8salert
# --------------------------------------

fCls = dkube.production()
tCls = tmpltk8salert.displayed
eCls = evrnotek8salert.sanbox()
eCls_u = evrnotek8salert.utils()
mCls = telegk8salert.production()


def execution( _number, _nameof_msg_rpt, _namespace, _sincelast, _lst_patterns, _lst_target=[], **kwargs):
    ALLOW_PARAM= False
    bAirtableReact = False
    bShowPrintlf_process_A1 = False
    bWriteDump_process_A1 = True
    bShowCommand_for_getAllInfoPods = False
    bShowCommand_for_getLogInPodsContainer = False
    # --
    count_detected_object = 0
    url_shareable_evernotes = ''

    if int(_number)!= 0 and str(_nameof_msg_rpt).strip()!='' and str(_namespace).strip()!='' and  str(_sincelast).strip()!='' and \
        'list' in str(type(_lst_patterns)) and len(_lst_patterns)!=0 and 'list' in str(type(_lst_target)):
        ALLOW_PARAM = True

    idAirtable=''; threadNumber=0; DiffMinSecondsSilentLogger_forUpdate=0; funct_pyairtable_update, \
    bparam = mpl.kwargs().getValueAllowed(kwargs, '_argFunctAirtable_update', mpl.variable_type.method.value, None)   
    if bparam==True:
        threadNumber, \
        bparam = mpl.kwargs().getValueAllowed(kwargs,'_argThreadNumber',mpl.variable_type.int.value, 0)
        if bparam==True:
            idAirtable, \
            bparam = mpl.kwargs().getValueAllowed(kwargs,'_argIdAirtable',mpl.variable_type.str.value, None)
            if bparam==True: 
                bAirtableReact = True
                DiffMinSecondsSilentLogger_forUpdate, \
                bparam = mpl.kwargs().getValueAllowed(kwargs,'_argDiffMinSecondsSilentLogger_forUpdate',mpl.variable_type.float.value,0)

    if ALLOW_PARAM == True:
        Q.logger(time7.currentTime7(),'')
        Q.logger(time7.currentTime7(),'      [ Begin k8s_alert_release - {0} ] シミュレーション'.format(_number),  _argFunctAirtable_update = funct_pyairtable_update, \
                                                                                                                _argThreadNumber = threadNumber, \
                                                                                                                _argIdAirtable = idAirtable)
        Q.logger(time7.currentTime7(),'        Arguments (パラメタ値):')
        Q.logger(time7.currentTime7(),'         - name of message :', _nameof_msg_rpt)
        Q.logger(time7.currentTime7(),'         - namespace :', _namespace)
        Q.logger(time7.currentTime7(),'         - sincelast :', _sincelast)
        Q.logger(time7.currentTime7(),'         - patterns :', str(_lst_patterns))
        Q.logger(time7.currentTime7(),'         - targets :', str(_lst_target))
        Q.logger(time7.currentTime7(),'      ', '.'*83)

        ## LOADING PROCESS # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        DICT_RELEASE_PodC = []
        START_DATE_TIME7 = time7.currentTime7()
        Q.logger(time7.currentTime7(),'       (1) - Loading Process ( ローディング )', _argFunctAirtable_update = funct_pyairtable_update, \
                                                                                     _argThreadNumber = threadNumber, \
                                                                                     _argIdAirtable = idAirtable)

        # skenario 1 :: [condition used AIRTABLE] option 'type' project
        try: 
            dict_rawiPodC = []
            dict_rawiPodC = fCls.getLst_info_allPods_by_ns_v2(_namespace, bShowCommand_for_getAllInfoPods)
            dict_layer1Filter_PodC = fCls.filter_dict_iPodC_the_get_unique_dicts(dict_rawiPodC, _lst_target)
            dict_layer2Filter_PodC = mpl.listofdictionary().sorted_listOfDictionary_inChildRange(dict_layer1Filter_PodC,'containers','restart')
            DICT_RELEASE_PodC = dict_layer2Filter_PodC
        except Exception as e: Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
        ## START PROCESS # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Result :
        # - lst_grpline     --> for report in Evernote
        # - lst_dtect_obj   --> for message in Telegran
        outstr = [];lst_grplines = [];lst_line = [];number=0;lst_dtect_obj = [];lst_sshexecparamiko_failed = []
        if len(DICT_RELEASE_PodC) !=0 and len(_lst_patterns)!= 0:
            f = fCls.printlf_infHeadPodContainers(DICT_RELEASE_PodC, bWriteDump_process_A1, 'DUMP_PROCESS.txt', bShowPrintlf_process_A1)
            Q.logger(time7.currentTime7(),'       (2) - Start Process ( はじめる )', _argFunctAirtable_update = funct_pyairtable_update, \
                                                                                    _argThreadNumber = threadNumber, \
                                                                                    _argIdAirtable = idAirtable)
            try:
                for idx , pod in enumerate(DICT_RELEASE_PodC):
                    pod_idx, pod_name, pod_namespace, dict_cont = fCls.trans_infParentContainer(idx,pod)
                    fCls.printlf_infParentContainer(f, bWriteDump_process_A1, bShowPrintlf_process_A1, pod_idx, pod_name, pod_namespace, dict_cont) 
                    lst_line.clear()
                    if len(dict_cont)!=0:
                        for cont in dict_cont:
                            Cont_STATUS = ''
                            get_bStatus_complete_sshcmd = False; get_exception_message_handler = ''

                            get_bStatus_complete_sshcmd, get_exception_message_handler, \
                            cont_name, cont_restart, cont_started, cont_stateStartedAt, cont_exitCode, cont_stateReason, \
                            cont_lastStateReason, cont_lastStateStartedAt, cont_lastStateFinishedAt, \
                            cont_STATUS, cont_REASON, cont_AGE = fCls.trans_infAllContainer_v2(cont)

                            if get_bStatus_complete_sshcmd == True and str(Cont_STATUS).strip() == '': Cont_STATUS = f'({str(fCls.getStatus_singlePods(pod_name,pod_namespace))})'

                            fCls.printlf_infAllContainer(f, bWriteDump_process_A1, bShowPrintlf_process_A1, \
                            cont_name, cont_restart, cont_started, cont_stateStartedAt, cont_exitCode, cont_stateReason, \
                            cont_lastStateReason, cont_lastStateStartedAt, cont_lastStateFinishedAt, \
                            cont_STATUS, cont_REASON, cont_AGE)

                            if get_bStatus_complete_sshcmd == False:
                                failed = {}
                                failed.clear()
                                failed['identifier'] = f'{_namespace}::{pod_name}::{cont_name}'
                                failed['position'] = f'For Loop: {cont_name}' 
                                failed['message'] = get_exception_message_handler
                                lst_sshexecparamiko_failed.append(failed)
                            else: # If status execsshparamiko completed in function trans_infAllContainer
                                for pattern in _lst_patterns:
                                    pattern = pattern.strip()

                                    # skenario 2 :: [condition used AIRTABLE] option 'type' project

                                    get_bStatus_complete_sshcmd = False; get_exception_message_handler = ''
                                    if bAirtableReact == False:
                                        get_bStatus_complete_sshcmd, get_exception_message_handler, outstr = fCls.getLst_log_pod_by_pattern_andTarget_v2(   _sincelast, pod_name, cont_name, _namespace, pattern, _lst_target, \
                                                                                                _argShowCommandkubectl=bShowCommand_for_getLogInPodsContainer)                                    
                                    else:
                                        get_bStatus_complete_sshcmd, get_exception_message_handler, outstr = fCls.getLst_log_pod_by_pattern_andTarget_v2(   _sincelast,pod_name, cont_name, _namespace, pattern, _lst_target, \
                                                                                                _argDiffMinSecondsSilentLogger_forUpdate = DiffMinSecondsSilentLogger_forUpdate, \
                                                                                                _argFunctAirtable_update = funct_pyairtable_update, _argThreadNumber=threadNumber, _argIdAirtable=idAirtable, \
                                                                                                _argShowCommandkubectl=bShowCommand_for_getLogInPodsContainer)

                                    if get_bStatus_complete_sshcmd == False:
                                        failed = {}
                                        failed.clear()
                                        failed['identifier'] = f'{_namespace}::{pod_name}::{cont_name}'
                                        failed['position'] = f'For Loop: {pattern}' 
                                        failed['message'] = get_exception_message_handler
                                        lst_sshexecparamiko_failed.append(failed)

                                    if mpl.variable_type.list.value in str(type(outstr)):
                                        if len(outstr)!=0:
                                            lenofstr = len(outstr);value_line = str(outstr[0][2:lenofstr-2])
                                            # Clean lines :
                                            value_line = eCls_u.remove_ANSI_escape_sequence(value_line)
                                            lst_line.append(tCls.tmplt_evrntLines.value.format(\
                                                value_str_patterns = html.escape(pattern),\
                                                value_str_sincelast = html.escape(_sincelast),\
                                                value_str_line = html.escape(value_line)))

                                            Q.logger('\n{0}'.format(str(time7.currentTime7())),f'             Detect a ( 見つける ) {_namespace}::{pod_name} | {cont_name}', _argFunctAirtable_update = funct_pyairtable_update, \
                                                                                                                                                                            _argThreadNumber = threadNumber, \
                                                                                                                                                                            _argIdAirtable = idAirtable)
                                            Q.logger('{0}'.format(str(time7.currentTime7())),f'             --> pattern ( パタン ): "{pattern}"', _argFunctAirtable_update = funct_pyairtable_update, \
                                                                                                                                                 _argThreadNumber = threadNumber, 
                                                                                                                                                 _argIdAirtable = idAirtable)
                                        else:
                                            print('\r',end='')

                            if len(lst_line)!=0:
                                number+=1
                                if cont_STATUS=='Running':
                                    color_status = 'Green'
                                else: color_status = '#FF5733' # Orange Color
                                lst_grplines.append(tCls.tmplt_evrntgrpLines.value.format(\
                                    value_str_number = html.escape(str(number)),\
                                    value_str_ns = html.escape(_namespace), \
                                    value_str_po = html.escape(pod_name), \
                                    value_str_cont = html.escape(cont_name), \
                                    value_str_color_status = html.escape(color_status), \
                                    value_str_status = html.escape(cont_STATUS), \
                                    value_str_restart = html.escape(cont_restart), \
                                    value_str_age = html.escape(cont_AGE), \
                                    value_str_lstlines = ''.join(lst_line)))
                                Q.logger('{0}'.format(str(time7.currentTime7())),f'             ..[ Line ( ライン ) - {str(number)} : Done ( ダン ) ]',  _argFunctAirtable_update =  funct_pyairtable_update, \
                                                                                                                                                        _argThreadNumber = threadNumber, 
                                                                                                                                                        _argIdAirtable = idAirtable)
                                line_dtect_obj = tCls.tmplt_telemsg_str_dtect_obj.value.format(\
                                        value_str_obj = mpl.telegram.escape_strparse_markdownv1(pod_name + ' | ' + cont_name), \
                                        value_obj_restart = mpl.telegram.escape_strparse_markdownv1(cont_restart), \
                                        value_obj_age = mpl.telegram.escape_strparse_markdownv1(cont_AGE))
                                lst_dtect_obj.append(line_dtect_obj)
            except Exception as e:
              Q.logger(time7.currentTime7(),'           Error Handling ( エラー ):',str(e),_argThreadNumber = threadNumber, _argIdAirtable = idAirtable)

        ## REPORT OF THE PROCESS ABOVE #  - -- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  
        ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        Q.logger(time7.currentTime7())
        Q.logger(time7.currentTime7(), ' '*8,' *'*25)
        if len(lst_sshexecparamiko_failed)!=0: Q.logger(time7.currentTime7(), ' '*9, f'Check length lst_sshexecparamiko_failed : {str(len(lst_sshexecparamiko_failed))} .')
        else: Q.logger(time7.currentTime7(), ' '*9, 'No data availbale for the lst_sshexecparamiko_failed.')
        Q.logger(time7.currentTime7(), ' '*8,' *'*25)
        Q.logger(time7.currentTime7())
        ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        ## EVERNOTE INTEGRATING #  インテグレーテット - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  
        ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        evrnt_urlshareable = None
        if len(lst_grplines) != 0:
            nameof_msg_rpt = _nameof_msg_rpt.strip()
            contexid = str(time7.generate_uuids_byTime7())
            Q.logger('{0}'.format(str(time7.currentTime7())),'       (3) - Evernote integrating ( レポート )')
            try: evrnt_urlshareable = eCls.evernote_generate_report(contexid, nameof_msg_rpt, lst_grplines, tCls.tmplt_evrntwrapper.value)
            # try: evrnt_urlshareable = eCls.evernote_generate_report(contexid, nameof_msg_rpt, lst_grplines, tCls.tmplt_evrntwrapper.value, \
            #                             _argShowErrorExplain=True)
            except Exception as e: Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))

        ## TELEGRAM INTEGRATING #  インテグレーテット - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  
        ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        if len(lst_dtect_obj)!=0:
            Q.logger(time7.currentTime7(),'       (4) - Telegram integrating ( メッセージ )')
            dtect_obj = '\n  \-\| '.join(lst_dtect_obj)
            telemsg = tCls.tmplt_telemsg.value.format(\
                        value_str_messagename = mpl.telegram.escape_strparse_markdownv1(nameof_msg_rpt),\
                        value_str_contextid = mpl.telegram.escape_strparse_markdownv1(contexid),\
                        value_str_StartDateTime7 = mpl.telegram.escape_strparse_markdownv1(START_DATE_TIME7),\
                        value_str_ns = mpl.telegram.escape_strparse_markdownv1(_namespace), \
                        value_str_count_dtect_obj = mpl.telegram.escape_strparse_markdownv1(str(len(lst_dtect_obj))),\
                        value_str_dtect_obj = dtect_obj,\
                        value_str_url_shareable = evrnt_urlshareable)
            Q.logger(time7.currentTime7(),'             Sending message to Telegram ( メッセージを送る )')
            mCls.sendmessage_telegram(telemsg)

        ## ERASE OLD REPORT #  イレーズ レポート - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        reports = None
        try: reports = eCls.evernote_erase_old_notes()
        except Exception as e: Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
        if str(reports)!= 'None' and str(reports).strip()!='':
            Q.logger(time7.currentTime7(),' '*15 ,reports)


        count_detected_object = int(len(lst_dtect_obj))
        url_shareable_evernotes = str(evrnt_urlshareable)
    return count_detected_object, url_shareable_evernotes