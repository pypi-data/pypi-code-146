from cakework import Cakework

def say_hello(name):
    return("hello")

cakework = Cakework("mytestapp", local=True)
cakework.add_task(say_hello)
