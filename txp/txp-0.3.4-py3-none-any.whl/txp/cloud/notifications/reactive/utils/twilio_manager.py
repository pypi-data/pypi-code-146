# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


simple_report_pdf = "https://storage.cloud.google.com/txp-reports/labshowroom-001/report_1/labshowroom-001_report_1_2022-09-30-22-00-00.pdf"


class TwilioManager:
    def __init__(self, twilio_client: Client):
        self.twilio_client = twilio_client

    def send_media(self, msg_body: str, from_phone: str, to_phone: str, media_url: str):
        message = self.twilio_client.messages.create(
            from_=from_phone,
            body=msg_body,
            to=to_phone,
            media_url=media_url,
        )
        return message.sid
