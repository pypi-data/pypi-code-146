from looqbox.render.chatbot.base_chatbot_render import BaseChatbotRender
import re


class TeamsRender(BaseChatbotRender):

    def __init__(self):
        super().__init__()
        self.file_extension_to_mime = {
            "pdf": "application/pdf",
            "csv": "application/csv",
            "png": "image/png",
        }

        self.formats = {
            "bold": {"start": "*", "end": "*"},
            "italic": {"start": "_", "end": "_"},
            "unispace": {"start": "```", "end": ""},
            "none": {"start": "", "end": ""},
        }

    @staticmethod
    def remove_newlines(text):
        new_line_groups = re.findall("(\n\n+)", text)
        if not new_line_groups:
            return text
        return re.sub("(.)\n(.)", r"\1 \2", text).replace("\n\n", "\n").replace("\n", "\n\r")
