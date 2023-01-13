from signaturizer import Signaturizer
import os
import pandas as pd
import numpy as np
from tqdm import tqdm
import joblib
from importlib import resources
from lime.lime_tabular import LimeTabularExplainer
import matplotlib.backends.backend_pdf
from matplotlib import pyplot as plt
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
                if key == 'MASTERISHERE':
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
        
class model_ensemble:
    def __init__(self,test,exp):        
        self.test = test
        self.exp = exp
    def extract_feature(self,data):        
        data=data.rename(columns={'GInstability_1':'GI','Apoptosis_1':'Apo','Electrophile_1':'Elec','Proliferation_1':'Prf','Oxidative_1':'Oxd','Epigenetics_1':'Epig'})
        return data.apply(pd.to_numeric)
    def get_labels(self,pred_test): #Getting discrete labels from probability values    
        test_pred = []        
        for i in range(pred_test.shape[0]):
            if(pred_test[i][0]>pred_test[i][1]):
                test_pred.append(0)
            else:
                test_pred.append(1)
        return test_pred 
    def explainibility(self,testdata,smi_list,mdl_id):
        pdf = []
        for r in range(len(mdl_id)):
            if mdl_id[r] == 'Unresolved':
                continue
            else:
                ID = mdl_id[r].split('_')[0].split('l')[-1]
                with resources.open_binary('Metabokiller','Ensemble-model_KFold'+ID+'train-data.csv') as fp:
                    traindata = fp.read()
                traindata=pd.read_csv(io.BytesIO(traindata))
                with resources.open_binary('Metabokiller','Ensmb_GBC_KFold'+ID+'.sav') as fp:
                    model_ensemble = fp.read()
                model_ensemble = joblib.load(io.BytesIO(model_ensemble))
                explainer = LimeTabularExplainer(np.array(traindata),mode='classification', feature_names=traindata.columns)
                explanation = explainer.explain_instance(testdata.values[r], model_ensemble.predict_proba)
                fig=explanation.as_pyplot_figure(label=1) 
                fig.suptitle(smi_list[r],fontweight ="bold",fontsize=8,ha="center",va='top')
                matplotlib.figure.Figure.set_figwidth(fig,15,forward=True)
                pdf.append(fig)
        return pdf
    def Voting(self,Rs):
        Epred=[]
        Eprob1=[]
        Eprob0=[]
        Best_mdl=[]
        Val1=Rs.filter(regex='_pred$').apply(lambda row: row[row == 1].index, axis=1)
        Val0=Rs.filter(regex='_pred$').apply(lambda row: row[row == 0].index, axis=1)
        for r in range(len(Rs)):
            if len(Val1[r])>len(Val0[r]):
                Epred.append(1)
                support_1=[]
                support_0=[]
                for c in Val1[r]:
                    c=c.split('_')[0]
                    support_1.append(c+'_1')
                    support_0.append(c+'_0')
                Eprob1.append(Rs[support_1].iloc[r].mean())
                Eprob0.append(Rs[support_0].iloc[r].mean())
                Best_mdl.append(Rs[support_1].iloc[r].sort_values(ascending=False).index[0])
            elif len(Val1[r])<len(Val0[r]):
                Epred.append(0)
                support_1=[]
                support_0=[]
                for c in Val0[r]:
                    c=c.split('_')[0]
                    support_1.append(c+'_1')
                    support_0.append(c+'_0')
                Eprob1.append(Rs[support_1].iloc[r].mean())
                Eprob0.append(Rs[support_0].iloc[r].mean())
                Best_mdl.append(Rs[support_1].iloc[r].sort_values(ascending=True).index[0])
            else:
                Epred.append('Unresolved')
                Eprob1.append('Unresolved')
                Eprob0.append('Unresolved')
                Best_mdl.append('Unresolved')
        return pd.DataFrame({'Ensemble_0':Eprob0,'Ensemble_1':Eprob1,'Ensemble_preds':Epred}),Best_mdl
       
    def test_model(self):
        test = self.test
        exp = self.exp
        test_filtered = self.extract_feature(test.filter(regex='_1$'))
        Ensmbl=pd.DataFrame()
        for m in range(20):
            with resources.open_binary('Metabokiller','Ensmb_GBC_KFold'+str(m)+'.sav') as fp:
                model = fp.read()
            model = joblib.load(io.BytesIO(model))
            probs = model.predict_proba(test_filtered)    
            preds = self.get_labels(probs)
            Ensmbl['Model'+str(m)+'_0']=probs[:,0]
            Ensmbl['Model'+str(m)+'_1']=probs[:,1]
            Ensmbl['Model'+str(m)+'_pred']=preds
        out,LM_mdls=self.Voting(Ensmbl)
        if exp == True:
            exp_fig = self.explainibility(test_filtered,test['smiles'],LM_mdls)
            return out,exp_fig
        else:
            return out
        
        
