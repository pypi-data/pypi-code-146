
import bz2,pickle,json
import numpy as np

__all__ = [
    'calTime','set_params',
    'ToJsonEncoder',
    'open_pklbz2_file',
    'open_jason_file',
    ]


def open_pklbz2_file(path):
    with bz2.open(path, 'rb') as fp:
        data = pickle.loads(fp.read())
    return data

def open_jason_file(path):
    with open(path, 'r') as fp:
        json_load = json.load(fp)
    return json_load

def calTime(end, start):
    elapsed_time = end - start
    q, mod = divmod(elapsed_time, 60)
    if q < 60:
        print('Calculation time: %d minutes %0.3f seconds.' % (q, mod))
    else:
        q2, mod2 = divmod(q, 60)
        print('Calculation time: %d h %0.3f minutes.' % (q2, mod2))

def check_folder(folder_dir):
    if not os.path.exists(folder_dir):
        os.makedirs(folder_dir)

def set_params(data,keys,*initial_data, **kwargs):
    for dictionary in initial_data:
        for key in dictionary:
            if not key in keys:
                raise KeyError(key)
            data[key] = dictionary[key]

    for key in kwargs:
        if not key in keys:
            raise KeyError(key)
        data[key] = kwargs[key]

class ToJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)
