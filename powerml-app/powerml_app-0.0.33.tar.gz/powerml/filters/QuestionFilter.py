from powerml import Filter

class QuestionFilter(Filter):
    '''
    This is a class that can be used to filter noise from data for QuestionAnswerModels.
    '''

    def __init__(self):
        super().__init__('question for students of the lesson')
    
    def _reformat_data(self, data):
        reformatted_data = []
        for datum in data:
            for question in datum['questions']:
                reformatted_data.append({'prompt': f"Lesson: {datum['lesson']}\nAnswer: {datum['answer']}", 'completion': question})
        return reformatted_data
    
    def _reformat_filtered_data(self, data):
        reformatted_data = []
        prev_prompt = None
        questions = []
        for i, datum in enumerate(data):
            if not prev_prompt or prev_prompt == datum['prompt']:
                questions.append(datum['completion'])
                prev_prompt = datum['prompt']
            else:
                lesson, answer = prev_prompt.split('\n')
                reformatted_data.append({'lesson': lesson.split('Lesson: ')[1], 'answer': answer.split('Answer: ')[1], 'questions': questions})
                prev_prompt = datum['prompt']
                questions = [data['completion']]
            if i == len(data) - 1:
                lesson, answer = datum['prompt'].split('\n')
                reformatted_data.append({'lesson': lesson.split('Lesson: ')[1], 'answer': answer.split('Answer: ')[1], 'questions': questions})
        return reformatted_data