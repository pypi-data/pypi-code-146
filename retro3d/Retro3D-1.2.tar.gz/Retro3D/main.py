from Retro3D import *


###############################################################################
#
# sample usage of Retro3D
# 
# to run, make sure to undoc call to main at the bottom of this file
#
###############################################################################



###############################################################################
#
###############################################################################
class TheCube(Game):


    ###############################################################################
    #
    ###############################################################################
    def __init__(self):
    
        # init game engine with screen resolution and background color
        super().__init__(SiVector2(1600, 900), pg.Color(100, 100, 255))

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

        key_pressed_dict = pg.key.get_pressed()

        if key_pressed_dict[pg.K_UP] or key_pressed_dict[pg.K_DOWN]:
         
            if key_pressed_dict[pg.K_UP]:
                vel = self.move_speed;
            else:
                vel = -self.move_speed;

            # move forward backward
            self.camera_pos += (self.engine.camera.forward * vel)
               
        if key_pressed_dict[pg.K_LEFT] or key_pressed_dict[pg.K_RIGHT]:
         
            if key_pressed_dict[pg.K_LSHIFT]:

                if key_pressed_dict[pg.K_LEFT]:
                    vel = -self.move_speed;
                else:
                    vel = self.move_speed;

                # move left/right
                self.camera_pos += (self.engine.camera.right * vel)

            else:

                if key_pressed_dict[pg.K_LEFT]:
                    vel = -self.rot_speed;
                else:
                    vel = self.rot_speed;

                self.camera_rot.y += vel


        if key_pressed_dict[pg.K_a] or key_pressed_dict[pg.K_z]:
         
                if key_pressed_dict[pg.K_a]:
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
    game = TheCube()
    game.run()
