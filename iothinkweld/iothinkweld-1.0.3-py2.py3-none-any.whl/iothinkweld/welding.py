import pandas as pd
import numpy as np
import time
from iothinkdb import icache
import requests
import math
from scipy.stats import pearsonr


def iothink_create_std_curve(df,p1,p2,p3,p4):
	if df.shape[1] == 1:
		model_power = df.iloc[:,0]
		hmean=max(model_power)
		amean=sum(model_power)
		d11 = 1 - p1
		d21 = hmean*(1-p2)
		d22 = hmean*(1+p2)
		d31 = amean*(1-p3)
		d32 = amean*(1+p3)
		d41 = 1-p4
		model_power = list(model_power)
		model_power = [round(i,2) for i in model_power]
		model={"power":model_power,"d11":d11,"d21":d21,"d22":d22,"d31":d31,"d32":d32,"d41":d41}
	if df.shape[1] > 1:
		corr_table = df.corr()
		corr_table_tri=corr_table.values[np.triu_indices_from(corr_table.values,1)]
		corr_table_mean = corr_table_tri.mean()
		corr_table_std = corr_table_tri.std()
		cutoff = corr_table_mean - corr_table_std
		match_ratio =  pd.DataFrame(corr_table[corr_table >= cutoff].count()/len(df.columns), columns=['match_ratio'])
		df_T = pd.DataFrame(df.values.T)
		good_sample = df_T[match_ratio['match_ratio']>=0.7]
		model_power = good_sample.mean()
		df_point=good_sample.agg([np.max,np.sum],axis=1)
		hmean = df_point['amax'].agg([np.mean,np.std])[0]
		amean = df_point['sum'].agg([np.mean,np.std])[0]
		d11 = 1 - p1
		d21 = hmean*(1-p2)
		d22 = hmean*(1+p2)
		d31 = amean*(1-p3)
		d32 = amean*(1+p3)
		d41 = 1-p4
		model_power = list(model_power)
		model_power = [round(i,2) for i in model_power]
		model={"power":model_power,"d11":d11,"d21":d21,"d22":d22,"d31":d31,"d32":d32,"d41":d41}
	return model

def iothink_corr_confidence(x,a=0.98,benchmark_p=0.9,benchmark_n=0.82):
	if x == 1:
		return 1.
	log = math.log(x,a)
	z = 1-1/log
	output1 = benchmark_p +  (x - a)/(1-a) * (1-benchmark_p)
	output2 = benchmark_n +  (1-1/log) * (1-benchmark_n)
	return output1 if 1/log >= a else output2

def iothink_update_param(equipment_name):
	cache = icache.iCache()
	counter = cache.get(equipment_name+'_counter')
	if counter is not None:
		counter = int(counter) + 1
	else:
		counter = 1
	cache.set(equipment_name+'_counter',counter)
	last_model_time = cache.get(equipment_name+"_last_model_time")
	return counter,int(last_model_time)

def iothink_init_param(equipment_name,modeltime):
	cache = icache.iCache()
	cache.set(equipment_name+'_counter',1)
	cache.set(equipment_name+"_last_model_time", int(time.mktime(modeltime.timetuple())))

def iothink_crossline(line1,line2):
	line3 = []
	for i in range(len(line1)):
		if line1[i]<=line2[i]:
			line3.append(line1[i])
		else:
			line3.append(line2[i])
	return line3

def iothink_shift_corr(line1,line2):
    cut_point = max(line2)*0.1
    length = len(line2)
    for i in range(len(line2)):
        if line2[i] > cut_point:
            break
    for j in range(len(line1)):
        if line1[j] > cut_point:
            break
    if j >= length/2:
        corri = 0.1
    elif i>=j:
        line1_new = [cut_point]*i+line1[j:j+length-i]
        line2_new = [cut_point]*i+line2[i:]
        corri = pearsonr(list(line2_new),line1_new)[0]
    else:
        line1_new = [cut_point]*j+line1[j:]
        line2_new = [cut_point]*j+line2[i:i+length-j] 
        corri = pearsonr(line2_new,line1_new)[0]
    return corri

def iothink_check_std_curve(df,model):
	d1 = iothink_shift_corr(df,model["power"])
	d12 = pearsonr(df,model["power"])[0]
	d2 = max(df)
	d3 = sum(df)
	d4 = sum(iothink_crossline(df,model["power"]))/sum(model["power"])
	hmean = (model["d21"]+model["d22"])/2
	amean = (model["d31"]+model["d32"])/2
	result_list = [d1>=model["d11"],model["d21"]<=d2<=model["d22"],model["d31"]<=d3<=model["d32"],d4>=model["d41"]]
	d41 = model["d41"]
	if d4 <= d41:
		r = 7
	elif d4 <= d41+0.05:
		r = 6
	elif d4 <= d41+0.1:
		r = 5
	else:
		r = 0											 
	c = round(iothink_corr_confidence(d1),5)
	result = {"confidence":c,"prediction":r,"power":model['power']}
	result2 = {"confidence":c,"prediction":r,"corri":d1,"corri2":d12,"gi":hmean,"gi2":d2,"ai":amean,"ai2":d3,"ai3":d4}
	return result,result2
	
def iothink_check_std_curve2(df,model):
	d1 = iothink_shift_corr(df,model["power"])
	d12 = pearsonr(df,model["power"])[0]
	d2 = max(df)
	d3 = sum(df)
	d4 = sum(iothink_crossline(df,model["power"]))/sum(model["power"])
	hmean = (model["d21"]+model["d22"])/2
	amean = (model["d31"]+model["d32"])/2							 
	c = round(iothink_corr_confidence(d1),5)
	return c,d1,d12,d2,d3,d4,hmean,amean

def iothink_autoupdate_model(current_model,current_modeltime,ip,modelid,init_sample_count,step_sample_count,update_sample_count,s):
	counter,last_model_time = iothink_update_param("eq1")
	if counter <= init_sample_count or last_model_time == int(time.mktime(current_modeltime.timetuple())):
		if counter == init_sample_count:
			url=f"http://{ip}:7600/api/v1/model?model={modelid}&s={s}&num={init_sample_count}&model_type=1"
			requests.post(url)
		return "",counter
	else:
		if counter == step_sample_count:
			url=f"http://{ip}:7600/api/v1/model?model={modelid}&s={s}&num={step_sample_count}&model_type=1"
			requests.post(url)
		if counter%update_sample_count == 0:
			url=f"http://{ip}:7600/api/v1/model?model={modelid}&s={s}&num={step_sample_count}&model_type=2"
			requests.post(url)
		return current_model,counter