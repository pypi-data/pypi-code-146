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
    hive = Waggle(tests["username2"], wifs=tests["wifs2"])
    
    author = "cheeamaka"
    permlink = "connected-yet-very-disconnected"
    
    counter += 1
    print(f"\nTEST #{counter}: Voted")
    voted = hive.voted(author, permlink)
    print("Voted:", voted)
    
    counter += 1
    print(f"\nTEST #{counter}: Upvote")
    hive.vote(author, permlink, 10000, check=True)


if __name__ == "__main__":
    main()
