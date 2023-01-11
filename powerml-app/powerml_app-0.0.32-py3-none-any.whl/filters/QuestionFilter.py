from powerml import Filter

class QuestionFilter(Filter):
    '''
    This is a class that can be used to filter noise from data for QuestionAnswerModels.
    '''

    def __init__(self):
        super().__init__('question for students of the lesson')