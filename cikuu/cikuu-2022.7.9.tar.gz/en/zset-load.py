# 2022.10.25  zset-like:  (key, name, value) 
import json, traceback,sys, time,  fileinput, os, pymysql,fire
def run(infile, host='127.0.0.1', port=3307):
	''' saveto: mysql/file '''
	name = infile.split('.')[0] 
	print ("started:", infile , flush=True)
	my_conn = pymysql.connect(host=host,port=port,user='root',password='cikuutest!',db='zset')
	with my_conn.cursor() as cursor: 
		cursor.execute(f"drop TABLE if exists {name}")
		cursor.execute(f"CREATE TABLE if not exists {name}(k varchar(64) COLLATE latin1_bin not null, n varchar(64) COLLATE latin1_bin not null, v int not null default 0, primary key(k,n,v) ) engine=myisam  DEFAULT CHARSET=latin1 COLLATE=latin1_bin") # not null default ''
		for sid, line in enumerate(fileinput.input(infile,openhook=fileinput.hook_compressed)): 
			try:
				arr = line.strip().split("\t") 
				if len(arr) == 3: 
					cursor.execute(f"insert ignore into {name}(k, n, v) values(%s, %s, %s)", arr) 
			except Exception as e:
				print ("ex:", e, sid, line) 
		my_conn.commit()
	print(f"{infile} is finished") 

if __name__	== '__main__':
	fire.Fire(run)