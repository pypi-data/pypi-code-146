import uuid
from ai_dashboard.tabs.data_report.blocks.base import BaseBlock


class Image(BaseBlock):
    def __init__(self, image_url: str, title: str = "", width_percentage: int = 100):
        self.title = title
        self.image_url = image_url
        self.block = {
            "type": "appBlock",
            "content": [
                {
                    "type": "imageDisplayBlock",
                    "attrs": {
                        "imageSrc": image_url,
                        "title": title,
                        "width": f"{width_percentage}%",
                        "height": "auto",
                    },
                }
            ],
        }

    def postprocess(self, report_client):
        """
        Upload the image to the report app and return the block.
        """
        filename = f"{self.title}.png" if self.title else f"{str(uuid.uuid4())}.png"
        self.file_url = report_client._endpoints._upload_file(
            report_client.dataset_id, self.image_url, filename
        )
        self.block["content"][0]["attrs"]["imageSrc"] = self.file_url


class Audio(BaseBlock):
    def __init__(self, audio_url: str, title: str = "", width_percentage: int = 100):
        self.title = title
        self.audio_url = audio_url
        self.block = {
            "type": "appBlock",
            "content": [
                {
                    "type": "audioDisplayBlock",
                    "attrs": {
                        "audioSrc": audio_url,
                        "title": title,
                        "width": f"{width_percentage}%",
                        "height": "auto",
                    },
                }
            ],
        }

    def postprocess(self, report_client):
        """
        Upload the image to the report app and return the block.
        """
        filename = f"{self.title}.wav" if self.title else f"{str(uuid.uuid4())}.wav"
        self.file_url = report_client._endpoints._upload_file(
            report_client.dataset_id, self.audio_url, filename
        )
        self.block["content"][0]["attrs"]["audioSrc"] = self.file_url


class Video(BaseBlock):
    def __init__(self, video_url: str, title: str = "", width_percentage: int = 100):
        self.title = title
        self.video_url = video_url
        self.block = {
            "type": "appBlock",
            "content": [
                {
                    "type": "videoDisplayBlock",
                    "attrs": {
                        "videoSrc": video_url,
                        "title": title,
                        "width": f"{width_percentage}%",
                        "height": "auto",
                    },
                }
            ],
        }

    def postprocess(self, report_client):
        """
        Upload the image to the report app and return the block.
        """
        filename = f"{self.title}.mp4" if self.title else f"{str(uuid.uuid4())}.mp4"
        self.file_url = report_client._endpoints._upload_file(
            report_client.dataset_id, self.video_url, filename
        )
        self.block["content"][0]["attrs"]["videoSrc"] = self.file_url
