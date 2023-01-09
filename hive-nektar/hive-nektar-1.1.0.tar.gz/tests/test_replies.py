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

    counter += 1
    print(f"\nTEST #{counter}: Initialize Waggle class.")
    hive = Waggle(tests["username1"])

    blogs = hive.blogs(limit=1)
    for blog in blogs:
        author = blog["author"]
        permlink = blog["permlink"]

        counter += 1
        print(
            f"\nTEST #{counter}: Get the content (blog or comment)."
        )
        content = hive.get_content(author, permlink)
        print(json.dumps(content, indent=2))

        counter += 1
        print(
            f"\nTEST #{counter}: Get the list replies in a blog post."
        )
        replies = hive.replies(author, permlink)
        print(json.dumps(replies, indent=2))

        counter += 1
        print(
            f"\nTEST #{counter}: Get the list of votes in a blog post."
        )
        votes = hive.votes(author, permlink)
        print(json.dumps(votes, indent=2))

        counter += 1
        print(
            f"\nTEST #{counter}: Returns a list of authors that have reblogged a post."
        )
        reblogs = hive.reblogs(author, permlink)
        print("Reblogged by: " + ", ".join(reblogs))


if __name__ == "__main__":
    main()