# conversion json and command line parameters to functional input variables 
#	add more context to key definition
# Jaesub Hong

import json
#import pyjson5 as json5
import hjson   as hjson

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

# there must be a better way to do this...
if 'clise' in __file__:
	STARTUP  = 'CLISE_STARTUP'
	AUTO_GEN = 'clise.rabbit.multiply_by_file'
	MANU_GEN = 'clise.rabbit.multiply_by_id'
else:
	STARTUP  = 'HERON_STARTUP'
	AUTO_GEN = 'rabbit.multiply_by_file'
	MANU_GEN = 'rabbit.multiply_by_id'

#----------------------------------------------------------------------------
class cc: 
	""" color codes
	"""
	orange	 ="\033[38;2;190;165;0m"
	green		 ="\033[38;2;46;145;36m"
	pink		 ="\033[38;2;185;145;175m"
	red		 ="\033[38;2;230;0;0m"
	# steelblue	 ="\033[38;2;176;196;222m"
	steelblue	 ="\033[38;2;156;176;202m"
	darkgrey	 ="\033[38;2;90;90;90m"
	reset		 ="\033[38;2;160;160;160m"

	key   = orange
	type  = green
	reset = reset
	none  = darkgrey
	hl    = pink
	err   = red
	defs  = steelblue
	""" """

class tk:
	eval  = '#'
	float = '##'
	list  = '\*'
	sep   = ','
	dict  = '\*\*'
	json  = '='
	nest  = ':'
	neg   = '^'
	key   = '[#\*^]'
	vstart= '{'
	vstop = '}'

def str_to_list(input):
	if type(input) is str: return [input]
	else: return input

def extract(dict, key='-main', level='-top'):
	""" recursively extract the value for a key
	"""

	ans=OrderedDict()
	unique=OrderedDict()
	if key in dict.keys(): 
		ans[level] = dict[key]
		unique[ans[level]]=''


	for k,v in dict.items():
		if type(v) is not dict and type(v) is not OrderedDict: continue
		if level == '-top': cans, _ = extract(v, key=key, level=k)
		else:               cans, _ = extract(v, key=key, level=level+':'+k)

		for k_, v_ in cans.items():
			ans[k_] = v_
			unique[v_] =''
		
	unique = list(unique.keys())

	return ans, unique

	""" """

def simplify(value):
	if   value > 1099511627776:	return "{:.1f}".format(value/1099511627776)+'T'
	elif value > 1073741824:	return "{:.1f}".format(value/1073741824)+'G'
	elif value > 1048576:		return "{:.1f}".format(value/11048576)+'M'
	elif value > 1024:		return "{:.1f}".format(value/1024)+'k'
	else:					return str(value)
#----------------------------------------------------------------------------
def truekey(key, tk=tk.key):
	if type(key) is str: return re.sub(tk,'',key)
	else:			   return [re.sub(tk,'',k) for k in key]

def merge(base, add, onlynew=	False):
	# this doesn't deal with 
	#	sub dict parameters:  only when given with the special key: e.g., -k1:k2...
	#	value substitute:	    this could be messy
	#	special keys:	    easy? make sure the order

	if type(add).__name__ == 'NoneType': return base
	if len(add) == 0: return base
	add_keys      = list(add.keys())
	true_add_keys = truekey(add_keys)

	if not onlynew:
		for each in true_add_keys:
			idx       = true_add_keys.index(each)
			key       = add_keys[idx]
			base[key] = add[key]

		return base

	base_keys      = list(base.keys())
	true_base_keys = truekey(base_keys)

	for each in true_add_keys:
		if each not in true_base_keys:
			idx       = true_add_keys.index(each)
			key       = add_keys[idx]
			base[key] = add[key]

	return base

def merge_before(base, add):
	# this doesn't deal with 
	#	sub dict parameters:  only when given with the special key: e.g., -k1:k2...
	#	value substitute:	    this could be messy
	#	special keys:	    easy? make sure the order

	accept = str_to_list(base.get('-accept',True))  # bool or list of key names or matching reg expr
	reject = str_to_list(base.get('-reject',[]))    # list of key names or matching reg expr

	add_keys      = list(add.keys())
	true_add_keys = truekey(add_keys)

	base_keys      = list(base.keys())
	true_base_keys = truekey(base_keys)

	if type(accept) is list:
		if '--listed' in accept:
			accept.remove('--listed')
			accept = accept + list(base.keys())

		for each in accept: 
			if each in true_add_keys: 
				idx       = true_add_keys.index(each)
				key       = add_keys[idx]
				if key not in true_base_keys: base[key] = add[key]
			else:
				for each2 in true_add_keys:
					if bool(re.search(each, each2)):
						idx       = true_add_keys.index(each2)
						key       = add_keys[idx]
						if key not in true_base_keys: base[key] = add[key]
						break
		return base

	if '--listed' in reject:
		reject.remove('--listed')
		reject = reject + list(base.keys())

	if accept:
		for each2 in true_add_keys:
			acceptable=True
			for each in reject: 
				if bool(re.search(each, each2)): 
					acceptable=False
					break
			if acceptable:  
				idx       = true_add_keys.index(each2)
				key       = add_keys[idx]
				if key not in true_base_keys: base[key] = add[key]
	return base

def merge_after(base, add):
	# this doesn't deal with 
	#	sub dict parameters:  only when given with the special key: e.g., -k1:k2...
	#	value substitute:	    this could be messy
	#	special keys:	    easy? make sure the order

	accept = str_to_list(base.get('-accept',True))  # bool or list of key names or matching reg expr
	reject = str_to_list(base.get('-reject',[]))    # list of key names or matching reg expr

	add_keys      = list(add.keys())
	true_add_keys = truekey(add_keys)

	base_keys      = list(base.keys())
	true_base_keys = truekey(base_keys)

	if type(accept) is list:
		if '--listed' in accept:
			accept.remove('--listed')
			accept = accept + list(base.keys())

		for each in accept: 
			if each in true_add_keys: 
				idx       = true_add_keys.index(each)
				key       = add_keys[idx]
				base[key] = add[key]
				try:
					idx      = true_base_keys.index(each)
					okey	   = base_keys[idx]
					if okey != key: base.pop(okey)
				except:
					pass

			else:
				for each2 in true_add_keys:
					if bool(re.search(each, each2)):
						idx       = true_add_keys.index(each2)
						key       = add_keys[idx]
						base[key] = add[key]
						try:
							idx      = true_base_keys.index(each2)
							okey	   = base_keys[idx]
							if okey != key: base.pop(okey)
						except:
							pass
						break
		return base

	if '--listed' in reject:
		reject.remove('--listed')
		reject = reject + list(base.keys())

	if accept:
		for each2 in true_add_keys:
			acceptable=True
			for each in reject: 
				if bool(re.search(each, each2)): 
					acceptable=False
					break
			if acceptable:  
				idx       = true_add_keys.index(each2)
				key       = add_keys[idx]
				base[key] = add[key]
				try:
					idx      = true_base_keys.index(each2)
					okey	   = base_keys[idx]
					if okey != key: base.pop(okey)
				except:
					pass
	return base

