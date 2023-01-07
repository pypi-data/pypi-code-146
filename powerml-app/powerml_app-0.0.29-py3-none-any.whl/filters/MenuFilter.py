from powerml import Filter

class MenuFilter(Filter):
    '''
    This is a class that can be used to filter noise from data for ExtractMenuItemsModels.
    '''

    def __init__(self):
        super().__init__('text-davinci-002', 'order for the conversation')