import enum
from abc import ABC, abstractmethod
from typing import List, Optional

from meshgrid.grids.square import SquareGrid2D
from meshgrid.grids.square_multilayer import SquareMultilayerGrid2D

class SquareGridGame(ABC):
    '''A basic inheritable game on a square grid.

    Game classes define all of the Grids, internal components, and rules for a game,
    including how user input (eg: button presses) should be resolved by the game. Aka
    a game knows what to do if you tell it that the "Z" key was pressed, but it has
    no way of reading the keyboard input itself. It also does not specify how the 
    game engine decides to visualize the game.

    This is an abstract base class suitable for inheritance by games that plan to use
    a single Grid. It automatically sets up a Stats enum, and by default lets you end
    the game by pressing the escape key.

    The game object will automatically create a default Grid object for you. If
    you specify `layers`>1 then the grid will be a SquareMultilayerGrid2D object,
    and otherwise will default to a SquareGrid2D object (which has only one layer).
    
    For more information on `layers`, see the SquareMultilayerGrid2D class documentation.

    Parameters
    ----------
    :grid_width: The width of the default Grid, measured in squares
    :grid_height: The height of the default Grid, measured in squares
    :max_units: The maximum number of units that can be created on the default Grid
    :shape_manager: A shape manager object
    :stats_list: The desired columns in the Grid's Stats object
    :layers: The number of layers in the game's default grid

    Methods
    ----------
    :step: Is called every "tick" of the game while the game is running (update game rules here)
    :on_notebook_key_down: If usinig a notebook-based visualizer is called on key press

    '''
    
    def __init__(self,grid_width:int,grid_height:int,max_units:int, shape_manager, stats_list:List[str], layers:Optional[int]=None, **kwargs):
        
        self.done = False

        self.dims = 2
        self.width = grid_width
        self.height = grid_height
        self.max_units = max_units
        
        self.STAT = enum.IntEnum('StatsEnum', { stat:e for e,stat in enumerate(stats_list) })
        self.shape = shape_manager
        if layers is None:
            self.grid = SquareGrid2D(grid_width,grid_height,max_units,shape_manager,self.STAT)
        else:
            self.grid = SquareMultilayerGrid2D(grid_width,grid_height,max_units,shape_manager,self.STAT,layers=layers)
    
    @abstractmethod
    def step(self):
        '''Run for each "tick" of the game to update the game's state.
        
        This is the "main loop function" for your game, and should be
        overridden by your inheriting game class.

        To end the game, set `self.done=True` inside this function.
        '''
        
        ...

    def on_notebook_key_down(self, key, shift_key, ctrl_key, meta_key):
        '''Run a function that received keyboard input & updates the game.'''
        
        if key == "Escape":
            self.done = True # this ends the game
