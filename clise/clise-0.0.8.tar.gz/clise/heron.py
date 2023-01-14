# heron dives into a module and execute a function just as 
# herons dive into water and catch fish.

__version__    = '0.0.8'

import json
import hjson    as hjson

if 'clise' in __file__:
	import clise.jsontool as jt
	import clise.rabbit   as rb
else:
	import jsontool as jt
	import rabbit   as rb

import re
import sys
import math
import glob 
import hashlib      
import textwrap3	# we modify one of its routines below: len

import numpy  as np

from os		import path, makedirs, chdir, getcwd, getenv, mkdir
from pathlib	import Path
from socket		import gethostname
from collections  import OrderedDict
from datetime     import datetime
from importlib    import import_module
from IPython	import embed

cc = jt.cc()

def version():
	return __version__

# handle input parameters
def get_func_parameters(func):
	""" check func input parameters and keyword
	    and update them with the given cfg dictionary
	""" 

	if hasattr(func,'__code__'):
		keys = func.__code__.co_varnames[:func.__code__.co_argcount][::-1]
	else: 
		return [], {}
	sorter = {j: i for i, j in enumerate(keys[::-1])} 
	if func.__defaults__ != None:
		values = func.__defaults__[::-1]
		kwargs = {i: j for i, j in zip(keys, values)}
		sorted_args = tuple(
			sorted([i for i in keys if i not in kwargs], key=sorter.get)
		)
		sorted_kwargs = {
			i: kwargs[i] for i in sorted(kwargs.keys(), key=sorter.get)
		}   
	else:
		sorted_args = keys[::-1]
		sorted_kwargs = OrderedDict()

	return sorted_args, sorted_kwargs

def set_func_parameters(sorted_args, sorted_kwargs, cfg=None):
	""" check func input parameters and keyword
	    and update them with the given cfg dictionary
	""" 
	updated_args=[]
	for par in sorted_args:
		if par in cfg: updated_args.append(cfg[par])
		else:		   updated_args.append(None)

	if sorted_kwargs != None:
		updated_kwargs=OrderedDict()
		for par in sorted_kwargs:
			if par in cfg: updated_kwargs[par]=cfg[par]
			else:		   updated_kwargs[par]=sorted_kwargs[par]

	# if you meet this, the function doesn't tell us what it needs
	# e.g., math.sin
	if updated_args == []:
		for par in cfg.get('-pars',[]):
#			print(par)
			if par in cfg.keys() - updated_kwargs.keys():
				updated_args.append(cfg[par])
	for par in cfg.get('-kwpars',[]):
		if par in cfg:
			updated_kwargs[par] = cfg[par]
		else:
			updated_kwargs[par] = None
	
	# only when -pars are set
	if cfg.get('-collect',False):
		for par in cfg:
			if par in cfg.get('-exclude_kwpars',[]):      continue
#			if par[0:1] == '-':		 continue
			if not bool(re.search('^[a-zA-Z_]',par)): continue
			# if par in cfg.get('-pars',[]): continue
			if par in sorted_args: continue
			if par not in updated_kwargs.keys():
				updated_kwargs[par] = cfg[par]

	if len(sorted_args) >0:
		if sorted_args[0] == 'self': 
			sorted_args = sorted_args[1:]
			updated_args = updated_args[1:]

	return updated_args, updated_kwargs

def set_module_parameters(module, cfg, keys=None):
	""" set module global parameters
	""" 
	if cfg == None: return
	if keys == None:
		for key in cfg:			setattr(module, key, cfg[key])
	else:
		for key in keys & cfg.keys(): setattr(module, key, cfg[key])

#----------------------------------------------------------------------------

def global_diagnostic(cfgs):
	if help_text(cfgs[0].get('-help', False), raw=cfgs[0].get('-rawtext',False)): exit()

	userhelp=str(cfgs[0].get('-Help',False))
	if 'True' in userhelp:
		for each in cfgs: Help_text(each)
		exit()
	elif 'False' not in userhelp:
		Help_text(cfgs[0], userhelp)
		exit()

