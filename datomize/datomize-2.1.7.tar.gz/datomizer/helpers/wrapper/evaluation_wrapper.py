TOTAL_SCORE = "totalScore"
SUMMARY = "measuresSummary"


class EvaluationWrapper(object):
    evaluation = {}

    def __init__(self, evaluation):
        self.evaluation = evaluation

    def get_total_score(self):
        return self.evaluation[TOTAL_SCORE]

    def get_summary(self):
        return self.evaluation[SUMMARY]

    def __str__(self):
        return f"total_score: {str(self.get_total_score())}, summary: {str(self.get_summary())}"
