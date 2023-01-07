from cakework import Client
import time

client = Client("app", local=True)
request_id = client.say_hello(name="jessie 2")
print("Got request id: " +  request_id)
status = client.get_status(request_id)
print("got status: " + status)

while status != "FAILED" and status != "SUCCEEDED":
    time.sleep(1)
    status = client.get_status(request_id)
    print("got status: " + status)

print("Terminal status: " + status)

result = client.get_result(request_id)
print("Got result: " + result)
# print(request_id)

# import requests
# FRONTEND_URL = "http://localhost:8080"

# # FRONTEND_URL = "https://cakework-frontend.fly.dev"

# response = requests.patch(f"{FRONTEND_URL}/update-status", json={"userId": "shared", "app": "app", "requestId": "asdf", "status": "IN_PROGRESS"})
# print(response)