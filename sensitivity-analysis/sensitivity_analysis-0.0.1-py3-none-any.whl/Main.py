# -*- coding: utf-8 -*-
import numpy as np
import SALib
from SALib.sample import morris as ms
from SALib.analyze import morris as ma
from SALib.sample import saltelli
from SALib.analyze import sobol
from SALib.test_functions import Ishigami

import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib.pyplot import title, legend
import plotly.graph_objects as go
import math
import pandas as pd
from sklearn import preprocessing
from sklearn.cluster import KMeans
import seaborn as sns

# import csv
#import pip
#pip.main(['install', 'vehiclemodels'])
#import vehiclemodels
from vehiclemodels.parameters_vehicle2 import parameters_vehicle2
from vehiclemodels.init_ks import init_ks
from vehiclemodels.init_st import init_st
from vehiclemodels.init_mb import init_mb
from vehiclemodels.init_std import init_std
from vehiclemodels.vehicle_dynamics_ks import vehicle_dynamics_ks
from vehiclemodels.vehicle_dynamics_st import vehicle_dynamics_st
from vehiclemodels.vehicle_dynamics_mb import vehicle_dynamics_mb
from vehiclemodels.vehicle_dynamics_std import vehicle_dynamics_std
from Simulation import Simulation
import testing

"""
Created on Thu Sep 29 13:34:20 2022

@author: youss
"""

# load parameters
p = parameters_vehicle2()

delta0 = 0
vel0 = 15
Psi0 = 0
dotPsi0 = 0
beta0 = 0
sy0 = 0
initialState = [
    0,
    sy0,
    delta0,
    vel0,
    Psi0,
    dotPsi0,
    beta0,
]  # initial state for simulation
# x0_KS = init_ks(initialState)  # initial state for kinematic single-track model
x0_ST = init_st(initialState)  # initial state for single-track model
# x0_MB = init_mb(initialState, p)  # initial state for multi-body model
# x0_STD = init_std(initialState, p)  # initial state for single-track drift model
# --------------------------------------------------------------------------


# Sensitivity analysis
## SA parameters
noTrajectory = 10  # Number of trajectories to generate
noLevel = 4  # Number of levels
confidenceLevel = 0.95  # Confidence interval level

## Let's get parameter Attributes
parameterAttribute = [attr for attr in dir(p) if attr[0] != "_"]

parameterAttribute_l = [attr for attr in dir(p.longitudinal) if attr[0] != "_"]
parameterAttribute_s = [attr for attr in dir(p.steering) if attr[0] != "_"]
parameterAttribute_tir = [attr for attr in dir(p.tire) if attr[0] != "_"]
parameterAttribute_tr = [attr for attr in dir(p.trailer) if attr[0] != "_"]
##Now we need to know the length of the sub-parameters
lengthParameter_l = len(parameterAttribute_l)
lengthParameter_s = len(parameterAttribute_s)
lengthParameter_tir = len(parameterAttribute_tir)
lengthParameter_tr = len(parameterAttribute_tr)

parameter_l = np.empty(lengthParameter_l)
parameter_s = np.empty(lengthParameter_s)
parameter_tir = np.empty(lengthParameter_tir)
parameter_tr = np.empty(lengthParameter_tr)

for i in range(lengthParameter_l):
    value = getattr(p.longitudinal, parameterAttribute_l[i])
    np.append(parameter_l, value)
for i in range(lengthParameter_s):
    value = getattr(p.steering, parameterAttribute_s[i])
    np.append(parameter_s, value)
for i in range(lengthParameter_tir):
    value = getattr(p.tire, parameterAttribute_tir[i])
    np.append(parameter_tir, value)
for i in range(lengthParameter_tr):
    value = getattr(p.trailer, parameterAttribute_tr[i])
    np.append(parameter_tr, value)
parameterAttribute_s = list(
    map(lambda x: x.replace("v_max", "v_max_s"), parameterAttribute_s)
)
parameterAttribute_s = list(
    map(lambda x: x.replace("v_min", "v_min_s"), parameterAttribute_s)
)
parameterAttribute_l = list(
    map(lambda x: x.replace("v_max", "v_max_s"), parameterAttribute_l)
)
parameterAttribute_l = list(
    map(lambda x: x.replace("v_min", "v_min_s"), parameterAttribute_l)
)
parameterAttribute_tr = list(
    map(lambda x: x.replace("l", "l_tr"), parameterAttribute_tr)
)
parameterAttribute_tr = list(
    map(lambda x: x.replace("w", "w_tr"), parameterAttribute_tr)
)

lengthParameter = len(parameterAttribute)
index_l = parameterAttribute.index("longitudinal")
index_s = parameterAttribute.index("steering")
index_tir = parameterAttribute.index("tire")
index_tr = parameterAttribute.index("trailer")

parameter_old = np.empty(lengthParameter)
for i in range(lengthParameter):
    value = getattr(p, parameterAttribute[i])
    np.append(parameter_old, value)
