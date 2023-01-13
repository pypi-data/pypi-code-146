import requests

from spinsrv import spin

DEBUG = False


class KeyServerHTTPClient(object):
    def __init__(self, session=requests.Session()):
        self.url = "https://keys.spinsrv.com"
        self.session = session

    def which(self, req: spin.KeyWhichRequest):
        if DEBUG:
            print(f"KeyServerHTTPClient.which {req}")

        url = self.url + "/which"
        return spin.KeyWhichResponse.from_json(
            self.session.post(url, json=req.to_json()).json()
        )

    def temp(self, req: spin.KeyTempRequest):
        if DEBUG:
            print(f"KeyServerHTTPClient.temp {req}")

        url = self.url + "/temp"
        return spin.KeyTempResponse.from_json(
            self.session.post(url, json=req.to_json()).json()
        )


class DirServerHTTPClient(object):
    def __init__(self, session=requests.Session()):
        self.url = "https://dir.spinsrv.com"
        self.session = session

    def tree(self, req: spin.DirTreeRequest):
        if DEBUG:
            print(f"DirServerHTTPClient.tree {req}")

        url = self.url + "/tree"
        return spin.DirTreeResponse.from_json(
            self.session.post(url, json=req.to_json()).json()
        )

    def apply(self, req: spin.DirApplyRequest):
        if DEBUG:
            print(f"DirServerHTTPClient.apply {req}")

        url = self.url + "/apply"
        return spin.DirApplyResponse.from_json(
            self.session.post(url, json=req.to_json()).json()
        )


class BitServerHTTPClient(object):
    def __init__(self, session=requests.Session()):
        self.url = "https://store.spinsrv.com"
        self.session = session

    def apply(self, req: spin.BitApplyRequest):
        if DEBUG:
            print(f"BitServerHTTPClient.apply {req}")

        url = self.url + "/apply"
        return spin.BitApplyResponse.from_json(
            self.session.post(url, json=req.to_json()).json()
        )
