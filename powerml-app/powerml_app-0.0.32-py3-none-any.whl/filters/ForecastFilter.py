from powerml import Filter


class ForecastFilter(Filter):
    '''
    This is a class that can be used to filter noise from data for ForecastSequenceModels.
    '''

    def __init__(self):
        super().__init__('daily revenue forecast that does not include null values')
