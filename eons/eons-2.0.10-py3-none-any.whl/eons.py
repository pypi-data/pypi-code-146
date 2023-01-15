import logging
import os
import shutil
from copy import deepcopy
import sys
import pkgutil
import importlib.machinery
import importlib.util
import types
import traceback
import jsonpickle
import inspect
import ctypes
import re
from pathlib import Path
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT
import operator
import argparse
import requests
from tqdm import tqdm
from zipfile import ZipFile
from distutils.dir_util import mkpath

######## START CONTENT ########
def INVALID_NAME():
	return "INVALID_NAME"

class ActualType(type):
	def __repr__(self):
		return self.__name__

class NotInstantiableError(Exception, metaclass=ActualType): pass

class MissingArgumentError(Exception, metaclass=ActualType): pass

class FunctorError(Exception, metaclass=ActualType): pass
class MissingMethodError(FunctorError, metaclass=ActualType): pass
class CommandUnsuccessful(FunctorError, metaclass=ActualType): pass
class InvalidNext(FunctorError, metaclass=ActualType): pass

class ErrorResolutionError(Exception, metaclass=ActualType): pass
class FailedErrorResolution(ErrorResolutionError, metaclass=ActualType): pass

class SelfRegisteringError(Exception, metaclass=ActualType): pass
class ClassNotFound(SelfRegisteringError, metaclass=ActualType): pass

class HelpWanted(Exception, metaclass=ActualType): pass
class HelpWantedWithRegistering(HelpWanted, metaclass=ActualType): pass

class Fatal(Exception, metaclass=ActualType): pass
class FatalCannotExecute(Fatal, metaclass=ActualType): pass

class PackageError(Exception, metaclass=ActualType): pass

class MethodPendingPopulation(Exception, metaclass=ActualType): pass


#Self registration for use with json loading.
#Any class that derives from SelfRegistering can be instantiated with:
#   SelfRegistering("ClassName")
#Based on: https://stackoverflow.com/questions/55973284/how-to-create-this-registering-factory-in-python/55973426
class SelfRegistering(object):

	def __init__(this, *args, **kwargs):
		#ignore args.
		super().__init__()

	@classmethod
	def GetSubclasses(cls):
		for subclass in cls.__subclasses__():
			# logging.info(f"Subclass dict: {subclass.__dict__}")
			yield subclass
			for subclass in subclass.GetSubclasses():
				yield subclass

	@classmethod
	def GetClass(cls, classname):
		for subclass in cls.GetSubclasses():
			if subclass.__name__ == classname:
				return subclass

		# no subclass with matching classname found (and no default defined)
		raise ClassNotFound(f"No known SelfRegistering class: {classname}")			

	#TODO: How do we pass args to the subsequently called __init__()?
	def __new__(cls, classname, *args, **kwargs):
		toNew = cls.GetClass(classname)
		logging.debug(f"Creating new {toNew.__name__}")

		# Using "object" base class method avoids recursion here.
		child = object.__new__(toNew)

		#__dict__ is always blank during __new__ and only populated by __init__.
		#This is only useful as a negative control.
		# logging.debug(f"Created object of {child.__dict__}")

		return child

	@staticmethod
	def RegisterAllClassesInDirectory(directory):
		logging.debug(f"Loading SelfRegistering classes in {directory}")
		logging.debug(f"Available modules: {os.listdir(directory)}")
		for file in os.listdir(directory):
			if (file.startswith('_') or not file.endswith('.py')):
				continue

			moduleName = file.split('.')[0]

			# logging.debug(f"Attempting to registering classes in {moduleName}.")
			loader = importlib.machinery.SourceFileLoader(moduleName, os.path.join(directory, file))
			module = types.ModuleType(loader.name)
			loader.exec_module(module)

			# NOTE: the module is not actually imported in that it is available through sys.modules.
			# However, this appears to be enough to get both inheritance and SelfRegistering functionality to work.
			sys.modules[moduleName] = module #But just in case...
			logging.debug(f"{moduleName} imported.")

			#### Other Options ####
			# __import__(module)
			# OR
			# for importer, module, _ in pkgutil.iter_modules([directory]):
			#	 importer.find_module(module).exec_module(module) #fails with "AttributeError: 'str' object has no attribute '__name__'"
			#	 importer.find_module(module).load_module(module) #Deprecated

		# enable importing and inheritance for SelfRegistering classes
		if (directory not in sys.path):
			sys.path.append(directory)


# A Datum is a base class for any object-oriented class structure.
# This class is intended to be derived from and added to.
# The members of this class are helpful labels along with the ability to invalidate a datum.
class Datum(SelfRegistering):

	# Don't worry about this.
	# If you really want to know, look at SelfRegistering.
	def __new__(cls, *args, **kwargs):
		return object.__new__(cls)


	def __init__(this, name=INVALID_NAME(), number=0):
		# logging.debug("init Datum")

		# Names are generally useful.
		this.name = name

		# Storing validity as a member makes it easy to generate bad return values (i.e. instead of checking for None) as well as manipulate class (e.g. each analysis step invalidates some class and all invalid class are discarded at the end of analysis).
		this.valid = True

	# Override this if you have your own validity checks.
	def IsValid(this):
		return this.valid == True


	# Sets valid to true
	# Override this if you have members you need to handle with care.
	def MakeValid(this):
		this.valid = True


	# Sets valid to false.
	def Invalidate(this):
		this.valid = False


# util is a namespace for any miscellaneous utilities.
# You cannot create a util.
class util:
	def __init__(this):
		raise NotInstantiableError("util is a namespace, not a class; it cannot be instantiated.")

	#dot.notation access to dictionary attributes
	class DotDict(dict):
		__getattr__ = dict.get
		__setattr__ = dict.__setitem__
		__delattr__ = dict.__delitem__

		def __deepcopy__(this, memo=None):
			return util.DotDict(deepcopy(dict(this), memo=memo))

	# DotDict doesn't pickle right, since it's a class and not a native dict.
	class DotDictPickler(jsonpickle.handlers.BaseHandler):
		def flatten(this, dotdict, data):
			return dict(dotdict)

	@staticmethod
	def RecursiveAttrFunc(func, obj, attrList):
		attr = attrList.pop(0)
		if (not attrList):
			return eval(f"{func}attr(obj, attr)")
		if (not hasattr(obj, attr)):
			raise AttributeError(f"{obj} has not attribute '{attr}'")
		return util.RecursiveAttrFunc(func, getattr(obj, attr), attrList)

	@staticmethod
	def HasAttr(obj, attrStr):
		return util.RecursiveAttrFunc('has', obj, attrStr.split('.'))

	@staticmethod
	def GetAttr(obj, attrStr):
		return util.RecursiveAttrFunc('get', obj, attrStr.split('.'))

	@staticmethod
	def SetAttr(obj, attrStr):
		raise NotImplementedError(f"util.SetAttr has not been implemented yet.")


	@staticmethod
	def LogStack():
		logging.debug(traceback.format_exc())


	class console:

		# Read this (just do it): https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences

		saturationCode = {
			'dark': 3,
			'light': 9
		}

		foregroundCodes = {
			'black': 0,
			'red': 1,
			'green': 2,
			'yellow': 3,
			'blue': 4,
			'magenta': 5,
			'cyan': 6,
			'white': 7
		}

		backgroundCodes = {
			'none': 0,
			'black': 40,
			'red': 41,
			'green': 42,
			'yellow': 43,
			'blue': 44,
			'magenta': 45,
			'cyan': 46,
			'white': 47,
		}

		styleCodes = {
			'none': 0,
			'bold': 1,
			'faint': 2, # Not widely supported.
			'italic': 3, # Not widely supported.
			'underline': 4,
			'blink_slow': 5,
			'blink_fast': 6, # Not widely supported.
			'invert': 7,
			'conceal': 8, # Not widely supported.
			'strikethrough': 9, # Not widely supported.
			'frame': 51,
			'encircle': 52,
			'overline': 53
		}

		@classmethod
		def GetColorCode(cls, foreground, saturation='dark', background='none', styles=None):
			if (styles is None):
				styles = []
			#\x1b may also work.
			compiledCode = f"\033[{cls.saturationCode[saturation]}{cls.foregroundCodes[foreground]}"
			if (background != 'none'):
				compiledCode += f";{cls.backgroundCodes[background]}"
			if (styles):
				compiledCode += ';' + ';'.join([str(cls.styleCodes[s]) for s in styles])
			compiledCode += 'm'
			return compiledCode

		resetStyle = "\033[0m"


	# Add a logging level
	# per: https://stackoverflow.com/questions/2183233/how-to-add-a-custom-loglevel-to-pythons-logging-facility/35804945#35804945
	@staticmethod
	def AddLoggingLevel(level, value):
		levelName = level.upper()
		methodName = level.lower()

		if hasattr(logging, levelName):
			raise AttributeError('{} already defined in logging module'.format(levelName))
		if hasattr(logging, methodName):
			raise AttributeError('{} already defined in logging module'.format(methodName))
		if hasattr(logging.getLogger(), methodName):
			raise AttributeError('{} already defined in logger class'.format(methodName))

		# This method was inspired by the answers to Stack Overflow post
		# http://stackoverflow.com/q/2183233/2988730, especially
		# http://stackoverflow.com/a/13638084/2988730
		def logForLevel(this, message, *args, **kwargs):
			if this.isEnabledFor(value):
				this._log(value, message, args, **kwargs)
		def logToRoot(message, *args, **kwargs):
			logging.log(value, message, *args, **kwargs)

		logging.addLevelName(value, levelName)
		setattr(logging, levelName, value)
		setattr(logging.getLogger(), methodName, logForLevel)
		setattr(logging, methodName, logToRoot)


