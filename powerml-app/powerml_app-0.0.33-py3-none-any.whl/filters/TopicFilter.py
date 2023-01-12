from powerml import Filter

class TopicFilter(Filter):
    '''
    This is a class that can be used to filter noise from data for CreateTopicsModels.
    '''

    def __init__(self):
        super().__init__('message that discusses one-word system components')