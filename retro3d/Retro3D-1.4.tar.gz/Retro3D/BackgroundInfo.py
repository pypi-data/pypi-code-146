import pygame as pg
from Retro3D import *



###############################################################################
#
###############################################################################
class BackgroundInfo:

    class SectionInfo:
        def __init__(self):
            self.rect = pg.Rect(0, 0, 1, 1)
            self.color = pg.Color(0, 0, 0)

    class SectionInfoGradient:
        def __init__(self):
            self.rect = pg.Rect(0, 0, 1, 1)
            self.color_start = pg.Color(255, 255, 255)
            self.color_end = pg.Color(0, 0, 0)
            self.direction = SiDirection.VERTICAL

    ###############################################################################
    #
    ###############################################################################
    def __init__(self):

        self.list_section_info = list()


    ###############################################################################
    #
    ###############################################################################
    def add_section_info(self, section_info: 'SectionInfo'):

        self.list_section_info.append(section_info)





