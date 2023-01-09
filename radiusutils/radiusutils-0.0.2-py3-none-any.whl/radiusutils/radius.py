import math

class Radius:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def circumference(self):
        return 2 * math.pi * self.radius

    def area(self):
        return math.pi * (self.radius ** 2)

    def diameter(self):
        return 2 * self.radius

    def contains_point(self, x, y):
        distance = ((self.x - x) ** 2 + (self.y - y) ** 2) ** 0.5
        return distance <= self.radius