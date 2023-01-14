# rabbit generate task list from the -loop or -id key
#

import re
import json
#import pyjson5 as json5
import hjson    as hjson

if 'clise' in __file__:
	import clise.jsontool as jt
else:
	import jsontool as jt

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

cc=jt.cc()
#----------------------------------------------------------------------------
# grab time
def timestr2stamp(tstr):

	match=re.search(r'([0-9]+)([^0-9])[0-9]+([^0-9])[0-9]+', tstr)
	if match == None: 
		try:    modtime = Path(tstr).expanduser().stat().st_mtime
		except: return None
		return modtime

	date = tstr.split()
	if len(date) == 1:
		time=None
		date=date[0]
	elif len(date) >=2:
		time=date[1]
		date=date[0]
	else:
		return None

	match=re.search(r'([0-9]+)([^0-9])[0-9]+([^0-9])[0-9]+', date)
	if match == None: return None

	if len(match.group(1)) <=2: yr='%y'
	else:				    yr='%Y'
	sep1 = match.group(2)
	sep2 = match.group(3)

	dformat=yr+sep1+"%m"+sep2+"%d"
	#print(dformat)
	if time == None:
		return datetime.timestamp(datetime.strptime(date,dformat))

	#print(time)
	match=re.search(r'[0-9]+([^0-9])[0-9]+([^0-9])[0-9]+', time)

	sep3 = match.group(1)
	sep4 = match.group(2)

	tformat="%H"+sep3+"%M"+sep4+"%S"
	#print(tformat)
	return datetime.timestamp(datetime.strptime(tstr,dformat+" "+tformat))

def sizestr2size(sstr):
	try:
		resize=int(sstr)
	except:
		try: resize = Path(sstr).expanduser().stat().st_size
		except ValueError: resize = -1
	return resize

# fix column type from panda table to astropy table
# perhaps a better way to do this, but for now...

def new_ext(filename, new):
	return re.sub('\.[^\.]+$','.'+new, filename)
#-------------------------------------------------------------------
# semi-regex handling in the parameters regarding file names
def find_tag(expression, inp, tagid='', pre='{', post='}'):
	""" get tags from a parameter
	"""
	if expression == None: return ''

	# this means inp can be drived from expression itself by removing '(' and ')'
	if inp == None:
		inp=expression.replace('(','')
		inp=inp.replace(')','')
		return_inp=True
	else:
		return_inp=False

	subexpr=re.findall(expression,inp)
	if type(subexpr[0]) is tuple: subexpr = [item for t in subexpr for item in t] 

	tag=OrderedDict()

	for idx, expr in enumerate(subexpr):
		tag[pre+tagid+str(idx+1)+post]=expr
	
	if return_inp:  return tag, inp
	else: 	    return tag
	""" """

def apply_tag(inp, tags):
	""" apply tags to a parameter
	"""
	if tags == None: return inp
	if inp  == None: return inp

	out=inp
	for key in tags: out=out.replace(key,tags[key])

	return out
	""" """

def combine_tags(keys, tags, ids=None, cfg=None):
	""" get more tags from other files used in the program
	"""

	if cfg  == None: cfg=OrderedDict()
	if ids  == None: ids=[key+':' for key in keys]

	if tags == None: tags=OrderedDict()
	combined=tags.copy()

	values=[]
	for ckey, cid in zip(keys, ids):
#		expre		= self.apply_tag(cfg[ckey],tags)
#		tag, value  = self.find_tag(expre, None, tagid=cid)
		expre		= apply_tag(cfg[ckey],tags)
		tag, value  = find_tag(expre, None, tagid=cid)
		values.append(value)
		for key_, tag_ in tag.items(): combined[key_]=tag_
	
	return combined, values
	""" """

#-------------------------------------------------------------------
def regex2searchable(regex, wild='*'):
	""" convert regular expression to file searchable expression
	"""
	if not bool(re.search('\(',regex)): return regex

	spexpr=regex.split('(')

	newexpr=[]
	for seg in spexpr:
		if not bool(re.search('\)', seg)): 
			newexpr.append(seg)
			continue

		newexpr.append(re.sub(r'(.*\))','*',seg))

