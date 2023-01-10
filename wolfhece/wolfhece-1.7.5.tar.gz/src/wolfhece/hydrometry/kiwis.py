from datetime import datetime, timedelta
import requests
import pandas as pd
from os.path import join,exists
from os import mkdir
from osgeo import ogr
from osgeo import osr  

import matplotlib.pyplot as plt

from ..RatingCurve import gaugingstation

'''
KIWIS WebServices command :
    getTimeseriesList
    getTimeseriesValues
    getStationList
    getSiteList
    getParameterList
    getParameterTypeList
'''

URL_SPW='https://hydrometrie.wallonie.be/services/KiWIS/KiWIS'

# Q1H  ='03b-Debit.1h'
Q1H         = '03d-Debit.1h.CalculAgregation'
Q1HMEDIAN   = '13-Debit.1h.Median'
Q1HMOYEN    = '10-Debit.1h.Moyen'
Q5MIN       = '02b-Debit.5min'
Q5MINAG     = '02d-Debit.5min.CalculAgregation'
QMAXAN      = '52-Debit.An.Maximum'
QMAXANHYD   = '62-Debit.AnHydro.Maximum'
QMINANHYD   = '61-Debit.AnHydro.Minimum'

# H1H  ='03b-Hauteur.1h.Production'
H1H         = '03d-Hauteur.1h.CalculDebit'
H1HMOYEN    = "10-Hauteur absolue.1h.Moyen"
H5MIN       = '02d-Hauteur.5min.CalculDebit'
HMAXAN      = '52-Hauteur.An.Maximum'
HMAXANHYD   = '62-Hauteur.AnHydro.Maximum'
HMINANHYD   = '61-Hauteur.AnHydro.Minimum'

P1H         = '03b-Precipitation.1h.Production'
P5MIN       = '02b-Precipitation.5min.Production'
P5MINIRM    = '02d-Precipitation.5min.ValidIRM'

T1H         = '03a-Temperature.1h.Origine'
T5MIN       = '02b-Temperature.5min.Production'

ALL_VALUES_SPW_HYDRO=[Q1H,Q5MIN,QMAXAN,QMAXANHYD,QMINANHYD,H1H,H5MIN,HMAXAN,HMAXANHYD,HMINANHYD,P1H,P5MIN,P5MINIRM,T1H,T5MIN]

