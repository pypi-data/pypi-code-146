class work_two(object):

    def __init__(self, world, world2):
        self.world = world
        self.world2 = world2

    def merge(self):  # Объединяем два словаря
        dic3 = self.world2.copy()
        dic3.update(self.world)
        return dic3

    def chunk(self):  # Разбиение на фрагменты
        return [self.world[i:i + int(self.world2)] for i in range(0, len(self.world), int(self.world2))]
