from review_recommender.ranker import getRanking
from review_recommender.data_retriveal import RepoRetriveal
import logging

def is_among_top_K(sorted_recommended_reviewers, actual_reviewers, K):
    for i, reviewer in enumerate(sorted_recommended_reviewers):
        if i+1 > K: return 0
        if reviewer in actual_reviewers: return 1
    return 0

#def jaccard_similarity(set1, set2):
#    return len(set1.intersection(set2))/len(set1.union(set2))

class MetricAdder:
    def __init__(self):
        self.current_metric = 0
        self.num_of_pulls = 0
    
    def add(self, metric):
        self.current_metric += metric
        self.num_of_pulls += 1
    
    def getAverage(self):
        return self.current_metric/self.num_of_pulls

token = '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'
REPOS = [('opencv/opencv', 23008), ('numpy/numpy', 22891)]

selected_repo = REPOS[0]
startingPullNumber = selected_repo[1]
repo = RepoRetriveal(*selected_repo[0].split('/'), token)
NUM_OF_PULLS = 30
NUM_OF_COMMITS = 10

def evaluate_on_single_pull(pull):
    logger = logging.getLogger('evaluation')
    scores = getRanking(repo, pull.number, NUM_OF_PULLS, NUM_OF_COMMITS)
    sorted_recommended_reviewers = scores.getSorted()
    actual_reviewers = set(pull.reviewers)
    #similarity = jaccard_similarity(recommended_reviewers, actual_reviewers)
    metric = is_among_top_K(sorted_recommended_reviewers, actual_reviewers, K=3)
    logger.info(f'{pull}')
    logger.info(scores.prettyFormat())
    #logging.info(f'jaccard: {similarity}')
    logger.info(f'metric: {metric}')
    return metric

def evaluate_ranker():
    logger = logging.getLogger('evaluation')
    logger.setLevel(logging.INFO)
    fileHandler = logging.FileHandler(logger.name + '.log', mode='w')
    logger.addHandler(fileHandler)

    adder = MetricAdder()
    for pull in repo.getPullIterable(startingPullNumber, 50):
        if not pull.reviewers: continue
        adder.add(evaluate_on_single_pull(pull))
    
    print(adder.getAverage())

if __name__ == '__main__':
    #pull = repo.getPullByNumber(23008)
    evaluate_ranker()