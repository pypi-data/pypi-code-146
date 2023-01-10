from looqbox.render.chatbot.base_chatbot_render import BaseChatbotRender


class WhatsAppRender(BaseChatbotRender):

    def __init__(self):
        super().__init__()

        self.file_extension_to_mime = {
            "pdf": "application/pdf",
            "csv": "text/csv",
            "png": "image/png",
        }

        self.formats = {
            "bold": {"start": "*", "end": "*"},
            "italic": {"start": "_", "end": "_"},
            "unispace": {"start": "```", "end": "```"},
            "none": {"start": "", "end": ""},
        }