# dict routines
def substitute_local(inp, pre=None, post='}', level=0):
	""" parameters starting with ^ and . are used to replace variables of the same names
	"""

	if pre == None:
		if   level ==-1:pre='{<'
		elif level ==0: pre='{'
		elif level ==1: pre='{>'
		else:		    pre='{>>'

	text=json.dumps(inp)

	keys  = list(inp.keys())
	tkeys = truekey(keys)

	for key, tkey in zip(keys, tkeys):
		if tkey == '': continue
		
		# to avoid the infinite loop, skip the self reference
		val = str(inp[key])
		if bool(re.search(pre+tkey+post,val)): continue

		new_text=text
		while True:
			text=new_text
			new_text=text.replace(pre+tkey+post,val)
			if new_text == text: break
	
	out=json.loads(text, object_pairs_hook=OrderedDict)
	return out
	""" """

def substitute_global_truekeys(inp, pre='{', post='}'):
	""" parameters starting with ^ and . are used to replace variables of the same names
	"""
	text=json.dumps(inp)

	merged=inp[0].copy()

	keys =[]
	for each in inp:
		keys  = keys+list(each.keys())
		merged = merge(merged, each)
	tkeys = truekey(keys)

	for key, tkey in zip(keys, tkeys):
		if tkey == '': continue
			
		# to avoid the infinite loop, skip the self reference
		val = str(merged[key])
		if bool(re.search(pre+tkey+post,val)): continue

		new_text=text
		while True:
			text=new_text
			new_text=text.replace(pre+tkey+post,val)
			if new_text == text: break
	
	out=json.loads(text, object_pairs_hook=OrderedDict)
	return out
	""" """

def substitute_global(inp, pre='{', post='}'):
	""" parameters starting with ^ and . are used to replace variables of the same names
	"""
	text=json.dumps(inp)

	merged=inp[0].copy()

	keys =[]
	for each in inp:
		keys  = keys+list(each.keys())
		merged = merge(merged, each)

	for key in keys:
			
		# to avoid the infinite loop, skip the self reference
		val = str(merged[key])
		key_=key.replace('*','\*') # to handle str -> dict conversion with **key
		if bool(re.search(pre+key_+post,val)): continue

		new_text=text
		while True:
			text=new_text
			new_text=text.replace(pre+key+post,val)
			if new_text == text: break
	
	out=json.loads(text, object_pairs_hook=OrderedDict)
	return out
	""" """

#----------------------------------------------------------------------------
def nested_key(cfg, key, val=None, sep=':', pop=True):
	""" simple par into a nested variable

	"""
	if val == None: val=cfg[key]

	itype=type(cfg)
	mat=re.search("^(.+)"+sep+"(.+)$",key)
	if not bool(mat): 
		cfg[key] = val
		return cfg

	if pop: cfg.pop(key, None)
	key, rest = mat.group(1, 2)

	if key not in cfg.keys(): cfg[key] = OrderedDict()

	cfg[key] = nested_key(cfg[key],rest,val=val, sep=sep)

	return cfg

def expand_nested(cfg, sep=":", pop=True):
	if sep == ''   : return cfg

	new=cfg.copy()
	for k, v in cfg.items():
		new = nested_key(new, k,sep=sep, pop=pop)
	return new

def correct_json_par(cfg, pre="=", pop=True):
	if pre == ''   : return cfg

	new=cfg.copy()
	for k, v in cfg.items():
		if type(v) is dict or type(v) is OrderedDict: 
			new[k]=correct_json_par(cfg[k], pre=pre, pop=pop)
			continue

		if k[0] == "=":
			new[k[1:]] = v
			if pop: del new[k]

	return new

def expand_dict(cfg, pre="\*\*", pop=True):
	if pre == ''   : return cfg

	new=cfg.copy()
	for k, v in cfg.items():
		if type(v) is dict or type(v) is OrderedDict: 
			new[k]=expand_dict(cfg[k], pre=pre, pop=pop)
			continue

		# this may leave some weird key, parameter pair
		# since it doesn't pop
		if type(v) is not str: continue

		mat=re.search("^([-]*)"+pre+"(.+)$",k)
		if not bool(mat): continue

		newk = mat.group(1)+mat.group(2)

		if not bool(re.search('^[\n\s]*{',v)): v='{'+v+'}'
		vals=hjson.loads(v, object_pairs_hook=OrderedDict)

		new[newk] = vals
		if pop: del new[k]

	return new

def expand_list(cfg, pre="\*", sep=",", pop=True):
	if pre == ''   : return cfg

	new=cfg.copy()
	for k, v in cfg.items():
		if type(v) is dict or type(v) is OrderedDict: 
			new[k]=expand_list(cfg[k], pre=pre, pop=pop)
			continue

		if type(v) is not str: continue

		mat=re.search("^([-]*)"+pre+"(.+)$",k)
		if not bool(mat): continue
		newk = mat.group(1)+mat.group(2)

		vals = v.split(sep)
		new[newk] = vals
		if pop: del new[k]

	return new

