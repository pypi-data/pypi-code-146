# Test qa file
from pprint import pprint

def test_qafile():
    """Test qa file load."""
    from fhs_anki_ctrl.qa_file import load_qa_file

    questions = load_qa_file('tests/data/qa_file.txt')
    pprint(questions)

    assert questions[0] == {'a': 'answer 1', 'q': 'question 1'}, "question 1 not identified"
    assert questions[1] == {'a': 'answer 2', 'q': 'multiline\n\nquestion 2\n'}, "question 2 not identified"
    assert questions[2] == {'a': 'single line answer', 'q': 'multiline\nquestion 3\n'}, "question 3 not identified"