def diagnostic(cfg):

	global show

	if '-main' not in cfg.keys():
		print('no -main: need the main subroutine to execute')
		if '-show' in cfg.keys(): show(cfg, full=True)
		return True
	
	show = str(cfg.get('-show',None))
	if 'True' in show:
		print(cc.hl+'job', cfg['-id']+':',cfg['-main'],cc.reset)
		jt.show(cfg)
		return True

	return False

def skip(cfg):

	# input files exist?
	for each in jt.str_to_list(cfg.get('-checkin',[])):
		target = cfg.get(each,'')
		if target == None or target == '': continue
		if not path.exists(target): 
			print(cc.err+'missing input',target,'skipping...'+cc.reset) 
			return True

	# output files exist?
	# this needs to be combined with -timecheck or -sizecheck
	if not cfg.get('-clobber',False):
		for each in jt.str_to_list(cfg.get('-checkout',[])):
			target = cfg.get(each,'')
			if target == None or target == '': continue
			if path.exists(target): 
				if cfg['-verbose'] == 0: target = path.basename(target)
				print(cc.err+'output',target,'exists. skipping...'+cc.reset) 
				return True
	else:
		for each in jt.str_to_list(cfg.get('-after',[])):
			key, reference = each.split(':')
			target = cfg.get(key,'')
			if target == None or target == '': continue
			mt_target    = Path(target).expanduser().stat().st_mtime
			if reference not in mt_refer:
				mt_refer[reference] = Path(reference).expanduser().stat().st_mtime
			if mt_target < mt_refer[reference]: 
				print(cc.err+key, target,'is modified earlier than',reference+'. skipping...'+cc.reset) 
				return True

		for each in jt.str_to_list(cfg.get('-before',[])):
			key, reference = each.split(':')
			target = cfg.get(key,'')
			if target == None or target == '': continue
			mt_target    = Path(target).expanduser().stat().st_mtime
			if reference not in mt_refer:
				mt_refer[reference] = Path(reference).expanduser().stat().st_mtime
			if mt_target > mt_refer[reference]: 
				print(cc.err+key, target,'is later than',reference+'. skipping...'+cc.reset) 
				return True


	# include
	for each in jt.str_to_list(cfg.get('-include',[])):
		key, phrase = each.split(':')
		target = cfg.get(key,None)
		if target == None or target == '': continue
		mat=re.search(phrase,target)
		if not bool(mat): 
			print(cc.err+key, target,'does not have',phrase+'. skipping...'+cc.reset) 
			return True

	# exclude
	for each in jt.str_to_list(cfg.get('-exclude',[])):
		key, phrase = each.split(':')
		target = cfg.get(key,None)
		if target == None or target == '': continue
		mat=re.search(phrase,target)
		if bool(mat): 
			print(cc.err+key, target,'has',phrase+'. skipping...'+cc.reset) 
			return True

	return False

def create_dir(trgdir):
	if not path.isdir(trgdir):
		if trgdir !='':
			mkdir(trgdir)