def to_float(k, v, pre='##'):
	mat=re.search("^([-]*)"+pre+"(.+)$",k)
	if not bool(mat): return k, v

	newk = mat.group(1)+mat.group(2)

	if type(v) is str:
		try:
			return newk, float(v)
		except ValueError:
			print(cc.key+'warning: enforcing floats failed for:',k, v,cc.reset)
			return newk, v
	elif type(v) is list:
		newv = []
		for ev in v:
			if type(ev) is not str: 
				newv.append(ev)
				continue
			try:
				newv.append(float(ev))
			except ValueError:
				print(cc.key+'warning: enforcing floats failed for:',k, ev,'in', v,cc.reset)
				newv.append(ev)
		return newk, newv
	else:
		print('warning: enforcing floats failed for:',k, v)
		return newk, v

def to_numeric_(k, v, pre='#'):

	mat=re.search("^([-]*)"+pre+"(.+)$",k)
	if not bool(mat): return k, v

	newk = mat.group(1)+mat.group(2)
	if type(v) is str:
		try:
			return newk, int(v)
		except ValueError:
			try:
				return newk, float(v)
			except ValueError:
				print(cc.key+'warning: enforcing numeric failed for:',k, v,cc.reset)
				return newk, v
	elif type(v) is list:
		newv=[]
		for ev in v:
			if type(ev) is not str: 
				newv.append(ev)
				continue
			try:
				newv.append(int(ev))
			except ValueError:
				try:
					newv.append(float(ev))
				except ValueError:
					print(cc.key+'warning: enforcing numeric failed for:',k, ev,'in', v,cc.reset)
					newv.append(ev)
		return newk, newv
	else:
		print(cc.key+'warning: enforcing numeric failed for:',k, v,cc.reset)
		return newk, v

def to_numeric(k, v, pre='#', float=False):

	mat=re.search("^([-]*)"+pre+"(.+)$",k)
	if not bool(mat): return k, v

	newk = mat.group(1)+mat.group(2)
	if type(v) is str:
		try:
			if float: v=v+"*1.0"
			return newk, eval(v)
		except ValueError:
			print(cc.key+'warning: enforcing numeric failed for:',k, v,cc.reset)
			return newk, v
	elif type(v) is list:
		newv=[]
		for ev in v:
			if type(ev) is not str: 
				newv.append(ev)
				continue
			try:
				if float: ev=ev+"*1.0"
				newv.append(eval(ev))
			except ValueError:
				print(cc.key+'warning: enforcing numeric failed for:',k, ev,'in', v, cc.reset)
				newv.append(ev)
			except NameError:
				newv.append(ev)
		return newk, newv
	else:
		print(cc.key+'warning: enforcing numeric failed for:',k, v, cc.reset)
		return newk, v

def enforce_numeric(cfg, 
		pre4n="#",	# prefix for number (integer and floats)
		pre4f='##', # prefix for floats
		pop=True):
	if pre4n == False and pre4n == None or pre4n == '': return cfg

	new=cfg.copy()
	for k, v in cfg.items():
		if type(v) is dict or type(v) is OrderedDict: 
			new[k]=enforce_numeric(cfg[k], pre4n=pre4n, pre4f=pre4f, pop=pop)
			continue

		if pre4f !=None and pre4f != "":
			newk, newv = to_numeric(k, v, pre=pre4f, float=True)
			if k != newk:
				new[newk] = newv
				if pop: del new[k]
				continue

		newk, newv = to_numeric(k, v, pre=pre4n)
		if k == newk: continue
		new[newk] = newv
		if pop: del new[k]
		continue

	return new

def enforce_format(cfg, enforcer=None):

	if enforcer == None: return cfg
	new=cfg.copy()
	for k, v in enforcer.items():
		if k not in cfg.keys(): continue

		if type(v) is dict or type(v) is OrderedDict: 
			new[k]=enforce_format(cfg[k], enforcer[k])
			continue

		if type(cfg[k]) is list:
			try:
				if   v ==     'int': new[k] = [    int(ev) for ev in cfg[k]]
				elif v ==   'float': new[k] = [  float(ev) for ev in cfg[k]]
				elif v ==    'bool': new[k] = [   bool(ev) for ev in cfg[k]]
				elif v == 'complex': new[k] = [complex(ev) for ev in cfg[k]]
				elif v ==     'str': new[k] = [    str(ev) for ev in cfg[k]]
			except ValueError:
				print(cc.key+'enforcing type',v,'failed for', k+ ':', cfg[k], cc.reset)
				exit()
		else:
			try:
				if   v ==     'int': new[k] =     int(cfg[k])
				elif v ==   'float': new[k] =   float(cfg[k])
				elif v ==    'bool': new[k] =    bool(cfg[k])
				elif v == 'complex': new[k] = complex(cfg[k])
				elif v ==     'str': new[k] =     str(cfg[k])
			except ValueError:
				print(cc.key+'enforcing type',v,'failed for', k+ ':', cfg[k], cc.reset)
				exit()

	return new

def update_specific(cfg, only):
	new = cfg.copy()
	if only != None:
		for k, v in only.items():
			if k not in cfg.keys(): new[k] = only[k]
			elif type(v) is dict or type(v) is OrderedDict: 
				newv = new[k] if k in new.keys() else OrderedDict()
				for ek in v.keys() - newv.keys(): newv[ek] = v[ek]
				new[k] = newv
	return new

def routine_specific(cfg):

	if '-main' not in cfg: return cfg
	routine = cfg['-main']

	# ignore this if multiple mains are called, for now
	if type(routine) is not str: return cfg
	new = cfg.copy()

	for k, v in cfg.items():
		if not bool(re.search('^--only for ',k)): continue

		levels = routine
		while levels !='':
			if bool(re.search('^'+k,'--only for '+levels)): 
				new=update_specific(new, cfg[k].copy())
				break
			levels='.'.join(levels.split('.')[:-1])

		del new[k]
	

	return new
	
def discard(cfg, pop=True):
	discard=cfg.get('-discard',[])
	if type(discard) is not list: discard = [discard]
	for each in discard: cfg.pop(each, None)
	if pop: cfg.pop('-discard', None)
	return cfg

def nonify(cfg, pop=True):
	nonify=cfg.get('-nonify',[])
	if type(nonify) is not list: nonify = [nonify]
	for each in nonify: cfg[each] = None
	if pop: cfg.pop('-nonify', None)
	return cfg

