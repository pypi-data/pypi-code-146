from cakework import Client

client = Client("myproj", "dfde5b1d47f2134e90273ccd8b452ad157ffd6a4c850db29f9bdc0695affa0d2", local=True)

request_id = client.say_hello(name="jessie")
result = client.get_result(request_id)
print(result)
