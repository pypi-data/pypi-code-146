from Retro3D import *


###############################################################################
#
###############################################################################
class Mesh:

    ###############################################################################
    #
    # requires a wavefront.obj file
    #
    ###############################################################################
    def __init__(self, fname):

        obj_file = ObjFile(fname);

        self.list_vertex = obj_file.list_vertex
        self.list_face = obj_file.list_face
        self.list_face_normal = obj_file.list_face_normal


