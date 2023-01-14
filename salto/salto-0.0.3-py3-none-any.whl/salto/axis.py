import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt
from functools import reduce
from operator import add


class axis:
    '''
    
    Create a new axis using the line passing through the negative and positive pole.
    
    Parameters
    ----------
    negative_pole: numpy.array
        A vector (point), which indicates negative side of the axis
    positive_pole: numpy.array
        A vector (point), which indicates positive side of the axis
     
    Attributes
    ----------
    dims: int
        The expected number of dimensions    
    midpoint: numpy.array
        The midpoint between the negative and positive pole
    transform: numpy.array
        A matrix to shift the space to place the midpoint in the origin
    shifted_negative_pole: numpy.array
        The negative pole shifted with the affine transfromation defined in the self.transform matrix
    shifted_positive_pole: numpy.array
        The positive pole shifted with the affine transfromation defined in the self.transform matrix
    unit_vector: numpy.array
        A unit vector which indicates the line passing through the shifted negative pole and shifted positive pole
     
        
    Examples
    --------
    >>> import numpy as np
    >>> import spacy
    >>> import salto
    >>>
    >>> nlp = spacy.load('en_core_web_md')
    >>> fire = nlp('fire')
    >>>
    >>> ice = nlp('ice')
    >>> ice_fire_axis = salto.axis(ice.vector, fire.vector)
    >>>
    >>> cold = ['ice cream', 'polar', 'snow', 'winter', 'fridge', 'Antarctica']
    >>> warm = ['boiling water', 'tropical', 'sun', 'summer', 'oven', 'Africa']
    >>>
    >>> cold_vecs = [nlp(w).vector for w in cold]
    >>> warm_vecs = [nlp(w).vector for w in warm]
    >>>
    >>> cold_values = [ice_fire_axis(p) for p in cold_vecs]
    >>> warm_values = [ice_fire_axis(p) for p in warm_vecs]
    >>>
    >>> ice_fire_axis.plot(
    >>>     {'values': cold_values, 'labels': cold, 'color': 'tab:blue'},
    >>>     {'values': warm_values, 'labels': warm, 'color': 'tab:red'},
    >>>     poles = {'negative': {'label': 'ice', 'color': 'blue'}, 
    >>>              'positive': {'label': 'ice', 'color': 'red'}}
    >>> )
    '''
    def __init__(self, negative_pole: npt.NDArray, positive_pole: npt.NDArray):
        
        self.dims = len(negative_pole)
        
        # Original values
        self.negative_pole = negative_pole 
        self.positive_pole = positive_pole
        self.midpoint = _midpoint(negative_pole, positive_pole)  
        
        # Transformation
        self.transform = _transformation_matrix(self.dims, self.midpoint)       
        self.shifted_negative_pole = self._shift(negative_pole)
        self.shifted_positive_pole = self._shift(positive_pole)
        
        self.unit_vector = self.shifted_positive_pole / np.linalg.norm(self.shifted_positive_pole)      # shifted_midpoint is (0, 0, ...) 

    def __call__(self, vector: npt.NDArray):
        
        if (len(vector) != self.dims):
            raise ValueError(
                f'Vector length is {len(vector)}, but it should equal {self.dims}' 
            )
        
        shifted_vector = self._shift(vector)
        return (self.unit_vector.T @ shifted_vector)[0, 0]
    
    def plot(*args, title = "Embedding vectors", figsize = (10, 5), 
             poles = {'negative': {'label': 'Negative pole', 'color': 'blue'}, 
                      'positive': {'label': 'Positive pole', 'color':'red'}}):
        '''
        
        Plot the groups of vectors on the on the axis (in the one-dimensional space)
    
        Parameters
        ----------
        title: str
            Plot title
        figsize: Tuple
            Figure size
        
        Examples
        --------
        >>> ice_fire_axis = salto.axis(ice.vector, fire.vector)
        >>> 
        >>> ice_fire_axis.plot(
        >>>     {'values': cold_values, 'labels': cold, 'color': 'tab:blue'},
        >>>     {'values': warm_values, 'labels': warm, 'color': 'tab:red'},
        >>>     poles = {'negative': {'label': 'ice', 'color': 'blue'}, 
        >>>              'positive': {'label': 'ice', 'color': 'red'}}
        >>> )   
   
        ''' 
         
        # Init plot
        fig, ax = plt.subplots(figsize=figsize, constrained_layout=True)
        ax.set(title=title)
        
        # Horizontal line       
        neg_value = self(self.negative_pole)
        pos_value = self(self.positive_pole)
        
        all_values = reduce(add, [a['values'] for a in args])
        all_values = all_values + [neg_value, pos_value]
        
        ax.plot(all_values, np.zeros_like(all_values), "-o",
        color="k", markerfacecolor="w")  # Baseline and markers on it.
        
        # Generate colours if not defined
        for group in args:

            values = group['values']
            labels = group['labels']
            color  = group['color']
            
            levels = np.tile([-5, 5, -3, 3, -1, 1],
                 int(np.ceil(len(values)/6)))[:len(values)]
            
            ax.vlines(values, 0, levels, color=color)  
            vert = np.array(['top', 'bottom'])[(levels > 0).astype(int)]

            for d, l, r, va in zip(values, levels, labels, vert):
                ax.annotate(r, xy=(d, l), xytext=(1, np.sign(l)*3),
                            textcoords="offset points", va=va, ha="right")
        
        # Show poles
        neg_pole = poles['negative']
        pos_pole = poles['positive']

        ax.vlines(neg_value, 0, 4, neg_pole['color'])  
        ax.annotate(neg_pole['label'], xy=(neg_value, 4), xytext=(4, np.sign(4)*3),
            textcoords="offset points", va=va, ha="right", weight='bold')

        ax.vlines(pos_value, 0, 4, color=pos_pole['color'])  
        ax.annotate(pos_pole['label'], xy=(pos_value, 4), xytext=(4, np.sign(4)*3),
            textcoords="offset points", va=va, ha="right", weight='bold')
        
        # Show the plot
        ax.yaxis.set_visible(False)
        ax.spines[["left", "top", "right"]].set_visible(False)
        ax.margins(y=0.1)
        plt.show()

    def _shift(self, vector: npt.NDArray):
        extended_vector = _extend_with_one(vector)
        return (self.transform @ extended_vector)[0:self.dims]
    
        
def _extend_with_one(vector: npt.NDArray) -> npt.NDArray:
    vector = vector[np.newaxis].T
    return np.vstack([vector, [1]])      

def _transformation_matrix(dims: int, midpoint: npt.NDArray) -> npt.NDArray:
    mat = np.eye(dims + 1)
    mat[0:dims, -1] = -midpoint
    return mat   
    
def _midpoint(x: npt.NDArray, y: npt.NDArray) -> npt.NDArray:
    if (len(x) != len(y)):
        raise ValueError(
            f'Vectors come from different spaces! ' + 
            f'x: {len(x)} dimensions, y: {len(y)} dimensions')
    return (x + y) / 2
