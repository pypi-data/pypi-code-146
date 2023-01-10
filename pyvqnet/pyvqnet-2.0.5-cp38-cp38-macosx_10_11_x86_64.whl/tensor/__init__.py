"""
inti for tensor
"""
# pylint: disable=redefined-builtin
from .tensor import QTensor
from .tensor import mean,max,empty,ones,\
    ones_like,full,full_like,zeros_like,zeros,floor,\
    ceil,arange,linspace,logspace,eye,diag,randu,randn,\
    sort,argsort,nonzero,isfinite,isinf,isnan,isneginf,\
    isposinf,logical_and,logical_or,logical_xor,logical_not,\
    greater,greater_equal,less,less_equal,equal,not_equal,\
    broadcast,add,sub,mul,divide,sums,frobenius_norm,matmul,reciprocal,\
    round,sign,neg,triu,tril,trace,exp,acos,asin,atan,tanh,sinh,cosh,\
    maximum,minimum,clip,power,abs,log,sqrt,square,flatten,swapaxis,\
    reshape,sin,cos,tan,median,std,var,where,min,select,set_select,\
        concatenate,stack,permute,transpose,tile,squeeze,unsqueeze,\
            masked_fill,argtopK,topK,cumsum,flip,log_softmax
from .tensor import *
