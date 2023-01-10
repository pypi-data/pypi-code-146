import requests
from .base import base
from loguru import logger
from qiniu import put_file


class cjdgQiniu(base):

    def __init__(self, token, app_secret):
        super().__init__(token, app_secret)
        qn_token = self.get_token()
        self.domain = qn_token.get("domain")
        if self.domain:
            self.appId = qn_token.get("appId")
            self.qn_token = qn_token.get("uptoken")
        else:
            msg = {
                "msg": "token错误，换不到七牛TOKEN",
                "token": token,
                "app_secret": app_secret,
                "response": qn_token,
            }
            logger.error(msg)

    def get_token(self):
        api_name = "file/qiniu/getUpToken"
        return self.request(api_name)

    def upload(self, filename: str, keyname: str):
        ret, info = put_file(self.qn_token, keyname, filename)
        logger.debug({"ret": ret, "info": info})
        url = f"http://{self.domain}/{keyname}"
        return url
