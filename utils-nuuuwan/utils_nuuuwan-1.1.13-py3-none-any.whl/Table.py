class TableRow:
    def __init__(self, d):
        self.d = d

    def to_dict(self):
        return self.d

    @property
    def fields(self):
        return list(self.d.keys())

    @staticmethod
    def from_dict(self, d):
        return TableRow(d)

    def __eq__(self, other):
        if isinstance(other, TableRow):
            return self.d == other.d
        return False

    def __getattr__(self, key):
        if key in self.fields:
            return self.d[key]
        raise AttributeError


class Table:
    def __init__(self, d_list):
        self.d_list = d_list

    @staticmethod
    def from_dict(d_list):
        return Table(d_list)

    def to_dict_list(self):
        return self.d_list

    def __len__(self):
        return len(self.d_list)

    def filter(self, func_filter):
        return Table([d for d in self.d_list if func_filter(d)])

    def map(self, func_map):
        return Table([func_map(d) for d in self.d_list])

    def __eq__(self, other):
        if isinstance(other, Table):
            return self.d_list == other.d_list
        return False

    @property
    def first_d(self):
        return self.d_list[0]

    @property
    def fields(self):
        return list(self.first_d.keys())

    def __getitem__(self, idx):
        return TableRow(self.d_list[idx])

    def __add__(self, other):
        assert isinstance(other, Table)
        assert self.fields == other.fields
        return Table(self.d_list + other.d_list)
