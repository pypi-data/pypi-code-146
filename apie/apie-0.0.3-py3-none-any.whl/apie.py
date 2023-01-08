import os
import logging
import shutil
import jsonpickle
from pathlib import Path
import eons
from flask import request
from flask import Response
import traceback
from flask import Flask
from waitress import serve

######## START CONTENT ########
# All APIer errors
class APIError(Exception): pass


# Exception used for miscellaneous API errors.
class OtherAPIError(APIError): pass

# APIE Functors extend Eons Functors in order to:
# 1. Improve Fetch() behavior when cascading multiple Functor executions.
# 2. Allow Fetching from a http request.
class Functor(eons.Functor):
	def __init__(this, name=eons.INVALID_NAME()):
		super().__init__(name)

		this.enableRollback = False

		# Default places to Fetch from.
		# Add to this list when extending Fetch().
		# Remove from this list to restrict Fetching behavior.
		# Reorder this list to make Fetch more efficient for your use case.
		# Also see FetchWith and FetchWithout for ease-of-use methods.
		this.fetchFrom = [
			'this',
			'args',
			'precursor',
			'request_args',
			'request_form',
			'request_json',
			'request_files',
			'executor',
			'environment',
		]

		# The request object to process
		this.request = None


	# Grab any known and necessary args from this.kwargs before any Fetch calls are made.
	# There should always be a request.
	def ParseInitialArgs(this):
		super().ParseInitialArgs()
		if (this.precursor):
			this.request = this.precursor.request
		else:
			this.request = this.kwargs.pop('request')


	def FetchFromRequest(this, field, varName, default):
		val = getattr(this.request, field).get(varName)
		if (val is not None):
			return val, True
		return default, False


	def fetch_location_request_args(this, varName, default, fetchFrom, attempted):
		return this.FetchFromRequest('args', varName, default)


	def fetch_location_request_form(this, varName, default, fetchFrom, attempted):
		if (not this.request.data):
			return default, False
		return this.FetchFromRequest('form', varName, default)


	def fetch_location_request_json(this, varName, default, fetchFrom, attempted):
		if (this.request.content_type != "application/json"):
			return default, False
		return this.FetchFromRequest('json', varName, default)


	def fetch_location_request_files(this, varName, default, fetchFrom, attempted):
		if (not this.request.files):
			return  default, False
		return this.FetchFromRequest('files', varName, default)


# Authenticator is a Functor which validates whether or not a request is valid.
# The inputs will be the path of the request and the request itself.
# If you need to check whether the request parameters, data, files, etc. are valid, please do so in your Endpoint.
# Because this class will be invoked often, we have made some performant modifications to the default Functor methods.
# Authenticators may be called sequentially but in such a case, only the last Authenticator will Authenticate(), all precursors are skipped over.
# NOTE: All logic for *this should be in Authenticate. There are no extra functions called (e.g. PreCall, PostCall, etc.)
# Authenticate should either return False or raise an exception if the provided request is invalid and should return True if it is.
class Authenticator(Functor):
	def __init__(this, name="Authenticator"):
		super().__init__(name)

	# Override of eons.Functor method. See that class for details
	# NOTE: All logic for *this should be in Authenticate. There are no extra functions called (e.g. PreCall, PostCall, etc.)
	# Authenticate should either return False or raise an exception if the provided request is invalid and should return True if it is.
	def Authenticate(this):
		return True

	# This will be called whenever an unauthorized request is made.
	def Unauthorized(this, path):
		logging.debug(f"Unauthorized: {this.name} on {path}")
		return "Unauthorized", 401

	# Override of eons.Functor method. See that class for details
	def ParseInitialArgs(this):
		super().ParseInitialArgs()

		this.path = this.kwargs.pop('path')

	# Override of eons.Functor method. See that class for details
	# Slimmed down for performance
	def __call__(this, *args, **kwargs):
		this.args = args
		this.kwargs = kwargs
		
		this.PopulatePrecursor()
		this.Initialize() # nop on call 2+
		this.PopulateMethods() # Doesn't require Fetch; depends on precursor
		this.ParseInitialArgs() # Usually where config is read in.
		this.ValidateStaticArgs() # nop on call 2+
		this.ValidateArgs()
		this.PopulateNext()
		this.ValidateMethods()

		if (this.next):
			return this.CallNext()
		return this.Authenticate()


