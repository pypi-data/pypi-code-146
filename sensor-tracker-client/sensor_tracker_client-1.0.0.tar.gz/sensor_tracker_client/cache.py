NO_ARGUMENT = "___"


class CacheCell:
    def __init__(self):
        self.headers = []
        self.values = []

    def set_value(self, header, value):
        if header in self.headers:
            n = self.headers.index(header)
            self.headers[n] = value
        else:
            self.headers.append(header)
            self.values.append(value)

    def get_value(self, header):
        if header in self.headers:
            n = self.headers.index(header)
            return self.values[n]
        else:
            return None


class Cache:
    def __init__(self):
        self.my_cache = {}

    def get_cache(self, key_value, *args):
        if key_value in self.my_cache:
            return self.my_cache[key_value].get_value(args[0])
        else:
            return None

    def set_cache(self, key_value, value, *args):
        if key_value in self.my_cache:
            cache_item = self.my_cache[key_value]
            cache_item.set_value(args[0], value)
        else:
            new_cache_item = CacheCell()
            new_cache_item.set_value(args[0], value)
            self.my_cache[key_value] = new_cache_item


cache = Cache()
del Cache