#----------------------------------------------------------------------------
# load module
def load_routine_(name, cfg=None, show_trace=False, 
		class_name=None, class_obj=None, module_main=None):
	levels  = name.split('.')
	nlevels = len(levels)

	# -init is set, then search for class_def again
	skip_init=False
	if "-init" in cfg:
		init=cfg['-init']
		if type(init) is bool:
			if init: 
				class_name='.'.join(levels[0:-1:])
				init=OrderedDict()
				init['-class'] = class_name
			else:
				skip_init=True
		elif '-class' not in cfg:
			class_name='.'.join(levels[0:-1:])
		else: class_name=init['-class']

	use_class = False
	if not skip_init:
		if class_name != None:
			if bool(re.search('^'+class_name,name)):
				use_class = True

	if nlevels == 1:
		if type(__builtins__).__name__ == 'dict':
			routine=__builtins__[levels[0]]
		else: routine=getattr(__builtins__,levels[0])
		if show_trace: print(routine, type(routine).__name__)
		module=None
	else:
		if levels[0] == module_main: module = module_main
		else:                        
			# no preloader? generalize later
			if levels[0] == 'cjpy':
				module = __import__('cjpy.'+levels[1])
			else:
				module = __import__(levels[0])

		routine = module
		if show_trace: print(routine, type(routine).__name__)
		for idx, each in enumerate(levels[1:]): 
			try:
				routine = getattr(routine, each)
			except AttributeError:
				routine = import_module(each, routine)

			if show_trace: print(routine, type(routine).__name__)

#			if init_class:
			if use_class:
				if idx == nlevels-3: # this doesn't seem good enough, what if the levels are higher?
					if type(routine).__name__ == 'type':
						if class_obj != None:
							routine = getattr(class_obj, levels[-1])
						else:
							icfg=init.copy()
							# assume initialization parameters should be specified
							icfg['-collect'] = icfg.get('-collect',True)
							init_args,  init_kwargs = set_func_parameters([], [],cfg=icfg)
							# print(init_args, init_kwargs)
							try:
								class_obj=routine(*init_args,**init_kwargs)
								routine = getattr(class_obj, levels[-1])
							except:
								# oops, not class
								routine = getattr(routine, levels[-1])
						break
	return routine, module, class_obj, class_name

def load_routine(name, cfg=None, show_trace=False):

	levels  = name.split('.')
	nlevels = len(levels)

	if nlevels == 1:
		if type(__builtins__).__name__ == 'dict': routine = __builtins__[levels[0]]
		else:							routine = getattr(__builtins__,levels[0])
		if show_trace: print(routine, type(routine).__name__)
		return routine, None

	if levels[0] not in sys.modules:
		module = __import__(levels[0]) 
	else:
		module = sys.modules[levels[0]]

	# potential class name
	class_name_ = '.'.join(levels[0:-1])
	global class_object, class_name
	if "-object" in cfg:
		if cfg["-object"] in class_obj:
			if show_trace: print('loading the requested object', cfg["-object"])
			object = class_obj[cfg["-object"]]
			routine = getattr(object, levels[-1])
			return routine, module
	else:
		if class_name_ in class_obj:
			if show_trace: print('loading the existing object', class_name_)
			object = class_obj[class_name_]
			routine = getattr(object, levels[-1])
			return routine, module

	routine = module
	if show_trace: print(routine, type(routine).__name__)
	for idx, each in enumerate(levels[1:]): 
		try:
			routine = getattr(routine, each)
		except AttributeError:
			routine = import_module(each, routine)

		if show_trace: print(idx, routine, type(routine).__name__)

		if idx == nlevels-3: # -3 indicates the next to the last name

			icfg=cfg.get('-init',OrderedDict()).copy()
			icfg['-collect'] = icfg.get('-collect',True)  # by default, collect everything in "-init"
			init_args,  init_kwargs = set_func_parameters([], [],cfg=icfg)

			# print(init_args, init_kwargs)
			try:
				# now we are loading a new class or attempting

				class_obj_  = routine(*init_args,**init_kwargs)
				routine     = getattr(class_obj_, levels[-1])

				# if not specified, then use class_name_ for the key of the object
				# so that the same class name will share the same object
				# if there needs to be more than an object for the same class,
				# one has to specify "-object" to separate them
				objkey	= cfg.get("-object", class_name_) 

				# if you are here, then safe to assign these
				class_name[objkey] = class_name_
				class_obj [objkey] = class_obj_
			except:
				# oops, not class
				routine = getattr(routine, levels[-1])
			break

	return routine, module