# Endpoints are what is run when a given request is successfully authenticated.
# Put all your actual API logic in these!
# Keep in mind that Endpoints will be made available in a just-in-time, as-needed basis. There is no need to preload logic, etc.
# That also means that each Endpoint should operate in isolation and not require any other Endpoint to function.
# The exception to this isolation is when Endpoints are intended to be called in sequence.
# Any number of Endpoints can be chained together in any order. The behavior of the first affects the behavior of the last.
# This allows you to create generic "upload" Endpoints, where what is uploaded is determined by the preceding Endpoint.
# For example, you might have 3 Endpoints: "package", "photo", and "upload"; both package and photo set a member called "file_data"; upload Fetches "file_data" and puts it somewhere; you can thus use upload with either precursor (e.g. .../package/upload and .../photo/upload).
# What is returned by an Endpoint is the very last Endpoint's return value. All intermediate values are skipped (so you can throw errors if calling things like .../package without a further action).
# NOTE: Endpoints should be published as api_s (i.e. projectType="api")
class Endpoint(Functor):
	def __init__(this, name=eons.INVALID_NAME()):
		super().__init__(name)

		this.enableRollback = False

		# Internal logic; used when calling 'help', etc.
		this.bypassCall = False

		# What methods can be used with this Endpoint?
		this.supportedMethods = [
			'POST',
			'GET',
			'PUT',
			'DELETE',
			'PATCH'
		]

		# Only the items listed here will be allowed as next Endpoints.
		# If this list is empty, all endpoints are allowed.
		# When creating your endpoints, make sure to adjust this!
		# Also, please keep 'help'. It helps.
		#
		# To allow all Endpoints, set this to [].
		this.allowedNext = ['help']

		this.next = []

		# Hop-by-hop headers are forbidden by WSGI.
		this.forbidden_headers = [
			'Keep-Alive',
			'Transfer-Encoding',
			'TE',
			'Connection',
			'Trailer',
			'Upgrade',
			'Proxy-Authorization',
			'Proxy-Authenticate',
		]

		# What should the return type of *this be?
		this.mime = 'application/json'

		# If the client can store the result of *this locally, let them know.
		# When querying this, it is best to use the IsCachable() method.
		this.cacheable = False

		# If compiling data, from this.response.content.data for example, the response.content.string of *this will be overwritten.
		# You can override this behavior and force the compiled data to be lost by setting clobberContent to False.
		# This is useful if you are forwarding json requests and don't want to parse then recompile the content.
		this.clobberContent = True

		# What is returned after Call()
		this.response = eons.util.DotDict()
		this.response.content = eons.util.DotDict()
		this.ResetResponse()

