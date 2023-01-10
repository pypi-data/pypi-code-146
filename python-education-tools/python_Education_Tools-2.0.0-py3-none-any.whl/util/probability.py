import random


def probability(prob=.3, space=100):
    return (0, 1)[random.randint(0, space) in range(int(prob * 100))]

#二分类分布
bin_probability = lambda prob=.3, space=100: (0, 1)[random.randint(0, space) in range(int(prob * 100))]



def multi_probability(dis_dict:dict,space=100):
    """
    #多分类分布
    {print:3,len:4,probability:9}
    """

    values=dis_dict.values()

    #get each ratio list
    prob_values=[round(i/sum(values),len(str(space))-1) for i in values]

    #convert to space distribution
    #right point
    scope_right = [int((sum(prob_values[:i]) + prob_values[i])*space) for i in range(len(prob_values))]
    scope_right[-1]=space #修正右端点，因为转化为概率然后映射后，有累计误差，导致右端点可能大于或小于space的值
    #left pointy
    scope_left=[0]+scope_right[:-1]
    #get scope of each probability
    scope = [range(*i) for i in zip(scope_left, scope_right)]
    keys= dis_dict.keys()
    tables= dict(zip(keys,scope))
    #print(tables)
    #随机生成整数，落在不同分布期间，取得分布区间对应的key，只能落在 一个区间因此 下面的t的元素只能是1个，t[0]
    x=random.randint(0,space-1)
    t=[k for k,v in tables.items() if x in v][0]
    return t



if __name__ == '__main__':
    a = [probability(.332,space=1000) for _ in range(10000)]

    print(sum(a)/len(a))
    d={'a':4.3,'b':5.4,'c':6.9,'d':7.23,'e':8.314,'f':9.11}
    print(multi_probability(d,space=1000))
    results=[multi_probability(d,space=133) for _ in range(1000)]
    t=[results.count(i) for i in d.keys()]
    test_results=map(lambda  x: round(x/sum(t),3),t)
    #print(sum(test_results))
    print(*test_results)
