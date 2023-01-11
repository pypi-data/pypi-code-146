import numpy as np
from Retro3D import *


###############################################################################
#
###############################################################################
class Camera:


    ###############################################################################
    #
    ###############################################################################
    def __init__(self, pos: SiVector3):

        self.pos = np.array([pos.x, pos.y, pos.z, 1.0])
        self.rot = np.array([0.0, 0.0, 0.0])


    ###############################################################################
    #
    ###############################################################################
    def calc_camera_matrix(self):

        p = SiVector3(self.pos[0], self.pos[1], self.pos[2])

        mat_cam = Matrix.RotateZ(self.rot[2])
        mat_cam = np.matmul(mat_cam,  Matrix.RotateX(self.rot[0]))
        mat_cam = np.matmul(mat_cam,  Matrix.RotateY(self.rot[1]))
        mat_cam = np.matmul(mat_cam,  Matrix.Translate(p))
        mat_cam = np.linalg.inv(mat_cam)

        return mat_cam





