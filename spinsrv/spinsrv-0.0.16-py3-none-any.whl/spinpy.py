import requests

from spinsrv import spin


class KeyServerHTTPClient(object):
    def __init__(self, session=requests.Session()):
        self.url = "https://keys.spinsrv.com"
        self.session = session

    def which(self, req: spin.KeyWhichRequest):
        url = self.url + "/which"
        return spin.KeyWhichResponse.from_json(
            self.session.post(url, json=req.to_json()).json()
        )

    def temp(self, req: spin.KeyTempRequest):
        url = self.url + "/temp"
        return spin.KeyTempResponse.from_json(
            self.session.post(url, json=req.to_json()).json()
        )


class DirServerHTTPClient(object):
    def __init__(self, session=requests.Session()):
        self.url = "https://dir.spinsrv.com"
        self.session = session

    def tree(self, req: spin.DirTreeRequest):
        url = self.url + "/tree"
        return spin.DirTreeResponse.from_json(
            self.session.post(url, json=req.to_json()).json()
        )

    def apply(self, req: spin.DirApplyRequest):
        url = self.url + "/apply"
        return spin.DirApplyResponse.from_json(
            self.session.post(url, json=req.to_json()).json()
        )


class BitServerHTTPClient(object):
    def __init__(self, session=requests.Session()):
        self.url = "https://store.spinsrv.com"
        self.session = session

    def apply(self, req: spin.BitApplyRequest):
        url = self.url + "/apply"
        return spin.BitApplyResponse.from_json(
            self.session.post(url, json=req.to_json()).json()
        )
