
class RESTAction:
    
    def __init__(self, name, path, method, **kwargs):
        self.name = name
        self.path = path
        self.method = method
        self.kwargs = kwargs