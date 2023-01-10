class AnalogicMap:
    """
       create_map = AnalogicMap()
       print(create_map.create_map(x, 0, 64300, 0, 100))
    """
    def __init__(self, return_float=False):
        self._return_float = return_float

    def create_map(
        self,
        x,
        in_min,
        in_max,
        out_min,
        out_max
    ):
        
        _value_map = (
            (x-in_min)*(out_max-out_min)/(in_max - in_min)+out_min
        )
        return _value_map if self._return_float else int(_value_map)