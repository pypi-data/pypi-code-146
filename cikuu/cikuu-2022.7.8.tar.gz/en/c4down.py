import os, fire

def run(ibeg, iend):
	''' python c4down.py 2 10 '''
	for i in range(ibeg,iend):
		head = int(i / 100)
		j = str(10000 + i)
		name = f"c4-train.0{j[1:]}-of-01024.docjsonlg.3.4.1.gz"
		if not os.path.exists(name):
			print (f"{name} is started, head={head}, j = {j}", flush=True) 
			os.system(f"wget http://cpu76.wrask.com:8008/{head}/{name}")
			print (f"{name} is done") 
		else: 
			print (f"{name} exists") 

if __name__ == '__main__': 
	fire.Fire(run) 