#		print(''.join(newexpr))
	return ''.join(newexpr)
	""" """

def mixed2regexsrchable(mixed, wild='*', single='?'):
	""" convert mixed expression to file searchable and regex expression
	"""
	if not bool(re.search('\(',mixed)): 
		regex=mixed
		regex=regex.replace('.','\.')
		regex=regex.replace(wild,'.*')
		regex=regex.replace(single,'.')
		return mixed, regex

	spexpr=mixed.split('(')

	srchable=[]
	regex=[]

	for seg in spexpr:
		if not bool(re.search('\)', seg)): 
			reg = seg
			reg = seg.replace('.','\.')
			reg = reg.replace(wild,'.*')
			reg = reg.replace(single,'.')
			regex.append(reg)
			srchable.append(seg)
			continue

		srchable.append(re.sub(r'.*\)','*',seg))

		mat = re.match(r'(.*\))(.*)',seg)
		reg = mat.group(2)
		reg = reg.replace('.','\.')
		reg = reg.replace(wild,'.*')
		reg = reg.replace(single,'.')
		regex.append(mat.group(1)+reg)


	srchable=''.join(srchable)
	srchable=srchable.replace('**','*')
	regex='('.join(regex)
	return srchable, regex
	""" """

#----------------------------------------------------------------------------
# filtering file selections
def pick(infile, indir=None, include=None, exclude=None, verbose=0):
	""" see if the given filename meets the requirement as an input file
	"""
	# set by "from" and/or "except" options
	if infile == "": return False

	pick=True
#	if 'from'   in cfg.keys(): pick = pick and     bool(re.search(cfg['from'], infile))
#	if 'except' in cfg.keys(): pick = pick and not bool(re.search(cfg['except'],infile))
	if include != None: pick = pick and     bool(re.search(include, infile))
	if exclude != None: pick = pick and not bool(re.search(exclude, infile))

	if not pick:
		if verbose >= 3: print('not picking',infile)
		return False

	if indir != None: infile_=(Path(indir) / Path(infile)).expanduser()
	else:             infile_=infile

	if not path.isfile(infile_):
		if verbose >= 2: print(infile, 'does not exist.')
		return False

	return pick
	""" """

# iteration loop settings
def search_infile(infile_expre, tagid='', indir=None, 
		include=None, exclude=None, 
		recursive_search=True, sortby='', 
		verbose=0):
	""" make file list from wild card input file parameters
	"""
#	if type(expre) is not str: return None

	cdir=getcwd()
	if indir != None: chdir(indir)
	
	infile_expre=jt.str_to_list(infile_expre)

	# convert regex to searchable expression
	# e.g.,  dummy_([0-9]+).fits => dummy_*.fits
	canfiles = OrderedDict()

	prev_fullname = None
	for idx, expre in enumerate(infile_expre):
		
		# this allows tagging but somewhat too cryptic and unconventional
		# avoid id starting with a number since number id is reserved for automatic assignment
		mat=re.search('^(.*)\s+\>([^0-9].*)$',expre)

		if bool(mat): fullname, id = mat.group(1,2)
		else:		  fullname, id = expre, str(idx)

		if fullname == "==":
			if prev_fullname == None:
				print(cc.err+'requires at least one valid file name expression'+cc.reset)
				exit()
			else:
				fullname = prev_fullname

		dir  = path.dirname (fullname)
		file = path.basename(fullname)

		if dir == '.': dir='' 
		if dir != '' : dir=dir+'/'
	
		schdir,  rexdir  = mixed2regexsrchable(dir)
		schfile, rexfile = mixed2regexsrchable(file)

		x = OrderedDict()
		x['schdir' ] = schdir
		x['schfile'] = schfile
		x['rexfile'] = rexdir+rexfile
		x['isregex'] = schfile != file
		
		canfiles[id] = x
		
		prev_fullname=fullname

	
	# now actual file search for each searchable file expression
	ans = OrderedDict()
	for id, cfile in canfiles.items():

		if cfile['schfile'] == '': continue
	
		# not sure why the search is this convoluted
