from signaturizer import Signaturizer
import os
import pandas as pd
import numpy as np
from tqdm import tqdm
import joblib
from importlib import resources
import io
import pkg_resources
import warnings
import socket

warnings.filterwarnings('ignore', '.*X does not have valid feature names*', )
warnings.filterwarnings('ignore', '.*signatures are NaN*', )
warnings.filterwarnings('ignore', '.*tensorflow:6*', )

def license(key='',package_path=''):
        d={'A':'C','B':'D','C':'E','D':'F','E':'G','F':'H','G':'I','H':'J','I':'K','J':'L','K':'M','L':'N','M':'O','N':'P','O':'Q','P':'R','Q':'S','R':'T','S':'U','T':'V','U':'W','V':'X','W':'Y','X':'Z','Y':'A','Z':'B'}
        if len(key)==0:
                with resources.open_binary('Metabokiller','license.lic') as fp:
                        lcdata = fp.read()
                lcdata=io.BytesIO(lcdata)
                host_name = socket.gethostname()
                clean_nm=''.join([x for x in host_name if x.isalnum()])
                clean_key=[]
                for i in clean_nm:
                        if i.isalpha():
                                clean_key.append(d[i.upper()])
                        if i.isnumeric():
                                clean_key.append(str(int(i)+2))
                ob_key=''.join(clean_key)
                if lcdata.getvalue().decode() == 'MASTERISHERE':
                        return 'GO'
                if lcdata.getvalue().decode() == ob_key:
                        return 'GO'
                else:
                        print('Metabokiller unlicensed: Please use license key for activation')
                        return 'STOP'
        else:
                host_name = socket.gethostname()
                clean_nm=''.join([x for x in host_name if x.isalnum()])
                clean_key=[]
                for i in clean_nm:
                        if i.isalpha():
                                clean_key.append(d[i.upper()])
                        if i.isnumeric():
                                clean_key.append(str(int(i)+2))
                ob_key=''.join(clean_key)
                if ob_key == key:
                        if len(package_path)==0:
                                package_path = pkg_resources.get_distribution('Metabokiller').location
                                write_byte = io.BytesIO(key.encode('ascii'))
                                with open(package_path+"/Metabokiller/license.lic", "wb") as f:
                                        f.write(write_byte.getbuffer())
                        else:
                                if os.path.exists():
                                        write_byte = io.BytesIO(key.encode('ascii'))
                                        with open(package_path+"/license.lic", "wb") as f:
                                                f.write(write_byte.getbuffer())
                                else:
                                        print('Package path couild not be found !! please provide path along the licens :(')
                        print('License installed successfuly :)')
                else:
                        print('Invalid license key provided !! Metabokiller activation failed :(')



def Feature_Signaturizer(dat):
    sig_df=pd.DataFrame()
    desc=['A','B','C','D','E']
    for dsc in tqdm(desc):
        for i in range(1,6):
            sign = Signaturizer(dsc+str(i),)
            results = sign.predict(dat)
            df=pd.DataFrame(results.signature)
            for clm in list(df.columns):
                df=df.rename(columns={clm:dsc+str(i)+'_'+str(clm)})
            sig_df=pd.concat([sig_df,df],axis = 1)
    sig_df = handle_missing_values(sig_df)
    res = pd.DataFrame()
    res['smiles'] = dat
    res = pd.concat([res,sig_df],axis = 1)
    return res
def handle_missing_values(data):
    print('Handling missing values')
    data = data.replace([np.inf, -np.inf, "", " "], np.nan)
    data = data.replace(["", " "], np.nan)
    for i in data.columns:
        data[i] = data[i].fillna(data[i].mean())
    return data


class model_epigenetic:
    def __init__(self,test):        
        self.test = test
    def extract_feature(self,data):        
        with resources.open_binary('Metabokiller','Epigenetics_features.csv') as fp:
                F_names = fp.read()
        F_names=pd.read_csv(io.BytesIO(F_names))
        features=F_names.iloc[:,0].tolist()
        return data[features]
    def get_labels(self,pred_test): #Getting discrete labels from probability values    
        test_pred = []        
        for i in range(pred_test.shape[0]):
            if(pred_test[i][0]>pred_test[i][1]):
                test_pred.append(0)
            else:
                test_pred.append(1)
        return test_pred 
       
    def test_model(self):
        test = self.test
        test_filtered = self.extract_feature(test.drop(['smiles'],axis=1))
        with resources.open_binary('Metabokiller','Epigenetic_svm.pkl') as fp:
                model = fp.read()
        model = joblib.load(io.BytesIO(model))
        probs = model.predict_proba(test_filtered)    
        preds = self.get_labels(probs)
        return probs,preds


