import os
import json
from arkivist import Arkivist
from sometime import Sometime
from nektar import Waggle
import nektar

def main():

    dt = Sometime().custom("%Y.%m.%d")

    counter = 0
    print("Initializing tests...")
    path = os.path.expanduser("~").replace("\\", "/")
    tests = Arkivist(path + "/nektar-tests.json", autosave=False)

    ##################################################
    # Waggle Class                                   #
    # Methods for blogging and engagement            #
    ##################################################

    counter += 1
    print(f"\nTEST #{counter}: Initialize Waggle class with dictionary of WIFs.")
    hive = Waggle(tests["username0"], wifs=tests["wifs0"])
    
    author = "merit.ahama"
    permlink = "get-acquainted-with-chain-chatter-by-leofinance-leo-and-hodl-contest"
    
    counter += 1
    print(f"\nTEST #{counter}: Reblog")
    hive.reblog(author, permlink)


if __name__ == "__main__":
    main()
