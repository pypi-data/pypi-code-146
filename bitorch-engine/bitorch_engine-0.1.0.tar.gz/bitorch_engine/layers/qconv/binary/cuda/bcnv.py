from enum import Enum


class BCNV(Enum):
    '''
    Indicates which Bit-Conv implmentation will be used
    '''
    BMM_BSTC32 = 1  # standard binary conv implmeneation: im2col+bmm bstc32
    BMM_BTC32 = 2  # standard binary conv implmeneation: im2col+bmm btc32
    ADAPTIVE = 3  # best combination regarding the specific dimension constrains of inputs and weights
    BCNV_32 = 4  # 32-bit binary conv layer kernel
    BCNV_64 = 5  # 64-bit binary conv layer kernel
    BCNV_BMMA_FMT = 6  # binary conv layer kernel using 1-bit tensor core
