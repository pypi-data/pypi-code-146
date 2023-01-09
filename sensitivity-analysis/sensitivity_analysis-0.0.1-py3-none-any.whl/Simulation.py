# -*- coding: utf-8 -*-


import numpy as np

from vehiclemodels.parameters_vehicle2 import parameters_vehicle2

# from vehiclemodels.vehicle_dynamics_ks import vehicle_dynamics_ks
from vehiclemodels.vehicle_dynamics_st import vehicle_dynamics_st
# from vehiclemodels.vehicle_dynamics_st import vehicle_dynamics_st

# from PYTHON.vehiclemodels.vehicle_dynamics_std import vehicle_dynamics_std

"""
 vehicleDynamics_mb - multi-body vehicle dynamics based on the DOT (department of transportation) vehicle dynamics
 reference point: center of mass

 Syntax:
     f = X_dot for different situations

 Inputs:
     :param x: vehicle state vector
     :param t: time vector
     :param u: vehicle input vector
     :param p: vehicle parameter vector

 Outputs:
     :return f: evaluation of X_dot vector

Created on Thu Nov  3 10:47:01 2022

@author: Youssef Ibrahim

 Written: 03-November-2022
 Last update: ---
 Last revision: ---
"""
# get the parameter class
# load parameters
p = parameters_vehicle2()
g = 9.81  # [m/s^2]         #acceleration due to gravity


# dynamics definition

#
def assignOrder(order):
    def do_assignment(to_func):
        to_func.order = order
        return to_func

    return do_assignment


class Simulation:
    def __init__(self, x, parameterMatrix, parameterAttribute):
        self.x = x
        self.u = None
        self.parameterMatrix = parameterMatrix
        self.parameterAttribute = parameterAttribute
        self.Y_cornering_left = None
        self.Y_oversteer_understeer_coasting = None
        self.Y_oversteer_understeer_breaking = None
        self.Y_oversteer_understeer_accelerating = None
        self.Y_braking = None
        self.Y_accelerating = None
        self.Y_all_situations = None

    def func_ST(self):
        # Reassign parameters
        noParameter = len(self.parameterMatrix[0])
        noTest = len(self.parameterMatrix)
        Y = np.zeros((noTest, len(self.x)))
        for i_Test in range(noTest - 1):
            for i_Parameter in range(noParameter - 1):
                if hasattr(p, self.parameterAttribute[i_Parameter]):
                    setattr(p, self.parameterAttribute[i_Parameter], self.parameterMatrix[i_Test, i_Parameter])
                elif hasattr(p.longitudinal, self.parameterAttribute[i_Parameter]):
                    setattr(p.longitudinal, self.parameterAttribute[i_Parameter],
                            self.parameterMatrix[i_Test, i_Parameter])
                elif hasattr(p.steering, self.parameterAttribute[i_Parameter]):
                    setattr(p.steering, self.parameterAttribute[i_Parameter], self.parameterMatrix[i_Test, i_Parameter])
                elif hasattr(p.tire, self.parameterAttribute[i_Parameter]):
                    setattr(p.tire, self.parameterAttribute[i_Parameter], self.parameterMatrix[i_Test, i_Parameter])
                else:
                    setattr(p.trailer, self.parameterAttribute[i_Parameter], self.parameterMatrix[i_Test, i_Parameter])

            Y[i_Test] = vehicle_dynamics_st(self.x, self.u, p)
        return Y

    def cornering_left(self):
        v_delta = 0.15
        a_long = 0
        self.u = [v_delta, a_long]
        self.Y_cornering_left = self.func_ST()

        return (self.Y_cornering_left)

    def oversteer_understeer_MB_Coasting(self):
        v_delta = 0.15

        # coasting
        self.u = [v_delta, 0]
        self.Y_oversteer_understeer_coasting = self.func_ST()

        return (self.Y_oversteer_understeer_coasting)

    def oversteer_understeer_MB_Breaking(self):
        v_delta = 0.15

        # braking
        self.u = [v_delta, -0.7 * g]
        self.Y_oversteer_understeer_braking = self.func_ST()

        return (self.Y_oversteer_understeer_braking)

    def oversteer_understeer_MB_Accelerating(self):
        v_delta = 0.15

        # accelerating
        self.u = [v_delta, 0.63 * g]
        self.Y_oversteer_understeer_accelerating = self.func_ST()

        return (self.Y_oversteer_understeer_accelerating)

    def braking(self):
        v_delta = 0.0
        acc = -0.7 * g
        self.u = [v_delta, acc]

        # simulate car
        self.Y_braking = self.func_ST()

        return (self.Y_braking)

    def accelerating(self):
        v_delta = 0.0
        acc = 0.63 * g
        self.u = [v_delta, acc]

        # simulate car
        self.Y_accelerating = self.func_ST()

        return (self.Y_accelerating)

    def allSituations(self):
        self.Y_all_situations = [self.cornering_left(), self.oversteer_understeer_MB_Coasting(), self.oversteer_understeer_MB_Breaking(),
                     self.oversteer_understeer_MB_Accelerating(), self.braking(), self.accelerating()]
        return (self.Y_all_situations)
