import numpy as np
from engine import *



###############################################################################
#
###############################################################################
class Projection:


    ###############################################################################
    #
    ###############################################################################
    def __init__(self, engine, screen_res: SiVector2):
      
        #view frustrum
        FOV = 60
        self.near_plane = 0.1
        self.far_plane = 100
        self.horiz_fov = math.radians(FOV)
        self.vert_fov = self.horiz_fov * (screen_res.y / screen_res.x)

        # precalc vars
        n = self.near_plane
        f = self.far_plane
        r = math.tan(self.horiz_fov / 2)
        l = -r
        t = math.tan(self.vert_fov / 2)
        b = -t

        # calc perspective projection matrix. view_frustrum -> unit_cube
        m00 = 2 / (r - l)
        m11 = 2 / (t - b)
        m22 = (f + n) / (f - n)
        m32 = -2 * n * f / (f - n)
        self.projection_matrix = np.array([[m00, 0, 0, 0],
                                           [0, m11, 0, 0],
                                           [0, 0, m22, 1],
                                           [0, 0, m32, 0]])

        # calc screen matrix. unit_cube -> screen
        hw = engine.screen_res_half.x
        hh =  engine.screen_res_half.y
        self.to_screen_matrix = np.array([[hw, 0, 0, 0],
                                          [0, -hh, 0, 0],
                                          [0, 0, 1, 0],
                                          [hw, hh, 0, 1]])