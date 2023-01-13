import os, fire

def run(ibeg, iend):
	''' python c4-trp.py 0 1024 '''
	for i in range(ibeg,iend):
		head = int(i / 100)
		j = str(10000 + i)
		name = f"c4-train.0{j[1:]}-of-01024.docjsonlg.3.4.1.gz"
		print (f"{name} is started, head={head}, j = {j}", flush=True) 
		os.system(f"wget http://daka.wrask.com:8008/{head}/{name}")
		os.system(f"python3 c4trp.py {name}")
		os.remove(name)
		#os.system("sshpass -p Cikuutest1 scp *.trp.gz ubuntu@daka.wrask.com:/ftp/c4trp")
		#os.system("rm *.trp.gz")
		print (f"{name} is done") 

if __name__ == '__main__': 
	fire.Fire(run) 