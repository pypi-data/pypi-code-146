import os, fire

maphost= {"0": "py.jukuu.com:8008",
"1":"101.35.195.71:8008",
}

def run(ibeg, iend):
	''' python c4-np.py 0 100 '''
	for i in range(ibeg,iend):
		head = int(i / 100)
		j = str(10000 + i)
		name = f"c4-train.0{j[1:]}-of-01024.docjsonlg.3.4.1.gz"
		print (f"{name} is started, head={head}, j = {j}", flush=True) 
		if head > 9:  head = 'a' # added 2022.11.6
		#os.system(f"wget http://py.jukuu.com:8008/{head}/{name}")
		os.system(f"wget http://cpu76.wrask.com:8008/{head}/{name}")
		os.system(f"python3 c4np.py {name}")
		os.remove(name)
		os.system("sshpass -p cikuutest!2345 scp *.np.gz ubuntu@rabbitmq.wrask.com:/data/c4np")
		os.system("rm *.np.gz")
		print (f"{name} is done") 

if __name__ == '__main__': 
	fire.Fire(run) 