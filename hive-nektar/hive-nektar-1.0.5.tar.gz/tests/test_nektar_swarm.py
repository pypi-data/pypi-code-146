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
    
    custom_nodes = ["testnet.openhive.network"]
    TESTNET = "18dcf0a285365fc58b71f18b3d3fec954aa0c141c44e4e5cb4cf777b9eab274e"

    counter += 1
    print(f"\nTEST #{counter}: Initialize Swarm class")
    hive = Swarm(tests["community1"], tests["username0"], wif=tests["wifs0"]["posting"], role="posting")
    
    counter += 1
    print(f"\nTEST #{counter}: Initialize Swarm class with dictionary of WIFs.")
    hive = Swarm(tests["community1"], tests["username0"], wifs=tests["wifs0"])
    
    counter += 1
    print(f"\nTEST #{counter}: Initialize Swarm class with app and version")
    hive = Swarm(tests["community1"], tests["username0"], app="nektar.app", version=dt)

    counter += 1
    print(f"\nTEST #{counter}: Initialize Swarm class with custom parameters")
    hive = Swarm(tests["community1"], tests["username0"], wifs=tests["wifs0"],
        nodes=custom_nodes,
        chain_id=TESTNET,
        timeout=25,
        retries=1,
        warning=True)
    
    hive = Swarm(tests["community1"], tests["username0"])

    counter += 1
    print(f"\nTEST #{counter}: Mute a post.")
    hive.mute(tests["username3"], tests["permlink3"], "test-mute")
    print("Transaction: " + json.dumps(hive.appbase.signed_transaction, indent=2))
    
    counter += 1
    print(f"\nTEST #{counter}: Unmute a post - option 1.")
    hive.mute(tests["username3"], tests["permlink3"], "test-mute", mute=False)
    print("Transaction: " + json.dumps(hive.appbase.signed_transaction, indent=2))

    counter += 1
    print(f"\nTEST #{counter}: Unmute a post - option 2.")
    hive.unmute(tests["username3"], tests["permlink3"], "test-unmute")
    print("Transaction: " + json.dumps(hive.appbase.signed_transaction, indent=2))

    counter += 1
    print(f"\nTEST #{counter}: Mark post as spam.")
    hive.mark_spam(tests["username3"], tests["permlink3"])
    print("Transaction: " + json.dumps(hive.appbase.signed_transaction, indent=2))

    counter += 1
    print(f"\nTEST #{counter}: Update community properties.")
    title = tests["community1-title"]
    about = tests["community1-about"]
    is_nsfw = tests["community1-is-nsfw"]
    description = tests["community1-description"]
    flag_text = tests["community1-flag-text"]
    hive.update(title, about, is_nsfw, description, flag_text, debug=True)
    print("Transaction: " + json.dumps(hive.appbase.signed_transaction, indent=2))

    counter += 1
    print(f"\nTEST #{counter}: Subscribe to a community.")
    hive.subscribe()
    print("Transaction: " + json.dumps(hive.appbase.signed_transaction, indent=2))
    
    counter += 1
    print(f"\nTEST #{counter}: Unsubscribe to a community - option 1.")
    hive.subscribe(subscribe=False)
    print("Transaction: " + json.dumps(hive.appbase.signed_transaction, indent=2))

    counter += 1
    print(f"\nTEST #{counter}: Unsubscribe to a community - option 2.")
    hive.unsubscribe()
    print("Transaction: " + json.dumps(hive.appbase.signed_transaction, indent=2))
    
    hive.subscribe()

    counter += 1
    print(f"\nTEST #{counter}: Pin a post.")
    hive.pin(tests["username3"], tests["permlink3"])
    print("Transaction: " + json.dumps(hive.appbase.signed_transaction, indent=2))
    
    counter += 1
    print(f"\nTEST #{counter}: Unpin a post - option 1.")
    hive.pin(tests["username3"], tests["permlink3"], pin=False)
    print("Transaction: " + json.dumps(hive.appbase.signed_transaction, indent=2))

    counter += 1
    print(f"\nTEST #{counter}: Unpin a post - option 2.")
    hive.unpin(tests["username3"], tests["permlink3"])
    print("Transaction: " + json.dumps(hive.appbase.signed_transaction, indent=2))

    counter += 1
    print(f"\nTEST #{counter}: Flag a post.")
    hive.flag(tests["username3"], tests["permlink3"], "test-flag")
    print("Transaction: " + json.dumps(hive.appbase.signed_transaction, indent=2))


if __name__ == "__main__":
    main()