def process_cfg(cfg, level=0, ignore_main=False):

	cfg=cfg.copy()

	# order 3
	# load default parameters
	if '-load' in cfg.keys():
		if type(cfg['-load']) is str: cfg['-load']=cfg['-load'].split(':')
		# note: this should be reversed in order 
		for each in cfg['-load'][::-1]:
			each = path.expanduser(each)
			if not path.isfile(each): 
				print('file not found for -load:',each)
				continue
			cfg_=load_file(each)
			for each2 in cfg_:
				cfg =merge(cfg, each2, onlynew=True)

	# order 2
	# startup file or other load file with
	# "--only for ..." key
	cfg = routine_specific(cfg)

	# start up file
	# order 1
	startup = getenv(STARTUP) 
	if startup != None:
		startup=startup.split(':')
		# note: this should be reversed in order 
		for each in startup[::-1]:
			each = path.expanduser(each)
			if not path.isfile(each): 
				print('file not found for', STARTUP+':',each)
				continue
			cfg_=load_file(each)
			for each2 in cfg_:
				cfg =merge(cfg, each2, onlynew=True)

	if not ignore_main:
		if "-main" not in cfg: return cfg

	pop = cfg.get('-pop_modifier',True)
	# order 4
	# expand a string value to a dict, useful for cmdline or json file
	# -*key '"val1":1,"val2":2,... => "key": {"val1":1,"val2":2,..]
	cfg = expand_dict(cfg, pop=pop, 
			 pre=cfg.get('-dict_pre',tk.dict))

	# order 5
	# expand a key to a nested dict or OrderedDict from cmdline or json file
	# useful for cmdline, and adding parameters to an existing dict or OrderedDict
	# -k1:k2 val => "k1": { "k2": val}
	cfg = expand_nested(cfg, pop=pop, 
			   sep=cfg.get('-expand_nested',tk.nest))

	# order 6
	# expand a string value to a list, useful for cmdline or json file
	# -*key val1,val2,... => "key": [val1,val2]
	cfg = expand_list(cfg, pop=pop, 
			pre=cfg.get('-list_pre',tk.list),
			sep=cfg.get('-list_sep',tk.sep))


	cfg = correct_json_par(cfg, pop=pop,
			pre=cfg.get('-json_pre',tk.json))

	# order 7
	# substitution?
	cfg = substitute_local(cfg, level=level)

	# order 8
	# enforce numeric parameter from cmdline or json file
	# -#key "12.34" => "key": 12.34
	cfg = enforce_numeric(cfg, pop=pop,
			pre4n=cfg.get('-enforce_numeric',tk.eval),
			pre4f=cfg.get('-enforce_floats',tk.float))

	# order 9
	cfg = enforce_format(cfg, 
			enforcer =cfg.get('-enforce_format',None))

	# order 10
	# either delete variables or set them None
	cfg = discard(cfg, pop=False)
	cfg = nonify (cfg, pop=False)

	return cfg 

#----------------------------------------------------------------------------
# reconfig a single task
def reconfig_to_taskgen(cfg, id=''):

	if type(id) is str: auto = True
	else:			  auto = False

	temp = cfg.get('-loop',OrderedDict()).copy()
	cfg.pop('-loop',None)
	temp[cfg.get('-seed_key','seed')] = cfg.copy()
	cfg = temp

	if '-main' not in cfg: 
		if auto: cfg['-main'] = AUTO_GEN
		else:	   cfg['-main'] = MANU_GEN

	# cfg['-rabbit']=cfg.get('-rabbit',True)
	cfg['-block']=cfg.get('-block','rabbit')
	return cfg

# reconfig all task
def reconfig_to_alltaskgen_(cfgs, id=''):
	inloop=False
	looped=[]
	for each in cfgs[:]: 
		# if each.get('-rabbit',False) > True:
		if 'release' in each.get('-block',''):
			new=each.copy()
			new['-block']='rabbit'	# clean up now
			seed=[]
			inloop=True
			looped.append(new)
		elif inloop:
			# if each.get('-rabbit',False) < False:
			if 'capture' in each.get('-block',''):
				ceach=each.copy()
				ceach['-block']=''	# clean up now
				seed.append(ceach)
				new['seed'] = seed
				inloop=False
			else:
				seed.append(each.copy())
		else:
			looped.append(each)
			
	return looped

def reconfig_to_alltaskgen(cfgs, id=''):
	inloop=False
	looped=[]
	# need to be more natural and systematic in future
	k1 = '-apply until -block'
	k2 = '>> -block'
	for each in cfgs[:]: 
		# if each.get('-rabbit',False) > True:
		# if 'rabbit' in each.get('-block','') or \
		if '-main' in each and (k1 in each or k2 in each):
		# if '-main' in each and bool(re.search('(-apply until|>>)( -block)', each)):
				new=each.copy()
				new['-block']='rabbit'	# clean up now
				if k1 in each: apply_until = new[k1]
				else:		   apply_until = new[k2]
				seed=[]
				inloop=True
				looped.append(new)
		elif inloop:
			# if each.get('-rabbit',False) < False:
			if apply_until in each.get('-block',''):
				ceach=each.copy()
				ceach['-block']=''	# clean up now
				seed.append(ceach)
				new['seed'] = seed
				inloop=False
			else:
				seed.append(each.copy())
		else:
			looped.append(each)
			
	return looped

def matchID(cid, cfg, matkey='-id'):
	""" case match for a given parameter, and reset other parameters accordingly
	This is targeted for CLI only.
	"""

	if cid == '': return cfg

	ans = cfg.copy()
	regex = '(==|!=|~=|~!=)'

	for k, v in cfg.items():
		mat=re.search(matkey+regex+'(.*)',k)
		if not bool(mat): continue

		matype = mat[1]

		mat_=re.search('(.*):(.*)',mat[2])
		if bool(mat_):
			# this is likely cli
			phrase = mat_[1]
			newkey = mat_[2]

			if matype == '==': 
				if cid == phrase: ans[newkey] = ans[k]
			elif matype == '!=': 
				if cid != phrase: ans[newkey] = ans[k]
			elif matype == '~=': 
				if bool(re.search(phrase, cid)): ans[newkey] = ans[k]
			elif matype == '~!=': 
				if not bool(re.search(phrase, cid)): ans[newkey] = ans[k]

		else:
			# this is likely from a file, v should be dictionary
			phrase = mat[2]

			feedit=False
			if matype == '==': 
				if cid == phrase: feedit=True
			elif matype == '!=': 
				if cid != phrase: feedit=True
			elif matype == '~=': 
				if bool(re.search(phrase, cid)): feedit=True
			elif matype == '~!=': 
				if not bool(re.search(phrase, cid)): feedit=True

			if feedit:
				for each in v: ans[each] = v[each]


		ans.pop(k)

	return ans

