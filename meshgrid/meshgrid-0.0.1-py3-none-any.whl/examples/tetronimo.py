import numpy as np

from meshgrid.games.square import SquareGridGame
from meshgrid.shape.square import SquareShapeManager

class TetronimoGame(SquareGridGame):
    '''An example falling-tetronimo game on a sinigle square Grid.

    Falling pieces have four squares and can be rotated. Only one "active" piece
    is ever falling at one time. Once the active piece can no longer fall any 
    further, either blocked by the bottom of the Grid or another piece, they're 
    converted to four 1x1 "inactive" pieces that can be "cleared" when an entire 
    row is filled.

    Try altering this simple toy class to make more complex falling block puzzle
    games!

    Parameters
    ----------
    :grid_width: The width of the default Grid, measured in squares
    :grid_height: The height of the default Grid, measured in squares
    :colors: The colors to assign to pieces. These can be color names or hex codes
    :drop_delay: Controls the speed that pieces fall. Larger = slower.

    Methods
    -------
    :make_shape_manager: The function specifying the Shape Manager object for the game
    :rotate_piece_clockwise: Rotates the current active (aka falling) piece clockwise
    :rotate_piece_counterclockwise: Rotates the current active piece counterclockwise
    :new_active_piece: Creates a new active (aka falling) piece at the top of the Grid
    :init_inactive_pieces: Initialize the Stats for "inactive" pieces
    :make_active_piece_inactive: Convert the "active" piece to four 1x1 "inactive" pieces
    :get_new_single_block_id: Get an unused `unit_id` for a new 1x1 "inactive" piece
    :init_grid: Initialize the Grid at the start of the game
    :remove_filled_horizontal_lines: Remove inactive pieces & shift board down by a square
    :step: The function called at every "tick" of the game
    :on_notebook_key_down: If usinig a notebook-based visualizer is called on key press
    '''

    def __init__(self, grid_width, grid_height, colors, drop_delay=10, **kwargs):
        
        self.done = False
        self.drop_delay = drop_delay
        max_units = grid_width*grid_height + 1
        self.active_piece_id = 0
        self.inactive_piece_ids = slice(1,max_units,None) # every ID except the active_piece_id
        self.colors = colors
        self.shape_manager = self.make_shape_manager()

        # mappers to map between shapes when turning clockwise (cw) or counterclockwise (ccw)
        self.cw_mapper  = [0, 2, 1, 3, 7, 4, 5, 6, 11, 8, 9, 10, 15, 12, 13, 14, 17, 16, 19, 18]
        self.ccw_mapper = [0, 2, 1, 3, 5, 6, 7, 4, 9, 10, 11, 8, 13, 14, 15, 12, 17, 16, 19, 18]
        
        stats_list = ['VISIBLE','SHAPE','COLOR']
        super().__init__(grid_width, grid_height, max_units, self.shape_manager, stats_list, **kwargs)
        self.init_grid()
        self._step = 1
        
    def make_shape_manager(self):
        '''Create a Shape Manager object to be used by the game.

        Modify this function to specify the unique shapes that pieces can take
        in this game.

        :return: A Shape Manager object
        '''

        tetronimoes = []
        tetronimoes.append( np.array([[1]]) ) # the first shape is the only single 1x1 square shape
        tetronimoes.append( np.array([1]*4)[None,:] )
        tetronimoes.append( np.array([1]*4)[:,None])
        tetronimoes.append( 
            np.array([
                [1,1],
                [1,1],
            ])
        )
        tetronimoes.append( 
            np.array([
                [1,1],
                [1,0],
                [1,0],
            ])
        )
        tetronimoes.append(self._rotate_shape(tetronimoes[-1]))
        tetronimoes.append(self._rotate_shape(tetronimoes[-1]))
        tetronimoes.append(self._rotate_shape(tetronimoes[-1]))
        tetronimoes.append(np.flip(tetronimoes[-1],axis=1))
        tetronimoes.append(self._rotate_shape(tetronimoes[-1]))
        tetronimoes.append(self._rotate_shape(tetronimoes[-1]))
        tetronimoes.append(self._rotate_shape(tetronimoes[-1]))
        tetronimoes.append( 
            np.array([
                [1,0],
                [1,1],
                [1,0],
            ])
        )
        tetronimoes.append(self._rotate_shape(tetronimoes[-1]))
        tetronimoes.append(self._rotate_shape(tetronimoes[-1]))
        tetronimoes.append(self._rotate_shape(tetronimoes[-1]))
        tetronimoes.append( 
            np.array([
                [1,0],
                [1,1],
                [0,1],
            ])
        )
        tetronimoes.append(self._rotate_shape(tetronimoes[-1]))
        tetronimoes.append(np.flip(tetronimoes[-1],axis=1))
        tetronimoes.append(self._rotate_shape(tetronimoes[-1]))
        return SquareShapeManager(tetronimoes)
    
    def _rotate_shape(self,arr):
        '''Rotate a numpy array by 90 degrees.

        :arr: A numpy array
        :return: The rotated array
        '''
        
        return arr.T[::-1]
    
    def rotate_piece_clockwise(self,unit_id):
        '''Rotate a piece with the given `unit_id` 90 degrees clockwise.

        :unit_id: The unit to rotate
        :return: Whether or not the rotation was successful
        '''

        i,j = self.grid.loc[unit_id]
        old_shape = self.grid.stats[unit_id,self.STAT.SHAPE]
        new_shape = self.cw_mapper[self.grid.stats[unit_id,self.STAT.SHAPE]]

        self.grid.remove_piece(unit_id)
        
        self.grid.stats[unit_id,self.STAT.SHAPE] = new_shape
        placed = self.grid.place_piece(unit_id,i,j)
        if placed:
            return True
        else:
            self.grid.stats[unit_id,self.STAT.SHAPE] = old_shape
            self.grid.place_piece(unit_id,i,j)
            return False
    
    def rotate_piece_counterclockwise(self,unit_id):
        '''Rotate a piece with the given `unit_id` 90 degrees counterclockwise.

        :unit_id: The unit to rotate
        :return: Whether or not the rotation was successful
        '''

        i,j = self.grid.loc[unit_id]
        old_shape = self.grid.stats[unit_id,self.STAT.SHAPE]
        new_shape = self.ccw_mapper[self.grid.stats[unit_id,self.STAT.SHAPE]]

        self.grid.remove_piece(unit_id)
        
        self.grid.stats[unit_id,self.STAT.SHAPE] = new_shape
        placed = self.grid.place_piece(unit_id,i,j)
        if placed:
            return True
        else:
            self.grid.stats[unit_id,self.STAT.SHAPE] = old_shape
            self.grid.place_piece(unit_id,i,j)
            return False
    
    def new_active_piece(self):
        '''Place a new "active" piece at the top of the Board.

        :return: Whether or not the new piece was successfully placed
        '''

        # note: shape #0 is a 1x1 square used for inactive pieces, so we can't use it for the active pieces
        self.grid.stats[self.active_piece_id,self.STAT.SHAPE] = np.random.randint(1,len(self.shape.shapes))
        self.grid.stats[self.active_piece_id,self.STAT.COLOR] = np.random.randint(0,len(self.colors))
        placed = self.grid.place_piece(self.active_piece_id,0,self.grid.board.shape[1]//2)
        self.grid.stats[self.active_piece_id,self.STAT.VISIBLE] = placed
        return placed
        
    def init_inactive_pieces(self):
        '''Initialize the Stats on the "inactive" pieces.'''
        
        self.grid.stats[self.inactive_piece_ids,self.STAT.VISIBLE] = 0
        self.grid.stats[self.inactive_piece_ids,self.STAT.SHAPE] = 0 # shape #0 is a 1x1 square
        self.grid.stats[self.inactive_piece_ids,self.STAT.COLOR] = -1
    
    def make_active_piece_inactive(self):
        '''Convert the "active" piece into four 1x1 "inactive" pieces.'''
    
        new_i,new_j = np.where( self.grid.board==self.active_piece_id )
        self.grid.remove_piece(self.active_piece_id)
        self.grid.stats[self.active_piece_id,self.STAT.VISIBLE] = 0
        for i,j in zip(*(new_i,new_j)):
            new_id = self.get_new_single_block_id()
            self.grid.place_piece(new_id,i,j)
            self.grid.stats[new_id,self.STAT.VISIBLE] = 1
            self.grid.stats[new_id,self.STAT.COLOR] = self.grid.stats[self.active_piece_id,self.STAT.COLOR]
    
    def get_new_single_block_id(self):
        '''Get a new valid `unit_id` to use for a new "inactive" piece.

        :return: A new unit_id value
        '''
        
        unused_pieces = np.where(self.grid.stats[:,self.STAT.VISIBLE]==0)[0]
        unused_inactive_pieces = np.delete(unused_pieces,self.active_piece_id)
        return unused_inactive_pieces[0]

    def init_grid(self):
        '''Initialize the Grid. Used at the start of the game.'''
        
        self.grid.board[:] = -1
        self.new_active_piece()
        self.init_inactive_pieces()
        
    def remove_filled_horizontal_lines(self):
        '''Remove filled horizontal rows and drop the board down a row.'''
        
        self._move_board_down_over_filled_rows()
        self._refresh_piece_visibility_based_on_board_state()

    def _move_board_down_over_filled_rows(self):
        '''Push the board down a row. Generally used when a row is filled.'''

        filled_rows = np.where((self.grid.board!=-1).all(axis=1))[0]
        for filled_row in filled_rows:
            self.grid.board[1:filled_row+1] = self.grid.board[:filled_row]
            self.grid.board[0] = -1
        self.grid.rebuild_loc_from_board()

    def _refresh_piece_visibility_based_on_board_state(self):
        '''Resynchronize Stats for "inactive" pieces based on Board state.'''

        self.grid.stats[self.inactive_piece_ids,self.STAT.VISIBLE] = 0
        visible_pieces = self.grid.board[self.grid.board!=-1]
        self.grid.stats[visible_pieces,self.STAT.VISIBLE] = 1

    def step(self):
        '''Run for each "tick" of the game to update the game's state.

        For this game, each tick of the game involves occasionally dropping
        the "active" piece downward (based on the drop_delay value).
        '''

        self._step += 1
        if self._step % self.drop_delay == 0 and not self.done:
            success = self.grid.move_piece(self.active_piece_id,1,0)
            if not success:
                self.make_active_piece_inactive()
                placed = self.new_active_piece()
                self.remove_filled_horizontal_lines()
                if not placed:
                    self.done = True
    
    def on_notebook_key_down(self, key, shift_key, ctrl_key, meta_key):
        '''Run a function that received keyboard input & updates the game.'''
        
        if key=="ArrowRight":
            self.grid.move_piece(self.active_piece_id,0,1)
        elif key=="ArrowLeft":
            self.grid.move_piece(self.active_piece_id,0,-1)
        elif key=="ArrowUp":
            self.rotate_piece_clockwise(self.active_piece_id)
        elif key=="ArrowDown":
            self.grid.move_piece(self.active_piece_id,1,0)
            
        elif key == "Escape":
            self.done = True