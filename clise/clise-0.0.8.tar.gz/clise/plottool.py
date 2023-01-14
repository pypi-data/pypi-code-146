
# Jaesub Hong (jhong@cfa.harvard.edu)
# to do 
#	- log scale tick labeling 
#	- multiplot for modeling fitting

if 'clise' in __file__:
	import clise.jsontool as jt
	import clise.tabletool as tt
else:
	import jsontool as jt
	import tabletool as tt

from collections import OrderedDict

import pandas
import astropy
from astropy.table import Table, QTable
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.colors import Normalize, LogNorm, ListedColormap
import matplotlib.cm	 as cm
import matplotlib		 as mpl
from matplotlib.patches		import Circle
from matplotlib			import rc,rcParams
from matplotlib.ticker		import LogLocator
#from mpl_toolkits.axes_grid1  import make_axes_locatable
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

import numpy as np
import math
import healpy	as hp

from astropy.io import fits

from scipy import optimize as opt
from scipy import ndimage

from os		import path
from functools	import wraps

from IPython	import embed
import subprocess
from scipy.signal import savgol_filter
import re
from pathlib	import Path

cc=jt.cc

# obsolete?
def help_rcParams():
	text=OrderedDict()
	text["figure.figsize"       ] ="changes the figure size; keeps the font size the same"
	text["figure.dpi"		    ] ="changes the figure size; keep relative size of font to figure the same"
	text["font.size"		    ] ="change the font size; keeps the figure size the same"

	text["axes.labelsize"	    ] ="Fontsize of the x and y labels"
	text["axes.titlesize"	    ] ="Fontsize of the axes title"
	text["figure.titlesize"	    ] ="Size of the figure title (Figure.suptitle())"
	text["xtick.labelsize"	    ] ="Fontsize of the tick labels"
	text["ytick.labelsize"	    ] ="Fontsize of the tick labels"

	text["legend.fontsize"	    ] ="Fontsize for legends (plt.legend(), fig.legend())"
	text["legend.title_fontsize"] ="Fontsize for legend titles, None sets to the same as the default axes."
	text["legend.facecolor"	    ]	="Background color for legend"
	text["legend.edgecolor"	    ]	="Edge color for legend"
	text["legend.framealpha"    ]	="Background alpha for legend: 0.5"
	text["legend.labelspacing"  ]	="Vertical spacing for legend: 0.5"
	text["legend.frameon"       ]	="Legend frame: true"
	text["legend.loc"		    ] ="Location for legend: best"

	text["axes.grid"] ="Grid True or False"
	text["grid.alpha"] ="Grid transparency"
	text["grid.color"] ="Grid color"

	text["xtick.direction"] ="xtick direction"
	text["ytick.direction"] ="ytick direction"
	return text

# obsolete?
def help_text(param):
	if param != None:
		if param == "mpl":
			print("rcParams:")
			jt.show(help_rcParams(),  notype=True)
			print("e.g., -*#rcParams:figure.figsize '12,10'")
			print
			print("See also",mpl.matplotlib_fname())
		elif param == "1d":
			print("Parameters for 1-d plot")
		elif param == "2d":
			print("Parameters for 2-d plot")
		elif param == "m1d":
			print("Parameters for 1-d plot for multiple data sets")
		elif param == "m2d":
			print("Parameters for 2-d plot for multiple data sets")
		elif param == "overview":
			print("decorator:")
			print("	prep_data_deco")
			print("	prep_model_deco")
			print("for one data set:")
			print("	plot1d     : 1-D plot, scatter, histogram, line ")
			print("	dplot      : 2-D density plot with 1-D histograms")
			print("	hp2mollview: healpix to mollview conversion")
			print("	plotDMR    : plot data, model & residual, usually for spectral fits")
			print("for multiple data sets:")
			print("	mplot1d       : 1-D plot, scatter, histogram, line ")
			print("	rplot1d       : 1-D ratio plot against one reference data set ")
			print("	mdplot        : 2-D density plot with 1-d histograms")
			print("	mdplot_3color : 2-D density plot of up-to 3 sets using true 3 color composite")
			print("	scan_fits_cols: plot all the columns of a fits file hdu")
			print("	scan_fits_hdus: plot a column of all the hdus of a fits hdu")
		else:
			print("params: overview mpl 1d 2d m1d m2d")

		exit()

#----------------------------------------------------------------------------------------
class LogNorm_mid(LogNorm):
	def __init__(self, vmin=None, vmax=None, mid=None, clip=False):
		LogNorm.__init__(self,vmin=vmin, vmax=vmax, clip=clip)
		self.mid=mid
	def __call__(self, value, clip=None):
		# I'm ignoring masked values and all kinds of edge cases to make a
		# simple example...
		x, y = [np.log(self.vmin), np.log(self.mid), np.log(self.vmax)], [0, 0.5, 1]
		return np.ma.masked_array(np.interp(np.log(value), x, y))

class Norm_mid(Normalize):
	def __init__(self, vmin=None, vmax=None, mid=None, clip=False):
		Normalize.__init__(self,vmin=vmin, vmax=vmax, clip=clip)
		self.mid=mid
	def __call__(self, value, clip=None):
		# I'm ignoring masked values and all kinds of edge cases to make a
		# simple example...
		x, y = [self.vmin, self.mid, self.vmax], [0, 0.5, 1]
		return np.ma.masked_array(np.interp(value, x, y))

#----------------------------------------------------------------------------------------
def minmax(data, nonzero=False):
	if nonzero: 
		data=np.array(data)
		return [np.min(data[np.nonzero(data)]), np.max(data)]
	else:       return [np.min(data), np.max(data)]

#----------------------------------------------------------------------------------------
scino = re.compile('[+\-]?(?:0|[1-9]\d*)(?:\.\d*)?(?:[eE][+\-]?\d+)?')
def get_number(array):
	# need to vectorize this....
	# and implement this in tabletool to separate them out
	ans=[]
	# if type(array[0]) is not str: return array
	for each in array:
		# val=re.split('(\D|^\.)',each)
		# val=re.search('^\s*([-\+][0-9.]+)',each)
		val=re.findall(scino, each)
		try: ans.append(float(val[0]))
		except: 
			ans.append(0.0)
			print('cannot find a number in', each)
	return ans

#----------------------------------------------------------------------------------------
def read_pars(par,  data=None, nopandas=True, dataset=None):
	ans=OrderedDict()
	if type(dataset).__name__ == 'NoneType': dataset=OrderedDict()
	for key, val in par.items():
		if type(val) is str:
			ans[key] = data[val]
		else:
			if not path.isfile(val['file']):
				print("cannot read the file:", val['file'])
				return None

			if val['file'] not in dataset:
				dataset[val['file']]=tt.from_csv_or_fits(val['file'],
						ftype=val.get('ftype',None), 
						hdu=val.get('hdu',1), nopandas=nopandas)
			ans[key] = dataset[val['file']][val['column']]
	return ans
	
def read(infile, x="", y="", hdu=1, data=None,
		xlabel=None, ylabel=None,
		ftype=None, nopandas=True, attr=''):
	if type(data).__name__ == "NoneType":
		if infile == None: 
			print(cc.err+"input data or file is required.",cc.reset)
			return None, None, None, None, None 

		if not path.isfile(infile):
			print(cc.err+"cannot read the file:", infile,cc.reset)
			return None, None, None, None, None

		data=tt.from_csv_or_fits(infile, ftype=ftype, hdu=hdu, nopandas=nopandas)

	if x == "" or y == "":
		if   type(data) is pandas.core.frame.DataFrame: colnames=data.columns.values.tolist()
		elif type(data) is   astropy.table.table.Table: colnames=data.colnames
		else: print('need to know column names or provide -x and -y')

#		colnames=data.colnames
		if x == "": 
			if len(colnames) == 1: x='_auto_'
			else:			     x=colnames[0]
		if y == "": 
			if len(colnames) == 1: y=colnames[0]
			else:			     y=colnames[1]
	
	# default label
	if xlabel == None:
		if x != '_auto_':
			xlabel = x 
			if hasattr(data[x],'info'):
				if hasattr(data[x].info,'unit'):
					xunit=data[x].info.unit
					if xunit != None: xlabel = xlabel +' ('+str(xunit)+')'

	if ylabel == None:
		attrs = attr.split(',')
		if 'makehist' not in attrs:
			ylabel = y 
			if hasattr(data[y],'info'):
				if hasattr(data[y].info,'unit'):
					yunit=data[y].info.unit
					if yunit != None: ylabel = ylabel +' ('+str(yunit)+')'
		else:
			ylabel='counts'

	return data, x, y, xlabel, ylabel
	
def minmax(data, nonzero=False):
	if nonzero: 
		data=np.array(data)
		return [np.min(data[np.nonzero(data)]), np.max(data)]
	else:       return [np.min(data), np.max(data)]

def set_range(data, margin=None, 
		dr=None, # data range
		dmin=None, dmax=None,
		scale='linear', drawdown=None):

	if type(dr) is list: 
		if dr[0] == None: dr = None
	
	if type(dr).__name__ == 'NoneType': dr= minmax(data, nonzero= scale != 'linear')

	if dmin != None: dr[0] = dmin
	if dmax != None: dr[1] = dmax

	if margin != None:
		dr = add_margin(dr, margin=margin, scale=scale, drawdown=drawdown)

	return dr

def set_range_2D(xdata, ydata, margin=None, xr=None, yr=None, 
		xmin=None, xmax=None, ymin=None, ymax=None,
		xlowdata=None, xhighdata=None, xerrdata=None,
		ylowdata=None, yhighdata=None, yerrdata=None, 
		attr='', nbin=None, binsize=None,
		xscale='linear', yscale='linear', drawdown=None):

	if type(xr) is list: 
		if xr[0] == None: xr = None
	if type(yr) is list: 
		if yr[0] == None: yr = None
	
	ignore_xr=False
	ignore_yr=False
	if type(xr).__name__ == 'NoneType': 
		ignore_xr=True
		if type(xlowdata).__name__ != 'NoneType':
			xr= minmax(np.concatenate((np.array(xlowdata),np.array(xhighdata))), nonzero= xscale != 'linear')
		elif type(xerrdata).__name__ != 'NoneType':
			xr= minmax(np.concatenate((np.array(xdata-xerrdata),np.array(xdata+xerrdata))), nonzero= xscale != 'linear')
		else:
			xr= minmax(xdata, nonzero= xscale != 'linear')

	if type(yr).__name__ == 'NoneType': 
		ignore_yr=True
		if type(ylowdata).__name__ != 'NoneType':
			yr= minmax(np.concatenate((np.array(ylowdata),np.array(yhighdata))), nonzero= yscale != 'linear')
		elif type(yerrdata).__name__ != 'NoneType':
			yr= minmax(np.concatenate((np.array(ydata-yerrdata),np.array(ydata+yerrdata))), nonzero= yscale != 'linear')
		else:
			yr= minmax(ydata, nonzero= yscale != 'linear')

	if xmin != None: xr[0] = xmin
	if xmax != None: xr[1] = xmax
	if ymin != None: yr[0] = ymin
	if ymax != None: yr[1] = ymax

	if margin != None:
		if type(margin) is not list:
			xr = add_margin(xr, margin=margin, scale=xscale, drawdown=drawdown)
			yr = add_margin(yr, margin=margin, scale=yscale, drawdown=drawdown)
		elif len(margin) == 2:
			xr = add_margin(xr, margin=margin[0], scale=xscale, drawdown=drawdown)
			yr = add_margin(yr, margin=margin[1], scale=yscale, drawdown=drawdown)
		elif len(margin) == 4:
			xr = add_margin(xr, margin=margin[0:1], scale=xscale, drawdown=drawdown)
			yr = add_margin(yr, margin=margin[2:3], scale=yscale, drawdown=drawdown)

	edges=None
	attrs = attr.split(',')
	if 'makehist' in attrs:
		if ignore_xr or ignore_yr:
			if binsize==None:  binsize = (xr[1]-xr[0])/nbin
			else:              nbin = int((xr[1]-xr[0])/binsize)

			edges = get_edges(xr, nbin, scale = xscale)
			new_y, *_ = np.histogram(xdata, bins=edges)
			xh, yh, new_x = hist2line(edges, new_y)

			if ignore_xr: xr=None
			if ignore_yr: yr=None
			xr, yr, edges = set_range_2D(new_x, new_y, xr=xr, yr=yr, 
				xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax,
				margin=margin, drawdown=drawdown, 
				xlowdata=xlowdata, xhighdata=xhighdata, xerrdata=xerrdata,
				ylowdata=ylowdata, yhighdata=yhighdata, yerrdata=yerrdata,
				xscale=xscale, yscale=yscale)
	return xr, yr, edges

def get_log_edges(vr, nbin):
	logvr = [math.log(vr[0],10), math.log(vr[1],10)]
	logslope = logvr[1] - logvr[0]
	return [10.0**(logslope*v/nbin+logvr[0]) for v in range(0,nbin+1)]

def get_edges(vr, nbin, scale='linear'):
	if scale == 'linear':
		step = (vr[1] - vr[0])/nbin
		return [v*step+vr[0] for v in range(0,nbin+1)]
	elif scale == 'log':
		logvr = [math.log(vr[0],10), math.log(vr[1],10)]
		logslope = logvr[1] - logvr[0]
		return [10.0**(logslope*v/nbin+logvr[0]) for v in range(0,nbin+1)]

def add_margin(prange, margin=None, scale='linear', drawdown=None):

	if   margin == None     : margin=[0.2,0.2]
	elif np.isscalar(margin): margin=[margin, margin]
	if scale == 'linear':
		diff=prange[1]-prange[0]
		prange=[prange[0]-margin[0]*diff,prange[1]+margin[1]*diff]
	else:
		if prange[0] <= 0.0:
			if drawdown == None: drawdown = 1.e-5
			prange[0]=prange[1]*drawdown

		logpr = [math.log(v,10) for v in prange]
		diff = logpr[1]-logpr[0]
		logpr=[logpr[0]-margin[0]*diff,logpr[1]+margin[1]*diff]
		prange=[10.0**v for v in logpr]

	return prange

def filter_by_range(xdata, ydata, xr, yr, weights=None):
#	embed()
#	xdata=np.array(xdata)
#	ydata=np.array(ydata)
	mask = (xdata >= xr[0]) & (xdata <= xr[1]) & (ydata >= yr[0]) & (ydata <= yr[1]) 
	xdata=xdata[mask]
	ydata=ydata[mask]

	if type(weights).__name__ != 'NoneType':
		weights=weights[mask]
#	if filter:
#		 data=data[data[x] >= xr[0]]
#		 data=data[data[x] <= xr[1]]
#		 data=data[data[y] >= yr[0]]
#		 data=data[data[y] <= yr[1]]

	return xdata, ydata, weights

def val2pix(val, vr=None, pr=None):
	# value to pixel
	slope=(pr[1]-pr[0])/(vr[1]-vr[0])
	if type(val) is not list:
		return int(slope*(val-vr[1])+pr[0])
	return [int(slope*(v-vr[1])+pr[0]) for v in val]

def pix2val(pix, vr=None, pr=None):
	# pixel to value
	slope=(vr[1]-vr[0])/(pr[1]-pr[0])
	if type(pix) is not list:
		return slope*(pix-pr[0])+vr[0]
	return [slope*(p-pr[0])+vr[0] for p in pix]

#----------------------------------------------------------------------------------------
def set_rcParams(rcParams=None, verbose=0, force=False, name=None):
	# run only once unless forced
	if not force:
		if hasattr(set_rcParams,'new'): return
	set_rcParams.new=False

	defaults = OrderedDict()
	if rcParams == None: 
		if name == None: return
		elif name == "dplot":
			defaults["xtick.top"		]= False
			defaults["ytick.right"		]= False
			defaults["axes.grid"		]= False
			defaults["xtick.direction"	]= "out"
			defaults["ytick.direction"	]= "out"
		else: return
		rcParams= OrderedDict()

	for key, val in rcParams.items():
		if verbose >=2: print(key,val)
		plt.rcParams[key] = val

	for key in defaults.keys() - rcParams.keys():
		if verbose >=2: print(key,defaults[key])
		plt.rcParams[key] = defaults[key]
	
