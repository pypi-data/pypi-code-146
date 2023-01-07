import torch
from torch import nn
import random


class ScaledDecoder(nn.Module):
    """Last decoder layers - likely for classification

    Args:
        ninp (int): Input dimesnion
        nhid (int): Hidden layer dimension
        nout (int): Output dimension
    """
    def __init__(self, ninp, nhid, nout):
        """The decoder layer

        Args:
            ninp (int): Input dimesnion
            nhid (int): Hidden layer dimension
            nout (int): Output dimension
        """
        super().__init__()
        self.linear = nn.Linear(ninp, nhid)
        self.linear1 = nn.Linear(nhid, nout)
        self.linear2 = nn.Linear(nhid, 10)

    def forward(self, x):
        """Forwads input through the last the single layer perceptron with GELU

        Args:
            x (tensor): input

        Returns:
            tensor: output tensor (scaled with softmax?) before softmax dimension nout
        """
        #return torch.cat([self.linear1(x), self.linear2(x)], -1)
        x = self.linear(x)
        x = nn.GELU()(x)
        
        temps = self.linear2(x).softmax(-1) @ torch.tensor([1.,1.4,1.7,2.,5.,10.,20.,40.,80.,160.], device=x.device)
        if random.random() > .99:
            print(temps.shape,temps[:,:2])
        return self.linear1(x) / temps.unsqueeze(-1)

class FixedScaledDecoder(nn.Module):
    """Last decoder layers - likely for bayesian inference

    Args:
        ninp (int): Input dimesnion
        nhid (int): Hidden layer dimension
        nout (int): Output dimension
    """
    def __init__(self, ninp, nhid, nout):
        """Initiates the single layer perceptron with GELU 

        Args:
            ninp (int): Input dimesnion
            nhid (int): Hidden layer dimension
            nout (int): Output dimension
        """
        super().__init__()
        self.mapper = nn.Sequential(nn.Linear(ninp, nhid), nn.GELU(), nn.Linear(nhid, nout))
        self.T = nn.Parameter(torch.ones(10000)/10000)

    def forward(self, x):
        """Forwards x through the decoder

        Args:
            x (tensor): input

        Returns:
            tensor: dimension of nout
        """
        return self.mapper(x)/self.T.sum()