#		print(recursive_search, each)
		if indir != None:
			if recursive_search: files = glob.glob('**/'+cfile['schfile'], recursive=recursive_search)
			else:			   files = glob.glob(cfile['schfile'])
		else:				   files = glob.glob(cfile['schdir']+cfile['schfile'], recursive=recursive_search)
	
		if len(files) == 0: continue
	
		# check if the found match with the original regular expression
		if cfile['isregex']: 
			survived =[]
			tags     =[]
			for found in files:
				if not re.search(cfile['rexfile'], found): continue
				survived.append(found)
				tags.     append(find_tag(cfile['rexfile'], found, tagid=tagid))
		else:
			survived = files
			tags	   = [OrderedDict()]*len(files)
	
		if len(survived) == 0: continue

		# if infile_order != 'unsort':
		# 	zipped = zip(survived, tags)
		# 	sortee = sorted(zipped, reverse= infile_order == 'reverse')
		# 	tuples = zip(*sortee )
		# 	survived, tags = [ list(tuple) for tuple in tuples]
	
		# collect any that survives
		for file, tag in zip(survived, tags): 
			x = OrderedDict()
			x['name'] = file
			x['tag' ] = tag
			x['id'  ] = id
			x['pick'] = pick(file, indir=indir, include=include, exclude=exclude, verbose=verbose)
			key = file + ' ' +str(id)
			# unique key is determined by the filename and group id
			ans[key] = x

	chdir(cdir)
	
	return ans

def get_outfile(outfile, infile, outdir=None, outsubdir=None, \
		mirror_indir=True, tags=None, switch_subdir=None, \
		cfg=None, verbose=0):
	""" get output file name based on input filename and other options
	"""

	if outfile == None: return None, None

	if cfg     == None: cfg=OrderedDict()
	if outdir  == None: mirror_indir = False 
	
	insubdir = path.dirname(infile)
	if outsubdir == None:
		outsubdir= insubdir
		if outsubdir != '': outsubdir=outsubdir+'/'
	
	if switch_subdir == True:
		for src, trg in switch_subdir.items():
			outsubdir=outsubdir.replace(src, trg)
	
	if tags != None: 
		outsubdir = apply_tag(outsubdir,tags)
		outfile   = apply_tag(outfile,tags)

	if mirror_indir:
		outdir  = (Path(outdir) / Path(outsubdir)).expanduser()
		outfile = (Path(outdir) / Path(outfile)  ).expanduser()
	else:
		# usually in this case, this function is not likely needed
		if outdir == None: 
			outdir  = Path(path.dirname(outfile)).expanduser()
#			outfile = Path(outdir) / Path(path.basename(outfile))
		else:
			outfile = (Path(outdir) / Path(outfile)).expanduser()

#	print(outdir,outfile)
	return outfile, outdir
	""" """

#----------------------------------------------------------------------------
# this part can be combined with matchID and get_task_Ready in jsontool
# essentially the same thing, but it is done in a slightly different way
regtk = ['==','!=','~=','~!=']
regex = '('+"|".join(regtk)+")"

def group_cfg_for_match_(seed, matkey=''):
	common =OrderedDict()
	common['-id'] = ''
	common['-main'] = seed['-main']

	global regtk, regex

	matchc =OrderedDict()
	for each in regtk: matchc[each]=OrderedDict()

	for key in seed:
		if key == matkey: continue
		mat=re.search('^'+matkey+regex+'(.*)',key)
		if not bool(mat): 
			common[key] = seed[key]
			continue
		con, par = mat.group(1, 2)
		for each in regtk: 
			if con == each:
				matchc[each][key]=seed[key]
	return common, matchc

