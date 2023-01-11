from io import StringIO


class TruncatingStringIO(StringIO):
    def write(self, s: str):
        if self.tell() == 0:
            self.truncate()
        super().write(s)
