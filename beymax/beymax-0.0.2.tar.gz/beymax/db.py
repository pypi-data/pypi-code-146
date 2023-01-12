import sqlalchemy as alch
import sqlalchemy.ext.asyncio as alchasync
from sqlalchemy import orm
import asyncio
from contextlib import asynccontextmanager, contextmanager

class DBConnection(object):
	"""
	Represents an ongoing connection to the database backend.
	Instantiates individual sessions
	"""

	def __init__(self, database_string):
		self.database_string = database_string
		self.engine = None
		self.connection = None
		self.sessionmaker = None
		self._orm_base = orm.declarative_base()

	@property
	def base(self):
		return self._orm_base
	
	async def __aenter__(self):
		self.engine = alchasync.create_async_engine(self.database_string, echo=False)
		self.connection = await self.engine.begin().__aenter__()
		self.sessionmaker = orm.sessionmaker(self.engine, expire_on_commit=False, class_=alchasync.AsyncSession)
		return self
	
	async def __aexit__(self, *args):
		await self.connection.__aexit__(*args)
		self.sessionmaker = None
		self.connection = None
		self.engine = None
	
	@asynccontextmanager
	async def session(self):
		async with self.sessionmaker() as session:
			async with session.begin():
				yield session

class SyncDBConnection(object):
	"""
	Represents an ongoing connection to the database backend.
	Instantiates individual sessions
	This class is entirely synchronous, best used for debug
	"""

	def __init__(self, database_string):
		self.database_string = database_string
		self.engine = None
		self.connection = None
		self.sessionmaker = None
		self._orm_base = orm.declarative_base()

	@property
	def base(self):
		return self._orm_base
	
	def __enter__(self):
		self.engine = alch.create_engine(self.database_string, echo=True)
		self.connection = self.engine.begin().__enter__()
		self.sessionmaker = orm.sessionmaker(self.engine, expire_on_commit=False)
		return self
	
	def __exit__(self, *args):
		self.connection.__exit__(*args)
		self.sessionmaker = None
		self.connection = None
		self.engine = None
	
	@contextmanager
	def session(self):
		with self.sessionmaker() as session:
			with session.begin():
				yield session