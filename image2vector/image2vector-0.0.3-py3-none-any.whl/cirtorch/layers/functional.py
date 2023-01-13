import torch
from torch import Tensor
import torch.nn.functional as F

# --------------------------------------
# pooling
# --------------------------------------


def mac(x):
    return F.max_pool2d(x, (x.size(-2), x.size(-1)))
    # return F.adaptive_max_pool2d(x, (1,1)) # alternative


def spoc(x):
    return F.avg_pool2d(x, (x.size(-2), x.size(-1)))
    # return F.adaptive_avg_pool2d(x, (1,1)) # alternative


def gem(x: Tensor, p: int = 3, eps: float = 1e-6) -> Tensor:
    t = F.avg_pool2d(
        x.clamp(min=eps).pow(p),
        (x.size(-2), x.size(-1))
    ).pow(1./p)
    return t


# --------------------------------------
# normalization
# --------------------------------------

def l2n(x: Tensor, eps: float = 1e-6) -> Tensor:

    return x / (torch.norm(x, p=2, dim=1, keepdim=True) + eps).expand_as(x)


# --------------------------------------
# loss
# --------------------------------------


def contrastive_loss(x, label, margin=0.7, eps=1e-6):
    # x is D x N
    dim = x.size(0)  # D
    nq = torch.sum(label.data == -1)  # number of tuples
    S = x.size(1) // nq  # number of images per tuple including query: 1+1+n

    x1 = x[:, ::S].permute(1, 0).repeat(
        1, S-1).view((S-1)*nq, dim).permute(1, 0)
    idx = [i for i in range(len(label)) if label.data[i] != -1]
    x2 = x[:, idx]
    lbl = label[label != -1]

    dif = x1 - x2
    D = torch.pow(dif+eps, 2).sum(dim=0).sqrt()

    y = 0.5*lbl*torch.pow(D, 2) + 0.5*(1-lbl) * \
        torch.pow(torch.clamp(margin-D, min=0), 2)
    y = torch.sum(y)
    return y


def triplet_loss(x, label, margin=0.1):
    # x is D x N
    dim = x.size(0)  # D
    nq = torch.sum(label.data == -1).item()  # number of tuples
    S = x.size(1) // nq  # number of images per tuple including query: 1+1+n

    xa = x[:, label.data == -
           1].permute(1, 0).repeat(1, S-2).view((S-2)*nq, dim).permute(1, 0)
    xp = x[:, label.data == 1].permute(1, 0).repeat(
        1, S-2).view((S-2)*nq, dim).permute(1, 0)
    xn = x[:, label.data == 0]

    dist_pos = torch.sum(torch.pow(xa - xp, 2), dim=0)
    dist_neg = torch.sum(torch.pow(xa - xn, 2), dim=0)

    return torch.sum(torch.clamp(dist_pos - dist_neg + margin, min=0))
