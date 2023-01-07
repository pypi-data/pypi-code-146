# 22-8-22
import requests

dsk = requests.get("http://cpu76.wrask.com:8000/dsk", params={"essay":"She has ready. It are ok."}).json()
print (dsk ) 

for ar in dsk['snt']:
	for kp, v in ar['feedback'].items():
		print(v.get('kp',''),  v.get('cate',''),  v.get('ibeg',0), v.get('short_msg','') )
