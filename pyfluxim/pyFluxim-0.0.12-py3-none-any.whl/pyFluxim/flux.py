import numpy as np
import matplotlib.pyplot as plt
import h5py
from .utils import plotJV, getChunk, flux2timestamp
RTYPES = ["JV","LIGHT","CV","CC","MPP"]
        
class Experiment:
    def __init__(self, f):
        self.f = f
        self.key = f.name.split("/")[-1]
    
    def getParameters(self):
        return {x:(self.f['parameters'][x][()], self.f['parameters'][x].attrs['unit'].decode('ansi')) for x in self.f['parameters']}
        
    def getResults(self, chunk=None):
        r = {}
        for i in self.f['results']:
            R = self.f['results'][i]
            name = R.attrs['label'].decode('ansi')
            unit = R.attrs['unit'].decode('ansi')
            data = R[()]
            if chunk is not None:
                data = getChunk(data, chunk)
            r[name] = (data, unit)
        return r
        
class Device:
    def __init__(self, f):
        self.f = f
        assert f.name.startswith('/devices/')
        self.name = f.name[9:]
    
    def listExperiments(self):
        for i,ex in enumerate(self.f['experiments']):
            E = self.f['experiments'][ex]
            _type = E.attrs['type'].decode('utf8')
            start_time = flux2timestamp(E.attrs['start_time'])
            print("{}) {} [{}]".format(i,_type, start_time[0].strftime("%Y/%m/%d %H:%M:%S")))
    
    def getExperimentById(self, id):
        keys = list(self.f['experiments'].keys())
        assert id<len(keys)
        key = keys[id]
        return Experiment(self.f['experiments'][key])
        
    def getExperimentByKey(self, key):
        keys = self.f['experiments'].keys()
        assert key in keys
        return Experiment(self.f['experiments'][key])
        
class Flux:
    def __init__(self, path):
        self.f = h5py.File(path, 'r')
     
    def listDevices(self):
        for dev in self.f['devices']:
            print("- {}".format(dev))
           
    def getDevice(self, name):
        return Device(self.f['devices'][name])
        
    def close(self):
        self.f.close()