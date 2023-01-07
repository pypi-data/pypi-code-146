import os
import json
from arkivist import Arkivist
from nektar import Waggle, Swarm
from sometime import Sometime

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
    
    # custom_nodes = ["testnet.openhive.network"]
    # TESTNET = "18dcf0a285365fc58b71f18b3d3fec954aa0c141c44e4e5cb4cf777b9eab274e"

    print("\nTEST: Initialize Waggle class.")
    hive = Waggle(tests["username0"], wifs=tests["wifs0"])

    """
    print("\nTEST: Get the delegators")
    delegators = hive.delegators()
    print(json.dumps(delegators, indent=2))


    print("\nTEST: Get the list of active account delegators of another account.")
    delegators = hive.delegators(account=tests["username1"], active=True)
    print(json.dumps(delegators, indent=2))
    """
    
    print("\nTEST: Get the list of account delegatees.")
    delegatees = hive.delegatees()
    print(json.dumps(delegatees, indent=2))

    print("\nTEST: Get the list of active account delegatees of another account.")
    delegatees = hive.delegatees(account=tests["username1"], active=True)
    print(json.dumps(delegatees, indent=2))


if __name__ == "__main__":
    main()
