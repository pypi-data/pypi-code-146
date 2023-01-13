# 2022.12.12 , 
import json, traceback,sys, time, fire,os,traceback,fileinput,en, pymysql

def run(infile, host:str='172.17.0.1', port:int=3309, db:str='spacy'):
	'''  '''
	name = infile.split('.jsonlg')[0] 
	start = time.time()
	my_conn = pymysql.connect(host=host,port=port,user='root',password='cikuutest!',db=db)
	print ("started:", infile , my_conn,  flush=True)
	with my_conn.cursor() as cursor: 
		cursor.execute(f"drop TABLE if exists {name}") #_spacy
		cursor.execute(f"CREATE TABLE if not exists {name}(sid int primary key, snt text not null, spacy JSON) ENGINE=InnoDB ROW_FORMAT=COMPRESSED")
		for sid, line in enumerate(fileinput.input(infile,openhook=fileinput.hook_compressed)):  
			try:
				arr = json.loads(line.strip()) 
				doc = spacy.from_json(arr) 
				cursor.execute(f"insert ignore into {name}(sid, snt, spacy) values(%s, %s, %s)", (sid ,doc.text.strip(), line.strip()) )
			except Exception as e: 
				print ("ex:", e, sid,line)
				exc_type, exc_value, exc_traceback_obj = sys.exc_info()
				traceback.print_tb(exc_traceback_obj)
	my_conn.commit() 
	print(f"{infile} is finished, \t| using: ", time.time() - start) 

if __name__	== '__main__':
	fire.Fire(run)

'''
18874368 Dec 12 21:06 gzjc.ibd
121634816 Dec 12 21:07 clec.ibd
'''