def matchblock(source, target, tk_word='apply to', tk_symbol='>>', ifnone=True):
	merge=False
	apply=[]
	# perhaps natural and systematic enough?
	for skey in source:
		mat=re.search('('+tk_word+'|'+tk_symbol+') (.*)(| except| contains| without| ==| !=| ~=| ~!=)',skey)
		if not bool(mat): continue
		apply.append(skey)
		tkey = mat.group(2)
		if tkey not in target: continue

		# source[sky] can be string or string list
		if mat.group(3) == "" or mat.group(3) == " ==":
			if target[tkey] in source[skey]: merge=True
		if mat.group(3) == " except" or mat.group(3) == " !=":
			if target[tkey] not in source[skey]: merge=True

		# source[sky] is assumed to be string
		if mat.group(3) == " contains" or mat.group(3) == " ~=":
			if type(source[skey]) is not str: 
				print(cc.err+'expect a regex string for', skey, source[skey],cc.reset)
				continue
			if bool(re.search(source[skey],target[tkey])): merge=True

		if mat.group(3) == " without" or mat.group(3) == " ~!=":
			if type(source[skey]) is not str: 
				print(cc.err+'expect a regex string for', skey, source[skey],cc.reset)
				continue
			if not bool(re.search(source[skey],target[tkey])): merge=True

	if ifnone:
		if len(apply) == 0: merge=True 
	return merge, apply

def defaults(cfg):
	cfg['-verbose'] = cfg.get('-verbose',0)
	cfg['-clobber'] = cfg.get('-clobber',False)
	return cfg

def get_task_ready(task, before, after, 
			 matval=None, matkey=['-id','-main','-nid','-fid'], doprocess=True):

	if matval ==None: 
		matval = []
		for each in matkey: matval.append(task.get(each,''))

	filtered_before=OrderedDict()
	for ckey, cmat in zip(matkey, matval):
		filtered_before = merge(filtered_before, matchID(cmat, before, matkey=ckey))

	filtered_after=OrderedDict()
	for ckey, cmat in zip(matkey, matval):
		filtered_after = merge(filtered_after, matchID(cmat, after, matkey=ckey))

	task   = merge_before(task, filtered_before)
	task   = merge_after (task, filtered_after )

	task   = defaults(task)
	if doprocess: return process_cfg(task, level=doprocess-1)
	else:         return task

def set_id(short, counter, pref=''):
	nid = f"{counter:02}"
	#   short id: there can be duplicate for this
	# numeric id: no duplicate is possible
	#    full id:
	return short, pref+nid, pref+nid+':'+short

#----------------------------------------------------------------------------
json_counter = 0

def load_file(file, astext=False):
	""" read json file, add proper beginning and brackets, and remove trailing ","
	"""
	out=OrderedDict()
	try:
		jsonfile=open(file)
		text=jsonfile.read()
		jsonfile.close()
	except FileNotFoundError:
		print(cc.err+'file not found:',file,cc.reset)

	# add beginning and ending {} if missing
	# if it has {}, it's either multiple sets or single complete set
	ready=True
	if not bool(re.match('[\n\s]*[{\[]',text)): 
		# this is designed for merge or single set as the main input
		text='{'+text+'}'
		# ready=False # essentially maybe

	if not bool(re.match('[\n\s]*[\[]', text)): text='['+text+']'

	# now get rid of trailing ","
	text=re.sub(r',([\n\s]*)([}\]])',r'\1\2',text)
	if astext: return text

	try:
		out=hjson.loads(text, object_pairs_hook=OrderedDict)
		out=substitute_global(out)
	except ValueError as ve:
		print(cc.err+'The file',file,'failed parsing!')
		print(ve,cc.reset)
		exit()

	# if not ready:
		# if '-main' in out[0]: ready=True

	return out#, ready
	""" """

def group_cli(cli=sys.argv[1:]):
	""" group the cli sets
	the main function, enables a series of runs 
	"""

	# cli=sys.argv[1:]

	if type(cli) is not list: cli=cli.split()

	# lower priority: set with --with
	mergefile=[] # common json file set
	merge_cli=[] # common command line
	
	# normal priority: supercede mergefile, and merge_cli
	stackfile=[] # json file set
	stack_cli=[] # command line for each json

	# high priority: supercede stackfile, stack_cli, set with --WITH
	overwfile=[] # json file set
	overw_cli=[] # command line for each json

	# order in CLISE 
	# clise stack* .... --with merge* .... --WITH overw* ...

	parse = True
	if '-^-parse'    in cli: parse=False
	if '--^parse'    in cli: parse=False

	ext ='(json|json5|hjson|jsonc)'
	expr="^[^-{].*\."+ext+"$"

	prev_par = "^-=[a-zA-Z]"

	# The extended JSON format is used to feed the input parameters
	# since it is easy to convert to a python dictionary.
	# Check for JSON, JSON5, JSONC, HJSON files for now:
	# The accepted format allows a simple math expr using python's
	# eval function with '<', '>'.
	# Since JSON is not exactly optimized for configuration files,
	# in future perhaps other configuration file formats will are accepted as
	# well: e.g., yaml?
	# Note the format without the outer most brackets '{',''}' like in JSON5 is
	# allowed to simulate a more config-like file, but this violates the JSON
	# syntax set by LSP, which can be annoying for some editors. 

	# check common variables

	if '--WITH' in cli: 
		idx=cli.index('--WITH')
		for par in cli[idx+1:]:
			if bool(re.search(expr,par)): overwfile.append(par)
			else:                         overw_cli.append(par)
		cli=cli[0:idx]

	if '--with' in cli: 
		idx=cli.index('--with')
		for par in cli[idx+1:]:
			if bool(re.search(expr,par)): mergefile.append(par)
			else:                         merge_cli.append(par)
		cli=cli[0:idx]

	# run one by one
	# need to fix this for command line version
	orphan=[]
	expect_jsfile = False
	for par in cli:
		if bool(re.search(expr,par)) and parse and not expect_jsfile:
			stackfile.append(par)
			new=[]
			stack_cli.append(new)
		else:
			try:
				new.append(par)
			except NameError:
				orphan.append(par)

		if bool(re.search(prev_par,par)): expect_jsfile=True


	if len(stackfile) == 0:
		return [orphan+mergefile+merge_cli+stack_cli], overwfile+overw_cli

	cli_sets=[]
	for eachfile, each_cli in zip(stackfile, stack_cli): 
		cli_sets.append(orphan+mergefile+[eachfile]+merge_cli+each_cli)
		# now eachfile can have multiple tasks

	return cli_sets, overwfile+overw_cli
	""" """

