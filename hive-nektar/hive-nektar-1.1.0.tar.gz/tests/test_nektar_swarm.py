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
    # Swarm Class                                    #
    # Community Management methods                   #
    ##################################################
    
    # custom_nodes = ["testnet.openhive.network"]
    # TESTNET = "18dcf0a285365fc58b71f18b3d3fec954aa0c141c44e4e5cb4cf777b9eab274e"

    counter += 1
    print(f"\nTEST #{counter}: Initialize Swarm class")
    hive = Swarm(tests["community1"], tests["username0"], wifs=tests["wifs0"])

    counter += 1
    print(f"\nTEST #{counter}: Mute a post.")
    hive.mute(tests["username3"], tests["permlink3"], "test-mute", mock=True)
    print("Transaction: " + json.dumps(hive.appbase.signed_transaction, indent=2))
    
    counter += 1
    print(f"\nTEST #{counter}: Unmute a post - option 1.")
    hive.mute(tests["username3"], tests["permlink3"], "test-mute", mute=False, mock=True)
    print("Transaction: " + json.dumps(hive.appbase.signed_transaction, indent=2))

    counter += 1
    print(f"\nTEST #{counter}: Unmute a post - option 2.")
    hive.unmute(tests["username3"], tests["permlink3"], "test-unmute", mock=True)
    print("Transaction: " + json.dumps(hive.appbase.signed_transaction, indent=2))

    counter += 1
    print(f"\nTEST #{counter}: Mark post as spam.")
    hive.mark_spam(tests["username3"], tests["permlink3"], mock=True)
    print("Transaction: " + json.dumps(hive.appbase.signed_transaction, indent=2))

    counter += 1
    print(f"\nTEST #{counter}: Update community properties.")
    title = tests["community1-title"]
    about = tests["community1-about"]
    is_nsfw = tests["community1-is-nsfw"]
    description = tests["community1-description"]
    flag_text = tests["community1-flag-text"]
    hive.update(title, about, is_nsfw, description, flag_text, mock=True)
    print("Transaction: " + json.dumps(hive.appbase.signed_transaction, indent=2))

    counter += 1
    print(f"\nTEST #{counter}: Subscribe to a community.")
    hive.subscribe()
    print("Transaction: " + json.dumps(hive.appbase.signed_transaction, indent=2))
    
    counter += 1
    print(f"\nTEST #{counter}: Unsubscribe to a community - option 1.")
    hive.subscribe(subscribe=False, mock=True)
    print("Transaction: " + json.dumps(hive.appbase.signed_transaction, indent=2))

    counter += 1
    print(f"\nTEST #{counter}: Unsubscribe to a community - option 2.")
    hive.unsubscribe(mock=True)
    print("Transaction: " + json.dumps(hive.appbase.signed_transaction, indent=2))
    
    hive.subscribe(mock=True)

    counter += 1
    print(f"\nTEST #{counter}: Pin a post.")
    hive.pin(tests["username3"], tests["permlink3"], mock=True)
    print("Transaction: " + json.dumps(hive.appbase.signed_transaction, indent=2))
    
    counter += 1
    print(f"\nTEST #{counter}: Unpin a post - option 1.")
    hive.pin(tests["username3"], tests["permlink3"], pin=False, mock=True)
    print("Transaction: " + json.dumps(hive.appbase.signed_transaction, indent=2))

    counter += 1
    print(f"\nTEST #{counter}: Unpin a post - option 2.")
    hive.unpin(tests["username3"], tests["permlink3"], mock=True)
    print("Transaction: " + json.dumps(hive.appbase.signed_transaction, indent=2))

    counter += 1
    print(f"\nTEST #{counter}: Flag a post.")
    hive.flag(tests["username3"], tests["permlink3"], "test-flag", mock=True)
    print("Transaction: " + json.dumps(hive.appbase.signed_transaction, indent=2))


if __name__ == "__main__":
    main()