#----------------------------------------------------------------------------------------
def wrap(plt, xr=None, yr=None, xlabel=None, ylabel=None, 
		title="", xscale='linear', yscale='linear', outfile=None, 
		y_title=1.0, rect=[0,0,1,1],
		ax2=None, ay2=None, ax=None, 
		xlabel2=None, ylabel2=None, 
		xr2=None, yr2=None, tight=True,
		xticks=None, yticks=None,
		xtickv=None, ytickv=None, grid=None,
		text=None, text_kw=None,
		polygon=None, polygon_kw=None,
		ellipse=None, ellipse_kw=None,
		loc_ylabel='center', rcParams=None,
		label=True, display=True, ion=False):

	if rcParams!=None: 
		set_rcParams(rcParams, force=True, name=None)
	annotate(data=text, common_kwargs=text_kw)
	add_polygon(data=polygon, common_kwargs=polygon_kw)
	add_ellipse(data=ellipse, common_kwargs=ellipse_kw)

	if label:
		if xlabel != None: ax.set_xlabel(xlabel)
		if ax2 != None: 
			if xlabel2 != None: 
				# print(ax2, xlabel2)
				ax2.set_xlabel(xlabel2)

		if ylabel != None: ax.set_ylabel(ylabel, loc=loc_ylabel)
		if ay2 != None: 
			if ylabel2 != None: 
#				print(ay2, ylabel2)
				ay2.set_ylabel(ylabel2)
#		print('rect',rect)
		# this needs a clean up
		plt.title(title, y=y_title)

	if type(xr).__name__ != "NoneType":
		ax.set_xlim(xr)

	if ax2 != None: 
		if type(xr2).__name__ != "NoneType":
			ax2.set_xlim(xr2)

	if type(yr).__name__ != "NoneType":
		ax.set_ylim(yr)
	if ay2 != None: 
		if type(yr2).__name__ != "NoneType":
			ay2.set_ylim(yr2)

	# if xscale != None: plt.xscale(xscale)
	# if yscale != None: plt.yscale(yscale)
	aux_xtick=False
	if xscale != None: 
		ax.set_xscale(xscale)
		if xscale == "log":
			xr=ax.get_xlim()
			if xr[1]/xr[0] < 100:
				aux_xtick=True
		if ax2 != None: 
			ax2.set_xscale(xscale)
	aux_ytick=False
	if yscale != None: 
		ax.set_yscale(yscale)
		if yscale == "log":
			yr=ax.get_ylim()
			if yr[1]/yr[0] < 100:
				aux_ytick=True
		if ay2 != None: 
			ay2.set_yscale(yscale)

	# locs, labels = plt.xticks()
	# embed()

	if type(xticks).__name__ != "NoneType":
		if type(xtickv).__name__ == "NoneType":
			xtickv=[float(v) for v in xticks]
		ax.set_xticks(xtickv, xticks)
		# ax.set_xticks(xtickv)
	if type(yticks).__name__ != "NoneType":
		if type(ytickv).__name__ == "NoneType":
			ytickv=[float(v) for v in yticks]
		ax.set_yticks(ytickv, yticks)

	if tight:
		plt.tight_layout(rect=rect)
	if grid != None:
		if type(grid) is bool:
			if grid == True:
				ax.grid(True)
				if ax2 != None: ax2.grid(False)
				if ay2 != None: ay2.grid(False)
			else:
				ax.grid(False)
				if ax2 != None: ax2.grid(False)
				if ay2 != None: ay2.grid(False)
		else:
			if type(grid) is str: grid=[grid]
			if ax2 != None and ay2 != None:
				if 'ax2' in grid and 'ay2' in grid: 
					ax2.grid(True, axis='x')
					ay2.grid(True, axis='y')
			elif ax2 != None:
				if 'ax2' in grid: 
					ax.grid(True, axis='y')
					ax2.grid(True, axis='x')
			elif ay2 != None:
				if 'ay2' in grid: 
					ax.grid(True, axis='x')
					ax2.grid(True, axis='y')

	if not ion: 
		if outfile != None: 
			plt.savefig(Path(outfile).expanduser())
			plt.close("all")
		else: 
			if display: plt.show()

def colorbar_multivertical(im, ax, fig, label, 
		rect=[1.01, 0.0, 0.03, 1], gap=0.03, ticklocation='right'):

	nbar=len(im)
	vsize=(rect[3] - gap*(nbar-1))/nbar
	ii=0
	for key in im:
		cax = ax.inset_axes([rect[0],(vsize+gap)*ii+rect[1],rect[2],vsize]) #, transform=ax.transAxes)
		cb  = fig.colorbar(im[key], pad=0.01, label=label[key], cax=cax, ticklocation=ticklocation)
		cb.ax.tick_params(direction='out')
		cb.ax.tick_params(direction='out', which='minor')
		ii = ii+1

def colorbar_multihorizontal(im, ax, fig, label, 
		rect=[0.0, 1.01, 1.0, 0.05], gap=0.03, ticklocation='top'):

	nbar=len(im)
	hsize=(rect[2] - gap*(nbar-1))/nbar
	ii=0
	for key in im:
		cax = ax.inset_axes([rect[0]+(hsize+gap)*ii,rect[1],hsize,rect[3]]) #, transform=ax.transAxes)
		cb  = fig.colorbar(im[key], pad=0.01, label=label[key], cax=cax, 
				ticklocation=ticklocation, orientation='horizontal')
		cb.ax.tick_params(direction='out')
		cb.ax.tick_params(direction='out', which='minor')
		ii = ii+1

def colorbar_multi(_im, ax, fig, _label, 
		rect=[1.01, 0.0, 0.03, 1], gap=0.03, ticklocation='right', orientation='vertical'):
	if type(_im).__name__ == 'OrderedDict':
		im = _im 
		label = _label
	else:
		im    = OrderedDict(); im[0]    = _im
		label = OrderedDict(); label[0] = _label

	if orientation == 'vertical':
		colorbar_multivertical(im, ax, fig, label, rect=rect, gap=gap, ticklocation=ticklocation)
	else:
		colorbar_multihorizontal(im, ax, fig, label, rect=rect, gap=gap, ticklocation=ticklocation)

def tick_orientation(cbar, ticklocation=None, orientation=None):
	if orientation == None:
		if cbar[2] > cbar[3]: orientation='horizontal'
		else:                 orientation='vertical'
	if ticklocation == None:
		if orientation == 'vertical':
			if cbar[0] > 0.5: ticklocation = 'right'
			else:			ticklocation = 'left'
		else:
			if cbar[1] > 0.5: ticklocation = 'top'
			else:			ticklocation = 'bottom'
	return ticklocation, orientation

def colorbar(im, ax, fig, label,  
		cbar=None, gap=None, ticklocation=None, orientation=None,
		hsize=0.0, xhist=False, yhist=False, loc_ylabel=None, y_title=None):

	if y_title == None: y_title=1.0
	if xhist: 
		yhsize=0.05*hsize
		y_title=1.0+hsize
	else: yhsize=0.0

	if yhist: xhsize=0.05*hsize
	else:	    xhsize=0.0
	rect=[0,0,1.+xhsize, 1.0+yhsize]
	
	if type(cbar) is bool:
		if cbar: 
			if xhist and yhist: 
				cbar = [-0.15, 0.0, 0.03, 0.6 ]
				if gap == None: gap=0.02
				if loc_ylabel == None: loc_ylabel='top'
			elif yhist:		  
				cbar = [0.0, 1.01, 1.00, 0.03]
				if gap == None: gap=0.03
			else:
				colorbar_multi(im, ax, fig, label)
				return rect, loc_ylabel, y_title

	if type(cbar) is list:
		cbar=[float(v) for v in cbar]

		ticklocation, orientation = tick_orientation(cbar, 
							ticklocation=ticklocation, orientation=orientation)

		colorbar_multi(im,ax,fig, label, 
				rect=cbar, gap=gap, 
				ticklocation = ticklocation,
				orientation  = orientation)
	
	return rect, loc_ylabel, y_title

def despine_axes(ax, despine):
	if despine == None: despine = False
	if type(despine) is bool:
		if despine:
			ax.spines['top'].set_visible(False)
			ax.spines['right'].set_visible(False)
	else:
		for each in despine.split(','):
			ax.spines[each].set_visible(False)

#----------------------------------------------------------------------------------------
def hist2line(edges, values):
	edges = np.array(edges)
	values = np.array(values)
	x, y = [edges[0]], [values[0]]
	c = []
	for i in range(1, len(values)):
		x.append(edges[i])
		x.append(edges[i])
		y.append(values[i-1])
		y.append(values[i])
		c.append((edges[i-1]+edges[i])*0.5)
	x.append(edges[-1])
	y.append(values[-1])
	c.append((edges[-2]+edges[-1])*0.5)
	return x, y, c

#----------------------------------------------------------------------------------------
# routines for addition to plots
def annotate(data=None, common_kwargs={}):
	if data == None: return

	for kwargs in data:
		t = kwargs.pop('t')
		x = kwargs.pop('x')
		y = kwargs.pop('y')
		for key in common_kwargs:
			if key not in kwargs:
				kwargs[key] = common_kwargs[key]
		plt.text(x, y, t, **kwargs)

def add_polygon(data=None, common_kwargs={}):
	if data == None: return

	for kwargs in data:
		x = kwargs.pop('x')
		y = kwargs.pop('y')
		for key in common_kwargs:
			if key not in kwargs:
				kwargs[key] = common_kwargs[key]
		plt.plot(x, y, **kwargs)

def add_ellipse(data=None, common_kwargs={}):
	if data == None: return

	import math as m
	N=100
	t = np.arange(0, m.pi*2, m.pi*2/N)
	np.append(t,m.pi*2)
	for kwargs in data:
		x0 = kwargs.pop('x')
		y0 = kwargs.pop('y')
		r = kwargs.pop('r')
		try:
			s = kwargs.pop('s')
		except:
			s = r
		x = [r*m.cos(et) +x0 for et in t]
		y = [s*m.sin(et) +y0 for et in t]

		for key in common_kwargs:
			if key not in kwargs:
				kwargs[key] = common_kwargs[key]
		plt.plot(x, y, **kwargs)

#----------------------------------------------------------------------------------------
# common core plotting routine for plot1d
def plot1d_core(x, y, attr=None, xscale='linear',  
		xlow=None, xhigh=None, ylow=None, yhigh=None, 
		xerr=None, yerr=None, xlerr=None, ylerr=None,
		color=None, label=None, alpha=None, 
		errcolor=None, erralpha=None,
		marker=None, linestyle=None, linewidth=None,
		ax=None, ax2=None, ay2=None, 
		binsize=None, nbin=None, edges=None,
		xr=None, yr=None, 
		smooth=None, savgol=None, 
		datfile=None, overwrite=True, 
		colnames=['x','y'], units=['',''], extname='Plottool',
		altx=False, alty=False, add_ax2=False, add_ay2=False):

	at=ax
	if alty or add_ay2:
		if ay2 == None: 
			ay2 = ax.twinx()
			if alty:
				ay2.yaxis.label.set_color(color)
				ay2.tick_params(axis='y', colors=color)
				ay2.tick_params(axis='y', colors=color, which='minor')
				ay2.spines['right'].set_color(color)
				at=ay2
		
	elif altx or add_ax2:
		if ax2 == None: 
			ax2 = ax.twiny()
			if altx:
				ax2.xaxis.label.set_color(color)
				ax2.tick_params(axis='x', colors=color)
				ax2.tick_params(axis='x', colors=color, which='minor')
				ax2.spines['top'].set_color(color)
				at=ax2

	# if len(x) == len(y) +1:
	attrs = attr.split(',')
	if 'hist' in attrs:
		# we assume this is for histogram
		if type(x).__name__ != 'ndarray': x=np.array(x)
		if type(y).__name__ != 'ndarray': y=np.array(y)
		if len(x) == len(y)+1:
			xh, yh, xc = hist2line(x, y)
			x=xc
		elif len(x) == len(y):
			extend=np.concatenate([x[0]*2-x[1],x,x[-1]*2-x[-2]], axis=None)
			roll =np.roll(extend, 1)
			edges = (extend+roll)/2
			xh, yh, xc = hist2line(edges[1:], y)
		pid, = at.plot(xh, yh,
			color=color, label=label, alpha=alpha,
			marker=None, linestyle=linestyle, linewidth=linewidth)
		pid_, = at.plot(x, y,
			color=color,  alpha=alpha,
			marker=marker, linestyle='none')
		# print('here', len(x), len(y), len(xc), len(xh), len(yh))
		# x, y

	elif 'makehist' in attrs:
		# we assume this is to make a new histogram
		if edges== None:
			if binsize==None:  binsize = (xr[1]-xr[0])/nbin
			else:              nbin = int((xr[1]-xr[0])/binsize)

			edges = get_edges(xr, nbin, scale = xscale)
			# y, *_ = np.histogram(x, bins=edges)

		xh, xedges, _ = at.hist(x, bins=edges, histtype='stepfilled', 
				facecolor=color, label=label,
				# weights=weights,
				alpha=alpha)
		xh, xedges, _ = at.hist(x, bins=edges, histtype='step', 
				# weights=weights,
				edgecolor=color)

		# xh, yh, x = hist2line(edges, y)
		# xedges, xh
		x = xedges[:-1]
		y = xh

		pid = at

	else:
		if type(smooth).__name__ == 'NoneType':
			pid, = at.plot(x, y,
				color=color, label=label, alpha=alpha,
				marker=marker, linestyle=linestyle, linewidth=linewidth, zorder=10)
			if errcolor == None: errcolor=color
			if erralpha == None: erralpha=alpha
			if type(yerr).__name__ != 'NoneType':
				if type(ylerr).__name__ == 'NoneType':
					for ex, ey, err in zip(x,y,yerr):
						pid_, = at.plot([ex,ex], [ey-err,ey+err],
							color=errcolor,  alpha=erralpha,
							marker=None, linestyle='solid', zorder=9)
				else:
					for ex, ey, err, lerr in zip(x,y,yerr,ylerr):
						pid_, = at.plot([ex,ex], [ey+lerr,ey+err],
							color=errcolor,  alpha=erralpha,
							marker=None, linestyle='solid', zorder=9)
			if type(xerr).__name__ != 'NoneType':
				if type(xlerr).__name__ == 'NoneType':
					for ex, ey, err in zip(x,y,xerr):
						pid_, = at.plot([ex-err,ex+err], [ey,ey],
							color=errcolor,  alpha=erralpha,
							marker=None, linestyle='solid', zorder=9)
				else:
					for ex, ey, err, lerr in zip(x,y,xerr, xlerr):
						pid_, = at.plot([ex+lerr,ex+err], [ey,ey],
							color=errcolor,  alpha=erralpha,
							marker=None, linestyle='solid', zorder=9)

			# x, y, [xerr, yerr]

		else: 
			if type(savgol).__name__ == 'NoneType': savgol=[11,2]
			y_sm=y
			finite=np.isfinite(y)
			y_sm[finite]= savgol_filter(y[finite], savgol[0], savgol[1])

			if smooth == 'replace':
				pid, = at.plot(x, y_sm,
					color=color, label=label, alpha=alpha,
					marker=marker, linestyle=linestyle, linewidth=linewidth)
			elif smooth == 'overlay':
				pid, = at.plot(x, y,
					color=color, label=label, alpha=alpha,
					marker=marker, linestyle=linestyle, linewidth=linewidth)
				pid_, = at.plot(x, y_sm,
					color=color, label='savgol smooth', linestyle='solid')
			# x, y, y_sm

	if 'poisson_error' in attrs:
		for exc, ey in zip(x, y):
			err= math.sqrt(ey)
			pid_, = at.plot([exc,exc], [ey-err,ey+err],
				color=color,  alpha=alpha,
				marker=None, linestyle='solid')

	if datfile != None:
		pdt=QTable([x,y], names=colnames, units=units, meta={'extname':extname})
		tt.to_fits(datfile,pdt, overwrite=overwrite)

	return pid, ax2, ay2

#----------------------------------------------------------------------------------------
# common core plotting routine for dplot
def get_bin(binsize, nbin, binr, nbinr, rr):

	if binsize != None:  binr = binsize
	if nbin    != None: nbinr = nbin

	if binr==None:  binr = (rr[1]-rr[0])/nbinr
	else:          nbinr = int((rr[1]-rr[0])/binr)

	return binr, nbinr

