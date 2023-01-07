# 2023.1.4 
import json,os,sqlite3

def db(name:str='c4vend-nac', folder:str="/usr/local/lib/python3.8/site-packages/api/db", suffix:str='sqlite'):
	''' '''
	if not hasattr(db, name): setattr(db, name, sqlite3.connect(f"{folder}/{name}.{suffix}", check_same_thread=False) ) 
	return getattr(db, name) 

query = lambda sql="select * from nac limit 2", name="c4vend-nac" :  db(name).execute(sql).fetchall()

if __name__ == "__main__":  
	pass