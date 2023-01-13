# 2023.1.6
import json,os,pymysql,platform

myhost	= os.getenv("myhost", "files.jukuu.com" if not "Windows" in platform.system() else "files.jukuu.com")
myport  = int(os.getenv("myport", 3309))
mydb	= os.getenv("mydb", "nac")
conn	= pymysql.connect(host=myhost,port=myport,user='root',password='cikuutest!',db=mydb)

def get_cursor(ssdict:bool=False):
	try:
		conn.ping()
	except:
		conn = pymysql.connect(host=myhost,port=myport,user='root',password='cikuutest!',db=mydb)
	return conn.cursor(pymysql.cursors.SSDictCursor) if ssdict else conn.cursor()

def fetchall(sql:str="select attr, count from dic where name = 'open:VERB:dobj:NOUN' order by count desc limit 10", ssdict:bool=False, columns:str=None): # asdic:bool=False,
	''' ssdict: True to return [{k:v}] else [row], columns=name,value '''
	cursor = get_cursor(ssdict)
	cursor.execute(sql)
	rows =  [row for row in cursor.fetchall() ] 
	if columns: 
		columns = [s.strip() for s in columns.strip().split(',')]
		return [dict(zip(columns, row)) for row in rows]
	return rows

def fetchone(sql:str="select count(*) from corpuslist", ssdict:bool=False):
	cursor = get_cursor(ssdict)
	cursor.execute(sql)
	return cursor.fetchone() 

def geti(sql): return (row := fetchone(sql), int(row[0]) if row else 0)[-1]

def my_query(sql:str="select attr, count from dic where name = 'open:VERB:dobj:NOUN' order by count desc limit 10"): 
	return fetchall(sql,True)

if __name__ == "__main__":  
	pass