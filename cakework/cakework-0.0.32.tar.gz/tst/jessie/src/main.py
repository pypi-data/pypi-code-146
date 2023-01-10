from cakework import Cakework

def say_hello(name):
    return("Hello " + name)

if __name__ == "__main__":
    app = Cakework("jessie")
    app.add_task(say_hello)
