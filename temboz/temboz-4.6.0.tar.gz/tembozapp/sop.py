import sqlite3, sys

class Cursor:
  def __init__(self, c):
    self.c = c
  def execute(self, *args, **kwargs):
    print('EXECUTE', args, kwargs, file=param.log)
    return self.c.execute(*args, **kwargs)
  def __getattr__(self, *args, **kwargs):
    return getattr(self.c, *args, **kwargs)
  def __setattr__(self, *args, **kwargs):
    if args[0] != 'c':
      return object.__setattr__(self.c, *args, **kwargs)
    else:
      object.__setattr__(self, 'c', args[1])
    
class DB(object):
  def __init__(self, db):
    object.__init__(self)
    self.db = db
  def cursor(self):
    return Cursor(self.db.cursor())
  def __enter__(self):
    return self
  def __exit__(self, *args, **kwargs):
    self.db.__exit__(*args, **kwargs)
  def __getattr__(self, *args, **kwargs):
    return getattr(self.db, *args, **kwargs)
  def __setattr__(self, *args, **kwargs):
    if args[0] != 'db':
      return object.__setattr__(self.db, *args, **kwargs)
    else:
      object.__setattr__(self, 'db', args[1])
  

d = sqlite3.connect('dbname=rss.db')
db = DB(d)

print(db.__enter__)

with db as foo:
  pass
