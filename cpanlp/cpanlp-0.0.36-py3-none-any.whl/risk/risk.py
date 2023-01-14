class Risk:
    def __init__(self, likelihood, impact):
        self.likelihood = likelihood
        self.impact = impact
        self.time_horizon = 1.0
        self.mitigation_cost =0.0