def analyze_cli(cli):
	""" for a given cli set, get the cfg sets
	since the main cjson file can have multiple sets
	"""

	cfg_cli = OrderedDict() # current cli cfg

	potential=False # could be potentially not a boolean parameter
	jsonpar=[]

	for par in cli:
		# dela with negation operator '^'
		mat=re.search("^-([^0-9].*)",par)
		if bool(mat):
			key=mat.group(1)
			# first deal with -^key or -^-key
			matneg=re.search("^\^(.+)",key)
			if bool(matneg):
				key=matneg.group(1)
				cfg_cli[key] = False
			else:
				# second deal with --^key, which is the same as -^-key
				matneg2=re.search("^-\^(.+)",key)
				if bool(matneg2): 
					key='-'+matneg2.group(1)
					cfg_cli[key] = False
				else:
					cfg_cli[key] = True
					potential=True
		else:
			# now we assume everything else is value for a key or json (either par or file)
			# which include a negative number
			# so keys like -5a are not allowed, which may cause an error or
			# taken as value of a key
			if potential:
				cfg_cli[key]=par
				potential=False
			else:
				# these are json
				jsonpar.append(par)

	# handle json file or json format parameter
	before = OrderedDict() # before base
	after  = OrderedDict() # after base
	base   = []	        # these are the base sets
	shared = []	        # these are blocks shared for some
	# jsonfiles =[]
	global json_counter
	for par in jsonpar:
		mat=re.search("^{(.+)",par)
		if bool(mat):
			cfg_=hjson.loads(par, object_pairs_hook=OrderedDict)
			for key in cfg_: cfg_cli[key]=cfg_[key]
		else:
			# cfg_file, ready=load_file(par)
			# jsonfiles.append(par)
			# ncfg=len(cfg_file)
			# if not ready:
			# 	if len(base) == 0: before=merge(before, cfg_file[0])
			# 	else:			 after =merge(after , cfg_file[0])
			# else:
			# 	base = base + cfg_file
			json_counter=json_counter+1
			cfg_file=load_file(par)
			cfg_file=reconfig_to_alltaskgen(cfg_file)
			for each in cfg_file:
				# need to be more natural and systematic?
				# esp need to absorp seed block for task gen, 
				# then we don't need this rabbit part
				# the challenge is this part might not be ready for reconfig...
				# we can force one file contains the full list of task gen
				# if '-main' not in each and 'rabbit' not in each.get('-block',''):
				# downside is CLI options may not easily go in here...
				if '-main' not in each:
					# the latter is common block for rabbit's task gen, 
					# so don't separate out
					shared = shared + [each]
				else:
					base = base + [each]


	after = merge(after, cfg_cli)
	# feed cfg_cli to task_gen seed if requested
	# this should have some option: use accept and reject?
	k1 = '-apply until -block'
	k2 = '>> -block'
	for each in base:
		if '-main' in each and (k1 in each or k2 in each):
			seed=each.get('seed',[OrderedDict()])
			seed=seed+[cfg_cli]
			each['seed']=seed


	# -main is given by the cli
	if len(base) == 0: 
		if '-main' in after: 
			base=[after]
			after=OrderedDict()
		elif '-main' in before: 
			base=[before]
			before=OrderedDict()
		else:
			after = merge(after, before)
			base = [after] # this should be a simple task run

	return base, before, after, shared

def load_cli(cli=sys.argv[1:]):
	cli_sets, cli_ovw = group_cli(cli)
	if len(cli_ovw) >0:
		ovw_base, *_ = analyze_cli(cli_ovw) 
		ovw_base = ovw_base[0]
	else: ovw_base = OrderedDict()
	cfgs    = []
	befores = []
	afters  = []
	itask= 0
	for cli in cli_sets:
		base, before, after, shared = analyze_cli(cli) # a bit of redundancy
		# base=reconfig_to_alltaskgen(base)
		for task in base:

			# assign -id 
			if '-main' in task:
				# if '-loop' in task or type(id) is not str:
				if '-loop' in task:
					# task generator routine
					id = task.get('-id','')
					task=reconfig_to_taskgen(task, id=id)

					# set basic id
					name=task['-main'].split('.')[-1]
					task['-id'], task['-nid'], task['-fid'] = set_id(name, itask+1)

					# need to handle -id match
					task = get_task_ready(task, before, after, doprocess=False)

					# feed cli to generated tasks
					# some task generator will do actual io in addition to pushing around
					# the variables, the parameters have to be real: i.e., doprocess=True
					task['seed'] = get_task_ready(task['seed'], before, after, 
						    matval=task['-id'], doprocess=True)

					task = process_cfg(task)
				else:

					# now check shared ones for common
					for share in shared:
						merge, apply = matchblock(share, task)
						if merge:
							# clean up keys with -apply to ...
							share_=share.copy()
							for each in apply:
								if each in share_: del share_[each]
							task = merge_before(task, share_)
							task = substitute_local(task, level=-1)

					# this is a regular routine
					id = task.get('-id','')
					if id == '': name=task['-main'].split('.')[-1]
					else:		 name=task['-id']
					task['-id'], task['-nid'], task['-fid'] = set_id(name, itask+1)

					# need to handle -id match
					task = get_task_ready(task, before, after, doprocess=True)
			else:
				if len(base) == 1:
					# this is a (only) regular routine
					task = defaults(task)
					task = process_cfg(task, ignore_main=True)
				else:
					# now this is a partial block that needs to be distributed
					# perhaps right now it never gets here?
					pass
					# embed()

			skip=False
			for share in shared:
				skip, apply = matchblock(share, task, tk_word='skip', tk_symbol='<<', ifnone=False)
				if skip: break

			if skip: continue

			cfgs    .append(task)
			befores .append(before)
			afters  .append(after)

			itask=itask+1

	return cfgs, befores, afters, ovw_base