def execute_routine(routine, args, kwargs, cfg=None, show_out=False):
	out=routine(*args, **kwargs)
	if type(out).__name__ == 'function': 
		args,  kwargs = get_func_parameters(out)
		args,  kwargs = set_func_parameters(args, kwargs, cfg=cfg)
		out=out(*args, **kwargs)
	if show_out: print(out)
	return out

# should we use a class
routines   =OrderedDict()
modules    =OrderedDict()
taskkey    = 0
maxtask    = 1
class_obj  =OrderedDict()
class_name =OrderedDict()
output     =OrderedDict()
mt_refer   =OrderedDict()
show	     =''

# execute configuration file

# to avoid conflict with expression in eval, most variables start and end with _
def inherit(_cfg_):
	global output
	_output_ = output.copy()
	if "-inherit" in _cfg_:
		for _each_ in _output_:
			locals()[_each_]=_output_[_each_]

		# this is not necessarily a scalar value, but it's just the first
		# element of the dictionary values instead of the whole dictionary.
		if "-scalar" in _cfg_["-inherit"]:
			_selected_ = _cfg_["-inherit"]["-scalar"]
			for _each_ in _selected_:
				locals()[_each_]=eval("list("+_each_+".values())[0]")

		# this returns the dictionary values as a list
		if "-list" in _cfg_["-inherit"]:
			_selected_ = _cfg_["-inherit"]["-list"]
			for _each_ in _selected_:
				locals()[_each_]=eval("list("+_each_+".values())")

		for _key_, _val_ in _cfg_["-inherit"].items():
			if _key_[0] == "-": continue
			_cfg_[_key_] = eval(_val_)
	return _cfg_

