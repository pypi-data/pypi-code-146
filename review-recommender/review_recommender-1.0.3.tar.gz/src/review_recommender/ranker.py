from . import data_retriveal
from .inverted_files import InvertedFile
from .tokenizer import Tokenizer
from .scorer import Scorer


# def loadingBarCallback(done, total):
#     numOfTicks = 50
#     percentage = int(done/total*100)
#     print('done: ' + '-'* int(done/total* numOfTicks) + f'{percentage} %', end="\r")
#     if percentage == 100: print('\n')

def getRanking(repo: data_retriveal.RepoRetriveal, pullNumber, 
               numberOfPulls=30, numberOfCommits=30):
    """
    Given a repository and a pull number, returns a rank of possible revisors:

    Args:
        repo(data_retriveal.RepoRetriveal) : the repository
        pullNumber(int): the number of the pull
        numberOfPulls(int): number of pulls you want to retrieve, defaults to 30
        numberOfCommits(int): number of commits you want to retrieve, defaults to 30

    Raises:
        requests.HTTPError: the repository or the pull number is invalid.
    """
    scorer = Scorer()
    invertedFile = InvertedFile()

    newPull = repo.getPullByNumber(pullNumber)

    print('collecting pulls...')
    for pull in repo.getPullIterable(pullNumber, numberOfPulls):
        files = repo.getPullFiles(pull)
        pullTokenFreqs = Tokenizer.getTokenFreqs(files)
        invertedFile.add(pull, pullTokenFreqs)

    print('collecting commits...')
    for commit in repo.getCommitsIterable(newPull.date, numberOfCommits):
        files = repo.getCommitFiles(commit)
        commitTokenFreqs = Tokenizer.getTokenFreqs(files)
        invertedFile.add(commit, commitTokenFreqs)
    
    newPullTokenFreqs = Tokenizer.getTokenFreqs(repo.getPullFiles(newPull))
    similar = invertedFile.getSimilar(newPullTokenFreqs)

    print('getting rank...')
    for item, score in similar.items():
        if isinstance(item, data_retriveal.RepoRetriveal.Commit) \
            and not item.author_login == newPull.author_login:
            scorer.addReviewerScore(item.author_login, score)
        elif isinstance(item, data_retriveal.RepoRetriveal.PullRequest):
            for reviewer in item.reviewers:
                if not reviewer == newPull.author_login:
                    scorer.addReviewerScore(reviewer, score)

    return scorer