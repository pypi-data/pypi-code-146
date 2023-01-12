from re import U
import numpy as np
import matplotlib.pyplot as plt
import h5py
from .utils import plotJV, getChunk, getJVparams, sort_ids
from datetime import datetime
import fnmatch
import itertools

# results types enum
# newest version of litos lite has only the CV recipe which is equivalent for stressing
RTYPES = ["JV", "LIGHT", "CV", "CC", "MPP"]
MTYPES = ["stop", "wait", "sweep", "loop", "set_light", "jv", "stress", "cc", "mppt", "set_temp"]   
SWEEP_DIRECTIONS = ["forward", "backward", "for+backward", "back+forward"]
SWEEP_DIRECTION_FWD = 0
SWEEP_DIRECTION_BCKW = 1
SWEEP_DIRECTION_FWD_BCKW = 2
SWEEP_DIRECTION_BCK_FWD = 3

class Step:
    """
    Class to handle Recipe Step
    """
    def __init__(self, hHdf):
        self.f = hHdf
        self.ID = self.f.attrs['ID']
        self.type = self.f.attrs['type']
        self.timestamp = self.f.name.split("/")[-1]

    def __repr__(self):
        return f'Step({self.ID} - {MTYPES[self.type]})'

    def __str__(self):
        return "  "*self.ID.count('.')+f'{self.ID}: {MTYPES[self.type]}'


class Recipe:
    """
    Class to handle a Recipe
    """
    def __init__(self, hHdf):
        self.f = hHdf
        self.ID = self.f.name.split("/")[-1]
        self.name = self.f.attrs['name']

    def __repr__(self):
        return f'Recipe({self.ID} : {self.name})'

    def show(self):
        print(self.f.attrs['name'])
        steps = list(self.f['steps'].keys())
        steps = sort_ids(steps)
        for step in steps:
            s = Step(self.f['steps'][step])
            print(str(s))

class Sample:
    """
    Class to handle Sample
    """
    def __init__(self, hHdf):
        self.f = hHdf
        self.name = self.f.attrs['name']
        self.num_devices = self.f.attrs['num devices']
        self.sampleID = self.f.attrs['sample ID']
    
    def get_result(self, meas):
        res = self.f['results']
        if meas.timestamp in res:
            return res[meas.timestamp]


