from powerml import Filter

class EmailFilter(Filter):
    '''
    This is a class that can be used to filter noise from data for WriteEmailModels.
    '''

    def __init__(self):
        super().__init__('marketing email for the company')