import math
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from scipy.optimize import minimize

def Slover_UniSec_func(data,model,guess,method,chooseModel,tol):
    print('------Begin to estimate the parameters -------')
    print('Program will fit the data with a univariate second-order differential equation.')
    print('The differential equation is:')
    print("x(2) = beta1 * x + beta2 * x(1)")
    userdata = data
    if all(np.isnan(guess)):
        guess = [0,0,0,0,userdata.iloc[0,1],0]
        print('The initial guess values are')
        print('beta1:',guess[0],', beta2:',guess[1],', init01(x_0):',guess[4])
    else:
        print('The initial guess values you input are ',guess)
    print(f'The optimization method is {method}.')
    user_CalcUniSec_data = calc_UniSec_func(userdata,guess,method,chooseModel,tol)
    print(f'beta1:{user_CalcUniSec_data.x[0]},beta2:{user_CalcUniSec_data.x[1]},init01:{user_CalcUniSec_data.x[4]}')
    Predictor_UniSec_data = Predictor_UniSec_func(userdata,user_CalcUniSec_data)
    R_squared_UniSec_data = R_squared_UniSec_func(userdata,Predictor_UniSec_data)
    RMSE_UniSec_data = RMSE_UniSec_func(userdata,Predictor_UniSec_data)
    SE_UniSec_data = Hessian_UniSec_func(user_CalcUniSec_data.hess_inv)
    if user_CalcUniSec_data.success == False:
        outconvergence = f'convergence: False (tol={tol}, See Tolerance Details)'
    else:
        outconvergence = f'convergence: True (tol={tol}, See Tolerance Details)'
    userdata_field = userdata.copy()
    del userdata_field['time']
    outputDE1 = f'{userdata_field.columns.tolist()[0]}(2) = {user_CalcUniSec_data.x[0]}*{userdata_field.columns.tolist()[0]}(0) + {user_CalcUniSec_data.x[1]}*{userdata_field.columns.tolist()[0]}(1)'
    outputDE2 = f'Init t0:{user_CalcUniSec_data.x[4]}'
    outtable = pd.DataFrame()
    outtable['parameter'] = [f'{userdata_field.columns.tolist()[0]}(0) to {userdata_field.columns.tolist()[0]}(2)',
                             f'{userdata_field.columns.tolist()[0]}(1) to {userdata_field.columns.tolist()[0]}(2)',
                             f'init01']
    outtable['value'] = [user_CalcUniSec_data.x[0],
                         user_CalcUniSec_data.x[1],
                         user_CalcUniSec_data.x[4]]
    outtable['SE'] = [SE_UniSec_data[0,0],SE_UniSec_data[1,1],SE_UniSec_data[4][4]]
    out = {'userdata':userdata,
           'parameter':user_CalcUniSec_data,
           'equation':[outputDE1,outputDE2],
           'predict':Predictor_UniSec_data,
           'r_squared':R_squared_UniSec_data,
           'RMSE':RMSE_UniSec_data,
           'SE':SE_UniSec_data,
           'table':outtable,
           'convergence':outconvergence}
    return out

def calc_UniSec_func(userdata,guess,method,chooseModel,tol):
    args = [userdata, chooseModel]
    mid_calc_UniSec_data = minimize(mini_de_func,
                                    x0=guess,
                                    method=method,
                                    tol=tol,
                                    options={'disp':False},
                                    args=args)
    return mid_calc_UniSec_data

def mini_de_func(x0,args):
    data = args[0]
    mid_min_t = data['time']
    chooseModel = args[1]
    mid_num = chooseModel['varnum']
    mid_num = len(x0) - mid_num -1
    y0 = x0[mid_num:]
    mid_args = x0[:mid_num]
    # mid_args = (str(list(mid_args)))
    # print(fieldlist)
    mid_min_data = solve_ivp(Solve_UniSec_func,
                             [0, max(mid_min_t)],
                             y0=y0,
                             t_eval=mid_min_t,
                             args=[mid_args])

    min_result_y0list = mid_min_data.y
    min_result_y0list = min_result_y0list[0].tolist()
    mid_data_df = data.copy()
    del mid_data_df['time']
    mid_data_df.columns = range(0, len(mid_data_df.columns))
    min_result_y0df = pd.DataFrame(np.asarray(min_result_y0list).T)
    dfsquare = (min_result_y0df - mid_data_df) ** 2
    dfsum = sum(dfsquare.sum())
    return dfsum

def Solve_UniSec_func(t,y0,args):
    mid_args = args
    mid_args_list = list(mid_args)
    first = y0[1]
    second = mid_args_list[0] * y0[0] + mid_args_list[1] * y0[1]
    #os.system("pause")
    return [first,second]

def Predictor_UniSec_func(userdata,calcdata):
    mid_times = userdata.loc[:,'time']
    y0 = calcdata.x[4:6].tolist()
    # print('y0',y0)
    mid_args = calcdata.x[0:2]
    mid_usersol_data = solve_ivp(Solve_UniSec_func,
                             [0, max(mid_times)],
                             y0=y0,
                             t_eval=mid_times,
                             args=[mid_args])
    # print(mid_usersol_data.y[0])
    usercolumn = userdata.copy()
    mid_data = pd.DataFrame()
    mid_data['time'] = userdata['time']
    del usercolumn['time']
    solvercolumn = 'solver_' + usercolumn.columns.tolist()[0]
    mid_data[solvercolumn] = mid_usersol_data.y[0]
    return mid_data

def R_squared_UniSec_func(userdata,Predictor_data):
    R_square_df = pd.merge(userdata,Predictor_data,left_on='time',right_on='time')
    del R_square_df['time']
    R_square_cor = np.corrcoef(np.array(R_square_df.iloc[:,0].tolist()),np.array(R_square_df.iloc[:,1].tolist()))
    R_square_cor = R_square_cor[0][1] **2
    return R_square_cor

def RMSE_UniSec_func(userdata,Predictor_data):
    RMSE_UniSec_df = pd.merge(userdata, Predictor_data, left_on='time', right_on='time')
    del RMSE_UniSec_df['time']
    SSxe = sum((RMSE_UniSec_df.iloc[:,0] - RMSE_UniSec_df.iloc[:,1]) **2)
    RMSEx = math.sqrt(SSxe / len(RMSE_UniSec_df.iloc[:,0]))
    return RMSEx

def Hessian_UniSec_func(hessian):
    hessian[hessian <0] = np.nan
    hessian = np.sqrt(hessian)
    return hessian