def Individual_predictions(Sig_data,exp):   
    predictions = pd.DataFrame(columns=['smiles','Epigenetics_0','Epigenetics_1','Epigenetics_preds',
    'Oxidative_0','Oxidative_1','Oxidative_preds','GInstability_0','GInstability_1','GInstability_preds',
    'Apoptosis_0','Apoptosis_1','Apoptosis_preds','Proliferation_0','Proliferation_1','Proliferation_preds',
    'Electrophile_0','Electrophile_1','Electrophile_preds'])
    predictions['smiles'] = Sig_data['smiles']
    m1 = model_epigenetic(Sig_data)
    m2 = model_oxidative(Sig_data)
    m3 = model_ginstability(Sig_data)
    m4 = model_electrophile(Sig_data)
    m5 = model_proliferation(Sig_data)   
    m6 = model_apoptosis(Sig_data)   
    probs,preds = m1.test_model()
    predictions['Epigenetics_0'] = probs[:,0]
    predictions['Epigenetics_1'] = probs[:,1]
    predictions['Epigenetics_preds'] = preds    
    probs,preds = m2.test_model()
    predictions['Oxidative_0'] = probs[:,0]
    predictions['Oxidative_1'] = probs[:,1]
    predictions['Oxidative_preds'] = preds    
    probs,preds = m3.test_model()    
    predictions['GInstability_0'] = probs[:,0]
    predictions['GInstability_1'] = probs[:,1]
    predictions['GInstability_preds'] = preds    
    probs,preds = m5.test_model()    
    predictions['Proliferation_0'] = probs[:,0]
    predictions['Proliferation_1'] = probs[:,1]
    predictions['Proliferation_preds'] = preds      
    probs,preds = m6.test_model()
    predictions['Apoptosis_0'] = probs[:,0]
    predictions['Apoptosis_1'] = probs[:,1]
    predictions['Apoptosis_preds'] = preds        
    probs,preds = m4.test_model() 
    predictions['Electrophile_0'] = probs[:,0]
    predictions['Electrophile_1'] = probs[:,1]
    predictions['Electrophile_preds'] = preds
    print('Compiling the results !!')
    m7 = model_ensemble(predictions,exp)
    if exp == True:
        votout , figures = m7.test_model() 
        predictions['Ensemble_0'] = votout['Ensemble_0']
        predictions['Ensemble_1'] = votout['Ensemble_1']
        predictions['Ensemble_preds'] = votout['Ensemble_preds']
        return predictions,figures
    else:
        votout = m7.test_model() 
        predictions['Ensemble_0'] = votout['Ensemble_0']
        predictions['Ensemble_1'] = votout['Ensemble_1']
        predictions['Ensemble_preds'] = votout['Ensemble_preds']
        return predictions
    
def predict(smi_list,explainability=False):
    st=license()
    if st=='STOP':
        return 0
    print('Performing descriptor calculation')
    Feature_data = pd.DataFrame()
    Feature_data['smiles'] = smi_list
    Sig_Carcin=Feature_Signaturizer(smi_list)
    if explainability == True:
        Final_out,exp_figures =Individual_predictions(Sig_Carcin,True)
        return Final_out,exp_figures
    else:
        Final_out = Individual_predictions(Sig_Carcin,False)
        return Final_out
