import base64
import hashlib
import requests


class RongYingCommon:
    def __init__(self):
        pass

    def GetMD5string(self, paramStr: str = None) -> str:
        hmd5 = hashlib.md5()
        hmd5.update(paramStr.encode('utf-8'))
        sig = hmd5.hexdigest()
        return sig.upper()

    def GetBase64String(self, paramStr: str = None) -> str:
        return base64.b64encode(paramStr.encode('utf-8'))

    def SendPostRequest(self, url: str = None, body: dict = None, auth: str = None) -> dict:
        try:
            headers = {'content-type': 'application/json;charset=utf-8', 'Authorization': auth,
                       'Accept': 'application/json'}
            req = requests.post(url, json=body, headers=headers)
            return req.json()
        except Exception as error:
            return {"Flag": 400, "Msg": "发起请求失败,请检查请求参数信息;" + error.message}
            exit()
