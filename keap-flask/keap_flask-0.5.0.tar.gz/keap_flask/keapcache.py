import pickle


class KeapCache:

    def __init__(self, cache_file=None):
        self.cache_file = cache_file
        self.cache = self.get_dict('keap_cache')

    def refresh_cache(self):
        self.cache = self.get_dict('keap_cache')

    def update_cache(self, key, data):
        self.refresh_cache()
        self.cache[key] = data
        self.update_dict_data("keap_cache", self.cache)

    def update_dict_data(self, dict_name, data):
        cache = self.read_all_data().copy()
        if dict_name in cache.keys():
            cache[dict_name].update(data)
        else:
            cache[dict_name] = data
        # if dict_name in current_cache:
        pickle_out = open(self.cache_file, "wb")
        pickle.dump(cache, pickle_out)
        pickle_out.close()

    def read_all_data(self):
        try:
            pickle_in = open(self.cache_file, "rb")
            data = pickle.load(pickle_in)
            pickle_in.close()
        except FileNotFoundError:
            data = {}
            pickle_out = open(self.cache_file, "wb")
            pickle.dump(data, pickle_out)
            pickle_out.close()
        return data

    def get_dict(self, dict_name):
        data = self.read_all_data().get(dict_name)
        if data is None:
            self.update_dict_data(dict_name, {})
            return self.read_all_data().get(dict_name)
        else:
            return data
