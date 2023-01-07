import os, fire

def run(ibeg, iend):
	''' python c4-postag.py 2 10 '''
	for i in range(ibeg,iend):
		head = int(i / 100)
		j = str(10000 + i)
		name = f"c4-train.0{j[1:]}-of-01024.docjsonlg.3.4.1.gz"
		print (f"{name} is started, head={head}, j = {j}", flush=True) 
		os.system(f"wget http://cpu76.wrask.com:8008/{head}/{name}")
		os.system(f"python3 c4postag.py {name}")
		os.remove(name)
		print (f"{name} is done") 

if __name__ == '__main__': 
	fire.Fire(run) 