jsonpickle.handlers.registry.register(util.DotDict, util.DotDictPickler)

# Don't import Method or Executor, even though they are required: it will cause a circular dependency.
# Instead, pretend there's a forward declaration here and don't think too hard about it ;)
################################################################################

# Functor is a base class for any function-oriented class structure or operation.
# This class derives from Datum, primarily, to give it a name but also to allow it to be stored and manipulated, should you so desire.
# Functors will automatically Fetch any ...Args specified.
# You may additionally specify required methods (per @method()) and required programs (i.e. external binaries).
# When Executing a Functor, you can say 'next=[...]', in which case multiple Functors will be Executed in sequence. This is necessary for the method propagation machinary to work.
# When invoking a sequence of Functors, only the result of the last Functor to be Executed or the first Functor to fail will be returned.
class Functor(Datum):

	def __init__(this, name=INVALID_NAME()):
		super().__init__(name)

		this.initialized = False

		# All necessary args that *this cannot function without.
		this.requiredKWArgs = []

		# Static arguments are Fetched when *this is first called and never again.
		# All static arguments are required.
		this.staticKWArgs = []
		this.staticArgsValid = False

		# Because values can be Fetched from *this, values that should be provided in arguments will be ignored in favor of those Fetched by a previous call to *this.
		# Thus, we can't enable 'this' when Fetching required or optional KWArgs (this is done for you in ValidateArgs)
		# If you want an arg to be populated by a child's member, make it static.

		# For optional args, supply the arg name as well as a default value.
		this.optionalKWArgs = {}

		# Instead of taking ...Args and ...KWArgs, we only take KWArgs.
		# You can list ordered arguments here which will correspond with either required or optional KWArgs.
		# If the arg you specify here does not exist in ...KWArgs, an error will be thrown.
		# Use this to make calling your Functor easier (e.g. MyMethod('some value') vs MyMethod(my_value='some value'))
		this.argMapping = []

		# Default places to Fetch from.
		# Add to this list when extending Fetch().
		# Remove from this list to restrict Fetching behavior.
		# Reorder this list to make Fetch more efficient for your use case.
		# Also see FetchWith and FetchWithout for ease-of-use methods.
		this.fetchFrom = [
			'this',
			'args',
			'config', #local (if applicable) or per Executor; should be before 'executor' if using a local config.
			'precursor',
			'executor',
			'environment',
		]

		# Fetch is modular.
		# You can add your own {'from':this.customSearchMethod} pairs to fetchLocations by overriding PopulateFetchLocations().
		# Alternatively, you may add to fetchLocations automatically by adding a fetchFrom entry and defining a method called f"fetch_location_{your new fetchFrom entry}(this, varName, default)".
		# The order of fetchLocations does not matter; the order of each fetchFrom provided to Fetch() does. This allows users to set their preferred search order for maximum efficiency.
		this.fetchLocations = {}

		# All @methods.
		# See Method.py for details.
		# NOTE: Functor cannot have @methods, since it would create a circular dependency. However, all downstream children of Functor may.
		this.methods = {}

		# You probably don't need to change this.
		# Similar to fetchFrom, methodSources lists where methods should be populated from and in what order
		# Each entry is a key-value pair representing the accessible member (member's members okay) and whether or not to honor Method.propagate.
		# If the value is False, all methods will be added to *this.methods and will overwrite any existing methods. Otherwise, only methods with propagate == True will be added and combined with existing methods. When in doubt, prefer True.
		this.methodSources = {
			'classMethods': False, # classMethods is created when a class uses @method()s
			'precursor.methods': True
		}

		# Specify any methods / member functions you need here.
		# *this will not be invoked unless these methods have been provided by a precursor.
		this.requiredMethods = []

		# All external dependencies *this relies on (binaries that can be found in PATH).
		# These are treated as static args (see above).
		this.requiredPrograms = []

		# For converting config value names.
		# e.g. "type": "projectType" makes it so that when calling Set("projectType", ...),  this.type is changed.
		this.configNameOverrides = {}

		# Rolling back can be disabled by setting this to False.
		this.enableRollback = True

		# Numerical result indication the success or failure of *this.
		# Set automatically.
		# 0 is invalid; 1 is best; higher numbers are usually worse.
		this.result = 0

		# Whether or not we should pass on exceptions when calls fail.
		this.raiseExceptions = True

		# Ease of use members
		# These can be calculated in Function and Rollback, respectively.
		this.functionSucceeded = False
		this.rollbackSucceeded = False

		# That which came before.
		this.precursor = None

		# The progenitor of *this.
		this.executor = None

		# Those which come next (in order).
		this.next = []


	# Override this and do whatever!
	# This is purposefully vague.
	def Function(this):
		pass


	# Undo any changes made by Function.
	# Please override this too!
	def Rollback(this):
		pass


	# Override this to check results of operation and report on status.
	# Override this to perform whatever success checks are necessary.
	def DidFunctionSucceed(this):
		return this.functionSucceeded


	# RETURN whether or not the Rollback was successful.
	# Override this to perform whatever success checks are necessary.
	def DidRollbackSucceed(this):
		return this.rollbackSucceeded


	# Grab any known and necessary args from this.kwargs before any Fetch calls are made.
	def ParseInitialArgs(this):
		pass


	# Override this with any logic you'd like to run at the top of __call__
	def BeforeFunction(this):
		pass


	# Override this with any logic you'd like to run at the bottom of __call__
	def AfterFunction(this):
		pass

	# Create a list of methods / member functions which will search different places for a variable.
	# See the end of the file for examples of these methods.
	def PopulateFetchLocations(this):
		try:
			for loc in this.fetchFrom:
				this.fetchLocations.update({loc:getattr(this,f"fetch_location_{loc}")})
		except:
			# If the user didn't define fetch_location_{loc}(), that's okay. No need to complain
			pass


	# Convert Fetched values to their proper type.
	# This can also allow for use of {this.val} expression evaluation.
	# If evaluateExpressions is True, this will automatically evaluate any strings containing {} expressions.
	def EvaluateToType(this, value, evaluateExpressions=True):
		if (value is None or value == "None"):
			return None

		if (isinstance(value, (bool, int, float))):
			return value

		if (isinstance(value, dict)):
			ret = util.DotDict()
			for key, val in value.items():
				ret[key] = this.EvaluateToType(val, evaluateExpressions)
			return ret

		if (isinstance(value, list)):
			ret = []
			for val in value:
				ret.append(this.EvaluateToType(val, evaluateExpressions))
			return ret

		if (isinstance(value, str)):
			# Automatically determine if the string is an expression.
			# If it is, evaluate it.
			if (evaluateExpressions and ('{' in value and '}' in value)):
				evaluatedValue = eval(f"f\"{value}\"")
			else:
				evaluatedValue = value

			# Check resulting type and return a casted value.
			# TODO: is there a better way than double cast + comparison?
			if (evaluatedValue.lower() == "false"):
				return False
			elif (evaluatedValue.lower() == "true"):
				return True

			try:
				if (str(float(evaluatedValue)) == evaluatedValue):
					return float(evaluatedValue)
			except:
				pass

			try:
				if (str(int(evaluatedValue)) == evaluatedValue):
					return int(evaluatedValue)
			except:
				pass

			# The type must be a plain-old string.
			return evaluatedValue

		# Meh. Who knows?
		return value


	# Wrapper around setattr
	def Set(this, varName, value, evaluateExpressions=True):
		value = this.EvaluateToType(value, evaluateExpressions)
		for key, var in this.configNameOverrides.items():
			if (varName == key):
				varName = var
				break
		logging.debug(f"Setting ({type(value)}) {varName} = {value}")
		setattr(this, varName, value)


	# Will try to get a value for the given varName from:
	#	first: this
	#	second: whatever was called before *this
	#	third: the executor (args > config > environment)
	# RETURNS:
	#   When starting: the value of the given variable or default
	#   When not starting (i.e. when called from another Fetch() call): a tuple containing either the value of the given variable or default and a boolean indicating if the given value is the default or if the Fetch was successful.
	# The attempted argument will keep track of where we've looked so that we don't enter any cycles. Attempted implies not start.
	def Fetch(this, varName, default=None, fetchFrom=None, start=True, attempted=None):
		if (attempted is None):
			attempted = []

		if (this.name in attempted):
			logging.debug(f"...{this.name} detected loop ({attempted}) while trying to fetch {varName}; using default: {default}.")
			if (start):
				return default
			else:
				return default, False

		attempted.append(this.name)

		if (fetchFrom is None):
			fetchFrom = this.fetchFrom

		if (start):
			logging.debug(f"Fetching {varName} from {fetchFrom}...")

		for loc in fetchFrom:
			if (loc not in this.fetchLocations.keys()):
				# Maybe the location is meant for executor, precursor, etc.
				continue

			ret, found = this.fetchLocations[loc](varName, default, fetchFrom, attempted)
			if (found):
				logging.debug(f"...{this.name} got {varName} from {loc}.")
				if (start):
					return ret
				return ret, True

		if (start):
			logging.debug(f"...{this.name} could not find {varName}; using default: {default}.")
			return default
		else:
			return default, False


	# Ease of use method for Fetching while including certain search locations.
	def FetchWith(this, doFetchFrom, varName, default=None, currentFetchFrom=None, start=True, attempted=None):
		if (currentFetchFrom is None):
			currentFetchFrom = this.fetchFrom
		fetchFrom = list(set(currentFetchFrom + doFetchFrom))
		return this.Fetch(varName, default, fetchFrom, start, attempted)

	# Ease of use method for Fetching while excluding certain search locations.
	def FetchWithout(this, dontFetchFrom, varName, default=None, currentFetchFrom=None, start=True, attempted=None):
		if (currentFetchFrom is None):
			currentFetchFrom = this.fetchFrom
		fetchFrom = [f for f in this.fetchFrom if f not in dontFetchFrom]
		return this.Fetch(varName, default, fetchFrom, start, attempted)

	# Ease of use method for Fetching while including some search location and excluding others.
	def FetchWithAndWithout(this, doFetchFrom, dontFetchFrom, varName, default=None, currentFetchFrom=None, start=True, attempted=None):
		if (currentFetchFrom is None):
			currentFetchFrom = this.fetchFrom
		fetchFrom = [f for f in this.fetchFrom if f not in dontFetchFrom]
		fetchFrom = list(set(fetchFrom + doFetchFrom))
		return this.Fetch(varName, default, fetchFrom, start, attempted)


	# Make sure arguments are not duplicated.
	# This prefers optional args to required args.
	def RemoveDuplicateArgs(this):
		deduplicate = [
			'requiredKWArgs',
			'requiredMethods',
			'requiredPrograms'
		]
		for dedup in deduplicate:
			setattr(this, dedup, list(dict.fromkeys(getattr(this, dedup))))

		for arg in this.requiredKWArgs:
			if (arg in this.optionalKWArgs.keys()):
				logging.warning(f"Making required kwarg optional to remove duplicate: {arg}")
				this.requiredKWArgs.remove(arg)


	# Populate all static details of *this.
	def Initialize(this):
		if (this.initialized):
			return

		this.PopulateFetchLocations()
		this.RemoveDuplicateArgs()

		for prog in this.requiredPrograms:
			if (shutil.which(prog) is None):
				raise FunctorError(f"{prog} required but not found in path.")

		this.initialized = True

	# Make sure all static args are valid.
	def ValidateStaticArgs(this):
		if (this.staticArgsValid):
			return

		for skw in this.staticKWArgs:
			if (hasattr(this, skw)): # only in the case of children.
				continue

			fetched = this.Fetch(skw)
			if (fetched is not None):
				this.Set(skw, fetched)
				continue

			# Nope. Failed.
			raise MissingArgumentError(f"Static key-word argument {skw} could not be Fetched.")

		this.staticArgsValid = True


	# Pull all propagating precursor methods into *this.
	# DO NOT USE Fetch() IN THIS METHOD!
	def PopulateMethods(this):

		# In order for this to work properly, each method needs to be a distinct object; hence the need for deepcopy.
		# In the future, we might be able to find a way to share code objects between Functors. However, for now we will allow each Functor to modify its classmethods as it pleases.

		# We have to use util.___Attr() because some sources might have '.'s in them.

		for source, honorPropagate in this.methodSources.items():
			if (not util.HasAttr(this, source)):
				continue
			for method in util.GetAttr(this, source).values():
				if (honorPropagate and not method.propagate):
					continue
				if (method.name in this.methods.keys() and honorPropagate):
					existingMethod = this.methods[method.name]
					if (not existingMethod.inheritMethods):
						continue

					methodToInsert = deepcopy(method)
					methodToInsert.UpdateSource()

					if (existingMethod.inheritedMethodsFirst):
						logging.debug(f"Will call {method.name} from {source} to prior to this.")
						methodToInsert.next.append(this.methods[method.name])
						this.methods[method.name] = methodToInsert
					else:
						logging.debug(f"Appending {method.name} from {source} to this.")
						this.methods[method.name].next.append(methodToInsert)
				else:
					this.methods[method.name] = deepcopy(method)
					this.methods[method.name].UpdateSource()

		for method in this.methods.values():
			logging.debug(f"Populating method {this.name}.{method.name}({', '.join([a for a in method.requiredKWArgs] + [a+'='+str(v) for a,v in method.optionalKWArgs.items()])})")
			method.object = this

			# Python < 3.11
			# setattr(this, method.name, method.__call__.__get__(this, this.__class__))

			# appears to work for all python versions >= 3.8
			setattr(this, method.name, method.__call__.__get__(method, method.__class__))



