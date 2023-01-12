import os
import logging
import shutil
from pathlib import Path
import eons
import platform
import jsonpickle
import sqlalchemy as sql
import sqlalchemy.orm as orm
from eot import EOT

######## START CONTENT ########

# All Merx errors
class MerxError(Exception, metaclass=eons.ActualType): pass

# Exception used for miscellaneous Merx errors.
class OtherMerxError(MerxError, metaclass=eons.ActualType): pass


# CatalogCards are classes which will be stored in the catalog.db
SQLBase = orm.declarative_base()

# The Epitome class is an object used for tracking the location, status, and other metadata of a Tome package.
# epi = above, so metadata of a tome would be above a tome, would be epitome. Note that the "tome" portion of epitome actually derives from the word for "to cut". Epitome roughly means an abridgement or surface incision. Abridgement is appropriate here.
# Epitomes should not be extended when creating packages. They are only to be used by Merx for tracking existing packages.
class Epitome(SQLBase):
	__tablename__ = 'tomes'
	id = sql.Column(sql.Integer, primary_key=True)
	name = sql.Column(sql.String)
	version = sql.Column(sql.String) # not all versions follow Semantic Versioning.
	installed_at = sql.Column(sql.String) # semicolon-separated list of file paths.
	retrieved_from = sql.Column(sql.String) # repo url
	first_retrieved_on = sql.Column(sql.Float) # startdate (per eot).
	last_retrieved_on = sql.Column(sql.Float) # startdate (per eot).
	additional_notes = sql.Column(sql.String) # TODO: Let's convert this to PickleType and store any user-defined values.

	path = None

	def __repr__(this):
		return f"<Epitome(id={this.id}, name={this.name}, version={this.version}, installed_at={this.installed_at}, retrieved_from={this.retrieved_from}, retrieved_on={this.retrieved_on}, additional_notes={this.additional_notes})>"

	def __init__(this, name=None):
		this.name = name


# Transaction logs are recorded whether or not the associated Merx.Transaction() completed.
class TransactionLog(SQLBase):
	__tablename__ = 'transactions'
	id = sql.Column(sql.Integer, primary_key=True)
	when = sql.Column(sql.Float)  # startdate (per eot).
	merx = sql.Column(sql.String) # name of merx
	tomes = sql.Column(sql.String) # semicolon-separated list of tome arguments
	result = sql.Column(sql.Integer) # return value of Merx.DidTransactionSucceed()

	def __init__(this, merx, tomes):
		this.when = EOT.GetStardate()
		this.merx = merx
		this.tomes = tomes

# This is here just to ensure all SQLBase children are created before *this is called.
# TODO: Can we move this into EMI?
def ConstructCatalog(engine):
	SQLBase.metadata.create_all(engine)