def update_cfg_by_match_(task, seed, matchc, matkey=None, matval=None):

	# now inherit this specific options
	# more general to specific
	for key in matchc['!=']:
		mat = re.search('^'+matkey+'!=(.*)',key)
		par = mat.group(1)
		mat_= re.search('(.*):(.*)',par)
		if bool(mat_):
			par, newkey = mat_.group(1,2)
			if par != matval: task[newkey] = seed[key]
		else:
			if par != matval:
				for each in seed[key]: task[each] = seed[key][each]

	for key in matchc['~!=']:
		mat = re.search('^'+matkey+'~!=(.*)',key)
		par = mat.group(1)
		mat_= re.search('(.*):(.*)',par)
		if bool(mat_):
			par, newkey = mat_.group(1,2)
			if not bool(re.search(par, matval)):
				task[newkey] = seed[key]
		else:
			if not bool(re.search(par, matval)):
				for each in seed[key]: task[each] = seed[key][each]

	for key in matchc['~=']:
		mat=re.search('^'+matkey+'~=(.*)',key)
		par = mat.group(1)
		mat_= re.search('(.*):(.*)',par)
		if bool(mat_):
			par, newkey = mat_.group(1,2)
			if bool(re.search(par, matval)):
				task[newkey] = seed[key]
		else:
			if bool(re.search(par, matval)):
				for each in seed[key]: task[each] = seed[key][each]

	for key in matchc['==']:
		mat=re.search('^'+matkey+'==(.*)',key)
		par = mat.group(1)
		mat_= re.search('(.*):(.*)',par)
		if bool(mat_):
			par, newkey = mat_.group(1,2)
			if par == matval:
				task[newkey] = seed[key]
		else:
			if par == matval:
				for each in seed[key]: task[each] = seed[key][each]

	return task

def group_cfg_for_match(seed):
	global regtk, regex

	common =OrderedDict()
	matchc =OrderedDict()
	for each in regtk: matchc[each]=OrderedDict()

	for key in seed:
		mat=re.search('^(.+)'+regex+'(.+)',key)
		if not bool(mat): 
			common[key] = seed[key]
			continue
		con, par = mat.group(2, 3)
		for each in regtk: 
			if con == each:
				matchc[each][key]=seed[key]
	return common, matchc

def group_cfg_for_match_simple(seed):
	global regtk, regex

	common =OrderedDict()
	matchc =OrderedDict()

	for key in seed:
		mat=re.search('^(.+)'+regex+'(.+)',key)
		if not bool(mat): 
			common[key] = seed[key]
			continue
		matchc[key]=seed[key]
	return common, matchc

def update_cfg_by_match(task, matchc, matkey=None, matval=None):

	# now inherit this specific options
	# more general to specific
	# need to track that no update has been made...
	for key in matchc['!=']:
		mat = re.search('^'+matkey+'!=(.*)',key)
		if not bool(mat): continue
		par = mat.group(1)
		mat_= re.search('(.*):(.*)',par)
		if bool(mat_):
			par, newkey = mat_.group(1,2)
			if par != matval: task[newkey] = matchc['!='][key]
		else:
			if par != matval:
				for each in matchc['!='][key]: task[each] = matchc['!='][key][each]

	for key in matchc['~!=']:
		mat = re.search('^'+matkey+'~!=(.*)',key)
		if not bool(mat): continue
		par = mat.group(1)
		mat_= re.search('(.*):(.*)',par)
		if bool(mat_):
			par, newkey = mat_.group(1,2)
			if not bool(re.search(par, matval)):
				task[newkey] = matchc['~!='][key]
		else:
			if not bool(re.search(par, matval)):
				for each in matchc['~!='][key]: task[each] = matchc['~!='][key][each]

	for key in matchc['~=']:
		mat=re.search('^'+matkey+'~=(.*)',key)
		if not bool(mat): continue
		par = mat.group(1)
		mat_= re.search('(.*):(.*)',par)
		if bool(mat_):
			par, newkey = mat_.group(1,2)
			if bool(re.search(par, matval)):
				task[newkey] = matchc['~='][key]
		else:
			if bool(re.search(par, matval)):
				for each in matchc['~='][key]: task[each] = matchc['~='][key][each]

	for key in matchc['==']:
		mat=re.search('^'+matkey+'==(.*)',key)
		if not bool(mat): continue
		par = mat.group(1)
		mat_= re.search('(.*):(.*)',par)
		if bool(mat_):
			par, newkey = mat_.group(1,2)
			if par == matval:
				task[newkey] = matchc['=='][key]
		else:
			if par == matval:
				for each in matchc['=='][key]: task[each] = matchc['=='][key][each]

	return task

