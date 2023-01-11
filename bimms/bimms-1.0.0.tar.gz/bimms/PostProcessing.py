"""
	Python library to use BIMMS measurement setup - Post Processing 
	Authors: Florian Kolbl / Louis Regnacq
	(c) ETIS - University Cergy-Pontoise
		IMS - University of Bordeaux
		CNRS

	Requires:
		Python 3.6 or higher

"""
import andi as ai
import numpy as np
import json
from scipy.signal import savgol_filter

def SplitFit(N_fit,freq,data,polyOrder):
	SizeN = int(len(freq)/N_fit)
	if (N_fit==1):
		coef_list = [np.polyfit(freq, data, polyOrder)]
		freq_lim = [0]
	else:
		coef_list = []
		freq_lim = []
		for idx in range (N_fit):
			idx_min = SizeN*idx
			if (idx == N_fit):
				idx_max = SizeN*(idx+1)-1
			else:
				idx_max = SizeN*(idx+1)
			freq_split = freq[idx_min:idx_max]
			data_split = data[idx_min:idx_max]

			if type(polyOrder) is list:
				coef_split = np.polyfit(freq_split, data_split, polyOrder[idx])
			else:
				coef_split = np.polyfit(freq_split, data_split, polyOrder)

			coef_list.append(coef_split)
			freq_lim.append(freq_split[-1])
	return(coef_list,freq_lim)

def ComputeSplitFit(coef_list,freq_lim,freq):
	Nsplit = len(freq_lim)
	data_arr = []
	data = []
	freq_list_array = []
	if (Nsplit == 1):
		data_poly = np.poly1d(coef_list[0])
		data = data_poly(freq)
	else:
		for idx in range (Nsplit):
			if (idx==0):
				x = np.where(freq<=freq_lim[idx])
			else:
				x = np.where((freq<=freq_lim[idx]) & (freq>freq_lim[idx-1]))
			if (x):
				freq_split = freq[x]
				data_poly = np.poly1d(coef_list[idx])
				data = np.concatenate((data,data_poly(freq_split)),axis =0)
				freq_list_array = np.concatenate((freq_list_array,freq_split),axis =0)
		data = np.interp(freq, freq_list_array, data)
	return(data)

def unwrap_phase(phase):
	for x in range (len(phase)):
		if phase[x]>180:
			phase[x] = 360-phase[x]
			#print(open_cal_phase[x])
		if phase[x]<0:
			phase[x] = -(phase[x])
	return(-phase)

class MeasObj(object):
	def __init__(self,mag,phase,freq):
		super(MeasObj, self).__init__()
		self.mag = mag
		self.phase = phase
		self.freq = freq
		self.mag_filtered = []
		self.phase_filtered = []
		self.mag_coeff = []
		self.mag_freq_range = []
		self.phase_coeff  = []
		self.phase_freq_range  = []

	def FilterData(self,mag_filter_length,mag_filter_order,phase_filter_length,phase_filter_order):
		self.mag_filtered = savgol_filter(self.mag, mag_filter_length, mag_filter_order)								
		self.phase_filtered = savgol_filter(self.phase, phase_filter_length, phase_filter_order)

	def GetPoly(self,mag_n_split,mag_poly_order,phase_n_split,phase_poly_order):
		self.mag_coeff,self.mag_freq_range = SplitFit(mag_n_split,self.freq,self.mag_filtered,mag_poly_order)	
		self.phase_coeff,self.phase_freq_range = SplitFit(phase_n_split,self.freq,self.phase_filtered,phase_poly_order)	

	def PlotMagPoly(self,freq):
		mag_plot = ComputeSplitFit(self.mag_coeff,self.mag_freq_range,freq)
		return(mag_plot)

	def PlotPhasePoly(self,freq):
		phase_plot = ComputeSplitFit(self.phase_coeff,self.phase_freq_range,freq)
		return(phase_plot)

	def getMagErrorFit(self):
		mag_plot = self.PlotMagPoly(self.freq)
		mag_error_fit = 100*np.abs(mag_plot-self.mag_filtered)/self.mag_filtered
		return(mag_error_fit)

	def getPhaseErrorFit(self):
		phase_plot = self.PlotPhasePoly(self.freq)
		phase_error_fit = np.abs(phase_plot-self.phase_filtered)/self.phase_filtered
		return(phase_error_fit)

	def toJson(self):
		data = {}
		data['mag_coeff'] = np.array(self.mag_coeff).tolist()
		data['mag_freq_range'] = np.array(self.mag_freq_range).tolist()
		data['phase_coeff'] = np.array(self.phase_coeff).tolist()
		data['phase_freq_range'] = np.array(self.phase_freq_range).tolist()
		return(data)