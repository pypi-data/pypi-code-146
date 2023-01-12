from powerml import Filter

class EmailFilter(Filter):
    '''
    This is a class that can be used to filter noise from data for WriteEmailModels.
    '''

    def __init__(self):
        super().__init__('marketing email for the company')

    def _reformat_data(self, data):
        reformatted_data = []
        for datum in data:
            reformatted_data.append({'prompt': datum['subject'], 'completion': datum['email']})
        return reformatted_data
    
    def _reformat_filtered_data(self, data):
        reformatted_data = []
        for datum in data:
            reformatted_data.append({'subject': datum['prompt'], 'email': datum['completion']})
        return reformatted_data