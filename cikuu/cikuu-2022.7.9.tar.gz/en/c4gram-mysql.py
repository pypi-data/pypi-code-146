# 2022.12.10
import json, traceback,sys, time,  fileinput, os, fire, pymysql

def run(infile, host='192.168.98.3', port=3309, batch:int=10000000):
	''' a0-c4gram.uniq.gz '''
	start = time.time()
	name = infile.split('-')[0]
	my_conn = pymysql.connect(host=host,port=port,user='root',password='cikuutest!',db='c4')
	print ("started:", infile , my_conn, host, name,  flush=True)
	with my_conn.cursor() as cursor: 
		cursor.execute(f"drop table if exists c4gram_{name}")
		#cursor.execute(f"create table if not exists c4gram_{name}( gram varchar(128) not null primary key, cnt int not null default 0) engine=myisam COLLATE=utf8_bin")
		cursor.execute(f"create table if not exists c4gram_{name}( gram varchar(128) not null, cnt int not null default 0) engine=myisam COLLATE=utf8_bin")

		data = []
		for sid, line in enumerate(fileinput.input(infile,openhook=fileinput.hook_compressed)): 
			try:
				if not isinstance(line, str): line = bytes.decode(line) # bytes 
				line = line.strip()
				idx = line.find(' ') 
				if idx < 0: continue
				cnt = int(line[0:idx])
				gram = line[idx+1:].strip()
				if not gram or gram > 'zzzzzz' or len(gram) > 128 : continue 
				#cursor.execute(f"INSERT INTO c4gram_{name}(gram, cnt) VALUES (%s,%s) ON DUPLICATE KEY UPDATE cnt=cnt+{cnt}", (gram,cnt))
				data.append( (gram, cnt) )
				if len(data) >= batch : 
					res = cursor.executemany(f"INSERT ignore INTO c4gram_{name}(gram, cnt) VALUES (%s,%s)",data) 
					print (f"[{name}] sid = {sid}, \t| {line} \t|", res, time.strftime('%H:%M:%S',time.localtime(time.time())), flush=True)
					data = []
			except Exception as e:
				print ("ex:", e, sid, line) 

		if len(data) > 0 : cursor.executemany(f"INSERT ignore INTO c4gram_{name}(gram, cnt) VALUES (%s,%s)",data) 
		my_conn.commit()
	print(f"{infile} is finished, \t| using: ", time.time() - start)

if __name__	== '__main__':
	fire.Fire(run)