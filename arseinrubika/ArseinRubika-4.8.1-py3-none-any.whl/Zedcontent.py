from arsein.Arsein import Messenger
from re import findall
from arsein.Error import AuthError,TypeAnti
from arsein.Copyright import copyright
from arsein.PostData import method_Rubika


class Antiadvertisement:
    def __init__(self,Sh_account: str):
        self.Auth = str("".join(findall(r"\w",Sh_account)))
        self.prinet = copyright.CopyRight
        self.methods = method_Rubika(Sh_account)
        self.bot = Messenger(Sh_account)

        if self.Auth.__len__() < 32:
            raise AuthError("The Auth entered is incorrect")
        elif self.Auth.__len__() > 32:
            raise AuthError("The Auth entered is incorrect")
    def Anti(self,Type:str,guid_gap:str,msg):
        if Type == "Gif":
            if msg["file_inline"]["type"] == "Gif":
                self.bot.deleteMessages(guid_gap, [msg.get("message_id")])
                return "delete Gif"
        elif Type == "Sticker":
            if msg["file_inline"]["type"] == "Sticker":
                self.bot.deleteMessages(guid_gap, [msg.get("message_id")])
                return "delete Sticker"
        elif Type == "Image":
            if msg["file_inline"]["type"] == "Image":
                self.bot.deleteMessages(guid_gap, [msg.get("message_id")])
                return "delete Image"
        elif Type == "Music":
            if msg["file_inline"]["type"] == "Music":
                self.bot.deleteMessages(guid_gap, [msg.get("message_id")])
                return "delete Music"
        elif Type == "Video":
            if msg["file_inline"]["type"] == "Video":
                self.bot.deleteMessages(guid_gap, [msg.get("message_id")])
                return "delete Video"
        elif Type == "Voice":
            if msg["file_inline"]["type"] == "Voice":
                self.bot.deleteMessages(guid_gap, [msg.get("message_id")])
                return "delete Voice"
        elif Type == "File":
            if msg["file_inline"]["type"] == "File":
                self.bot.deleteMessages(guid_gap, [msg.get("message_id")])
                return "delete File"
        elif Type == "forward":
            if "forwarded_from" in msg.keys():
                msge = self.bot.getMessagesInfo(guid_gap, [msg.get("message_id")])
                messag = msge["data"]["messages"]
                for ms in messag:
                    msgID = ms["message_id"]
                    getjsfor = ms["forwarded_from"]["type_from"]
                    if getjsfor == "Channel" or "User":
                        self.bot.deleteMessages(guid_gap, [msgID])
                        return "delete forward"
        elif Type == "link":
            msgID = msg.get("message_id")
            if findall(r"https://rubika.ir/joing/\w{32}", msg['text']) or findall(r"https://rubika.ir/joinc/\w{32}", msg['text']) or findall(r"https://rubika.ir/\w{32}", msg['text']) or findall(r"https://\w", msg['text']) or findall(r"http://\w", msg['text']) or findall(r"@\w", msg['text']) != []:
                self.bot.deleteMessages(guid_gap, [msgID])
                return "delete link"
        else: raise TypeAnti("The TypeAnti entered is incorrect")