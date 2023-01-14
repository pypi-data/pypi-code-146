import enum

_session = {}


def _get_session(self):
   if _session.get(self):
       self.session = _session[self]

def _clear_session(self):
   from telethon.sessions import StringSession
   if self.session and self.session.auth_key:
        ss = self.session
        _session.update({self:ss})
        self.session = StringSession("")
        self.session._dc_id = ss.dc_id

