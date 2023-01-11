import numpy as np

class SquareMultilayerGrid2D:
    '''A two-dimensional square-based Grid class with multiple layers.
    
    Grid objects include a Board (as a numpy array) and Pieces (represented by 
    the Loc and Stats objects). 

    This Grid class uses a two-dimensional Board with many layers. You can
    think of it as being akin to a chess board per-layer. So, if you specify
    three layers, it's as if you have three stacked chess boards.

    The three most important internal objects are:
    * Board - A 3D numpy array where the indices are `(i,j,layer)`
    * Loc - A 2D numpy array whose columns are `[i,j,layer]`
    * Stats - A 2D numpy array whose columns are specified by `STAT_ENUM`

    Parameters
    ----------
    :grid_width: The width of the Board, measured in squares
    :grid_height: The height of the Board, measured in squares
    :max_units: The maximum number of units that can be stored by Loc & Stats
    :shape_manager: A shape manager object
    :STAT_ENUM: The desired columns in the Grid's Stats object
    :layers: The number of layers to specify on the Board

    Methods
    -------
    :random_grid_locs: Returns random `(i,j)` locations for each piece (layer not specified)
    :place_pieces_randomly: Place pieces randomly, retrying on failure (layer is specified)
    :get_dist: The Manhattan distance between two unit IDs (layer is ignored)
    :get_nearest_enemy: Get the ID of the nearest living enemy piece (different side)
    :get_nearest_ally: Get the ID of the nearest living ally piece (same side)
    :move_piece: Move a piece by specifying how much to shift its `(i,j)` location
    :place_piece: Place a piece at a precise `(i,j)` location
    :remove_piece: Remove a piece by its unit ID
    :piece_can_be_placed_here: Determine if a given unit ID can be placed here
    :rebuild_loc_from_board: Clear Loc and rebuild it from piece locations on Board
    :rebuild_board_from_loc: Clear Board and rebuild it from piece locations on Loc
    :step_closer: Move one unit a single non-diagonal square closer to another unit
    '''
    
    def __init__(self,grid_width,grid_height,max_units,
                 shape_manager,STAT_ENUM,layers=1):
        
        self.loc_dims = 3 # dimensions = (i,j,layer)
        self.width = grid_width
        self.height = grid_height
        self.layers = layers
        self.max_units = max_units
        
        self.STAT = STAT_ENUM
        
        self.board = np.zeros((self.height,self.width,self.layers),dtype=np.int32)-1
        self.loc = np.zeros((max_units,self.loc_dims),dtype=np.int32)-1
        self.stats = np.zeros((max_units,len(self.STAT)),dtype=np.int32)
        self.shape = shape_manager
    
    def random_grid_locs(self):
        '''Select random locations for every possible piece, assuming pieces are 1x1.
        
        This function selects a random board location for each piece, without
        replacement. This means that no two pieces can select the same location, but
        it assumes pieces take up just a single square. If your pieces take mup more
        than one square use `place_pieces_randomly()` instead.

        :return: A Loc-like 2d numpy array of new location values for every piece
        '''
        
        choices = np.random.choice(self.width*self.height,self.max_units)
        return np.vstack((choices//self.width, choices-choices//self.width*self.width)).T

    def place_pieces_randomly(self,attempts=10,layer=0):
        '''Place pieces randomly on one layer, but highly inefficiently.
        
        This function places pieces randomly, and retries if it fails. Since it places
        pieces one-at-a-time this function is suitable for pieces that take up more than
        a 1x1 square on the Board. if your pieces take up only one square use 
        `random_grid_locs()` instead.
        
        :attempts: The number of piece placement attempts before the function errors out
        :layer: The layer to place the pieces
        '''
        
        for unit_id in range(self.stats.shape[0]):
            success = False
            for _ in range(attempts):
                i = np.random.randint(0,self.board.shape[0])
                j = np.random.randint(0,self.board.shape[1])
                if self.place_piece(unit_id,i,j,layer=layer):
                    success = True
                    break
            if not success:
                raise Exception(f"Failed to place a unit")
    
    def get_dist(self,a,b):
        '''Get the distance betwen two `(i,j)` locations (ignoring layers)
        
        :a: The first `(i,j)` location
        :b: The second `(i,j)` location
        :return: The Manhattan distance `(i_a-i_b,j_a-j_b)` between `a` and `b`
        '''
        
        return np.float64(np.sum(np.abs(self.loc[a,:-1]-self.loc[b,:-1]))) # Manhattan distance
        #return np.sum((self.loc[a,:-1]-self.loc[b,:-1])**2)   # Euclidean distance

    def get_nearest_enemy(self,unit_id,ignore_layer=False):
        '''Return the nearest unit with a different STAT.SIDE as the given unit.
        
        :unit_id: The unit ID to find the nearest enemy for
        :ignore_layer: Set to True to allow finding enemies on different layers from the unit
        :return: The ID of the nearest enemy & the distance of that enemy
        '''

        dist = float(1e10)
        best_dist = float(1e10)
        best_id = -1
        
        for _id in range(self.loc.shape[0]):
            if self.stats[_id,self.STAT.ALIVE]:                                             # no dead pieces
                if ignore_layer or (self.loc[_id,-1]==self.loc[unit_id,-1]):                # must be on same layer
                    if self.stats[_id,self.STAT.SIDE]!=self.stats[unit_id,self.STAT.SIDE]:  # only match enemies
                        dist = self.get_dist(unit_id,_id)
                        if dist < best_dist:
                            best_dist = dist
                            best_id = _id
        return best_id, best_dist

    def get_nearest_ally(self,unit_id,ignore_layer=False):
        '''Return the nearest unit with the same STAT.SIDE as the given unit.
        
        :unit_id: The unit ID to find the nearest enemy for
        :ignore_layer: Set to True to allow finding allies on different layers from the unit
        :return: The ID of the nearest ally & the distance of that ally
        '''

        dist = float(1e10)
        best_dist = float(1e10)
        best_id = -1
        
        for _id in range(self.loc.shape[0]):
            if self.stats[_id,self.STAT.ALIVE]:                                            # no dead pieces
                if ignore_layer or (self.loc[_id,-1]==self.loc[unit_id,-1]):               # must be on same layer
                    if self.stats[_id,self.STAT.SIDE]==self.stats[unit_id,self.STAT.SIDE]: # only match allies
                        if _id!=unit_id:                                                   # no self-matching
                            dist = self.get_dist(unit_id,_id)
                            if dist < best_dist:
                                best_dist = dist
                                best_id = _id
        return best_id, best_dist

    def move_piece(self,unit_id,di,dj,layer=0):
        '''Move a piece with `unit_id` to location `(i+di,j+dj)`.

        This function will check that a piece can be moved to the new location. If
        the piece was originally located at `(i,j)` then its new location is `(i+di,j+dj)`.
        
        If the piece cannot move, this function will not move the piece, and return False.
        If the piece can move, this function will move the piece and return True.

        A unit's layer can also be changed via this function.

        :unit_id: The ID of the piece to move
        :di: The change in the i-direction (vertical) for the piece
        :dj: The change in the j-direction (horizontal) for the piece
        :layer: The layer to move the piece to
        :return: A boolean value for the success or failure of the attempted move
        '''

        i,j,layer = self.loc[unit_id]
        if self.piece_can_be_placed_here(unit_id,i+di,j+dj,layer=layer):
            self._move_piece_without_checking_if_it_can_be_placed(unit_id,di,dj,layer=layer)
            return True
        else:
            return False
    
    def _move_piece_without_checking_if_it_can_be_placed(self,unit_id,di,dj,layer=None):
        '''Move a piece with `unit_id` to location `(i+di,j+dj)`, without safety checks.

        This function forcefully move a piece, even if this overwrites another piece
        occupying the same location. If the piece was originally located at `(i,j)` 
        then its new location is `(i+di,j+dj)`.

        :unit_id: The ID of the piece to move
        :di: The change in the i-direction (vertical) for the piece
        :dj: The change in the j-direction (horizontal) for the piece
        :layer: The layer to move the piece to
        '''

        si,sj = 0,0
        i,j,old_layer = self.loc[unit_id]
        new_layer = old_layer if layer is None else layer # don't move between layers if layer arg isn't specified
        shape_start = self.shape.info[self.stats[unit_id,self.STAT.SHAPE],self.shape.START]
        shape_end   = self.shape.info[self.stats[unit_id,self.STAT.SHAPE],self.shape.END]
        for s in range(shape_start,shape_end):
            si,sj = self.shape.mask[s]
            self.board[i+si,j+sj,old_layer] = -1
        for s in range(shape_start,shape_end):
            si,sj = self.shape.mask[s]
            self.board[i+si+di,j+sj+dj,new_layer] = unit_id
        self.loc[unit_id,0] += di
        self.loc[unit_id,1] += dj
        self.loc[unit_id,2] = new_layer

    def place_piece(self,unit_id,i,j,layer=0):
        '''Place a piece with `unit_id` to location `(i,j)`, optionally specifying a layer.

        This function will check that a piece can be placed at the given location.
        
        If the piece cannot be placed, this function will not place the piece, and return False.
        If the piece can be placed, this function will place the piece and return True.

        :unit_id: The ID of the piece to move
        :i: The i-location (vertical) for the piece to be placed
        :j: The j-location (horizontal) for the piece to be placed
        :layer: The layer to place the piece on
        :return: A boolean value for the success or failure of the attempted placement
        '''

        if self.piece_can_be_placed_here(unit_id,i,j,layer=layer):
            self._place_piece_without_checking_if_it_can_be_placed(unit_id,i,j,layer=layer)
            return True
        else:
            return False
            
    def _place_piece_without_checking_if_it_can_be_placed(self,unit_id,i,j,layer=0):
        '''Place a piece with `unit_id` to location `(i,j)`, without safety checks.

        This function forcefully place a piece, even if this overwrites another piece
        occupying the same location. The piece is placed to the location `(i,j)`.
        
        :unit_id: The ID of the piece to be moved
        :i: The i-location (vertical) for the piece to be placed
        :j: The j-location (horizontal) for the piece to be placed
        :layer: The layer to move the piece to
        '''
        
        si,sj = 0,0
        shape_start = self.shape.info[self.stats[unit_id,self.STAT.SHAPE],self.shape.START]
        shape_end   = self.shape.info[self.stats[unit_id,self.STAT.SHAPE],self.shape.END]
        for s in range(shape_start,shape_end):
            si,sj = self.shape.mask[s]
            self.board[i+si,j+sj,layer] = unit_id
        self.loc[unit_id,0] = i
        self.loc[unit_id,1] = j
        self.loc[unit_id,2] = layer
            
    def remove_piece(self,unit_id):
        '''Remove the piece with the given `unit_id` from the Board & from Loc.
        
        :unit_id: The piece to remove from the Board & Loc
        '''

        si,sj = 0,0
        i,j,layer = self.loc[unit_id]
        shape_start = self.shape.info[self.stats[unit_id,self.STAT.SHAPE],self.shape.START]
        shape_end   = self.shape.info[self.stats[unit_id,self.STAT.SHAPE],self.shape.END]
        for s in range(shape_start,shape_end):
            si,sj = self.shape.mask[s]
            self.board[i+si,j+sj,layer] = -1
        self.loc[unit_id,:] = -1
    
    def piece_can_be_placed_here(self,unit_id,i,j,layer=0):
        '''Check if the piece with the given `unit_id` can be placed to `(i,j)`.
        
        :unit_id: The ID of the piece to be placed
        :i: The i-location (vertical) for the piece to be placed
        :j: The j-location (horizontal) for the piece to be placed
        :blank_square: The value on the Board of an empty square
        :layer: The layer to place the piece on
        :return: A boolean value for whether or not the piece can be placed here
        '''

        if layer<0 or layer>=self.board.shape[0]:
            return False
        shape_start = self.shape.info[self.stats[unit_id,self.STAT.SHAPE],self.shape.START]
        shape_end   = self.shape.info[self.stats[unit_id,self.STAT.SHAPE],self.shape.END]
        for s in range(shape_start,shape_end):
            si,sj = self.shape.mask[s]
            if ( i+si<0 or i+si>=self.board.shape[0] or 
                 j+sj<0 or j+sj>=self.board.shape[1] ):
                return False
            elif ( self.board[i+si,j+sj,layer] != -1 and
                   self.board[i+si,j+sj,layer] != unit_id ):
                return False
        return True
    
    def rebuild_loc_from_board(self,blank_square=-1,off_board=-1):
        '''Clear Loc and fill it in using piece locations on the Board.
        
        This function is mainly used if you've edited the Board manually,
        and want to make sure Loc isn't desynchronized from the Board state.

        Note, this function rebuilds over all layers!
    
        :blank_square: The value of a blank square on the Board
        :off_board: The value assigned to Loc values when a piece has no location
        '''

        self.loc[:] = off_board
        piece_mask = (self.board!=blank_square)
        piece_ids = self.board[piece_mask]
        self.loc[piece_ids] = np.vstack(np.where(piece_mask)).T

    def rebuild_board_from_loc(self,blank_square=-1,off_board=-1):
        '''Clear Board and fill it in using piece locations on Loc.
        
        This function is mainly used if you've edited Loc manually, and
        want to make sure the Board isn't desynchronized from Loc's values.
    
        Note, this function rebuilds over all layers!

        :blank_square: The value of a blank square on the Board
        :off_board: The value assigned to Loc values when a piece has no location
        '''

        self.board[:] = blank_square
        self.board[self.loc[:,0],self.loc[:,1],self.loc[:,2]] = np.arange(self.loc.shape[0])

    def step_closer(self,unit_id,target_id):
        '''Convenience function to move one unit a single square closer to another.
        
        This function should be called repeatedly if you need to move a piece more
        than one square and want to still collide with other pieces or trigger 
        other location-based effects.

        Note that this function will prioritize moving in the further dimension
        (eg: if you're 3 squares away horizontally and 1 square away vertically,
        then this function will move you horizontally preferentially, since 3>1).

        This function does not let pieces move diagonally as a single move.

        Layers are ignored by this function.

        :unit_id: The piece on the board to move
        :target_id: The piece on the board that unit_id will move closer to
        :return: A boolean value for whether or not the piece moved successfully
        '''

        di,dj = self.loc[unit_id,:-1]-self.loc[target_id,:-1]
        if np.abs(di)>=np.abs(dj):
            if di<0:
                result = self.move_piece(unit_id,1,0) # down
            elif di>0:
                result = self.move_piece(unit_id,-1,0) # up
        else:
            if dj<0:
                result = self.move_piece(unit_id,0,1) # right
            elif dj>0:
                result = self.move_piece(unit_id,0,-1) # left
        
        return result