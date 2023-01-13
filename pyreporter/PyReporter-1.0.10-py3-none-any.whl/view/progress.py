from .subject import Subject


# ProgressSubject: Subject used to print out the progress of running the report
class ProgressSubject(Subject):
    def __init__(self):
        super().__init__()
