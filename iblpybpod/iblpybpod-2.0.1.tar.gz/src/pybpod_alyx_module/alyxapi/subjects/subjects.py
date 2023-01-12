from pybpod_alyx_module.alyxapi.subjects.get import Get
from pybpod_alyx_module.alyxapi.subjects.post import Post


class Subjects:
    
    def __init__(self, _apibase):
        # print('Subject base init')
        self.apibase = _apibase
        self.get = Get(_apibase)
        self.post = Post(_apibase)
