import numpy as np

from meshgrid.games.square import SquareGridGame
from meshgrid.shape.square import SquareShapeManager
from meshgrid.queueing.discrete import UnitIDOrderedTurnQueue

class BasicRPG(SquareGridGame):
    '''An example tactical RPG game on a single square Grid.

    Units are divided into a "blue" and "red" team. Both teams attach one-another
    until only one team remains. One hit will kill an enemy piece, and pieces can
    move one square at a time.

    All pieces are 1x1 squares (but 1x1, 2x2, and 3x3 square sizes are pre-specified).

    Try altering this simple toy class to make more complex tactical RPG games!

    Parameters
    ----------
    :grid_width: The width of the default Grid, measured in squares
    :grid_height: The height of the default Grid, measured in squares
    :max_units: The maximum number of units that can be created on the default Grid

    Methods
    -------
    :make_shape_manager: The function specifying the Shape Manager object for the game
    :init_grid: Function called to initialize the game's Grid at the start of the game
    :step: The function called at every "tick" of the game
    :act: The function called to request that the given unit ID take an action
    :damage_piece: The function called when one unit successfully hits another unit
    :on_notebook_key_down: If usinig a notebook-based visualizer is called on key press
    '''
    
    def __init__(self, grid_width, grid_height, max_units, **kwargs):
        
        shape_manager = self.make_shape_manager()        
        stats_list = ['VISIBLE','ALIVE','SIDE','SHAPE','COLOR','MOVE','HP','DMG']
        super().__init__(grid_width, grid_height, max_units, shape_manager, stats_list, **kwargs)
        self.init_grid()
        
        self.turn_queue = UnitIDOrderedTurnQueue(self.grid.stats,self.STAT)

    def make_shape_manager(self):
        '''Create a Shape Manager object to be used by the game.

        Modify this function to specify the unique shapes that pieces can take
        in this game.

        :return: A Shape Manager object
        '''
        
        return SquareShapeManager([
            np.ones((1,1),dtype=bool),
            np.ones((2,2),dtype=bool),
            np.ones((3,3),dtype=bool),
        ])

    def init_grid(self):
        '''Initialize the game's Grid at the start of a new game.'''
        
        self.grid.stats[:,self.STAT.VISIBLE] = True
        self.grid.stats[:,self.STAT.ALIVE] = True
        self.grid.stats[:,self.STAT.SHAPE] = 0
        self.grid.stats[:,self.STAT.SIDE] = np.arange(self.max_units)%2
        self.grid.stats[:,self.STAT.COLOR] = np.arange(self.max_units)%2        
        self.grid.stats[:,self.STAT.MOVE] = 2
        self.grid.stats[:,self.STAT.HP] = 1
        self.grid.stats[:,self.STAT.DMG] = 2
        self.grid.place_pieces_randomly()
        
    def step(self):
        '''Run for each "tick" of the game to update the game's state.

        For this game, each tick of the game involves determining which unit can
        act next, and then requesting that this unit take its action.
        '''

        unit_id = self.turn_queue.pop()
        self.done = self.act(unit_id)

    def act(self,unit_id):
        '''Perform a complete turn for the given unit.

        :unit_id: The unit requested to act
        :return: Whether or not a target to attack exists
        '''

        target_id,target_dist = self.grid.get_nearest_enemy(unit_id)

        # no enemy is nearby
        if target_id == -1:
            return True

        # move toward the enemy
        for _ in range(self.grid.stats[unit_id,self.STAT.MOVE]):
            if target_dist==1:
                break
            self.grid.step_closer(unit_id,target_id)
            target_dist = self.grid.get_dist(unit_id,target_id)

        # the enemy is within range
        if target_dist==1: 
            self.damage_piece(unit_id,target_id)

        return False
        
    def damage_piece(self,unit_id,target_id):
        '''Apply damage to the target_id piece using the unit_id piece's DMG stat.
        
        :unit_id: The attacking unit
        :target_id: The unit receiving damage
        '''

        self.grid.stats[target_id,self.STAT.HP] -= self.grid.stats[unit_id,self.STAT.DMG]
        if self.grid.stats[target_id,self.STAT.HP] <= 0:
            self.grid.remove_piece(target_id)
            self.grid.stats[target_id,self.STAT.ALIVE] = False
            self.grid.stats[target_id,self.STAT.VISIBLE] = False