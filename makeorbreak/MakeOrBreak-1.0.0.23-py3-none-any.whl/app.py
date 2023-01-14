from sys import argv
from controller import timer

def run():
    choice = argv[1]
    interval = argv[2]
    timer(choice, interval)

if __name__ == "__main__":
    run()