def execute(cfg):
	""" execute the main routine called in cfg
	"""

	global show

	# rabbit=cfg.get('-rabbit', False) >= True
	block ='rabbit' in cfg.get('-block', '') 
	if diagnostic(cfg): 
		if not block: return True
		return False

	job_str=['job', f"{cfg['-jobc']}/{cfg['-maxjob']}",
		"%-8s: %-25s:" % (cfg['-nid'],cfg['-id']), cfg['-main']]
	job_str=" ".join(job_str)
	if 'job' in show:
		idf = cfg['-id'].split(':')
		print(cc.hl+job_str, cc.reset)

	if 'input' in show:
		jt.show(cfg, full=False)
		if not block: return True

	if 'hidden' in show:
		jt.show(cfg, full=True)
		if not block: return True

	if 'file' in show:
		jt.show_files(cfg)

	if cfg.get('-dump','') != '':
		try:
			cfg_str = json.dumps(cfg.copy())
			hfile = open(path.expanduser(cfg['-dump']),"a")
			hfile.write('// '+job_str+'\n')
			hfile.write(cfg_str.replace(',',',\n\t'))
			hfile.write(',\n')
			hfile.close()
		except:
			print(cc.err+"cannot dump cfg since serializing cfg failed"+cc.reset)

	# anything not at the base level, assume it's a function inside a class
	# cfg['-init'] = cfg.get('-init',len(cfg['-main'].split('.'))>1)

	global taskkey
	routine, module = load_routine(cfg['-main'], cfg=cfg, show_trace='trace' in show)

	routines[taskkey] = routine
	modules [taskkey] = module

	routine_args,  routine_kwargs = get_func_parameters(routine)

	if 'func' in show:
		jt.show_feed(routine_args, routine_kwargs, cfg['-main'])
		return True

	# -------------------------------------------------------------------------
	# variable inherit
	cfg=inherit(cfg)
	# -------------------------------------------------------------------------
	# when the routine has clear input parameters exposed, take advantage of it
	# if hasattr(routine,'__code__'):
	# 	routine_keys = routine.__code__.co_varnames[:routine.__code__.co_argcount][::-1]
	# else: routine_keys = []
	#
	# cfg['-pars'] = cfg.get('-pars', routine_keys[::-1])
	# actualy this part requires switching the unique parameter sets
	# default=OrderedDict()
	# for each in cfg['-pars']:
	# 	if each in cfg: default[each] = cfg[each]
	#
	# if len(default)==0: default=copy(cfg)
	# -------------------------------------------------------------------------
	# set module level global parameters
	if '-global' in cfg.keys(): 
		gvar = cfg['-global']
		# doing this here for safety
		if type(gvar) is list:
			gvar=OrderedDict()
			for each in cfg['-global']:
				if each in cfg.keys(): gvar[each] = cfg[each]
		set_module_parameters(module, gvar)

	if 'time' in show: start_time=datetime.now()

	# if this is a native routine, feed the whole thing either by class itself or cfg
	sorted_args   = OrderedDict()
	sorted_kwargs = OrderedDict()
	sorted_args, sorted_kwargs = set_func_parameters(routine_args, routine_kwargs, cfg=cfg)

	# -------------------------------------------------------------------------
	# feed all the configuration parameters if the input keyword is correct
	roundup=cfg.get('-roundup', '_heron_')
	if   roundup in routine_args : sorted_args  [routine_args.index(roundup)] = cfg
	elif roundup in sorted_kwargs: sorted_kwargs[roundup] = cfg

	# a bit too risky, so not now
	# roundup=cfg.get('-roundupall', '__heron__')
	# if   roundup in routine_args : sorted_args  [routine_args.index(roundup)] = all
	# elif roundup in sorted_kwargs: sorted_kwargs[roundup] = all

	# -------------------------------------------------------------------------
	if 'feed' in show:
		jt.show_feed(routine_args, routine_kwargs, cfg['-main'], 
					inargs=sorted_args, inkwargs=sorted_kwargs)

	for each in cfg.get('-mkoutdir',[]): 
		target = path.dirname(cfg.get(each,''))
		if not path.exists(target): create_dir(target)

	if skip(cfg): return -1

	# -------------------------------------------------------------------------
	output_ = execute_routine(routine, sorted_args, sorted_kwargs, cfg=cfg, 
				show_out='output' in show)

	if 'time' in show: 
		runtime(start_time, datetime.now(), cfg['-main'], jobid='job '+str(taskkey), cc=cc)

	if '-return' in cfg:
		global output
		if type(output_) is not tuple: output_ = [output_]
		for idx, each in enumerate(cfg.get('-return','').replace(' ','').split(',')):
			if each not in output:
				output[each]=OrderedDict()
			# this needs a mod for rabbit's task generation
			output[each][cfg['-nid']] = output_[idx]
		return output
	else:
		return output_

	""" """

def go(cfgs=None, befores=None, afters=None, ovw=None, cli=sys.argv[1:], level=-1):
	global taskkey, mt_refer, maxtask, show

	if cfgs == None: cfgs, befores, afters, ovw = jt.load_cli(cli)
	if type(cfgs) is not list: cfgs=[cfgs]

	global_diagnostic(cfgs)

	# search for self containing rabbit and reconfig?
	# cfgs=jt.reconfig_to_alltaskgen(cfgs)

	level=level+1
	if level == 0:
		taskkey=0
		mt_refer=OrderedDict()
		maxtask=len(cfgs)

	start_time=datetime.now()

	for idx, each in enumerate(cfgs): 
		taskkey = taskkey+1

		each['-level' ] = level
		each['-jobc'  ] = taskkey
		each['-maxjob'] = maxtask

		out=execute(each)

		if type(befores) is list: before=befores[idx]
		else:				  before=befores
		if type(afters ) is list: after =afters [idx]
		else:				  after =afters 

		_, after_ = rb.get_common_vs_match(after)
		after_    = jt.merge(after_, ovw)

		# if each.get('-rabbit', False) >=True and type(out) is not bool:
		if 'rabbit' in each.get('-block', '') and type(out) is not bool:
			# id augmentation by level depth
			# a bit adhoc: too intertwined with internal steps of jt.load_cli
			# need a more clean break btw the two
			if len(out) == 0: continue

			maxtask=maxtask+len(out)

			for idx2, each2 in enumerate(out):
				# update the number and full id
				each2['-id'], each2['-nid'], each2['-fid'] \
						= jt.set_id(each2.get('-id',''), idx2+1, pref=each['-nid']+'.')

				# only applied selected cases in after?
				# other wise this supercede
				# what if one needs to apply globally?
				out[idx2] = jt.get_task_ready(each2, before, after_, doprocess=level+2)

			go(out, befores=before, afters=after, level=level)

	global show
	end_time=datetime.now()
	if 'time' in show: 
		runtime(start_time, end_time, '', jobid='job all', cc=cc)
	log(cfgs, start_time, end_time)

