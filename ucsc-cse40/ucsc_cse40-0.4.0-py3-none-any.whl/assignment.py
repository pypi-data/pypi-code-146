"""
What is necessary to grade a single assignment.
"""

import datetime

from cse40.question import Question

class Assignment(object):
    """
    A collection of questions to be scored.
    """

    def __init__(self, name, questions):
        self._name = name
        self._questions = questions

        self._grading_start = None
        self._grading_end = None

    def grade(self, submission, additional_data = {}, show_exceptions = False):
        self._grading_start = datetime.datetime.now().isoformat()
        score = 0

        for question in self._questions:
            score += question.grade(submission, additional_data = additional_data,
                show_exceptions = show_exceptions)

        self._grading_end = datetime.datetime.now().isoformat()

        return score

    def get_score(self):
        """
        Return (total score, max score).
        """

        total_score = 0
        max_score = 0

        for question in self._questions:
            total_score += question.score
            max_score += question.max_points

        return (total_score, max_score)

    def report(self, question_prefix = ''):
        """
        Return a string representation of the grading for this assignment.
        """

        output = [
            "Autograder transcript for project: %s." % (self._name),
            "Grading started at %s and ended at %s." % (self._grading_start, self._grading_end)
        ]

        total_score = 0
        max_score = 0

        for question in self._questions:
            total_score += question.score
            max_score += question.max_points

            output.append(question.scoring_report(prefix = question_prefix))

        output.append('')
        output.append("Total: %d / %d" % (total_score, max_score))

        return "\n".join(output)

    def to_dict(self):
        """
        Convert to all simple structures that can be later converted to JSON.
        """

        return {
            'name': self._name,
            'start': self._grading_start,
            'end': self._grading_end,
            'questions': [question.to_dict() for question in self._questions],
        }

    @staticmethod
    def from_dict(data):
        """
        Partner to to_dict().
        Questions constructed with this will not have an implementation for score_question().
        """

        questions = [Question.from_dict(question) for question in data['questions']]
        assignment = Assignment(data['name'], questions)

        assignment._grading_start = data['start']
        assignment._grading_end = data['end']

        return assignment
