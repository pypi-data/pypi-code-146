class D2DVector:
    """A two-dimensional immutable vector."""
    
    def __init__(self, x, y):
        self.vec = (x, y)

    def __repr__(self):
        return f'({self[0]}, {self[1]})'
        
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.vec == other.vec
        else:
            return False
    
    def to_tuple(self):
        return self.vec
    
    def to_list(self):
        return list(self.vec)

    def __add__(self, other):
        return D2DVector(self[0] + other[0], self[1] + other[1])
    
    def __mul__(self, other):
        return D2DVector(self[0] * other[0], self[1] * other[1])
    
    def __sub__(self, other):
        return D2DVector(self[0] - other[0], self[1] - other[1])
    
    def __len__(self):
        return 2
    
    def __getitem__(self, i):
        length = len(self)
        if i < 0:
            i += length
        if 0 <= i < length:
            return self.vec[i]
        raise IndexError(f'Index out of range: {i}')