parameterAttributeL = (
    parameterAttribute[:index_l]
    + parameterAttribute_l
    + parameterAttribute[index_l + 1 : index_s]
    + parameterAttribute_s
    + parameterAttribute[index_s + 1 : index_tir]
    + parameterAttribute_tir
    + parameterAttribute[index_tir + 1 : index_tr]
    + parameterAttribute_tr
    + parameterAttribute[index_tr + 1 :]
)
parameterAttribute = np.array(parameterAttributeL)

parameter = np.empty(0)
parameter = np.insert(parameter, np.size(parameter), parameter_old[:index_l])
parameter = np.insert(parameter, np.size(parameter), parameter_l)
parameter = np.insert(
    parameter, np.size(parameter), parameter_old[index_l + 1 : index_s]
)
parameter = np.insert(parameter, np.size(parameter), parameter_s)
parameter = np.insert(
    parameter, np.size(parameter), parameter_old[index_s + 1 : index_tir]
)
parameter = np.insert(parameter, np.size(parameter), parameter_tir)
parameter = np.insert(
    parameter, np.size(parameter), parameter_old[index_tir + 1 : index_tr]
)
parameter = np.insert(parameter, np.size(parameter), parameter_tr)
parameter = np.insert(parameter, np.size(parameter), parameter_old[index_tr + 1 :])

parameter_max = np.zeros(np.size(parameter))
parameter_min = np.zeros(np.size(parameter))

# Adjust small values
for i in range(np.size(parameter)):
    if abs(parameter[i]) < 0.1:
        parameter_max[i] = 100
        parameter_min[i] = -100
    elif parameter[i] >= 0:
        parameter_max[i] = parameter[i] * 100
        parameter_min[i] = parameter[i] * -100
    else:
        parameter_min[i] = parameter[i] * 100
        parameter_max[i] = parameter[i] * -100
bound = np.empty((np.size(parameter), 2))
bound[:, 0] = parameter_min
bound[:, 1] = parameter_max

attributeList = parameterAttribute.tolist()
bounds = bound.tolist()

##Analysis
problem = {"num_vars": np.size(parameter), "names": attributeList, "bounds": bound}

parameterMatrix = ms.sample(problem, noTrajectory, num_levels=noLevel)

# getting boundaries of states
x = testing.cornering_left()
x_bound = np.empty((x[0, :].size, 2))
x_name = []  # Just a dummy variable to enter the sampling function
for i in range(x[0, :].size):
    x_bound[i] = [np.min(x[:, i]), np.max(x[:, i])]
    if x_bound[i, 0] == x_bound[i, 1]:
        x_bound[i, 0] = x_bound[i, 0] - 0.1 * x_bound[i, 0]
        x_bound[i, 1] = x_bound[i, 1] + 0.1 * x_bound[i, 1]
    if i == 0:  ###Filling the dummy variable
        x_name.append("First")
    else:
        x_name.append("Other")
# sampling system states
xProblem = {"num_vars": np.size(x_bound[:, 0]), "names": x_name, "bounds": x_bound}
#change back 3 to noTrajectory
xMatrix = ms.sample(xProblem, 2, num_levels=noLevel)

#Create a matrix for the attribute assignment
attributeAssign = np.empty((len(parameterAttribute), 1))
for i_attr_assign in range(len(parameterAttribute)): attributeAssign[i_attr_assign] = i_attr_assign

# load simulation
simulation = Simulation(xMatrix[0], parameterMatrix, parameterAttribute)
si_state = []
for i_test in range(len(x_bound[:, 0])): si_state.append([])
    
# Now looping through different state combinations
for i in range(np.size(xMatrix[:, 0])):
    si_i = []
    df_si_i = []
    # simulate
    simulation = Simulation(xMatrix[i], parameterMatrix, parameterAttribute)
    X_dot = simulation.allSituations()
 #Now looping through situations
    for j in range(len(X_dot)):
        X_dot_situation = X_dot[j]
        # Now looping through different states (outputs)
        si_j = []
        for k in range(len(X_dot_situation[0])):
            si_k = ma.analyze(
                problem, parameterMatrix, X_dot_situation[:, k], print_to_console=False
            )
            si_k['stateCombination'] = i
            si_k['situation'] = j
            # Now eliminate parameters that have no effect
            i_zero = []
            for ind_s in range(len(si_k["mu"])):
                if (
                    (si_k["mu"][ind_s] == 0 or math.isnan(si_k["mu"][ind_s]))
                    and (
                        si_k["mu_star"][ind_s] == 0
                        or math.isnan(si_k["mu_star"][ind_s])
                    )
                    and (si_k["sigma"][ind_s] == 0 or math.isnan(si_k["sigma"][ind_s]))
                    and (
                        si_k["mu_star_conf"][ind_s] == 0
                        or math.isnan(si_k["mu_star_conf"][ind_s])
                    )
                ):
                    i_zero.append(ind_s)
            si_k["mu"] = np.delete(si_k["mu"], i_zero)
            si_k["mu_star"] = np.delete(si_k["mu_star"], i_zero)
            si_k["sigma"] = np.delete(si_k["sigma"], i_zero)
            si_k["mu_star_conf"] = np.delete(si_k["mu_star_conf"], i_zero)
            for i_del in reversed(i_zero):
                del si_k['names'][i_del]

            for i_test in range(len(si_k['mu_star'])):
                si_state[k].append([si_k['names'][i_test], si_k['mu_star'][i_test], si_k['stateCombination'], si_k['situation']])

            si_k = pd.DataFrame(si_k)
            si_j.append(si_k)

        df_si_i.append(pd.concat(si_j))
        si_i.append(si_j)
    si = pd.concat(df_si_i)


