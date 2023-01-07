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
    
    NEKTAR_VERSION = nektar.__version__
    custom_nodes = ["testnet.openhive.network"]
    # TESTNET = "18dcf0a285365fc58b71f18b3d3fec954aa0c141c44e4e5cb4cf777b9eab274e"
    # MAINNET = "beeab0de00000000000000000000000000000000000000000000000000000000"

    counter += 1
    print(f"\nTEST #{counter}: Initialize Waggle class.")
    hive = Waggle(tests["username2"], wif=tests["wifs2"]["posting"], role="posting")

    counter += 1
    print(f"\nTEST #{counter}: Initialize Waggle class with dictionary of WIFs.")
    hive = Waggle(tests["username2"], wifs=tests["wifs2"])

    counter += 1
    print(f"\nTEST #{counter}: Initialize Waggle class with app and version")
    hive = Waggle(tests["username2"], wifs=tests["wifs2"], app="nektar.app", version=dt)

    counter += 1
    custom_nodes = ["testnet.openhive.network"]
    print(f"\nTEST #{counter}: Initialize Waggle class with custom parameters")
    hive = Waggle(tests["username2"], wifs=tests["wifs2"],
        timeout=25,
        retries=1,
        warning=True)

    counter += 1
    print(f"\nTEST #{counter}: Get the list of communities")
    communities = {}
    sorting = ["new", "rank", "subs"]
    for sort in sorting:
        for community in hive.communities(limit=100, sort=sort):
            communities.update({community["name"]: community})
    community = list(communities.keys())[5]
    print(", ".join(list(communities.keys())))

    counter += 1
    print(f"\nTEST #{counter}: Get the name and title of each community")
    print(len(communities))
    for name, data in communities.items():
        print(name + "\t" + data["title"])
        break

    counter += 1
    print(f"\nTEST #{counter}: Get the subscribers of a community.")
    subscribers = {}
    for subscriber in hive.subscribers(community, limit=10):
        subscribers.update({subscriber[0]: subscriber})
        print(subscriber[0])
        break

    counter += 1
    print(f"\nTEST #{counter}: Get the list of 100 Hive blockchain accounts.")
    accounts = {}
    for account in hive.accounts():
        print(account)
        break

    counter += 1
    print(
        f"\nTEST #{counter}: Get the list of 10 Hive blockchain starting with `a`."
    )
    accounts = {}
    for account in hive.accounts(start="a", limit=10):
        print(account)

    counter += 1
    print(
        f"\nTEST #{counter}: Get the list of 10 community posts in order of creation and not yet paid out."
    )
    posts = hive.posts(community, limit=10, sort="created", paidout=False)
    for post in posts:
        print(post["title"])

    counter += 1
    print(
        f"\nTEST #{counter}: Get the list of 1000 followers of the initialized account."
    )
    followers = hive.followers()
    print(", ".join(followers))

    counter += 1
    print(
        f"\nTEST #{counter}: Get the list of 10 muted followers of another account."
    )
    followers = hive.followers(account=tests["username1"], ignore=True, limit=10)
    print(", ".join(followers))

    counter += 1
    print(
        f"\nTEST #{counter}: Get the list of up to 1000 account transactions, most recent first."
    )
    transactions = hive.history()
    print("Transactions:", json.dumps(transactions[1], indent=2))

    counter += 1
    print(
        f"\nTEST #{counter}: Get the list of up to 1000 account transactions of another account."
    )
    transactions = hive.history(account=tests["username1"], start=1000, low=0)
    print("Transactions:", json.dumps(transactions[1], indent=2))

    counter += 1
    print(
        f"\nTEST #{counter}: Get the list of up to 100 account transactions of another account starting from the 5000th transaction to the oldest."
    )
    transactions = hive.history(account=tests["username1"], start=5000, limit=100)
    for transaction in transactions[:1]:
        print(transaction[0], transaction[1]["op"])

    counter += 1
    print(
        f"\nTEST #{counter}: Get the list of posts of the initizalized account."
    )
    blogs = hive.blogs()
    print(json.dumps(blogs[0], indent=2))

    counter += 1
    print(
        f"\nTEST #{counter}: Get the list of posts of another account with non-default values."
    )
    blogs = hive.blogs(account=tests["username1"], sort="created", paidout=True, limit=100)
    print(json.dumps(blogs[0], indent=2))

    counter += 1
    print(f"\nTEST #{counter}: Get the post data.")
    author = tests["username1"]
    permlink = tests["permlink1"]
    data = hive.get_post(author, permlink)
    print(json.dumps(data, indent=2))

    counter += 1
    print(
        f"\nTEST #{counter}: Try to get the post data, return empty if not yet present in the blockchain."
    )
    author = tests["username1"]
    permlink = "abc-123-def-456"
    data = hive.get_post(author, permlink, retries=2)
    print(json.dumps(data, indent=2))
    
    counter += 1
    print(f"\nTEST #{counter}: Publish a new post.")
    dt = Sometime().custom("%Y-%m-%d %H:%M:%S%Z")
    title = f"UPDATE! Connect to Hive with Nektar v{NEKTAR_VERSION} for Python"
    body = f"Introducing Nektar v{NEKTAR_VERSION}! \n\n![](https://images.hive.blog/1536x0/https://images.ecency.com/DQmSYmmPbB9DqXRhgMpC3Ef4NyaF1QJCxm2CqGi9vWpfWTa/honey.jpg)\n<center><sup>Photo by [micheile dot com](https://unsplash.com/photos/lgBPvNjHe6k) on Unsplash</sup></center>\n\n\"How do I connect to Hive?\"\n\nWell, you can now use Nektar.\n\n**[Nektar](https://github.com/rmaniego/nektar)** allows you to to the Hive blockchain using the Hive API.\n\n*Checkout the ReadMe for the full list of features and udpates!*\n\n\n---\n\n\n**TEST DATE:** {dt}\n\n***DISCLAIMER:** This is an official Nektar SDK test, do not flag!!*"
    description = "Nektar is here!"
    tags = "nektar hive api coderundebug"
    community = tests["community2"]
    result = hive.new_post(title, body, description, tags, community)
    
    counter += 1
    print(f"\nTEST #{counter}: Reply a comment to a post or another comment.")
    author = tests["username1"]
    permlink = tests["permlink1"]
    body = "Great work in there, keep it up!\n\n---\n" "Check our [community](#) page!\n\n***DISCLAIMER:**This is an official Nektar SDK test only, do not flag!!*"
    hive.reply(author, permlink, body)

    counter += 1
    print(f"\nTEST #{counter}: Vote to a post or another comment.")
    author = tests["username1"]
    permlink = tests["permlink1"]
    weight = 100
    hive.vote(author, permlink, weight)

    counter += 1
    print(f"\nTEST #{counter}: Get a recently signed transaction.")
    signed_transaction = hive.appbase.signed_transaction

    counter += 1
    # Passing on MAINNET only!
    print(
        f"\nTEST #{counter}: Verify if signed transaction contains required auths."
    )
    verified = hive.verify_authority(signed_transaction)
    print("OK:" + str(verified))
    
    counter += 1
    print(f"\nTEST #{counter}: Power Up")
    hive.power_up(tests["username2"], 0.001)


if __name__ == "__main__":
    main()
