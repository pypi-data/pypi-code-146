import time
from dataclasses import dataclass
from ez_disk_cache import DiskCacheConfig, disk_cache

@dataclass
class Config(DiskCacheConfig):
    color: str

class CarDealer:
    def __init__(self):
        self.cars = []
        for color in ("red", "yellow", "blue"):
            self.cars += [self._order_car(config=Config(color))]

    @staticmethod  # <-- This lets us avoid the self parameter in the decorated function
    @disk_cache()
    def _order_car(config: Config):  # <-- Only the config parameter object should be here
        time.sleep(2)  # Delivery of a car takes some time
        return f"A fancy {config.color} car"

car_dealer = CarDealer()  # First instantiation takes a while
car_dealer = CarDealer()  # Second instantiation returns immediately
print(car_dealer.cars)