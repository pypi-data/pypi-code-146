import enum

class UnitIDOrderedTurnQueue():
    '''A turn queue whose ordering is based smallest-to-largest unit ID.

    Turn queues help manage which unit is currently allowed to act. Calling
    `pop()` will return the next unit ID ready to act. If a turn queue is
    emptied it automatically will refill itself with new entries.

    As an "ordered" turn queue, there is no sense of "clock time". Instead
    units are sorted by some value.

    In the case of this ordered turn queue, units are sorted by their unit ID,
    from smallest unit ID to largest. If units are grouped into two opposing
    teams then it is recommended that one team take even unit IDs, and the
    other team take odd unit IDs, to ensure initial equal turn-taking. Note 
    that this turn queue does not guarantee that teams take an equal number 
    of turns once units die! If unit ID 1 dies, then turns are given to units 
    in the following order: [0,2,3,...], which means the even team would go 
    twice in a row because unit #1 can no longer take a turn.

    This turn queue only lets units with the Stat `ALIVE=1` take actions.
    
    Parameters
    ----------
    :stats: A Stats object (a 2D numpy array) from the game's Grid object
    :STAT_ENUM: The enum used to build the `stats` object passed in the first arg
    
    Methods
    -------
    :pop: Return the ID of the next unit ready to take an in-game action
    '''
    
    def __init__(self,stats,STAT_ENUM):
        
        self.stats = stats
        self.STAT = STAT_ENUM
        self._queue = []
        self._validate_stats_enum(STAT_ENUM)

    def _validate_stats_enum(self, STAT_ENUM):
        '''Ensure that stats used by this class exist (to avoid errors).
        
        :STAT_ENUM: An enum object used to define a Grid's Stats columns
        '''
        
        if 'ALIVE' not in dir(STAT_ENUM):
            raise Exception("The following stats are required when using DiscreteTurnQueue: ALIVE")
        
    def __len__(self):
        '''The length of a turn queue object is returned as the length of its internal queue.
        
        :return: The length of the current turn queue
        '''
        
        return len(self._queue)
    
    def pop(self):
        '''Return the next unit ID ready to take an action.
        
        As is required by all turn queues, `pop()` will automatically replenish
        the internal turn queue if it ever becomes empty.

        :return: The next unit ID ready to take an action
        '''
        
        unit_id = None
        while unit_id is None:
            if len(self._queue)==0:
                self._queue = self._new_queue()
            unit_id = self._queue.pop(0)
            unit_id = self._return_None_if_unit_not_alive(unit_id)

        return unit_id
    
    def _return_None_if_unit_not_alive(self,unit_id):
        '''Determine if a unit is alive, and available to be on the queue.
        
        :unit_id: The unit ID to check for being alive
        :return: Returns None if the unit is alive, and the unit's ID otherwise
        '''

        return unit_id if self.stats[unit_id,self.STAT.ALIVE] else None
    
    def _new_queue(self):
        '''Create a new internal queue. Typically called when the queue is empty.
        
        :return: A new turn queue in the form of a python list object
        '''
        
        return [ unit_id for unit_id in range(self.stats.shape[0])
                 if self.stats[unit_id,self.STAT.ALIVE] ] 