noActiveState = len(si_state)
stateDatabase =  []
for i_empty in reversed(range(len(si_state))):
    if len(si_state[i_empty]) == 0:
        si_state.remove(si_state[i_empty])
        noActiveState -= 1
    else:
        for i_point in si_state[i_empty]:
            stateDatabase.append(i_empty, attributeList.index(i_point[0]), (i_point[1].astype(np.float))
            #stateDatabase_1.append(attributeList.index(i_point[0]))
            #stateDatabase_2.append(i_point[1].astype(np.float))




#Trying out the integer axes
stateDatabase = np.array(stateDatabase)
#stateDatabase_1 = np.array(stateDatabase_1)
#stateDatabase_2 = np.array(stateDatabase_2)
#stateDatabase = np.array([stateDatabase_0, stateDatabase_1, stateDatabase_2])
stateDatabase = np.transpose(stateDatabase)
stateSensitivityIndex = [[], [], []]
activeState = [stateDatabase[0, 0]]
for i_activeState in stateDatabase[:, 0]:
    if i_activeState != activeState[-1]:
        activeState.append(i_activeState)
    else:
        None
stateSensitivityIndex[0] = activeState
sum = 0
n = 0

#now let's get the average index of each state
for i_state in range(len(stateSensitivityIndex[0])):
    for i_average in range(len(stateDatabase[:, 0])):
        if stateDatabase[i_average, 0] == stateSensitivityIndex[0][i_state]:
            sum += stateDatabase[i_average, 2]
            n += 1
        else:
            None
    stateSensitivityIndex[1].append(stateDatabase[i_average, 1])
    stateSensitivityIndex[2].append(sum/n)
    sum = 0
    n = 0
stateSensitivityIndex = np.array(stateSensitivityIndex)

#Plotting results of the simulation
  
xs = stateDatabase[:,0] # Selects all xs from the array
ys = stateDatabase[:,1]  # Selects all ys from the array
zs= stateDatabase[:,2]  # Selects all ys from the array

# Creating plot

fig = plt.figure(figsize = (10, 7))
ax = plt.axes(projection ="3d")

ax.scatter3D(xs, ys, zs, color = "green")
plt.yticks(np.arange(len(attributeList)), attributeList)
plt.title("Simulation results")
plt.show()

#sns.scatterplot(x=xs, y=ys, hue=group)


# Dataframe of the results
DF_stateDatabase = pd.DataFrame({'State' : xs, 'Parameter' : ys, 'Sensitivity_Index' : zs})
# The random_state needs to be the same number to get reproducible results
initialCentroid = []
startIndex = 0
for i_init in stateDatabase[:, 0]:
    if i_init != startIndex:
        initialCentroid.append([i_init, 0])
        startIndex = i_init
    else:
        None
initialCentroid = np.array(initialCentroid)

DF_Array = np.array(DF_stateDatabase)   # Converting into an array
DF_Norm = preprocessing.normalize(DF_Array) #Normalizing the data

kmeans = KMeans(n_clusters=6) #random_state=42)
kmeans.fit(DF_Norm)
DF_stateDatabase['cluster'] = kmeans.labels_


PLOT = go.Figure()

#Plotting clustered data
for C in list(DF_stateDatabase.cluster.unique()):
    
    PLOT.add_trace(go.Scatter3d(x = DF_stateDatabase[DF_stateDatabase.cluster == C]['State'],
                                y = DF_stateDatabase[DF_stateDatabase.cluster == C]['Parameter'],
                                z = DF_stateDatabase[DF_stateDatabase.cluster == C]['Sensitivity_Index'],
                                mode = 'markers', marker_size = 8, marker_line_width = 1,
                                name = 'Cluster ' + str(C)))


PLOT.update_layout(width = 800, height = 800, autosize = True, showlegend = True,
                   scene = dict(xaxis=dict(title = 'State', titlefont_color = 'black'),
                                yaxis=dict(title = 'Parameter', titlefont_color = 'black'),
                                zaxis=dict(title = 'Sensitivity_Index', titlefont_color = 'black')),
                   font = dict(family = "Gilroy", color  = 'black', size = 12))
PLOT.show()
"""
ax.scatter3D(xs, ys, zs, hue=kmeans.labels_)
plt.show()
"""


si.to_excel(excel_writer = "C:/Users/youss/test_02_1.xlsx")
DF_stateDatabase.to_excel(excel_writer = "C:/Users/youss/compare_02_1.xlsx")
