class Image:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.filename = kwargs.get("filename")
        self.path = kwargs.get("path")
        self.title = kwargs.get("title")
        self.alt_text = kwargs.get("alt_text")
        self.url = kwargs.get("url")

    def __repr__(self):
        return f"<Image(id={self.id}, filename='{self.filename}', path='{self.path}'), url='{self.url}'>"
