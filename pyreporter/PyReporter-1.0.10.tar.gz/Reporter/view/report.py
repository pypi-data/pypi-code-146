from .subject import Subject

# ReportSubject: Subject used to print out report into all observers
class ReportSubject(Subject):
    def __init__(self):
        super().__init__()