class Result:
    """
    Handle Litos Lits .lls result file
    """
    def __init__(self, path):
        """ 
        Open Litos Lite .lls file

        Args:
            path (str): filepath of the .lls file 
        """
        self.f = h5py.File(path, 'r')
        self.samples: dict[str, str] = {}
        for x in self.f['Results']['samples']:
            name = self.f['Results']['samples'][x].attrs['name']
            self.samples[name] = x
        
    def getStartStopData(self, sample_name, resultID):
        """
        Returns the start_values and stop_values of 
        - sample holder climate: temperature
        - sample holder climate: relative Humidity
        - IR temperature
        - Stage temperature
        - Light intensity

        Args:
            sample_name (str): Name of the sample
            resultID (int|str): index of the experimental result
        Ret:
            (dict): dict containing the results indicated above
        """
        tc = self.getResultTimestamp(sample_name, resultID, raw=True)
        r = self.__getSample(sample_name)['results'][tc]['data']
        return {x:(r.attrs['start_values'][i], r.attrs['stop_values'][i], r.attrs['units'][i]) for i,x in enumerate(r.attrs['name'])}
    
    def getSampleList(self, filt=None):
        """        
        Get a list of all samples present in the result.
        The return values containms the name of the sample as well as the number of devices (pixels) present on the sample

        Args:
        Ret:
            (list[dict]): It returns a list of dicts containing: 'name', 'num devices' and 'sample ID'
        """ 
        samples = [{
            "name":x, 
            "devices":self.f['Results']['samples'][self.samples[x]].attrs['num devices'], 
            "sampleID":self.f['Results']['samples'][self.samples[x]].attrs['sample ID']
            } for x in self.samples ]
        if filt is None:
            return samples 
        sample_names = [x['name'] for x in samples]
        return [x for x in samples if x['name'] in fnmatch.filter(sample_names, filt)]
            
    def getResultTimestamp(self, sample_name, resultID, raw=False):
        """        
        Return the UNIX Timestamp of the result (start time)
        
        Args:
            sample_name (str): Name of the sample
            resultID (int|str): index of the experimental result
        Ret:
            (str|float): UNIX Timestamp of the result (start time)
        """
        tc = list(self.__getSample(sample_name).get('results').keys())[resultID]
        if raw:
            return tc
        return float(tc)-2082844800
    
    def getRecipes(self):
        """        
        Returns the recipes object

        Args:
        Ret:
            (Recipe)
        """
        return [Recipe(self.f['recipes'][x]) for x in self.f['recipes']]

    def getResultStartTime(self, sample_name, resultID):
        """
        Return the Start time of the result

        Args:
            sample_name (str): Name of the sample
            resultID (int|str): index of the experimental result
        Ret:
            (datetime)
        """
        return datetime.fromtimestamp(int(self.getResultTimestamp(sample_name, resultID)))
        
    def __getSample(self, sample_name):
        """        
        get HDF5 group for a given sample
        
        Args:
            sample_name (str): Name of the sample
        Ret:
            (h5py.Group)
        """
        s = self.f['Results']['samples']
        return s.get(self.samples[sample_name])
    
    def getResultsIndicesByType(self, sample_name, result_type, hr=True):
        """        
        Returns the resultIDs of all results of a given type
        
        Args:
            sample_name (str): Name of the sample
            result_type (str): Result type (indicated in RTYPES)
        Ret:
            (list[int])
        """
        return [i for i,t in enumerate(self.getResultsTypes(sample_name, hr=hr)) if t==result_type]
        
    def getResultsTypes(self, sample_name, hr=True):
        """        
        Return the type of the result as integer.
        if hr (for human-readble) is True, then the result are strings ("JV","LIGHT","CV","CC","MPP") otherwise they are integer
        
        Args:
            sample_name (str): Name of the sample
        Ret:
            (list[int|str])
        """
        r = self.__getSample(sample_name)['results']
        t=[int(r[x].attrs['type']) for x in r]
        if hr:
            return [RTYPES[x] for x in t]
        return t
    
    def listSensors(self, sample_name, resultID):
        """        
        List the (name, unit) of sensors recorded for a given sample and resultID
        
        Args:
            sample_name (str): Name of the sample
            resultID (int|str): index of the experimental result
        Ret:
            (list[list[str]])
        """
        s = self.__getSample(sample_name)['results']
        R = s.get(str(self.getResultTimestamp(sample_name, resultID, raw=True)))
        time = np.array(R['1']['time'])
        if 'variables' in R['1']:
            names = [[x for x in n] for n in list(R['1']['variables'])]
        else:
            keys = [x[4:] for x in R['1'].keys() if x[:4]=='data']
            keys.sort()
            names = [[R['1']['data'+x].attrs[v] for v in ['name', 'unit']] for x in keys]
        return names
         
    def getSensorResultByName(self, sample_name, resultID, sensor_name):
        """
        Return the result for a given Sample, resultID and sensor name
        
        Args:
            sample_name (str): Name of the sample
            resultID (int|str): index of the experimental result
            sensor_name (str): Name of the sensor
        Ret:
            (dict): return the sensor 'name', 'unit', 'time' and 'data'
        """
        s = self.__getSample(sample_name)['results']
        R = s.get(self.getResultTimestamp(sample_name, resultID, raw=True))
        time = np.array(R['1']['time'])
        names = self.listSensors(sample_name, resultID)
        if 'variables' in R['1']:
            names = [[x.replace('\udcb0','°') for x in n] for n in list(R['1']['variables'])]
            for i,(n,u) in enumerate(names):
                if n==sensor_name:
                    return {'name':n, 'unit':u, 't':time, 'data':np.ravel(R['1']['data'][i,:])}
        else:
            for x in R['1']:
                if x[:4]!='data':
                    continue
                name = R['1'][x].attrs['name']
                if name == sensor_name:
                    return {
                        'name':name,
                        'unit':R['1'][x].attrs['unit'].replace('\udcb0','°'),
                        't':time, 
                        'data':np.ravel(R['1'][x][:])
                        }
        return None

    def plotSensorResultByName(self, sample_name, resultID, sensor_name, ax=None):
        """
        Plots sensor result by name
        
        Args:
            sample_name (str): Name of the sample
            resultID (int|str): index of the experimental result
            sensor_name (str): Name of the sensor
        Ret:
            (plt.axis)
        """
        if ax is None:
            ax = plt.gca()
        r = self.getSensorResultByName(sample_name, resultID, sensor_name)
        if r is None:
            return None
        ax.plot(r['t'],r['data'],label=r['name'])
        ax.set_xlabel("Time [min]")
        ax.set_ylabel(f"{r['name']} ({r['unit']})")
    
    def getRecipeStepFromTimestamp(self, timestamp):
        """
        To be double checked
        """
        self.f['Results']['Recipe_steps']

    def getDevices(self, sample_name='*', pixels=True, used=False):
        """
        Returns a list of devices for a specific sample_name containing 'sample_name', 'pixelID' and 'sampleID'

        Args:
            sample_name (str): Name of the sample
        Ret:
            (list[dict])
        """
        samples = self.getSampleList(sample_name)
        devices = [{
            'sample_name': s['name'], 
            'pixelID': p, 
            'sampleID': s['sampleID'] 
            }  for s in samples for p in range(s['devices'])]
        return devices

    def getMeasurements(self):
        """
        Retrieve a list of all measurements with parameters

        Args:
        Ret:
            (list)
        """
        ts = list(self.f['Results']['Recipe_steps'].keys())
        ts.sort()
        meas = [Step(self.f['Results']['Recipe_steps'][x]) for x in ts]
        return meas

    def getResult(self, sample_name, pixelID, resultID, includeSensors=False, use_pandas=False, hyst=True):
        """
        Gets the result for a given sample and a given pixelID.
        The pixelID is 0-indexed, meaning that the ID 0 corresponds to the first pixel of the sample
        resultID can be either an integer N that point to the Nth result of the given sample or it can be a string representing the timestamp as retrieved by self.getResultTimestamp with the raw=True argument
        Disctionary with all the result of the measurement (units are SI: so voltage in (V) and current in (A))

        Args:
            sample_name (str): Name of the sample
            pixelID (int): Pixel ID
            resultID (int|str): index of the experimental result
        Ret:
            (dict)
        """
        s = self.__getSample(sample_name)['results']
        if type(resultID) is int:
            tc = self.getResultTimestamp(sample_name, resultID, raw=True)
        else:
            tc = resultID
        R = s.get(tc) # HDF5 group of the sample result
        pixel_used = list(R['pixel_used'])
        if pixelID in pixel_used:
            pixelIndex = pixel_used.index(pixelID)
        else:
            pixelIndex = None
        if R.attrs["type"]==0: #JV
            if pixelIndex is None:
                raise Exception(f"pixelID {pixelID} not found for the given result")
            data = np.array(R['IV'])
            V = data[pixelIndex,0,:]
            I = data[pixelIndex,1,:]
            params = {"up":{},"down":{}}
            if hyst:
                numC = np.sum(np.isnan(V))
                Vs = [getChunk(V,i) for i in range(numC)]
                UPs = [v[-1]>v[0] for v in Vs]
                Is = [getChunk(I,i) for i in range(numC)]
                iUP = [j for j,u in enumerate(UPs) if u]
                iDOWN = [j for j,u in enumerate(UPs) if not u]
                if use_pandas:
                    import pandas as pd
                    res = {}
                    if True in UPs:
                        res["voltage_up"] = Vs[iUP[0]]
                        res["current_up"] = Is[iUP[0]]
                        params["up"] = getJVparams(Vs[iUP[0]],Is[iUP[0]])
                    if False in UPs:
                        res["voltage_down"] = Vs[iDOWN[0]]
                        res["current_down"] = Is[iDOWN[0]]
                        params["down"] = getJVparams(Vs[iDOWN[0]],Is[iDOWN[0]])
                    p = list(params.get("up",{}).keys())+list(params.get("down",{}).keys())
                    p = set(p)
                    xx = {par:[params.get(x, {}).get(par, np.nan) for x in ["up", "down"]] for par in p}
                    max_length = np.max([len(res[x]) for x in res])
                    df_params = pd.DataFrame(xx)
                    df_params.index = ["up", "down"]
                    return pd.DataFrame({x:np.pad(res[x], (0,max_length-len(res[x])), 'constant', constant_values=np.nan) for x in res}), df_params
                else:
                    res = {'type':"JV"}
                    if True in UPs:
                        res["up"] = {
                            'voltage':Vs[iUP[0]],
                            'current':Is[iUP[0]],
                            'params':getJVparams(Vs[iUP[0]],Is[iUP[0]])
                            }
                    if False in UPs:
                        res["down"] = {
                            'voltage':Vs[iDOWN[0]],
                            'current':Is[iDOWN[0]],
                            'params':getJVparams(Vs[iDOWN[0]], Is[iDOWN[0]])
                            }
                return res
            else:
                if use_pandas:
                    return pd.DataFrame({'voltage':V, 'current':I}),getJVparams(V, I)
                else:
                    return {'type':"JV", 'voltage':V, 'current':I, "params":getJVparams(V, I)}
        elif R.attrs["type"] in [2, 3, 4]:
            if pixelIndex is None:
                return None
            t = np.array(R['0']['time'])
            if 'data' in R['0'].keys(): # old data format
                data = np.array(R['0']['data'])
                V = data[0,pixelIndex,:]
                I = data[1,pixelIndex,:]
            else: # new data forma
                V = None
                I = None
                for x in R['0']:
                    if x[:4]!='data':
                        continue
                    n = R['0'][x].attrs['name']
                    if n.lower()=='voltage':
                        V = np.array(R['0'][x])[pixelIndex,:]
                    elif n.lower()=='current':
                        I = np.array(R['0'][x])[pixelIndex,:]
            if includeSensors:
                keys = [x[4:] for x in R['1'].keys() if x[:4]=='data']
                keys.sort()
                if 'data' in R['1'].keys(): # old format
                    sens = {
                        't': np.array(R['1']['time']),
                        'name': list(R['1']['variables']),
                        'data':np.array(R['1']['data'])
                        }
                else: # new format
                    sens = sens = {
                        't': np.array(R['1']['time']),
                        'sensors' : {R['1']['data'+x].attrs["name"]:{
                            'unit':R['1']['data'+x].attrs["unit"].replace('\udcb0','°'),
                            'data': np.ravel(R['1']['data'+x])} for x in keys}
                        }
                return {'type':"Stress", 't':t, 'voltage':V, 'current':I, 'start_time':R.attrs.get("start_time"), "sensors":sens}
            return {
                'type':"Stress",
                't':t, 
                'voltage':V,
                'current':I,
                'start_time':R.attrs.get("start_time")
                }

    def getResultData(self, sample_name, resultID):
        """
        Returns the results data 'name', 'start_values', 'stop_values', 'units'.
        
        Args:
            sample_name (str): Name of the sample
            resultID (int|str): index of the experimental result
        Ret:
            (dict[str,dict[str,str|float]])
        """
        s = self.__getSample(sample_name)['results']
        R = s.get(self.getResultTimestamp(sample_name, resultID, raw=True)) # HDF5 group of the sample result
        data = R['data'].attrs
        return {data['name'][i]:{
            'unit':data['units'][i],
            'start':data['start_values'][i],
            'stop':data['stop_values'][i]
            } for i,_ in enumerate(data['name'])}

    def plotJVparams(self, sample_name, pixelID, param="MPP", ax=None, up=True, **kargs):
        """
        Plots the specific param indicated as arg. It can be:
        MPP, FF, Voc, Isc, Vmpp, Impp.

        Args:
            sample_name (str): Name of the sample
            pixelID (int): Pixel ID
        Ret:
            (plt.axis)
        """
        if ax is None:
            ax = plt.gca()
        direct = ['down','up'][up]
        t,p = self.getJVparams(sample_name, pixelID, **kargs)
        units = {
            "MPP":(1e3,"mW"),
            "FF":(100,"%"),
            "Voc":(1,"V"),
            "Isc":(1e3,"mA"),
            "Vmpp":(1,"V"),
            "Impp":(1e3,"mA")
            }
        unit = units.get(param, (1,"???"))
        ax.plot((t-t[0])/3600, np.array(p[direct][param])*unit[0], label=f"{param} [{direct}]")
        ax.set_xlabel("Time [h]")
        ax.set_ylabel(param+f" [{unit[1]}]")
        if kargs.get("legend", True):
            ax.legend()
        return ax
        
    def getJVparams(self, sample_name, pixelID, min_resID=0, max_resID=None, **kargs):
        """
        Returns a tuple containing an array (time), and a dictionary containing JV parameters.

        Args:
            sample_name (str): Name of the sample
            pixelID (int): Pixel ID
        Ret:
            (tuple[np.array,dict])
        """
        t = []
        params = {"up":{},"down":{}}
        for i in self.getResultsIndicesByType(sample_name, "JV"):
            if i<min_resID: continue
            if max_resID is not None and i>max_resID: break
            t.append(self.getResultTimestamp(sample_name, i))
            r = self.getResult(sample_name, pixelID, i)
            for direct in ["up","down"]:
                for pp in r.get(direct, {'params':{}})['params']:
                    if pp in params[direct]:
                        params[direct][pp] = np.vstack([params[direct][pp], r[direct]['params'][pp]])
                    else:
                        params[direct][pp] = np.array([r[direct]['params'][pp]])
        return np.array(t),params
           
    def plotResult(self, sample_name, pixelID, resultID, globalTime=False, ax=None, axb=None, col='C0', colb='C1', V=True, I=True, hyst=False, **kargs):
        """
        Plots the result.

        Args:
            sample_name (str): Name of the sample
            pixelID (int): Pixel ID
        Ret:
            (plt.axis) 
        """
        data = self.getResult(sample_name, pixelID, resultID, hyst=hyst)
        if ax is None:
            ax = plt.gca()
        if data["type"] == "Stress":
            if axb is None and I:
                axb = ax.twinx()
        
        if data["type"] == "JV":
            ax = plotJV(data, ax=ax, **kargs)
            if kargs.get("legend",True):
                ax.legend()
            return ax
        else:
            if globalTime:
                t0 = np.datetime64('1904-01-01 00:00:00.000') + np.timedelta64(int(data['start_time'][1]), 's') # LV timestamp is from the 1st of January 1904
                dt = np.vectorize(lambda x: np.timedelta64(int(x), 's'))(data['t'])
                t = t0 + dt
                ax.set_xlabel("Date")
            else:
                t = data['t']
                ax.set_xlabel("Time [s]")

            if V:
                ax.plot(t,data['voltage'], color=col)
                ax.set_ylabel("Voltage [V]", color=col)
                ax.tick_params(axis='y', colors=col)
                ax.grid(color=col, alpha=.2)
            if I:
                axb.tick_params(axis='y', colors=colb)
                axb.plot(t,data['current']*1e3,color=colb)
                axb.set_ylabel("Current [mA]", color=colb);
                axb.grid(color=colb, alpha=.2)
        return ax,axb

    def plotResults(self, sample_name, pixelID, res_type, globalTime=False, ax=None, axb=None, col='C0', colb='C1',I=True, V=True):
        """
        Plot the results
        
        Args:
            sample_name (str): Name of the sample
            pixelID (int): Pixel ID
            res_type (str): Result type (indicated in RTYPES)
        Ret:
            (plt.axis)
        """
        if ax is None:
            ax = plt.gca()
        if axb is None:
            axb = ax.twinx()
        if type(res_type) is not int:
            res_type = RTYPES.index(res_type)
        for i,t in enumerate(self.getResultsTypes(sample_name)):
            if t==res_type:
                self.plotResult(sample_name, pixelID, i, globalTime, ax=ax, axb=axb, col=col, colb=colb,I=I,V=V)
        if globalTime: plt.gcf().autofmt_xdate()
        return ax, axb
        
    def close(self):
        self.f.close()