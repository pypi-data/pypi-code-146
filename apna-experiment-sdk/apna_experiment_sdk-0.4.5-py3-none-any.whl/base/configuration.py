class Configuration:
    conf = dict()
    
    def __init__(self, **kwargs):
        self.conf.update(kwargs)
        
    def get_conf(self) -> dict:
        return self.conf
    
    def validate_conf(self, caller: str='Configuration'):
        for k, v in self.conf.items():
            if v is None:
                raise AttributeError(f"{caller}: Value for conf: {k} can't be None.")
