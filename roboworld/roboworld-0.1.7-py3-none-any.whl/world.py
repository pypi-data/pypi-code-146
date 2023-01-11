# external modules
from matplotlib.animation import FuncAnimation
from matplotlib.figure import Figure
import numpy as np

# std lib
import copy
from typing import Sequence
import random
import enum

# local modules
from roboworld.vector import D2DVector
from roboworld.visualization import MatplotVisualizer

class CellState(enum.IntEnum):
    """
    All possible states of a cell of the grid (cellular automaton).
    WALL is immovable while STONE and LEAF is moveable.
    Numbers are choosen to achieve a nice visualization.
    """

    EMPTY = 19
    WALL = 16
    LEAF = 9
    STONE = 4

    # unsed
    GOAL = 12

    # ROBO = 0,1,2,3 N,W,S,E
    # STONE = 4
    # LEAF = 9
    # Empty 19
    # WALL = 16

    def __repr__(self) -> str:
        return str(self.value)

@enum.unique
class Orientation(enum.Enum):
    """All possible orientations of robo."""

    # ccw ordered (y, x)!!!
    EAST = D2DVector(0, 1)
    NORTH = D2DVector(1, 0)
    WEST = D2DVector(0, -1)
    SOUTH = D2DVector(-1, 0)

    def next(self):
        """Rotates the current direction by 90 degrees in ccw order.

        Returns:
            Orientation: The next orientation turning the current one by 90 degrees.
        """

        if self == Orientation.EAST:
            return Orientation.NORTH
        if self == Orientation.NORTH:
            return Orientation.WEST
        if self == Orientation.WEST:
            return Orientation.SOUTH
        else:
            return Orientation.EAST

    def to_int(self) -> int:
        """Transforms the direction to to a integer.

        Returns:
            int: the integer representation of this orientation
        """

        if self == Orientation.EAST:
            return 0
        if self == Orientation.NORTH:
            return 1
        if self == Orientation.WEST:
            return 2
        else:
            return 3

    def __str__(self) -> str:
        return self.__repr__()
    
    def __repr__(self) -> str:
        """Transforms the direction to to a string.

        Returns:
            str: the string representation of this orientation
        """
        if self == Orientation.NORTH:
            return 'N'
        elif self == Orientation.SOUTH:
            return 'S'
        elif self == Orientation.EAST:
            return 'E'
        else:
            return 'W'

StateGrid = Sequence[Sequence[CellState]]

