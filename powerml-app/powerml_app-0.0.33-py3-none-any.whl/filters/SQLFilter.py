from powerml import Filter

class SQLFilter(Filter):
    '''
    This is a class that can be used to filter noise from data for AutocompleteSQLModels.
    '''

    def __init__(self):
        super().__init__('SQL query')