# Merx are actions: things like "install", "update", "remove", etc.
# These should be stored on the online repo as merx_{merx.name}, e.g. merx_install, etc.
class Merx(eons.Functor):
	def __init__(this, name=eons.INVALID_NAME()):
		super().__init__(name)

		this.requiredKWArgs = [
			"tomes", # emi cli arguments 2 and beyond
			"paths", # where to put things, as determined by EMI
		]
		# executor and catalog are treated specially; see ValidateArgs(), below, for details.

		# For optional args, supply the arg name as well as a default value.
		this.optionalKWArgs = {}

		this.transactionSucceeded = False


	# Do stuff!
	# Override this or die.
	def Transaction(this):
		pass


	# Undo any changes made by Transaction.
	# Please override this too!
	def Rollback(this):
		this.catalog.rollback() # removes all records created by *this (see: https://docs.sqlalchemy.org/en/14/orm/tutorial.html# rolling-back).


	# RETURN whether or not the Transaction was successful.
	# While you can override this, it is preferred that you simply set this.transactionSucceeded throughout Transaction().
	def DidTransactionSucceed(this):
		return this.transactionSucceeded


	# API compatibility shim with eons.Functor method.
	def DidFunctionSucceed(this):
		this.functionSucceeded = this.transactionSucceeded
		return this.DidTransactionSucceed()


	# RETURN whether or not the Rollback was successful.
	# While you can override this, it is preferred that you simply set this.rollbackSucceeded
	# Override of eons.Functor method.
	def DidRollbackSucceed(this):
		 return this.rollbackSucceeded


	# Hook for any pre-transaction configuration
	def PreTransaction(this):
		pass


	# Hook for any post-transaction configuration
	def PostTransaction(this):
		pass


	# Grab any known and necessary args from kwargs before any Fetch calls are made.
	# Override of eons.Functor method.
	def ParseInitialArgs(this):
		super().ParseInitialArgs()
		setattr(this, 'catalog', this.kwargs['catalog'])


	# Override of eons.Functor method. See that class for details
	def Function(this):
		logging.info(f"Initiating Transaction {this.name} for {this.tomes}")

		this.PreTransaction()
		this.Transaction()
		this.PostTransaction()


	# Open or download a Tome.
	# tomeName should be given without the "tome_" prefix
	# RETURNS an Epitome containing the given Tome's Path and details or None.
	def GetTome(this, tomeName):
		return this.executor.GetTome(tomeName)


class PathSelector:
	def __init__(this, name, systemPath):
		this.name = name
		this.systemPath = systemPath
		this.selectedPath = None

