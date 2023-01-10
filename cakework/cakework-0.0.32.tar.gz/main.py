from cakework import Cakework

def say_hello(name, local=True):
    print("hello " + name)

cakework = Cakework(name="myproj")
cakework.add_task(say_hello)
