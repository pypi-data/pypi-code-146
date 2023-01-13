# 2022.12.28 , 
import json, traceback,sys, time, fire,os,traceback,fileinput,en

def run(infile, outfile:str=None):
	'''  '''
	name = infile.split('.jsonlg')[0] 
	if outfile is None: outfile = name + ".snt"
	start = time.time()
	print ("started:", infile ,  flush=True)
	with open(outfile, 'w') as fw: 
		for sid, line in enumerate(fileinput.input(infile,openhook=fileinput.hook_compressed)):  
			try:
				arr = json.loads(line.strip()) 
				snt = arr.get("text",'').strip()
				if not snt: 
					print("no text found:\t|", line)
					continue
				fw.write(f"{snt}\n")
			except Exception as e: 
				print ("ex:", e, sid,line)
				exc_type, exc_value, exc_traceback_obj = sys.exc_info()
				traceback.print_tb(exc_traceback_obj)
	print(f"{infile} is finished, \t| using: ", time.time() - start) 

if __name__	== '__main__':
	fire.Fire(run)

'''
18874368 Dec 12 21:06 gzjc.ibd
121634816 Dec 12 21:07 clec.ibd
'''