# Please override this for each of your Endpoints.
	# RETURN a string that tells the user how to call *this.
	# It is recommended to return a static string, without Fetching anything.
	#
	# The 'help' Endpoint will print this text.
	# Setting this will inform users on how to use your Endpoint.
	# Help will automatically print the name of *this for you, along with optional and required args, supported methods, and allowed next
	def GetHelpText(this):
		return '''\
LOL! Look at you: needing help. Pathetic.
'''

	# Call things!
	# Override this or die.
	def Call(this):
		pass


	# Override this to perform whatever success checks are necessary.
	# Override of eons.Functor method. See that class for details
	def DidCallSucceed(this):
		return True


	# If an error is thrown while Call()ing *this, APIE will attempt to return this method.
	def HandleBadRequest(this, request, error):
		message = f"Bad request for {this.name}: {str(error)}. "
		if ('help' in this.allowedNext):
			message += "Try appending /help."
		return message, 400


	# Hook for any pre-call configuration
	# Override of eons.Functor method. See that class for details
	def PreCall(this):
		pass


	# Hook for any post-call configuration
	# Override of eons.Functor method. See that class for details
	def PostCall(this):
		pass


	# Because APIE caches endpoints, the last response given will be stored in *this.
	# Call this method to clear the stale data.
	def ResetResponse(this):
		this.response.code = 200
		this.response.headers = {}
		this.response.content.data = {}
		this.response.content.string = ""


	# Called right before *this returns.
	# Handles json pickling, etc.
	def ProcessResponse(this):
		if (this.clobberContent):
			if(this.mime == 'application/json'):
				if (len(this.response.content.string)):
					logging.info(f"Clobbering content.string ({this.response.content.string})")

				this.response.content.data.update({'cacheable': this.cacheable})
				this.response.content.string = jsonpickle.encode(dict(this.response.content.data))

		if ('Content-Type' not in this.response.headers):
			this.response.headers.update({'Content-Type': this.mime})

		for header in this.forbidden_headers:
			try:
				this.response.headers.pop(header)
			except KeyError:
				pass

		return Response(
			response = this.response.content.string,
			status = this.response.code,
			headers = this.response.headers.items(),
			mimetype = this.mime, #This one is okay, I guess???
			content_type = None, #why is this here, we set it in the header. This is a problem in Flask.
			direct_passthrough = True # For speed??
		)


	# Override of eons.Functor method. See that class for details
	def Function(this):
		this.bypassCall = False
		if (this.next and this.next[-1] == 'help'):
			this.bypassCall = True
			return None

		this.ResetResponse()
		this.PreCall()
		this.Call()
		this.PostCall()
		return this.ProcessResponse()


	#### SPECIALIZED OVERRIDES. IGNORE THESE ####

	# API compatibility shim
	def DidFunctionSucceed(this):
		if (this.bypassCall):
			return True
		return this.DidCallSucceed()

	def PopulatePrecursor(this):
		super().PopulatePrecursor()

		# We want to let the executor know who we are as soon as possible, in case any errors come up in validation.
		this.executor.lastEndpoint = this

	#Grab any known and necessary args from this.kwargs before any Fetch calls are made.
	# This is executed first when calling *this.
	def ParseInitialArgs(this):
		super().ParseInitialArgs()


	def ValidateMethod(this):
		if (this.request.method not in this.supportedMethods):
			raise OtherAPIError(f"Method not supported: {this.request.method}")

	def ValidateNext(this, next):
		if (next and this.allowedNext and next not in this.allowedNext):
			logging.error(f"{next} is not allowed after {this.name}; only {this.allowedNext}")
			if (next in ['hack'] and not this.executor.dev):
				raise OtherAPIError(f"Hacking is forbidden on production servers.")
			else:
				raise OtherAPIError(f"Next Endpoint not allowed: {next}")
		return True

	def ValidateArgs(this):
		try:
			super().ValidateArgs()
		except eons.MissingArgumentError as e:
			logging.recovery(f"Error is irrelevant; user is seeking help ({str(e)})")
			# It doesn't matter if *this isn't valid if the user is asking for help.
			if (this.next and this.next[-1] == 'help'):
				return
			raise e
		