#----------------------------------------------------------------------------
def show_(dict, ref=None, tab=0, cc=cc, full=False, 
		notype=False, hidden='-', exceptions=['-prep','-post']):
	""" show input parameters
	"""

	do=False
	if len(dict) == 0: do=True

	if do:
		keys   = dict.keys()
		if len(keys) == 0: return
		types  = [type(each).__name__ for each in dict.values()]
		values = dict.values()
		strval = [str(each) for each in dict.values() 
				if type(each) is not dict and type(each) is not OrderedDict]

		maxkey   = len(max(keys,   key=len))
		maxtype  = len(max(types,  key=len))
		maxvalue = len(max(strval, key=len))
		if maxvalue > 50: maxvalue=50
	else:
		maxtype = 6
		maxvalue = 6

	doref=False
	if ref != None:
		lenref=len(ref)
		if lenref > 0: doref=True

	# nothing to do
	if not do and not doref: return

	if doref:
		reftypes   = [type(each).__name__ for each in ref.values()]
		maxreftype = len(max(reftypes, key=len))
		if not do:
			maxkey= len(max(ref.keys(), key=len))

	tab_ = ''.rjust(tab)
	if notype: nextab=tab+maxkey+5
	else:	     nextab=tab+maxkey+maxtype+5

	if do:
		for key, typ, value in zip(keys, types, values):
			cckey =cc.key
			if key[0:1] == hidden: 
				cckey= cc.defs
				if not full: 
					if key not in exceptions: continue

			key_ = tab_+cckey+key.rjust(maxkey+1)

			if typ == 'NoneType': 
				typ_   = cc.none + typ.ljust(maxtype)
				value_ = cc.none + str(value).ljust(maxvalue)
			else:
				typ_   = cc.type  + typ.ljust(maxtype)
				value_ = cc.reset + str(value).ljust(maxvalue)

			if typ == 'dict' or typ == 'OrderedDict':
				if notype:	
					print(key_, cc.reset)
					maxtype=0
				else:		print(key_, typ_, cc.reset)
				cref=None
				if doref:
					if key in ref.keys(): cref=ref[key]
				show(value, tab=nextab, full=full, ref=cref, notype=notype)
				continue

			if typ == 'list':
				if len(value) >0:
					if type(value[0]).__name__ == 'dict' or type(value[0]).__name__ == 'OrderedDict':
						if notype: print(key_,  cc.reset,'[')
						else:      print(key_, typ_, cc.reset,'[')
						for each in value:
							cref=None
							if doref:
								if key in ref.keys(): cref=ref[key]
							show(each, tab=nextab, full=full, ref=cref, notype=notype)
							if each != value[-1]:
								print(tab_+','.rjust(maxkey+3+maxtype*(1-notype)))
						print(tab_+']'.rjust(maxkey+3+maxtype*(1-notype)))
						continue

			if doref:
				if key in ref.keys():
					reftype = type(ref[key]).__name__
					if reftype == 'NoneType': 
						reftype = cc.none  + reftype.ljust(maxreftype)
						refval  = cc.none  + str(ref[key])
						feed    = cc.none + '<<'
					else:
						if reftype != typ and typ != 'NoneType':
							reftype = cc.hl   + reftype.ljust(maxreftype)
						else:
							reftype = cc.type + reftype.ljust(maxreftype)
						feed   = cc.reset + '<<'
						refval = cc.reset + str(ref[key])

					if notype: 
						print(key_, value_, feed, refval, cc.reset)
					else:      
						print(key_, typ_, value_, feed, reftype, refval, cc.reset)
			else:
				if notype: print(key_, value_, cc.reset)
				else:      print(key_, typ_,  value_, cc.reset)
	
	if doref:
		typ_   = cc.err + '?'.rjust(maxtype)
		value_ = cc.err + '?'.ljust(maxvalue)
		if do: keys = ref.keys() - dict.keys()  # why does this keep changing the order???
		else:  keys = ref.keys()
		for key in keys:
			key_ = tab_+cc.key+key.rjust(maxkey+1)
			reftype = type(ref[key]).__name__

			if reftype == 'dict' or reftype == 'OrderedDict':
				print(key, reftype, cc.reset)
				cref=None
				show(OrderedDict(), tab=nextab, full=full, ref=ref[key], notype=notype)
				continue

			if reftype == 'NoneType': 
				reftype = cc.none  + reftype.ljust(maxreftype)
				refval  = cc.none  + str(ref[key])
				feed    = cc.none + '<<'
			else:
				reftype = cc.hl   + reftype.ljust(maxreftype)
				feed   = cc.reset + '<<'
				refval = cc.reset + str(ref[key])
			if notype: 
				print(key_, value_, feed, refval, cc.reset)
			else:      
				print(key_, typ_, value_, feed, reftype, refval, cc.reset)


	""" """

from rich import box
from rich.console import Console
from rich.table import Table

