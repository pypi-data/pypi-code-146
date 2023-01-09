import random


def getRandomNumSet(bits):
    ''' 随机生成定长的小写字母和数字组合'''
    num_set = [chr(i) for i in range(48, 58)]
    total_set = num_set

    value_set = "".join(random.sample(total_set, bits))
    return value_set
