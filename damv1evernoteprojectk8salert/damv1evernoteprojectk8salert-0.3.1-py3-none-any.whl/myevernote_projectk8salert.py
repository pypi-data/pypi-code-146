import html
import re

import damv1env as env
import damv1time7 as time7
import damv1time7.mylogger as Q
from evernote.api.client import EvernoteClient
import evernote.edam.notestore.ttypes as NoteStoreTypes
import evernote.edam.type.ttypes as Types
import evernote.edam.error.ttypes as Errors

class utils():

    def getEvernoteList_CreatedDiffDays(self, _token):
        lst_output = [] 
        try:
            client = EvernoteClient(token=_token) 
            noteStore = client.get_note_store()

            filter=NoteStoreTypes.NoteFilter()
            filter.order=Types.NoteSortOrder.CREATED
            filter.ascending = True
            resultSpec=NoteStoreTypes.NotesMetadataResultSpec()
            resultSpec.includeTitle=True
            resultSpec.includeCreated=True
            resultSpec.includeContentLength=True
            resultSpec.includeUpdated=True
            resultSpec.includeDeleted=True
            resultSpec.includeUpdateSequenceNum=False
            resultSpec.includeNotebookGuid=True
            resultSpec.includeTagGuids=True
            resultSpec.includeAttributes=False
            resultSpec.includeLargestResourceMime=False
            resultSpec.includeLargestResourceSize=False

            noteMetaList=noteStore.findNotesMetadata(filter,0,100,resultSpec)
            for noteMeta in noteMetaList.notes:
                note_guid = noteMeta.guid
                note_dtz_created = time7.convert_timestamp_to_datetimezone7(noteMeta.created)
                note_dtz_diff_days = time7.difference_datetimezone7_by_day_from_now(note_dtz_created)
                line_note_info_formated = f"{note_guid} | {note_dtz_created} | {note_dtz_diff_days} days"
                lst_output.append(line_note_info_formated)
        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "getEvernoteList_CreatedDiffDays"')    
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
        return lst_output

    def deleteEvernote_WhenGreaterOfDays(self,_token, _lst_evernoteListDays, _days=2):
        reports=None
        try:
            client = EvernoteClient(token=_token) 
            noteStore = client.get_note_store()

            lst_report = []
            if len(_lst_evernoteListDays) != 0:
                Q.logger(time7.currentTime7(),'       (5) - Delete Old Notes ( デリートパーマネント )')
                for inf in _lst_evernoteListDays:
                    lst_note = inf.split('|')
                    if (len(lst_note)>1):
                        guid = lst_note[0].strip()
                        created = lst_note[1].strip()
                        int_day = int(lst_note[2].replace('days',''))
                        if int_day >= _days:
                            noteStore.expungeNote(_token, guid)  # delete permanent |  デリートパーマネント
                            lst_report.append(f'Note {guid} ({created}) is deleted. ( デリート )')
                if len(lst_report)!=0:
                    reports = (f'\n{str(time7.currentTime7())}' + ' '*17).join(lst_report)
        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "deleteEvernote_WhenGreaterOfDays"')    
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
        return reports    

    def remove_ANSI_escape_sequence(self, strContent):
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', strContent)