# Set this.precursor
	# Also set this.executor because it's easy.
	def PopulatePrecursor(this):
		if (this.executor is None):
			if ('executor' in this.kwargs):
				this.executor = this.kwargs.pop('executor')
			else:
				logging.warning(f"{this.name} was not given an 'executor'. Some features will not be available.")

			if ('precursor' in this.kwargs):
				this.precursor = this.kwargs.pop('precursor')
				logging.debug(f"{this.name} was preceded by {this.precursor.name}")
			else:
				this.precursor = None
				logging.debug(f"{this.name} was preceded by None")


	# Override this with any additional argument validation you need.
	# This is called before BeforeFunction(), below.
	def ValidateArgs(this):
		# logging.debug(f"this.kwargs: {this.kwargs}")
		# logging.debug(f"required this.kwargs: {this.requiredKWArgs}")

		if (len(this.args) > len(this.argMapping)):
			raise MissingArgumentError(f"Too many arguments. Got ({len(this.args)}) {this.args} but expected at most ({len(this.argMapping)}) {this.argMapping}")
		argMap = dict(zip(this.argMapping[:len(this.args)], this.args))
		logging.debug(f"Setting values from args: {argMap}")
		for arg, value in argMap.items():
			this.Set(arg, value)

		#NOTE: In order for *this to be called multiple times, required and optional kwargs must always be fetched and not use stale data from *this.

		if (this.requiredKWArgs):
			for rkw in this.requiredKWArgs:
				if (rkw in argMap.keys()):
					continue

				fetched = this.FetchWithout(['this'], rkw)
				if (fetched is not None):
					this.Set(rkw, fetched)
					continue

				# Nope. Failed.
				logging.error(f"{rkw} required but not found.")
				raise MissingArgumentError(f"Key-word argument {rkw} could not be Fetched.")

		if (this.optionalKWArgs):
			for okw, default in this.optionalKWArgs.items():
				if (okw in argMap.keys()):
					continue

				this.Set(okw, this.FetchWithout(['this'], okw, default=default))

	# When Fetching what to do next, everything is valid EXCEPT the environment. Otherwise, we could do something like `export next='nop'` and never quit.
	# A similar situation arises when using the global config for each Functor. We only use the global config if *this has no precursor.
	def PopulateNext(this):
		dontFetchFrom = [
			'this',
			'environment',
			'executor'
		]
		# Let 'next' evaluate its expressions if it chooses to. We don't need to do that pre-emptively.
		this.Set('next', this.FetchWithout(dontFetchFrom, 'next', []), evaluateExpressions=False)


	# Make sure that precursors have provided all necessary methods for *this.
	# NOTE: these should not be static nor cached, as calling something else before *this will change the behavior of *this.
	def ValidateMethods(this):
		for method in this.requiredMethods:
			if (hasattr(this, method) and callable(getattr(this, method))):
				continue

			raise MissingMethodError(f"{this.name} has no method: {method}")


	# RETURNS whether or not we should trigger the next Functor.
	# Override this to add in whatever checks you need.
	def ValidateNext(this, next):
		return True


	# Hook for whatever logic you'd like to run before the next Functor is called.
	# FIXME: This isn't actually called.
	def PrepareNext(this, next):
		pass


	# Call the next Functor.
	# RETURN the result of the next Functor or None.
	def CallNext(this):
		if (not this.next):
			return None

		if (this.GetExecutor() is None):
			raise InvalidNext(f"{this.name} has no executor and cannot execute next ({this.next}).")

		next = this.next.pop(0)
		if (not this.ValidateNext(next)):
			raise InvalidNext(f"Failed to validate {next}")
		return this.GetExecutor().Execute(next, precursor=this, next=this.next)


	# Make functor.
	# Don't worry about this; logic is abstracted to Function
	def __call__(this, *args, **kwargs) :
		logging.debug(f"<---- {this.name} ---->")

		this.args = args
		this.kwargs = kwargs

		logging.debug(f"{this.name}({this.args}, {this.kwargs})")

		ret = None
		nextRet = None
		try:
			this.PopulatePrecursor()
			this.Initialize() # nop on call 2+
			this.PopulateMethods() # Doesn't require Fetch; depends on precursor
			this.ParseInitialArgs() # Usually where config is read in.
			this.ValidateStaticArgs() # nop on call 2+
			this.PopulateNext()
			this.ValidateArgs()
			this.ValidateMethods()

			this.BeforeFunction()

			ret = this.Function()

			if (this.DidFunctionSucceed()):
					this.result = 1
					# logging.info(f"{this.name} successful!")
					nextRet = this.CallNext()
			elif (this.enableRollback):
				logging.warning(f"{this.name} failed. Attempting Rollback...")
				this.Rollback()
				if (this.DidRollbackSucceed()):
					this.result = 2
					# logging.info(f"Rollback succeeded. All is well.")
					nextRet = this.CallNext()
				else:
					this.result = 3
					logging.error(f"Rollback FAILED! SYSTEM STATE UNKNOWN!!!")
			else:
				this.result = 4
				logging.error(f"{this.name} failed.")

			this.AfterFunction()

		except Exception as e:
			if (this.raiseExceptions):
				raise e
			else:
				logging.error(f"ERROR: {e}")
				util.LogStack()

		if (this.raiseExceptions and this.result > 2):
			raise FunctorError(f"{this.name} failed with result {this.result}")

		logging.debug(f">---- {this.name} complete ----<")
		if (nextRet is not None):
			return nextRet
		else:
			return ret


	# Adapter for @recoverable.
	# See Recoverable.py for details
	def GetExecutor(this):
		return this.executor


	# Add support for deepcopy.
	# Copies everything besides methods; those will be created by PopulateMethods or removed.
	def __deepcopy__(this, memodict=None):
		logging.debug(f"Creating new {this.__class__} from {this.name}")
		cls = this.__class__
		ret = cls.__new__(cls)
		ret.__init__()

		memodict[id(this)] = ret
		for key, val in [tup for tup in this.__dict__.items() if tup[0] not in ['methods']]:
			if (callable(val)):
				# PopulateMethods will take care of recreating skipped Methods
				# All other methods are dropped since they apparently have problems on some implementations.
				continue
			setattr(ret, key, deepcopy(val, memodict))
		return ret


	######## START: Fetch Locations ########

	def fetch_location_this(this, varName, default, fetchFrom, attempted):
		if (hasattr(this, varName)):
			return getattr(this, varName), True
		return default, False


	def fetch_location_precursor(this, varName, default, fetchFrom, attempted):
		if (this.precursor is None):
			return default, False
		return this.precursor.FetchWithAndWithout(['this'], ['environment'], varName, default, fetchFrom, False, attempted)


	def fetch_location_args(this, varName, default, fetchFrom, attempted):

		# this.args can't be searched.

		for key, val in this.kwargs.items():
			if (key == varName):
				return val, True
		return default, False


	# Call the Executor's Fetch method.
	# Exclude 'environment' because we can check that ourselves.
	def fetch_location_executor(this, varName, default, fetchFrom, attempted):
		return this.GetExecutor().FetchWithout(['environment'], varName, default, fetchFrom, False, attempted)


	#NOTE: There is no config in the default Functor. This is done for the convenience of children.
	def fetch_location_config(this, varName, default, fetchFrom, attempted):
		if (not hasattr(this, 'config') or this.config is None):
			return default, False

		for key, val in this.config.items():
			if (key == varName):
				return val, True

		return default, False


	def fetch_location_environment(this, varName, default, fetchFrom, attempted):
		envVar = os.getenv(varName)
		if (envVar is not None):
			return envVar, True
		return default, False

	######## END: Fetch Locations ########


