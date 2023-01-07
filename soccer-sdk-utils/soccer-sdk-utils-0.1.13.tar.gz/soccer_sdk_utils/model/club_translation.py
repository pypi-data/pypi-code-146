class ClubTranslation:
    def __init__(self, **kwargs):
        for arg in kwargs:
            value = kwargs.get(arg)

            if arg in ["_id", "id"]:
                self.id = value
            elif arg in ["src", "from"]:
                self.src = value
            elif arg in ["dst", "to"]:
                self.dst = value
            else:
                raise ValueError("Invalid argument: %s" % arg)

    @property
    def is_noop(self):
        return self.src == self.dst

    def __repr__(self):
        return f"<ClubTranslation(src='{self.src}', dst='{self.dst}', id='{self.id}')>"
