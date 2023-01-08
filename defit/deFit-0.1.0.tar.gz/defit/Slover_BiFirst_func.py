import math
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from scipy.optimize import minimize

def Slover_BiFirst_func(data,model,guess,method,chooseModel,tol):
    print('------Begin to estimate the parameters -------')
    print('Program will fit the data with a bivariate first-order differential equation.')
    print('The differential equations are:')
    print("dx/dt = beta1 * x + beta2 * y")
    print('dy/dt = beta3 * x + beta4 * y')
    userdata = data
    if all(np.isnan(guess)):
        guess = [0, 0, 0, 0, userdata.iloc[0, 1], userdata.iloc[0, 2]]
        print('The initial guess values are')
        print('beta1:',guess[0],', beta2:',guess[1],', beta3:',guess[2],', beta4:',guess[3],', x0:',guess[4],', y0:',guess[5])
    else:
        print('The initial guess values you input are ', guess)
    print(f'The optimization method is {method}.')
    user_CalcUniSec_data = calc_BiFirst_func(userdata, guess, method, chooseModel,tol)
    Predictor_UniSec_data = Predictor_BiFirst_func(userdata, user_CalcUniSec_data)
    R_squared_UniSec_data = R_squared_BiFirst_func(userdata, Predictor_UniSec_data)
    RMSE_UniSec_data = RMSE_BiFirst_func(userdata, Predictor_UniSec_data)
    SE_UniSec_data = Hessian_BiFirst_func(user_CalcUniSec_data.hess_inv)
    if user_CalcUniSec_data.success == False:
        outconvergence = f'convergence: False (tol={tol}, See Tolerance Details)'
    else:
        outconvergence = f'convergence: True (tol={tol}, See Tolerance Details)'
    userdata_field = userdata.copy()
    del userdata_field['time']
    outputDE1 = f'{userdata_field.columns.tolist()[0]}(1) = {user_CalcUniSec_data.x[0]}*{userdata_field.columns.tolist()[0]}(0) + {user_CalcUniSec_data.x[1]}*{userdata_field.columns.tolist()[1]}(0)'
    outputDE2 = f'{userdata_field.columns.tolist()[1]}(1) = {user_CalcUniSec_data.x[2]}*{userdata_field.columns.tolist()[0]}(0) + {user_CalcUniSec_data.x[3]}*{userdata_field.columns.tolist()[1]}(0)'
    outputDE3 = f'Init t0:{user_CalcUniSec_data.x[4]}'
    outputDE4 = f'Init t0:{user_CalcUniSec_data.x[5]}'
    outtable = pd.DataFrame()
    outtable['parameter'] = [f'{userdata_field.columns.tolist()[0]}(0) to {userdata_field.columns.tolist()[0]}(1)',
                             f'{userdata_field.columns.tolist()[1]}(0) to {userdata_field.columns.tolist()[0]}(1)',
                             f'{userdata_field.columns.tolist()[0]}(0) to {userdata_field.columns.tolist()[1]}(1)',
                             f'{userdata_field.columns.tolist()[1]}(0) to {userdata_field.columns.tolist()[1]}(1)',
                             f'init01',
                             f'init01']
    outtable['value'] = [user_CalcUniSec_data.x[0],
                         user_CalcUniSec_data.x[1],
                         user_CalcUniSec_data.x[2],
                         user_CalcUniSec_data.x[3],
                         user_CalcUniSec_data.x[4],
                         user_CalcUniSec_data.x[5]]
    outtable['SE'] = [SE_UniSec_data[0, 0],
                      SE_UniSec_data[1, 1],
                      SE_UniSec_data[2, 2],
                      SE_UniSec_data[3, 3],
                      SE_UniSec_data[4][4],
                      SE_UniSec_data[5][5]]
    out = {'userdata': userdata,
           'parameter': user_CalcUniSec_data,
           'equation': [outputDE1, outputDE2,outputDE3,outputDE4],
           'predict': Predictor_UniSec_data,
           'r_squared': R_squared_UniSec_data,
           'RMSE': RMSE_UniSec_data,
           'SE': SE_UniSec_data,
           'table': outtable,
           'convergence': outconvergence}
    return out