def METHOD_PENDING_POPULATION(obj, *args, **kwargs):
	raise MethodPendingPopulation("METHOD PENDING POPULATION")

# Use the @method() decorator to turn any class function into an eons Method Functor.
# Methods are Functors which can be implicitly transferred between classes (see Functor.PopulateMethods)
# Using Methods also gives us full control over the execution of your code; meaning, we can change how Python interprets what you wrote!
# All Methods will be stored in the method member of your Functor. However, you shouldn't need to access that.
#
# If you would like to specify a custom implementation, set the 'impl' kwarg (e.g. @method(impl='MyMethodImplementation'))
# Beside 'impl', all key-word arguments provided to the @method() decorator will be set as member variables of the created Method.
# For example, to set whether or not the Method should be propagated, you can use @method(propagate=True).
# This means, you can create a custom means of interpreting your code with your own feature set and still use this @method decorator.
# Perhaps you'd like something along the lines of: @method(impl='MakeAwesome', awesomeness=10000).
# NOTE: in order for impl to work, the implementation class must already be Registered (or this must be called from an appropriate @recoverable function).
def method(impl='Method', **kwargs):

	# Class decorator with __set_name__, as described here: https://stackoverflow.com/questions/2366713/can-a-decorator-of-an-instance-method-access-the-class
	class MethodDecorator:
		def __init__(this, function):
			this.function = function

		# Apparently, this is called when the decorated function is constructed.
		def __set_name__(this, cls, functionName):
			logging.debug(f"Constructing new method for {this.function} in {cls}")

			# Create and configure a new Method

			method = SelfRegistering(impl)
			method.Constructor(this.function, cls)
			for key, value in kwargs.items():
				setattr(method, key, value)

			# Store the new method in the class
			if (not hasattr(cls, 'classMethods') or not isinstance(cls.classMethods, dict)):
				cls.classMethods = {}
			cls.classMethods[functionName] = method

			# Self-destruct by replacing the decorated function.
			# We rely on Functor.PopulateMethods to re-establish the method as callable.
			# It seems like this just outright removes the methods. There may be an issue with using __get__ this way.
			# Regardless deleting the method is okay as long as we add it back before anyone notices.
			setattr(cls, functionName, METHOD_PENDING_POPULATION.__get__(cls))

	return MethodDecorator

class Method(Functor):

	def __init__(this, name=INVALID_NAME()):
		super().__init__(name)

		# Whether or not *this should be combined with other Methods of the same name.
		this.inheritMethods = True

		# Where should inherited methods be inserted?
		# First here means "before *this".
		# If False, inherited code will be run after *this.
		this.inheritedMethodsFirst = True # otherwise ...Last

		# Propagation allows for Functors called after that which defines *this to also call *this.
		# This system allows for partial, implicit inheritance.
		# By default, Methods will not be propagated. Use @propagate to enable propagation.
		this.propagate = False

		# We don't care about these checks right now.
		# Plus, we can't exactly wrap 2 functions even if we wanted to Rollback.
		this.functionSucceeded = True
		this.rollbackSucceeded = True
		this.enableRollback = False

		# The source code of the function we're implementing.
		this.source = ""

		# The instance of the class to which *this belongs.
		# i.e. the object that called *this, aka 'owner', 'caller', etc.
		this.object = None

		this.original = util.DotDict()
		this.original.cls = None
		this.original.function = None


	# Make *this execute the code in this.source
	def UpdateSource(this):
		wrappedFunctionName = f'_eons_method_{this.name}'
		completeSource = f'''\
def {wrappedFunctionName}(this):
{this.source}
'''
		if (this.executor and this.executor.verbosity > 3):
			logging.debug(f"Source for {this.name} is:\n{completeSource}")
		code = compile(completeSource, '', 'exec')
		exec(code)
		exec(f'this.Function = {wrappedFunctionName}.__get__(this, this.__class__)')

	# Parse arguments and update the source code
	# TODO: Implement full python parser to avoid bad string replacement (e.g. "def func(self):... self.selfImprovement" => "... this.object.this.object.Improvement").
	def PopulateFrom(this, function):
		this.source = ':'.join(inspect.getsource(function).split(':')[1:]) #Remove the first function definition

		args = inspect.signature(function, follow_wrapped=False).parameters
		thisSymbol = next(iter(args))
		#del args[thisSymbol] # ??? 'mappingproxy' object does not support item deletion
		this.source = this.source.replace(thisSymbol, 'this.object')

		first = True
		for arg in args.values(): #args.values[1:] also doesn't work.
			if (first):
				first = False
				continue

			replaceWith = arg.name

			if (arg.kind == inspect.Parameter.VAR_POSITIONAL):
				replaceWith = 'this.args'

			elif (arg.kind == inspect.Parameter.VAR_KEYWORD):
				replaceWith = 'this.kwargs'

			else:
				if (arg.default != inspect.Parameter.empty):
					this.optionalKWArgs[arg.name] = arg.default
				else:
					this.requiredKWArgs.append(arg.name)
				replaceWith = f'this.{arg.name}'

				if (arg.kind in [inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.POSITIONAL_ONLY]):
					this.argMapping.append(arg.name)

			this.source = this.source.replace(arg.name, replaceWith)


	# When properly constructing a Method, rely only on the function *this should implement.
	# The class and all other properties are irrelevant. However, they are provided and intended for debugging only.
	def Constructor(this, function, cls):
		this.name = function.__name__
		this.original.cls = cls
		this.original.function = function

		this.PopulateFrom(function)
		this.UpdateSource()


	# Grab any known and necessary args from this.kwargs before any Fetch calls are made.
	def PopulatePrecursor(this):
		if (not this.object):
			raise MissingArgumentError(f"Call {this.name} from a class instance: {this.original.cls.__name__}.{this.name}(...). Maybe Functor.PopulateMethods() hasn't been called yet?")

		this.executor = this.object.executor

		if ('precursor' in this.kwargs):
			this.precursor = this.kwargs.pop('precursor')
		else:
			this.precursor = None


	# Next is set by Functor.PopulateMethods.
	# We  definitely don't want to Fetch 'next'.
	def PopulateNext(this):
		pass


	# Method.next should be a list of other Methods, as opposed to the standard string; so, instead of Executor.Execute..., we can directly invoke whatever is next.
	# We skip all validation here.
	# We also don't pass any args that were given in the initial function call. Those can all be Fetched from 'precursor'.
	def CallNext(this):
		if (not this.next):
			return None

		for next in this.next:
			next(precursor=this)


