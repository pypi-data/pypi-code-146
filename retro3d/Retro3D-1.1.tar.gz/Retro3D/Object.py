import numpy as np
import pygame as pg
from Retro3D import *



###############################################################################
#
###############################################################################
class Object:


    ###############################################################################
    #
    ###############################################################################
    def __init__(self):

        self.mat_world = np.array([[1.0, 0.0, 0.0, 0.0],
                                   [0.0, 1.0, 0.0, 0.0],
                                   [0.0, 0.0, 1.0, 0.0],
                                   [0.0, 0.0, 0.0, 1.0]])

        self.pos = SiVector3(0.0, 0.0, 0.0)
        self.rot = SiVector3(0.0, 0.0, 0.0)
        self.scale = 1.0

        self.mesh = None
        self.list_face_normal = None

        self.draw_vertices = False
        self.draw_normals = False


    ###############################################################################
    #
    ###############################################################################
    def set_mesh(self, mesh: Mesh, face_color: pg.Color):

        self.mesh = mesh

        # face info
        #   color of face
        #       color belongs to obj so that diff objs can share the same 
        #       mesh but have diff colors
        #   indicies of the 4 vertices that make up the face
        #
        self.list_face_info = [(face_color, face) for face in mesh.list_face]
        


    ###############################################################################
    #
    ###############################################################################
    def set_pos(self, x, y, z):
        self.pos.x = x
        self.pos.y = y
        self.pos.z = z


    ###############################################################################
    #
    ###############################################################################
    def set_rot(self, x, y, z):
        self.rot.x = x
        self.rot.y = y
        self.rot.z = z



    ###############################################################################
    #
    ###############################################################################
    def set_scale(self, s):
        self.scale = s


    ###############################################################################
    #
    ###############################################################################
    def update(self):
        
        self.mat_world = Matrix.RotateZ(self.rot.z)
        self.mat_world = np.matmul(self.mat_world,  Matrix.RotateX(self.rot.x))
        self.mat_world = np.matmul(self.mat_world,  Matrix.RotateY(self.rot.y))
        self.mat_world = np.matmul(self.mat_world,  Matrix.Translate(self.pos))
        self.mat_world = np.matmul(self.mat_world, Matrix.Scale(self.scale))





        


        