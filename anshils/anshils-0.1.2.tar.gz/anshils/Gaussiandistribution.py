from collections import Counter


class work_ones(object):

    def __init__(self, world):
        self.world = world

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
