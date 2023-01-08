import numpy as np
import pandas as pd
import warnings
def IntiOption_func(userdata,model,choosemodel,guess,method,tol):
    data = pd.DataFrame()
    usersVariable = model[model['operator'] == '=~']
    # print(usersVariable['variable'])
    for i in range(len(usersVariable['variable'])):
        if usersVariable['variable'][i] in userdata.columns.tolist():
            data[usersVariable['field'][i]] = userdata[usersVariable['variable'][i]]
        else:
            print(usersVariable['variable'][i],' is not found in columns of data.')
            warnings.warn(f"{usersVariable['variable'][i]} is not found in columns of data.", category=None, stacklevel=1,
                          source=None)

    # choose method by choosemodel
    if method is None:
        if choosemodel == {'varnum': 2, 'ordernum': 1}:
            method = 'Nelder-Mead'
        if choosemodel == {'varnum': 1, 'ordernum': 2}:
            method = 'BFGS'
        else:
            method = 'BFGS'

    # keep to modify guess values
    if guess is None:
        guess = [np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]
    else:
        print('The values of your guess are',guess)
    # return {userdata:data,choosemodel:choosemodel,guess:guess,method:method}
    if tol is None:
        tol = 1e-8
    else:
        print('The values of your tolerance is',tol)
    d = data.pop('time')
    data.insert(0,'time',d)
    return [data,choosemodel,guess,method,tol]