def edges_to_data(xedges, yedges, 
			xr=None, binx=None, nbinx=None, 
			yr=None, biny=None, nbiny=None): 

	if type(xedges) is not list:
		xedges_ = [ii*binx+xr[0]+binx*0.5 for ii in range(0,nbinx)]
	else:
		xedges_ = [(v+w)*0.5 for v, w in zip(xedges[:-1:], xedges[1::])]

	xdata   = [[v]  * nbiny for v in xedges_]
	xdata   = np.array(xdata).flatten()
	# xdata   = xedges_ * nbiny

	if type(yedges) is not list:
		yedges_ = [ii*binx+yr[0]+binx*0.5 for ii in range(0,nbiny)]
	else:
		yedges_ = [(v+w)*0.5 for v, w in zip(yedges[:-1:], yedges[1::])]
	ydata   = yedges_ * nbinx

	return xdata, ydata

def get_norm(zlog=None, zmid=None, zmin=None, zmax=None, zr=None, zlthresh=None, zlscale=None):
	if zr != None: 
		zmin =zr[0]
		zmax =zr[1]
	if not zlog:

		if zmid != None:
			norm=colors.CenteredNorm(zmid) #, vmin=zmin, vmax=zmax)
		else:
			norm=colors.Normalize(vmin=zmin, vmax=zmax)

	else:
		# log, with negative

		zclip=True
		if zmin > 0:
			norm=colors.LogNorm(vmin=zmin, vmax=zmax, clip=zclip)
		elif zmin < 0:
			if zlthresh == None: zlthresh=-zmin
			if zlscale  == None: zlscale=-zmin/zmax
			norm=colors.SymLogNorm(vmin=zmin, vmax=zmax, clip=zclip, linthresh=zlthresh, linscale=zlscale)
		else:
			if zlthresh == None: zlthresh=zmax/1.e3
			if zlscale  == None: zlscale=0.2
			norm=colors.SymLogNorm(vmin=zmin, vmax=zmax, clip=zclip, linthresh=zlthresh, linscale=zlscale)
	return norm, zmin, zmax

def project_hist(_mdata, _adata, _image, _weights, _colors, edges, 
		mr=None, ar=None, zlog=False, 
		scale='linear', direction='x', grid=None,
		nbin=100, anbin=100, slice=False, hgap=0.04, hheight=0.15, halpha=0.1, hscale='linear',
		doimage=False, plt=None, ax=None, despine=False):

	if type(_mdata).__name__ == 'OrderedDict':
		mdata   = _mdata
		adata   = _adata
		image   = _image
		weights = _weights
		colors  = _colors
	else:
		mdata   = OrderedDict();  	mdata  [0] = _mdata
		adata   = OrderedDict();  	adata  [0] = _adata
		image   = OrderedDict();  	image  [0] = _image
		weights = OrderedDict();	weights[0] = _weights
		colors  = OrderedDict();	colors [0] = _colors 

	mdata_  =mdata
	weights_=weights

	mh	=OrderedDict()

	if direction == 'x':
		axis=1; orientation='vertical'
		rect=[0,1.+hgap,1,hheight]
		sxr0=mr; sxr1=mr
		align='mid'; orientation='vertical'
		mhax	=ax.inset_axes(rect , transform=ax.transAxes, sharex=ax)
	else:
		axis=0; orientation='horizontal'
		rect=[1.+hgap,0.0,hheight,1]
		syr0=mr; syr1=mr
		align='mid'; orientation='horizontal'
		mhax	=ax.inset_axes(rect , transform=ax.transAxes, sharey=ax)
	
	if type(grid) is bool:
		if grid == True: mhax.grid()

	if slice != None:
		if type(slice) is not list: 
			p2v=pix2val([0,1], vr=ar, pr=[0,nbin])
			p2v=p2v[1]-p2v[0]
			slice=[slice,slice+p2v]

		pix_slice=val2pix(slice, vr=ar, pr=[0,nbin])

		if pix_slice[0] == pix_slice[1]: pix_slice[1]=pix_slice[1]+1

		if direction == 'x':
			syr0=[slice[0],slice[0]]; syr1=[slice[1],slice[1]]
			for key in image:
				mh[key] = image[key][:,pix_slice[0]:pix_slice[1]].sum(axis=axis)
		else:
			sxr0=[slice[0],slice[0]]; sxr1=[slice[1],slice[1]]
			for key in image:
				mh[key] = image[key][pix_slice[0]:pix_slice[1],:].sum(axis=axis)

		ax.plot(sxr0,syr0, linestyle='solid', clip_on=True, color='white', alpha=0.5)
		ax.plot(sxr1,syr1, linestyle='solid', clip_on=True, color='white', alpha=0.5)

		if not doimage:
			for key in adata:
				pick = (adata[key] >= slice[0]) & (adata[key] <= slice[1])
				mdata_  [key] = mdata[key][pick]
				weights_[key] = weights[key][pick]
	else:
		for key in adata:
			mh[key] = image[key].sum(axis=axis)

	for key in mdata_:
		if not doimage:		   
			sel  = mdata_[key]
			wsel = weights_[key]
		else:
			# note it is not tested whether this should be nbin or anbin
			if direction == 'x': sel = mdata_[key][::nbin]
			else:			   sel = mdata_[key][:anbin]
			wsel = mh[key]

		mhax.hist(sel, weights=wsel, bins=edges, histtype='stepfilled', align=align, 
					orientation=orientation, facecolor=colors[key], alpha=halpha)
		mhax.hist(sel, weights=wsel, bins=edges, histtype='step', align=align, 
					orientation=orientation, edgecolor=colors[key])

	if hscale == None:
		if zlog: hscale='log'
		else:    hscale='linear'

	if direction == 'x':
		mhax.set_xlim(mr)
		mhax.set_xscale(scale)
		plt.setp(mhax.get_xticklabels(), visible=False)
		plt.setp(mhax.get_xlabel(),      visible=False)
		mhax.set_yscale(hscale)
	else:
		mhax.set_ylim(mr)
		mhax.set_yscale(scale)
		plt.setp(mhax.get_yticklabels(), visible=False)
		plt.setp(mhax.get_ylabel(),      visible=False)
		mhax.set_xscale(hscale)

	despine_axes(mhax, despine)

#----------------------------------------------------------------------------------------
def prep_data_deco(func):
	"""
	decorator for data loader. Used for 1-d and 2-d data as well as 2-d images
	Some nontrivial parameters:
		 attr:
			 makehist: to make a histogram on the fly
			 hist: data is a histogram
			 poisson_error: add Poisson error

	"""

	def xdexpr(expr, x, y, vars=None):
		if vars != None:
			for key, val in vars.items():
				locals()[key] = val
		if expr !=None: return eval(expr)
		else: return x

	def ydexpr(expr, x, y, vars=None):
		if vars != None:
			for key, val in vars.items():
				locals()[key] = val
		if expr !=None: return eval(expr)
		else: return y

	def zdexpr(expr, x, y, vars=None):
		if vars != None:
			for key, val in vars.items():
				locals()[key] = val
		if expr !=None: return eval(expr)
		else: return None

	def errexpr(expr, err, x, y, vars=None):
		if vars != None:
			for key, val in vars.items():
				locals()[key] = val
		if expr !=None: 
			ans=eval(expr)
			return ans.copy()
		else: return err

	@wraps(func)
	def prep_data(*args, xdata=None, ydata=None, zdata=None, weights=None,
			xexpr=None, yexpr=None, zexpr=None, 
			xerr=None, yerr=None, xerrexpr=None, yerrexpr=None, 
			xlerr=None, ylerr=None, xlerrexpr=None, ylerrexpr=None, 
			xerrdata=None, yerrdata=None, xlerrdata=None, ylerrdata=None, 
			xhighdata=None, xlowdata=None, xhigh=None, xlow=None,
			yhighdata=None, ylowdata=None, yhigh=None, ylow=None,
			data=None, image=None, infile=None, x="", y="", 
			xlabel=None, ylabel=None, xr=None, yr=None, 
			infile2=None, attr='', pars=None, nbin=100, binsize=None,
			xmin=None, xmax=None, ymin=None, ymax=None,
			margin=0.0, drawdown=None, filter=False, 
			xscale=None, yscale=None, xlog=False, ylog=False, 
			rcParams=None, clip=None,  # pixel coordinates
			verbose: int=0, ftype=None, hdu=None, help=None, **kwargs):

		help_text(help)

		loaded = None

		# try loading an image
		if type(image) is bool:
			if image:
				# read image
				# assume fits image for now
				hdul=fits.open(infile)
				if hdu == None: hdu=0
#				image=np.transpose(hdul[hdu].data)
				image=hdul[hdu].data
				loaded='image'
		elif type(image).__name__ != "NoneType":
			loaded='image'

		# make sure 2-d image and clip if requested
		if loaded == "image":
			ndim = image.ndim
			if ndim == 3: 
				image = image.sum(axis=0)
			image=np.transpose(image)
			#print(image.shape)

			if type(clip) is list:
				# x and y seem to be swapped
				#image=image[clip[2]:clip[3],clip[0]:clip[1]]
				image=image[clip[0]:clip[1],clip[2]:clip[3]]

			nbinx, nbiny=image.shape
			#print(nbinx,nbiny)
			if type(clip) is not list:
				if xr == None: xr=[0,nbinx]
				if yr == None: yr=[0,nbiny]
			else:
				if xr == None: xr=[clip[0],clip[1]]
				if yr == None: yr=[clip[2],clip[3]]

		# if there is no image then try loading a table
		if type(xdata).__name__ == "NoneType" and loaded == None:
			if hdu == None: hdu=1
			if infile2 == None:
				data, x, y, xlabel, ylabel = read(infile, x=x, y=y, data=data, 
						xlabel=xlabel, ylabel=ylabel, ftype=ftype, hdu=hdu, attr=attr)
				if type(data).__name__ == "NoneType": return False
				data2=data
			else:
				data, x, y_, xlabel, ylabel_ = read(infile, x=x, y=None, data=data, 
						xlabel=xlabel, ylabel=None, ftype=ftype, hdu=hdu, attr=attr)
				data2, x_, y, xlabel_, ylabel = read(infile2, x=None, y=y, 
					xlabel=None, ylabel=ylabel, ftype=ftype, hdu=hdu, attr=attr)
			ydata=data2[y]

			if xerr  != None: xerrdata  = data [xerr ]
			if yerr  != None: yerrdata  = data2[yerr ]
			if xlow  != None: xlowdata  = data [xlow ]
			if xhigh != None: xhighdata = data [xhigh]
			if ylow  != None: ylowdata  = data2[ylow ]
			if yhigh != None: yhighdata = data2[yhigh]
			if xlerr != None: xlerrdata = data [xlerr]
			if ylerr != None: ylerrdata = data2[ylerr]

			if   x == '_auto_' : xdata=np.arange(0, len(ydata))
			elif x == '_range_': xdata=(xlowdata+xhighdata)*0.5
			elif x == '_range_log_': xdata=np.exp((np.log(xlowdata)+np.log(xhighdata))*0.5)
			else: xdata=data[x]

			if type(xdata[0]) is str: xdata = get_number(xdata)
			if type(ydata[0]) is str: ydata = get_number(ydata)

			loaded='table'

		if xscale == None: 
			xscale = 'log' if xlog else 'linear'
		if yscale == None: 
			yscale = 'log' if ylog else 'linear'

		# change xdata and ydata by expr
		if type(pars).__name__ != 'NoneType': 
			vars=read_pars(pars, data=data)
		else: vars=None
		

		xdata_     = xdexpr (xexpr    ,		 xdata, ydata, vars=vars)
		ydata_     = ydexpr (yexpr    ,		 xdata, ydata, vars=vars)
		xerrdata_  = errexpr(xerrexpr , xerrdata,  xdata, ydata, vars=vars)
		yerrdata_  = errexpr(yerrexpr , yerrdata,  xdata, ydata, vars=vars)
		xlerrdata_ = errexpr(xlerrexpr, xlerrdata, xdata, ydata, vars=vars)
		ylerrdata_ = errexpr(ylerrexpr, ylerrdata, xdata, ydata, vars=vars)
		zdata_     = zdexpr (zexpr    ,		 xdata, ydata, vars=vars)

		xdata     = xdata_     
		ydata     = ydata_     
		xerrdata  = xerrdata_  
		yerrdata  = yerrdata_  
		xlerrdata = xlerrdata_ 
		ylerrdata = ylerrdata_ 
		zdata     = zdata_     

		xr, yr, edges =  set_range_2D(xdata, ydata, xr=xr, yr=yr, 
				xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax,
				margin=margin, drawdown=drawdown, 
				attr=attr, nbin=nbin, binsize=binsize,
				xlowdata=xlowdata, xhighdata=xhighdata, xerrdata=xerrdata,
				ylowdata=ylowdata, yhighdata=yhighdata, yerrdata=yerrdata,
				xscale=xscale, yscale=yscale)

		if filter:
#			if loaded == 'table':
			if type(xdata).__name__ != 'NoneType':
				xdata, ydata, weights = filter_by_range(xdata, ydata, xr, yr, weights=weights)
				# need to clip the image

		set_rcParams(rcParams, verbose=verbose, name=func.__name__)

		if type(image    ).__name__ != 'NoneType': kwargs['image'      ] = image
		if type(ftype    ).__name__ != 'NoneType': kwargs['ftype'      ] = ftype
		if type(xerrdata ).__name__ != 'NoneType': kwargs['xerrdata'   ] = xerrdata
		if type(yerrdata ).__name__ != 'NoneType': kwargs['yerrdata'   ] = yerrdata
		if type(xlerrdata).__name__ != 'NoneType': kwargs['xlerrdata'  ] = xlerrdata
		if type(ylerrdata).__name__ != 'NoneType': kwargs['ylerrdata'  ] = ylerrdata
		if type(xlowdata ).__name__ != 'NoneType': kwargs['xlowdata'   ] = xlowdata
		if type(ylowdata ).__name__ != 'NoneType': kwargs['ylowdata'   ] = ylowdata
		if type(xhighdata).__name__ != 'NoneType': kwargs['xhighdata'  ] = xhighdata
		if type(yhighdata).__name__ != 'NoneType': kwargs['yhighdata'  ] = yhighdata

		# if type(infile   ).__name__ != 'NoneType': kwargs['infile'     ] = infile
		# if type(hdu      ).__name__ != 'NoneType': kwargs['hdu'        ] = hdu
		if type(weights  ).__name__ != 'NoneType': kwargs['weights'    ] = weights
		# if type(data     ).__name__ != 'NoneType': kwargs['data'       ] = data

		return func(*args, xdata=xdata, ydata=ydata, 
			# weights=weights, drawdown=drawdown, data=data, 
			# image=image, 
			xlabel=xlabel, ylabel=ylabel, xr=xr, yr=yr, 
			xscale=xscale, yscale=yscale, 
			margin=margin, edges=edges,
			nbin=nbin, binsize=binsize,
			verbose=verbose, help=None, attr=attr, **kwargs)

	return prep_data

# two part reading
# combined model matching the regular data point to set up residual
# combined model and its components with high x-axis scaling
# the latter could be in a different HDU, while the former can be in the same HDU as the data
def prep_model_deco(func):

	def mdexpr(expr, m, x, y):
		if expr !=None: return eval(expr)
		else: return m

	def rdexpr(expr,  r, m, x, y):
		if expr !=None: return eval(expr)
		else: return r

	@wraps(func)
	def prep_data(*args, x=None, m=None, r=None,
			infile=None, ftype=None, hdu=None, 
			xdata=None, ydata=None, mdata=None, 
			rexpr=None, mexpr=None,
			rlabel=None, rr=None, rscale='linear',
			mlabel=None,
			xlabel=None, ylabel=None, xr=None, yr=None, 
			xscale=None, yscale=None, 
			margin=None, drawdown=None,
			rmin=None, rmax=None, 
			rmargin=0.0, data=None,
			xerrdata=None, yerrdata=None, 
			xlowdata=None, xhighdata=None,
			ylowdata=None, yhighdata=None,
			verbose: int=0, attr='',
			mhdu=None, phdu=None,
			help=None, **kwargs):

		help_text(help)

		loaded = None

		# if there is no image then try loading a table
		if type(mdata).__name__ == "NoneType" and loaded == None:
			if hdu == None: hdu=1
			data_, m_, r_, mlabel, rlabel = read(infile, x=m, y=r, data=data, 
					xlabel=None, ylabel=rlabel, ftype=ftype, hdu=hdu, attr=attr)
			if type(data).__name__ == "NoneType": return False

			if m != None: mdata=data[m]
			else:         mdata=None
			if r != None: rdata=data[r]
			else:         rdata=None

			loaded='table'

		# change xdata and ydata by expr
		mdata = mdexpr(mexpr, mdata, xdata, ydata)
		rdata = rdexpr(rexpr, rdata, mdata, xdata, ydata)

		rr =  set_range(rdata, dr=rr, 
				dmin=rmin, dmax=rmax,
				margin=rmargin, drawdown=None,
				scale=rscale)

		# if mhdu is present replace mdata
		if type(mhdu).__name__ != 'NoneType':
			toUnpack = read(infile, ftype=ftype, hdu=mhdu)
			mdata = toUnpack[0]

		# if phdu is present read parameter data
		if type(phdu).__name__ != 'NoneType':
			toUnpack = read(infile, ftype=ftype, hdu=phdu)
			pdata = toUnpack[0]
		else:
			pdata=None

		return func(*args, xdata=xdata, ydata=ydata, 
			mdata=mdata, rdata=rdata, pdata=pdata,
			xlabel=xlabel, ylabel=ylabel, xr=xr, yr=yr, 
			xscale=xscale, yscale=yscale, 
			margin=margin, drawdown=drawdown,
			data=data, rlabel=rlabel, rr=rr, mlabel=mlabel,
			xerrdata=xerrdata, yerrdata=yerrdata, 
			xlowdata=xlowdata, xhighdata=xhighdata,
			ylowdata=ylowdata, yhighdata=yhighdata,
			rmargin=rmargin, attr=attr,
			verbose=verbose, help=None, **kwargs)

	return prep_data