class World():    
    """
    The world the roboter is exploring.

    The world is the rectangular discrete grid of a cellular automaton.
    A cell can be in one of four CellState: EMPTY, WALL (immovable, none-traversable), STONE (moveable, none-traversable), LEAF (moveable), traversable).
    """

    def __init__(self, nrows:int, ncols:int, cells:StateGrid=None, 
                 robo_orientation=Orientation.NORTH, 
                 robo_initial_position:D2DVector=None, 
                 goal_position:D2DVector=None, 
                 nleafs:int=0) -> None:
        """
        Initializes the world in serveral ways, depending on the arguments.
        If cells==None, each cell, will be empty, that is, walkable by the roboter.
        If robo_positionn==None, the roboter position will be the center of the grid.
        If goal_position==None, the goal will be placed randomly such that it is distinct from the robo position.
        
        :param nrows: Number of rows.
        :type nrows: int
        :param cols: Number of cols.
        :type cols: int
        :param cells: Optional predefined grid.
        :type cells: StateGrid
        :param robo_orientation: Optional initial orientation of the roboter of this world. Defaults to Orientation.NORTH.
        :type robo_orientation: Orientation
        :param robo_initial_position: Optional initial position of the roboter of this world. Defaults to None.
        :type robo_initial_position: D2DVector
        :param goal_position: Optional immoveable goal position. Defaults to None.
        :type goal_position: D2DVector
        :param nleafs: Optional initial number of leafs of the roboter. Defaults to 0.
        :type nleafs: int
        
        :rtype: World
        :return: A new world
        
        :raise InvalidWorldArgumentsExeception: If the predefined grid does not match with nrows and ncols or any position is outside of the grid.
        """
            
        # generate empty grid if cell is undefined
        if cells == None:
            cells = [[CellState.EMPTY for _ in range(ncols)] for _ in range(nrows)]
        elif len(cells) != nrows or (len(cells) < 0 or len(cells[0]) != ncols):
            raise InvalidWorldArgumentsExeception(f'Invalid grid dimensions.') 

        # determine the robo position if it is undefined
        if robo_initial_position == None:
            robo_initial_position = D2DVector(nrows // 2, ncols // 2)
            
        if type(robo_initial_position) is not D2DVector:
            if isinstance(robo_initial_position, (list, tuple)):
                robo_initial_position = D2DVector(*robo_initial_position)
            else:
                raise InvalidWorldArgumentsExeception(f'Robo\'s initial position is invalid: {robo_initial_position}')

        # determine the goal position if it is undefined
        if goal_position == None:
            # determine all possible positions
            possibilities = []
            for row in range(nrows):
                for col in range(ncols):
                    if cells[row][col] == CellState.EMPTY:
                        vec = D2DVector(row, col)
                        if vec != robo_initial_position:
                            possibilities.append(vec)

            if len(possibilities) == 0:
                raise InvalidWorldArgumentsExeception(f'The goal can not be placed. No EMPTY cell available.')
            
            goal_position = possibilities[random.randint(0, len(possibilities)-1)]
                   
        self._grid : Grid = Grid(cells, goal_position)
            
        if type(goal_position) is not D2DVector:
            if isinstance(goal_position, (list, tuple)):
                goal_position = D2DVector(*goal_position)
            else:
                raise InvalidWorldArgumentsExeception(f'Robo\'s goal is invalid: {robo_initial_position}')
        
        if self._grid._is_wall_at(*robo_initial_position):
            raise InvalidWorldArgumentsExeception(f'Robo position {robo_initial_position} is outside of the ({self._grid.nrows} times {self._grid.ncols}) grid / world.') 

        self._robo : Robo = Robo(robo_initial_position, self._grid, orientation=robo_orientation, nleafs=nleafs)

    def __repr__(self) -> str:
        """
        Returns a str-representation of the robo world.
        
        :return: A string representation of the world.
        :rtype: str
        """
        return self._grid.torepr(self._robo)

    @property
    def grid(self):
        """
        Returns a deepcopy of the grid to avoid direct manipulation of it.
        
        :return: A deep-copy of the grid.
        :rtype: Grid
        """
        return copy.deepcopy(self._grid)

    @property
    def robo(self):
        """
        Returns the Robo of the world.
        
        :return: The Robo of the world.
        :rtype: RoboProxy
        """
        return RoboProxy(self._robo)

    def is_successful(self):
        """
        Returns True if and only if the Robo found its goal.
        
        :return: True if and only if the Robo found its goal.
        :rtype: bool
        """
        return self._robo.is_at_goal()

    # visualization (matplotlib is the default)
    def show(self, scale=0.5, visualizer = lambda robo, scale: MatplotVisualizer().show(robo, scale=scale)) -> Figure:
        """
        Returns a displayabel representation (a figure) of the world.
        
        :param scale: Optional scaling of the figure.
        :type scale: int
        :param visualizer: Optional function that contructs the figure.
        :type visualizer: Function (Robo, float) -> Figure
        :return: A displayabel representation (a figure) of the world.
        :rtype: Figure
        """
        fig = visualizer(self._robo, scale)
        return fig

    def animate(self, scale=0.5, animator = lambda recorder, scale: MatplotVisualizer().animate(recorder, scale=scale)) -> FuncAnimation:
        """
        Returns a displayable animation of the recorder that was lastely added to the roboter.
        A recorder records the movements and actions of the robo.
        The generated animation reflects this.
        The Animation is defined by the animator (strategy pattern)

        :param scale: Optional scaling of the figure.
        :type scale: int
        :param animator: Optional function that contructs the animation.
        :type animator: Function (Robo, float) -> FuncAnimation
        :return: A displayable animation of the recorder that was lastely added to the roboter.
        :rtype: FuncAnimation
        """
        if len(self._robo.recorders) <= 0:
            return None
        return animator(self._robo.recorders[-1], scale)

    # record the actions of the robo
    def add_recorder(self, recorder):
        """
        Adds and starts a recorder such that it will be notified about the roboters actions.
        
        :param recorder: A oberver that will records the roboters instructions.
        :type recorder: ArrayRecorder
        """
        self._robo.recorders.append(recorder)
        recorder.resume()
        recorder.notify(self._robo)
        
    def remove_recorder(self, recorder):
        """
        Removes and stops a recorder if it is actually registered.
        
        :param recorder: A oberver that currently records the roboters instructions.
        :type recorder: ArrayRecorder    
        """
        rec = self._robo.recorders.remove(recorder)
        if rec != None:
            rec.pause()
        return rec

    def remove_all_recorders(self):
        """Removes and stops all registered recorders."""
        for recorder in self._robo.recorders:
            self.remove_recorder(recorder)

    def pause_recordings(self):
        """
        Pauses all recorders.
        """
        for recorder in self._robo.recorders:
            recorder.pause()

    def resume_recordings(self):
        """
        Resumes all recorders.
        """
        for recorder in self._robo.recorders:
            recorder.resume()

    def clear_recordings(self):
        """
        Clears/resets all recorders.
        This will free the memory required for the recordings.
        """
        for recorder in self._robo.recorders:
            recorder.clear()

    # compatibility reasons
    def disable_animation(self):
        """
        Pauses and clears/resets all recorders.
        """
        self.pause_recordings()
        self.clear_recordings()

    def enable_animation(self):
        """
        Resumes all recorders (identical to resume_recordings())
        """
        self.resume_recordings()

    def get_robo(self):
        """
        Returns the Robo of the world.
        
        :return: The Robo of the world.
        :rtype: RoboProxy
        """
        return self.robo

    # static factory methods
    @staticmethod
    def corridor(length:int=10, random_headway:bool=False, nstones:int=0):
        """
        Returns a corridor (1 times length world) filled with randomly placed moveable stones.
        The roboter is placed right at the beginning of the corridor.
        There can be at most length-3 stones because there can be no at the cell occupied by the roboter and the goal.
        Furthermore at least one neighboring cell of the roboter has to be empty, otherwise the roboter is stuck (impossible task).

        :param length: Optional length of the corridor.
        :type length: int
        :param random_headway: Optional, if True the orientation of Robo is randomly choosen. Otherwise Robo is oriented towards the EAST.
        :type random_headway: bool
        :param nstones: Optional randomly placed stones.
        :type nstones: int

        :return: A (1 times length) world (corridor) containing stones.
        :rtype: World
        """
        stones = [CellState.STONE for _ in range(min(nstones, length-3))]
        emptys = [CellState.EMPTY for _ in range(length-3-len(stones))]
        combined = stones + emptys
        random.shuffle(combined)

        cells = [[CellState.EMPTY] + [CellState.EMPTY] + combined + [CellState.EMPTY]]

        robo_direction = Orientation.EAST
        if random_headway:
            robo_direction = random.choice([Orientation.NORTH, Orientation.SOUTH, Orientation.WEST, Orientation.EAST])
        return World(nrows=len(cells), ncols=len(cells[0]), cells=cells, robo_orientation=robo_direction, robo_initial_position=D2DVector(0,0), goal_position=D2DVector(0,length-1))

    @ staticmethod
    def maze():
        """
        Returns a small 6 times 13 simple maze.
        
        :return: An empty maze.
        :rtype: World
        """
        text = """N#---#---#---
-#-#-#-#-#-#-
-#-#-#-#-#-#-
-#-#-#-#-#-#-
-#-#-#-#-#-#-
---#---#---#G"""

        return World.str_to_world(text)

    @staticmethod
    def leaf_corridor(nleafs:int=0):
        """
        Returns a (1 times 7 world) corridor with 3 leafs.
        
        :return: A (1 times 7) world (corridor) containing 3 leafs.
        :rtype: World
        """
        text = """EL-LL-G"""
        return World.str_to_world(text, nleafs)

    @staticmethod
    def tunnel(tunnel_length:int=4, length:int=8, goal_at_end=True):
        """
        Returns a (3 times length) large world conisting of a tunnel.
        The tunnel is randomly placed.
        
        :param tunnel_length: Optional length of the tunnel.
        :type tunnel_length: int
        :param length: Optional length of the corridor.
        :type length: int
        :param goal_at_end: Optional either the goal is palced at the start (False) or end (True) of the tunnel.
        :type goal_at_end: bool
        :raise ValueError: If it is not possible to construct a valid world.

        :return: A corridor containing a tunnel.
        :rtype: World
        """
        if length < 2:
            raise ValueError('length < 2')

        tunnel_length = min(tunnel_length, length)

        left = random.randint(0, length-tunnel_length)
        right = random.randint(0, length-tunnel_length-left)
        walls = tunnel_length + left + right
        emptyleft = random.randint(0, length-walls)
        emptyright = length-walls-emptyleft
        
        top = [CellState.WALL for _ in range(left)] + [CellState.WALL for _ in range(tunnel_length)] + [CellState.EMPTY for _ in range(right)] 
        bottom = [CellState.EMPTY for _ in range(left)] + [CellState.WALL for _ in range(tunnel_length)] + [CellState.WALL for _ in range(right)] 

        top = [CellState.EMPTY for _ in range(emptyleft)] + top + [CellState.EMPTY for _ in range(emptyright)]
        bottom = [CellState.EMPTY for _ in range(emptyleft)] + bottom + [CellState.EMPTY for _ in range(emptyright)]

        center = [CellState.EMPTY for _ in range(length)]
        goal_col = emptyleft + left
        if random.choice([True, False]):
            top, bottom = bottom, top

        if goal_at_end:
            goal_col += tunnel_length - 1
        
        cells = [top, center, bottom]
        robo_direction = Orientation.EAST
        return World(nrows=len(cells), ncols=len(cells[0]), cells=cells, robo_orientation=robo_direction, robo_initial_position=D2DVector(1,0), goal_position=D2DVector(1,goal_col))

    @staticmethod
    def simple_slalom(lentgth:int=8, nwalls:int=3):
        """
        Returns a (3 times length) world where immovable walls are randomly placed in the center.

        :param length: Optional length of the corridor.
        :type length: int
        :param nwalls: Optional randomly placed walls.
        :type nwalls: int

        :return: A (3 times length) world where immovable walls are randomly placed in the center.
        :rtype: World
        """
        possibilities = list(range((lentgth-1)//2))
        nwalls = min(len(possibilities), nwalls)
        
        choices = []
        for _ in range(nwalls):
            index = random.randint(0,len(possibilities)-1)
            choices.append(possibilities[index])
            del possibilities[index]

        choices.sort()
        center = [CellState.EMPTY for _ in range(lentgth)]
        for i in choices:
            center[1+i*2] = CellState.WALL

        top = [CellState.EMPTY for _ in range(lentgth)]
        bottom = [CellState.EMPTY for _ in range(lentgth)]
        cells = [top, center, bottom]
        robo_direction = Orientation.EAST
        return World(nrows=len(cells), ncols=len(cells[0]), cells=cells, robo_orientation=robo_direction, robo_initial_position=D2DVector(1,0), goal_position=D2DVector(1,lentgth-1))

    @staticmethod
    def multi_slalom(lentgth:int=8, ngaps:int=3):
        """
        Returns a (3 times length) world where immovable walls are randomly placed in the center.
        In fact, the center is a wall with ngaps gaps.

        :param length: Optional number of columns of the world.
        :type length: int
        :param ngaps: Optional number of gaps within the wall.
        :type ngaps: int

        :return: A (3 times length) World where immovable walls are randomly placed in the center.
        :rtype: World
        """
        top = [CellState.EMPTY for _ in range(lentgth)]
        center = [CellState.EMPTY] + [CellState.WALL for _ in range(lentgth-2)] + [CellState.EMPTY]
        bottom = [CellState.EMPTY for _ in range(lentgth)]

        possibilities = list(range(1,lentgth-2))
        choices = []

        for _ in range(ngaps):
            index = random.randint(0,len(possibilities)-1)
            choices.append(possibilities[index])
            del possibilities[index]

        for i in choices:
            center[i] = CellState.EMPTY

        cells = [top, center, bottom]
        robo_direction = Orientation.EAST
        return World(nrows=len(cells), ncols=len(cells[0]), cells=cells, robo_orientation=robo_direction, robo_initial_position=D2DVector(1,0), goal_position=D2DVector(1,lentgth-1))

    @staticmethod
    def round_trip():
        """
        Returns a (11 times 27) world full of walls where there is only one possible round trip to traverse.
        The world contains some leafs to work with.
        
        :return: A (11 times 27) world full of walls where there is only one possible round trip to traverse.
        :rtype: World
        """
        
        text = """###########################
#GE--###-------####-------#
#-##-----#####---L--#####-#
#-#######################-#
#-#######################-#
#-#######################-#
#-#######################-#
#-##########-------######-#
#-#---######-#####-------L#
#-L-#---L----##############
###########################"""
        return World.str_to_world(text)

    @staticmethod
    def pacman():
        """
        Returns a (11 times 27) world containing a path occupied by leafs.
        The idea is that Robo should follow the leafs.
        
        :return: A (11 times 27) world containing a path occupied by leafs.
        :rtype: World
        """
        
        text = """---------------------------
-ELLLLL--------------------
------L--------------------
------LLLLLLLLLLLLLLLLLLLL-
-------------------------L-
-LLLLLLLLLLLLLLLLLLLLLL--L-
-L--------------------L--L-
-L---GLLLLLLLLLLLLLLLLL--L-
-L-----------------------L-
-LLLLLLLLLLLLLLLLLLLLLLLLL-
---------------------------"""
        return World.str_to_world(text)

    @staticmethod
    def sorting(n:int=8):
        """
        Returns a randomized (n times n+1) world where each column represents a number in a list.

        :param n: Optional Number of numbers to sort.
        :type n: int

        :return: A (n times n+1) world (corridor) containing stones.
        :rtype: World
        """
        cells = [[CellState.LEAF for _ in range(random.randint(1,n))] for _ in range(n)]
        for row in cells:
            row += [CellState.EMPTY for _ in range(1+n-len(row))]
        #random.shuffle(cells)
        return World(nrows=len(cells), ncols=len(cells[0]), cells=cells, robo_orientation=Orientation.WEST, robo_initial_position=D2DVector(0,n), goal_position=D2DVector(n-1,n))

    @staticmethod
    def game_of_life():
        """
        Returns a (10 times 9) world containing leafs forming a starting configuration for Conway's Game of Life.
        
        :return: A (10 times 9) world containing leafs forming a starting configuration for Conway's Game of Life.
        :rtype: World
        """
        text = """E---------
---L------
--LL------
-LLLL-----
LLLLLL----
LLLLLLL---
-LLLLL----
--LLL-----
---L-----G"""
        return World.str_to_world(text, len(text)) 

    @staticmethod
    def leaf_cross(nleafs:int=0):
        """
        Returns a (9 times 9) world containing leafs forming a cross.
        
        :param nleafs: Optional number of leafs the roboter has in its initial state.
        :type nleafs: int
        :return: A (9 times 9) world containing leafs forming a cross.
        :rtype: World
        """
        text = """LL-----LL
LLL---LLL
-LLL-LLL-
--LLLLL--
---LLL---
--LLLLL--
-LLL-LLL-
LLL---LLL
LLG---ELL"""
        return World.str_to_world(text, nleafs)

    def hole_maze(nrows:int=11, ncols:int=10):
        cells = [[CellState.EMPTY if row%2==0 else CellState.WALL for _ in range(ncols)] for row in range(nrows)]
        gloal_position = None
        for row in range(nrows):
            hole_index = random.randint(0, ncols-1)
            cells[row][hole_index] = CellState.EMPTY

            if row == nrows-1:
                gloal_position = D2DVector(row, hole_index)
        return World(nrows=len(cells), ncols=len(cells[0]), cells=cells, robo_orientation=Orientation.EAST, robo_initial_position=D2DVector(0,0), goal_position=gloal_position)

    @staticmethod
    def complex_maze(nrows:int=10, ncols:int=10, robo_direction:Orientation=None):
        """
        Returns a complex, randomly generated (nrows times ncols) maze.
        It is guaranteed that there is a path from the roboter to its goal.
        If robo_orientation is None, then it is choosen at random.
        Robo as well as its goal is placed at random positions.

        :param nrows: Optional Number of rows of the world.
        :type nrows: int
        :param ncols: Optional Number of columns of the world
        :type ncols: int
        :param robo_direction: Optional starting orientation of the roboter.
        :type robo_position: bool
        :raises ValueError: if the maze is too small.
        :return: A new completely empty world.
        :rtype: World

        """
    
        if nrows + ncols < 2:
            raise ValueError('nrows + ncols < 2')

        cells = [[CellState.WALL for _ in range(ncols)] for _ in range(nrows)]

        visited = [[False for _ in range(ncols)] for _ in range(nrows)]

        stack = []
        start = (np.random.randint(0, nrows), np.random.randint(0, ncols))

        def moore(pos):
            return [(pos[0]-1, pos[1]), (pos[0]-1, pos[1]+1), (pos[0], pos[1]+1), (pos[0]+1, pos[1]+1), (pos[0]+1, pos[1]), (pos[0]+1, pos[1]-1), (pos[0], pos[1]-1), (pos[0]-1, pos[1]-1)]

        def critical(pos):
            l1 = [(pos[0]-1, pos[1]), (pos[0]-1, pos[1]+1), (pos[0], pos[1]+1)]
            l2 = [(pos[0], pos[1]+1), (pos[0]+1, pos[1]+1), (pos[0]+1, pos[1])]
            l3 = [(pos[0]+1, pos[1]), (pos[0]+1, pos[1]-1), (pos[0], pos[1]-1)]
            l4 = [(pos[0], pos[1]-1), (pos[0]-1, pos[1]-1), (pos[0]-1, pos[1])]
            return [l1, l2, l3, l4]

        def contains(pos):
            return pos[0] >= 0 and pos[1] >= 0 and pos[0] < nrows and pos[1] < ncols

        def get_neighbours(position):
            return [pos for pos in [
                (position[0] + 1, position[1]),
                (position[0] - 1, position[1]),
                (position[0], position[1] + 1),
                (position[0], position[1] - 1)] if contains(pos)]

        def random_neighbour(position):
            tmp_neighbours = get_neighbours(position)
            neighbours = []
            for neighbour in tmp_neighbours:
                if not visited[neighbour[0]][neighbour[1]]:
                    neighbours.append(neighbour)

            if len(neighbours) > 0:
                return random.choice(neighbours)
            else:
                return None

        def mark(position):
            visited[position[0]][position[1]] = True
            cells[position[0]][position[1]] = CellState.EMPTY
            for nh in moore(position):
                test_positions = critical(nh)
                for test_pos in test_positions:
                    if all(map(lambda e: contains(e) and cells[e[0]][e[1]] == CellState.EMPTY, test_pos)):
                        visited[nh[0]][nh[1]] = True
                        cells[nh[0]][nh[1]] = CellState.WALL
                        break

        stack.append(start)
        end = start
        max_distance = 0
        while len(stack) > 0:
            next = random_neighbour(stack[-1])
            # dead end
            if next == None:
                stack.pop()
            else:
                mark(next)
                stack.append(next)
                if max_distance < len(stack):
                    max_distance = len(stack)
                    end = next

        if robo_direction == None:
            robo_direction = random.choice([Orientation.NORTH, Orientation.SOUTH, Orientation.WEST, Orientation.EAST])

        cells[start[0]][start[1]] = CellState.EMPTY
        cells[end[0]][end[1]] = CellState.EMPTY
        return World(nrows=len(cells), ncols=len(cells[0]), cells=cells, robo_orientation=robo_direction, robo_initial_position=D2DVector(start[0], start[1]), goal_position=D2DVector(end[0], end[1]))

    @staticmethod
    def str_to_world(text: str, nleafs=0):
        """
        Returns a world by parsing a string that represents the world.
        Single characters have the following semantic:

        #: (immovable) WALL
        
        G: Goal position
        
        N: Robo position (orientation==NORTH)
        
        S: Robo position (orientation==SOUTH)
        
        W: Robo position (orientation==WEST)
        
        E: Robo position (orientation==EAST)
        
        R: Robo position (random orientation)
        
        O: STONE
        
        L: LEAF
        
        Everything else: EMPTY
        
        :param text: Representation of the world.
        :type text: str
        :param nleafs: Optional number of leafs the roboter has in its initial state.
        :type nleafs: int
        :return: A world constructed from its string representation.
        :rtype: World
        """

        cells = []
        robo_direction = Orientation.EAST
        robo_position = None
        goal_position = None
        for row, line in enumerate(text.splitlines()):
            cells.append([])
            for col, c in enumerate(line):
                if c in ['N', 'S', 'E', 'W', 'R']:
                    state = CellState.EMPTY
                    robo_position = D2DVector(row, col)
                    if c == 'N':
                        robo_direction = Orientation.NORTH
                    elif c == 'S':
                        robo_direction = Orientation.SOUTH
                    elif c == 'W':
                        robo_direction = Orientation.WEST
                    elif c == 'E':
                        robo_direction = Orientation.EAST
                    else:
                        robo_direction = random.choice(
                            [Orientation.NORTH, Orientation.SOUTH, Orientation.WEST, Orientation.EAST])
                elif c == '#':
                    state = CellState.WALL
                elif c == 'G':
                    state = CellState.EMPTY
                    goal_position = D2DVector(row, col)
                elif c == 'O':
                    state = CellState.STONE
                elif c == 'L':
                    state = CellState.LEAF
                else:
                    state = CellState.EMPTY
                cells[row].append(state)
        return World(nrows=len(cells), ncols=len(cells[0]), cells=cells, robo_orientation=robo_direction, robo_initial_position=robo_position, goal_position=goal_position, nleafs=nleafs)

class Grid():
    """
    The grid the roboter is exploring.
    The difference between a Grid and a World is that, Grid does not know Robo or the rules of the World.
    Grid just helps accessing the state of each cell.

    The grid similar to two-dimensional a cellular automaton.
    A cell of the grid can be in one of four CellState: EMPTY, WALL, STONE, LEAF.
    """

    def __init__(self, cells:StateGrid, goal_position:D2DVector) -> None:
        """
        Initializes the (perceivable) grid of the robo world.
        
        :param cells: Pure cell state data (i.e. the Grid's data without methods).
        :type cells: Sequence[Sequence[CellState]]
        :param goal_position: Immoveable goal position.
        :type goal_position: D2DVector
        
        :rtype: Grid
        :return: A new grid.
        """

        if len(cells) == 0 or len(cells[0]) == 0:
            raise InvalidWorldArgumentsExeception(f'Invalid grid dimensions.')
        
        self.ncols : int = len(cells[0])
        self.nrows : int = len(cells)
        self.cells : StateGrid = cells

        if self._is_wall_at(goal_position[0], goal_position[1]):
            raise InvalidWorldArgumentsExeception(f'Goal at {goal_position} is outside of the world of dimension {self.nrows} times {self.ncols}.')

        self.goal_position : D2DVector = goal_position
        self.marks = [[False for _ in range(self.ncols)] for _ in range(self.nrows)]

    def __repr__(self) -> str:
        """Returns a str-representation of the robo world."""
        return self.torepr()

    def torepr(self, robo=None) -> str:
        """Returns a str-representation of the grid including the robo."""
        representation = ''
        for row in range(self.nrows-1,-1,-1):
            for col in range(self.ncols):
                state = self.cells[row][col]
                char = "-"
                if robo != None and robo._is_at(row, col):
                    char = robo._char()
                elif self.goal_position == D2DVector(row, col):
                    char = 'G'
                elif state == CellState.WALL:
                    char = '#'
                elif state == CellState.STONE:
                    char = 'O'
                elif state == CellState.LEAF:
                    char = 'L'
                else:
                    char = '-'
                representation += char
            representation += '\n'
        return representation.strip()

    ## proteced methods

    def _get_state(self, row: int, col: int) -> CellState:
        """Returns the state of the cell at (row, col)."""
        return self.cells[row][col]

    def _set_state(self, row: int, col: int, state: CellState):
        """Sets the state of the cell at (row, col)."""
        self.cells[row][col] = state

    #def _is_robo_at(self, row, col):
    #    """Returns true if and only if the roboter is at (row, col)."""
    #    return self._get_state(row, col) == CellState.ROBO or self._get_state(row, col) == CellState.ROBO_AT_GOAL

    def _is_stone_at(self, row: int, col: int):
        """Returns true if and only if a moveable stone is at (row, col)."""
        return self._get_state(row, col) == CellState.STONE

    def _is_leaf_at(self, row: int, col: int):
        """Returns true if and only if a moveable LEAF is at (row, col)."""
        return self._get_state(row, col) == CellState.LEAF

    def _is_wall_at(self, row: int, col: int):
        """Returns true if and only if (row, col) is outside of the world."""
        return row >= self.nrows or col >= self.ncols or self._get_state(row, col) == CellState.WALL

    def _is_goal_at(self, row: int, col: int):
        """Returns true if and only if (row, col) is at the goal of the world."""
        return self.goal_position[0] == row and self.goal_position[1] == col

    def _is_impassable(self, row: int, col: int):
        """Returns true if and only if (row, col) is occupied by a stone, obstacle or the wall (i.e. outside of the world)."""
        return self._is_stone_at(row, col) or self._is_wall_at(row, col)

    def _is_occupied(self, row: int, col: int) -> bool:
        """Returns true if and only if (row, col) is occupied by a leaf, stone, obstacle or the wall (i.e. outside of the world)."""
        return self._is_impassable(row, col) or self._is_leaf_at(row, col)

    def _remove_stone_at(self, row: int, col: int) -> CellState:
        """
        Removes a stone at (row, col) and returns it if it is there.
        Otherwise an exception is raised.
        """
        if self._is_stone_at(row, col):
            result = self._get_state(row, col)
            self._set_state(row, col, CellState.EMPTY)
            return result
        else:
            raise StoneMissingException()

    def _set_stone_at(self, row: int, col: int):
        if self._is_occupied(row, col):
            raise CellOccupiedException()
        else:
            self._set_state(row, col, CellState.LEAF)

    def _set_stone_at(self, row: int, col: int):
        if self._is_occupied(row, col):
            raise CellOccupiedException()
        else:
            self._set_state(row, col, CellState.STONE)

    def _set_leaf_at(self, row: int, col: int):
        if self._is_occupied(row, col):
            raise CellOccupiedException()
        else:
            self._set_state(row, col, CellState.LEAF)

    def _set_mark_at(self, row: int, col: int):
        self.marks[row][col] = True

    def _remove_leaf_at(self, row: int, col: int) -> CellState:
        """Removes a leaf from the position (row, col) and returns CellState.LEAF."""
        if self._is_leaf_at(row, col):
            result = self._get_state(row, col)
            self._set_state(row, col, CellState.EMPTY)
            return result
        else:
            raise LeafMissingException()

    def _unset_mark_at(self, row: int, col: int):
        self.marks[row][col] = False

    def _is_mark_at(self, row: int, col: int):
        return self.marks[row][col]
    
    ## private methods

    def __find_cell(self, *states):
        for i, col in enumerate(self.cells):
            for j, cell in enumerate(col):
                for state in states:
                    if cell == state:
                        return (i, j)
        return None

class Robo():
    """
    A representation of the roboter of the robo world.

    A roboter occupies exactly one cell. It can pick up and carray at most one moveable stone.
    Stones can only put at empty cells.
    Robo can turn by 90 degree to the left.
    It can only analyse the cell directly in front, therefore, it has an orientation (headway).
    It can mark and unmark cells it occupies but can only spot marks in front.
    """

    def __init__(self, position:D2DVector, grid: Grid, orientation: Orientation=Orientation.EAST, print_actions: bool=True, nleafs: int = 0) -> None:
        """
        Initializes a new Robo.
        
        :position nrows: Initial position of Robo.
        :type position: D2DVector
        :param grid: The grid Robo can sensor and manipulate.
        :type grid: Grid
        :param orientation: Optional initial orientation of the roboter of this world. Defaults to Orientation.EAST.
        :type orientation: Orientation
        :param print_actions: Optional If False there will be no printing of Robo's actions.
        :type print_actions: bool
        :param nleafs: Optional initial number of leafs of Robo.
        :type nleafs: int
        
        :rtype: Robo
        :return: A new Robo
        """
        
        self.grid : Grid = grid
        self.position : D2DVector = position
        self.orientation : Orientation = orientation
        self.stone : CellState = None
        self.nmarks : int = 0
        self.nleafs : int = nleafs
        self.print_actions : bool = print_actions
        self.recorders = []

    def __repr__(self) -> str:
        """Returns a str-representation of the roboter."""
        return f'position = {self.position}, orientation = {self.orientation}.'

    def notify_recorders(self):
        for recorder in self.recorders:
            recorder.notify(self)

    def disable_print(self):
        """Deactivates the printing."""
        self.print_actions = False

    def enable_print(self):
        """Activates the printing."""
        self.print_actions = True

    # non-privates
    def is_stone_in_front(self) -> bool:
        """
        Returns True if and only if there is a stone in front of robo.
        
        :return: True if and only if there is a stone in front of robo.
        :rtype: bool
        """
        return self.is_front_clear() and self.__get_state_at(self.orientation) == CellState.STONE

    def take_stone_in_front(self) -> None:
        """
        Takes a stone that is in front.
        
        :raises SpaceIsFullException: If Robo does already carry a stone.
        :raises WallInFrontException: If there is a wall in front, i.e., no stone.
        :raises LeafInFrontException: If there is a leaf in front.
        :raises StoneMissingException: If there is no stone in front.
        """
        if self.stone != None:
            raise SpaceIsFullException()
        if self.is_wall_in_front():
            raise WallInFrontException()
        if self.is_leaf_in_front():
            raise LeafInFrontException()
        if not self.is_stone_in_front():
            raise StoneMissingException()
        self.stone = self.grid._remove_stone_at(*self.__front())
        self.__print(f'take stone at {self.__front()}')
        self.notify_recorders()

    def put_stone_in_front(self) -> None:
        """
        Puts the carrying stone down in front.
        
        :raises SpaceIsEmptyException: If Robo does not carry a stone.
        :raises WallInFrontException: If there is a wall in front, i.e., no stone.
        :raises StoneInFrontException: If there is another stone in front.
        :raises LeafInFrontException: If there is a leaf in front.
        """
        if not self.is_carrying_stone():
            raise SpaceIsEmptyException()
        if self.is_wall_in_front():
            raise WallInFrontException()
        if self.is_stone_in_front():
            raise StoneInFrontException()
        if self.is_leaf_in_front():
            raise LeafInFrontException()

        self.grid._set_stone_at(*self.__front())
        self.__print(f'put stone at {self.__front()}')
        self.stone = None
        self.notify_recorders()

    def put_leaf(self) -> None:
        """
        Puts a leaf at Robo's current position.
        
        :raises NoMoreLeafsException: If Robo does not carry any leaf.
        :raises CellOccupiedException: If there is an object (leaf, wall, stone) at the current cell.
        """
        if not self.is_carrying_leafs():
            raise NoMoreLeafsException()

        self.grid._set_leaf_at(*self.position)
        self.__print(f'put leaf at {self.__front()}')
        self.nleafs -= 1
        self.notify_recorders()
        
    def take_leaf(self) -> None:
        """
        Takes a leaf at Robo's current position.
        
        :raises LeafMissingException: If there is no leaf the Robo's position.
        """
        self.grid._remove_leaf_at(*self.position)
        self.__print(f'take leaf at {self.position}')
        self.nleafs += 1
        self.notify_recorders()

    def is_carrying_leafs(self):
        """
        Returns True if and only if thre the robo carries any leafs.
        
        :return: True if and only if thre the robo carries any leafs.
        :rtype: bool
        """
        return self.nleafs > 0

    def is_front_clear(self) -> bool:
        """
        Returns True if and only if thre is no wall in front, i.e., no (immoveable) wall and not the boundary of the world.
        
        :return: True if and only if thre is no wall in front, i.e., no (immoveable) wall and not the boundary of the world.
        :rtype: bool
        """
        return not self.is_wall_in_front()

    def is_leaf_in_front(self) -> bool:
        """
        Returns True if and only if thre is a leaf in front.
        
        :return: True if and only if thre is a leaf in front.
        :rtype: bool
        """
        return self.is_front_clear() and self.__get_state_at(self.orientation) == CellState.LEAF

    def is_mark_in_front(self) -> bool:
        """
        Returns True if and only if there is a mark in front.
        
        :return: True if and only if there is a mark in front.
        :rtype: bool
        """
        return self.is_front_clear() and self.__is_mark_at(self.orientation)

    def is_wall_in_front(self) -> bool:
        """
        Returns True if and only if there is an (immoveable) wall or the boundary of the world in front.
        
        :return: True if and only if there is an (immoveable) wall or the boundary of the world in front.
        :rtype: bool
        """
        return not self.__is_reachable(self.orientation)

    def move(self) -> D2DVector:
        """
        Moves Robo one cell ahead.
        
        :raises WallInFrontException: If there is an (immoveable, not traverseable) wall in front (WALL or boundary of the world).
        :raises StoneInFrontException: If there is a stone (moveable, not traverseable) in front.
        :return: Robo's new position.
        :rtype: D2DVector
        """
        before = self.position
        if self.is_wall_in_front():
            raise WallInFrontException()
        if self.is_stone_in_front():
            raise StoneInFrontException()
        self.position += self.orientation.value
        #self._world._move_robo(before, self._position)

        #self._world._push()
        self.__print(f'move {before} -> {self.position}')
        self.notify_recorders()
        return self.position

    def set_mark(self) -> None:
        """Marks the current cell, i.e., position."""
        self.grid._set_mark_at(*self.position)
        self.__print(f'mark {self.position}')
        self.notify_recorders()

    def unset_mark(self) -> None:
        """Unmarks the current cell, i.e., position."""
        self.grid._unset_mark_at(self.position[0], self.position[1])
        self.__print(f'remove mark at {self.position}')
        self.notify_recorders()

    def is_carrying_stone(self) -> bool:
        """
        Returns True if and only if robo is carrying a stone.
        
        :return: True if and only if robo is carrying a stone.
        :rtype: bool
        """
        return self.stone != None

    def turn_left(self) -> None:
        """
        Robo turns 90 degrees to the left (counter-clockwise order NORTH->WEST->SOUTH->EAST).
        """
        before = self.orientation
        self.orientation = self.orientation.next()
        self.__print(f'turn {before} -> {self.orientation}')
        self.notify_recorders()

    def is_facing_north(self) -> bool:
        """
        Returns True if and only if robo is oriented towords the north.
        
        :return: True if and only if robo is oriented towords the north.
        :rtype: bool
        """
        return self.orientation == Orientation.NORTH

    def toss(self) -> bool:
        """
        Returns randomly True or False.
        
        :return: Either True or False by chance 50/50.
        :rtype: bool
        """
        toss = random.randint(0, 1) == 1
        self.__print(f'toss {toss}')
        return toss

    def is_at_goal(self):
        """
        Returns True if and only if robo is standing at the goal.
        
        :return: True if and only if robo is standing at the goal.
        :rtype: bool
        """
        return self.grid._is_goal_at(self.position[0], self.position[1])

    ## protected methods
    def _char(self):
        return str(self.orientation)

    def _is_at(self, row, col):
        """Returns true if and only if the roboter is at (row, col)."""
        return self.position[0] == row and self.position[1] == col

    ## private methods
    def __print(self, fstring: str):
        if self.print_actions:
            print(fstring)

    def __get_state_at(self, direction: Orientation) -> CellState:
        y, x = self.position
        if direction == Orientation.WEST:
            return self.grid._get_state(y, x-1)
        elif direction == Orientation.EAST:
            return self.grid._get_state(y, x+1)
        elif direction == Orientation.NORTH:
            return self.grid._get_state(y+1, x)
        else:
            return self.grid._get_state(y-1, x)

    def __is_mark_at(self, direction: Orientation) -> bool:
        y, x = self.position
        if direction == Orientation.WEST:
            return self.grid._is_mark_at(y, x-1)
        elif direction == Orientation.EAST:
            return self.grid._is_mark_at(y, x+1)
        elif direction == Orientation.NORTH:
            return self.grid._is_mark_at(y+1, x)
        else:
            return self.grid._is_mark_at(y-1, x)

    def __is_reachable(self, direction: Orientation) -> bool:
        y, x = self.position
        if direction == Orientation.WEST:
            return x-1 >= 0 and self.grid._get_state(y, x-1) != CellState.WALL
        elif direction == Orientation.EAST:
            return x+1 < self.grid.ncols and self.grid._get_state(y, x+1) != CellState.WALL
        elif direction == Orientation.NORTH:
            return y+1 < self.grid.nrows and self.grid._get_state(y+1, x) != CellState.WALL
        else:
            return y-1 >= 0 and self.grid._get_state(y-1, x) != CellState.WALL

    def __front(self) -> D2DVector:
        return self.position + self.orientation.value

    def __back(self):
        return self.position - self.orientation.value

    # These methods should be implemented by the students in excercises!
    def __turn(self) -> int:
        self.turn_left()
        self.turn_left()
        return 2

    def __turn_right(self) -> int:
        self.turn_left()
        self.turn_left()
        self.turn_left()
        return 3

    def __turn_to_north(self) -> int:
        turns = 0
        while not self.is_facing_north():
            self.turn_left()
            turns += 1
        return turns

    def __turn_to_south(self) -> int:
        turns = self.__turn_to_north()
        turns += self.__turn()
        return turns

    def __turn_to_east(self) -> int:
        turns = self.__turn_to_south()
        self.turn_left()
        return turns + 1

    def __turn_to_west(self) -> int:
        turns = self.__turn_to_north()
        self.turn_left()
        return turns + 1

    def __reverse_turns(self, turns: int):
        for _ in range(4 - (turns % 4)):
            self.turn_left()

    def __is_wall_at(self, direction: Orientation) -> bool:
        if direction == Orientation.NORTH:
            turns = self.__turn_to_north()
        elif direction == Orientation.EAST:
            turns = self.__turn_to_east()
        elif direction == Orientation.SOUTH:
            turns = self.__turn_to_south()
        else:
            turns = self.__turn_to_west()
        result = self.is_wall_in_front()
        self.__reverse_turns(turns)
        return result

    def __is_wall_at_west(self) -> bool:
        return self.__is_wall_at(Orientation.WEST)

    def __is_wall_at_east(self) -> bool:
        return self.__is_wall_at(Orientation.EAST)

    def __is_wall_at_north(self) -> bool:
        return self.__is_wall_at(Orientation.NORTH)

    def __is_wall_at_south(self) -> bool:
        return self.__is_wall_at(Orientation.SOUTH)

    def __move_west(self):
        self.__turn_to_west()
        return self.move()

    def __move_east(self):
        self.__turn_to_east()
        return self.move()

    def __move_north(self):
        self.__turn_to_north()
        return self.move()

    def __move_south(self):
        self.__turn_to_south()
        return self.move()

    # methods for testing
    def __get_direction(self):
        return self.orientation

class RoboProxy:
    def __init__(self, robo: Robo):
        self._robo = robo

    def __repr__(self) -> str:
        """
        Returns a str-representation of the roboter.
        """
        return self._robo.__repr__()

    def disable_print(self) -> None:
        """
        Deactivates the printing of executed Robo-instructions
        """
        self._robo.print_actions = False

    def enable_print(self) -> None:
        """
        Activates the printing of executed Robo-instructions.
        """
        self._robo.print_actions = True

    # methods that can be used by the learners
    def take_stone_in_front(self) -> None:
        """
        Takes a stone that is in front.
        
        :raises SpaceIsFullException: If Robo does already carry a stone.
        :raises WallInFrontException: If there is a wall in front, i.e., no stone.
        :raises LeafInFrontException: If there is a leaf in front.
        :raises StoneMissingException: If there is no stone in front.
        """
        self._robo.take_stone_in_front()

    def put_stone_in_front(self) -> None:
        """
        Puts the carrying stone down in front.
        
        :raises SpaceIsEmptyException: If Robo does not carry a stone.
        :raises WallInFrontException: If there is a wall in front, i.e., no stone.
        :raises StoneInFrontException: If there is another stone in front.
        :raises LeafInFrontException: If there is a leaf in front.
        """
        self._robo.put_stone_in_front()

    def is_leaf_in_front(self) -> bool:
        """
        Returns True if and only if thre is a leaf in front.
        
        :return: True if and only if thre is a leaf in front.
        :rtype: bool
        """
        return self._robo.is_leaf_in_front()

    def is_front_clear(self) -> bool:
        """
        Returns True if and only if thre is no wall in front, i.e., no (immoveable) wall and not the boundary of the world.
        
        :return: True if and only if thre is no wall in front, i.e., no (immoveable) wall and not the boundary of the world.
        :rtype: bool
        """
        return self._robo.is_front_clear()

    def is_mark_in_front(self) -> bool:
        """
        Returns True if and only if there is a mark in front.
        
        :return: True if and only if there is a mark in front.
        :rtype: bool
        """
        return self._robo.is_mark_in_front()

    def is_wall_in_front(self) -> bool:
        """
        Returns True if and only if there is an (immoveable) wall or the boundary of the world in front.
        
        :return: True if and only if there is an (immoveable) wall or the boundary of the world in front.
        :rtype: bool
        """
        return self._robo.is_wall_in_front()

    def is_stone_in_front(self) -> bool:
        """
        Returns True if and only if there is a stone in front of robo.
        
        :return: True if and only if there is a stone in front of robo.
        :rtype: bool
        """
        return self._robo.is_stone_in_front()

    def is_carrying_leafs(self) -> bool:
        """
        Returns True if and only if thre the robo carries any leafs.
        
        :return: True if and only if thre the robo carries any leafs.
        :rtype: bool
        """
        return self._robo.is_carrying_leafs()

    def put_leaf(self) -> None:
        """
        Puts a leaf at Robo's current position.
        
        :raises NoMoreLeafsException: If Robo does not carry any leaf.
        :raises CellOccupiedException: If there is an object (leaf, wall, stone) at the current cell.
        """
        self._robo.put_leaf()
        
    def take_leaf(self) -> None:
        """
        Takes a leaf at Robo's current position.
        
        :raises LeafMissingException: If there is no leaf the Robo's position.
        """
        self._robo.take_leaf()

    def move(self) -> D2DVector:
        """
        Moves Robo one cell ahead.
        
        :raises WallInFrontException: If there is an (immoveable, not traverseable) wall in front (WALL or boundary of the world).
        :raises StoneInFrontException: If there is a stone (moveable, not traverseable) in front.
        :return: Robo's new position.
        :rtype: D2DVector
        """
        return self._robo.move()
    
    @property
    def position(self) -> D2DVector:
        return self._robo.position

    def set_mark(self) -> None:
        """
        Marks the current cell, i.e., position.
        """
        self._robo.set_mark()

    def unset_mark(self) -> None:
        """
        Unmarks the current cell, i.e., position.
        """
        self._robo.unset_mark()

    def is_carrying_stone(self) -> bool:
        """
        Returns True if and only if robo is carrying a stone.
        
        :return: True if and only if robo is carrying a stone.
        :rtype: bool
        """
        return self._robo.is_carrying_stone()

    def turn_left(self) -> None:
        """
        Robo turns 90 degrees to the left (counter-clockwise order NORTH->WEST->SOUTH->EAST).
        """
        self._robo.turn_left()

    def is_facing_north(self) -> bool:
        """
        Returns True if and only if robo is oriented towords the north.
        
        :return: True if and only if robo is oriented towords the north.
        :rtype: bool
        """
        return self._robo.is_facing_north()

    def toss(self) -> bool:
        """
        Returns randomly True or False.
        
        :return: Either True or False by chance 50/50.
        :rtype: bool
        """
        return self._robo.toss()

    def is_at_goal(self) -> bool:
        """
        Returns True if and only if robo is standing at the goal.
        
        :return: True if and only if robo is standing at the goal.
        :rtype: bool
        """
        return self._robo.is_at_goal()
    
class RoboException(Exception):
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)


class InvalidWorldArgumentsExeception(Exception):
    def __init__(self, message="Invalid world arguments."):
        self.message = message
        super().__init__(self.message)


class CellOccupiedException(RoboException):
    def __init__(self, message="There something in the way."):
        self.message = message
        super().__init__(self.message)

class WallInFrontException(RoboException):
    def __init__(self, message="There is a wall in front."):
        self.message = message
        super().__init__(self.message)

class LeafInFrontException(RoboException):
    def __init__(self, message="There is a leaf in front."):
        self.message = message
        super().__init__(self.message)

class LeafMissingException(RoboException):
    def __init__(self, message="There is no leaf at the current position."):
        self.message = message
        super().__init__(self.message)

class NoMoreLeafsException(RoboException):
    def __init__(self, message="Robo does not carry any more leafs."):
        self.message = message
        super().__init__(self.message)

class StoneMissingException(RoboException):
    def __init__(self, message="There is no stone in front that can be taken."):
        self.message = message
        super().__init__(self.message)


class StoneInFrontException(RoboException):
    def __init__(self, message="The space in front is occupied by a stone."):
        self.message = message
        super().__init__(self.message)


class SpaceIsFullException(RoboException):
    def __init__(self, message="The space is occupied by something."):
        self.message = message
        super().__init__(self.message)


class SpaceIsEmptyException(RoboException):
    def __init__(self, message="There is nothing to pick up."):
        self.message = message
        super().__init__(self.message)