from cakework import Client
import time

def run():
    client = Client("myproj", "e18f932363a14047c39573bcf7bcbefb290e16fec23eddeab9d98df11f3ec2df", local=True) # when this initializes, we pull from the repo the registered activities
    request_id = client.say_hello("jesie")
    status = client.get_status(request_id)
    while(status == 'IN_PROGRESS' or status == 'PENDING'):
        time.sleep(1)
        status = client.get_status(request_id)
    if status == 'SUCCEEDED':
        result = client.get_result(request_id)
        print(result)
    else:
        print("Failed")

if __name__ == '__main__':
    run()