class model_apoptosis:
    def __init__(self,test):        
        self.test = test
    def extract_feature(self,data):        
        with resources.open_binary('Metabokiller','Apoptosis_features.csv') as fp:
                F_names = fp.read()
        F_names=pd.read_csv(io.BytesIO(F_names))
        features=F_names.iloc[:,0].tolist()
        return data[features]
    def get_labels(self,pred_test): #Getting discrete labels from probability values    
        test_pred = []        
        for i in range(pred_test.shape[0]):
            if(pred_test[i][0]>pred_test[i][1]):
                test_pred.append(0)
            else:
                test_pred.append(1)
        return test_pred 
       
    def test_model(self):
        test = self.test
        test_filtered = self.extract_feature(test.drop(['smiles'],axis=1))
        with resources.open_binary('Metabokiller','Apoptosis_KNN.sav') as fp:
                model = fp.read()
        model = joblib.load(io.BytesIO(model))
        probs = model.predict_proba(test_filtered)    
        preds = self.get_labels(probs)
        return probs,preds
        

class model_oxidative:
    def __init__(self,test):        
        self.test = test
    def extract_feature(self,data):        
        with resources.open_binary('Metabokiller','Oxidative_features.csv') as fp:
                F_names = fp.read()
        F_names=pd.read_csv(io.BytesIO(F_names))
        features=F_names.iloc[:,0].tolist()
        return data[features]
    def get_labels(self,pred_test): #Getting discrete labels from probability values    
        test_pred = []        
        for i in range(pred_test.shape[0]):
            if(pred_test[i][0]>pred_test[i][1]):
                test_pred.append(0)
            else:
                test_pred.append(1)
        return test_pred 
       
    def test_model(self):
        test = self.test
        test_filtered = self.extract_feature(test.drop(['smiles'],axis=1))
        with resources.open_binary('Metabokiller','Oxidative_mlp.pkl') as fp:
                model = fp.read()
        model = joblib.load(io.BytesIO(model))
        probs = model.predict_proba(test_filtered)    
        preds = self.get_labels(probs)
        return probs,preds
        

class model_ginstability:
    def __init__(self,test):        
        self.test = test
    def extract_feature(self,data):        
        with resources.open_binary('Metabokiller','Genomic_Instability_features.csv') as fp:
                F_names = fp.read()
        F_names=pd.read_csv(io.BytesIO(F_names))
        features=F_names.iloc[:,0].tolist()
        return data[features]
    def get_labels(self,pred_test): #Getting discrete labels from probability values    
        test_pred = []        
        for i in range(pred_test.shape[0]):
            if(pred_test[i][0]>pred_test[i][1]):
                test_pred.append(0)
            else:
                test_pred.append(1)
        return test_pred 
       
    def test_model(self):
        test = self.test
        test_filtered = self.extract_feature(test.drop(['smiles'],axis=1))
        with resources.open_binary('Metabokiller','Genomic_Instabilty_RF.sav') as fp:
                model = fp.read()
        model = joblib.load(io.BytesIO(model))
        probs = model.predict_proba(test_filtered)    
        preds = self.get_labels(probs)
        return probs,preds
        
class model_proliferation:
    def __init__(self,test):        
        self.test = test
    def extract_feature(self,data):        
        with resources.open_binary('Metabokiller','Proliferation_features.csv') as fp:
                F_names = fp.read()
        F_names=pd.read_csv(io.BytesIO(F_names))
        features=F_names.iloc[:,0].tolist()
        return data[features]
    def get_labels(self,pred_test): #Getting discrete labels from probability values    
        test_pred = []        
        for i in range(pred_test.shape[0]):
            if(pred_test[i][0]>pred_test[i][1]):
                test_pred.append(0)
            else:
                test_pred.append(1)
        return test_pred 
       
    def test_model(self):
        test = self.test
        test_filtered = self.extract_feature(test.drop(['smiles'],axis=1))
        with resources.open_binary('Metabokiller','Proliferation_RF.pkl') as fp:
                model = fp.read()
        model = joblib.load(io.BytesIO(model))
        probs = model.predict_proba(test_filtered)    
        preds = self.get_labels(probs)
        return probs,preds
        
