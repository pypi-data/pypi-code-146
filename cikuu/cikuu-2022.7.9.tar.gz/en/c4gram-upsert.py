#!/usr/bin/env python 2022.12.13
import redis ,fire,json, fileinput, traceback,sqlite3

def run(infile, sqlite:str="c4gram.sqlite", batch=1000000):
	''' uniq result to sqlite3, initially '''
	name = infile.split('-')[0]
	conn =	sqlite3.connect(sqlite, check_same_thread=False) 
	conn.execute('''CREATE TABLE if not exists c4gram(gram varchar(128) not null primary key, 
c0003 int not null default 0,
c0306 int not null default 0,
c0609 int not null default 0,
c10 int not null default 0,
c15 int not null default 0,
c2023 int not null default 0,
c2326 int not null default 0,
c2629 int not null default 0,
c3033 int not null default 0,
c3336 int not null default 0,
c3639 int not null default 0,
c40 int not null default 0,
c45 int not null default 0,
c50 int not null default 0,
c55 int not null default 0,
c60 int not null default 0,
c65 int not null default 0,
c7073 int not null default 0,
c7376 int not null default 0,
c7679 int not null default 0,
c8083 int not null default 0,
c8386 int not null default 0,
c8689 int not null default 0,
c9093 int not null default 0,
c9396 int not null default 0,
c9699 int not null default 0,
ca0 int not null default 0,
total int not null default 0) without rowid''')
	conn.execute('PRAGMA synchronous=OFF')
	conn.execute('PRAGMA case_sensitive_like = 1')
	conn.commit()

	print("started:", infile, conn , name,  flush=True)
	for sid, line in enumerate(fileinput.input(infile,openhook=fileinput.hook_compressed)): 
		try:
			if not isinstance(line, str): line = bytes.decode(line) # bytes 
			line = line.strip()
			idx = line.find(' ') 
			if idx < 0: continue
			cnt = int(line[0:idx])
			gram = line[idx+1:].strip()
			if not gram or gram > 'zzzzzz': continue #insert or ignore into si(s,i) values(?,?)
			#conn.execute(f'''INSERT INTO si(s,i) VALUES('{gram.replace("'", "''")}', {cnt})  ON CONFLICT(gram) DO UPDATE SET i = i + {cnt}''')
			conn.execute(f"INSERT INTO c4gram(gram,c{name}) VALUES(?,?) ON CONFLICT(gram) DO UPDATE SET c{name} = {cnt}", (gram, cnt))
			#conn.commit()
			#conn.execute(f"INSERT OR REPLACE INTO c4gram(gram,c{name}) VALUES(?,?)", (gram, cnt))
			if (sid) % batch == 0 : 
				print (f"[{name}] sid = {sid}, \t| {line} ", flush=True)
				conn.commit()
		except Exception as e:
			print ("ex:", e, "\t|", line) 

	conn.commit()
	print("finished:", infile)

if __name__ == '__main__':
	fire.Fire(run)

'''
INSERT into c4gram(gram,ca0) values('one', 12) on CONFLICT(gram) do update set ca0 = 12;
sqlite> select * from c4gram; 
one|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|7|12|0

sqlite> select * From c4gram; 
one|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|12|0
sqlite> INSERT OR REPLACE INTO c4gram(gram,c9699) values('one', 7);
sqlite> select * From c4gram; 
one|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|7|0|0
'''