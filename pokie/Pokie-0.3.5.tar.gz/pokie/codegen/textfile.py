from io import StringIO


class TextBuffer:
    TAB_SIZE = 4

    def __init__(self, buffer: StringIO = None):
        self.buf = buffer
        if buffer is None:
            self.buf = StringIO()

    def tab(self, count=0):
        return " " * (count * self.TAB_SIZE)

    def newline(self, count=1):
        return "\n" * count

    def writeln(self, content, level=0, newlines=1):
        self.buf.write(self.tab(level))
        self.buf.write(content)
        self.buf.write(self.newline(newlines))

    def read(self) -> str:
        self.buf.seek(0)
        return self.buf.read()