#----------------------------------------------------------------------------------------
# 1-D plots from a single data set
@prep_data_deco
def plot1d(xdata=None, ydata=None, data=None, 
		xlowdata=None, xhighdata=None, ylowdata=None, yhighdata=None, xerrdata=None, yerrdata=None,
		xr=None, yr=None, xlabel=None, ylabel=None,  
		xr2=None, yr2=None, xlabel2=None, ylabel2=None,  
		outfile=None, attr='', alpha=None,
		xscale='linear', yscale='linear',
		nbin=100, binsize=None, edges=None, weights=None, margin=None,  # for making a new histogram
		marker='.', linestyle='None', color=None, linewidth=None, errcolor=None,
		display=True, savgol=None, ion=False, grid=None,
		text=None, text_kw=None, title=None,
		polygon=None, polygon_kw=None,
		ellipse=None, ellipse_kw=None,
		help=None, hold=False, verbose: int= 0, **kwargs):
	"""Plot 1-D from input table
	"""

	def show(ion=True):
		if ion: plt.ion()

		nonlocal xdata, ydata, marker
		nonlocal binsize, nbin, edges, weights, yr, margin

		plt.close('all')
		fig, ax = plt.subplots()

		pid, ax2, ay2 = plot1d_core(xdata, ydata, attr=attr, xscale=xscale,  
			xlow=xlowdata, xhigh=xhighdata, ylow=ylowdata, yhigh=yhighdata, xerr=xerrdata, yerr=yerrdata,
			color=color, label=None, alpha=alpha, errcolor=errcolor,
			marker=marker, linestyle=linestyle, linewidth=linewidth,
			ax=ax, ax2=None, ay2=None, 
			binsize=binsize, nbin=nbin, edges=edges,
			xr=xr, yr=yr, savgol=savgol,
			altx=False, alty=False, 
			add_ax2=type(xr2).__name__ != 'NoneType',
			add_ay2=type(yr2).__name__ != 'NoneType')

		wrap(plt, xr, yr, xlabel, ylabel, 
				xscale=xscale, yscale=yscale, outfile=outfile, 
				ax=ax, grid=grid,
				text=text, text_kw=text_kw,
				polygon=polygon, polygon_kw=polygon_kw,
				ellipse=ellipse, ellipse_kw=ellipse_kw,
				display=display, ion=ion)

	show(ion=ion)
	if hold: embed()

	return plt

# 2-D plots from a single data set
@prep_data_deco
def dplot(xdata=None, ydata=None, image=None, data=None,
		xr=None, yr=None, zr=None,
		zmin=None, zmax=None, zoff=None, zmid=None,
		zlthresh=None, zlscale=None,
		outfile=None, 
		xscale='linear', yscale='linear', xedges=None, yedges=None,
		xlabel=None, ylabel=None, title=None, loc_ylabel=None, y_title=None,
		xr2=None, yr2=None, xlabel2=None, ylabel2=None, zlabel=None,
		binx=None, biny=None, nbinx=100, nbiny=100, nbin=None, binsize=None,
		zlog=False, cmap='Blues', aspect='auto',
		interpolation=None, display=True, weights=None,
		cbar=True, cb_orientation=None, cb_ticklocation=None, cb_outside=False,
		cb_off=None, cb_width=None, cb_length=None, 
		cb_gap=0.03,
		zclip=False,
		xhist=False, xh_height=0.15, xh_scale=None, 
		yhist=False, yh_height=0.15, yh_scale=None, 
		xslice=None, yslice=None, # data coordinateslike xr or yr (not necessarily pixels)
		halpha=0.3, hcolor="darkblue", hgap=0.04, hheight: float=0.15,
		despine=None, margin=0.0, drawdown=None,
		noplot=False, grid=None,
		text=None, text_kw=None,
		polygon=None, polygon_kw=None,
		ellipse=None, ellipse_kw=None,
		help=None, hold=False, verbose:int= 0, **kwargs):
	""" 2-d density plot 
	"""

	if type(image).__name__ == 'NoneType':
		# data points
		binx, nbinx = get_bin(binsize, nbin, binx, nbinx, xr)
		biny, nbiny = get_bin(binsize, nbin, biny, nbiny, yr)
		doimage=False
	else:
		# image input
		if zmax == None: zmax = np.max(image)
		if zmin == None: zmin = np.min(image)

		nbinx, nbiny = image.shape
		binx = (xr[1]-xr[0])/nbinx
		biny = (yr[1]-yr[0])/nbiny
		doimage=True

	if type(xedges).__name__ == 'NoneType':
		xedges = get_edges(xr, nbinx, scale = xscale)

	if type(yedges).__name__ == 'NoneType':
		yedges = get_edges(yr, nbiny, scale = yscale)

	bins = [xedges, yedges]

	if not doimage:
		# to get zmax
		heatmap, *_ = np.histogram2d(xdata, ydata, bins=bins, weights=weights)
		image=heatmap.T

		weights = np.ones(len(xdata))
	else:
		xdata, ydata = edges_to_data(xedges, yedges, 
					xr=xr, binx=binx, nbinx=nbinx, 
					yr=yr, biny=biny, nbiny=nbiny)

		weights = image.flatten()

	if noplot: return image, xedges, yedges
	if zmax == None: zmax=np.max(image)
	if zmin == None: zmin=np.min(image)

	def show(ion=True):

		nonlocal zmin,zmax, zoff
		nonlocal zmid
		nonlocal zlthresh, zlscale
		nonlocal zclip
		nonlocal xr, yr
		nonlocal loc_ylabel, y_title
		plt.close('all')
		fig, ax = plt.subplots()

		if ion: plt.ion()
		norm, zmin, zmax = get_norm(zlog=zlog, zmid=zmid, zmin=zmin, zmax=zmax, 
					zr=zr, zlthresh=zlthresh, zlscale=zlscale)

		image, xedges, yedges, im = ax.hist2d(xdata, ydata, weights=weights,
									norm=norm, bins=bins,  cmap=cmap)
		ax.set_aspect(aspect)
		# if grid != None:
		# 	if grid:
		# 		# why is this working with only xgrid?
		# 		xgrid=ax.get_xgridlines()
		# 		for each in xgrid: ax.plot(each.get_xdata(),each.get_ydata())

		if noplot: return image

		nonlocal cbar, despine, cb_outside, margin, xslice, yslice

		if xhist or yhist:
			if despine == None: despine=True
		despine_axes(ax, despine)

		if xhist:
			nonlocal xh_height, xh_scale
			project_hist(xdata, ydata, image, weights, hcolor, xedges,
					direction='x',
					mr=xr, ar=yr, zlog=zlog, grid=grid,
					scale=xscale, nbin=nbiny, anbin=nbinx, slice=yslice,
					hscale=xh_scale, hgap=hgap, hheight=hheight, halpha=halpha, 
					doimage=doimage, plt=plt, ax=ax, despine=despine)

		if yhist:
			nonlocal yh_height, yh_scale
			project_hist(ydata, xdata, image, weights, hcolor, yedges,
					direction='y',
					mr=yr, ar=xr, zlog=zlog, grid=grid,
					scale=yscale, nbin=nbinx, anbin=nbiny, slice=xslice,
					hscale=yh_scale, hgap=hgap, hheight=hheight, halpha=halpha, 
					doimage=doimage, plt=plt, ax=ax, despine=despine)

		rect, loc_ylabel, y_title = colorbar(im, ax, fig, zlabel,  cbar=cbar, gap=cb_gap, 
					ticklocation=cb_ticklocation, orientation=cb_orientation,
					hsize=hheight+hgap, xhist=xhist, yhist=yhist, 
					loc_ylabel=loc_ylabel, y_title=y_title)

		wrap(plt, xr, yr, xlabel, ylabel, title=title, label=not cb_outside,
				rect=rect, y_title=y_title,
				xscale=xscale, yscale=yscale, loc_ylabel=loc_ylabel,
				outfile=outfile, 
				ax=ax, grid=grid,
				text=text, text_kw=text_kw,
				polygon=polygon, polygon_kw=polygon_kw,
				ellipse=ellipse, ellipse_kw=ellipse_kw,
				ion=ion, display=display)
		return image

	image = show(ion=False)
	if hold: embed()

	return image, xedges, yedges

#----------------------------------------------------------------------------------------
def hp2mollview(infile=None, hdu=1, outfile=None, xsize=800, title="",
		nest=False, min=None, max=None, cmap=None, gridcolor="white",
		hold=False, display=False, ion=False, **kwargs):
	map = hp.read_map(infile, hdu=hdu)
	print("title",title)
	hp.mollview(map, xsize=xsize, title=title, nest=nest, cmap=cmap, 
			min=min, max=max, **kwargs)
	hp.graticule(color=gridcolor)
	wrap(plt, outfile=outfile,  title=title,
		display=display, ion=ion, tight=False)
	if hold: embed()

#----------------------------------------------------------------------------------------
# multiple data set into a plot
class plottool:
	
	key = 0
	maxkey = 0

	# data set: one for each
	xdata,     ydata     = OrderedDict(), OrderedDict()
	rexpr		         = OrderedDict()
	xr,        yr	   = OrderedDict(), OrderedDict()
	label,     marker    = OrderedDict(), OrderedDict()
	linestyle, linewidth = OrderedDict(), OrderedDict()
	alpha,     color     = OrderedDict(), OrderedDict()
	erralpha,  errcolor  = OrderedDict(), OrderedDict()
	altx,      alty	   = OrderedDict(), OrderedDict()
	attr			   = OrderedDict()
	image			   = OrderedDict()
	cmap			   = OrderedDict()
	savgol		   = OrderedDict()
	smooth		   = OrderedDict() 
	xlowdata, xhighdata  = OrderedDict(), OrderedDict()
	ylowdata, yhighdata  = OrderedDict(), OrderedDict()
	xerrdata, yerrdata   = OrderedDict(), OrderedDict()
	xlerrdata, ylerrdata = OrderedDict(), OrderedDict()

	# common options
	xlabel  = ylabel  = None
	xscale  = yscale  = 'linear'
	title   = outfile = None
	display = ion     = hold     = False
	verbose = 1
	datfile = None
	xcol    = 'x'
	ycol    = 'y'
	xunit   = yunit   = ''
	xlabel2 = ylabel2 = ''
	xr2     = yr2	= None
	bbox_to_anchor    = None
	grid    = None

	binsize = None
	nbin	  = 100
	edges	  = None

	# for 2-D map
	doimage = False
	binx    = biny   = None
	nbinx   = nbiny  = None
	zmax    = zmin   = None
	xedges  = yedges = None
	zr      = None
	zlog    = None
	zoff    = None
	zmid    = None
	zlthresh= None
	zlscale = None
	zlclip  = None
	aspect  = 'auto'

	xhist   = yhist   = False
	despine = None

	# colormap for 2-d map
	cb_outside = False
	margin  = 0.00
	cbar	  = False
	cb_orientation =None
	cb_ticklocation=None
	cb_outside=False
	cb_gap=0.03

	cb_off=None
	cb_width=None
	cb_length=None
	zclip=False

	# projection histogram related
	xhist     = yhist     = False 
	xh_height = yh_height = 0.15
	xh_scale  = yh_scale  = None 
	xslice    = yslice    = None

	halpha    = 0.1
	hgap      = 0.04
	hheight   = 0.15
	hcolor    = "darkblue"
	noplot    = False

	loc_ylabel=None
	y_title   =None

	# annotation: text, ellipse, polygon
	text         = None
	text_kw      = {}
	ellipse      = None
	ellipse_kw   = {}
	polygon      = None
	polygon_kw   = {}

	invert	 = False # for mdplot_rgb

	# alternative axes
	add_ax2	 = False
	add_ay2	 = False
	dolegend	 = True

	# 1-dplot with reference data set
	refkey	= 0 # for reference data
	refer		= False
	refset	= False

	# data save
	colnames	= ['x','y']
	units		= ['','']

	# RGB 
	dorgb		= False

	def __init__(self, **kwpars):
		self.set_kwpars(kwpars)
		self.xdata = OrderedDict()
		self.ydata = OrderedDict()

	def set_kwpars(self, kwargs):

		ignored=[]
		for key, val in kwargs.items(): 
			if hasattr(self, key): setattr(self, key, val)
			else:			     ignored.append(key)
		if len(ignored) >0:
			print(cc.err,'Followings are not defined, so ignored, so double check:'+cc.reset)
			print(cc.err,ignored,cc.reset)

		return 1

	def wrap(self, plt, ax, **kwpars):
		wrap(plt, xlabel=self.xlabel, ylabel=self.ylabel, title=self.title, 
				xscale=self.xscale, yscale=self.yscale, outfile=self.outfile, 
				ax=ax, grid=self.grid,
				xlabel2=self.xlabel2, ylabel2=self.ylabel2, xr2=self.xr2, yr2=self.yr2,
				loc_ylabel=self.loc_ylabel, y_title=self.y_title,
				text=self.text, text_kw=self.text_kw,
				polygon=self.polygon, polygon_kw=self.polygon_kw,
				ellipse=self.ellipse, ellipse_kw=self.ellipse_kw,
				ion=self.ion, display=self.display, **kwpars)

	def set_default_range(self):

		pcolor = ["black","red","green","blue","purple","magenta","brown","orange","cyan"]
		icolor = 0
		lcolor = len(pcolor)

		pcmap = ["Blues","Reds","Greens","Greys","Purples","Oranges"]
		icmap = 0
		lcmap = len(pcmap)
		
		for key in self.xdata:
			if 'xrf' not in locals(): xrf=self.xr[key]
			if 'yrf' not in locals(): yrf=self.yr[key]

			if xrf[0] > self.xr[key][0]: xrf[0] = self.xr[key][0]
			if xrf[1] < self.xr[key][1]: xrf[1] = self.xr[key][1]
			if yrf[0] > self.yr[key][0]: yrf[0] = self.yr[key][0]
			if yrf[1] < self.yr[key][1]: yrf[1] = self.yr[key][1]

			if self.color[key] == None:
				self.color[key] = pcolor[icolor]
				icolor = (icolor+1) % lcolor

			if self.alpha[key] == None:
				self.alpha[key] = 1.0 #/self.key

			if self.cmap[key] == None:
				self.cmap[key] = pcmap[icmap]
				icmap = (icmap+1) % lcmap

		if self.verbose >1: print("range:",xrf, yrf)
		return xrf, yrf

	@prep_data_deco
	def collect_data(self, xdata=None, ydata=None, key=None,
			xlowdata=None, xhighdata=None, ylowdata=None, yhighdata=None, 
			xerrdata=None, yerrdata=None, xlerrdata=None, ylerrdata=None,
			image=None, cmap=None,
			xr=None, yr=None, label=None, 
			marker='.', linestyle='None', linewidth=1.5,
			color=None, alpha=None, errcolor=None, erralpha=None, 
			altx=False, alty=False, rexpr=None, attr='',
			savgol=None, smooth=None,
#			rcParams=None,
			help=None, hold=False, verbose: int= 0, **kwargs):
		"""
		collect multiple data set for plot
			 -parameters are divided into two groups: one for each data
				set, and the other for common use
			 -relies on the decorator for data load: see
				'(cjpy.)plottool.prep_data_deco' 

			 Some nontrivial parameters:
				 altx, alty: 2ndary axes data 
				 rexpr: not used?
				 attr:
					 makehist: to make a histogram on the fly
					 hist: data is a histogram
					 poisson_error: add Poisson error
		"""

		if key == None: key = self.key

		self.xdata		[key] = xdata
		self.ydata		[key] = ydata
		self.xr		[key] = xr
		self.yr		[key] = yr
		self.marker		[key] = marker
		self.linestyle	[key] = linestyle
		self.linewidth	[key] = linewidth
		self.color		[key] = color
		self.alpha		[key] = alpha
		self.altx		[key] = altx
		self.alty		[key] = alty
		self.rexpr		[key] = rexpr
		self.attr		[key] = attr
		self.image		[key] = image
		self.cmap		[key] = cmap
		self.savgol		[key] = savgol
		self.smooth		[key] = smooth
		self.xlowdata	[key] = xlowdata
		self.ylowdata	[key] = ylowdata
		self.xhighdata	[key] = xhighdata
		self.yhighdata	[key] = yhighdata
		self.xerrdata	[key] = xerrdata
		self.yerrdata	[key] = yerrdata
		self.xlerrdata	[key] = xlerrdata
		self.ylerrdata	[key] = ylerrdata

		if errcolor == None: errcolor=color
		if erralpha == None: erralpha=alpha
		self.errcolor	[key] = errcolor
		self.erralpha	[key] = erralpha

		if label == None: self.label[key] = str(key)
		else:			self.label[key] = label
	
		# in order to set options any time
		# in this way one time options can be set in the -main options
		# but it becomes redundantly repeated when collect_data is
		# repeatedly called as -main
		# should go either class initialization or 
		# the -post routine, but that would make the -option setting a bit deeper
		self.set_kwpars(kwargs)
		if len(self.xdata.keys()) == 1:
			self.verbose = kwargs.get('verbose', verbose)