class model_electrophile:
    def __init__(self,test):        
        self.test = test
    def extract_feature(self,data):        
        with resources.open_binary('Metabokiller','Electrophile_features.csv') as fp:
                F_names = fp.read()
        F_names=pd.read_csv(io.BytesIO(F_names))
        features=F_names.iloc[:,0].tolist()
        return data[features]
    def get_labels(self,pred_test): #Getting discrete labels from probability values    
        test_pred = []        
        for i in range(pred_test.shape[0]):
            if(pred_test[i][0]>pred_test[i][1]):
                test_pred.append(0)
            else:
                test_pred.append(1)
        return test_pred 
       
    def test_model(self):
        test = self.test
        test_filtered = self.extract_feature(test.drop(['smiles'],axis=1))
        with resources.open_binary('Metabokiller','Electrophile_MLP.pkl') as fp:
                model = fp.read()
        model = joblib.load(io.BytesIO(model))
        probs = model.predict_proba(test_filtered)    
        preds = self.get_labels(probs)
        return probs,preds

    
def Epigenetics(smi_list):
    st=license()
    if st=='STOP':
        return 0
    print('Performing descriptor calculation')
    Feature_data = pd.DataFrame()
    Feature_data['smiles'] = smi_list
    Sig_Carcin=Feature_Signaturizer(smi_list)
    m1 = model_epigenetic(Sig_Carcin)
    probs,preds = m1.test_model()
    Feature_data['Epigenetics_0'] = probs[:,0]
    Feature_data['Epigenetics_1'] = probs[:,1]
    Feature_data['Epigenetics_preds'] = preds 
    return Feature_data
def Oxidative(smi_list):
    st=license()
    if st=='STOP':
        return 0
    print('Performing descriptor calculation')
    Feature_data = pd.DataFrame()
    Feature_data['smiles'] = smi_list
    Sig_Carcin=Feature_Signaturizer(smi_list)
    m2 = model_oxidative(Sig_Carcin)
    probs,preds = m2.test_model()
    Feature_data['Oxidative_0'] = probs[:,0]
    Feature_data['Oxidative_1'] = probs[:,1]
    Feature_data['Oxidative_preds'] = preds
    return Feature_data
def GInstability(smi_list):
    st=license()
    if st=='STOP':
        return 0
    print('Performing descriptor calculation')
    Feature_data = pd.DataFrame()
    Feature_data['smiles'] = smi_list
    Sig_Carcin=Feature_Signaturizer(smi_list)
    m3 = model_ginstability(Sig_Carcin)
    probs,preds = m3.test_model()    
    Feature_data['GInstability_0'] = probs[:,0]
    Feature_data['GInstability_1'] = probs[:,1]
    Feature_data['GInstability_preds'] = preds
    return Feature_data
def Electrophile(smi_list):
    st=license()
    if st=='STOP':
        return 0
    print('Performing descriptor calculation')
    Feature_data = pd.DataFrame()
    Feature_data['smiles'] = smi_list
    Sig_Carcin=Feature_Signaturizer(smi_list)
    m4 = model_electrophile(Sig_Carcin)
    probs,preds = m4.test_model() 
    Feature_data['Electrophile_0'] = probs[:,0]
    Feature_data['Electrophile_1'] = probs[:,1]
    Feature_data['Electrophile_preds'] = preds
    return Feature_data
def Proliferation(smi_list):
    st=license()
    if st=='STOP':
        return 0
    print('Performing descriptor calculation')
    Feature_data = pd.DataFrame()
    Feature_data['smiles'] = smi_list
    Sig_Carcin=Feature_Signaturizer(smi_list)
    m5 = model_proliferation(Sig_Carcin)
    probs,preds = m5.test_model()    
    Feature_data['Proliferation_0'] = probs[:,0]
    Feature_data['Proliferation_1'] = probs[:,1]
    Feature_data['Proliferation_preds'] = preds
    return Feature_data
def Apoptosis(smi_list):
    st=license()
    if st=='STOP':
        return 0
    print('Performing descriptor calculation')
    Feature_data = pd.DataFrame()
    Feature_data['smiles'] = smi_list
    Sig_Carcin=Feature_Signaturizer(smi_list)
    m6 = model_apoptosis(Sig_Carcin)
    probs,preds = m6.test_model()
    Feature_data['Apoptosis_0'] = probs[:,0]
    Feature_data['Apoptosis_1'] = probs[:,1]
    Feature_data['Apoptosis_preds'] = preds
    return Feature_data
