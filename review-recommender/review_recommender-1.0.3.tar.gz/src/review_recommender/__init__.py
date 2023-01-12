import argparse
from .ranker import getRanking
from .data_retriveal import RepoRetriveal

def parse():
    parser = argparse.ArgumentParser(
                        prog = 'review_recommender',
                        description = 'Given pull request, rank revisors')

    parser.add_argument('owner', help='the owner of the repository') 
    parser.add_argument('repo', help='the name of the repository') 
    parser.add_argument('num', type=int, help='the number of the pull request')
    parser.add_argument('token', help='the github access token')

    args = parser.parse_args()
    return args.owner, args.repo, args.num, args.token

def run():
    owner, repo_name, pullNumber, token = parse()
    repo = RepoRetriveal(owner, repo_name, token)
    print(getRanking(repo, pullNumber).prettyFormat())