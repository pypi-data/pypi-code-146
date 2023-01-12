from Retro3D import *


###############################################################################
#
# sample usage of Retro3D
# 
###############################################################################



###############################################################################
#
###############################################################################
class TheCube(Game):


    ###############################################################################
    #
    ###############################################################################
    def __init__(self, config: ConfigGame):
    
        super().__init__(config)

        # create mesh from obj file            	
        base_path = os.path.dirname(__file__)
        path = base_path + os.sep + "models" + os.sep + "cube" + os.sep + "cube.obj"
        mesh_cube  = Mesh(path)

        # setup camera info
        self.camera_pos = SiVector3(0.0, 0.0, -10.0)
        self.camera_rot = SiVector3(0.0, 0.0, 0.0)

        self.move_speed = 0.1
        self.rot_speed = 0.01

        # create game objs
        self.list_game_obj = list()

        object = Object()         
        object.set_mesh(mesh_cube, pg.Color('blue'))
        object.draw_vertices = True
        object.draw_normals = True
        object.set_pos(0.0, 0, 0.0)
        object.set_rot(0.0, 0.0, 0.0) 
        object.set_scale(1.0) 
        self.list_game_obj.append(object)
        self.engine.add_display_object(object, Engine.DISPLAY_LIST_SHADED)



    ###############################################################################
    #
    ###############################################################################
    def get_player_input(self):

        super().get_player_input()

        vel = 0.0

        if self.is_key_down(pg.K_UP) or self.is_key_down(pg.K_DOWN):
         
            if self.is_key_down(pg.K_UP):
                vel = self.move_speed;
            else:
                vel = -self.move_speed;

            # move forward backward
            self.camera_pos += (self.engine.camera.forward * vel)
               
        if self.is_key_down(pg.K_LEFT) or self.is_key_down(pg.K_RIGHT):
         
            if self.is_key_down(pg.K_LSHIFT):

                if self.is_key_down(pg.K_LEFT):
                    vel = -self.move_speed;
                else:
                    vel = self.move_speed;

                # move left/right
                self.camera_pos += (self.engine.camera.right * vel)

            else:

                if self.is_key_down(pg.K_LEFT):
                    vel = -self.rot_speed;
                else:
                    vel = self.rot_speed;

                self.camera_rot.y += vel


        if self.is_key_down(pg.K_a) or self.is_key_down(pg.K_z):
         
                if self.is_key_down(pg.K_a):
                    vel = -self.rot_speed;
                else:
                    vel = self.rot_speed;

                self.camera_rot.x += vel


        self.engine.camera.pos = self.camera_pos
        self.engine.camera.rot = self.camera_rot


     
        
    ###############################################################################
    #
    ###############################################################################
    def update(self):
        
        super().update()

        for obj in self.list_game_obj:
 
            obj.rot.x += 0.005
            obj.rot.y += 0.03

            obj.update()




###############################################################################
#
#
#  
#
#
#
###############################################################################
if __name__ == '__main__':

    # sample game
     
    config = ConfigGame()
    config.screen_resolution = SiVector2(1600, 900)
    config.background_color = pg.Color(100, 25, 255)
    config.light_direction = SiVector3(1.0, 0.0, 0.0)

    game = TheCube(config)
    game.run()