class EMI(eons.Executor):

	def __init__(this):

		# The library is where all Tomes are initially distributed from (i.e. the repo_store)
		#   and where records for all Tome locations and Merx Transactions are kept.
		# We need to create these files for there to be a valid config.json to read from. Otherwise, eons.Executor crashes.
		this.library = Path.home().joinpath(".eons")
		this.sqlEngine = sql.create_engine(f"sqlite:///{str(this.library.joinpath('catalog.db'))}")
		this.catalog = orm.sessionmaker(bind=this.sqlEngine)() # sqlalchemy: sessionmaker()->Session()->session.
		this.SetupHome()

		super().__init__(name="Eons Modular Interface", descriptionStr="A universal state manager.")

		# Windows paths must be set in the config.json.
		this.paths = [
			PathSelector("exe", "/usr/local/bin/"),
			PathSelector("inc", "/usr/local/include/"),
			PathSelector("lib", "/usr/local/lib/")
		]
		
		# Ease of use method for processed paths.
		this.selectedPaths = {}

	# Create initial resources if they don't already exist.
	def SetupHome(this):
		if (not this.library.exists()):
			logging.info(f"Creating home folder: {str(this.library)}")
			this.library.mkdir()
			this.library.joinpath("tmp").mkdir()

		catalogFile = this.library.joinpath("catalog.db")
		if (not catalogFile.exists()):
			logging.info(f"Creating catalog: {str(catalogFile)}")
			catalogFile.touch()
		if (not catalogFile.stat().st_size):
			logging.info("Constructing catalog scheme")
			ConstructCatalog(this.sqlEngine)

		configFile = this.library.joinpath("config.json")
		if (not configFile.exists() or not configFile.stat().st_size):
			logging.info(f"Initializing config file: {str(configFile)}")
			config = open(configFile, "w+")
			config.write("{\n}")


	# Override of eons.Executor method. See that class for details
	def Configure(this):
		super().Configure()
		this.tomeDirectory = this.library.joinpath("tmp")
		this.defaultRepoDirectory = str(this.library.joinpath("merx"))
		this.defaultConfigFile = str(this.library.joinpath("config.json"))
		this.defaultPackageType = "merx"

	# Override of eons.Executor method. See that class for details
	def RegisterAllClasses(this):
		super().RegisterAllClasses()

	# Override of eons.Executor method. See that class for details
	def AddArgs(this):
		super().AddArgs()
		this.argparser.add_argument('merx', type=str, metavar='merx', help='what to do (e.g. \'install\' or \'remove\')')
		this.argparser.add_argument('tomes', type=str, nargs='*', metavar='tome', help='how to do it (e.g. \'my_package\')')

	# Override of eons.Executor method. See that class for details
	def ParseArgs(this):
		super().ParseArgs()
		# NOTE: THERE SHOULD BE NO this.extraArgs

	# Override of eons.Executor method. See that class for details
	def Function(this):

		super().Function()
		
		# paths will be provided to each Merx as a dictionary.
		this.SelectPaths()
		merxList = this.parsedArgs.merx.split('/')
		
		this.Execute(merxList.pop(0), next=merxList)

	def SelectPaths(this):
		for path in this.paths:
			preferredPath = Path(this.Fetch(f"{path.name}_path", default=path.systemPath))
			if (preferredPath.exists() and os.access(str(preferredPath), os.W_OK | os.X_OK)):
				path.selectedPath = preferredPath
			else:
				path.selectedPath = this.library.joinpath(path.name)
				logging.debug(f"The preferred path for {path.name} ({str(preferredPath)}) was unusable.")
				path.selectedPath.mkdir(exist_ok=True)
			this.selectedPaths[path.name] = path.selectedPath
			logging.debug(f"Path for {path.name} set to {str(path.selectedPath)}.")
			
	def Execute(this, merx, *args, **kwargs):
		transaction = TransactionLog(merx, '; '.join(this.parsedArgs.tomes))
		transaction.result = super().Execute(merx, *args, tomes=this.parsedArgs.tomes, paths=this.selectedPaths, catalog=this.catalog, **kwargs)
		this.catalog.add(transaction)
		
		# make sure the transaction log gets committed.
		# TODO: develop TransactionLog retention policy (i.e. trim records after 1 year, 1 day, or don't record at all).
		this.catalog.commit()

	# GetRegistered modified for use with Tomes.
	# tomeName should be given without the ".tome" suffix
	# RETURNS an Epitome containing the given Tome's Path and details or None.
	def GetTome(this, tomeName, download=True):
		logging.debug(f"Fetching {tomeName}.tome.")

		tomePath = this.tomeDirectory.joinpath(f"{tomeName}.tome")
		logging.debug(f"Will place {tomeName} in {tomePath}.")

		epitome = this.catalog.query(Epitome).filter(Epitome.name==tomeName).first()
		if (epitome is None):
			epitome = Epitome(tomeName)
			if (not download):
				logging.warning(f"Epitome for {tomeName} did not exist and will not be downloaded.")
		else:
			logging.debug(f"Got exiting Epitome for {tomeName}.")

		if (tomePath.exists()):
			logging.debug(f"Found {tomeName} on the local filesystem.")
			epitome.path = tomePath
		elif (download):
			preservedRepo = this.repo['store']
			preservedUrl = this.repo['url']
			if (epitome.retrieved_from is not None and len(epitome.retrieved_from)):
				this.repo['url'] = epitome.retrieved_from
			this.repo['store'] = str(this.tomeDirectory)
			logging.debug(f"Attempting to download {tomeName} from {this.repo['url']}")
			this.DownloadPackage(packageName=f"{tomeName}.tome", registerClasses=False, createSubDirectory=True)
			if (tomePath.exists()):
				epitome.path = tomePath
				epitome.retrieved_from = this.repo['url']
				if (epitome.first_retrieved_on is None or epitome.first_retrieved_on == 0):
					epitome.first_retrieved_on = EOT.GetStardate()
				epitome.last_retrieved_on = EOT.GetStardate()
				if (epitome.version is None):
					epitome.version = ""
					# TODO: populate epitome.version. Blocked by https://github.com/infrastructure-tech/srv_infrastructure/issues/2
			else:
				logging.error(f"Failed to download {tomeName}.tome")

			this.repo['url'] = preservedUrl
			this.repo['store'] = preservedRepo
		else:
			logging.warning(f"Could not find {tomeName}; only basic info will be available.")

		return epitome