#			set_rcParams(rcParams, verbose=verbose)
		#print(self.verbose)

		if self.refer: 
			self.refkey=key
			self.refer = False

		# self.key = key + 1
		self.maxkey = self.maxkey + 1
		self.key = self.maxkey

		if self.verbose > 2:
			print(xdata)
			print(ydata)
		return 1

	def composite_data(self, key=None, inkeys=None, 
			  xexpr=None, yexpr=None, 
			  varx= None, vary=None, defkey=None, **kwpars):
		if type(inkeys).__name__ == None: return
		if key == None: 
			self.maxkey = self.maxkey+1
			key = self.maxkey

		nkeys_= len(inkeys)

		if type(varx).__name__ == 'NoneType': 
			varx=[]
			for idx_, each_ in enumerate(inkeys):
				varx.append('x'+str(idx_))

		if type(vary).__name__ == 'NoneType': 
			vary=[]
			for idx_, each_ in enumerate(inkeys):
				vary.append('y'+str(idx_))

		for idx_, each_ in enumerate(inkeys):
			if each_ not in self.xdata:
				print(cc.err+'No data found for',each_,cc.reset)
				return

			locals()[varx[idx_]] = self.xdata[each_]
			locals()[vary[idx_]] = self.ydata[each_]

		xdata = eval(xexpr)
		ydata = eval(yexpr)


		self.collect_data(xdata=xdata, ydata=ydata, key=key)
		self.set_prop(key, **kwpars)

	def set_prop(self, key, **kwpars):
		for k, v in kwpars.items():
			x = getattr(self, k)
			x[key] = v
			setattr(self, k, x)

	def scan_fitsfile_moot(self, infile=None, hdu="", x=None):
		if infile == None:
			return None
		hdul=fits.open(infile)
		tasks=OrderedDict()
		loops=[]
		for each in hdul:
			if hdu !="":
				if hdu != each.name: continue
			if not hasattr(each, 'columns'): continue
			for subeach in each.columns:
				new=False
				if bool(re.search('A',str(subeach.format))):
					continue
				if x != None:
					if x != subeach.name: 
						if hdu !="":
							loopid = subeach.name
						else:
							loopid = each.name + ' '+ subeach.name
						new=True
				else:
					x = subeach.name
				if new:
					loops.append(loopid)
					task=OrderedDict()
					task['infile']	=infile
					task['hdu']		=each.name
					task['x']		=x
					task['y']		=subeach.name
					task['label']	=loopid

					tasks['-loop=='+loopid] = task

		tasks['-loop'] = loops
		return tasks

	def scan_fits_cols(self, infile=None, hdu="", x=None):
		if infile == None:
			return None
		hdul=fits.open(infile)
		tasks=OrderedDict()
		for each in hdul:
			if hdu !="":
				if hdu != each.name: continue
			if not hasattr(each, 'columns'): continue
			for subeach in each.columns:
				new=False
				if bool(re.search('A',str(subeach.format))):
					continue
				if x != None:
					if x != subeach.name: 
						if hdu !="":
							loopid = subeach.name
						else:
							loopid = each.name + ' '+ subeach.name
						new=True
				else:
					x = subeach.name
				if new:
					task=OrderedDict()
					task['infile']	=infile
					task['hdu']		=each.name
					task['x']		=x
					task['y']		=subeach.name
					task['label']	=loopid

					tasks[loopid] = task
		return tasks

	def scan_fits_hdus(self, infile=None, x=None, y=None, hdu="", verbose=0, tolist=False, seed=None):
		if infile == None:
			return None

		infile=str(Path(infile).expanduser())
		hdul=fits.open(infile)
		tasks=OrderedDict()
		for each in hdul:

			if not hasattr(each, 'columns'): continue

			if hdu != "":
				if not bool(re.search(hdu,each.name)): continue
			if int(verbose)>0: print(each.name)

			ind=[]
			for idx, subeach in enumerate(each.columns):
				if bool(re.search('A',str(subeach.format))): continue
				ind.append(idx)
			if x == None or x == "": x=each.columns[ind[0]].name
			if y == None or y == "": y=each.columns[ind[1]].name

			x_bingo = False
			y_bingo = False
			for subeach in each.columns:
				if x == subeach.name: x_bingo=True
				if y == subeach.name: y_bingo=True

			if not x_bingo*y_bingo: continue

			task=OrderedDict()
			task['infile']	=infile
			task['hdu']		=each.name
			task['x']		=x
			task['y']		=y
			task['label']	=each.name

			if type(seed).__name__ != 'NoneType':
				for key in seed:
					if key not in task: task[key] =seed[key] 

			tasks[each.name] = task

		if tolist:
			idx=1
			for key, val in tasks.items(): 
				val['-id'] = f"{idx:02}:" + key
				idx=idx+1

			tasks=list(tasks.values())

		return tasks

	def mplot1d(self, xr=None, yr=None, keys=None, rcParams=None, lncols=1, **kwpars):
		"""Multiple Plot 1-D from input table
		"""

		if len(self.rexpr) == list(self.rexpr.values()).count(None):
			xrf, yrf=self.set_default_range()
			xref = yref = None
		else:
			if not self.refset:
				xref = self.xdata.pop(self.refkey)
				yref = self.ydata.pop(self.refkey)
				self.xref=xref
				self.yref=yref
				self.refset=True
			else:
				xref=self.xref
				yref=self.yref

			xrf  = self.xr[self.refkey]
			yrf  = self.yr[self.refkey]
			_, _ = self.set_default_range()

		self.set_kwpars(kwpars)
		if xr != None: xrf=xr
		if yr != None: yrf=yr

		def show(ion=True):
			if self.ion: plt.ion()

			plt.close('all')
			fig, ax = plt.subplots()
			ax2     = None
			ay2     = None

			nonlocal xrf, yrf
			nonlocal xref, yref
			nonlocal keys

			if self.datfile != None: pdt=OrderedDict()

			pids=[]
			overwrite=True
			if type(keys).__name__ == 'NoneType':
				keys = self.xdata.keys()
			for key in keys:

				if key not in self.xdata:
					print(cc.err+'No data found for',key,cc.reset)
					continue

				x=self.xdata[key]
				y=self.ydata[key]

				if self.rexpr[key] != None: x, y=eval(self.rexpr[key])

				pid, ax2, ay2 = plot1d_core(x, y, attr=self.attr[key], 
					xlow=self.xlowdata[key], xhigh=self.xhighdata[key], 
					ylow=self.ylowdata[key], yhigh=self.yhighdata[key], 
					xerr=self.xerrdata[key], yerr=self.yerrdata[key],
					xlerr=self.xlerrdata[key], ylerr=self.ylerrdata[key],
					xscale=self.xscale,  marker=self.marker[key], 
					label=self.label[key], 
					color=self.color[key], alpha=self.alpha[key],
					errcolor=self.errcolor[key], erralpha=self.erralpha[key],
					linestyle=self.linestyle[key], linewidth=self.linewidth[key],
					ax=ax, ax2=ax2, ay2=ay2, binsize=self.binsize, nbin=self.nbin,
					xr=xrf, yr=yrf, 
					smooth=self.smooth[key], savgol=self.savgol[key],
					altx=self.altx[key], alty=self.alty[key], 
					add_ax2=self.add_ax2, add_ay2=self.add_ay2,
					datfile=self.datfile, overwrite=overwrite,
					colnames=self.colnames, units=self.units, extname=self.label[key])

				overwrite=False

				if self.label[key] != "": pids.append(pid)
				
			if self.noplot: return ax, ax2, ay2
			if self.dolegend:
				plt.legend(labelcolor='linecolor', 
						bbox_to_anchor=self.bbox_to_anchor,
						ncol=lncols, handles=pids)

			if self.verbose >1: print('outfile',self.outfile)

			self.wrap(plt, ax, xr=xrf, yr=yrf, ax2=ax2, ay2=ay2, rcParams=rcParams)
			return ax, ax2, ay2

		ax, ax2, ay2 = show(ion=False)
		if self.hold: embed()

		return ax, ax2, ay2

	def mdplot(self, xr=None, yr=None, **kwpars):
		""" 
		2-d density plot for multiple data set
			- use this with plottool.plottool.collect_data for data load
			- best used with white color for low values (or low density)
			  the color map is auto alpha corrected for low values
				- alpha: sets the minimum transparency for each image
				- halpha: sets transparency for x and y histograms
			- in principle, there is no limit for the number of data sets:
			  an alternative approach is using true 3 color composition, which
			  is limited to 3 separate data sets
			  
		"""

		xrf, yrf=self.set_default_range()

		self.set_kwpars(kwpars)
		if xr != None: xrf=xr
		if yr != None: yrf=yr

		if self.doimage == False:
			# data points
			self.binx, self.nbinx = get_bin(self.binsize, self.nbin, self.binx, self.nbinx, xrf)
			self.biny, self.nbiny = get_bin(self.binsize, self.nbin, self.biny, self.nbiny, yrf)
		else:
			# image input
			# assume xr, and yr is given, and probably no log scale for x and y axes?
			zmax=None
			zmin=None

			for key in self.image:
				zmax_ = np.max(self.image[key])
				if zmax == None: zmax=zmax_
				elif zmax < zmax_: zmax=zmax_

				zmin_ = np.min(self.image[key])
				if zmin == None: zmin=zmin_
				elif zmin > zmin_: zmin=zmin_

				# assume everything is identical for now
				nbinx, nbiny = self.image[key].shape
				binx = (xrf[1]-xrf[0])/nbinx
				biny = (yrf[1]-yrf[0])/nbiny

			if self.zmax == None: self.zmax=zmax
			if self.zmin == None: self.zmin=zmin


		if type(self.xedges).__name__ == 'NoneType':
			self.xedges = get_edges(xrf, self.nbinx, scale = self.xscale)

		if type(self.yedges).__name__ == 'NoneType':
			self.yedges = get_edges(yrf, self.nbiny, scale = self.yscale)

		bins = [self.xedges, self.yedges]

		zmax=None
		zmin=None
		if not self.doimage:
			# to get zmax
			self.weights=OrderedDict()
			image = OrderedDict()

			for key in self.xdata:
				heatmap, *_ = np.histogram2d(self.xdata[key], self.ydata[key], bins=bins) #, weights=weights)
				image[key] = heatmap.T

				zmax_=np.max(image[key])
				if zmax == None: zmax=zmax_
				elif zmax < zmax_: zmax=zmax_

				zmin_ = np.min(image[key])
				if zmin == None: zmin=zmin_
				elif zmin > zmin_: zmin=zmin_

				self.weights[key] = np.ones(len(self.xdata[key]))

		else:
			xdata, ydata = edges_to_data(self.xedges, self.yedges, 
						xr=self.xr, binx=self.binx, nbinx=self.nbinx, 
						yr=self.yr, biny=self.biny, nbiny=self.nbiny) 

			image = copy(self.image)
			self.weights=OrderedDict()
			for key in self.image:
				self.weights[key] = image[key].flatten()
				zmax_=np.max(self.weights[key])
				if zmax == None: zmax=zmax_
				elif zmax < zmax_: zmax=zmax_

				zmin_ = np.min(self.weights[key])
				if zmin == None: zmin=zmin_
				elif zmin > zmin_: zmin=zmin_

				if self.alpha[key] == None:
					self.alpha[key] = 1.0#/self.key

		if self.dorgb:
			self.image = np.zeros((self.nbinx, self.nbiny, 3))
			if not self.invert:
				for key in self.xdata:
					if self.color[key] == "red":
						self.image[:,:,0] = image[key]
					elif self.color[key] == "green":
						self.image[:,:,1] = image[key]
					elif self.color[key] == "blue":
						self.image[:,:,2] = image[key]
			else:
				for key in self.xdata:
					if self.color[key] == "red":
						self.image[:,:,1] = image[key]/2. +self.image[:,:,1]
						self.image[:,:,2] = image[key]/2. +self.image[:,:,2]
					elif self.color[key] == "green":
						self.image[:,:,0] = image[key]/2. +self.image[:,:,0]
						self.image[:,:,2] = image[key]/2. +self.image[:,:,2]
					elif self.color[key] == "blue":
						self.image[:,:,0] = image[key]/2. +self.image[:,:,0]
						self.image[:,:,1] = image[key]/2. +self.image[:,:,1]

		if self.noplot: return self.image, self.xedges, self.yedges
		if self.zmax == None: self.zmax=zmax
		if self.zmin == None: self.zmin=zmin


		def show(ion=True):

			plt.close('all')
			fig, ax = plt.subplots()

			if ion: plt.ion()
			norm, self.zmin, self.zmax = get_norm(zlog=self.zlog, zmid=self.zmid, 
						     zmin=self.zmin, zmax=self.zmax, zr=self.zr, 
						     zlthresh=self.zlthresh, zlscale=self.zlscale)

			im = OrderedDict()
			if not self.dorgb:
				for key in self.xdata:
					# cmap_N=20
					cmap            = plt.get_cmap(self.cmap[key]) #,cmap_N)
					cmap_alpha      = cmap(np.arange(cmap.N))
					cmap_alpha[:,3] = np.linspace(0, self.alpha[key],cmap.N)
					cmap            = ListedColormap(cmap_alpha)
					cmap.set_under((1,1,1,0))

					image[key], xedges, yedges, im[key] = ax.hist2d(self.xdata[key], self.ydata[key], 
								bins=bins, norm=norm, cmap=cmap, weights=self.weights[key])
			else:

				if not self.zlog:
					self.image=norm(self.image)
					# this will lose correct normalization factor
					if self.invert:
						diff=np.max(self.image)-np.min(self.image)
						self.image = 1.-self.image/diff
				else:
					self.image=norm(self.image.flatten()).reshape(self.nbinx, self.nbiny, 3)
					if self.invert: self.image = 1.-self.image

				for key in self.color:
					if not self.invert:
						if self.color[key] == 'red':
							colors_ = [(c,0,0,1) for c in np.linspace(0,1,256)]
						elif self.color[key] == 'green':
							colors_ = [(0,c,0,1) for c in np.linspace(0,1,256)]
						elif self.color[key] == 'blue':
							colors_ = [(0,0,c,1) for c in np.linspace(0,1,256)]
						else:
							continue
					else:
						if self.color[key] == 'red':
							colors_ = [(1,1-c,1-c,1) for c in np.linspace(0,0.5,256)]
						elif self.color[key] == 'green':
							colors_ = [(1-c,1,1-c,1) for c in np.linspace(0,0.5,256)]
						elif self.color[key] == 'blue':
							colors_ = [(1-c,1-c,1,1) for c in np.linspace(0,0.5,256)]
						else:
							continue

					cmap = colors.LinearSegmentedColormap.from_list('mycmap', colors_, N=256)
					im[key] = cm.ScalarMappable(norm=norm, cmap=cmap)

				xedges = self.xedges
				yedges = self.yedges

				ax.imshow(self.image, extent=[xrf[0],xrf[1],yrf[0],yrf[1]])

			ax.set_aspect(self.aspect)

			if self.noplot: return self.image

			if self.xhist or self.yhist:
				if self.despine == None: self.despine=True
			despine_axes(ax, self.despine)

			if self.xhist:
				project_hist(self.xdata, self.ydata, image, self.weights, self.color, xedges,
						direction='x',
						mr=xrf, ar=yrf, zlog=self.zlog, grid=self.grid,
						scale=self.xscale, nbin=self.nbiny, anbin=self.nbinx, 
						slice=self.yslice, hscale=self.xh_scale,
						hgap=self.hgap, hheight=self.hheight, halpha=self.halpha, 
						doimage=self.doimage, plt=plt, ax=ax, despine=self.despine)

			if self.yhist:
				project_hist(self.ydata, self.xdata, image, self.weights, self.color, yedges,
						direction='y',
						mr=yrf, ar=xrf, zlog=self.zlog, grid=self.grid,
						scale=self.yscale, nbin=self.nbinx, anbin=self.nbiny,
						slice=self.xslice, hscale=self.yh_scale,
						hgap=self.hgap, hheight=self.hheight, halpha=self.halpha, 
						doimage=self.doimage, plt=plt, ax=ax, despine=self.despine)


			rect, self.loc_ylabel, self.y_title = colorbar(im, ax, fig, self.label,  
					cbar=self.cbar, gap=self.cb_gap, 
					ticklocation=self.cb_ticklocation, orientation=self.cb_orientation,
					hsize=self.hheight+self.hgap, xhist=self.xhist, yhist=self.yhist, 
					loc_ylabel=self.loc_ylabel, y_title=self.y_title)
		
			self.wrap(plt, ax, xr=xrf, yr=yrf, label=not self.cb_outside, rect=rect)

			return self.image

		image = show(ion=False)
		if self.hold: embed()

		return image, self.xedges, self.yedges