def calc_BiFirst_func(userdata, guess, method, chooseModel,tol):
    args = [userdata, chooseModel]
    mid_calc_UniSec_data = minimize(mini_BiFirst_de_func,
                                    x0=guess,
                                    method=method,
                                    tol=tol,
                                    options={'disp': False},
                                    args=args)
    return mid_calc_UniSec_data


def mini_BiFirst_de_func(x0, args):
    data = args[0]
    mid_min_t = data['time']
    y0 = x0[4:]
    mid_args = x0[:4]
    # mid_args = (str(list(mid_args)))
    # print(fieldlist)
    mid_min_data = solve_ivp(Solve_BiFirst_func,
                             [0, max(mid_min_t)],
                             y0=y0,
                             t_eval=mid_min_t,
                             args=[mid_args])

    min_result_y0list = mid_min_data.y
    min_result_df = pd.DataFrame(np.asarray(min_result_y0list).T)
    mid_data_df = data.copy()
    del mid_data_df['time']
    mid_data_df.columns = range(0, len(mid_data_df.columns))
    # min_result_y0df = pd.DataFrame(np.asarray(min_result_y0).T)
    dfsquare_y0 = (min_result_df - mid_data_df) ** 2
    dfsum = sum(dfsquare_y0.sum())
    return dfsum


def Solve_BiFirst_func(t, y0, args):
    mid_args = args
    mid_args_list = list(mid_args)
    dxdt = mid_args_list[0] * y0[0] + mid_args_list[1] * y0[1]
    dydt = mid_args_list[2] * y0[0] + mid_args_list[3] * y0[1]
    # os.system("pause")
    return [dxdt, dydt]


def Predictor_BiFirst_func(userdata, calcdata):
    mid_times = userdata.loc[:, 'time']
    y0 = calcdata.x[4:6].tolist()
    # print('y0',y0)
    mid_args = calcdata.x[0:4]
    mid_usersol_data = solve_ivp(Solve_BiFirst_func,
                                 [0, max(mid_times)],
                                 y0=y0,
                                 t_eval=mid_times,
                                 args=[mid_args])
    # print(mid_usersol_data.y[0])
    usercolumn = userdata.copy()
    mid_data = pd.DataFrame()
    mid_data['time'] = userdata['time']
    del usercolumn['time']
    solvercolumn1 = 'solver_' + usercolumn.columns.tolist()[0]
    mid_data[solvercolumn1] = mid_usersol_data.y[0]
    solvercolumn2 = 'solver_' + usercolumn.columns.tolist()[1]
    mid_data[solvercolumn2] = mid_usersol_data.y[1]
    return mid_data


def R_squared_BiFirst_func(userdata, Predictor_data):
    R_square_df = pd.merge(userdata, Predictor_data, left_on='time', right_on='time')
    del R_square_df['time']
    R_square_cor1 = np.corrcoef(np.array(R_square_df.iloc[:, 0].tolist()), np.array(R_square_df.iloc[:, 2].tolist()))
    R_square_cor2 = np.corrcoef(np.array(R_square_df.iloc[:, 1].tolist()), np.array(R_square_df.iloc[:, 3].tolist()))
    R_square_cor1 = R_square_cor1[0][1] ** 2
    R_square_cor2 = R_square_cor2[0][1] ** 2
    return [R_square_cor1,R_square_cor2]


def RMSE_BiFirst_func(userdata, Predictor_data):
    RMSE_UniSec_df = pd.merge(userdata, Predictor_data, left_on='time', right_on='time')
    del RMSE_UniSec_df['time']
    SSxe1 = sum((RMSE_UniSec_df.iloc[:, 0] - RMSE_UniSec_df.iloc[:, 2]) ** 2)
    RMSEx1 = math.sqrt(SSxe1 / len(RMSE_UniSec_df.iloc[:, 0]))
    SSxe2 = sum((RMSE_UniSec_df.iloc[:, 1] - RMSE_UniSec_df.iloc[:, 3]) ** 2)
    RMSEx2 = math.sqrt(SSxe2 / len(RMSE_UniSec_df.iloc[:, 0]))
    print('RMSE:',RMSEx1,RMSEx2)
    return [RMSEx1,RMSEx2]


def Hessian_BiFirst_func(hessian):
    hessian[hessian < 0] = np.nan
    hessian = np.sqrt(hessian)
    return hessian