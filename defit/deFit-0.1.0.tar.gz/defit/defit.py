from .AdjustModel_func import AdjustModel_func
from .JudgeModel_func import JudgeModel_func
from .IntiOption_func import IntiOption_func
from .CalcDe_func import CalcDe_func
from .PlotDe_func import PlotDe_func
def defit(data,model,guess=None,method=None,plot=True,tol=None):
    """
    Fitting Differential Equations to Time Series Data
    :param data: a DataFrame containing all model variables. The "time" column must be included.
    :param model: a string specifying the model to be used. The "=~" operator is used to define variables, with the name of the variable user defined on the left and the name of the variable in the data on the right. The '~' operator specifies a differential equation, with the dependent variable on the left and the independent variables on the right. See also ‘Details’.
    :param guess: an optional vector that allows the user to give starting values for the model parameters, including the model coefficients and variable initial states.
    :param method: an optional string indicating which optimizer to use. The default method is subject to the specific model. The available options are 'Nelder-Mead','L-BFGS-B','SLSQP' and 'BFGS'.
    :param plot: True or False
    :param tol: a float. Tolerance for termination. When tol is specified, the selected minimization algorithm sets some relevant solver-specific tolerance(s) equal to tol.
    :return:  the dict type
    dict[userdata | parameter | predict | r_squared | RMSE | SE | equation | table | convergence]

    Examples
    --------
    >>> import defit
    >>> import pandas as pd
    >>> df = pd.read_csv('defit/data/example1.csv')
    >>> model = '''
...             x =~ myX
...             time =~ myTime
...             x(2) ~ x + x(1)
...         '''
    >>> result1 = defit.defit(data=df,model=model)

     See Also
    ----------
    https://github.com/yueqinhu/defit
    """

    mid_model = AdjustModel_func(model)
    print('-------Your Model-------')
    print(mid_model)
    print('-------Your Data (first 3 rows)-------')
    print(data.head(3))
    # print('-------Begin to estimate the parameters-------')
    chooseModel = JudgeModel_func(mid_model)
    # print('Choose model is ', chooseModel)
    InitOption = IntiOption_func(userdata=data,
                                 model=mid_model,
                                 choosemodel=chooseModel,
                                 guess=guess,
                                 method=method,
                                 tol=tol)
    calcDe = CalcDe_func(data=InitOption[0],
                         model=mid_model,
                         guess=InitOption[2],
                         method=InitOption[3],
                         chooseModel=InitOption[1],
                         tol=InitOption[4])
    print('R-squared:', calcDe['r_squared'])
    print('table: \n', calcDe['table'])
    print(calcDe['convergence'])
    if plot == False:
        pass
    elif plot == True:
        plotDe = PlotDe_func(userdata=calcDe['userdata'], calcdata=calcDe['predict'])
    return calcDe
# cd C:\673\Coding\BNU\defit\defit
# import os
# import defit
# import pandas as pd
# df = pd.read_csv('data/example1.csv')
# model = '''
#             x =~ myX
#             time =~ myTime
#             x(2) ~ x + x(1)
#         '''
# defit.defit(data=df,model=model)