class APIE(eons.Executor):

	def __init__(this):
		super().__init__(name="Application Program Interface with Eons", descriptionStr="A readily extensible take on APIs.")

		# this.RegisterDirectory("ebbs")

		this.optionalKWArgs['host'] = "0.0.0.0"
		this.optionalKWArgs['port'] = 80
		this.optionalKWArgs['dev'] = False
		this.optionalKWArgs['clean_start'] = True
		this.optionalKWArgs['authenticator'] = "noauth"
		this.optionalKWArgs['preprocessor'] = ""

		this.supportedMethods = [
			'POST',
			'GET',
			'PUT',
			'DELETE',
			'PATCH'
		]

		# Used in Function()
		this.auth = None
		this.flask = None

		# *this is single-threaded. If we want parallel processing, we can create replicas.
		this.lastEndpoint = None

		this.defaultConfigFile = "apie.json"

	# Override of eons.Executor method. See that class for details
	def RegisterIncludedClasses(this):
		super().RegisterIncludedClasses()
		this.RegisterAllClassesInDirectory(str(Path(__file__).resolve().parent.joinpath("api")))
		this.RegisterAllClassesInDirectory(str(Path(__file__).resolve().parent.joinpath("auth")))
		

	# Override of eons.Executor method. See that class for details
	def RegisterAllClasses(this):
		super().RegisterAllClasses()


	# Acquire and run the given endpoint with the given request.
	def ProcessEndpoint(this, endpointName, request, **kwargs):

		# Parse Endpoint syntax.
		# "[..., ...]something" => multi(domain=[..., ...], next="something")
		if (endpointName.startswith('[')):
			if ('domain' in kwargs):
				raise APIError(f"Domain already exists in multicall; domain={kwargs['domain']}; multicall={endpointName}")

			domainStrEndPos = endpointName.find(']')+1
			domainStr = endpointName[:domainStrEndPos]
			if ('next' in kwargs):
				kwargs['next'] = [endpointName[domainStrEndPos:]].extend(kwargs['next'])
			else:
				kwargs['next'] = endpointName[domainStrEndPos:]

			# Trim '(' and ')', then make list.
			kwargs['domain'] = domainStr[1:-1].split(',')

			endpointName = "multi"

		if (endpointName in this.cachedFunctors):
			return this.cachedFunctors[endpointName](executor=this, request=request, **kwargs)

		endpoint = this.GetRegistered(endpointName, "api")
		this.cachedFunctors.update({endpointName: endpoint})
		return endpoint(executor=this, request=request, **kwargs)


	# What to do when a request causes an exception to be thrown.
	def HandleBadRequest(this, request, error):
		message = f"Bad request: {str(error)}"
		return message, 400


	# Override of eons.Executor method. See that class for details
	def Function(this):
		super().Function()

		if (this.clean_start):
			this.Clean()

		this.auth = this.GetRegistered(this.authenticator, "auth")

		this.flask = Flask(this.name)

		@this.flask.route("/", defaults={"path": ""}, methods = this.supportedMethods)
		def root(path):
			return "It works!", 200

		@this.flask.route("/<string:path>", methods = this.supportedMethods)
		@this.flask.route("/<path:path>", methods = this.supportedMethods)
		def handler(path):
			try:
				if (this.auth(executor=this, path=path, request=request)):
					endpoints = []
					if (this.preprocessor):
						endpoints.append(this.preprocessor)
					if (path.endswith('/')):
						path = path[:-1]
					endpoints.extend(path.split('/'))
					this.lastEndpoint = None
					logging.debug(f"Responding to request for {path}; request: {request}")
					response = this.ProcessEndpoint(endpoints.pop(0), request, next=endpoints)
					logging.debug(f"Got headers: {response.headers}")
					logging.debug(f"Got response: {response}")
					return response
				else:
					return this.auth.Unauthorized(path)
			except Exception as error:
				traceback.print_exc()
				logging.error(str(error))
				if (this.lastEndpoint):
					try:
						return this.lastEndpoint.HandleBadRequest(request, error)
					except Exception:
						pass
				return this.HandleBadRequest(request, error) #fine. We'll do it ourselves.

		options = {}
		options['app'] = this.flask
		options['host'] = this.host
		options['port'] = this.port

		# Only applicable if using this.flask.run(**options)
		# if (this.args.verbose > 0):
		#	 options['debug'] = True
		#	 options['use_reloader'] = False

		serve(**options)


	# Remove possibly stale modules.
	def Clean(this):
		repoPath = Path(this.repo['store'])
		if (repoPath.exists()):
			shutil.rmtree(this.repo['store'])
		repoPath.mkdir(parents=True, exist_ok=True)