def get_common_vs_match(seed):
	global regtk, regex

	common =OrderedDict()
	matchc =OrderedDict()

	for key in seed:
		mat=re.search('^(.+)'+regex+'(.+)',key)
		if not bool(mat): 
			common[key]=seed[key]
			continue
		matchc[key]=seed[key]
	return common, matchc

#----------------------------------------------------------------------------
# seed  block: common for every iteration of each task
# cases block: includes
#	common block: common for all tasks for all iteration
#	matchc block: common for each iteration (and each task)

# this is more compatible with legacy code cjpy, but obsolete
def multiply_by_id(seed, matkey='-id', verbose=0):

	common, matchc = group_cfg_for_match(seed)
	tasks = []

	# cannot use -nid, -fid since they are not known at this time
	# only -id and -main is known
	# the order matters...
	udkey = OrderedDict()
	udkey['-main'] = seed['-main'].split('.')[-1]
		
	for idval in seed[matkey]:

		# first inherit common ones
		task = common.copy()

		# set proper id
		# task['-id'], task['-nid'], task['-fid'] = jt.set_id(id, idx+1)
		task [matkey] = idval
		udkey[matkey] = idval

		if '-changes' in common:
			from deepdiff import DeepDiff as dd 
			before = task.copy()

		# update by matching key
		for ematkey, ematval in udkey.items():
			task = update_cfg_by_match(task, matchc, matkey=ematkey, matval=ematval)

		if '-changes' in common:
			diff = dd(before, task)
			if len(diff) == 0:
				print(cc.key+'No changes by the -id selection for', idval,cc.reset)

		tasks.append(task)

	return tasks

# this is technically obsolete by the new scheme
def multiply_by_id_multi(seed, cases=None, matkey='-id', verbose=0, **kwpars):

	if type(seed) is str      : seed=jt.load_file(seed)
	if type(seed) is not list : seed=[seed]

	common = OrderedDict()
	for eseed in seed[:]: 
		if '-main' not in eseed:
			common = jt.merge(common, eseed)
			seed.remove(eseed)

	if cases != None: common = jt.merge(common, cases)
	common, matchc = group_cfg_for_match(common)

	tasks = []

	udkey = OrderedDict()
	for idval in common[matkey]:
		for sidx, eseed in enumerate(seed):

			# first inherit common ones
			task = common.copy()
			task = jt.merge(task, eseed)
			task['-id'   ] = idval +"."+str(sidx+1)

			# the order is meaningful for the exact match ('==')?
			udkey['-main'] = eseed['-main'].split('.')[-1]
			udkey[matkey ] = idval+"."+str(sidx+1)

			# update by matching key
			for ematkey, ematval in udkey.items():
				task = update_cfg_by_match(task, matchc, matkey=ematkey, matval=ematval)

			tasks.append(task)

	return tasks

