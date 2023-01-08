from .Slover_BiFirst_func import Slover_BiFirst_func
from .Slover_UniSec_func import Slover_UniSec_func
def CalcDe_func(data,model,guess,method,chooseModel,tol):
    if chooseModel == {'varnum': 2, 'ordernum': 1}:
        print('Bivariate first-order differential equation')
        solverdata = Slover_BiFirst_func(data=data,model=model,guess=guess,method=method,chooseModel=chooseModel,tol=tol)
    elif chooseModel == {'varnum': 1, 'ordernum': 2}:
        print('Univariate second-order differential equation')
        solverdata = Slover_UniSec_func(data=data, model=model, guess=guess, method=method,chooseModel=chooseModel,tol=tol)
    else:
        print('Your model is not supported!')
    return solverdata