console = Console()
def show(input_, ref=None, hidden='-', level=0, tab=0, notype=False, maxkey=1, maxtype=1, full=False):
	if len(input_) == 0: return

	if not full: input_ = { k: v for k, v in input_.items() if k[0] != '-'}
	input=input_.copy()
	
	keys    = list(input.keys())
	if len(keys) == 0: return
	types   = [type(each).__name__ for each in input.values()]
	types   = ['odict' if v == 'OrderedDict' else v for v in types]

	maxkey_ = len(max(keys,   key=len))
	maxtype_= len(max(types,  key=len))
	if maxkey  < maxkey_  : maxkey =maxkey_
	if maxtype < maxtype_ : maxtype=maxtype_
	
	space = ' '*tab

	table = Table(show_footer=False, show_header=False, show_edge=False)
	table.add_column('depth' ,  no_wrap=True)

	table.add_column("key"   ,  no_wrap=True)
	table.columns[1].width = maxkey
	table.columns[1].style = "bold dim yellow"
	table.columns[1].justify = "right"

	if notype:
		table.add_column("value" , no_wrap=False)
		table.columns[2].style = "dim white"
	else:
		table.add_column("type"  ,  no_wrap=True)
		table.columns[2].style = "green"
		table.columns[2].width = maxtype

		table.add_column("value" , no_wrap=False)
		table.columns[3].style = "dim white"

	table.border_style = None
	table.box          = None
	table.pad_edge     = False

	child = None
	# for k, v in input_.items():
	for k, t, v in zip(keys, types, input_.values()):

		if k[0] == hidden: k_='[cyan]'+k+'[/cyan]'
		else:              k_=k

		if t == 'dict' or t == 'odict': 
			if notype: table.add_row(space, k_, '')
			else:      table.add_row(space, k_, t, '')
			child = v.copy()
			isdict = True
			del input[k]
			break
		elif t == 'list':
			if len(v)>0:
				if type(v[0]).__name__ == 'dict' or type(v[0]).__name__ == 'OrderedDict':
					if notype: table.add_row(space, k_, ']')
					else:      table.add_row(space, k_, t, '[')
					child = [ev.copy() for ev in v]
					isdict = False
					del input[k]
					break
		
		if notype: table.add_row(space, k_, str(v))
		else:	     table.add_row(space, k_, t, str(v))
		del input[k]

	# table.width        = console.measure(table).maximum
	console.print(table)

	if child !=None: 
		level_ =level+1
		tab_   =tab+maxkey+2+(maxtype+2)*(1-notype)
		if isdict: show(child, ref=ref, hidden=hidden, level=level_, tab=tab_, notype=notype, full=full)
		else: 
			tab_   =tab_+3
			for v in child:
				show(v, ref=ref, hidden=hidden, level=level_, tab=tab_, notype=notype, full=full)
				if v != child[-1]: print(','.rjust(tab_))
				else:			 print(']'.rjust(tab_))
	if len(input)>0: show(input, ref=ref, hidden=hidden, level=level, maxkey=maxkey, maxtype=maxtype, 
			     tab=tab, notype=notype, full=full)

def show_feed(args, kwargs, name, inargs=[], inkwargs=OrderedDict(), cc=cc):

	# print(' main:',cc.key+name+cc.reset)
	print(' main:',cc.key+name+cc.reset)
	ninargs=len(inargs)
	ninkwargs=len(inkwargs)

	if len(args) >0:
		if 'self' in args: args=args[1:]
		if len(args) > 0:
			maxargs = len(max(args, key=len))

	if ninargs > 0:
		types   = [type(each).__name__ for each in inargs]
		maxtype = len(max(types, key=len))

	for i, each in enumerate(args):
		arg_ = cc.hl +each.rjust(maxargs+1)

		if i >= ninargs: 
			print(arg_,cc.reset)
			continue
		if types[i] == 'NoneType': 
			feed  = cc.none+'<<'
			type_ = cc.none+types[i].ljust(maxtype)
			inarg_= cc.none+str(inargs[i])
		else:
			feed  = cc.reset+'<<'
			type_ = cc.type+types[i].ljust(maxtype)
			inarg_= cc.reset+str(inargs[i])

		print(arg_+cc.reset,feed, type_, inarg_, cc.reset)
	
	show_(kwargs, ref=inkwargs, cc=cc)

def show_files(input, cc=cc):
	""" show files
	"""

	checkin  = input.get('-checkin',[])
	checkout = input.get('-checkout',[])
	if type(checkin)  is str: checkin  =[checkin]
	if type(checkout) is str: checkout =[checkout]
	check    = checkin + checkout
	lcheck   = len(check)
	if lcheck == 0: 
		# print(cc.key+'No files to check',cc.reset)
		return

	maxlen=max([len(input.get(v,'')) for v in check])

	# this is not a regular parameter for heron or jsontool any more
	if input.get('-basedir', None) != None:
		print('-basedir'.rjust(maxlen)+':',input['-basedir'])

	for k in check:
		if k not in input: print(cc.key+'No key named',k,'in inputs',cc.reset)

		# k_ = k.rjust(maxlen)
		k_ = k
		if k not in input: 
			print(cc.key+k,'is not in input',cc.reset)
			continue
		if path.isfile(input[k]):
			modtime = Path(input[k]).expanduser().stat().st_mtime
			size    = Path(input[k]).expanduser().stat().st_size
			regtime = str(datetime.fromtimestamp(modtime))[2:19:]
			if k in checkin:
				print(cc.key+k_+':', regtime,cc.reset+simplify(size).rjust(6),input[k])
			else:
				if input.get('-clobber',True):
					print(cc.err+'overwriting',k_+':', regtime,cc.reset+simplify(size).rjust(6), input[k])
				else:
					print(cc.key+k_+':', regtime,cc.reset+simplify(size).rjust(6),input[k])

		else:
			if k in checkin:
				print(k_+':'.ljust(7)+cc.err+'missing'.ljust(19), input[k]+cc.reset)
			else:
				print(k_+':'.ljust(7)+cc.key+'missing'.ljust(19), input[k]+cc.reset)

	""" """
#-------------------------------------------------------------------
# extracted from Jonathaneunice/ansiwrap
# to eliminate ansi_terminate_lines, which seems to have a bug
# string_types = basestring if sys.version_info[0] == 2 else str
def ansilen(s):
	"""
	Return the length of a string as it would be without common
	ANSI control codes. The check of string type not needed for
	pure string operations, but remembering we are using this to
	monkey-patch len(), needed because textwrap code can and does
	use len() for non-string measures.
	"""
#	if isinstance(s, string_types):
	if isinstance(s, str):
		s_without_ansi = re.compile('\x1b\\[(K|.*?m)').sub('', s)
		return len(s_without_ansi)
	else:
		return len(s)

# now replace the standard len of textwrap3 
textwrap3.len = ansilen





