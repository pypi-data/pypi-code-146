import pytest
from review_recommender.scorer import *

def test_scorer():
    scorer = Scorer()
    scorer.addReviewerScore("Reviewer1", 10)
    scorer.addReviewerScore("Reviewer1", 20)
    scorer.addReviewerScore("Reviewer2", 15)
    scorer.addReviewerScore("Reviewer3", 20)
    
    #assert scorer.getSorted() == {"Reviewer1": 30}

    assert scorer.getSorted() == {"Reviewer2": 15, "Reviewer3": 20, "Reviewer1": 30}

FORMATTED_DATA = """Reviewer         | Score      
-----------------------------
Reviewer1        | 46.15 %
Reviewer3        | 30.77 %
Reviewer2        | 23.08 %
"""

def test_scorer_prettyFormat():
    scorer = Scorer()
    scorer.addReviewerScore("Reviewer1", 10)
    scorer.addReviewerScore("Reviewer1", 20)
    scorer.addReviewerScore("Reviewer2", 15)
    scorer.addReviewerScore("Reviewer3", 20)
    
    print(scorer.prettyFormat())
    assert scorer.prettyFormat() == FORMATTED_DATA