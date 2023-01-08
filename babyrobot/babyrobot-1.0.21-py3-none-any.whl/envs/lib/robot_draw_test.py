from ipycanvas import Canvas, hold_canvas
from ipywidgets import Image
from time import sleep

import random
import os

from .robot_position import RobotPosition
from .draw_grid import Level


class RobotDrawTest( RobotPosition ):
    
    sprite_count = 0    
    canvas_sprites = []
    
    def __init__( self, 
                  level, 
                  x_size = 256, 
                  y_size = 256, 
                  initial_sprite = 0, 
                  start_pos = None,
                  x_offset = 0, y_offset = 0 ):
      
        super().__init__( level, x_size, y_size, start_pos, x_offset, y_offset )

        self.canvas = self.grid.canvases[Level.Robot]              
        
        # the number of steps before a sprite change
        self.sprite_change = 2
                       
        self.sprite_index = initial_sprite        
          
        self.load_single_sprint()          
        
        if not start_pos:
          self.show_cell_position(self.level.start)
        else:
          self.show_cell_position(start_pos)

    def load_single_sprint(self):
        image_path = os.path.join(self.level.working_directory,f'images/baby_robot_0.png')        
        self.sprite = Image.from_file(image_path)       

    def load_sprites(self):        
        ' load the sprite sheet and when loaded callback to split it into individual sprites '   

        for row in range(5):
          for col in range(2):                                                         
            index = row + col
            image_path = os.path.join(self.level.working_directory,f'images/baby_robot_{index}.png')        
            sprite = Image.from_file(image_path)
            self.canvas_sprites.append( sprite )      
        
        # add a sprite to the display
        self.canvas.clear()
        self.draw()       

    def get_number_of_sprites(self):
      ''' return the number of sprites on the sprite sheet '''
      num_sprites = len(self.canvas_sprites)
      return num_sprites        

    def draw_sprite(self,index):   
        ' remove the last sprite and add the new one at the current position ' 
        x = self.x + self.x_offset
        y = self.y + self.y_offset
        self.canvas.clear_rect(x-10, y-10, self.robot_size+10, self.robot_size+10)                      
        self.canvas.draw_image(self.sprite, x, y )                             

    def draw(self):    
        ' add the current sprite at the current position '     
        self.draw_sprite(self.sprite_index)
        # self.update_sprite()           

    def show_cell_position(self, *args):
      ''' set the robot position in grid coords '''      
      super().set_cell_position( *args )      
            
      # clear the canvas of any previous sprite
      self.canvas.clear()     
      self.draw()                

    def move_direction(self,direction):        
        ' move from one square to the next in the specified direction '  

        if self.test_for_valid_move( direction ):          
          move_method_name = f"move_{direction.name}"                                        
          with hold_canvas(self.canvas):         
            for _ in range(self.robot_size//self.step):
                getattr(self,move_method_name)()  
                self.canvas.clear_rect(self.x-10, self.y-10, self.robot_size+10, self.robot_size+10)             
                self.canvas.draw_image(self.sprite, self.x, self.y )                     
                self.canvas.sleep(40)  
                sleep(0.07) # pause between each move step 
                            
          self.move_count += 1 