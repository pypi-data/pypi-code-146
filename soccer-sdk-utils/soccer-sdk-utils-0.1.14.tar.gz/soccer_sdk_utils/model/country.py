class Country:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.code = kwargs.get("code")

    def __repr__(self):
        return f"<Country(id={self.id}, name='{self.name}', code='{self.code}')>"
