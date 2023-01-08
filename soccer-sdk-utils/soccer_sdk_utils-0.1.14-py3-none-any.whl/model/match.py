class Match:
    def __init__(self, **kwargs):
        self.date = kwargs.get("date")
        self.gender = kwargs.get("gender")
        self.division = kwargs.get("division")
        self.team1 = kwargs.get("team1")
        self.team2 = kwargs.get("team2")
        self.score1 = kwargs.get("score1", 0)
        self.score2 = kwargs.get("score2", 0)

    def __repr__(self):
        if self.date is None:
            if self.division is None:
                return f"{self.team1} [{self.score1}] - {self.team2} [{self.score2}]"
            else:
                return f"{self.division} {self.team1} [{self.score1}] - {self.team2} [{self.score2}]"
        else:
            if self.division is None:
                return f"{self.date} {self.team1} [{self.score1}] - {self.team2} [{self.score2}]"
            else:
                return f"{self.date} {self.division} {self.team1} [{self.score1}] - {self.team2} [{self.score2}]"

    @property
    def is_draw(self):
        return self.score1 == self.score2

    @property
    def winner(self):
        if self.is_draw:
            return None

        if self.score1 is None or self.score2 is None:
            return None

        if self.score1 > self.score2:
            return self.team1

        return self.team2

    @property
    def loser(self):
        if self.is_draw:
            return None

        if self.score1 is None or self.score2 is None:
            return None

        if self.score1 < self.score2:
            return self.team1

        return self.team2

    def has_team(self, team):
        return self.team1 == team or self.team2 == team

    def get_score(self, team):
        if self.team1 == team:
            return self.score1

        if self.team2 == team:
            return self.score2

        return None

    def opponent(self, team):
        if self.team1 == team:
            return self.team2

        if self.team2 == team:
            return self.team1

        return None
