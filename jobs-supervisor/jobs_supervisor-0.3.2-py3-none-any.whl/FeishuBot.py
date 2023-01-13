import requests

class FeishuBot():
    def __init__(self, webhook):
        self.webhook = webhook

    def send_msg(self, text):
        data = {
            "msg_type": "text",
            "content": {
                "text": text
            }
        }
        try:
            res=requests.post(self.webhook, json=data)
            return res.json()
        except Exception as e:
            return {"error":e}


if __name__ == '__main__':
    fei=FeishuBot(webhook)
    res=fei.send_msg("testing testing")
    print(res)

