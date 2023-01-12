from powerml import Filter


class ForecastFilter(Filter):
    '''
    This is a class that can be used to filter noise from data for ForecastSequenceModels.
    '''

    def __init__(self):
        super().__init__('daily revenue forecast that does not include null values')

    def _reformat_data(self, data):
        reformatted_data = []
        for datum in data:
            revenue = ", ".join([str(forecast) for forecast in datum['revenue']])
            reformatted_data.append({'prompt': f"Release Date: {datum['release_date']}\nTitle: {datum['title']}", 'completion': revenue})
        return reformatted_data
    
    def _reformat_filtered_data(self, data):
        reformatted_data = []
        for datum in data:
            release_date, title = datum['prompt'].split('\n')
            revenue = [int(forecast) for forecast in datum['completion'].split(', ')]
            reformatted_data.append({'release_date': release_date.split('Release Date: ')[1], 'title': title.split('Title: ')[1], 'revenue': revenue})
        return reformatted_data
