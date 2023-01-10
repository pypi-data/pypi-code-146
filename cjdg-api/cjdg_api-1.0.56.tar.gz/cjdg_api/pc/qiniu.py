from .base import base
from loguru import logger
from qiniu import put_file


class cjdgQiniu(base):

    def __init__(self, token):
        super().__init__(token)
        qn_token = self.get_token()
        logger.debug(qn_token)
        self.domain = qn_token.get("domain")
        if self.domain:
            self.appId = qn_token.get("appId")
            self.qn_token = qn_token.get("uptoken")
        else:
            msg = {
                "msg": "token错误，换不到七牛TOKEN",
                "token": token,
                "response": qn_token,
            }
            logger.error(msg)

    def get_token(self):
        api_name = "uploadgetUpToken.jhtml"
        data = {
            "fileType": 1
        }
        return self.request(api_name, data=data, api_prefix="", method="POST")

    def upload(self, filename: str, keyname: str):
        ret, info = put_file(self.qn_token, keyname, filename)
        logger.debug({"ret": ret, "info": info})
        url = f"http://{self.domain}/{keyname}"
        return url
