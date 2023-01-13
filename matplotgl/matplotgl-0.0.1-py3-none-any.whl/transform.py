class Transform:

    def __init__(self, origin=0, scale=1):

        self.origin = origin
        self.scale = scale
        self.zoomed_origin = None
        self.zoomed_scale = None

    def __call__(self, x):
        if self._zoomed():
            return (x - self.zoomed_origin) * self.zoomed_scale
        else:
            return (x - self.origin) * self.scale

    def __repr__(self):
        return f'Transform(origin={self.origin}, scale={self.scale})'

    def _zoomed(self):
        return None not in (self.zoomed_origin, self.zoomed_scale)

    def inverse(self, x):
        if self._zoomed():
            return x / self.zoomed_scale + self.zoomed_origin
        else:
            return x / self.scale + self.origin

    def update(self, low, high):
        self.origin = low
        self.scale = 1.0 / (high - low)

    def zoom(self, low, high):
        self.zoomed_origin = low
        self.zoomed_scale = 1.0 / (high - low)

    def reset(self):
        self.zoomed_origin = None
        self.zoomed_scale = None

    @property
    def low(self):
        if self._zoomed():
            return self.zoomed_origin
        else:
            return self.origin

    @property
    def high(self):
        if self._zoomed():
            return (1.0 / self.zoomed_scale) + self.zoomed_origin
        else:
            return (1.0 / self.scale) + self.origin
