
class TObject:
    @property
    def obj(self):
        return self._obj
    
    @obj.setter
    def obj(self, ref):
        if ref is None:
            self._obj = None
        else:
            fundamental_type = self.get_fundamental_type()
            if not isinstance(ref, fundamental_type):
                raise ValueError(f"Invalid ROOT object. Object must be an instance of {fundamental_type}.")
        self._obj = ref
    
    def __init__(self, obj=None):
        self.obj = obj
        
    def get_fundamental_type(self):
        raise NotImplementedError