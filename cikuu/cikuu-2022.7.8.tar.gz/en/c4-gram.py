# 2022.11.18
import os, fire

def run(ibeg, iend, keep:bool=True):
	''' python c4-gram.py 2 10 '''
	for i in range(ibeg,iend):
		try:
			head = int(i / 100)
			j = str(10000 + i)
			name = f"c4-train.0{j[1:]}-of-01024.docjsonlg.3.4.1.gz"
			print (f"{name} is started, head={head}, j = {j}", flush=True) 
			if head > 9:  head = 'a' # added 2022.11.6
			if not os.path.exists(name): #http://cpu76.wrask.com:8008/5/c4-train.00503-of-01024.docjsonlg.3.4.1.gz
				os.system(f"wget http://cpu76.wrask.com:8008/{head}/{name}")
			os.system(f"python3 c4gram.py {name}")
			os.remove(name)

			#if upload: # sudo apt install sshpass,  | initial , use scp to copy a small file manually 
			os.system("sshpass -p cikuutest!2345 scp *.7.gz ubuntu@rabbitmq.wrask.com:/data/c4gram")
			os.system("rm *.7")
			if not keep: os.system("rm *.7.gz")
			print (f"{name} is done") 
		except Exception as e:
			print ( "ex:", e, i) 

if __name__ == '__main__': 
	fire.Fire(run) 