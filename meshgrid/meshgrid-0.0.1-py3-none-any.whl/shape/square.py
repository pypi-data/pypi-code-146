import numpy as np
from typing import List

class SquareShapeManager:
    '''A Shape Manager class for square Grids.

    Shape managers store how to draw grid-based pieces on to a Grid's board.
    Different shape managers may have different strengths and drawbacks, such
    as not being able to draw certain piece shapes, or being faster or slower
    than other shape managers.

    Shapes are handed to shape managers in the form of a list of numpy arrays
    of an `int` type. Each numpy array should contain 1's for squares where
    the shape exists and 0's for squares where the shape does not exist. Here's
    an example below of a tetronimo-style "L" piece:
    ```
    np.array([
        [1,0],
        [1,0],
        [1,1]
    ])
    ```

    This shape manager is designed for square Grids.

    Parameters
    ----------
    :shapes: A list of numpy arrays, where each array is one piece shape
    '''

    def __init__(self,shapes:List[np.ndarray]):
        
        self.I_MAX = 0
        self.J_MAX = 1
        self.START = 2
        self.END   = 3
        
        self.shapes = shapes
        
        self.info = np.vstack((
            [ shape.shape[0] for shape in shapes ],
            [ shape.shape[1] for shape in shapes ],
            np.array([0]+[ shape.sum() for shape in shapes ]).cumsum()[:-1],
            np.array([ shape.sum() for shape in shapes ]).cumsum()
        )).T.astype(np.int32)
        
        self.mask = np.array([ 
            [i,j] 
            for shape in shapes
            for i in range(shape.shape[0])
            for j in range(shape.shape[1]) 
            if shape[i,j]
        ],dtype=np.int32)