from powerml import Generator
from powerml import WriteEmailModel

class EmailGenerator(Generator):
    '''
    This is a class that can be used to generate more data for WriteEmailModels.
    '''

    def __init__(self, gold_types=['Announcement']):
        super().__init__(gold_types)

    def coverage_generator(self, data, return_metrics=True):
        return super().coverage_generator(data, return_metrics, WriteEmailModel())