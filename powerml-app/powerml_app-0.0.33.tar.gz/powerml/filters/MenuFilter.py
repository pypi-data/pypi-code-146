from powerml import Filter

class MenuFilter(Filter):
    '''
    This is a class that can be used to filter noise from data for ExtractMenuItemsModels.
    '''

    def __init__(self):
        super().__init__('order for the conversation')
    
    def _reformat_data(self, data):
        reformatted_data = []
        for datum in data:
            reformatted_data.append({'prompt': datum['conversation'], 'completion': datum['order']})
        return reformatted_data
    
    def _reformat_filtered_data(self, data):
        reformatted_data = []
        for datum in data:
            reformatted_data.append({'conversation': datum['prompt'], 'order': datum['completion']})
        return reformatted_data