# this is more compatible with legacy code cjpy, not recommended
def multiply_by_file(seed, inkey="infile", outkey=None,
				  indir=None, outdir=None, outsubdir=None, basedir=None,
				  mirror_indir=True, switch_subdir=False,
				  checkin=None, checkout=None,
				  include=None, exclude=None,
				  appkeys=None, tagkeys=None,
				  rel2indir=None, rel2outdir=None, 
				  rel2nodir=None, # files relative to no set dir
				  recursive=True, sortby='', reverse=None,
				  before=None, after=None,
				  larger=None, smaller=None,
				  verbose=0):

	# among rel2indir, rel2outdir, rel2nodir, all the file keys should be covered

	if type(seed) is str      : seed=jt.load_file(seed)

	if type(checkin) .__name__ == 'NoneType': checkin=[inkey]

	infiles = search_infile(seed[inkey], indir=indir, include=include, exclude=exclude,
						recursive_search= recursive, sortby=sortby,
						verbose=verbose)

	if infiles == None: return []

	common, matchc = group_cfg_for_match(seed)

	tasks = []

	for mainkey, info in infiles.items():
	
		name = info.get('name' , None) 
		tag  = info.get('tag'  , None)
		id   = info.get('id'   , None)
		pick = info.get('pick' , True)

		if name == None: continue
		if not pick: continue

		# first inherit common ones
		task = common.copy()

		task['-id'] = mainkey
		task[inkey] = name

		task = update_cfg_by_match(task, matchc, matkey=inkey,	     matval=name)
		task = update_cfg_by_match(task, matchc, matkey='-'+inkey+'.key',matval=id  )

		# need to update tkeys and akeys
		# search for outfile?
		# incheck outcheck...
		# all these done by set_file_pars?

		if tagkeys !=None:
			tag, values= combine_tags(tagkeys, tag, ids=tagids, cfg=seed)
			for tkey, value in zip(tkeys, values): task[tkey]=value

		if appkeys !=None:
			for each in appkeys: task[each] = apply_tag(task[each], tag)

		if outkey in seed:
			outfile=seed.get(outkey,None)
			outfile, outdir =get_outfile(outfile, name, \
						outdir=outdir, outsubdir=outsubdir,
						mirror_indir=mirror_indir, switch_subdir=switch_subdir,
						tags=tag, cfg=seed, verbose=verbose)
			task[outkey]=Path(outfile).expanduser()

		# expand ~***
		if indir != None: task[inkey] = (Path(indir)/Path(name)).expanduser()
		else:             task[inkey] = Path(name).expanduser()

		# update files in a directory relative to input dir
		if rel2indir != None:
			fulldir = path.dirname(task[inkey])
			for key in rel2indir: 
				if key in seed:
					if task[key] != None:
						task[key]=(Path(fulldir)/Path(task[key])).expanduser()

		# update files in a directory relative to output dir
		if rel2outdir != None:
			if outkey != None:
				if mirror_indir: fulldir = path.dirname(Path(task[outkey]).expanduser())
				else:		     fulldir = Path(outdir).expanduser()

				for key in rel2outdir: 
					if key in seed:
						if task[key] != None:
							task[key]=(Path(fulldir) / Path(task[key])).expanduser()

		# rename file path relative to basedir if possible
		if basedir != None:
			try    : task[inkey] = task[inkey].relative_to(basedir)
			except : pass

			if outkey in task:
				if outkey != None:
					try    : task[outkey] = task[outkey].relative_to(basedir)
					except : pass

			for each in [rel2indir, rel2outdir, rel2nodir]:
				if each == None: continue
				if type(each) is str: each=[each]
				for key in each:
					if key not in task: continue
					if task[key] == None: continue
					try    : task[key] = task[key].relative_to(basedir)
					except : pass
		
		# update filename with proper strings
		task[inkey] = str(task[inkey])
		if outkey != None: task[outkey]=str(task[outkey])
		for each in [rel2indir, rel2outdir, rel2nodir]:
			if each == None: continue
			if type(each) is str: each=[each]
			for key in each:
				if key not in task: continue
				if task[key] == None: continue
				task[key] = str(task[key])

		if '-checkin'  not in task: task['-checkin' ] = []
		if '-checkout' not in task: task['-checkout'] = []

		task['-checkin'] = task['-checkin']+checkin 
		if type(checkout).__name__ != 'NoneType': 
			task['-checkout'] = task['-checkout']+checkout 


		tasks.append(task)

	# here we have to sort when we have both infile and outfile
	if before != None:
		if sortby == "":   sortby  = inkey+":mtime"
		if reverse== None: reverse = True
	if after != None:
		if sortby == "":   sortby  = inkey+":mtime"
		if reverse== None: reverse = False

	if larger != None:
		if sortby == "":   sortby  = inkey+":size"
		if reverse== None: reverse = False
	if smaller != None:
		if sortby == "":   sortby  = inkey+":size"
		if reverse== None: reverse = True

	if reverse== None: reverse = False
	if sortby != "":
		key, stype = sortby.split(':')
		for task in tasks:
			if   stype == "mtime"    : task["-sval"] = Path(task[key]).stat().st_mtime
			elif stype == "size"     : task["-sval"] = Path(task[key]).stat().st_size
			elif stype == "name"     : task["-sval"] = path.basename(task[key])
			elif stype == "fullname" : task["-sval"] = task[key]
			else: continue
		tasks = sorted(tasks,  key=lambda x: x['-sval'], reverse=reverse)


	return tasks
	""" """

