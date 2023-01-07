class BatchStatus:
    newCount = 0
    completed = 0
    total = 0
    inProgress = 0

    def __init__(self, new_count, in_progress, completed, total):
        self.completed = completed
        self.newCount = new_count
        self.inProgress = in_progress
        self.total = total

    def get_completed(self):
        return self.completed

    def get_total(self):
        return self.total
