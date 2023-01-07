from powerml import Filter


class ForecastFilter(Filter):
    '''
    This is a class that can be used to filter noise from data for ForecastSequenceModels.
    '''

    def __init__(self):
        # TODO: figure out a prompt that works
        super().__init__('text-davinci-002', 'daily revenue forecast for the podcast')
