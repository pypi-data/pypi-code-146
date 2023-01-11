__version__ = '0.1.7'
__author__ = 'Benedikt Zoennchen'

# external modules
from IPython.display import HTML, display

# local modules
from roboworld.world import World
from roboworld.visualization import ArrayRecorder
from roboworld.vector import D2DVector
from roboworld.world import RoboProxy as Robo

def animate(world: World) -> any:
    """
    Displays an animation of the world in a Jupyter notebook.

    :param length: The world that will be animated.
    :type length: World
    """
    anim = world.animate()
    if anim != None:
        display(HTML(anim.to_jshtml()))

# Factory methods
def leaf_corridor() -> World:
    """
    Returns a (1 times 7 world) corridor with 3 leafs.
    
    :return: A (1 times 7) world (corridor) containing 3 leafs.
    :rtype: World
    """
    world =  World.leaf_corridor()
    world.add_recorder(ArrayRecorder())
    return world

def corridor(length=10, random_headway=False, nstones=0) -> World:    
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
    world =  World.corridor(length=length, random_headway=random_headway, nstones=nstones)
    world.add_recorder(ArrayRecorder())
    return world

def simple_slalom(length:int=8, nwalls:int=3) -> World:
    """
    Returns a (3 times length) world where immovable walls are randomly placed in the center.

    :param length: Optional length of the corridor.
    :type length: int
    :param nwalls: Optional randomly placed walls.
    :type nwalls: int

    :return: A (3 times length) world where immovable walls are randomly placed in the center.
    :rtype: World
    """
    world =  World.simple_slalom(length, nwalls)
    world.add_recorder(ArrayRecorder())
    return world


def multi_slalom(lentgth:int=8, ngaps:int=3) -> World:    
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
    world =  World.multi_slalom(lentgth, ngaps)
    world.add_recorder(ArrayRecorder())
    return world

def round_trip() -> World:
    """
    Returns a (11 times 27) world full of walls where there is only one possible round trip to traverse.
    The world contains some leafs to work with.
    
    :return: A (11 times 27) world full of walls where there is only one possible round trip to traverse.
    :rtype: World
    """
    world =  World.round_trip()
    world.add_recorder(ArrayRecorder())
    return world

def pacman() -> World:
    """
    Returns a (11 times 27) world containing a path occupied by leafs.
    The idea is that Robo should follow the leafs.
    
    :return: A (11 times 27) world containing a path occupied by leafs.
    :rtype: World
    """
    world =  World.pacman()
    world.add_recorder(ArrayRecorder())
    return world

def game_of_life() -> World:
    """
    Returns a (10 times 9) world containing leafs forming a starting configuration for Conway's Game of Life.
    
    :return: A (10 times 9) world containing leafs forming a starting configuration for Conway's Game of Life.
    :rtype: World
    """
    world =  World.game_of_life()
    world.add_recorder(ArrayRecorder())
    return world

def leaf_cross(nleafs:int=0) -> World:
    """
    Returns a (9 times 9) world containing leafs forming a cross.
    
    :param nleafs: Optional number of leafs the roboter has in its initial state.
    :type nleafs: int
    :return: A (9 times 9) world containing leafs forming a cross.
    :rtype: World
    """
    world =  World.leaf_cross(nleafs)
    world.add_recorder(ArrayRecorder())
    return world

def sorting(n:int=8) -> World:
    """
    Returns a randomized (n times n+1) world where each column represents a number in a list.

    :param n: Optional Number of numbers to sort.
    :type n: int

    :return: A (n times n+1) world (corridor) containing stones.
    :rtype: World
    """
    world =  World.sorting(n)
    world.add_recorder(ArrayRecorder())
    return world

def tunnel(tunnel_length:int=4, length:int=8, goal_at_end=True) -> World:
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
    world =  World.tunnel(tunnel_length, length, goal_at_end)
    world.add_recorder(ArrayRecorder())
    return world

def maze() -> World:
    """
    Returns a small 6 times 13 simple maze.
    
    :return: An empty maze.
    :rtype: World
    """
    world = World.maze()
    world.add_recorder(ArrayRecorder())
    return world

def str_to_world(text:str, nleafs:int=0) -> World:
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
    
    world = World.str_to_world(text)
    world.add_recorder(ArrayRecorder())
    return world

def new_world(nrows=5, ncols=9, robo_position=None, goal_position=None) -> World:
    """
    Returns a new empty world.
    If goal_position is None, then it is placed randomly.
    If robo_position is None, then it is placed in the center of the world.

    :param nrows: Number of rows of the world.
    :type nrows: int
    :param ncols: Number of columns of the world
    :type ncols: int
    :param robo_position: Optional starting position of the roboter
    :type robo_position: D2DVector
    :param goal_position: Optional position of roboter's goal
    :type goal_position: D2DVector
    :return: A new completely empty world.
    :rtype: World

    """
    world = World(nrows=nrows, ncols=ncols, robo_initial_position=robo_position, goal_position=goal_position)
    world.add_recorder(ArrayRecorder())
    return world


def complex_maze(nrows=10, ncols=10, robo_orientation=None) -> World:
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
    world = World.complex_maze(nrows=nrows, ncols=ncols, robo_direction=robo_orientation)
    world.add_recorder(ArrayRecorder())
    return world

worlds = {
    complex_maze.__name__ : complex_maze(),
    new_world.__name__ : new_world(),
    str_to_world.__name__ : str_to_world("E-LL--G"),
    maze.__name__ : maze(),
    tunnel.__name__ : tunnel(),
    sorting.__name__ : sorting(),
    leaf_cross.__name__ : leaf_cross(),
    game_of_life.__name__ : game_of_life(),
    pacman.__name__ : pacman(),
    round_trip.__name__ : round_trip(),
    multi_slalom.__name__ : multi_slalom(),
    simple_slalom.__name__ : simple_slalom(),
    corridor.__name__ : corridor(),
    leaf_corridor.__name__ : leaf_corridor()
}