from collections import Counter


class work_dy(object):

    def __init__(self, *world):
        self.world = world[0]
        self.world2 = world[1]

    def merge(self):  # Объединяем два словаря
        dic3 = self.world2.copy()
        dic3.update(self.world)
        return dic3

    def chunk(self):  # Разбиение на фрагменты
        return [self.world[i:i + int(self.world2)] for i in range(0, len(self.world), int(self.world2))]

    def get_vowels(self):  # Получаем гласные
        return [each for each in self.world if each in "aeiou"]

    def capitalize(self):  # Первая буква в верхнем регистре
        return self.world.title()

    def check_duplicate(self):  # Проверка дубликатов
        return len(self.world) != len(set(self.world))

    def Filtering(self):  # Фильтрация значений
        return list(filter(None, self.world))

    def ByteSize(self):  # Размер в байтах
        return len(self.world.encode("utf8"))

    def anagrams(self):  # Анаграммы
        return Counter(self.world) == Counter(self.world)

    def palindrome(self):  # Проверка палиндромов
        return self.world == self.world[::-1]


