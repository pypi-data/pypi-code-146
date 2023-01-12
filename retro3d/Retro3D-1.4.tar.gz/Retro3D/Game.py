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
    def __init__(self, config: ConfigGame):
    
        self.key_pressed_dict = dict()

        self.engine = Engine(config)


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

        self.key_pressed_dict = pg.key.get_pressed()

        pass
                

    ###############################################################################
    #
    ###############################################################################
    def is_key_down(self, key: int):

        if self.key_pressed_dict[key]:
            return True
        
        return False


    ###############################################################################
    #
    # override me!
    #
    ###############################################################################
    def update(self):  
        pass




