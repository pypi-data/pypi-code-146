from pybpod_alyx_module.alyxapi.data.get import Get
from pybpod_alyx_module.alyxapi.data.post import Post

class Data():
    def __init__(self, _apibase):
        self.apibase = _apibase
        self.get = Get(_apibase)
        self.post = Post(_apibase)
