import execjs as j
# pip install pyexecjs


class ExecJs:
    def __init__(self, filename):
        self.filename = filename
        f = open(self.filename, 'r', encoding='utf-8')
        self.js_data = f.read()
        f.close()

        self.js = j.compile(self.js_data)

    def call(self, func, *args, **kwargs):
        return self.js.call(func, *args, **kwargs)


execjs = ExecJs
