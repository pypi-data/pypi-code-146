try:
    import torch
except ImportError:
    pass
import numpy as np
import os
try:
    import matplotlib.pyplot as plt
except ImportError:
    pass

def to_float_tensor(item): return item.float().div_(255.)
def add_colour_dimension(item):
    if item.dim() == 4:
        if item.shape[1] in [1,3]: # batch, channels, size, size
            return item
        elif item.shape[3] in [1,3]:  # batch, size, size, channels
            return item.permute(0,3,1,2)
    if item.dim() == 3:
        if item.shape[0] in [1,3]: # channels, size, size
            return item
        elif item.shape[2] in [1,3]: # size, size, channels
            return item.permute(2,0,1)
        else: return item.unsqueeze(1) # batch, size, size
    else: return item.unsqueeze(0) # size, size

def recursive_np_or(boolean_arrays):
    if len(boolean_arrays) == 1: return boolean_arrays[0]
    return np.logical_or(boolean_arrays[0],recursive_np_or(boolean_arrays[1:]))

def recursive_np_and(boolean_arrays):
    if len(boolean_arrays) == 1: return boolean_arrays[0]
    return np.logical_and(boolean_arrays[0],recursive_np_and(boolean_arrays[1:]))

def np_load_all(dir_name,comb_method='stack',restrict=-1,sort=True):
    all_fnames = os.listdir(dir_name)
    if restrict != -1:
        all_fnames = all_fnames[:restrict]
    if sort:
        all_fnames.sort()
    all_arrs = [np.load(os.path.join(dir_name,fn)) for fn in all_fnames]
    if comb_method=='none':
        return all_arrs
    elif comb_method=='cat':
        return np.concatenate(all_arrs)
    elif comb_method=='stack':
        return np.stack(all_arrs)

def noiseify(pytensor,constant):
    noise = torch.randn_like(pytensor)
    noise /= noise.max()
    return pytensor + noise*constant

def oheify(x):
    target_category = torch.argmax(x, dim=1)
    ohe_target = (torch.arange(x.shape[1]).to(x.device) == target_category[:,None])[:,:,None,None].float()
    return target_category, ohe_target

def numpyify(x):
    if isinstance(x,np.ndarray): return x
    elif isinstance(x,list): return np.array(x)
    elif torch.is_tensor(x): return x.detach().cpu().numpy()
    else:
        raise TypeError(f"can only numpyify an array, list or tensor; received object of type {type(x)}")

def mean_off_diagonal(mat):
    upper_sum = np.triu(mat,1).sum()
    lower_sum = np.tril(mat,-1).sum()
    num_el = np.prod(mat.shape) - mat.shape[0]
    return (upper_sum + lower_sum)/num_el

def cudify(x): return torch.tensor(x,device='cuda')

def print_tensors(*tensors):
    """Only works for one-element tensors"""
    print(*[t.item() for t in tensors])

def display_image(t):
    ready_for_display = displayify(t)
    plt.imshow(ready_for_display); plt.show()
    #a = numpyify(t.squeeze())
    #if a.ndim==2:
    #    plt.imshow(a); plt.show()
    #elif a.ndim==3 and a.shape[0]==3:
    #    plt.imshow(np.transpose(a,(1,2,0))); plt.show()
    #elif a.ndim==3 and a.shape[2]==3:
    #    plt.imshow(a); plt.show()
    #else:
    #    raise TypeError(f"invalid tensor shape {a.shape} for displaying images")

def displayify(t):
    a = numpyify(t.squeeze())
    if a.ndim==2 or (a.ndim==3 and a.shape[2] in [1,3]):
        return a
    elif a.ndim==3 and a.shape[0] in [1,3]:
        return np.transpose(a,(1,2,0))
    else:
        raise TypeError(f"invalid tensor shape {a.shape} for displaying images")
