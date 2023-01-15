from cakework import Client
import time 

client = Client("myproj", "dfde5b1d47f2134e90273ccd8b452ad157ffd6a4c850db29f9bdc0695affa0d2", local=True)

request_id = client.say_hello("jessie")
print(request_id)
status = client.get_status(request_id)
while status == 'PENDING' or status == 'IN_PROGRESS':
    time.sleep(1)
    status = client.get_status(request_id)
result = client.get_result(request_id)
print(result)
