from engine import *


###############################################################################
#
###############################################################################
class LightDirectional:

    ###############################################################################
    #
    ###############################################################################
    def __init__(self, dir: SiVector3):

        light_vector = list()

        dir = dir.normalize();

        self.direction = list()
        self.direction.append(dir.x)
        self.direction.append(dir.y)
        self.direction.append(dir.z)



        


        