import os, fire

def run(ibeg, iend, upload:bool=False):
	''' python c4-cl.py 2 10 '''
	for i in range(ibeg,iend):
		head = int(i / 100)
		j = str(10000 + i)
		name = f"c4-train.0{j[1:]}-of-01024.docjsonlg.3.4.1.gz"
		print (f"{name} is started, head={head}, j = {j}", flush=True) 
		if head > 9:  head = 'a' # added 2022.11.6
		if not os.path.exists(name): os.system(f"wget http://daka.wrask.com:8008/{head}/{name}")
		os.system(f"python3 c4cl.py {name}")
		os.remove(name)

		if upload: 
			os.system("sshpass -p cikuutest!2345 scp *.cl.gz ubuntu@rabbitmq.wrask.com:/ftp/c4cl")
			os.system("rm *.cl.gz")
		print (f"{name} is done") 

if __name__ == '__main__': 
	fire.Fire(run) 