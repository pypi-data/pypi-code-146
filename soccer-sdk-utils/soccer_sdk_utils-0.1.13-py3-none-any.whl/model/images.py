class Images:
    def __init__(self, **kwargs):
        self.logo = kwargs.get("logo")

    def __repr__(self):
        return f"Images(logo='{self.logo}')"