#----------------------------------------------------------------------------------------
class base:
	
	key = 0
	maxkey = 0

	# common
	xdata,     ydata     = OrderedDict(), OrderedDict()
	xr,        yr	   = OrderedDict(), OrderedDict()
	altx,      alty	   = OrderedDict(), OrderedDict()
	alpha,     color     = OrderedDict(), OrderedDict()
	attr			   = OrderedDict()
	label			   = OrderedDict()

	xlabel  = ylabel  = None
	xscale  = yscale  = 'linear'
	title   = outfile = None
	display = ion     = hold     = False
	verbose = 1
	
	datfile = None
	xcol    = 'x'
	ycol    = 'y'
	xunit   = yunit   = ''
	xlabel2 = ylabel2 = ''
	xr2     = yr2	= None
	bbox_to_anchor    = None
	grid    = None
	margin     = 0.00

	# annotation: text, ellipse, polygon
	text         = None
	text_kw      = {}
	ellipse      = None
	ellipse_kw   = {}
	polygon      = None
	polygon_kw   = {}

	# alternative axes
	add_ax2	 = False
	add_ay2	 = False
	dolegend	 = True

	# data save
	colnames	= ['x','y']
	units		= ['','']

	noplot    = False
	loc_ylabel=None
	y_title   =None

	binsize = None
	nbin	  = 100
	edges	  = None


	def __init__(self, **kwpars):
		self.set_kwpars(kwpars)

	def set_kwpars(self, kwargs):

		ignored=[]
		for key, val in kwargs.items(): 
			if hasattr(self, key): setattr(self, key, val)
			else:			     ignored.append(key)
		if len(ignored) >0:
			print(cc.err,'Followings are not defined, so ignored, so double check:'+cc.reset)
			print(cc.err,ignored,cc.reset)

		return 1

	def wrap(self, plt, ax, **kwpars):
		wrap(plt, xlabel=self.xlabel, ylabel=self.ylabel, title=self.title, 
				xscale=self.xscale, yscale=self.yscale, outfile=self.outfile, 
				ax=ax, grid=self.grid,
				xlabel2=self.xlabel2, ylabel2=self.ylabel2, xr2=self.xr2, yr2=self.yr2,
				loc_ylabel=self.loc_ylabel, y_title=self.y_title,
				text=self.text, text_kw=self.text_kw,
				polygon=self.polygon, polygon_kw=self.polygon_kw,
				ellipse=self.ellipse, ellipse_kw=self.ellipse_kw,
				ion=self.ion, display=self.display, **kwpars)

	def set_default_range(self):

		for key in self.xdata:
			if 'xrf' not in locals(): xrf=self.xr[key]
			if 'yrf' not in locals(): yrf=self.yr[key]

			if xrf[0] > self.xr[key][0]: xrf[0] = self.xr[key][0]
			if xrf[1] < self.xr[key][1]: xrf[1] = self.xr[key][1]
			if yrf[0] > self.yr[key][0]: yrf[0] = self.yr[key][0]
			if yrf[1] < self.yr[key][1]: yrf[1] = self.yr[key][1]

		if self.verbose >1: print("range:",xrf, yrf)
		return xrf, yrf

	@prep_data_deco
	def collect_data(self, xdata=None, ydata=None, key=None,
			xlowdata=None, xhighdata=None, ylowdata=None, yhighdata=None, 
			xerrdata=None, yerrdata=None, xlerrdata=None, ylerrdata=None,
			image=None, cmap=None,
			xr=None, yr=None, label=None, 
			marker='.', linestyle='None', linewidth=1.5,
			color=None, alpha=None, errcolor=None, erralpha=None, 
			altx=False, alty=False, rexpr=None, attr='',
			savgol=None, smooth=None,
#			rcParams=None,
			help=None, hold=False, verbose: int= 0, **kwargs):
		"""
		collect multiple data set for plot
			 -parameters are divided into two groups: one for each data
				set, and the other for common use
			 -relies on the decorator for data load: see
				'(cjpy.)plottool.prep_data_deco' 

			 Some nontrivial parameters:
				 altx, alty: 2ndary axes data 
				 rexpr: not used?
				 attr:
					 makehist: to make a histogram on the fly
					 hist: data is a histogram
					 poisson_error: add Poisson error
		"""

		if key == None: key = self.key

		self.xdata		[key] = xdata
		self.ydata		[key] = ydata
		self.xr		[key] = xr
		self.yr		[key] = yr
		self.marker		[key] = marker
		self.linestyle	[key] = linestyle
		self.linewidth	[key] = linewidth
		self.color		[key] = color
		self.alpha		[key] = alpha
		self.altx		[key] = altx
		self.alty		[key] = alty
		self.rexpr		[key] = rexpr
		self.attr		[key] = attr
		self.image		[key] = image
		self.cmap		[key] = cmap
		self.savgol		[key] = savgol
		self.smooth		[key] = smooth
		self.xlowdata	[key] = xlowdata
		self.ylowdata	[key] = ylowdata
		self.xhighdata	[key] = xhighdata
		self.yhighdata	[key] = yhighdata
		self.xerrdata	[key] = xerrdata
		self.yerrdata	[key] = yerrdata
		self.xlerrdata	[key] = xlerrdata
		self.ylerrdata	[key] = ylerrdata

		if errcolor == None: errcolor=color
		if erralpha == None: erralpha=alpha
		self.errcolor	[key] = errcolor
		self.erralpha	[key] = erralpha

		if label == None: self.label[key] = str(key)
		else:			self.label[key] = label
	
		# in order to set options any time
		# in this way one time options can be set in the -main options
		# but it becomes redundantly repeated when collect_data is
		# repeatedly called as -main
		# should go either class initialization or 
		# the -post routine, but that would make the -option setting a bit deeper
		self.set_kwpars(kwargs)
		if len(self.xdata.keys()) == 1:
			self.verbose = kwargs.get('verbose', verbose)
#			set_rcParams(rcParams, verbose=verbose)
		#print(self.verbose)

		if self.refer: 
			self.refkey=key
			self.refer = False

		# self.key = key + 1
		self.maxkey = self.maxkey + 1
		self.key = self.maxkey

		if self.verbose > 2:
			print(xdata)
			print(ydata)
		return 1

	def composite_data(self, key=None, inkeys=None, 
			  xexpr=None, yexpr=None, 
			  varx= None, vary=None, defkey=None, **kwpars):
		if type(inkeys).__name__ == None: return
		if key == None: 
			self.maxkey = self.maxkey+1
			key = self.maxkey

		nkeys_= len(inkeys)

		if type(varx).__name__ == 'NoneType': 
			varx=[]
			for idx_, each_ in enumerate(inkeys):
				varx.append('x'+str(idx_))

		if type(vary).__name__ == 'NoneType': 
			vary=[]
			for idx_, each_ in enumerate(inkeys):
				vary.append('y'+str(idx_))

		for idx_, each_ in enumerate(inkeys):
			if each_ not in self.xdata:
				print(cc.err+'No data found for',each_,cc.reset)
				return

			locals()[varx[idx_]] = self.xdata[each_]
			locals()[vary[idx_]] = self.ydata[each_]

		xdata = eval(xexpr)
		ydata = eval(yexpr)


		self.collect_data(xdata=xdata, ydata=ydata, key=key)
		self.set_prop(key, **kwpars)

	def set_prop(self, key, **kwpars):
		for k, v in kwpars.items():
			x = getattr(self, k)
			x[key] = v
			setattr(self, k, x)

class onedim(base):
	
	# for 1-d plot
	rexpr		         = OrderedDict()
	marker		   = OrderedDict()
	linestyle, linewidth = OrderedDict(), OrderedDict()
	erralpha,  errcolor  = OrderedDict(), OrderedDict()
	savgol		   = OrderedDict()
	smooth		   = OrderedDict() 
	xlowdata, xhighdata  = OrderedDict(), OrderedDict()
	ylowdata, yhighdata  = OrderedDict(), OrderedDict()
	xerrdata, yerrdata   = OrderedDict(), OrderedDict()
	xlerrdata, ylerrdata = OrderedDict(), OrderedDict()

	# 1-dplot with reference data set
	refkey	= 0 # for reference data
	refer		= False
	refset	= False

	def set_default_color(self):

		pcolor = ["black","red","green","blue","purple","magenta","brown","orange","cyan"]
		icolor = 0
		lcolor = len(pcolor)

		for key in self.xdata:
			if self.color[key] == None:
				self.color[key] = pcolor[icolor]
				icolor = (icolor+1) % lcolor

			if self.alpha[key] == None:
				self.alpha[key] = 1.0 #/self.key

	@prep_data_deco
	def collect_data(self, xdata=None, ydata=None, key=None,
			xlowdata=None, xhighdata=None, ylowdata=None, yhighdata=None, 
			xerrdata=None, yerrdata=None, xlerrdata=None, ylerrdata=None,
			xr=None, yr=None, label=None, 
			marker='.', linestyle='None', linewidth=1.5,
			color=None, alpha=None, errcolor=None, erralpha=None, 
			altx=False, alty=False, rexpr=None, attr='',
			savgol=None, smooth=None,
#			rcParams=None,
			help=None, hold=False, verbose: int= 0, **kwargs):
		"""
		collect multiple data set for plot
			 -parameters are divided into two groups: one for each data
				set, and the other for common use
			 -relies on the decorator for data load: see
				'(cjpy.)plottool.prep_data_deco' 

			 Some nontrivial parameters:
				 altx, alty: 2ndary axes data 
				 rexpr: not used?
				 attr:
					 makehist: to make a histogram on the fly
					 hist: data is a histogram
					 poisson_error: add Poisson error
		"""

		if key == None: key = self.key

		self.xdata		[key] = xdata
		self.ydata		[key] = ydata
		self.xr		[key] = xr
		self.yr		[key] = yr
		self.marker		[key] = marker
		self.linestyle	[key] = linestyle
		self.linewidth	[key] = linewidth
		self.color		[key] = color
		self.alpha		[key] = alpha
		self.altx		[key] = altx
		self.alty		[key] = alty
		self.rexpr		[key] = rexpr
		self.attr		[key] = attr
		self.savgol		[key] = savgol
		self.smooth		[key] = smooth
		self.xlowdata	[key] = xlowdata
		self.ylowdata	[key] = ylowdata
		self.xhighdata	[key] = xhighdata
		self.yhighdata	[key] = yhighdata
		self.xerrdata	[key] = xerrdata
		self.yerrdata	[key] = yerrdata
		self.xlerrdata	[key] = xlerrdata
		self.ylerrdata	[key] = ylerrdata

		if errcolor == None: errcolor=color
		if erralpha == None: erralpha=alpha
		self.errcolor	[key] = errcolor
		self.erralpha	[key] = erralpha

		if label == None: self.label[key] = str(key)
		else:			self.label[key] = label
	
		# in order to set options any time
		# in this way one time options can be set in the -main options
		# but it becomes redundantly repeated when collect_data is
		# repeatedly called as -main
		# should go either class initialization or 
		# the -post routine, but that would make the -option setting a bit deeper
		self.set_kwpars(kwargs)
		if len(self.xdata.keys()) == 1:
			self.verbose = kwargs.get('verbose', verbose)