class hydrometry:
    
    def __init__(self, url:str='',dir='') -> None:
        '''Initialisation sur base d'un URL de service KIWIS
        et recherche des sites et stations disponibles
        '''
        self.url=''
        self.dir=''
        
        if url!='':
            self.url=URL_SPW
        
        if dir!='':
            self.dir=dir
            
        # Spatial Reference System
        inputEPSG = 4326 #WGS84
        outputEPSG = 31370 #Lambert72

        # create coordinate transformation
        inSpatialRef = osr.SpatialReference()
        inSpatialRef.ImportFromEPSG(inputEPSG)

        outSpatialRef = osr.SpatialReference()
        outSpatialRef.ImportFromEPSG(outputEPSG)

        self.coordTransform = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)        

        self.get_sites()
        self.get_stations()
        if url=='':
            self.url=URL_SPW
    
    def plot(self,size:float=10.):
        for curstation in self.mystations.values():
            curstation.plot(size)                    

    def check_plot(self):
        self.plotted = True

    def uncheck_plot(self):
        self.plotted = False

    def save_struct(self,dir=''):
        
        if dir=='':
            return
        
        self.sites.to_csv(join(dir,'sites.csv'))
        self.stations.to_csv(join(dir,'stations.csv'))

    def get_stations(self):
        '''Obtention des stations pour le serveur courant'''
        
        if self.url!='':
            json_data = requests.get(self.url+'?request=getStationList&format=json',verify=False).json()
            self.stations = pd.DataFrame(json_data[1:], columns = json_data[0])
        
        if self.dir!='':
            self.stations = pd.read_csv(join(self.dir,'stations.csv'))
                
        #Conversion en minuscules
        self.stations['station_name']=self.stations['station_name'].str.lower()
        # #Utilisation du code comme index
        # self.stations.set_index('station_no',inplace=True)
        
        # create a geometry from coordinates
        lbx=[]
        lby=[]
        for lat, lon in zip(self.stations['station_latitude'],self.stations['station_longitude']):
            
            if not (pd.isna(lat) or lat==''):            
                pt = ogr.Geometry(ogr.wkbPoint)
                pt.AddPoint(float(lat), float(lon))
                pt.Transform(self.coordTransform)
                lbx.append(pt.GetX())
                lby.append(pt.GetY())
            else:
                lbx.append(-99999)
                lby.append(-99999)
        
        self.stations['LambertX'] = lbx
        self.stations['LambertY'] = lby
        
        self.realstations = self.stations[self.stations['LambertX']!=-99999]
        self.compstations = self.stations[self.stations['LambertX']==-99999]
        
        self.mystations={}
        for idx,curstation in self.realstations.iterrows():
            newstation = gaugingstation(curstation['station_name'],
                                        curstation['station_no'],
                                        '')
            newstation.x = curstation['LambertX']
            newstation.y = curstation['LambertY']
            if not ('L' == newstation.id[0] or \
                'E' == newstation.id[0] or \
                'T' == newstation.id[0] or \
                    'RR' == newstation.id[:2]):
                newstation.maintainer = 'SPW/DO223' 
            else:
                newstation.maintainer= 'SPW/DCENN'
            self.mystations[newstation.id]=newstation
        
    def get_sites(self):
        '''Obtention des sites pour le serveur courant'''
        if self.url!='':
            json_data = requests.get(self.url+'?request=getSiteList&format=json',verify=False).json()
            self.sites = pd.DataFrame(json_data[1:], columns = json_data[0])

        if self.dir!='':
            self.sites = pd.read_csv(join(self.dir,'sites.csv'))
        
    def timeseries_list(self,stationname='',stationcode=''):
        '''Récupération de la liste des TimeSeries pour l'id d'une station'''
        
        if stationname!='':
            id=self.get_stationid(stationname)
        elif stationcode!='':
            id=self.get_stationid(code=stationcode)
        
        json_data = requests.get(self.url+'?request=getTimeseriesList'
                                 +'&station_id='+str(id)
                                 +'&format=json'
                                 ,verify=False).json()

        return id,pd.DataFrame(json_data[1:], columns = json_data[0])
    
    def save_all_lists(self,dir):
        '''Sauveragde des listes pour toutes les stations'''
        for curstation in self.stations['station_no']:
            self.save_list(stationcode=curstation,dir=dir)
    
    def _get_filename_list(self,stationname='',stationcode=''):
        '''retourne un nom de fichier avec la station et le code
        
        Utile car dans certains noms de la BDD KIWIS il y a un caractère '/' qui ne peut être utilisé comme nom de fichier
        Il est remplacé par '-'
        '''
        if stationname=='':
            stationname = self.get_stationname(stationcode)
            
        if stationcode=='':
            stationcode = self.get_stationcode(stationname)
            
        id = self.get_stationid(stationname,stationcode)
            
        return stationname.replace('/','-') + '_' + stationcode + '_' + str(id) + '.csv'

    def _get_filename_series(self,stationname='',stationcode='',which=''):
        '''retourne un nom de fichier avec la station et le code et le type de données
        
        Utile car dans certains noms de la BDD KIWIS il y a un caractère '/' qui ne peut être utilisé comme nom de fichier
        Il est remplacé par '-'
        '''
        if stationname=='':
            stationname = self.get_stationname(stationcode)
            
        if stationcode=='':
            stationcode = self.get_stationcode(stationname)
            
        id = self.get_stationid(stationname,stationcode)
            
        return stationname.replace('/','-') + '_' + stationcode + '_' + str(id) + '_' + which + '.csv'        
    
    def save_list(self,stationname='',stationcode='',dir=''):
        '''Sauvegarde de la liste des des timeseries dans un fichier'''
        if not exists(dir):
            mkdir(dir)

        id,list=self.timeseries_list(stationname=stationname,stationcode=stationcode)                    
        filename = self._get_filename_list(stationname,stationcode)        
        list.to_csv(join(dir,filename))

    def timeseries(self,stationname='',stationcode='',dir='',fromdate=datetime.now()-timedelta(60),todate=datetime.now(),which=Q1H):
        '''Récupération des valeurs d'une TimeSeries pour l'id d'une station sur base des dates'''
        
        if stationname=='':
            stationname = self.get_stationname(stationcode)            
        if stationcode=='':
            stationcode = self.get_stationcode(stationname)
        id = self.get_stationid(stationname,stationcode)   
             
        if dir=='':    
            json_data = requests.get(self.url+'?request=getTimeseriesList'
                                    +'&station_id='+str(id)
                                    +"&ts_name="+which
                                    +"&format=json"
                                    ,verify=False).json()
            tsid = pd.DataFrame(json_data[1:], columns = json_data[0])
        else:
            filename = self._get_filename_list(stationname,stationcode)
            curlist=pd.read_csv(join(dir,filename))
            tsid = curlist.loc(curlist['ts_name'==which])
        
        if which==Q1H or which==Q1HMOYEN or which==Q1HMEDIAN or which==H1H:
            nb = (todate - fromdate).days*24
            cursec = 3600
        elif which==Q5MIN or which==H5MIN:
            nb = (todate - fromdate).days*24*12
            cursec = 300
        elif which== QMAXAN or which==QMAXANHYD or which==HMAXAN or which==HMAXANHYD:
            nb = int((todate - fromdate).days /365)+1 
            
        if nb>250000:
            curfrom = fromdate
            curend = curfrom+timedelta(seconds=200000 * cursec)
            locts=[]
            while curfrom<todate:
                locts.append(self.timeseries(stationname,stationcode,dir,curfrom,curend,which)[1])
                curfrom = curend
                curend = curfrom+timedelta(seconds=200000 * cursec)
                if curend>todate:
                    curend=todate
        
            return tsid,pd.concat(locts)
        else:
            json_data = requests.get(self.url+'?request=getTimeseriesValues&station_id='+str(id)
                                    +"&ts_id="+str(int(tsid['ts_id']))
                                    +"&from="+fromdate.strftime("%Y-%m-%dT%H:%M:%S+01")
                                    +"&to="+todate.strftime("%Y-%m-%dT%H:%M:%S+01")
                                    +"&format=json"
                                    ,verify=False).json()

            df = pd.DataFrame(json_data[0]['data'], columns = json_data[0]['columns'].split(','))
            df.set_index('Timestamp', inplace = True)
            df.index = pd.to_datetime(df.index,format="%Y-%m-%dT%H:%M:%S.%f%Z")

        return tsid,df.squeeze()

    def fromcsv(self,dir='spw',stationname='',stationcode='',which=Q1H,fromdate:datetime=None,todate:datetime=None):
        '''
        Lecture depuis un fichier csv créé depuis un import précédent
        Les fichiers doivent être disponibles depuis un sous-répertoire spw
        '''
        filename=filename=self._get_filename_series(stationname,stationcode,which)
           
        if exists(filename):
            mydata= pd.read_csv(filename,header=0,index_col=0,parse_dates=True,engine='pyarrow').squeeze("columns")
        else:
            return
        
        if fromdate is None and todate is None:
            return mydata
        elif fromdate is None:
            return mydata[:todate]
        elif todate is None:
            return mydata[fromdate:]
        else:
            return mydata[fromdate:todate]

    def saveas(self,flow:pd.Series,dir:str,stationname='',stationcode='',which=''):
        '''Sauvegarde d'une series pandas dans un fichier .csv'''
        filename=self._get_filename_series(stationname,stationcode,which)
        flow.to_csv(filename,header=['Data'])
    
    def get_stationid(self,name:str='',code=''):
        '''Récupération de l'id sur base du nom ou du code'''
        if name!='':
            return int(self.stations.loc[self.stations['station_name']==name.lower()]['station_id'])        
        elif code!='':
            return int(self.stations.loc[self.stations['station_no']==code]['station_id'])        

    def get_stationcode(self,name:str=''):
        '''Récupération du code sur base du nom'''
        if name!='':
            return self.stations.loc[self.stations['station_name']==name.lower()]['station_no'].squeeze()

    def get_stationname(self,code:str=''):
        '''Récupération du nom sur base du code'''
        if code!='':
            return self.stations.loc[self.stations['station_no']==code]['station_name'].squeeze()  


