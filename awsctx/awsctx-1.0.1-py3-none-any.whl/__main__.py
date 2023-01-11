import sys

# from awsctx import ctxmanager
from awsctx.awsctx import ctxmanager

def main():

    try:
        option = sys.argv[1]
    except IndexError as e:
        option = None
    
    ctxmanager(option)

if __name__ == "__main__":
    main()