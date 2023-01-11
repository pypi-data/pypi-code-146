from Retro3D import *



###############################################################################
#
# base class for all games
#
################################################################################
class Game:

    ###############################################################################
    #
    ###############################################################################
    def __init__(self, screen_res: SiVector2, background_color: pg.Color):
    
        self.res_width = screen_res.x
        self.res_height = screen_res.y
        
        self.res_width_half = self.res_width / 2
        self.res_height_half = self.res_height / 2      	

        light = LightDirectional(SiVector3(1.0, 0.0, 0.0))

        self.engine = Engine(SiVector2(self.res_width, self.res_height), background_color, light)


    ###############################################################################
    #
    ###############################################################################
    def run(self):

        is_game_active = True

        while is_game_active:

            self.get_player_input()

            self.update()

            self.engine.clear_screen()
            self.engine.update()

            self.engine.blit()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    is_game_active = False
                    break;
   
        pg.quit()


    
    ###############################################################################
    #
    # override me!
    #
    ###############################################################################
    def get_player_input(self):   
        pass

    
    ###############################################################################
    #
    # override me!
    #
    ###############################################################################
    def update(self):  
        pass