# ExecutorTracker is a global singleton which keeps a record of all Executors that have been launched.
# This can be abused quite a bit, so please try to restrict usage of this to only:
# * Ease of use global functions
#
# Thanks! 
class ExecutorTracker:
	def __init__(this):
		# Singletons man...
		if "instance" not in ExecutorTracker.__dict__:
			logging.debug(f"Creating new ExecutorTracker: {this}")
			ExecutorTracker.instance = this
		else:
			return None

		this.executors = [None]

	@staticmethod
	def Instance():
		if "instance" not in ExecutorTracker.__dict__:
			ExecutorTracker()
		return ExecutorTracker.instance

	@staticmethod
	def Push(executor):
		ExecutorTracker.Instance().executors.append(executor)

		# Adding the executor to our list here increases its reference count.
		# Executors are supposed to remove themselves from this list when they are deleted.
		# A python object cannot be deleted if it has references.
		# Thus, we forcibly decrease the reference count and rely on Exectuor's self-reporting to avoid accessing deallocated memory.
		# This appears to cause segfaults on some systems, so we'll just live with the fact that Executors will never be destroyed.
		# If you want your executor to stop being tracked, do it yourself. :(
		#
		# ctypes.pythonapi.Py_DecRef(ctypes.py_object(executor))

		logging.debug(f"Now tracking Executor: {executor}")

	@staticmethod
	def Pop(executor):
		try:
			ExecutorTracker.Instance().executors.remove(executor)
			logging.debug(f"No longer tracking Executor: {executor}")
		except:
			pass

	@staticmethod
	def GetLatest():
		return ExecutorTracker.Instance().executors[-1]


# Global Fetch() function.
# Uses the latest registered Executor
def Fetch(varName, default=None, fetchFrom=None, start=True, attempted=None):
    return ExecutorTracker.GetLatest().Fetch(varName, default, fetchFrom, start, attempted)

# Ease-of-use wrapper for the global Fetch()
def f(varName, default=None, fetchFrom=None, start=True, attempted=None):
    Fetch(varName, default, fetchFrom, start, attempted)

# The standard Functor extends Functor to add a set of standard members and methods.
# This is similar to the standard library in C and C++
# You must inherit from *this if you would like to use the functionality *this provides. The methods defined will not be propagated.
class StandardFunctor(Functor):
	def __init__(this, name="Standard Functor"):
		super().__init__(name)

	# Override this and do whatever!
	# This is purposefully vague.
	def Function(this):
		pass


	# Undo any changes made by UserFunction.
	# Please override this too!
	def Rollback(this):
		pass


	# Override this to check results of operation and report on status.
	# Override this to perform whatever success checks are necessary.
	def DidFunctionSucceed(this):
		return this.functionSucceeded


	# RETURN whether or not the Rollback was successful.
	# Override this to perform whatever success checks are necessary.
	def DidRollbackSucceed(this):
		return this.rollbackSucceeded


	######## START: UTILITIES ########

	# RETURNS: an opened file object for writing.
	# Creates the path if it does not exist.
	@method()
	def CreateFile(this, file, mode="w+"):
		Path(os.path.dirname(os.path.abspath(file))).mkdir(parents=True, exist_ok=True)
		return open(file, mode)

	# Copy a file or folder from source to destination.
	# This really shouldn't be so hard...
	# root allows us to interpret '/' as something other than the top of the filesystem.
	@method()
	def Copy(this, source, destination, root='/'):
		if (source.startswith('/')):
			source = str(Path(root).joinpath(source[1:]).resolve())
		else:
			source = str(Path(source).resolve())
		
		destination = str(Path(destination).resolve())
		
		Path(destination).parent.mkdir(parents=True, exist_ok=True)

		if (os.path.isfile(source)):
			logging.debug(f"Copying file {source} to {destination}")
			try:
				shutil.copy(source, destination)
			except shutil.Error as exc:
				errors = exc.args[0]
				for error in errors:
					src, dst, msg = error
					logging.debug(f"{msg}")
		elif (os.path.isdir(source)):
			logging.debug(f"Copying directory {source} to {destination}")
			try:
				shutil.copytree(source, destination)
			except shutil.Error as exc:
				errors = exc.args[0]
				for error in errors:
					src, dst, msg = error
					logging.debug(f"{msg}")
		else:
			logging.error(f"Could not find source to copy: {source}")

	# Delete a file or folder
	@method()
	def Delete(this, target):
		if (not os.path.exists(target)):
			logging.debug(f"Unable to delete nonexistent target: {target}")
			return
		if (os.path.isfile(target)):
			logging.debug(f"Deleting file {target}")
			os.remove(target)
		elif (os.path.isdir(target)):
			logging.debug(f"Deleting directory {target}")
			try:
				shutil.rmtree(target)
			except shutil.Error as exc:
				errors = exc.args[0]
				for error in errors:
					src, dst, msg = error
					logging.debug(f"{msg}")

	# Run whatever.
	# DANGEROUS!!!!!
	# RETURN: Return value and, optionally, the output as a list of lines.
	@method()
	def RunCommand(this, command, saveout=False, raiseExceptions=True):
		logging.debug(f"================ Running command: {command} ================")
		p = Popen(command, stdout=PIPE, stderr=STDOUT, shell=True)
		output = []
		while p.poll() is None:
			line = p.stdout.readline().decode('utf8')[:-1]
			if (saveout):
				output.append(line)
			if (line):
				logging.debug(f"| {line}")  # [:-1] to strip excessive new lines.

		if (p.returncode is not None and p.returncode):
			raise CommandUnsuccessful(f"Command returned {p.returncode}: {command}")
		
		logging.debug(f"================ Completed command: {command} ================")
		if (saveout):
			return p.returncode, output
		
		return p.returncode
	######## END: UTILITIES ########


# Use an ErrorStringParser for each "parsers" in order to avoid having to override the GetObjectFromError method and create a new class for every error you want to handle.
# ErrorStringParsers enable ErrorResolutions to be created on a per-functionality, rather than per-error basis, reducing the total amount of duplicate code.
# Each error has a different string. In order to get the object of the error, we have to know where the object starts and ends.
# NOTE: this assumes only 1 object per string. Maybe fancier parsing logic can be added in the future.
#
# startPosition is always positive
# endPosition is always negative
class ErrorStringParser:

	def __init__(this, applicableError, startPosition, endPosition):
		this.applicableError = applicableError
		this.startPosition = startPosition
		this.endPosition = endPosition

	def Parse(this, errorString):
		end = this.endPosition
		if (not end):
			end = len(errorString)
		return errorString[this.startPosition:end]


# ErrorResolution is a Functor which can be executed when an Exception is raised.
# The goal of this class is to do some kind of work that will fix the problem on the second try of whatever generated the error.
class ErrorResolution(StandardFunctor):

	def __init__(this, name=INVALID_NAME()):
		super().__init__(name)

		# What errors, as ErrorStringParser objects, is *this prepared to handle?
		this.parsers = []

		this.error = None
		this.errorType = ""
		this.errorString = ""
		this.errorObject = ""
		this.errorResolutionStack = {}

		# Provided directly from the recoverable decorator.
		this.optionalKWArgs["obj"] = None
		this.optionalKWArgs["function"] = None

		# We do want to know whether or not we should attempt to run whatever failed again.
		# So, let's store that in functionSucceeded. Meaning if this.functionSucceeded, try the original method again.
		# No rollback, by default and definitely don't throw Exceptions.
		this.enableRollback = False
		this.functionSucceeded = True
		this.raiseExceptions = False

		this.errorShouldBeResolved = False



	# Put your logic here!
	def Resolve(this):
		# You get the following members:
		# this.error (an Exception)
		# this.errorString (a string cast of the Exception)
		# this.errorType (a string)
		# this.errorObjet (a string or whatever you return from GetObjectFromError())

		# You get the following guarantees:
		# *this has not been called on this particular error before.
		# the error given is applicable to *this per this.parsers

		###############################################
		# Please throw errors if something goes wrong #
		# Otherwise, set this.errorShouldBeResolved   #
		###############################################
		
		pass



	# Helper method for creating ErrorStringParsers
	# To use this, simply take an example output and replace the object you want to extract with "OBJECT"
	def ApplyTo(this, error, exampleString):
		match = re.search('OBJECT', exampleString)
		this.parsers.append(ErrorStringParser(error, match.start(), match.end() - len(exampleString)))


	# Get the type of this.error as a string.
	def GetErrorType(this):
		return type(this.error).__name__


	# Get an actionable object from the error.
	# For example, if the error is 'ModuleNotFoundError', what is the module?
	def GetObjectFromError(this):
		for parser in this.parsers:
			if (parser.applicableError != this.errorType):
				continue

			this.errorObject = parser.Parse(this.errorString)
			return

		raise ErrorResolutionError(f"{this.name} cannot parse error object from ({this.errorType}): {str(this.error)}.")


	# Determine if this resolution method is applicable.
	def CanProcess(this):
		return this.GetErrorType() in [parser.applicableError for parser in this.parsers]


	# Grab any known and necessary args from this.kwargs before any Fetch calls are made.
	def ParseInitialArgs(this):
		super().ParseInitialArgs()
		if ('error' in this.kwargs):
			this.error = this.kwargs.pop('error')
			# Just assume the error is an actual Exception object.
		else:
			raise ErrorResolutionError(f"{this.name} was not given an error to resolve.")

		this.errorString = str(this.error)
		this.errorType = this.GetErrorType()

		# Internal member to avoid processing duplicates
		this.errorResolutionStack = this.executor.errorResolutionStack


	# Error resolution is unchained.
	def PopulateNext(this):
		this.next = []


	# Override of Functor method.
	# We'll keep calling this until an error is raised.
	def Function(this):
		this.functionSucceeded = True
		this.errorShouldBeResolved = True
		
		if (not this.CanProcess()):
			this.errorShouldBeResolved = False
			return this.errorResolutionStack, this.errorShouldBeResolved

		if (not this.errorString in this.errorResolutionStack.keys()):
			this.errorResolutionStack.update({this.errorString:[]})
		
		if (this.name in this.errorResolutionStack[this.errorString]):
			raise FailedErrorResolution(f"{this.name} already tried and failed to resolve {this.errorType}: {this.errorString}.")

		this.GetObjectFromError()

		try:
			this.Resolve()
		except Exception as e:
			logging.error(f"Error resolution with {this.name} failed: {e}")
			util.LogStack()
			this.functionSucceeded = False
		
		this.errorResolutionStack[this.errorString].append(this.name)
		return this.errorResolutionStack, this.errorShouldBeResolved


