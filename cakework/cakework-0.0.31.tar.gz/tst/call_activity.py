from cakework import Client
# from cakework import task

from functools import wraps

# @task(Client)
# def say_hello(name):
#     print("local")
#     return "hello " + name

def run():
    # somehow loads the client; either from 
    client = Client("myapp2") # when this initializes, we pull from the repo the registered activities
    # when we create a new app and register the activity, we store the activity's interface
    # when someone instantiates a new client, we check remotely the registered activities
    # q: can we auto-generate and import a 
    response = client.say_hello("jessie") # currently, no intellisense/auto complete
    print("Got greeting: " + response)

if __name__ == '__main__':
    run()
