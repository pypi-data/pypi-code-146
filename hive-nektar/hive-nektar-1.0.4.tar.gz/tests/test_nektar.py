import os
import json
from arkivist import Arkivist
from sometime import Sometime
from nektar import Nektar

def main():

    dt = Sometime().custom("%Y.%m.%d")

    counter = 0
    print("Initializing tests...")
    path = os.path.expanduser("~").replace("\\", "/")
    tests = Arkivist(path + "/nektar-tests.json", autosave=False)

    ##################################################
    # Nektar Class / Base Class                      #
    ##################################################
    
    # custom_nodes = ["testnet.openhive.network"]
    # TESTNET = "18dcf0a285365fc58b71f18b3d3fec954aa0c141c44e4e5cb4cf777b9eab274e"

    print(f"\nTEST: Initialize Nektar class with dictionary of WIFs.")
    hive = Nektar(tests["username0"], wifs=tests["wifs0"])

    """
    print(f"\nTEST: Initialize Nektar class with app and version")
    hive = Nektar(tests["username0"], wifs=tests["wifs0"], app="nektar.app", version=dt)

    print(f"\nTEST: Get the list of blockchain constants")
    # Hive Developer Portal > Understanding Configuration Values
    # https://developers.hive.io/tutorials-recipes/understanding-configuration-values.html
    data = hive.get_config()
    print(json.dumps(data, indent=2))

    print(f"\nTEST: Get the list of blockchain constants")
    data = hive.get_config(field="HIVE_CHAIN_ID", fallback="bee*")
    print("HIVE_CHAIN_ID: " + str(data))

    print(
        f"\nTEST: Get the initialized account's recent resource credits."
    )
    data = hive.resource_credits()
    print(data)

    print(f"\nTEST: Get another account's recent resource credits.")
    data = hive.resource_credits(tests["username0"])
    print(data)

    print(
        f"\nTEST: Get the initialized account's remaining mana in percentage."
    )
    percentage = hive.manabar()
    print("Current Mana: " + str(int(percentage)) + "%")

    print(
        f"\nTEST: Get another account's remaining mana in percentage."
    )
    percentage = hive.manabar()
    print("Current Mana: " + str(int(percentage)) + "%")

    print(f"\nTEST: Transfer HBD to another account with a message.")
    receiver = tests["username1"]
    amount = 0.001
    asset = "HBD"
    message = "Thanks for supporting us! - test"
    hive.memo(receiver, amount, asset, message)

    print(f"\nTEST: Transfer HIVE to another account with a message.")
    receiver = tests["username1"]
    amount = 0.001
    asset = "HIVE"
    message = "Thanks for supporting us! - test"
    result = hive.memo(receiver, amount, asset, message)

    print(f"\nTEST: Transfer HBD to savings with a message.")
    receiver = tests["username0"]
    amount = 0.001
    asset = "HBD"
    message = "Thanks for supporting us! - test"
    hive.transfer_to_savings(receiver, amount, asset, message)

    print(f"\nTEST: Transfer HIVE to savings with a message.")
    receiver = tests["username0"]
    amount = 0.001
    asset = "HIVE"
    message = "Thanks for supporting us! - test"
    hive.transfer_to_savings(receiver, amount, asset, message)

    print(f"\nTEST: Transfer to vesting.")
    receiver = tests["username0"]
    amount = 0.001
    hive.transfer_to_vesting(receiver, amount)

    print(f"\nTEST: Broadcast a custom JSON.")
    auths = [tests["username0"]]
    hive.custom_json(
        id_="nektar-tests",
        jdata={ "test": "nektar" },
        required_auths=auths)

    print(f"\nTEST: Broadcast a custom JSON.")
    auths = [tests["username0"]]
    hive.custom_json(
        id_="nektar-tests",
        jdata={ "test": "nektar" },
        required_posting_auths=auths)
    """

if __name__ == "__main__":
    main()