def multiply_by_file_multi(seed, cases=None, inkey="infile", outkey="outfile",
				  indir=None, outdir=None, outsubdir=None, basedir=None,
				  mirror_indir=True, switch_subdir=False,
				  checkin=None, checkout=None,
				  include=None, exclude=None,
				  appkeys=None, tagkeys=None,
				  rel2indir=None, rel2outdir=None, 
				  rel2nodir=None, # files relative to no set dir
				  recursive=True, sortby='', reverse=None,
				  before=None, after=None,
				  larger=None, smaller=None,
				  verbose=0):

	# among rel2indir, rel2outdir, rel2nodir, all the file keys should be covered

	if type(seed) is str      : seed=jt.load_file(seed)
	if type(seed) is not list : seed=[seed]


	common = OrderedDict()
	infile_expre=''
	if type(checkin) .__name__ == 'NoneType': checkin=[inkey]
	# for eseed in seed[:]: 
	for idx, eseed in enumerate(seed): 
		seed[idx], match = group_cfg_for_match_simple(eseed)
		if '-main' in eseed:
			if infile_expre == '': infile_expre=eseed[inkey]
		else:
			common = jt.merge(common, seed[idx].copy())
			# seed.remove(seed[idx])

		common = jt.merge(common, match)
		if type(checkout).__name__ == 'NoneType': 
			if outkey in eseed: checkout=[outkey]

	infiles = search_infile(infile_expre, indir=indir, include=include, exclude=exclude,
						recursive_search= recursive, sortby=sortby,
						verbose=verbose)

	if infiles == None: return []

	if cases != None: common = jt.merge(common, cases)
	common, matchc = group_cfg_for_match(common)

	tasks = []

	udkey = OrderedDict()
	for mainkey, info in infiles.items():
	
		name = info.get('name' , None) 
		tag  = info.get('tag'  , None)
		id   = info.get('id'   , None)
		pick = info.get('pick' , True)

		if name == None: continue
		if not pick: continue

		for sidx, eseed in enumerate(seed):
			if '-main' not in eseed: continue
			# first inherit common ones
			task = common.copy()
			task = jt.merge(task, eseed)

			task['-id'] = mainkey+"."+str(sidx) # this should be last?
			task[inkey] = name

			# the order is meaningful for the exact match ('==')?
			udkey['-main'] = eseed['-main'].split('.')[-1]
			udkey['-id'  ] = mainkey+"."+str(sidx) # this should be last?
			udkey[inkey  ] = name
			udkey['-'+inkey+'.key'] = id

			for ematkey, ematval in udkey.items():
				task = update_cfg_by_match(task, matchc, matkey=ematkey, matval=ematval)

			# need to update tkeys and akeys
			# search for outfile?
			# incheck outcheck...
			# all these done by set_file_pars?

			if tagkeys !=None:
				tag, values= combine_tags(tagkeys, tag, ids=tagids, cfg=eseed)
				for tkey, value in zip(tkeys, values): task[tkey]=value

			if appkeys !=None:
				for each in appkeys: 
					if each in task: task[each] = apply_tag(task[each], tag)

			if outkey in eseed:
				outfile=eseed[outkey]
				outfile, outdir =get_outfile(outfile, name, \
							outdir=outdir, outsubdir=outsubdir,
							mirror_indir=mirror_indir, switch_subdir=switch_subdir,
							tags=tag, cfg=eseed, verbose=verbose)
				task[outkey]=Path(outfile).expanduser()

			# expand ~***
			if inkey in task:
				if indir != None: task[inkey] = (Path(indir)/Path(name)).expanduser()
				else:             task[inkey] = Path(name).expanduser()

				# update files in a directory relative to input dir
				if rel2indir != None:
					fulldir = path.dirname(task[inkey])
					for key in rel2indir: 
						if key in task:
							if task[key] != None:
								task[key]=(Path(fulldir)/Path(task[key])).expanduser()

			# update files in a directory relative to output dir
			if outkey in task:
				if rel2outdir != None:
					if outkey != None:
						if mirror_indir: fulldir = path.dirname(Path(task[outkey]).expanduser())
						else:		     fulldir = Path(outdir).expanduser()

						for key in rel2outdir: 
							if key in task:
								if task[key] != None:
									task[key]=(Path(fulldir) / Path(task[key])).expanduser()

			# rename file path relative to basedir if possible
			if basedir != None:
				if inkey in task:
					try    : task[inkey] = task[inkey].relative_to(basedir)
					except : pass

				if outkey in task:
					if outkey != None:
						try    : task[outkey] = task[outkey].relative_to(basedir)
						except : pass

				for each in [rel2indir, rel2outdir, rel2nodir]:
					if each == None: continue
					if type(each) is str: each=[each]
					for key in each:
						if key not in task: continue
						if task[key] == None: continue
						try    : task[key] = task[key].relative_to(basedir)
						except : pass
			
			# update filename with proper strings
			if inkey in task: task[inkey] = str(task[inkey])
			if outkey in task:
				if outkey != None: task[outkey]=str(task[outkey])
			for each in [rel2indir, rel2outdir, rel2nodir]:
				if each == None: continue
				if type(each) is str: each=[each]
				for key in each:
					if key not in task: continue
					if task[key] == None: continue
					task[key] = str(task[key])

			if '-checkin'  not in task: task['-checkin' ] = []
			if '-checkout' not in task: task['-checkout'] = []

			task['-checkin'] = task['-checkin']+checkin 
			if type(checkout).__name__ != 'NoneType': 
				task['-checkout'] = task['-checkout']+checkout 

			tasks.append(task)

	# here we have to sort when we have both infile and outfile
	if before != None:
		if sortby == "":   sortby  = inkey+":mtime"
		if reverse== None: reverse = True
	if after != None:
		if sortby == "":   sortby  = inkey+":mtime"
		if reverse== None: reverse = False

	if larger != None:
		if sortby == "":   sortby  = inkey+":size"
		if reverse== None: reverse = False
	if smaller != None:
		if sortby == "":   sortby  = inkey+":size"
		if reverse== None: reverse = True

	if reverse== None: reverse = False
	if sortby != "":
		key, stype = sortby.split(':')
		for task in tasks:
			if   stype == "mtime"    : task["-sval"] = Path(task[key]).stat().st_mtime
			elif stype == "size"     : task["-sval"] = Path(task[key]).stat().st_size
			elif stype == "name"     : task["-sval"] = path.basename(task[key])
			elif stype == "fullname" : task["-sval"] = task[key]
			else: continue
		tasks = sorted(tasks,  key=lambda x: x['-sval'], reverse=reverse)

	return tasks
	""" """
