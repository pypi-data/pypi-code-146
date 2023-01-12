class Scorer:
    """
    A simple scoreboard for reviewers.
    """
    def __init__(self):
        self.reviewerToScore = {}
        
    def addReviewerScore(self, reviewer, score):
        """
        Add a score to a reviewer.

        Args:
            reviewer(string)
            score(float)
        """
        if reviewer not in self.reviewerToScore:
            self.reviewerToScore[reviewer] = 0
        self.reviewerToScore[reviewer] += score

    def getSorted(self):
        """
        Returns a dictionary sorted by decreasing order of scores.

        Returns:
            dict[string, float]: reviewer-score pairs.
        """
        reviewer = dict(sorted(self.reviewerToScore.items(), 
                               key=lambda item: item[1], 
                               reverse=True))
        return reviewer

    def prettyFormat(self):
        """
        Returns a formatted string of the scores in percentage.
        """
        totalScore = 0
        for score in self.reviewerToScore.values(): totalScore += score

        finalString = 'Reviewer         | Score      ' + '\n'
        finalString += '-----------------------------' + '\n'
        for reviewer, score in self.getSorted().items():
            spaces = ' ' * (len('Reviewer         ') - len(reviewer))
            finalString += (reviewer + spaces + '|' + f'{score/totalScore*100: .2f} %' + '\n')

        return finalString