#			set_rcParams(rcParams, verbose=verbose)
		#print(self.verbose)

		if self.refer: 
			self.refkey=key
			self.refer = False

		# self.key = key + 1
		self.maxkey = self.maxkey + 1
		self.key = self.maxkey

		if self.verbose > 2:
			print(xdata)
			print(ydata)
		return 1

	def scan_fitsfile_moot(self, infile=None, hdu="", x=None):
		if infile == None:
			return None
		hdul=fits.open(infile)
		tasks=OrderedDict()
		loops=[]
		for each in hdul:
			if hdu !="":
				if hdu != each.name: continue
			if not hasattr(each, 'columns'): continue
			for subeach in each.columns:
				new=False
				if bool(re.search('A',str(subeach.format))):
					continue
				if x != None:
					if x != subeach.name: 
						if hdu !="":
							loopid = subeach.name
						else:
							loopid = each.name + ' '+ subeach.name
						new=True
				else:
					x = subeach.name
				if new:
					loops.append(loopid)
					task=OrderedDict()
					task['infile']	=infile
					task['hdu']		=each.name
					task['x']		=x
					task['y']		=subeach.name
					task['label']	=loopid

					tasks['-loop=='+loopid] = task

		tasks['-loop'] = loops
		return tasks

	def scan_fits_cols(self, infile=None, hdu="", x=None):
		if infile == None:
			return None
		hdul=fits.open(infile)
		tasks=OrderedDict()
		for each in hdul:
			if hdu !="":
				if hdu != each.name: continue
			if not hasattr(each, 'columns'): continue
			for subeach in each.columns:
				new=False
				if bool(re.search('A',str(subeach.format))):
					continue
				if x != None:
					if x != subeach.name: 
						if hdu !="":
							loopid = subeach.name
						else:
							loopid = each.name + ' '+ subeach.name
						new=True
				else:
					x = subeach.name
				if new:
					task=OrderedDict()
					task['infile']	=infile
					task['hdu']		=each.name
					task['x']		=x
					task['y']		=subeach.name
					task['label']	=loopid

					tasks[loopid] = task
		return tasks

	def scan_fits_hdus(self, infile=None, x=None, y=None, hdu="", verbose=0, tolist=False, seed=None):
		if infile == None:
			return None

		infile=str(Path(infile).expanduser())
		hdul=fits.open(infile)
		tasks=OrderedDict()
		for each in hdul:

			if not hasattr(each, 'columns'): continue

			if hdu != "":
				if not bool(re.search(hdu,each.name)): continue
			if int(verbose)>0: print(each.name)

			ind=[]
			for idx, subeach in enumerate(each.columns):
				if bool(re.search('A',str(subeach.format))): continue
				ind.append(idx)
			if x == None or x == "": x=each.columns[ind[0]].name
			if y == None or y == "": y=each.columns[ind[1]].name

			x_bingo = False
			y_bingo = False
			for subeach in each.columns:
				if x == subeach.name: x_bingo=True
				if y == subeach.name: y_bingo=True

			if not x_bingo*y_bingo: continue

			task=OrderedDict()
			task['infile']	=infile
			task['hdu']		=each.name
			task['x']		=x
			task['y']		=y
			task['label']	=each.name

			if type(seed).__name__ != 'NoneType':
				for key in seed:
					if key not in task: task[key] =seed[key] 

			tasks[each.name] = task

		if tolist:
			idx=1
			for key, val in tasks.items(): 
				val['-id'] = f"{idx:02}:" + key
				idx=idx+1

			tasks=list(tasks.values())

		return tasks

	def mplot1d(self, xr=None, yr=None, keys=None, rcParams=None, lncols=1, **kwpars):
		"""Multiple Plot 1-D from input table
		"""

		if len(self.rexpr) == list(self.rexpr.values()).count(None):
			xrf, yrf=self.set_default_range()
			xref = yref = None
		else:
			if not self.refset:
				xref = self.xdata.pop(self.refkey)
				yref = self.ydata.pop(self.refkey)
				self.xref=xref
				self.yref=yref
				self.refset=True
			else:
				xref=self.xref
				yref=self.yref

			xrf  = self.xr[self.refkey]
			yrf  = self.yr[self.refkey]
			_, _ = self.set_default_range()

		self.set_default_color()
		self.set_kwpars(kwpars)
		if xr != None: xrf=xr
		if yr != None: yrf=yr

		def show(ion=True):
			if self.ion: plt.ion()

			plt.close('all')
			fig, ax = plt.subplots()
			ax2     = None
			ay2     = None

			nonlocal xrf, yrf
			nonlocal xref, yref
			nonlocal keys

			if self.datfile != None: pdt=OrderedDict()

			pids=[]
			overwrite=True
			if type(keys).__name__ == 'NoneType':
				keys = self.xdata.keys()
			for key in keys:

				if key not in self.xdata:
					print(cc.err+'No data found for',key,cc.reset)
					continue

				x=self.xdata[key]
				y=self.ydata[key]

				if self.rexpr[key] != None: x, y=eval(self.rexpr[key])

				pid, ax2, ay2 = plot1d_core(x, y, attr=self.attr[key], 
					xlow=self.xlowdata[key], xhigh=self.xhighdata[key], 
					ylow=self.ylowdata[key], yhigh=self.yhighdata[key], 
					xerr=self.xerrdata[key], yerr=self.yerrdata[key],
					xlerr=self.xlerrdata[key], ylerr=self.ylerrdata[key],
					xscale=self.xscale,  marker=self.marker[key], 
					label=self.label[key], 
					color=self.color[key], alpha=self.alpha[key],
					errcolor=self.errcolor[key], erralpha=self.erralpha[key],
					linestyle=self.linestyle[key], linewidth=self.linewidth[key],
					ax=ax, ax2=ax2, ay2=ay2, binsize=self.binsize, nbin=self.nbin,
					xr=xrf, yr=yrf, 
					smooth=self.smooth[key], savgol=self.savgol[key],
					altx=self.altx[key], alty=self.alty[key], 
					add_ax2=self.add_ax2, add_ay2=self.add_ay2,
					datfile=self.datfile, overwrite=overwrite,
					colnames=self.colnames, units=self.units, extname=self.label[key])

				overwrite=False

				if self.label[key] != "": pids.append(pid)
				
			if self.noplot: return ax, ax2, ay2
			if self.dolegend:
				plt.legend(labelcolor='linecolor', 
						bbox_to_anchor=self.bbox_to_anchor,
						ncol=lncols, handles=pids)

			if self.verbose >1: print('outfile',self.outfile)

			self.wrap(plt, ax, xr=xrf, yr=yrf, ax2=ax2, ay2=ay2, rcParams=rcParams)
			return ax, ax2, ay2

		ax, ax2, ay2 = show(ion=False)
		if self.hold: embed()

		return ax, ax2, ay2

class density(base):
	
	# for 2-d plot
	image	  = OrderedDict()
	cmap	  = OrderedDict()

	doimage = False
	binx    = biny   = None
	nbinx   = nbiny  = None
	zmax    = zmin   = None
	xedges  = yedges = None
	zr      = None
	zlog    = None
	zoff    = None
	zmid    = None
	zlthresh= None
	zlscale = None
	zlclip  = None
	aspect  = 'auto'

	xhist   = yhist   = False
	despine = None

	# colormap for 2-d map
	cb_outside = False
	cbar	     = False
	cb_outside =False
	cb_gap     =0.03
	cb_orientation =None
	cb_ticklocation=None

	cb_off    =None
	cb_width  =None
	cb_length =None
	zclip     =False

	# projection histogram related
	xhist     = yhist     = False 
	xh_height = yh_height = 0.15
	xh_scale  = yh_scale  = None 
	xslice    = yslice    = None

	halpha    = 0.1
	hgap      = 0.04
	hheight   = 0.15
	hcolor    = "darkblue"

	invert	 = False # for mdplot_rgb

	# RGB 
	dorgb		= False

	def set_default_color(self):

		pcmap = ["Blues","Reds","Greens","Greys","Purples","Oranges"]
		icmap = 0
		lcmap = len(pcmap)
		
		for key in self.xdata:
			if self.cmap[key] == None:
				self.cmap[key] = pcmap[icmap]
				icmap = (icmap+1) % lcmap

	@prep_data_deco
	def collect_data(self, xdata=None, ydata=None, key=None,
			xlowdata=None, xhighdata=None, ylowdata=None, yhighdata=None, 
			xerrdata=None, yerrdata=None, xlerrdata=None, ylerrdata=None,
			image=None, cmap=None,
			xr=None, yr=None, label=None, 
			marker='.', linestyle='None', linewidth=1.5,
			color=None, alpha=None, errcolor=None, erralpha=None, 
			altx=False, alty=False, rexpr=None, attr='',
			savgol=None, smooth=None,
#			rcParams=None,
			help=None, hold=False, verbose: int= 0, **kwargs):
		"""
		collect multiple data set for plot
			 -parameters are divided into two groups: one for each data
				set, and the other for common use
			 -relies on the decorator for data load: see
				'(cjpy.)plottool.prep_data_deco' 

			 Some nontrivial parameters:
				 altx, alty: 2ndary axes data 
				 rexpr: not used?
				 attr:
					 makehist: to make a histogram on the fly
					 hist: data is a histogram
					 poisson_error: add Poisson error
		"""

		if key == None: key = self.key

		self.xdata		[key] = xdata
		self.ydata		[key] = ydata
		self.xr		[key] = xr
		self.yr		[key] = yr

		self.altx		[key] = altx
		self.alty		[key] = alty
		# self.rexpr		[key] = rexpr
		self.attr		[key] = attr
		self.image		[key] = image
		self.cmap		[key] = cmap
		self.color		[key] = color
		self.alpha		[key] = alpha
		self.label		[key] = label


		if label == None: self.label[key] = str(key)
		else:			self.label[key] = label
	
		# in order to set options any time
		# in this way one time options can be set in the -main options
		# but it becomes redundantly repeated when collect_data is
		# repeatedly called as -main
		# should go either class initialization or 
		# the -post routine, but that would make the -option setting a bit deeper
		self.set_kwpars(kwargs)
		if len(self.xdata.keys()) == 1:
			self.verbose = kwargs.get('verbose', verbose)
#			set_rcParams(rcParams, verbose=verbose)
		#print(self.verbose)

		# self.key = key + 1
		self.maxkey = self.maxkey + 1
		self.key = self.maxkey

		if self.verbose > 2:
			print(xdata)
			print(ydata)
		return 1

	def mdplot(self, xr=None, yr=None, **kwpars):
		""" 
		2-d density plot for multiple data set
			- use this with plottool.plottool.collect_data for data load
			- best used with white color for low values (or low density)
			  the color map is auto alpha corrected for low values
				- alpha: sets the minimum transparency for each image
				- halpha: sets transparency for x and y histograms
			- in principle, there is no limit for the number of data sets:
			  an alternative approach is using true 3 color composition, which
			  is limited to 3 separate data sets
			  
		"""

		self.set_default_color()
		xrf, yrf=self.set_default_range()

		self.set_kwpars(kwpars)
		if xr != None: xrf=xr
		if yr != None: yrf=yr

		if self.doimage == False:
			# data points
			self.binx, self.nbinx = get_bin(self.binsize, self.nbin, self.binx, self.nbinx, xrf)
			self.biny, self.nbiny = get_bin(self.binsize, self.nbin, self.biny, self.nbiny, yrf)
		else:
			# image input
			# assume xr, and yr is given, and probably no log scale for x and y axes?
			zmax=None
			zmin=None

			for key in self.image:
				zmax_ = np.max(self.image[key])
				if zmax == None: zmax=zmax_
				elif zmax < zmax_: zmax=zmax_

				zmin_ = np.min(self.image[key])
				if zmin == None: zmin=zmin_
				elif zmin > zmin_: zmin=zmin_

				# assume everything is identical for now
				nbinx, nbiny = self.image[key].shape
				binx = (xrf[1]-xrf[0])/nbinx
				biny = (yrf[1]-yrf[0])/nbiny

			if self.zmax == None: self.zmax=zmax
			if self.zmin == None: self.zmin=zmin


		if type(self.xedges).__name__ == 'NoneType':
			self.xedges = get_edges(xrf, self.nbinx, scale = self.xscale)

		if type(self.yedges).__name__ == 'NoneType':
			self.yedges = get_edges(yrf, self.nbiny, scale = self.yscale)

		bins = [self.xedges, self.yedges]

		zmax=None
		zmin=None
		if not self.doimage:
			# to get zmax
			self.weights=OrderedDict()
			image = OrderedDict()

			for key in self.xdata:
				heatmap, *_ = np.histogram2d(self.xdata[key], self.ydata[key], bins=bins) #, weights=weights)
				image[key] = heatmap.T

				zmax_=np.max(image[key])
				if zmax == None: zmax=zmax_
				elif zmax < zmax_: zmax=zmax_

				zmin_ = np.min(image[key])
				if zmin == None: zmin=zmin_
				elif zmin > zmin_: zmin=zmin_

				self.weights[key] = np.ones(len(self.xdata[key]))

		else:
			xdata, ydata = edges_to_data(self.xedges, self.yedges, 
						xr=self.xr, binx=self.binx, nbinx=self.nbinx, 
						yr=self.yr, biny=self.biny, nbiny=self.nbiny) 

			image = copy(self.image)
			self.weights=OrderedDict()
			for key in self.image:
				self.weights[key] = image[key].flatten()
				zmax_=np.max(self.weights[key])
				if zmax == None: zmax=zmax_
				elif zmax < zmax_: zmax=zmax_

				zmin_ = np.min(self.weights[key])
				if zmin == None: zmin=zmin_
				elif zmin > zmin_: zmin=zmin_

				if self.alpha[key] == None:
					self.alpha[key] = 1.0#/self.key

		if self.dorgb:
			self.image = np.zeros((self.nbinx, self.nbiny, 3))
			if not self.invert:
				for key in self.xdata:
					if self.color[key] == "red":
						self.image[:,:,0] = image[key]
					elif self.color[key] == "green":
						self.image[:,:,1] = image[key]
					elif self.color[key] == "blue":
						self.image[:,:,2] = image[key]
			else:
				for key in self.xdata:
					if self.color[key] == "red":
						self.image[:,:,1] = image[key]/2. +self.image[:,:,1]
						self.image[:,:,2] = image[key]/2. +self.image[:,:,2]
					elif self.color[key] == "green":
						self.image[:,:,0] = image[key]/2. +self.image[:,:,0]
						self.image[:,:,2] = image[key]/2. +self.image[:,:,2]
					elif self.color[key] == "blue":
						self.image[:,:,0] = image[key]/2. +self.image[:,:,0]
						self.image[:,:,1] = image[key]/2. +self.image[:,:,1]

		if self.noplot: return self.image, self.xedges, self.yedges
		if self.zmax == None: self.zmax=zmax
		if self.zmin == None: self.zmin=zmin


		def show(ion=True):

			plt.close('all')
			fig, ax = plt.subplots()

			if ion: plt.ion()
			norm, self.zmin, self.zmax = get_norm(zlog=self.zlog, zmid=self.zmid, 
						     zmin=self.zmin, zmax=self.zmax, zr=self.zr, 
						     zlthresh=self.zlthresh, zlscale=self.zlscale)

			im = OrderedDict()
			if not self.dorgb:
				for key in self.xdata:
					# cmap_N=20
					cmap            = plt.get_cmap(self.cmap[key]) #,cmap_N)
					cmap_alpha      = cmap(np.arange(cmap.N))
					cmap_alpha[:,3] = np.linspace(0, self.alpha[key],cmap.N)
					cmap            = ListedColormap(cmap_alpha)
					cmap.set_under((1,1,1,0))

					image[key], xedges, yedges, im[key] = ax.hist2d(self.xdata[key], self.ydata[key], 
								bins=bins, norm=norm, cmap=cmap, weights=self.weights[key])
			else:

				if not self.zlog:
					self.image=norm(self.image)
					# this will lose correct normalization factor
					if self.invert:
						diff=np.max(self.image)-np.min(self.image)
						self.image = 1.-self.image/diff
				else:
					self.image=norm(self.image.flatten()).reshape(self.nbinx, self.nbiny, 3)
					if self.invert: self.image = 1.-self.image

				for key in self.color:
					if not self.invert:
						if self.color[key] == 'red':
							colors_ = [(c,0,0,1) for c in np.linspace(0,1,256)]
						elif self.color[key] == 'green':
							colors_ = [(0,c,0,1) for c in np.linspace(0,1,256)]
						elif self.color[key] == 'blue':
							colors_ = [(0,0,c,1) for c in np.linspace(0,1,256)]
						else:
							continue
					else:
						if self.color[key] == 'red':
							colors_ = [(1,1-c,1-c,1) for c in np.linspace(0,0.5,256)]
						elif self.color[key] == 'green':
							colors_ = [(1-c,1,1-c,1) for c in np.linspace(0,0.5,256)]
						elif self.color[key] == 'blue':
							colors_ = [(1-c,1-c,1,1) for c in np.linspace(0,0.5,256)]
						else:
							continue

					cmap = colors.LinearSegmentedColormap.from_list('mycmap', colors_, N=256)
					im[key] = cm.ScalarMappable(norm=norm, cmap=cmap)

				xedges = self.xedges
				yedges = self.yedges

				ax.imshow(self.image, extent=[xrf[0],xrf[1],yrf[0],yrf[1]])

			ax.set_aspect(self.aspect)

			if self.noplot: return self.image

			if self.xhist or self.yhist:
				if self.despine == None: self.despine=True
			despine_axes(ax, self.despine)

			if self.xhist:
				project_hist(self.xdata, self.ydata, image, self.weights, self.color, xedges,
						direction='x',
						mr=xrf, ar=yrf, zlog=self.zlog, grid=self.grid,
						scale=self.xscale, nbin=self.nbiny, anbin=self.nbinx, 
						slice=self.yslice, hscale=self.xh_scale,
						hgap=self.hgap, hheight=self.hheight, halpha=self.halpha, 
						doimage=self.doimage, plt=plt, ax=ax, despine=self.despine)

			if self.yhist:
				project_hist(self.ydata, self.xdata, image, self.weights, self.color, yedges,
						direction='y',
						mr=yrf, ar=xrf, zlog=self.zlog, grid=self.grid,
						scale=self.yscale, nbin=self.nbinx, anbin=self.nbiny,
						slice=self.xslice, hscale=self.yh_scale,
						hgap=self.hgap, hheight=self.hheight, halpha=self.halpha, 
						doimage=self.doimage, plt=plt, ax=ax, despine=self.despine)


			rect, self.loc_ylabel, self.y_title = colorbar(im, ax, fig, self.label,  
					cbar=self.cbar, gap=self.cb_gap, 
					ticklocation=self.cb_ticklocation, orientation=self.cb_orientation,
					hsize=self.hheight+self.hgap, xhist=self.xhist, yhist=self.yhist, 
					loc_ylabel=self.loc_ylabel, y_title=self.y_title)
		
			self.wrap(plt, ax, xr=xrf, yr=yrf, label=not self.cb_outside, rect=rect)

			return self.image

		image = show(ion=False)
		if self.hold: embed()

		return image, self.xedges, self.yedges

