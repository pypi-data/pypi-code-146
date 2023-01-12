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

        self.pos = pos
        self.rot = SiVector3(0.0, 0.0, 0.0)

        self.mat_cam = np.zeros((4, 4))

        self.right = SiVector3(1.0, 0.0, 0.0)
        self.up = SiVector3(0.0, 1.0, 0.0)
        self.forward = SiVector3(0.0, 0.0, 1.0)


    ###############################################################################
    #
    ###############################################################################
    def set_pos(self, pos: SiVector3):

        self.pos = pos 


    ###############################################################################
    #
    ###############################################################################
    def set_rot(self, rot: SiVector3):

        self.rot = rot


    ###############################################################################
    #
    ###############################################################################
    def calc_camera_matrix(self):

        self.mat_cam = Matrix.RotateZ(self.rot.z)
        self.mat_cam = np.matmul(self.mat_cam,  Matrix.RotateX(self.rot.x))
        self.mat_cam = np.matmul(self.mat_cam,  Matrix.RotateY(self.rot.y))
        self.mat_cam = np.matmul(self.mat_cam,  Matrix.Translate(self.pos))

        # make a copy before inverse (so we have a mat that represents the cam in the world)
        self.right.x = self.mat_cam[0][0]
        self.right.y = self.mat_cam[0][1]
        self.right.z = self.mat_cam[0][2]

        self.up.x = self.mat_cam[1][0]
        self.up.y = self.mat_cam[1][1]
        self.up.z = self.mat_cam[1][2]

        self.forward.x = self.mat_cam[2][0]
        self.forward.y = self.mat_cam[2][1]
        self.forward.z = self.mat_cam[2][2]

        self.mat_cam = np.linalg.inv(self.mat_cam)

        return self.mat_cam