#----------------------------------------------------------------------------
def log(cfg, start_time, end_time):
	""" write a log
	"""
	# called at the end of the program
	# requires the directory name: set by _hisdir
	# the filename is automatically assigned by date_time, 
	# but can be set manually by _hisfile

	if cfg[0].get('-dryrun', False)   : return
	if cfg[0].get('-logfile','') == "": return

	if not cfg[0].get('-save_cli_only_run', False):
		if jt.json_counter == 0: return  
	
#	username = getuser()
	hostname = gethostname()

	try:
		cfg_str = json.dumps(cfg)
	except:
		print(cc.err+"cannot log this since serializing cfg failed"+cc.reset)
		return
	hashres = hashlib.sha1(cfg_str.encode())

	### ------
	for each in cfg:
		if '-main' in each:
			main_name = each['-main'][0]
			break
	lmain     = len(cfg)
	if lmain >0: main_name = main_name + '+'+str(lmain)
	loginfo = ['{}'.format(start_time)[2:19],'{}'.format(end_time - start_time),
#			'{}'.format(time)[0:19],
			'SHA1:'+hashres.hexdigest(),
			main_name, '', hostname, 
			'']
	loginfo = ' '.join(loginfo)

	logfile=path.expanduser(cfg[0]['-logfile'])
	if path.isfile(logfile): 
		lfile = open(logfile,"a")
		lfile.write('\n'+loginfo)
	else:                    
		lfile = open(logfile,"w")
		lfile.write(loginfo)
	lfile.close()

	### ------
	hisfile = cfg[0].get('-hisfile', None)
	if hisfile == None: return
	if hisfile == '_auto_':
		filename = start_time.strftime("%y%m%d_%H%M%S")+'_'+main_name+'.json5'
		hisfile = (Path(logfile).parent / Path(filename)).expanduser()

#	json.dump(cfg, open(hisfile,"w"))
	hfile = open(path.expanduser(hisfile),"w")
	hfile.write('//'+loginfo+'\n')
	hfile.write(cfg_str.replace(',',',\n\t'))
	hfile.close()

	""" """

def runtime(start_time, end_time, label, jobid='', cc=cc):
	print(cc.key+jobid+':','{}'.format(end_time - start_time), 
			cc.type+'{}'.format(start_time), 
			cc.key+label, cc.reset)

