from sys import argv
from controller import timer

def run():
    mode = argv[1]
    choice = argv[2]
    interval = argv[3]
    timer(mode, choice, interval)

if __name__ == "__main__":
    run()