class spectral(onedim):

	mdata   , rdata   = OrderedDict(), OrderedDict()
	pdata   , data    = OrderedDict(), OrderedDict()
	mcxdata , mcydata = OrderedDict(), OrderedDict()
	mx      , my      = OrderedDict(), OrderedDict()
	mc = OrderedDict()
	rr = OrderedDict()

	ratio       = [3,1]
	rtype       ='relative'
	pfontsize   =8
	pfontfamily ="monospace"
	display     =True
	xticks      =None
	yticks      =None
	xtickv      =None
	ytickv      =None

	@prep_data_deco
	@prep_model_deco
	def collect_data(self, xdata=None, ydata=None, key=None,
			xlowdata=None, xhighdata=None, ylowdata=None, yhighdata=None, 
			xerrdata=None, yerrdata=None, xlerrdata=None, ylerrdata=None,
			xr=None, yr=None, label=None, 
			marker='.', linestyle='None', linewidth=1.5,
			color=None, alpha=None, errcolor=None, erralpha=None, 
			altx=False, alty=False, rexpr=None, attr='',
			savgol=None, smooth=None,
#			rcParams=None,
			help=None, hold=False, verbose: int= 0, **kwargs):
		"""
		collect multiple data set for plot
			 -parameters are divided into two groups: one for each data
				set, and the other for common use
			 -relies on the decorator for data load: see
				'(cjpy.)plottool.prep_data_deco' 

			 Some nontrivial parameters:
				 altx, alty: 2ndary axes data 
				 rexpr: not used?
				 attr:
					 makehist: to make a histogram on the fly
					 hist: data is a histogram
					 poisson_error: add Poisson error
		"""

		if key == None: key = self.key

		self.xdata		[key] = xdata
		self.ydata		[key] = ydata
		self.xr		[key] = xr
		self.yr		[key] = yr
		self.marker		[key] = marker
		self.linestyle	[key] = linestyle
		self.linewidth	[key] = linewidth
		self.color		[key] = color
		self.alpha		[key] = alpha
		self.altx		[key] = altx
		self.alty		[key] = alty
		self.rexpr		[key] = rexpr
		self.attr		[key] = attr
		self.savgol		[key] = savgol
		self.smooth		[key] = smooth
		self.xlowdata	[key] = xlowdata
		self.ylowdata	[key] = ylowdata
		self.xhighdata	[key] = xhighdata
		self.yhighdata	[key] = yhighdata
		self.xerrdata	[key] = xerrdata
		self.yerrdata	[key] = yerrdata
		self.xlerrdata	[key] = xlerrdata
		self.ylerrdata	[key] = ylerrdata

		if errcolor == None: errcolor=color
		if erralpha == None: erralpha=alpha
		self.errcolor	[key] = errcolor
		self.erralpha	[key] = erralpha

		if label == None: self.label[key] = str(key)
		else:			self.label[key] = label
	
		# in order to set options any time
		# in this way one time options can be set in the -main options
		# but it becomes redundantly repeated when collect_data is
		# repeatedly called as -main
		# should go either class initialization or 
		# the -post routine, but that would make the -option setting a bit deeper
		self.set_kwpars(kwargs)
		if len(self.xdata.keys()) == 1:
			self.verbose = kwargs.get('verbose', verbose)
#			set_rcParams(rcParams, verbose=verbose)
		#print(self.verbose)

		if self.refer: 
			self.refkey=key
			self.refer = False

		# self.key = key + 1
		self.maxkey = self.maxkey + 1
		self.key = self.maxkey

		if self.verbose > 2:
			print(xdata)
			print(ydata)
		return 1

#----------------------------------------------------------------------------------------
# plot Data Model Residual; e.g., spectral fit
@prep_data_deco
@prep_model_deco
def plotDMR(xdata=None, ydata=None, mdata=None, rdata=None, pdata=None, data=None,
		mcxdata=None, mcdata=None, mcdeco=None,		# module component x, data
		xr=None, yr=None, rr=None, 
		xerrdata=None, yerrdata=None, 
		xlowdata=None, xhighdata=None,
		ylowdata=None, yhighdata=None,
		mx=None, my=None, mc=None,
		marker ='None',  linestyle='None',   color='black', # for data
		emarker='None', elinestyle='solid', ecolor='black', # for data error or range
		mmarker='None', mlinestyle='solid', mcolor='red',   # for model
		rmarker='None', rlinestyle='None',  rcolor='black', # for residual
		smarker='None', slinestyle='solid', scolor='black', # for residual error or range
		xlabel=None, ylabel=None,  ylabel2=None, rlabel=None,	# 
		ratio=[3,1],						# data portion, error portion = 1.- data portion
		outfile=None, 
		xscale='log', yscale='log',				# often used for spectral analysis
		rtype  ='relative',
		pfontsize=8, pfontfamily="monospace",
		display=True, 
		xticks=None, yticks=None, xtickv=None, ytickv=None,
		help=None, hold=False, verbose: int= 0, **kwargs):

	pcolor = ["green","blue","purple","magenta","brown","orange"]
	icolor = 0
	lcolor = len(pcolor)
		
	def show(ion=True):
		if ion: plt.ion()

		nonlocal xdata, ydata, mdata, rdata, data
		nonlocal xerrdata, xlowdata, xhighdata
		nonlocal yerrdata, ylowdata, yhighdata
		nonlocal pcolor, icolor, lcolor

		plt.close('all')
		fig = plt.figure()
		gs  = fig.add_gridspec(2, hspace=0, height_ratios=ratio)
		axs = gs.subplots(sharex=True)
		ax = axs[0]

		label_statistic = ""
		if hasattr(data,'meta'):
			header = data.meta
			if "RCHI2" in header:
				label_statistic = label_statistic + "$\chi_r^2$ = %.2f" % (header["RCHI2"])
			if "DOF" in header:
				label_statistic = label_statistic + "  DoF = %d" % (header["DOF"])

		else:
			header = {}


		# plot models
		if type(mdata).__name__ == 'Table':
			ncols=len(mdata.columns)
		else:
			ncols= len(mdata.shape)

		if ncols == 1:
			ax.plot(xdata, mdata,
					color=mcolor,
					marker=mmarker, linestyle=mlinestyle)
		else:
			if (mx != None) and (my !=None):
				ax.plot(mdata[mx], mdata[my],
						color=mcolor,
						marker=mmarker, linestyle=mlinestyle)
				idx=1
				while True:
					try:
						mcdata = mdata[mc+str(idx)]
					except:
						break
					ax.plot(mdata[mx], mcdata,
						color=pcolor[icolor],
						marker=mmarker, linestyle=mlinestyle)
					icolor = (icolor +1) % lcolor
					idx = idx +1


		# plot data 
		ax.plot(xdata, ydata,
				color=color,
				marker=marker, linestyle=linestyle)

		# plot x and y error bars
		if type(xlowdata).__name__ == 'NoneType':
			xlowdata = xdata - xerrdata
			xhighdata= xdata + xerrdata
		if type(ylowdata).__name__ == 'NoneType':
			ylowdata = ydata - yerrdata
			yhighdata= ydata + yerrdata

		for ex, ey, exlow, exhigh in zip(xdata, ydata, xlowdata, xhighdata):
			ax.plot([exlow, exhigh],[ey,ey], 
				color=ecolor,
				marker=emarker, linestyle=elinestyle)
		for ex, ey, eylow, eyhigh in zip(xdata, ydata, ylowdata, yhighdata):
			ax.plot([ex,ex],[eylow, eyhigh],
				color=ecolor,
				marker=emarker, linestyle=elinestyle)

		# add fit parameter labels
		# will add more options
		if type(pdata).__name__ != 'NoneType':
			lineno=0
			for row in pdata:
				if row['frozen']: continue
				color_=mcolor
				if 'addcompno' in row.colnames:
					if row['addcompno'] >0:
						color_=pcolor[ (row['addcompno'] -1) % lcolor]
				t=ax.text(0.88,0.95-lineno*0.04, 
					row['aka'] + '.'+row['parameter']+': ',
					fontsize=pfontsize,
					fontfamily=pfontfamily,
					color=color_,
					horizontalalignment='right',
					transform=ax.transAxes)
				t.set_bbox(dict(alpha=0.5, facecolor="white", edgecolor="none", pad=0))
				lineno=lineno+1
			lineno=0
			addidx=0
			for row in pdata:
				if row['frozen']: continue
				color_=mcolor
				if 'addcompno' in row.colnames:
					if row['addcompno'] >0:
						color_=pcolor[ (row['addcompno'] -1) % lcolor]
				t=ax.text(0.88,0.95-lineno*0.04, 
					"%.2e" % (row['value']),
					fontsize=pfontsize,
					fontfamily=pfontfamily,
					color=color_,
					horizontalalignment='left',
					transform=ax.transAxes)
				t.set_bbox(dict(alpha=0.5, facecolor="white", edgecolor="none", pad=0))
				lineno=lineno+1
#			embed()

		# plot residuals
		axs[1].plot(xdata, rdata,
				color=rcolor,
				marker=rmarker, linestyle=rlinestyle)

		# plot residual x range
		for ex, ey, exlow, exhigh in zip(xdata, rdata, xlowdata, xhighdata):
			axs[1].plot([exlow, exhigh],[ey,ey], 
				color=scolor,
				marker=smarker, linestyle=slinestyle)

		# plot residual y error range
		if rtype =='relative':
			for ex, ey in zip(xdata, rdata):
				axs[1].plot([ex, ex],[-1+ey,1+ey], 
					color=scolor,
					marker=smarker, linestyle=slinestyle)
		elif rtype =='absolute':
			for ex, eylow, eyhigh in zip(xdata, ylowdata-ydata+rdata, yhighdata-ydata+rdata):
				axs[1].plot([ex, ex],[eylow,eyhigh], 
					color=scolor,
					marker=smarker, linestyle=slinestyle)

		t=axs[1].text(0.03,0.1, label_statistic, 
				horizontalalignment='left',
				transform=axs[1].transAxes)
		t.set_bbox(dict(alpha=0.5, facecolor="white", edgecolor="none", pad=0))

		wrap(plt, xr, yr, xlabel2=xlabel, ylabel=ylabel, 
				xscale=xscale, yscale=yscale, outfile=outfile, 
				ax=ax, ax2=axs[1], ay2=axs[1], ylabel2=ylabel2,
				xticks=xticks, yticks=yticks,
				xtickv=xtickv, ytickv=ytickv,
				display=display, ion=ion)

	show(ion=False)
	if hold: embed()

#----------------------------------------------------------------------------------------
# image merge for multipanel plots
def mergepdf(infile, layout=None, outfile=None, 
		 align=[0.5,0.5], # not used yet
		 firstdir='x', text=None,
		 verbose=0, debug=0, hold=False):
	""" merge multiple images in pdf into one page pdf file
	"""

	from PyPDF2 import PdfReader, PdfWriter, Transformation
	from PyPDF2.generic import RectangleObject

	ncol, nrow = [int(v) for v in layout.split('x')]

	images = OrderedDict()
	xsizes = np.zeros((ncol,nrow))#, dtype=int)
	ysizes = np.zeros((ncol,nrow))#, dtype=int)

	icol = OrderedDict()
	irow = OrderedDict()
	
	# figure out the size of each image
	new = True
	first = 0
	for idx, each in enumerate(infile):
		images[idx] = None

		if each == None: continue
		if each == ""  : continue

		ifile = PdfReader(each)
		images[idx] = ifile.pages[0]

		if firstdir == 'x':
			icol[idx] = int(idx % ncol)
			irow[idx] = int(idx / ncol)
		else:
			icol[idx] = int(idx / nrow)
			irow[idx] = int(idx % nrow)

		mdbox = images[idx].mediabox
		xsizes[icol[idx], irow[idx]] = mdbox.right-mdbox.left
		ysizes[icol[idx], irow[idx]] = mdbox.top  -mdbox.bottom

		if verbose>1: print("\t", idx, icol[idx], irow[idx], xsizes[icol[idx],irow[idx]], ysizes[icol[idx],irow[idx]])
		if new: 
			first=idx
			new = False

	widths  = [max(xsizes[i,:]) for i in range(0, ncol)]
	heights = [max(ysizes[:,j]) for j in range(0, nrow)]
	if verbose>1: print("\twidths: ", widths)
	if verbose>1: print("\theights: ", heights)

	twidth  = np.sum(widths)
	theight = np.sum(heights)

	if verbose>0: print(f"total size: {twidth} x {theight}")

	# now merge
	for key in images:
		if type(images[key]).__name__ == 'NoneType': continue
		image=images[key]
		swidth   = np.sum(widths  [:icol[key]  ])
		sheight  = np.sum(heights [:irow[key]  ])
		sheight2 = np.sum(heights [:irow[key]+1])
		image.mediabox = RectangleObject((0, 0, twidth, theight-sheight)) # this assumes each image starts at 0,0, if not....
		transformation = Transformation().translate(tx=swidth, ty=theight-sheight2)
		if verbose>1: print("\tshift", key, icol[key], irow[key], swidth, theight-sheight2, theight-sheight)
		image.add_transformation(transformation)

		if key == first: 
			base=image
		else:
			base.merge_page(image)
	
	if type(text).__name__ != 'NoneType':
		import io
		from reportlab.pdfgen.canvas import Canvas
		packet = io.BytesIO()
		c = Canvas(packet,pagesize=(twidth,theight))
		for each in text:
			x = int(each.pop('x')*twidth)
			y = theight-int(each.pop('y')*theight)
			t = each.pop('t')
			c.drawString(x,y,t)
		c.save()
		packet.seek(0)
		overlay_pdf = PdfReader(packet)
		overlay = overlay_pdf.pages[0]
		base.merge_page(overlay)

	if outfile != None:
		writer = PdfWriter()
		base.compress_content_streams()
		writer.add_page(base)
		with open(outfile, "wb") as fp:
		    writer.write(fp)

def mergepng(infile, layout=None, outfile=None, align=[0.5,0.5], 
		 bgcolor='white', firstdir='x', text=None,
		 verbose=0, debug=0, hold=False):
	""" merge multiple images in pdf into one page pdf file
	"""

	from PIL import Image, ImageDraw, ImageFont

	ncol, nrow = [int(v) for v in layout.split('x')]

	images = OrderedDict()
	xsizes = np.zeros((ncol,nrow), dtype=int)
	ysizes = np.zeros((ncol,nrow), dtype=int)

	icol = OrderedDict()
	irow = OrderedDict()
	
	# figure out the size of each image
	new = True
	first = 0
	for idx, each in enumerate(infile):
		images[idx] = None

		if each == None: continue
		if each == ""  : continue

		images[idx] = Image.open(each)

		icol[idx] = int(idx % ncol)
		irow[idx] = int(idx / ncol)

		xsizes[icol[idx], irow[idx]] = images[idx].width
		ysizes[icol[idx], irow[idx]] = images[idx].height 

		if verbose>1: print("\t", idx, icol[idx], irow[idx], xsizes[icol[idx],irow[idx]], ysizes[icol[idx],irow[idx]])
		if new: 
			first=idx
			new = False

	widths  = [max(xsizes[i,:]) for i in range(0, ncol)]
	heights = [max(ysizes[:,j]) for j in range(0, nrow)]
	if verbose>1: print("\twidths: ", widths)
	if verbose>1: print("\theights: ", heights)

	twidth  = np.sum(widths)
	theight = np.sum(heights)

	if verbose>0: print(f"total size: {twidth} x {theight}")

	# if firstdir =='x':
	# 	base = Image.new('RGBA', size=(theight, twidth), color=bgcolor)
	# else:
	base = Image.new('RGBA', size=(twidth, theight), color=bgcolor)

	# now merge
	for key in images:
		if type(images[key]).__name__ == 'NoneType': continue
		image=images[key]
		if firstdir =='x':
			i = icol[key]
			j = irow[key]
			y = sum(widths[:i]) + int((widths[i] - image.width) * align[0])
			x = sum(heights [:j]) + int((heights [j] - image.height ) * align[1])
			base.paste(image, (y, x))
		else:
			i = icol[key]
			j = irow[key]
			y = sum(heights[:i]) + int((heights[i] - image.height) * align[1])
			x = sum(widths [:j]) + int((widths [j] - image.width ) * align[0])
			base.paste(image, (x, y))

	if type(text).__name__ != 'NoneType':
		font = ImageFont.truetype("/usr/share/fonts/truetype/Helvetica/Helvetica.ttf", 40)
		draw = ImageDraw.Draw(base)
		for each in text:
			x = int(each.pop('x')*twidth)
			y = int(each.pop('y')*theight)
			t = each.pop('t')
			draw.text((x,y), t, font=font, fill='black', align = 'left')

	if outfile != None:
		base.save(outfile)

