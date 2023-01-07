import warnings
import numpy as np
from math import cos, sin, acos

def Matrix_Sim_Decomposition(M_Sim):
    if type(M_Sim) == type(None):
        return 0, 1, 0, 0
    else:
        t_x = M_Sim[0][2]
        t_y = M_Sim[1][2]
        s = (M_Sim[0][0] ** 2 + M_Sim[1][0] ** 2) ** 0.5
        if s == 0:
            return 0, 0, 0, 0
        R = M_Sim[0:1][0:1]/s
        theta = acos(R[0][0])
        return theta, s, t_x, t_y

def Matrix_Sim_Generation(theta=0, s=1, t_x=0, t_y=0):
    '''
    x: left:-; right:+
    y: up:-; down:+
    theta: clockwise:+; Anticlockwise:-; center is (0,0)
    '''
    return np.array([[s*cos(theta), -s*sin(theta), t_x], [s*sin(theta), s*cos(theta), t_y]])
    
def Matrix_Sim_Modification(M_Sim, theta_deta, s_deta, x_deta, y_deta):
    theta, s, t_x, t_y = Matrix_Sim_Decomposition(M_Sim)
    theta = theta + theta_deta
    s = s + s_deta
    t_x = t_x + x_deta
    t_y = t_y + y_deta
    return Matrix_Sim_Generation(theta, s, t_x, t_y)

def Matrix_Sim_cv2image(M_Sim_cv):
    '''
    x: left:+; right:-
    y: up:+; down:-
    theta: clockwise:-; Anticlockwise:+; center is (0,0)
    '''
    return (1.0/M_Sim_cv[0][0], -M_Sim_cv[0][1], -M_Sim_cv[0][2], -M_Sim_cv[1][0], 1.0/M_Sim_cv[1][1], -M_Sim_cv[1][2])

def Matrix_Sim_Scaled(M_Sim, scale):
    theta, s, t_x, t_y = Matrix_Sim_Decomposition(M_Sim)
    return Matrix_Sim_Generation(theta, s, t_x/scale, t_y/scale)