#----------------------------------------------------------------------------
def help_text(display=False, raw=False):
	""" print out the help text of cjpy and cjson
	"""

	display  = str(display)
	if 'True' in display:
		print("""Usage: clise JSON_input_file1 -options_for_file1 ... 
				[JSON_input_file2 -options_for_file2 ...] 
				[--with common_JSON_files -common_options ...]

		heron --help [keys]
		heron --help keys to see the list
		heron [JSON_files ...] --Help 
		heron --main module.routine --Help """.replace("\n\t\t","\n"))
		return True
	if 'False' in display: return False

	contents = OrderedDict()
	contents['heading'    ] = '### CLISe:'
	contents['contents'   ] = '### Table of Contents'
	contents['overview'   ] = '### Quick overview of the basic concept'
	contents['install'    ] = '### Installation and startup'
	contents['features'   ] = '### Features and limitation'
	contents['features'   ] = '### Features in parameter setting with JSON files'
	contents['iteration'  ] = '### Iterative calling and file search'
	contents['Sequential' ] = '### Sequential calling'
	contents['cli'	    ] = '### Options for command line parameters'
	contents['parameters' ] = '### Parameter list'
	contents['logging'    ] = '### Logging'
	contents['more'       ] = '### More'
	contents['changes'    ] = '### Changes'
	contents['end'        ] = ''
	keys = list(contents.keys())

	dir=path.dirname(__file__)
	rf = open(dir+'/doc/heron.md',"r")
	readme=rf.read()
	rf.close()

	if display == "all": display = keys[:-1]
	else:		         display = display.split(',')

	from rich.console import Console
	from rich.markdown import Markdown
	console = Console()

	for each in display:
		if each == "keys": 
			print(keys[:-1]+['all'])
			continue
		if each in keys:
			idx=keys.index(each)
			phrase='('+contents[each]+'.+)'+contents[keys[idx+1]]
			mat=re.search(phrase, readme, re.DOTALL)
			if not bool(mat): continue
			selected = mat.group(1)
			if raw: print(selected)
			else:   console.print(Markdown(selected))

	return True
	""" """

#----------------------------------------------------------------------------
def Help_text(cfg, what=None, keyword='-main', cc=cc):
	""" print out the Help text from the called routines
	    No argument: 
              if a single routine is called, then print out __doc__ of the routine
	        if multiple routines are called, list the modules and functions called
	    with an argument for a routine:
		  the print out __doc__ of the routine whose name is the same as argument 
		  this enables printing out any doc function 
	    with an argument for a module:
	         list all the functions of the module
		   this argument ends with .
	"""

	mdict, mlist = jt.extract(cfg, key=keyword)
	jt.show(mdict, full=True)
	if len(mlist) == 1:
		routine, module = load_routine(mlist[0], cfg=cfg)
		if routine.__doc__ == None: print('hmm, does not have any doc in', mlist[0])
		else:				    print(routine.__doc__.replace("\n\t","\n"))
	else:
		jt.show(mdict, full=True)
	
	if what == None: return True

	# forgot what's the point of all these.....
	if what in mlist:
		print(cc.key+what+cc.reset)
		routine, module = load_routine(what, cfg=cfg)
		if routine.__doc__ == None: print('hmm, does not have any doc in', what)
		else:				    print(routine.__doc__.replace("\n\t","\n"))
	else:
		if what[-1] == '.': 
			what=what[:-1]
			print('searching functions in module:', cc.key+what+cc.reset)

			from inspect import isfunction
			whats=what.split('.')
			if len(whats) >1:
				routine, module = load_routine(what, cfg=cfg)
			else:
				routine = __import__(what)
			members=dir(routine)
			for each in members: 
				if isfunction(getattr(routine, each)): print('	',each)
		else:
			print(cc.err+what,'is not called yet'+cc.reset)
			try:
				routine, module = load_routine(what, cfg=cfg)
				if routine.__doc__ == None: print('hmm, does not have any doc in', what)
				else:				    print(routine.__doc__.replace("\n\t","\n"))
			except:
				print(cc.err+"cannot load", what+cc.reset)

	return True
	""" """

def main():
	go()
#----------------------------------------------------------------------------
if __name__ == "__main__":
	""" in bash, use this program in this way
	    alias heron='python heron.py'

	    and then 
	    heron json_file [json_files ...] [-other parameters]

	    to run in ipython

	    import heron as hr
	    #	or if it's installed with pip
	    # import heron.heron as hr
	    # import heron.jsontool as jt

	    # run with one json file
	    cfg=jt.load_cli('cli_text')
	    out=hr.go(cfg)


	"""
	go()
	""" """



