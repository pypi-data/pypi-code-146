import warnings
def JudgeModel_func(model):
    varnum = model[model['operator'] == '=~']
    varnum = varnum['field'].tolist()
    varnum = len(varnum) - 1
    ordernum = model[model['operator'] == '~']
    ordernum = ordernum['field'].tolist()
    orderlist = []
    for i in range(len(ordernum)):
        orderi = list(filter(str.isdigit, ordernum[i]))[0]
        orderi = int(orderi)
        orderlist.append(orderi)
    ordernum = max(orderlist)
    ResDict = {'varnum': varnum, 'ordernum': ordernum}
    if 'time' in model['field'].tolist():
        pass
        # print('Checking your model whether it contains "time"')
    else:
        print('"time" is not included in your model. You can see here:https://github.com/yueqinhu/defit')
        warnings.warn('"time" is not included in your model. You can see here:https://github.com/yueqinhu/defit', category=None, stacklevel=1,
                      source=None)
    return ResDict