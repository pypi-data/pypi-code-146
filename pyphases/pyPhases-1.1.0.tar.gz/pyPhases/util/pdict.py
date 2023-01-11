class pdict(dict):
    def __getitem__(self, *args, create=False):
        k = args[0] if len(args) == 1 else args
        if not isinstance(k, list) and not isinstance(k, tuple):
            return super().__getitem__(k)

        value = self
        for field in k:
            try:
                value = value.__getitem__(field)
            except KeyError as e:
                if create:
                    v = pdict({})
                    value.__setitem__(field, v)
                    value = value.__getitem__(field)
                else:
                    raise e

        return value

    def __setitem__(self, orgPath, v):
        if not isinstance(orgPath, list) and not isinstance(orgPath, tuple):
            return super().__setitem__(orgPath, v)
        orgPath = list(orgPath)
        value = self
        k = orgPath.copy()
        overwriteField = k.pop()
        for field in k:
            try:
                value = value.__getitem__(field)
            except KeyError:
                value.__setitem__(field, pdict())
                value = value.__getitem__(field)
        value[overwriteField] = v

    def setdefaults(self, defaultDict):
        for key, value in pdict(defaultDict).items():
            if key in self:
                if isinstance(self[key], dict):
                    self[key].setdefaults(value)
            else:
                self[key] = value
        return self

    def update(self, values, path=None):
        path = path or []
        for field in values:
            value = values[field]

            if isinstance(value, dict) and field in self:
                self[field] = pdict(self[field])
                self[field].update(value)
            else:
                self[field] = value
        pass
