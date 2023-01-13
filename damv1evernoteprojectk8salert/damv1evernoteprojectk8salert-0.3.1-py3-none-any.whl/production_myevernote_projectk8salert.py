import html
import re

import damv1env as env
import damv1time7 as time7
import damv1time7.mylogger as Q
from evernote.api.client import EvernoteClient
import evernote.edam.notestore.ttypes as NoteStoreTypes
import evernote.edam.type.ttypes as Types
import evernote.edam.error.ttypes as Errors

from .myevernote_projectk8salert import utils

class production():
    TOKEN = env.production_evernote.dev_token.value

    def evernote_testcreate_elementContent_withoutErrorHandler(self):
        Q.logger(time7.currentTime7(),'             Test create note.')
        dev_token = str(self.TOKEN).strip()
        client = EvernoteClient(token=dev_token) 
        noteStore = client.get_note_store()
        newtitle = f'Test {time7.currentTime7()}'
        note = Types.Note() 
        note.title =  f'\U0001F4D1 {newtitle}'
        note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">' 
        eContent =  html.escape('\x1b[31merror\x1b[39m: ERROR sql insert with : DO failed created for Order Number  = 4ALCEN0TO7IUM')
        ## 01 remove ANSI Escape Sequences
        eContent = utils().remove_ANSI_escape_sequence(eContent)
        eContent = html.escape(eContent)
        note.content += f'<en-note><p>{{elementContent}}</p></en-note>'.format(elementContent=eContent)
        created_note = noteStore.createNote(note)
        noteGuid = created_note.guid
        Q.logger(time7.currentTime7(),'             Successfully created a new note with :')
        Q.logger(time7.currentTime7(),'               GUID: ', str(noteGuid))
        Q.logger(time7.currentTime7(),'               Title ( タイトル ): ', str(newtitle))

    def evernote_generate_report(self, _contexid, _nameof_msg_rpt, _lst_grplines, _tmplt_wrapper, **kwargs):

        bShowErrorExplain = False
        if '_argShowErrorExplain' in kwargs:
            if "'bool'" in str(type(bShowErrorExplain)):
                bShowErrorExplain = kwargs.get("_argShowErrorExplain") 

        oput_shareable =  None
        endpoint = "https://sandbox.evernote.com/"
        try:
            dev_token = self.TOKEN
            client = EvernoteClient(token=dev_token) 
            # - - - - - | prepared new Note
            userStore = client.get_user_store() 
            noteStore = client.get_note_store()
            newtitle = f'Report {time7.currentTime7()}'
            note = Types.Note() 
            note.title =  f'\U0001F4D1 {newtitle}'

            note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">' 
            Q.logger(time7.currentTime7(),"             E1 - completed")
        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "evernote_generate_report" E1')    
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
            return None

        try:
            note.content += _tmplt_wrapper.format(\
                value_str_ervnt_rptname = html.escape(_nameof_msg_rpt), \
                value_str_contexid = html.escape(_contexid), \
                value_strlst_grplines = ''.join(_lst_grplines)
            )
            # - - - - - | prepared created Note
            created_note = noteStore.createNote(note)
            Q.logger(time7.currentTime7(),"             E2 - completed")
        except Errors.EDAMUserException as edeu:
            Q.logger(time7.currentTime7(),'Fail of function "evernote_generate_report" E2')    
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(edeu)) 

            if bShowErrorExplain==True:
                Q.logger(time7.currentTime7(),'Explain :\n',str(note.content))
            return None

        try:
            noteGuid = created_note.guid
            Q.logger(time7.currentTime7(),'             Successfully created a new note with ( うまい ):')
            Q.logger(time7.currentTime7(),'               Contex Id: ', str(_contexid))
            Q.logger(time7.currentTime7(),'               GUID: ', str(noteGuid))
            Q.logger(time7.currentTime7(),'               Title ( タイトル ): ', str(newtitle))
            # - - - - - | prepared shareable Note
            user = userStore.getUser(dev_token).shardId
            shareKey = noteStore.shareNote(dev_token, noteGuid)
            Q.logger(time7.currentTime7(),'               Note URL set to clipboard. The note has been shared with the following URL ( リンク ):')
            shareable = "%s/shard/%s/sh/%s/%s" % (endpoint, user, noteGuid, shareKey)	 
            Q.logger(time7.currentTime7(),f'               {str(shareable)}')     
            oput_shareable = shareable    
            Q.logger(time7.currentTime7(),"             E3 - completed")
        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "evernote_generate_report" E3')    
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e)) 
        return oput_shareable

    def evernote_erase_old_notes(self):
        reports = None
        try:
            dev_token = self.TOKEN
            lst_notes_info = utils().getEvernoteList_CreatedDiffDays(dev_token)
            reports = utils().deleteEvernote_WhenGreaterOfDays(dev_token, lst_notes_info)
        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "evernote_erase_old_notes"')    
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
        return reports 


class testing():
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    ## uncomments this bellow for testing only ( テスティング ) !
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def execute(self):
        f = sanbox()
        f.evernote_testcreate_elementContent_withoutErrorHandler()

# test = testing()
# test.execute()
