import torch
from torch.utils import data
import torch.multiprocessing as mp
import os
import gc
from dl_utils.misc import test_mods_eq, check_dir

class CifarLikeDataset(data.Dataset):
    def __init__(self,x,y,transform=None):
        self.data, self.targets = x,y
        self.transform = transform
        assert len(x) == len(y)
    def __len__(self): return len(self.data)
    def __getitem__(self,idx):
        batch_x, batch_y = self.data[idx], self.targets[idx]
        if self.transform:
            batch_x = self.transform(batch_x)
        return batch_x, batch_y

def save_and_check(enc,dec,fname):
    torch.save({'enc': enc, 'dec': dec},fname)
    loaded = torch.load(fname)
    e,d = loaded['enc'], loaded['dec']
    test_mods_eq(e,enc); test_mods_eq(d,dec)

def torch_save(checkpoint,directory,fname):
    check_dir(directory)
    torch.save(checkpoint,os.path.join(directory,fname))

def apply_maybe_multiproc(func,input_list,split,single):
    if single:
        output_list = [func(item) for item in input_list]
    else:
        list_of_lists = []
        ctx = mp.get_context("spawn")
        num_splits = math.ceil(len(input_list)/split)
        for i in range(num_splits):
            with ctx.Pool(processes=split) as pool:
                new_list = pool.map(func, input_list[split*i:split*(i+1)])
            if num_splits != 1: print(f'finished {i}th split section')
            list_of_lists.append(new_list)
        output_list = [item for sublist in list_of_lists for item in sublist]
    return output_list

def show_gpu_memory():
    mem_used = 0
    for obj in gc.get_objects():
        try:
            if torch.is_tensor(obj) or hasattr(obj, 'data') and torch.is_tensor(obj.data):
                mem_used += obj.element_size() * obj.nelement()
        except: pass
    print(f"GPU memory usage: {mem_used}")