# A DataContainer allows Data to be stored and worked with.
# This class is intended to be derived from and added to.
# Each DataContainer is comprised of multiple Data (see Datum.py for more).
# NOTE: DataContainers are, themselves Data. Thus, you can nest your child classes however you would like.
class DataContainer(Datum):

	def __init__(this, name=INVALID_NAME()):
		super().__init__(name)

		# The data *this contains.
		this.data = []


	# RETURNS: an empty, invalid Datum.
	def InvalidDatum(this):
		ret = Datum()
		ret.Invalidate()
		return ret


	# Sort things! Requires by be a valid attribute of all Data.
	def SortData(this, by):
		this.data.sort(key=operator.attrgetter(by))


	# Adds a Datum to *this
	def AddDatum(this, datum):
		this.data.append(datum)


	# RETURNS: a Datum with datumAttribute equal to match, an invalid Datum if none found.
	def GetDatumBy(this, datumAttribute, match):
		for d in this.data:
			try: # within for loop 'cause maybe there's an issue with only 1 Datum and the rest are fine.
				if (str(getattr(d, datumAttribute)) == str(match)):
					return d
			except Exception as e:
				logging.error(f"{this.name} - {e.message}")
				continue
		return this.InvalidDatum()


	# RETURNS: a Datum of the given name, an invalid Datum if none found.
	def GetDatum(this, name):
		return this.GetDatumBy('name', name)


	# Removes all Data in toRem from *this.
	# RETURNS: the Data removed
	def RemoveData(this, toRem):
		# logging.debug(f"Removing {toRem}")
		this.data = [d for d in this.data if d not in toRem]
		return toRem


	# Removes all Data which match toRem along the given attribute
	def RemoveDataBy(this, datumAttribute, toRem):
		toRem = [d for d in this.data if str(getattr(d, datumAttribute)) in list(map(str, toRem))]
		return this.RemoveData(toRem)


	# Removes all Data in *this except toKeep.
	# RETURNS: the Data removed
	def KeepOnlyData(this, toKeep):
		toRem = [d for d in this.data if d not in toKeep]
		return this.RemoveData(toRem)


	# Removes all Data except those that match toKeep along the given attribute
	# RETURNS: the Data removed
	def KeepOnlyDataBy(this, datumAttribute, toKeep):
		# logging.debug(f"Keeping only class with a {datumAttribute} of {toKeep}")
		# toRem = []
		# for d in this.class:
		#	 shouldRem = False
		#	 for k in toKeep:
		#		 if (str(getattr(d, datumAttribute)) == str(k)):
		#			 logging.debug(f"found {k} in {d.__dict__}")
		#			 shouldRem = True
		#			 break
		#	 if (shouldRem):
		#		 toRem.append(d)
		#	 else:
		#		 logging.debug(f"{k} not found in {d.__dict__}")
		toRem = [d for d in this.data if str(getattr(d, datumAttribute)) not in list(map(str, toKeep))]
		return this.RemoveData(toRem)


	# Removes all Data with the name "INVALID NAME"
	# RETURNS: the removed Data
	def RemoveAllUnlabeledData(this):
		toRem = []
		for d in this.data:
			if (d.name =="INVALID NAME"):
				toRem.append(d)
		return this.RemoveData(toRem)


	# Removes all invalid Data
	# RETURNS: the removed Data
	def RemoveAllInvalidData(this):
		toRem = []
		for d in this.data:
			if (not d.IsValid()):
				toRem.append(d)
		return this.RemoveData(toRem)


	# Removes all Data that have an attribute value relative to target.
	# The given relation can be things like operator.le (i.e. <=)
	#   See https://docs.python.org/3/library/operator.html for more info.
	# If ignoreNames is specified, any Data of those names will be ignored.
	# RETURNS: the Data removed
	def RemoveDataRelativeToTarget(this, datumAttribute, relation, target, ignoreNames = []):
		try:
			toRem = []
			for d in this.data:
				if (ignoreNames and d.name in ignoreNames):
					continue
				if (relation(getattr(d, datumAttribute), target)):
					toRem.append(d)
			return this.RemoveData(toRem)
		except Exception as e:
			logging.error(f"{this.name} - {e.message}")
			return []


	# Removes any Data that have the same datumAttribute as a previous Datum, keeping only the first.
	# RETURNS: The Data removed
	def RemoveDuplicateDataOf(this, datumAttribute):
		toRem = [] # list of Data
		alreadyProcessed = [] # list of strings, not whatever datumAttribute is.
		for d1 in this.data:
			skip = False
			for dp in alreadyProcessed:
				if (str(getattr(d1, datumAttribute)) == dp):
					skip = True
					break
			if (skip):
				continue
			for d2 in this.data:
				if (d1 is not d2 and str(getattr(d1, datumAttribute)) == str(getattr(d2, datumAttribute))):
					logging.info(f"Removing duplicate Datum {d2} with unique id {getattr(d2, datumAttribute)}")
					toRem.append(d2)
					alreadyProcessed.append(str(getattr(d1, datumAttribute)))
		return this.RemoveData(toRem)


	# Adds all Data from otherDataContainer to *this.
	# If there are duplicate Data identified by the attribute preventDuplicatesOf, they are removed.
	# RETURNS: the Data removed, if any.
	def ImportDataFrom(this, otherDataContainer, preventDuplicatesOf=None):
		this.data.extend(otherDataContainer.data);
		if (preventDuplicatesOf is not None):
			return this.RemoveDuplicateDataOf(preventDuplicatesOf)
		return []


#from .Executor import Executor # don't import this, it'll be circular!

# @recoverable
# Decorating another function with this method will engage the error recovery system provided by *this.
# To use this, you must define a GetExecutor() method in your class and decorate the functions you want to recover from.
# For more info, see Executor.ResolveError and the README.md
def recoverable(function):
	def RecoverableDecorator(obj, *args, **kwargs):
		return RecoverableImplementation(obj, obj.GetExecutor(), function, *args, **kwargs)
	return RecoverableDecorator


# This needs to be recursive, so rather than having the recoverable decorator call or decorate itself, we just break the logic into this separate method.
def RecoverableImplementation(obj, executor, function, *args, **kwargs):
	try:
		return function(obj, *args, **kwargs)
	except FailedErrorResolution as fatal:
		raise fatal
	except Exception as e:
		if (not executor.resolveErrors):
			raise e

		logging.warning(f"Got error '{e}' from function ({function}) by {obj.name}.")
		util.LogStack()

		# We have to use str(e) instead of pointers to Exception objects because multiple Exceptions will have unique addresses but will still be for the same error, as defined by string comparison.
		if (str(e) not in executor.errorResolutionStack.keys()):
			executor.errorResolutionStack.update({str(e):[]})

		# ResolveError should be the only method which adds to executor.errorResolutionStack.
		# ResolveError is itself @recoverable.
		# So, each time we hit this point, we should also hit a corresponding ClearErrorResolutionStack() call. 
		# If we do not, an exception is passed to the caller; if we do, the stack will be cleared upon the last resolution.
		executor.errorRecursionDepth = executor.errorRecursionDepth + 1

		if (executor.errorRecursionDepth > len(executor.errorResolutionStack.keys())+1):
			raise FailedErrorResolution(f"Hit infinite loop trying to resolve errors. Recursion depth: {executor.errorRecursionDepth}; STACK: {executor.errorResolutionStack}.")

		for i, res in enumerate(executor.resolveErrorsWith):

			logging.debug(f"Checking if {res} can fix '{e}'.")
			if (not executor.ResolveError(e, i, obj, function)): # attempt to resolve the issue; might cause us to come back here with a new error.
				# if no resolution was attempted, there's no need to re-run the function.
				continue
			try:
				logging.debug(f"Trying function ({function}) again after applying {res}.")
				ret = function(obj, *args, **kwargs)
				executor.ClearErrorResolutionStack(str(e)) # success!
				logging.recovery(f"{res} successfully resolved '{e}'!")
				logging.debug(f"Error stack is now: {executor.errorResolutionStack}")
				return ret
			except Exception as e2:
				logging.debug(f"{res} failed with '{e2}'; will ignore and see if we can use another ErrorResolution to resolve '{e}'.")
				# Resolution failed. That's okay. Let's try the next.
				# Not all ErrorResolutions will apply to all errors, so we may have to try a few before we get one that works.
				pass

		#  We failed to resolve the error. Die
		sys.tracebacklimit = 0 # traceback is NOT helpful here.
		raise FailedErrorResolution(f"Tried and failed to resolve: {e} STACK: {executor.errorResolutionStack}. See earlier logs (in debug) for traceback.")


