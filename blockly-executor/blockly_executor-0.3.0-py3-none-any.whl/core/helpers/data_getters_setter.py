def data_getter_root_dict(self, name):
    try:
        return self.data[name]
    except KeyError:
        self.data[name] = {}
        return self.data[name]


def data_getter_root_str(self, name):
    try:
        return self.data[name]
    except KeyError:
        self.data[name] = ''
        return self.data[name]


def data_getter_root_list(self, name):
    try:
        return self.data[name]
    except KeyError:
        self.data[name] = []
        return self.data[name]


def data_setter_root(self, name, value):
    self.data[name] = value
