from cakework import Cakework

def say_hello(name):
    return("hello " + name)

cakework = Cakework(name="myproj", local=True)
cakework.add_task(say_hello)