# Executor: a base class for user interfaces.
# An Executor is a functor and can be executed as such.
# For example
#	class MyExecutor(Executor):
#		def __init__(this):
#			super().__init__()
#	. . .
#	myprogram = MyExecutor()
#	myprogram()
# NOTE: Diamond inheritance of Datum.
class Executor(DataContainer, Functor):

	def __init__(this, name=INVALID_NAME(), descriptionStr="eons python framework. Extend as thou wilt."):
		this.SetupLogging()

		super().__init__(name)

		# Error resolution configuration.
		this.resolveErrors = True
		this.errorRecursionDepth = 0
		this.errorResolutionStack = {}
		this.resolveErrorsWith = [ # order matters: FIFO (first is first).
			"find_by_fetch",
			'install_from_repo',
			'install_with_pip'
		]

		# Caching is required for Functor's staticKWArgs and other static features to be effective.
		# This is used in Execute().
		this.cachedFunctors = {}

		# General system info
		this.cwd = os.getcwd()
		this.syspath = sys.path  # not used atm.

		# CLI (or otherwise) args
		this.argparser = argparse.ArgumentParser(description = descriptionStr)
		this.parsedArgs = None
		this.extraArgs = None
		
		# How much information should we output?
		this.verbosity = 0

		# config is loaded with the contents of a JSON config file specified by --config / -c or by the defaultConfigFile location, below.
		this.config = None
		this.currentConfigKey = None # used for big, nested configs.

		# Where should we log to?
		# Set by Fetch('log_file')
		this.log_file = None

		# All repository configuration.
		this.repo = util.DotDict()

		# Defaults.
		# You probably want to configure these in your own Executors.
		this.defaultRepoDirectory = os.path.abspath(os.path.join(os.getcwd(), "./eons/"))
		this.registerDirectories = []
		this.defaultConfigFile = None
		this.defaultPackageType = ""

		# Track *this globally
		ExecutorTracker.Instance().Push(this)

		this.Configure()
		this.RegisterIncludedClasses()
		this.AddArgs()

	# Destructors do not work reliably in python.
	# NOTE: you CANNOT delete *this without first Pop()ing it from the ExecutorTracker.
	# def __del__(this):
	# 	ExecutorTracker.Instance().Pop(this)


	# Adapter for @recoverable.
	# See Recoverable.py for details
	def GetExecutor(this):
		return this


	# this.errorResolutionStack are whatever we've tried to do to fix whatever our problem is.
	# This method resets our attempts to remove stale data.
	def ClearErrorResolutionStack(this, force=False):
		if (force):
			this.errorRecursionDepth = 0

		if (this.errorRecursionDepth):
			this.errorRecursionDepth = this.errorRecursionDepth - 1

		if (not this.errorRecursionDepth):
			this.errorResolutionStack = {}


	# Configure class defaults.
	# Override this to customize your Executor.
	def Configure(this):
		this.fetchFrom.remove('executor') # No no no no!
		this.fetchFrom.remove('precursor') # Not applicable here.

		# Usually, Executors shunt work off to other Functors, so we leave these True unless a child needs to check its work.
		this.functionSucceeded = True
		this.rollbackSucceeded = True


	# Add a place to search for SelfRegistering classes.
	# These should all be relative to the invoking working directory (i.e. whatever './' is at time of calling Executor())
	def RegisterDirectory(this, directory):
		this.registerDirectories.append(os.path.abspath(os.path.join(this.cwd,directory)))


	# Global logging config.
	# Override this method to disable or change.
	# This method will add a 'setupBy' member to the root logger in order to ensure no one else (e.g. another Executor) tries to reconfigure the logger while we're using it.
	# The 'setupBy' member will be removed from the root logger by TeardownLogging, which is called in AfterFunction().
	def SetupLogging(this):
		try:
			util.AddLoggingLevel('recovery', logging.ERROR+1)
		except:
			# Could already be setup.
			pass

		class CustomFormatter(logging.Formatter):

			preFormat = util.console.GetColorCode('white', 'dark') + '%(asctime)s'
			format = ' [%(levelname)4s] %(message)s '
			postFormat = util.console.GetColorCode('white', 'dark') + '(%(filename)s:%(lineno)s)' + util.console.resetStyle

			formats = {
				logging.DEBUG: preFormat + util.console.GetColorCode('cyan', 'dark') + format + postFormat,
				logging.INFO: preFormat + util.console.GetColorCode('white', 'light') + format + postFormat,
				logging.WARNING: preFormat + util.console.GetColorCode('yellow', 'light') + format + postFormat,
				logging.ERROR: preFormat + util.console.GetColorCode('red', 'dark') + format + postFormat,
				logging.RECOVERY: preFormat + util.console.GetColorCode('green', 'light') + format + postFormat,
				logging.CRITICAL: preFormat + util.console.GetColorCode('red', 'light', styles=['bold']) + format + postFormat
			}

			def format(this, record):
				log_fmt = this.formats.get(record.levelno)
				formatter = logging.Formatter(log_fmt, datefmt = '%H:%M:%S')
				return formatter.format(record)

		# Skip setting up logging if it's already been done.
		if (hasattr(logging.getLogger(), 'setupBy')):
			return

		logging.getLogger().handlers.clear()
		stderrHandler = logging.StreamHandler()
		stderrHandler.setLevel(logging.CRITICAL)
		stderrHandler.setFormatter(CustomFormatter())
		logging.getLogger().addHandler(stderrHandler)
		setattr(logging.getLogger(), 'setupBy', this)


	# Global logging de-config.
	def TeardownLogging(this):
		if (not hasattr(logging.getLogger(), 'setupBy')):
			return
		if (not logging.getLogger().setupBy == this):
			return
		delattr(logging.getLogger(), 'setupBy')



	# Logging to stderr is easy, since it will always happen.
	# However, we also want the user to be able to log to a file, possibly set in the config.json, which requires a Fetch().
	# Thus, setting up the log file handler has to occur later than the initial SetupLogging call.
	# Calling this multiple times will add multiple log handlers.
	def SetLogFile(this):
		this.Set('log_file', this.Fetch('log_file', None, ['args', 'config', 'environment']))
		if (this.log_file is None):
			return

		log_filePath = Path(this.log_file).resolve()
		if (not log_filePath.exists()):
			log_filePath.parent.mkdir(parents=True, exist_ok=True)
			log_filePath.touch()

		this.log_file = str(log_filePath) # because resolve() is nice.
		logging.info(f"Will log to {this.log_file}")

		logFormatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s (%(filename)s:%(lineno)s)')
		fileHandler = logging.FileHandler(this.log_file)
		fileHandler.setFormatter(logFormatter)
		fileHandler.setLevel(logging.DEBUG)
		logging.getLogger().addHandler(fileHandler)


	# Adds command line arguments.
	# Override this method to change. Optionally, call super().AddArgs() within your method to simply add to this list.
	def AddArgs(this):
		this.argparser.add_argument('--verbose', '-v', action='count', default=0)
		this.argparser.add_argument('--config', '-c', type=str, default=None, help='Path to configuration file containing only valid JSON.', dest='config')

		# We'll use Fetch instead
		# this.argparser.add_argument('--log', '-l', type=str, default=None, help='Path to log file.', dest='log')
		# this.argparser.add_argument('--no-repo', action='store_true', default=False, help='prevents searching online repositories', dest='no_repo')


	# Create any sub-class necessary for child-operations
	# Does not RETURN anything.
	def InitData(this):
		pass


	# Register included files early so that they can be used by the rest of the system.
	# If we don't do this, we risk hitting infinite loops because modular functionality relies on these modules.
	# NOTE: this method needs to be overridden in all children which ship included Functors, Data, etc. This is because __file__ is unique to the eons.py file, not the child's location.
	def RegisterIncludedClasses(this):
		includePaths = [
			'resolve',
		]
		for path in includePaths:
			this.RegisterAllClassesInDirectory(str(Path(__file__).resolve().parent.joinpath(path)))


	# Executors should not have precursors
	def PopulatePrecursor(this):
		this.executor = this
		pass


	# Register all classes in each directory in this.registerDirectories
	def RegisterAllClasses(this):
		for d in this.registerDirectories:
			this.RegisterAllClassesInDirectory(os.path.join(os.getcwd(), d))
		this.RegisterAllClassesInDirectory(this.repo.store)


	# Populate the configuration details for *this.
	def PopulateConfig(this):
		this.config = None

		if (this.parsedArgs.config is None):
			this.parsedArgs.config = this.defaultConfigFile

		logging.debug(f"Populating config from {this.parsedArgs.config}")

		if (this.parsedArgs.config is None):
			return

		if (not os.path.isfile(this.parsedArgs.config)):
			logging.error(f"Could not open configuration file: {this.parsedArgs.config}")
			return

		configFile = open(this.parsedArgs.config, "r")
		this.config = jsonpickle.decode(configFile.read())
		configFile.close()


	#  Get information for how to download packages.
	def PopulateRepoDetails(this):
		details = {
			"online": not this.Fetch('no_repo', False, ['this', 'args', 'config']),
			"store": this.defaultRepoDirectory,
			"url": "https://api.infrastructure.tech/v1/package",
			"username": None,
			"password": None
		}
		for key, default in details.items():
			this.repo[key] = this.Fetch(f"repo_{key}", default=default)


	# How do we get the verbosity level and what do we do with it?
	# This method should set log levels, etc.
	def SetVerbosity(this, fetch=True):

		if (fetch):
			# Take the highest of -v vs --verbosity
			verbosity = this.EvaluateToType(this.Fetch('verbosity', 0, ['args', 'config', 'environment']))
			if (verbosity > this.verbosity):
				logging.debug(f"Setting verbosity to {verbosity}") # debug statements will be available when using external systems, like pytest.
				this.verbosity = verbosity

		if (this.verbosity == 1):
			logging.getLogger().handlers[0].setLevel(logging.WARNING)
			logging.getLogger().setLevel(logging.WARNING)
		elif (this.verbosity == 2):
			logging.getLogger().handlers[0].setLevel(logging.INFO)
			logging.getLogger().setLevel(logging.INFO)
		elif(this.verbosity >= 3):
			logging.getLogger().handlers[0].setLevel(logging.DEBUG)
			logging.getLogger().setLevel(logging.DEBUG)


	# Do the argparse thing.
	# Extra arguments are converted from --this-format to this_format, without preceding dashes. For example, --repo-url ... becomes repo_url ...
	# NOTE: YOU CANNOT USE @recoverable METHODS HERE!
	def ParseArgs(this):
		this.parsedArgs, extraArgs = this.argparser.parse_known_args()

		this.verbosity = this.parsedArgs.verbose

		# If verbosity was specified on the command line, let's print more info while reading in the config, etc.
		this.SetVerbosity(False)

		extraArgsKeys = []
		for index in range(0, len(extraArgs), 2):
			keyStr = extraArgs[index]
			keyStr = keyStr.replace('--', '').replace('-', '_')
			extraArgsKeys.append(keyStr)

		extraArgsValues = []
		for index in range(1, len(extraArgs), 2):
			extraArgsValues.append(extraArgs[index])

		this.extraArgs = dict(zip(extraArgsKeys, extraArgsValues))

	# Functor method.
	# We have to ParseArgs() here in order for other Executors to use ____KWArgs...
	def ParseInitialArgs(this):
		this.ParseArgs() # first, to enable debug and other such settings.
		this.PopulateConfig()
		this.SetVerbosity()
		this.SetLogFile()
		logging.debug(f"<---- {this.name} (log level: {logging.getLogger().level}) ---->")
		logging.debug(f"Got extra arguments: {this.extraArgs}") # has to be after verbosity setting
		logging.debug(f"Got config contents: {this.config}")
		this.PopulateRepoDetails()


	# Functor required method
	# Override this with your own workflow.
	def Function(this):
		this.RegisterAllClasses()
		this.InitData()


	# By default, Executors do not act on this.next; instead, they make it available to all Executed Functors.
	def CallNext(this):
		pass


	# Close out anything we left open.
	def AfterFunction(this):
		this.TeardownLogging()


	# Execute a Functor based on name alone (not object).
	# If the given Functor has been Executed before, the cached Functor will be called again. Otherwise, a new Functor will be constructed.
	@recoverable
	def Execute(this, functorName, *args, **kwargs):
		packageType = this.defaultPackageType
		if ('packageType' in kwargs):
			packageType = kwargs.pop('packageType')

		logging.debug(f"Executing {functorName}({', '.join([str(a) for a in args] + [k+'='+str(v) for k,v in kwargs.items()])})")

		if (functorName in this.cachedFunctors):
			return this.cachedFunctors[functorName](*args, **kwargs, executor=this)

		functor = this.GetRegistered(functorName, packageType)
		this.cachedFunctors.update({functorName: functor})

		return functor(*args, **kwargs, executor=this)


	# Attempts to download the given package from the repo url specified in calling args.
	# Will refresh registered classes upon success
	# RETURNS whether or not the package was downloaded. Will raise Exceptions on errors.
	# Does not guarantee new classes are made available; errors need to be handled by the caller.
	@recoverable
	def DownloadPackage(this,
		packageName,
		registerClasses=True,
		createSubDirectory=False):

		if (not this.repo.online):
			logging.debug(f"Refusing to download {packageName}; we were told not to use a repository.")
			return False

		logging.debug(f"Trying to download {packageName} from repository ({this.repo.url})")

		if (not os.path.exists(this.repo.store)):
			logging.debug(f"Creating directory {this.repo.store}")
			mkpath(this.repo.store)

		packageZipPath = os.path.join(this.repo.store, f"{packageName}.zip")

		url = f"{this.repo.url}/download?package_name={packageName}"

		auth = None
		if this.repo.username and this.repo.password:
			auth = requests.auth.HTTPBasicAuth(this.repo.username, this.repo.password)

		headers = {
			"Connection": "keep-alive",
		}

		packageQuery = requests.get(url, auth=auth, headers=headers, stream=True)

		if (packageQuery.status_code != 200):
			raise PackageError(f"Unable to download {packageName}")
		# let caller decide what to do next.

		packageSize = int(packageQuery.headers.get('content-length', 0))
		chunkSize = 1024 # 1 Kibibyte

		logging.debug(f"Writing {packageZipPath} ({packageSize} bytes)")
		packageZipContents = open(packageZipPath, 'wb+')

		progressBar = None
		if (this.verbosity >= 2):
			progressBar = tqdm(total=packageSize, unit='iB', unit_scale=True)

		for chunk in packageQuery.iter_content(chunkSize):
			packageZipContents.write(chunk)
			if (this.verbosity >= 2):
				progressBar.update(len(chunk))

		if (this.verbosity >= 2):
			progressBar.close()

		if (packageSize and this.verbosity >= 2 and progressBar.n != packageSize):
			raise PackageError(f"Package wrote {progressBar.n} / {packageSize} bytes")

		packageZipContents.close()

		if (not os.path.exists(packageZipPath)):
			raise PackageError(f"Failed to create {packageZipPath}")

		logging.debug(f"Extracting {packageZipPath}")
		openArchive = ZipFile(packageZipPath, 'r')
		extractLoc = this.repo.store
		if (createSubDirectory):
			extractLoc = os.path.join(extractLoc, packageName)
		openArchive.extractall(f"{extractLoc}")
		openArchive.close()
		os.remove(packageZipPath)

		if (registerClasses):
			this.RegisterAllClassesInDirectory(this.repo.store)

		return True

	# RETURNS and instance of a Datum, Functor, etc. (aka modules) which has been discovered by a prior call of RegisterAllClassesInDirectory()
	# Will attempt to register existing modules if one of the given name is not found. Failing that, the given package will be downloaded if it can be found online.
	# Both python modules and other eons modules of the same packageType will be installed automatically in order to meet all required dependencies of the given module.
	@recoverable
	def GetRegistered(this,
		registeredName,
		packageType=""):

		try:
			registered = SelfRegistering(registeredName)
		except Exception as e:
			# We couldn't get what was asked for. Let's try asking for help from the error resolution machinery.
			packageName = registeredName
			if (packageType):
				packageName = f"{registeredName}.{packageType}"
			logging.error(f"While trying to instantiate {packageName}, got: {e}")
			raise HelpWantedWithRegistering(f"Trying to get SelfRegistering {packageName}")

		# NOTE: Functors are Data, so they have an IsValid() method
		if (not registered or not registered.IsValid()):
			logging.error(f"No valid object: {registeredName}")
			raise FatalCannotExecute(f"No valid object: {registeredName}")

		return registered


	# Non-static override of the SelfRegistering method.
	# Needed for errorObject resolution.
	@recoverable
	def RegisterAllClassesInDirectory(this, directory):
		path = Path(directory)
		if (not path.exists()):
			logging.debug(f"Making path for SelfRegitering classes: {str(path)}")
			path.mkdir(parents=True, exist_ok=True)

		if (directory not in this.syspath):
			this.syspath.append(directory)

		SelfRegistering.RegisterAllClassesInDirectory(directory)


	# Utility method. may not be useful.
	@staticmethod
	def SplitNameOnpackageType(name):
		splitName = name.split('_')
		if (len(splitName)>1):
			return splitName[0], splitName[1]
		return "", name


	# Uses the ResolveError Functors to process any errors.
	@recoverable
	def ResolveError(this, error, attemptResolution, obj, function):
		if (attemptResolution >= len(this.resolveErrorsWith)):
			raise FailedErrorResolution(f"{this.name} does not have {attemptResolution} resolutions to fix this error: {error} (it has {len(this.resolveErrorsWith)})")

		resolution = this.GetRegistered(this.resolveErrorsWith[attemptResolution], "resolve") # Okay to ResolveErrors for ErrorResolutions.
		this.errorResolutionStack, errorMightBeResolved = resolution(executor=this, error=error, obj=obj, function=function)
		if (errorMightBeResolved):
			logging.debug(f"Error might have been resolved by {resolution.name}.")
		return errorMightBeResolved


	######## START: Fetch Locations ########

	def fetch_location_args(this, varName, default, fetchFrom, attempted):
		for key, val in this.extraArgs.items():
			if (key == varName):
				return val, True
		return default, False

	######## END: Fetch Locations ########

