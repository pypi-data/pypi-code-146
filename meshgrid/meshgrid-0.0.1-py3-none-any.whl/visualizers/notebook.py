import time
import asyncio
import ipycanvas
import ipywidgets
import numpy as np


class NotebookVisualizer:
    '''A Meshgrid visualizer for Jupyter Notebooks.

    Visualizer classes interact with your monitor, keyboard, mouse, etc.
    so that you can view and interact with Games as a person would expect
    to, rather than programmatically. After creating a Notebook object,
    don't forget to call the `bind_game()` function to hook that specific
    game object.

    This particular Visualizer class is designed for Jupyter Notebooks.

    Parameters
    ----------
    :grid_width: The width of the default Grid, measured in squares
    :grid_height: The height of the default Grid, measured in squares
    :fps: The target frames-per-second 
    :frame_per_step: The frames between each call of Game's `step()`
    :bkg_gutter: The amount of space to give between gray background squares
    :draw_game_over: Whether or not to gray the screen after the game ends
    :colors: The available colors for pieces. Can be string names or hex code

    Methods
    -------
    :bind_game: Hooks a Game object for visualization
    :display: Shows the game in the given Jupyter Notebook cell
    '''
    
    def __init__(self,grid_width,grid_height,fps=120,frame_per_step=2,scale=20,bkg_gutter=.1,
                 draw_game_over=True,colors=["blue","red"],**kwargs):
        
        self.canvas = ipycanvas.Canvas(width=grid_width*scale, height=grid_height*scale)
        self.frame_per_step = frame_per_step
        self.fps = fps
        self.draw_game_over = draw_game_over
        
        self.scale = scale
        self.colors = np.array(colors)
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.bkg_gutter = bkg_gutter
        
        self._create_background_grid()
        
        self.output = ipywidgets.Output()
    
    def _create_background_grid(self):
        '''Create a background grid of gray squares behind pieces.'''
        
        background_grid = np.dstack(np.mgrid[:self.grid_height,:self.grid_width]).reshape(-1,2)
        self.bkg_x = (background_grid[:,0]+self.bkg_gutter/2.)*self.scale
        self.bkg_y = (background_grid[:,1]+self.bkg_gutter/2.)*self.scale
        self.bkg_scale = self.scale*(1-self.bkg_gutter)
        self.bkg_color = "#E0E0E0"
    
    def bind_game(self,game):
        '''Hook a Game object to visualize.
        
        :game: The Game object to visualize.
        '''
        
        self.game = game
        self.color_id = game.grid.stats[:,game.STAT.COLOR]
        if "on_notebook_key_down" in dir(self.game):
            self.canvas.on_key_down(self.output.capture()(self.game.on_notebook_key_down))
        if "on_notebok_mouse_move" in dir(self.game):
            self.canvas.on_mouse_move(self.output.capture()(self.game.on_notebok_mouse_move))
        if "on_notebok_mouse_down" in dir(self.game):
            self.canvas.on_mouse_down(self.output.capture()(self.game.on_notebok_mouse_down))
        self._validate_stats_enum(self.game.STAT)

    def _validate_stats_enum(self, STAT_ENUM):
        '''Ensure that stats used by this class exist (to avoid errors).
        
        :STAT_ENUM: An enum object used to define a Grid's Stats columns
        '''
        if 'VISIBLE' not in dir(STAT_ENUM) or 'COLOR' not in dir(STAT_ENUM):
            raise Exception("The following stats are required when using NotebookVisualizer: VISIBLE, COLOR")

    def _clear_canvas(self):
        '''Clear the visualization canvas and redraw the background grid.'''
    
        self.canvas.clear()
        self._draw_background_grid()
        
    def _draw_background_grid(self):
        
        self.canvas.fill_style = self.bkg_color
        self.canvas.fill_rects(self.bkg_y,self.bkg_x,self.bkg_scale)

    def _draw_game_over(self):
        '''Dim the screen by drawing a transparent gray square over the grid.'''
        
        self.canvas.fill_style = "#43434380"
        self.canvas.fill_rect(0,0,self.grid_width*self.scale,self.grid_height*self.scale)
        
    def _print_square_locations(self):
        '''Draw 1x1 squares to the grid for the location of every game piece.'''

        for color_id,color in enumerate(self.colors):
            if self.game.grid.loc[unit_id,0]>=0: # negative coordinates imply being off the board 
                self.canvas.fill_style = color
                mask = (self.color_id==color_id)
                self.canvas.fill_rects(
                    self.game.loc[mask,1]*self.scale,
                    self.game.loc[mask,0]*self.scale, 
                    self.scale
            )

    def _print_square_pieces(self):
        '''Draw pieces to the grid by drawing squares to the canvas.'''
        
        grid = self.game.grid
        for unit_id in range(self.game.grid.stats.shape[0]):
            if self.game.grid.stats[unit_id,self.game.STAT.VISIBLE]:
                self.canvas.fill_style = self.colors[grid.stats[unit_id,self.game.STAT.COLOR]]
                shape_start = grid.shape.info[grid.stats[unit_id,self.game.STAT.SHAPE],self.game.shape.START]
                shape_end   = grid.shape.info[grid.stats[unit_id,self.game.STAT.SHAPE],self.game.shape.END]
                self.canvas.fill_rects(
                    self.scale * (grid.shape.mask[shape_start:shape_end,1]+grid.loc[unit_id,1]),
                    self.scale * (grid.shape.mask[shape_start:shape_end,0]+grid.loc[unit_id,0]),
                    self.scale
                )

    def display(self):
        '''Show the Game and all captured STDOUT & STDERR output values.'''
    
        self.game.done = False
        asyncio.get_event_loop().create_task(self._game_loop())
        display(self.canvas,self.output)
        
    async def _game_loop(self):
        '''Run the game's core loop in a separate thread, managing framerate.'''
    
        frame = 1
        self.game.done = False # this line exists so the game loop can be run separately of self.display()
        game_step = self.output.capture()(self.game.step) # capture print statements and errors in main loop
        while not self.game.done:
            time0 = time.time()
            
            with ipycanvas.hold_canvas():
                self._clear_canvas()
                self._print_square_pieces()
                if frame % self.frame_per_step == 0:
                    game_step()
                
            time_passed = time.time()-time0
            frame += 1
            await asyncio.sleep(max(0,1./self.fps-time_passed))
        
        if self.draw_game_over:
            with ipycanvas.hold_canvas():
                self._draw_game_over()