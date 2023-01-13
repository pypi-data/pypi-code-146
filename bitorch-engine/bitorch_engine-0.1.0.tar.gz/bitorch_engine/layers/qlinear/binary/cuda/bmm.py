from enum import Enum


class BMM(Enum):
    '''
    Indicates which Bit-Matrix-Multiplication kernel will be used.
    '''
    BSTC32 = 1  # software based tensor core implementation
    BTC32 = 2  # bmm using nv tesnsor core
    ADAPTIVE = 3  # best combination regarding the specific dimension constrains of inputs and weights
